from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

GROUPS = [
    ("apple", "Apple platforms", "Native projects found in the current Codehub workspace.", [
        ("ParkMemory Hub", "Current build", "A local-first iPhone app for private trip circles, shared memories, plans, voting, and optional location updates through CloudKit.", ["SwiftUI", "CloudKit", "iOS 18+"]),
        ("JxL Scheduler", "In development", "A local-first iPhone logistics app for schedules, routes, messages, uploads, and optional group sharing through iCloud.", ["SwiftUI", "SwiftData", "CloudKit"]),
        ("PulseTrackr", "Release preparation", "An iPhone community-safety app for incident reports, map awareness, evidence capture, verification signals, and trusted-contact SOS.", ["SwiftUI", "Firebase", "iOS 18+"]),
        ("Cosmix", "Desktop build", "A real-time macOS audio visualizer with particle, waveform, and circular modes driven by microphone FFT analysis.", ["SwiftUI", "AVFoundation", "Accelerate"]),
        ("Kasapa", "Prototype · milestone 3", "A privacy-first professional-networking prototype with exact sharing grants, local messaging, block/report controls, and on-device persistence.", ["SwiftUI", "Local-first", "iOS"]),
    ]),
    ("mobile", "Android", "The Android project currently represented in the local workspace.", [
        ("MoodQuest", "Prototype", "A mood-based adventure planner with optional nearby suggestions, custom activities, history, and offline Room persistence.", ["Kotlin", "Jetpack Compose", "Room"]),
    ]),
    ("web", "Web products", "Full-stack and browser projects with corresponding local source directories.", [
        ("PulseTrack", "Live", "A React and Firebase platform tracking Nigerian political sentiment, with maps, charts, submissions, and a scheduled Python NLP pipeline.", ["React", "TypeScript", "Firebase"]),
        ("LxRose", "Live", "A domain-aware healthcare website and protected operations dashboard backed by Firebase Functions and an Express API.", ["React", "Express", "Firebase"]),
        ("Wayfare", "Controlled rollout", "A mobile-first driver earnings ledger and payout-request system. It records work and payouts but does not move or hold money.", ["React", "Firestore", "Cloud Functions"]),
        ("Crystal Heart", "Live", "A private matchmaking application on Cloudflare Workers with a public applicant flow and a separately protected staff review workspace.", ["Cloudflare Workers", "D1", "Access"]),
        ("Upskill Institute", "Web platform", "A Flask learning platform with authentication, course and module progress, career recommendations, and Paystack enrollment.", ["Flask", "PostgreSQL", "Paystack"]),
        ("Guess Correctly", "Web game", "A responsive Halloween memory game with single-player and two-player real-time Firebase modes.", ["JavaScript", "Firebase", "HTML/CSS"]),
        ("Miriam’s Corner", "Editorial site", "A static Australian travel and lifestyle publication with destination pages, stories, and responsive layouts.", ["HTML", "CSS", "JavaScript"]),
    ]),
    ("tools", "AI, data, and design tools", "Local research tools, data applications, and reusable design-system work.", [
        ("Autobiz", "In development", "A source-backed business-listing research tool that deduplicates, scores, verifies, and ranks acquisition opportunities.", ["Python", "Multi-agent", "Data pipeline"]),
        ("Autoresearch for macOS", "Research fork", "An Apple Silicon adaptation of the autonomous LLM experiment loop, with fixed-time training and MPS support.", ["Python", "PyTorch", "Apple Silicon"]),
        ("Philly Real Estate Tracker", "Data application", "A Southeast Philadelphia property-trend explorer built from local data-processing and application code.", ["Python", "Pandas", "SQLite"]),
        ("Blockchain Transfer Simulation", "Learning prototype", "An interactive proof-of-work and transfer simulation intended for technical exploration rather than financial use.", ["Python", "Streamlit", "Simulation"]),
        ("Lumina Codex", "Published system", "A portable cross-medium design system and immersive portfolio prototype, distributed as @xlumina/system.", ["React", "Three.js", "Design system"]),
    ]),
]

