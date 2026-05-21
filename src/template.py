#!/usr/bin/env python3
"""Generate /home/sean/Desktop/syntaur-landing-preview.html — single-file landing page preview."""
from pathlib import Path

LOGO_B64 = Path("/tmp/syntaur-logo.b64").read_text().strip()

HTML = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Syntaur — Personal AI platform</title>
<meta name="description" content="Personal AI platform — one home for the services people already use. Smart home, finances, scheduling, voice, communications, all under one consistent interface.">
<link rel="icon" type="image/x-icon" href="/favicon.ico">
<link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Syntaur">
<meta property="og:title" content="Syntaur — Personal AI platform">
<meta property="og:description" content="One home for the services people already use. Smart home, finances, scheduling, voice, communications — all under one consistent interface.">
<meta property="og:url" content="https://syntaur.app/">
<meta property="og:image" content="https://syntaur.app/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Syntaur — Personal AI platform">
<meta name="twitter:description" content="One home for the services people already use.">
<meta name="twitter:image" content="https://syntaur.app/og-image.png">
<meta name="theme-color" content="#14554d">
<style>
  :root {{
    --bg: #ffffff;
    --bg-alt: #fafbfc;
    --bg-band: #f6f7f9;
    --text: #1a1a1a;
    --text-muted: #595959;          /* WCAG AA: 4.5:1 against white */
    --text-faint: #6b7280;          /* secondary muted (4.5:1 small-text threshold) */
    --border: #e5e7eb;
    --border-soft: #eef0f3;
    --teal: #14554d;
    --teal-dark: #0e3e38;
    --gold: #8d6800;                /* WCAG AA-passing gold for white backgrounds (~5.15:1) */
    --gold-bright: #d4a017;         /* brighter shade for use only on dark backgrounds */
  }}
  * {{ box-sizing: border-box; }}
  html, body {{
    margin: 0; padding: 0;
    background: var(--bg);
    color: var(--text);
    font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Segoe UI", "Inter", Roboto, sans-serif;
    font-size: 16px;
    line-height: 1.6;
    -webkit-font-smoothing: antialiased;
  }}
  a {{ color: var(--teal); text-decoration: none; }}
  a:hover {{ text-decoration: underline; }}

  .container {{ max-width: 1080px; margin: 0 auto; padding: 0 32px; }}

  /* ----- TOP NAV ----- */
  .nav {{
    position: sticky; top: 0;
    background: rgba(255, 255, 255, 0.92);
    backdrop-filter: blur(12px);
    border-bottom: 1px solid var(--border-soft);
    z-index: 10;
  }}
  .nav-inner {{
    display: flex; align-items: center;
    padding: 18px 32px;
    max-width: 1080px; margin: 0 auto;
  }}
  .nav-brand {{
    display: flex; align-items: center; gap: 12px;
    font-weight: 600; color: var(--teal); font-size: 17px; letter-spacing: 0.3px;
  }}
  .nav-brand img {{ width: 32px; height: 32px; }}
  .nav-links {{
    margin-left: auto; display: flex; gap: 28px;
  }}
  .nav-links a {{ color: var(--text-muted); font-size: 14px; font-weight: 500; }}
  .nav-links a:hover {{ color: var(--teal); text-decoration: none; }}

  /* ----- HERO ----- */
  .hero {{
    padding: 96px 32px 80px;
    text-align: center;
    background:
      radial-gradient(ellipse at 50% 0%, rgba(20, 85, 77, 0.06), transparent 60%);
  }}
  .hero img.logo {{
    width: 132px; height: 132px;
    margin-bottom: 28px;
  }}
  .hero h1 {{
    font-size: 56px;
    line-height: 1.05;
    font-weight: 700;
    letter-spacing: -1px;
    margin: 0 0 16px;
    color: var(--text);
  }}
  .hero h1 .accent {{ color: var(--teal); }}
  .hero .tagline {{
    font-size: 22px;
    color: var(--text-muted);
    font-style: italic;
    max-width: 640px;
    margin: 0 auto 28px;
    line-height: 1.4;
  }}
  .hero .pitch {{
    font-size: 17px;
    color: var(--text);
    max-width: 640px;
    margin: 0 auto;
    line-height: 1.6;
  }}
  .hero .pitch strong {{ color: var(--teal-dark); }}

  /* ----- SECTION SHARED ----- */
  section {{ padding: 96px 0; }}
  section.alt {{ background: var(--bg-band); }}
  section h2 {{
    font-size: 36px;
    font-weight: 700;
    letter-spacing: -0.5px;
    margin: 0 0 16px;
    color: var(--text);
  }}
  section .lede {{
    font-size: 18px;
    color: var(--text-muted);
    max-width: 720px;
    margin: 0 0 48px;
    line-height: 1.6;
  }}
  section .eyebrow {{
    color: var(--gold);
    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    font-weight: 700;
    margin-bottom: 12px;
  }}

  /* ----- ABOUT ----- */
  .about-grid {{
    display: grid;
    grid-template-columns: 1.2fr 1fr;
    gap: 64px;
    align-items: start;
  }}
  .about-grid p {{
    font-size: 17px;
    color: var(--text);
    line-height: 1.7;
    margin: 0 0 20px;
  }}
  .about-grid p.muted {{ color: var(--text-muted); font-size: 16px; }}
  .about-grid .sidebar {{
    background: var(--bg);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 28px;
  }}
  .about-grid .sidebar h3 {{
    font-size: 14px;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: var(--teal);
    margin: 0 0 16px;
  }}
  .about-grid .sidebar ul {{
    margin: 0; padding: 0; list-style: none;
  }}
  .about-grid .sidebar li {{
    padding: 10px 0;
    border-bottom: 1px solid var(--border-soft);
    color: var(--text);
    font-size: 14.5px;
  }}
  .about-grid .sidebar li:last-child {{ border-bottom: none; }}
  .about-grid .sidebar li b {{ color: var(--teal-dark); }}

  /* ----- MEMORY SECTION ----- */
  .memory-grid {{
    display: grid;
    grid-template-columns: 1.1fr 1fr;
    gap: 48px;
    align-items: start;
  }}
  .memory-narrative p {{
    font-size: 17px;
    color: var(--text);
    line-height: 1.7;
    margin: 0 0 18px;
  }}
  .memory-narrative p.muted {{ color: var(--text-muted); font-size: 16px; }}
  .memory-card {{
    background: linear-gradient(155deg, #ffffff 0%, #f6f7f9 100%);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 32px 28px;
    box-shadow: 0 8px 28px rgba(20, 85, 77, 0.06);
    position: relative;
    overflow: hidden;
  }}
  .memory-card::before {{
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, var(--teal) 0%, var(--gold-bright) 100%);
  }}
  .memory-card-header {{
    display: flex; align-items: center; gap: 10px;
    font-size: 13px; text-transform: uppercase; letter-spacing: 1px;
    color: var(--teal); font-weight: 700;
    margin-bottom: 18px;
  }}
  .memory-pulse {{
    display: inline-block; width: 9px; height: 9px; border-radius: 50%;
    background: var(--gold-bright);
    box-shadow: 0 0 0 0 rgba(212, 160, 23, 0.6);
    animation: memory-pulse 2.4s ease-out infinite;
  }}
  @keyframes memory-pulse {{
    0%   {{ box-shadow: 0 0 0 0 rgba(212, 160, 23, 0.6); }}
    70%  {{ box-shadow: 0 0 0 10px rgba(212, 160, 23, 0); }}
    100% {{ box-shadow: 0 0 0 0 rgba(212, 160, 23, 0); }}
  }}
  @media (prefers-reduced-motion: reduce) {{
    .memory-pulse {{ animation: none; }}
    .module, .partners-card .cta {{ transition: none; }}
  }}
  .memory-card-intro {{
    margin: 0 0 18px;
    color: var(--text-muted);
    font-size: 14.5px;
  }}
  .memory-list {{
    margin: 0; padding: 0; list-style: none;
  }}
  .memory-list li {{
    padding: 12px 0;
    border-bottom: 1px solid var(--border-soft);
    color: var(--text);
    font-size: 14.5px;
    line-height: 1.55;
  }}
  .memory-list li:last-child {{ border-bottom: none; }}
  .memory-list li b {{ color: var(--teal-dark); }}
  .memory-card-footer {{
    margin: 20px 0 0;
    padding-top: 18px;
    border-top: 1px solid var(--border-soft);
    color: var(--text-muted);
    font-size: 14px;
    font-style: italic;
    line-height: 1.55;
  }}

  /* ----- MODULES GRID ----- */
  .modules {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 24px;
  }}
  .module {{
    background: var(--bg);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 32px 28px;
    transition: all 0.18s ease;
  }}
  .module:hover {{
    transform: translateY(-2px);
    border-color: var(--teal);
    box-shadow: 0 8px 24px rgba(20, 85, 77, 0.08);
  }}
  .module .label {{
    display: inline-block;
    background: rgba(20, 85, 77, 0.07);
    color: var(--teal);
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.8px;
    text-transform: uppercase;
    padding: 4px 10px;
    border-radius: 4px;
    margin-bottom: 14px;
  }}
  .module h3 {{
    font-size: 19px;
    margin: 0 0 10px;
    color: var(--text);
    font-weight: 600;
  }}
  .module p {{
    margin: 0;
    color: var(--text-muted);
    font-size: 14.5px;
    line-height: 1.55;
  }}

  /* ----- PARTNERS ----- */
  .partners-card {{
    background: linear-gradient(135deg, var(--teal) 0%, var(--teal-dark) 100%);
    color: #ffffff;
    border-radius: 16px;
    padding: 64px;
    text-align: center;
  }}
  .partners-card .eyebrow {{ color: var(--gold-bright); }}  /* on dark teal, use the brighter shade */
  .partners-card h2 {{ color: #ffffff; }}
  .partners-card p {{
    color: rgba(255, 255, 255, 0.85);
    max-width: 640px;
    margin: 0 auto 32px;
    font-size: 17px;
    line-height: 1.6;
  }}
  .partners-card .cta {{
    display: inline-flex;
    align-items: center;
    gap: 10px;
    background: #ffffff;
    color: var(--teal-dark);
    padding: 14px 26px;
    border-radius: 8px;
    font-weight: 600;
    font-size: 15px;
    transition: transform 0.15s ease;
  }}
  .partners-card .cta:hover {{ transform: translateY(-1px); text-decoration: none; }}
  .partners-card .cta-sub {{
    margin-top: 18px;
    color: rgba(255, 255, 255, 0.7);
    font-size: 13px;
  }}

  /* ----- FOOTER ----- */
  footer {{
    background: var(--text);
    color: rgba(255, 255, 255, 0.7);
    padding: 64px 32px 32px;
    margin-top: 80px;
  }}
  footer .footer-inner {{
    max-width: 1080px;
    margin: 0 auto;
    display: grid;
    grid-template-columns: 1.5fr 1fr 1fr;
    gap: 48px;
  }}
  footer .col h4 {{
    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: 1.2px;
    color: rgba(255, 255, 255, 0.5);
    margin: 0 0 14px;
    font-weight: 600;
  }}
  footer .brand {{ display: flex; align-items: flex-start; gap: 16px; }}
  footer .brand img {{ width: 48px; height: 48px; }}
  footer .brand .wordmark {{ font-size: 20px; font-weight: 600; color: #ffffff; letter-spacing: 0.4px; }}
  footer .brand .sub {{ font-size: 14px; color: rgba(255, 255, 255, 0.55); margin-top: 4px; max-width: 280px; line-height: 1.5; }}
  footer .col ul {{ list-style: none; margin: 0; padding: 0; }}
  footer .col li {{ padding: 6px 0; font-size: 14px; }}
  footer .col a {{ color: rgba(255, 255, 255, 0.7); }}
  footer .col a:hover {{ color: #ffffff; text-decoration: none; }}
  footer .col p {{ margin: 0 0 8px; color: rgba(255, 255, 255, 0.7); font-size: 14px; }}
  footer .legal {{
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    margin-top: 48px;
    padding-top: 24px;
    font-size: 12.5px;
    color: rgba(255, 255, 255, 0.4);
    text-align: center;
  }}

  /* ----- REVIEW NOTES BANNER (only in preview file) ----- */
  .review-banner {{
    background: #fffbe6;
    border-left: 4px solid var(--gold);
    color: #5b4a00;
    padding: 18px 28px;
    font-size: 14px;
    line-height: 1.55;
  }}
  .review-banner h3 {{ margin: 0 0 8px; font-size: 14px; color: #5b4a00; }}
  .review-banner ul {{ margin: 4px 0 0 18px; padding: 0; }}
  .review-banner li {{ margin-bottom: 4px; }}

  /* ----- MOBILE ----- */
  @media (max-width: 820px) {{
    .nav-links {{ gap: 14px; font-size: 13px; }}
    .nav-links a {{ font-size: 13px; }}
    .nav-inner {{ flex-wrap: wrap; padding: 14px 16px; gap: 10px; }}
    .hero {{ padding: 64px 24px 48px; }}
    .hero h1 {{ font-size: 38px; }}
    .hero .tagline {{ font-size: 18px; }}
    .about-grid {{ grid-template-columns: 1fr; gap: 32px; }}
    .memory-grid {{ grid-template-columns: 1fr; gap: 32px; }}
    .modules {{ grid-template-columns: 1fr; gap: 16px; }}
    .partners-card {{ padding: 40px 24px; }}
    footer .footer-inner {{ grid-template-columns: 1fr; gap: 32px; }}
    section h2 {{ font-size: 28px; }}
  }}
</style>
</head>
<body>

<div class="review-banner">
  <h3>Review notes for Sean (this banner is preview-only and will be removed before deploy)</h3>
  <ul>
    <li><b>Design language</b>: matches the email — teal #14554d primary, warm gold #d4a017 accent, system-UI fonts, light background. Visually consistent with what a partner just received in their inbox.</li>
    <li><b>Five sections</b>: nav → hero → about → modules grid → partners CTA → footer. Single page, mobile-responsive.</li>
    <li><b>No GitHub link</b> — your github account is <code>buddyholly007</code>, which reads as personal. For B2B credibility, leaving GitHub off until you have a <code>github.com/syntaur-systems</code> org. Easy to add later. (If you want to override and link to <code>buddyholly007</code> now, I will.)</li>
    <li><b>Modules</b>: I picked 6 — Smart Home &amp; Network, Tax &amp; Finance, Scheduler, Voice &amp; Pendant, Privacy &amp; Security, Engine. Each gets a 1-line pitch. Names and descriptions are tunable; the labels (BETA / SHIPPED / etc) are placeholders.</li>
    <li><b>Partners CTA</b>: solid teal card to draw the eye, directly addresses the "are you a potential integration partner?" question, points to <code>partnerships@syntaur.app</code> — which is exactly the email address the e-file outreach uses, so anyone arriving from that email lands here and sees the same address echoed.</li>
    <li><b>No physical address shown on page</b>: Olympia, WA in footer only. We can adjust per your earlier "home address vs not" decision.</li>
    <li><b>What this preview does NOT include</b>: a "Login" button (no user accounts yet), pricing (no public pricing model decided), customer logos / testimonials (don't have them), animations (skipping for first iteration).</li>
  </ul>
</div>

<nav class="nav">
  <div class="nav-inner">
    <a href="#" class="nav-brand">
      <img src="data:image/png;base64,{LOGO_B64}" alt="">
      <span>Syntaur</span>
    </a>
    <div class="nav-links">
      <a href="#about">About</a>
      <a href="#memory">Memory</a>
      <a href="#modules">Modules</a>
      <a href="#partners">Partners</a>
      <a href="mailto:partnerships@syntaur.app">Contact</a>
    </div>
  </div>
</nav>

<section class="hero">
  <img class="logo" src="data:image/png;base64,{LOGO_B64}" alt="Syntaur">
  <h1>One home for everything <span class="accent">personal&nbsp;AI</span> should be.</h1>
  <div class="tagline">Personal AI platform — built so your daily services finally live under one roof.</div>
  <div class="pitch">
    Smart home, finances, scheduling, voice, communications — most people stitch these together across a dozen apps and accounts.
    <strong>Syntaur consolidates them.</strong> One interface, one identity, one place where your AI can actually be useful.
  </div>
</section>

<section id="about" class="alt">
  <div class="container">
    <div class="eyebrow">About Syntaur</div>
    <h2>Built for people, not for vendors.</h2>
    <div class="lede">Syntaur exists because personal AI shouldn't mean fragmenting your life across services that don't talk to each other.</div>

    <div class="about-grid">
      <div>
        <p>Every module Syntaur ships — smart home, tax preparation, scheduling, voice, communications — is designed around the same operating principle: <em>your data, your devices, your choice of partners, all in one place</em>.</p>
        <p class="muted">We build pure-Rust services that run on infrastructure you control. We integrate with established providers where the regulated industries require it (tax filing, payment processing, e-file submission), and we act as the intermediary that brings their service to you without standing between you and them.</p>
        <p class="muted">We don't sell your data. We don't lock you into our cloud. We don't mark up the services we route to. We just make personal AI feel like it should.</p>
      </div>

      <div class="sidebar">
        <h3>Operating Principles</h3>
        <ul>
          <li><b>Local-first.</b> Your home runs on your gateway, not our cloud.</li>
          <li><b>Pure Rust.</b> Every service we own is Rust. No proxy languages.</li>
          <li><b>Pass-through partnerships.</b> Third-party services are routed at cost.</li>
          <li><b>Open by design.</b> Standards-based (Matter, MQTT, IMAP, etc.) — not proprietary lock-in.</li>
          <li><b>One identity.</b> You sign in once, everywhere.</li>
        </ul>
      </div>
    </div>
  </div>
</section>

<section id="memory">
  <div class="container">
    <div class="eyebrow">What makes Syntaur different</div>
    <h2>An AI that actually remembers you.</h2>
    <div class="lede">Most personal AI starts every session from scratch. Syntaur doesn't — and where we're heading goes much further than where the industry is today.</div>

    <div class="memory-grid">
      <div class="memory-narrative">
        <p><b>What's shipped today.</b> Every Syntaur module is backed by a persistent, structured memory vault. It's human-readable, lives in a format you can audit and edit yourself, and survives across sessions — so conversations build on what came before instead of resetting each morning.</p>
        <p class="muted">Memories are written deliberately, not vacuumed up. They're organized by topic and tagged for retrieval, so relevant history surfaces when it's actually useful — not as a fire hose of "things you said three months ago."</p>
        <p class="muted">This already changes the daily experience: your home agent remembers which devices misbehave, your scheduler remembers what you've committed to, your finance agent remembers the context behind decisions you made months ago.</p>
      </div>

      <div class="memory-card">
        <div class="memory-card-header">
          <span class="memory-pulse"></span>
          In active development — a preview
        </div>
        <p class="memory-card-intro">We're building the next layer right now. A sneak peek at what's coming:</p>
        <ul class="memory-list">
          <li><b>Self-curating memory.</b> A layer that learns what's worth remembering without being told, and lets irrelevant context fade on its own.</li>
          <li><b>Per-module character development.</b> Each module's AI grows its own personality, vocabulary, and rapport with you over time.</li>
          <li><b>Cross-module recall.</b> Something noted in one module surfaces in another when it's relevant — even if you didn't ask.</li>
          <li><b>Episode memory.</b> The system remembers struggles, decisions, and the stories behind them — not just facts.</li>
        </ul>
        <p class="memory-card-footer">This is what we mean when we say <em>personal</em> AI. Not an assistant that forgets. A system that becomes more useful the longer you have it.</p>
      </div>
    </div>
  </div>
</section>

<section id="modules" class="alt">
  <div class="container">
    <div class="eyebrow">Capabilities</div>
    <h2>Modules across the surfaces of daily life.</h2>
    <div class="lede">Each module is built to stand on its own and to compose with the others — all of them sharing the memory layer above.</div>

    <div class="modules">
      <div class="module">
        <span class="label">Smart Home</span>
        <h3>Devices &amp; networks</h3>
        <p>Multi-protocol device control across Matter, Thread, BLE, MQTT, and vendor APIs. Pure-Rust gateway, no vendor cloud dependencies.</p>
      </div>
      <div class="module">
        <span class="label">Tax &amp; Finance</span>
        <h3>Year-round tax picture</h3>
        <p>Continuous bookkeeping, document organization, and prepared filings — routed through authorized e-file partners at pass-through cost.</p>
      </div>
      <div class="module">
        <span class="label">Scheduler</span>
        <h3>Calendar, tasks, habits</h3>
        <p>One coherent view of meetings, todos, and habits across personal and shared calendars. Voice and photo intake.</p>
      </div>
      <div class="module">
        <span class="label">Voice</span>
        <h3>Pendant &amp; conversation</h3>
        <p>Local speech-to-text and AI assistance via a Bluetooth pendant or your phone. Designed for hands-free interaction throughout the day.</p>
      </div>
      <div class="module">
        <span class="label">Privacy</span>
        <h3>Defense in depth</h3>
        <p>Per-device privacy policies, DNS sinkhole, and network segmentation for the smart devices in your home that shouldn't phone home.</p>
      </div>
      <div class="module">
        <span class="label">Engine</span>
        <h3>The platform underneath</h3>
        <p>The pure-Rust runtime — vault, scheduler, browser engine, and message broker — that every Syntaur module is built on.</p>
      </div>
    </div>
  </div>
</section>

<section id="partners" class="alt">
  <div class="container">
    <div class="partners-card">
      <div class="eyebrow">For partners</div>
      <h2>Are you a service Syntaur should integrate with?</h2>
      <p>We work with API partners across tax, finance, smart home, scheduling, and more — wherever regulated infrastructure or established expertise means it's better to integrate than rebuild. We pass your service through to our users at cost; you keep the full per-customer economics and the regulated relationship.</p>
      <a href="mailto:partnerships@syntaur.app" class="cta">
        partnerships@syntaur.app →
      </a>
      <div class="cta-sub">We reply to every inquiry. No automated funnels.</div>
    </div>
  </div>
</section>

<footer>
  <div class="footer-inner">
    <div class="col">
      <div class="brand">
        <img src="data:image/png;base64,{LOGO_B64}" alt="">
        <div>
          <div class="wordmark">Syntaur</div>
          <div class="sub">Personal AI platform built so your daily services finally live under one roof.</div>
        </div>
      </div>
    </div>
    <div class="col">
      <h4>Contact</h4>
      <ul>
        <li><a href="mailto:hello@syntaur.app">hello@syntaur.app</a></li>
        <li><a href="mailto:partnerships@syntaur.app">partnerships@syntaur.app</a></li>
        <li><a href="mailto:support@syntaur.app">support@syntaur.app</a></li>
      </ul>
    </div>
    <div class="col">
      <h4>Syntaur Systems</h4>
      <p>Olympia, Washington</p>
      <p>United States</p>
    </div>
  </div>
  <div class="legal">© 2026 Syntaur Systems. All rights reserved.</div>
</footer>

</body>
</html>
"""

Path("/home/sean/Desktop/syntaur-landing-preview.html").write_text(HTML)
print(f"wrote {len(HTML)} bytes")
