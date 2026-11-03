import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const codePath = path.resolve(__dirname, "../functions/downloads/[version]/[file].js");
const code = fs.readFileSync(codePath, "utf8");
const dataUrl = `data:text/javascript;base64,${Buffer.from(code).toString("base64")}`;

const { onRequest } = await import(dataUrl);

const CURRENT_FILE = "syntaur-server-windows-x86_64.msi";
function currentRequest(method = "GET", headers = {}) {
  return {
    request: new Request(`https://syntaur.app/downloads/v0.7.325/${CURRENT_FILE}`, { method, headers }),
    params: { version: "v0.7.325", file: CURRENT_FILE }
  };
}

test("encoded upstream binary is refused instead of changing download bytes", async () => {
  const originalFetch = globalThis.fetch;
  try {
    globalThis.fetch = async () => new Response("zip", { headers: {
      "Content-Type": "application/octet-stream", "Content-Encoding": "gzip", "Content-Length": "3"
    } });
    const response = await onRequest(currentRequest());
    assert.equal(response.status, 502);
    assert.equal(response.headers.get("Content-Length"), null);
  } finally { globalThis.fetch = originalFetch; }
});

test("actual v0.7.325 release and suffix download range remain supported", async () => {
  const originalFetch = globalThis.fetch;
  const calls = [];
  try {
    globalThis.fetch = async (url, init) => {
      calls.push({ url, init });
      return new Response("msi", { headers: { "Content-Type": "application/octet-stream" } });
    };
    assert.equal((await onRequest(currentRequest())).status, 200);
    assert.equal(calls[0].url, `https://github.com/syntaur-systems/syntaur-dist/releases/download/v0.7.325/${CURRENT_FILE}`);
    assert.equal((await onRequest(currentRequest("GET", { Range: "bytes=-500" }))).status, 200);
    assert.equal(calls[1].init.headers.Range, "bytes=-500");
  } finally { globalThis.fetch = originalFetch; }
});

test("malformed, unsafe and multipart ranges fail before any fetch", async () => {
  const originalFetch = globalThis.fetch;
  let calls = 0;
  try {
    globalThis.fetch = async () => { calls++; throw new Error("must not fetch"); };
    for (const Range of ["", "   ", "bytes=10-2", "bytes=0-1,4-5", "bytes=-0", "bytes=9007199254740992-", "items=0-1", "bytes=-"]) {
      assert.equal((await onRequest(currentRequest("GET", { Range }))).status, 400);
    }
    assert.equal(calls, 0);
  } finally { globalThis.fetch = originalFetch; }
});

test("nonstandard redirect ports and unexpected response media are refused", async () => {
  const originalFetch = globalThis.fetch;
  try {
    globalThis.fetch = async () => new Response(null, { status: 302, headers: { Location: "https://objects.githubusercontent.com:444/file.msi" } });
    assert.equal((await onRequest(currentRequest())).status, 502);
    for (const type of ["image/svg+xml", "text/javascript", ""]) {
      globalThis.fetch = async () => new Response("not msi", { headers: { "Content-Type": type } });
      assert.equal((await onRequest(currentRequest())).status, 502);
    }
  } finally { globalThis.fetch = originalFetch; }
});

function createMockFetch(handler) {
  return async (url, init) => {
    return handler(url, init);
  };
}

test("1. normal stream 200 via valid redirect", async () => {
  const originalFetch = globalThis.fetch;
  const recorded = [];
  try {
    globalThis.fetch = createMockFetch((url, init) => {
      recorded.push({ url, init });
      if (url.startsWith("https://github.com/")) {
        return new Response(null, {
          status: 302,
          headers: {
            "Location": "https://objects.githubusercontent.com/github-production-release-asset-2e65be/123/syntaur-server-windows-x86_64.msi"
          }
        });
      }
      return new Response("binary payload bytes", {
        status: 200,
        headers: {
          "Content-Type": "application/octet-stream",
          "Content-Length": "20",
          "ETag": '"abc123etag"',
          "Last-Modified": "Wed, 01 Jan 2026 00:00:00 GMT",
          "Accept-Ranges": "bytes"
        }
      });
    });

    const req = new Request("https://syntaur.app/downloads/v1.2.3/syntaur-server-windows-x86_64.msi", {
      method: "GET"
    });
    const res = await onRequest({
      request: req,
      params: { version: "v1.2.3", file: "syntaur-server-windows-x86_64.msi" }
    });

    assert.equal(res.status, 200);
    assert.equal(res.headers.get("Content-Type"), "application/x-msi");
    assert.equal(res.headers.get("Content-Disposition"), 'attachment; filename="syntaur-server-windows-x86_64.msi"');
    assert.equal(res.headers.get("Cache-Control"), "public, max-age=31536000, immutable");
    assert.equal(res.headers.get("X-Content-Type-Options"), "nosniff");
    assert.equal(res.headers.get("Content-Length"), "20");
    assert.equal(res.headers.get("ETag"), '"abc123etag"');
    assert.equal(res.headers.get("Last-Modified"), "Wed, 01 Jan 2026 00:00:00 GMT");
    assert.equal(res.headers.get("Accept-Ranges"), "bytes");
    const text = await res.text();
    assert.equal(text, "binary payload bytes");
  } finally {
    globalThis.fetch = originalFetch;
  }
});