def card(project):
    name, status, description, tags = project
    tag_html = "".join(f'<span class="tech-badge">{tag}</span>' for tag in tags)
    return f'<article class="project-card ds-card"><div class="project-label">{status}</div><h3>{name}</h3><p>{description}</p><div class="project-tags">{tag_html}</div></article>'

sections = "".join(f'<section id="{slug}" class="section site-section category-section"><div class="container"><div class="category-header"><div><p class="eyebrow ds-eyebrow">Verified locally</p><h2>{title}.</h2><p>{intro}</p></div></div><div class="project-grid">{"".join(card(p) for p in projects)}</div></div></section>' for slug, title, intro, projects in GROUPS)

html = f'''<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Apps & Projects - EdenTV Creator Studio</title><meta name="description" content="A source-verified selection of native apps, web platforms, AI tools, and design systems in the EdenTV Codehub workspace."><link rel="stylesheet" href="../css/styles.css?v=20260823b"><link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet"><link rel="icon" type="image/svg+xml" href="../assets/brand/etv-favicon.svg"></head>
<body class="page-apps"><nav class="navbar site-header" data-component="site-header" aria-label="Primary navigation"><div class="nav-container site-header__container"><a href="../index.html" class="nav-brand site-brand" data-component="site-brand"><span class="brand-name">EdenTV</span><span class="tagline site-brand__tagline">Creator Studio</span></a><div id="primary-navigation" class="nav-menu site-nav" data-component="site-nav"><a href="../index.html" class="nav-link site-nav__link">Home</a><a href="apps.html" class="nav-link site-nav__link active">Apps</a><a href="podcasts.html" class="nav-link site-nav__link">Podcasts</a><a href="multimedia.html" class="nav-link site-nav__link">Multimedia</a><a href="developer-docs.html" class="nav-link site-nav__link">Developer Docs</a><a href="about.html" class="nav-link site-nav__link">About</a></div><button type="button" class="nav-toggle site-nav__toggle" data-component="site-nav-toggle" aria-label="Open navigation menu" aria-controls="primary-navigation" aria-expanded="false"><span></span><span></span><span></span></button></div></nav>
<header class="sub-hero dark site-hero" data-component="page-hero"><div class="container narrow"><p class="eyebrow ds-eyebrow">Portfolio</p><h1>Software described from its source.</h1><p>This catalog reflects projects found in the local Codehub workspace as of August 23, 2026. Status labels distinguish live products, current builds, prototypes, and work in development.</p></div></header>
<div class="category-rail-wrap" data-component="portfolio-category-navigation"><nav class="container category-rail" aria-label="Portfolio categories"><a href="#apple">Apple platforms</a><a href="#mobile">Android</a><a href="#web">Web products</a><a href="#tools">AI, data & design</a></nav></div>
<main>{sections}</main>
<section class="section site-section contact-cta"><div class="container"><div class="contact-shell"><div><p class="eyebrow ds-eyebrow">Documentation</p><h2>Policies follow the products that need them.</h2><p>The documentation index contains maintained public privacy, terms, review, and support pages.</p></div><a href="developer-docs.html">Open documentation →</a></div></div></section>
<footer class="footer site-footer" data-component="site-footer"><div class="container"><div class="footer-content site-footer__content"><div class="footer-brand site-footer__brand"><h3>EdenTV</h3><p>Creating thoughtful digital experiences.</p></div><div class="footer-links site-footer__links"><div class="footer-section site-footer__section"><h4>Explore</h4><a href="apps.html">Apps</a><a href="about.html">About</a></div><div class="footer-section site-footer__section"><h4>Documentation</h4><a href="developer-docs.html">Developer docs</a><a href="../legal/support.html">Support</a></div></div></div><div class="footer-bottom site-footer__bottom"><p>&copy; 2026 EdenTV. All rights reserved.</p></div></div></footer><script src="../js/script.js"></script></body></html>'''

(ROOT / "pages" / "apps.html").write_text(html + "\n")
