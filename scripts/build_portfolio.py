from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

GROUPS = [
    ("apple", "Apple platforms", "Selected native applications featured by EdenTV.", [
        ("ParkMemory Hub", "Current build", "A local-first iPhone app for private trip circles, shared memories, plans, voting, and optional location updates through CloudKit.", ["SwiftUI", "CloudKit", "iOS 18+"]),
        ("JxL Scheduler", "In development", "A local-first iPhone logistics app for schedules, routes, messages, uploads, and optional group sharing through iCloud.", ["SwiftUI", "SwiftData", "CloudKit"]),
        ("PulseTrackr", "Release preparation", "An iPhone community-safety app for incident reports, map awareness, evidence capture, verification signals, and trusted-contact SOS.", ["SwiftUI", "Firebase", "iOS 18+"]),
        ("Cosmix", "Desktop build", "A real-time macOS audio visualizer with particle, waveform, and circular modes driven by microphone FFT analysis.", ["SwiftUI", "AVFoundation", "Accelerate"]),
        ("Kasapa", "Prototype · milestone 3", "A privacy-first professional-networking prototype with exact sharing grants, local messaging, block/report controls, and on-device persistence.", ["SwiftUI", "Local-first", "iOS"]),
    ]),
    ("mobile", "Android", "Selected Android projects and prototypes.", [
        ("MoodQuest", "Prototype", "A mood-based adventure planner with optional nearby suggestions, custom activities, history, and offline Room persistence.", ["Kotlin", "Jetpack Compose", "Room"]),
        ("Frisbie", "GitHub project", "A compact Android food-selector project built in Kotlin.", ["Kotlin", "Android"]),
    ]),
    ("web", "Web products", "Selected browser applications and platforms. Client brands are credited in Alexander’s personal portfolio.", [
        ("PulseTrack", "Live", "A React and Firebase platform tracking Nigerian political sentiment, with maps, charts, submissions, and a scheduled Python NLP pipeline.", ["React", "TypeScript", "Firebase"]),
        ("LxRose", "Live", "A domain-aware healthcare website and protected operations dashboard backed by Firebase Functions and an Express API.", ["React", "Express", "Firebase"]),
        ("Crystal Heart", "Live", "A private matchmaking application on Cloudflare Workers with a public applicant flow and a separately protected staff review workspace.", ["Cloudflare Workers", "D1", "Access"]),
        ("Upskill Institute", "Web platform", "A Flask learning platform with authentication, course and module progress, career recommendations, and Paystack enrollment.", ["Flask", "PostgreSQL", "Paystack"]),
        ("Guess Correctly", "Web game", "A responsive Halloween memory game with single-player and two-player real-time Firebase modes.", ["JavaScript", "Firebase", "HTML/CSS"]),
        ("Snapshot", "GitHub project", "A React photo-sharing project with Firebase-backed uploads, feeds, profiles, search, messages, and notifications.", ["React", "Firebase"]),
        ("NebulaChat", "GitHub project", "A real-time chat project with direct and group messaging, sentiment-aware themes, and a React/Firebase client.", ["React", "Firebase", "Express"]),
    ]),
    ("tools", "Research and design", "Experiments and design tools by founder Alexander Ukaga, with research projects clearly marked by their stage.", [
        ("Autobiz", "In development", "A source-backed business-listing research tool that deduplicates, scores, verifies, and ranks acquisition opportunities.", ["Python", "Multi-agent", "Data pipeline"]),
        ("Autoresearch for macOS", "Research fork", "Alexander’s local small-model research on Apple Silicon: training, state tracking, tool use, and project memory. Current evaluations expose reliability limits; this remains experimental.", ["Python", "PyTorch", "Apple Silicon"]),
        ("Orchestra", "Founder experiment", "Alexander’s multi-model conversation prototype, exploring directed streaming turns and avatar presence. Session continuity and conversational reliability remain development goals.", ["Python", "Next.js", "Conversation"]),
        ("Philly Real Estate Tracker", "Data application", "A Southeast Philadelphia property-trend explorer built from local data-processing and application code.", ["Python", "Pandas", "SQLite"]),
        ("Blockchain Transfer Simulation", "Learning prototype", "An interactive proof-of-work and transfer simulation intended for technical exploration rather than financial use.", ["Python", "Streamlit", "Simulation"]),
        ("Lumina Codex", "Published system", "A framework-independent design system with tokens, themes, layout decisions, and a feedback CLI, published as @xlumina/system.", ["TypeScript", "CSS", "Design system"]),
    ]),
]