test("2. HEAD request returns null body with headers and cancels upstream body", async () => {
  const originalFetch = globalThis.fetch;
  let bodyCancelled = false;
  try {
    globalThis.fetch = createMockFetch((url) => {
      const stream = new ReadableStream({
        cancel() {
          bodyCancelled = true;
        }
      });
      return new Response(stream, {
        status: 200,
        headers: {
          "Content-Type": "application/octet-stream",
          "Content-Length": "73015296",
          "ETag": '"e0d1a869676adfd27b12986abe887b818f60deabb2093b2c5f85146511f273ee"'
        }
      });
    });

    const req = new Request("https://syntaur.app/downloads/v1.0.0/syntaur-server-windows-x86_64.msi", {
      method: "HEAD"
    });
    const res = await onRequest({
      request: req,
      params: { version: "v1.0.0", file: "syntaur-server-windows-x86_64.msi" }
    });

    assert.equal(res.status, 200);
    assert.equal(res.body, null);
    assert.equal(res.headers.get("Content-Length"), "73015296");
    assert.equal(bodyCancelled, true);
  } finally {
    globalThis.fetch = originalFetch;
  }
});

test("3. Range request forwarding and 206 response / upstream 416", async () => {
  const originalFetch = globalThis.fetch;
  let forwardedRange = null;
  try {
    globalThis.fetch = createMockFetch((url, init) => {
      forwardedRange = init.headers["Range"];
      return new Response("range bytes", {
        status: 206,
        headers: {
          "Content-Type": "application/octet-stream",
          "Content-Range": "bytes 0-10/73015296",
          "Content-Length": "11"
        }
      });
    });

    const req = new Request("https://syntaur.app/downloads/v2.10.0/syntaur-server-windows-x86_64.msi", {
      method: "GET",
      headers: { "Range": "bytes=0-10" }
    });
    const res = await onRequest({
      request: req,
      params: { version: "v2.10.0", file: "syntaur-server-windows-x86_64.msi" }
    });

    assert.equal(res.status, 206);
    assert.equal(forwardedRange, "bytes=0-10");
    assert.equal(res.headers.get("Content-Range"), "bytes 0-10/73015296");
    assert.equal(res.headers.get("Content-Length"), "11");
    assert.equal(await res.text(), "range bytes");

    // Check upstream 416
    globalThis.fetch = createMockFetch(() => {
      return new Response("range unsatisfiable", {
        status: 416,
        headers: {
          "Content-Range": "bytes */73015296"
        }
      });
    });

    const req416 = new Request("https://syntaur.app/downloads/v2.10.0/syntaur-server-windows-x86_64.msi", {
      method: "GET",
      headers: { "Range": "bytes=99999999-99999999" }
    });
    const res416 = await onRequest({
      request: req416,
      params: { version: "v2.10.0", file: "syntaur-server-windows-x86_64.msi" }
    });
    assert.equal(res416.status, 416);
    assert.equal(res416.headers.get("Content-Range"), "bytes */73015296");
  } finally {
    globalThis.fetch = originalFetch;
  }
});

test("4. Invalid inputs, leading zeroes, bad methods, traversal refusal", async () => {
  // Method 405
  const postReq = new Request("https://syntaur.app/downloads/v1.0.0/syntaur-server-windows-x86_64.msi", {
    method: "POST"
  });
  const resPost = await onRequest({
    request: postReq,
    params: { version: "v1.0.0", file: "syntaur-server-windows-x86_64.msi" }
  });
  assert.equal(resPost.status, 405);
  assert.equal(resPost.headers.get("Allow"), "GET, HEAD");

  // Leading zero in major / minor / patch
  for (const badVer of ["v01.0.0", "v1.02.0", "v1.0.03", "1.0.0", "v1.0.0-beta"]) {
    const res = await onRequest({
      request: new Request(`https://syntaur.app/downloads/${badVer}/syntaur-server-windows-x86_64.msi`),
      params: { version: badVer, file: "syntaur-server-windows-x86_64.msi" }
    });
    assert.equal(res.status, 404);
  }

  // Bad filename
  const resBadFile = await onRequest({
    request: new Request("https://syntaur.app/downloads/v1.0.0/malicious.exe"),
    params: { version: "v1.0.0", file: "malicious.exe" }
  });
  assert.equal(resBadFile.status, 404);

  // Encoded slash / traversal in URL pathname
  const resTraversal = await onRequest({
    request: new Request("https://syntaur.app/downloads/v1.0.0%2f..%2f/syntaur-server-windows-x86_64.msi"),
    params: { version: "v1.0.0", file: "syntaur-server-windows-x86_64.msi" }
  });
  assert.equal(resTraversal.status, 404);
});

