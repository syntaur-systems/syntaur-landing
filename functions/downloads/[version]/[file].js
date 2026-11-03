const EXPECTED_FILENAME = "syntaur-server-windows-x86_64.msi";
const VERSION_REGEX = /^v(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$/;
const ALLOWED_REDIRECT_HOSTS = new Set([
  "release-assets.githubusercontent.com",
  "objects.githubusercontent.com"
]);
const USER_AGENT = "syntaur-download-adapter/1.0";

const ERROR_HEADERS = {
  "Cache-Control": "no-store, no-cache, must-revalidate",
  "Content-Type": "text/plain; charset=utf-8",
  "X-Content-Type-Options": "nosniff"
};

function errorResponse(status, message, extraHeaders = {}) {
  return new Response(message, {
    status,
    headers: {
      ...ERROR_HEADERS,
      ...extraHeaders
    }
  });
}

function cancelBody(res) {
  if (res && res.body && typeof res.body.cancel === "function") {
    res.body.cancel().catch(() => {});
  }
}

export async function onRequest(context) {
  const { request, params } = context;

  if (request.method !== "GET" && request.method !== "HEAD") {
    return errorResponse(405, "Method Not Allowed", { "Allow": "GET, HEAD" });
  }

  const { version, file } = params || {};
  if (typeof version !== "string" || typeof file !== "string") {
    return errorResponse(404, "Not Found");
  }

  if (file !== EXPECTED_FILENAME || !VERSION_REGEX.test(version)) {
    return errorResponse(404, "Not Found");
  }

  const url = new URL(request.url);
  const rawPath = url.pathname;
  if (rawPath.includes("%2f") || rawPath.includes("%2F") || rawPath.includes("..")) {
    return errorResponse(404, "Not Found");
  }

  // Forward one syntactically valid byte range, including suffix ranges.
  let rangeHeader = null;
  const rawRange = request.headers.get("Range");
  if (rawRange !== null) {
    const singleRangeRegex = /^bytes=(?:(\d+)-(\d*)|-(\d+))$/;
    const match = singleRangeRegex.exec(rawRange.trim());
    if (match) {
      const start = Number(match[1]);
      const end = match[2] ? Number(match[2]) : undefined;
      const suffix = match[3] ? Number(match[3]) : undefined;
      if ((suffix !== undefined && Number.isSafeInteger(suffix) && suffix > 0) ||
          (Number.isSafeInteger(start) && (end === undefined || (Number.isSafeInteger(end) && end >= start)))) {
        rangeHeader = match[0];
      }
    }
    if (!rangeHeader) return errorResponse(400, "Invalid Range");
  }

  let targetUrl = `https://github.com/syntaur-systems/syntaur-dist/releases/download/${version}/${EXPECTED_FILENAME}`;
  let redirectsRemaining = 3;
  const visited = new Set();

  while (true) {
    visited.add(targetUrl);

    const upstreamHeaders = {
      "Accept": "application/octet-stream",
      "Accept-Encoding": "identity",
      "User-Agent": USER_AGENT
    };
    if (rangeHeader) {
      upstreamHeaders["Range"] = rangeHeader;
    }

    let upstreamRes;
    try {
      upstreamRes = await fetch(targetUrl, {
        method: request.method,
        headers: upstreamHeaders,
        redirect: "manual"
      });
    } catch {
      return errorResponse(502, "Bad Gateway");
    }

    if ([301, 302, 303, 307, 308].includes(upstreamRes.status)) {
      cancelBody(upstreamRes);
      if (redirectsRemaining <= 0) {
        return errorResponse(502, "Bad Gateway: Too Many Redirects");
      }
      redirectsRemaining -= 1;

      const location = upstreamRes.headers.get("Location") || upstreamRes.headers.get("location");
      if (!location) {
        return errorResponse(502, "Bad Gateway: Missing Redirect Location");
      }

      let parsedLocation;
      try {
        parsedLocation = new URL(location, targetUrl);
      } catch {
        return errorResponse(502, "Bad Gateway: Invalid Redirect URL");
      }

      if (parsedLocation.protocol !== "https:" || parsedLocation.port) {
        return errorResponse(502, "Bad Gateway: Non-HTTPS Redirect");
      }
      if (parsedLocation.username || parsedLocation.password) {
        return errorResponse(502, "Bad Gateway: Userinfo Disallowed");
      }
      if (!ALLOWED_REDIRECT_HOSTS.has(parsedLocation.hostname)) {
        return errorResponse(502, "Bad Gateway: Disallowed Redirect Host");
      }

      const nextUrl = parsedLocation.href;
      if (visited.has(nextUrl)) {
        return errorResponse(502, "Bad Gateway: Redirect Loop");
      }

      targetUrl = nextUrl;
      continue;
    }

    if (upstreamRes.status === 404) {
      cancelBody(upstreamRes);
      return errorResponse(404, "Not Found");
    }

    if (upstreamRes.status === 416) {
      const cr = upstreamRes.headers.get("Content-Range") || upstreamRes.headers.get("content-range");
      cancelBody(upstreamRes);
      const resHeaders = {
        ...ERROR_HEADERS,
        ...(cr ? { "Content-Range": cr } : {})
      };
      return new Response("Requested Range Not Satisfiable", {
        status: 416,
        headers: resHeaders
      });
    }

    if (upstreamRes.status !== 200 && upstreamRes.status !== 206) {
      cancelBody(upstreamRes);
      return errorResponse(502, "Bad Gateway: Upstream Error");
    }

    const contentType = (upstreamRes.headers.get("Content-Type") || "").split(";", 1)[0].trim().toLowerCase();
    if (!["application/octet-stream", "application/x-msi", "application/x-msdownload", "application/x-ole-storage"].includes(contentType)) {
      cancelBody(upstreamRes);
      return errorResponse(502, "Bad Gateway: Invalid Content-Type");
    }

    const contentEncoding = (upstreamRes.headers.get("Content-Encoding") || "identity").trim().toLowerCase();
    if (contentEncoding !== "identity") {
      cancelBody(upstreamRes);
      return errorResponse(502, "Bad Gateway: Unexpected Content-Encoding");
    }

    const responseHeaders = new Headers();
    responseHeaders.set("Content-Type", "application/x-msi");
    responseHeaders.set("Content-Disposition", `attachment; filename="${EXPECTED_FILENAME}"`);
    responseHeaders.set("X-Content-Type-Options", "nosniff");
    responseHeaders.set("Cache-Control", "public, max-age=31536000, immutable");

    const copyHeaders = ["content-length", "content-range", "etag", "last-modified", "accept-ranges"];
    for (const h of copyHeaders) {
      const val = upstreamRes.headers.get(h);
      if (val !== null) {
        if (h === "content-length") responseHeaders.set("Content-Length", val);
        else if (h === "content-range") responseHeaders.set("Content-Range", val);
        else if (h === "etag") responseHeaders.set("ETag", val);
        else if (h === "last-modified") responseHeaders.set("Last-Modified", val);
        else if (h === "accept-ranges") responseHeaders.set("Accept-Ranges", val);
      }
    }

    const body = request.method === "HEAD" ? null : upstreamRes.body;
    if (request.method === "HEAD") {
      cancelBody(upstreamRes);
    }

    return new Response(body, {
      status: upstreamRes.status,
      headers: responseHeaders
    });
  }
}
