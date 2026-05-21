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
└── src/
    └── template.py         # Generator that emits index.html
```

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

MIT.