test("5. Credential non-forwarding and constant headers", async () => {
  const originalFetch = globalThis.fetch;
  let sentHeaders = null;
  try {
    globalThis.fetch = createMockFetch((url, init) => {
      sentHeaders = init.headers;
      return new Response("ok", {
        status: 200,
        headers: { "Content-Type": "application/octet-stream" }
      });
    });

    const req = new Request("https://syntaur.app/downloads/v1.0.0/syntaur-server-windows-x86_64.msi?token=secret123", {
      method: "GET",
      headers: {
        "Authorization": "Bearer secret_token",
        "Cookie": "session=abc",
        "X-Custom-Auth": "leak_attempt"
      }
    });
    await onRequest({
      request: req,
      params: { version: "v1.0.0", file: "syntaur-server-windows-x86_64.msi" }
    });

    assert.equal(sentHeaders["Authorization"], undefined);
    assert.equal(sentHeaders["Cookie"], undefined);
    assert.equal(sentHeaders["X-Custom-Auth"], undefined);
    assert.equal(sentHeaders["Accept"], "application/octet-stream");
    assert.equal(sentHeaders["Accept-Encoding"], "identity");
    assert.equal(sentHeaders["User-Agent"], "syntaur-download-adapter/1.0");
  } finally {
    globalThis.fetch = originalFetch;
  }
});

test("6. Foreign, insecure, loop, userinfo redirect refusal", async () => {
  const originalFetch = globalThis.fetch;
  try {
    // Foreign host
    globalThis.fetch = createMockFetch(() => new Response(null, {
      status: 302,
      headers: { "Location": "https://evil.attacker.com/malware.msi" }
    }));
    let res = await onRequest({
      request: new Request("https://syntaur.app/downloads/v1.0.0/syntaur-server-windows-x86_64.msi"),
      params: { version: "v1.0.0", file: "syntaur-server-windows-x86_64.msi" }
    });
    assert.equal(res.status, 502);

    // Insecure HTTP
    globalThis.fetch = createMockFetch(() => new Response(null, {
      status: 302,
      headers: { "Location": "http://objects.githubusercontent.com/file.msi" }
    }));
    res = await onRequest({
      request: new Request("https://syntaur.app/downloads/v1.0.0/syntaur-server-windows-x86_64.msi"),
      params: { version: "v1.0.0", file: "syntaur-server-windows-x86_64.msi" }
    });
    assert.equal(res.status, 502);

    // Userinfo in redirect URL
    globalThis.fetch = createMockFetch(() => new Response(null, {
      status: 302,
      headers: { "Location": "https://user:pass@objects.githubusercontent.com/file.msi" }
    }));
    res = await onRequest({
      request: new Request("https://syntaur.app/downloads/v1.0.0/syntaur-server-windows-x86_64.msi"),
      params: { version: "v1.0.0", file: "syntaur-server-windows-x86_64.msi" }
    });
    assert.equal(res.status, 502);

    // Redirect loop
    globalThis.fetch = createMockFetch((url) => {
      return new Response(null, {
        status: 302,
        headers: { "Location": "https://objects.githubusercontent.com/loop" }
      });
    });
    res = await onRequest({
      request: new Request("https://syntaur.app/downloads/v1.0.0/syntaur-server-windows-x86_64.msi"),
      params: { version: "v1.0.0", file: "syntaur-server-windows-x86_64.msi" }
    });
    assert.equal(res.status, 502);
  } finally {
    globalThis.fetch = originalFetch;
  }
});

test("7. Reject upstream HTML / error content types, 404, network failure", async () => {
  const originalFetch = globalThis.fetch;
  try {
    // Upstream HTML error page with 200 status
    globalThis.fetch = createMockFetch(() => new Response("<html><body>Login required</body></html>", {
      status: 200,
      headers: { "Content-Type": "text/html; charset=utf-8" }
    }));
    let res = await onRequest({
      request: new Request("https://syntaur.app/downloads/v1.0.0/syntaur-server-windows-x86_64.msi"),
      params: { version: "v1.0.0", file: "syntaur-server-windows-x86_64.msi" }
    });
    assert.equal(res.status, 502);

    // Upstream 404
    globalThis.fetch = createMockFetch(() => new Response("Not Found", { status: 404 }));
    res = await onRequest({
      request: new Request("https://syntaur.app/downloads/v1.0.0/syntaur-server-windows-x86_64.msi"),
      params: { version: "v1.0.0", file: "syntaur-server-windows-x86_64.msi" }
    });
    assert.equal(res.status, 404);

    // Upstream network failure / fetch throw
    globalThis.fetch = createMockFetch(() => { throw new Error("DNS resolution failed"); });
    res = await onRequest({
      request: new Request("https://syntaur.app/downloads/v1.0.0/syntaur-server-windows-x86_64.msi"),
      params: { version: "v1.0.0", file: "syntaur-server-windows-x86_64.msi" }
    });
    assert.equal(res.status, 502);
  } finally {
    globalThis.fetch = originalFetch;
  }
});