def card(project):
    name, status, description, tags = project
    from app_documents import APPS, TYPES
    app = next(((slug, info) for slug, info in APPS.items() if info[0] == name), None)
    if app:
        slug, (_, anchor, _) = app
        primary = f'/pages/{slug}'
        links = [("View app", primary)] + [(label, f'/docs/{slug}-{kind}') for kind,label in TYPES.items()]
    else:
        links = [("Project overview", "https://alexanderukaga.me/projects")]
        if name == 'Lumina Codex':
            links = [("View package", "https://www.npmjs.com/package/@xlumina/system")]
    actions = '<nav class="project-actions" aria-label="' + name + ' links">' + ''.join(f'<a href="{url}">{label}</a>' for label,url in links) + '</nav>'
    tag_html = "".join(f'<span class="tech-badge">{tag}</span>' for tag in tags)
    return f'<article class="project-card ds-card"><div class="project-label">{status}</div><h3>{name}</h3><p>{description}</p><div class="project-tags">{tag_html}</div>{actions}</article>'

sections = "".join(f'<section id="{slug}" class="section site-section category-section"><div class="container"><div class="category-header"><div><p class="eyebrow ds-eyebrow">Featured work</p><h2>{title}.</h2><p>{intro}</p></div></div><div class="project-grid">{"".join(card(p) for p in projects)}</div></div></section>' for slug, title, intro, projects in GROUPS)

html = f'''<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Apps & Projects - EdenTV Creator Studio</title><meta name="description" content="Software, prototypes, and founder research featured by EdenTV, a creative studio for digital experiences."><link rel="stylesheet" href="../css/styles.css?v=20260905"><link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet"><link rel="icon" type="image/svg+xml" href="../assets/brand/etv-favicon.svg"></head>
<body class="page-apps"><nav class="navbar site-header" data-component="site-header" aria-label="Primary navigation"><div class="nav-container site-header__container"><a href="../index.html" class="nav-brand site-brand" data-component="site-brand"><span class="brand-name">EdenTV</span><span class="tagline site-brand__tagline">Creator Studio</span></a><div id="primary-navigation" class="nav-menu site-nav" data-component="site-nav"><a href="../index.html" class="nav-link site-nav__link">Home</a><a href="apps.html" class="nav-link site-nav__link active">Apps</a><a href="podcasts.html" class="nav-link site-nav__link">Podcasts</a><a href="multimedia.html" class="nav-link site-nav__link">Multimedia</a><a href="developer-docs.html" class="nav-link site-nav__link">Documents &amp; Support</a><a href="about.html" class="nav-link site-nav__link">About</a></div><button type="button" class="nav-toggle site-nav__toggle" data-component="site-nav-toggle" aria-label="Open navigation menu" aria-controls="primary-navigation" aria-expanded="false"><span></span><span></span><span></span></button></div></nav>
<header class="sub-hero dark site-hero" data-component="page-hero"><div class="container narrow"><p class="eyebrow ds-eyebrow">EdenTV · Creative studio</p><h1>Software, design, and exploration.</h1><p>A selection of applications, prototypes, and founder research featured by the studio. Explore current builds, prototypes, and the ideas behind them.</p><p>For Alexander Ukaga’s broader body of work, including client projects for Joneva Logistics and Miriam’s Corner, <a href="https://alexanderukaga.me/projects">explore his personal portfolio →</a></p></div></header>
<div class="category-rail-wrap" data-component="portfolio-category-navigation"><nav class="container category-rail" aria-label="Portfolio categories"><a href="#apple">Apple platforms</a><a href="#mobile">Android</a><a href="#web">Web products</a><a href="#tools">Research & design</a></nav></div>
<main>{sections}</main>
<section class="section site-section contact-cta"><div class="container"><div class="contact-shell"><div><p class="eyebrow ds-eyebrow">Documentation</p><h2>Policies follow the products that need them.</h2><p>The documentation index contains maintained public privacy, terms, review, and support pages.</p></div><a href="developer-docs.html">Open documentation →</a></div></div></section>
<footer class="footer site-footer" data-component="site-footer"><div class="container"><div class="footer-content site-footer__content"><div class="footer-brand site-footer__brand"><h3>EdenTV</h3><p>Creating thoughtful digital experiences.</p></div><div class="footer-links site-footer__links"><div class="footer-section site-footer__section"><h4>Explore</h4><a href="apps.html">Apps</a><a href="about.html">About</a></div><div class="footer-section site-footer__section"><h4>Documentation</h4><a href="developer-docs.html">Documents &amp; Support</a><a href="../legal/support.html">Support</a></div></div></div><div class="footer-bottom site-footer__bottom"><p>&copy; 2026 EdenTV. All rights reserved.</p></div></div></footer><script src="../js/script.js"></script></body></html>'''

(ROOT / "pages" / "apps.html").write_text(html + "\n")
