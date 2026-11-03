# syntaur-landing

Source for the **Syntaur** landing page at **https://syntaur.app**.

Single-page site deployed to Cloudflare Pages with a custom domain at the apex of the syntaur.app zone. The page is generated from a Python template (`src/template.py`) that bakes in design tokens, content, and a watermark-removed transparent PNG logo.

## Layout

```
.
├── index.html              # Deployed page (no build step required)
├── logo.png                # Brand mark (transparent PNG)
├── favicon.ico             # Multi-resolution favicon
├── favicon-16x16.png       # 16×16
├── favicon-32x32.png       # 32×32
├── apple-touch-icon.png    # 180×180 for iOS
├── og-image.png            # 1200×630 social card
├── robots.txt              # Crawl rules + sitemap pointer
├── sitemap.xml             # Search engine sitemap
├── _routes.json            # Cloudflare Pages routing rule: invoke functions only for /downloads/*
├── functions/              # Cloudflare Pages Functions adapter
│   └── downloads/
│       └── [version]/
│           └── [file].js   # Streaming download adapter for Microsoft Store
├── tests/                  # Node builtin mock fetch tests
│   └── downloads.test.mjs
└── src/
    └── template.py         # Generator that emits index.html
```

## Direct Downloads Adapter

A direct-download adapter is provided for distribution channels such as the Microsoft Store, which require a direct 200/206 streaming endpoint rather than a 302 redirect to GitHub Releases:

- **Route**: `GET /downloads/v0.7.325/syntaur-server-windows-x86_64.msi` (and `HEAD`)
- **Authority**: GitHub Releases remains the sole source of truth and authority for release assets (`github.com/syntaur-systems/syntaur-dist/releases/download/v0.7.325/syntaur-server-windows-x86_64.msi`).
- **Binary Integrity**: The v0.7.325 origin artifact has SHA-256 `e0d1a869676adfd27b12986abe887b818f60deabb2093b2c5f85146511f273ee` (73,015,296 bytes). The adapter streams it without transformation or buffering; the delivered bytes must be checked after deployment. It does not add a signing authority or perform runtime signature verification.
- **Routing**: `_routes.json` limits function execution to `/downloads/*`; existing static marketing pages do not invoke this function.
- **Checks**: `node --test tests/downloads.test.mjs` runs the mocked HTTP tests. Deploy through the existing GitHub Actions workflow on `main`, then verify a direct HTTP 200, the full downloaded hash, and a partial download before using the URL in Partner Center.

## Deploy

The site is deployed via [Cloudflare Pages](https://pages.cloudflare.com/) with the project name `syntaur` in the Cloudflare account that owns the `syntaur.app` domain.

```bash
# One-time: install wrangler
npx --yes wrangler@latest --version

# Deploy from the repo root
export CLOUDFLARE_API_TOKEN=<token-with-pages-edit-and-dns-edit-scopes>
export CLOUDFLARE_ACCOUNT_ID=<account-id>
npx wrangler pages deploy . --project-name=syntaur --branch=main
```

Cloudflare automatically:
- Provisions an SSL certificate (Google CA, free, auto-renewing)
- Routes apex + `www.syntaur.app` to the deployment via CNAME flattening at the proxied zone
- Pushes the site to its global edge

## Local preview

`index.html` is fully self-contained (logo + favicons + OG image referenced as relative paths). Open it directly in a browser — no dev server needed.

## License

Proprietary — © 2026 Syntaur Systems, all rights reserved. The repo is
public so the site can be inspected and deployed transparently, but it
is not open source; see [LICENSE](LICENSE). (Syntaur itself is also
proprietary, closed-source software.)
