from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

NAV = """<nav class="navbar site-header" data-component="site-header" aria-label="Primary navigation"><div class="nav-container site-header__container"><a href="../index.html" class="nav-brand site-brand" data-component="site-brand"><span class="brand-name">EdenTV</span><span class="tagline site-brand__tagline">Creator Studio</span></a><div id="primary-navigation" class="nav-menu site-nav" data-component="site-nav"><a href="../index.html" class="nav-link site-nav__link">Home</a><a href="../pages/apps.html" class="nav-link site-nav__link">Apps</a><a href="../pages/podcasts.html" class="nav-link site-nav__link">Podcasts</a><a href="../pages/multimedia.html" class="nav-link site-nav__link">Multimedia</a><a href="../pages/developer-docs.html" class="nav-link site-nav__link active">Documents &amp; Support</a><a href="../pages/about.html" class="nav-link site-nav__link">About</a></div><button type="button" class="nav-toggle site-nav__toggle" data-component="site-nav-toggle" aria-label="Open navigation menu" aria-controls="primary-navigation" aria-expanded="false"><span></span><span></span><span></span></button></div></nav>"""

FOOTER = """<footer class="footer site-footer" data-component="site-footer"><div class="container"><div class="footer-content site-footer__content"><div class="footer-brand site-footer__brand"><h3>EdenTV</h3><p>Creating thoughtful digital experiences.</p></div><div class="footer-links site-footer__links"><div class="footer-section site-footer__section"><h4>Documentation</h4><a href="privacy-policy.html">Privacy</a><a href="terms-of-service.html">Terms</a><a href="app-store-compliance.html">App Store review</a><a href="support.html">Support</a></div></div></div><div class="footer-bottom site-footer__bottom"><p>&copy; 2026 EdenTV. All rights reserved.</p></div></div></footer>"""

PAGES = {
    "privacy-policy.html": (
        "Privacy index", "Privacy notices by product", "Choose the notice for the product you use. Product notices describe the data handled by that product and the services involved.",
        [("PulseTrackr", "Community reports, evidence, account data, location, and trusted-contact SOS.", "../docs/pulsetrackr-privacy.html"), ("JxL Scheduler", "On-device schedules, routes, messages, uploads, and optional iCloud sharing.", "../docs/jxl-scheduler-privacy.html"), ("ParkMemory Hub", "Local memories, plans, circle membership, and optional CloudKit sharing.", "../docs/parkmemory-privacy.html")]
    ),
    "terms-of-service.html": (
        "Terms index", "Terms by product", "Public user agreements are maintained at product level so their wording follows the current software model.",
        [("PulseTrackr", "Terms for community safety reports, user content, SOS messaging, and service limits.", "../docs/pulsetrackr-terms.html"), ("ParkMemory Hub", "Terms for private circles, shared memories, plans, and acceptable use.", "../docs/parkmemory-terms.html")]
    ),
    "app-store-compliance.html": (
        "App Store review", "Review references by product", "Release notes describe current behavior for reviewers. They are operational references, not consumer promises or legal advice.",
        [("PulseTrackr", "Review URLs, feature scope, privacy permissions, safety positioning, and review notes.", "../docs/pulsetrackr-compliance.html"), ("JxL Scheduler", "Local-first behavior, optional CloudKit sharing, permissions, and review notes.", "../docs/jxl-scheduler-compliance.html"), ("ParkMemory Hub", "CloudKit circle sharing, user content, permissions, and review notes.", "../docs/parkmemory-compliance.html")]
    ),
    "support.html": (
        "Product support", "Help by product", "Open the guide that matches your app. For unresolved issues, email support@edentv.us and include the product name, device model, OS version, and a short description.",
        [("PulseTrackr", "Setup, permissions, reports, map and feed, SOS, and troubleshooting.", "../docs/pulsetrackr-support.html"), ("JxL Scheduler", "Schedules, routes, messages, uploads, location, and iCloud sharing.", "../docs/jxl-scheduler-support.html"), ("ParkMemory Hub", "Circle invites, permissions, memories, planner, radar, and iCloud sync.", "../docs/parkmemory-support.html")]
    ),
}

for filename, (eyebrow, title, intro, rows) in PAGES.items():
    items = "".join(f'<a class="document-row" href="{href}" role="listitem"><span><strong>{name}</strong><small>{description}</small></span><span aria-hidden="true">→</span></a>' for name, description, href in rows)
    contact = '<p class="docs-contact-note">Contact <a href="mailto:support@edentv.us">support@edentv.us</a> for product help or <a href="mailto:legal@edentv.us">legal@edentv.us</a> for policy questions.</p>'
    html = f'''<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>{title} - EdenTV</title><meta name="description" content="{intro}"><link rel="stylesheet" href="../css/styles.css?v=20260905"><link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet"><link rel="icon" type="image/svg+xml" href="../assets/brand/etv-favicon.svg"></head><body class="page-docs">{NAV}<header class="docs-index-hero"><div class="container narrow"><p class="eyebrow ds-eyebrow">{eyebrow}</p><h1>{title}.</h1><p>{intro}</p>{contact}</div></header><main class="docs-index"><section class="docs-index-section"><div class="container docs-index-layout"><div class="docs-index-heading"><p class="eyebrow ds-eyebrow">Current documents</p><h2>Choose a product</h2><p>Reviewed August 23, 2026. Product behavior can differ, so use the matching document.</p></div><div class="document-index" role="list">{items}</div></div></section></main>{FOOTER}<script src="../js/script.js"></script></body></html>'''
    (ROOT / "legal" / filename).write_text(html + "\n")
