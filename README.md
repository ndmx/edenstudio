# EdenTV Creator Studio Website

A modern, responsive website showcasing EdenTV's complete portfolio of software and media projects across all platforms, with comprehensive developer documentation and legal compliance materials.

## 🌟 Features

- **Responsive Design**: Optimized for all devices (desktop, tablet, mobile)
- **Design System**: Shared `site-*` and `ds-*` component classes with reusable visual tokens
- **Modern UI**: Light editorial interface with warm paper surfaces, original pencil artwork, clear states, and restrained motion
- **Dynamic Content**: Interactive cycling cards and animated sections
- **Complete Documentation**: Comprehensive legal and technical documentation
- **Well-Organized**: Clean folder structure for easy maintenance

## 📁 Project Structure

```
edentv/
├── index.html                 # Homepage
├── css/
│   └── styles.css            # All styling
├── js/
│   └── script.js             # All JavaScript
├── assets/
│   ├── artwork/
│   │   ├── studio-pencil-paper.webp
│   │   ├── apps-pencil-paper.webp
│   │   └── media-docs-pencil-paper.webp
│   └── brand/
│       └── etv-favicon.svg   # EdenTV Etv browser icon
├── pages/
│   ├── apps.html             # Apps showcase
│   ├── podcasts.html         # Podcasts (coming soon)
│   ├── multimedia.html       # Multimedia (coming soon)
│   ├── developer-docs.html   # Documentation hub
│   └── about.html            # About page
├── legal/
│   ├── privacy-policy.html   # Privacy policy
│   ├── terms-of-service.html # Terms of service
│   ├── app-store-compliance.html # App Store compliance
│   └── support.html          # Support docs
├── docs/
    ├── parkmemory-privacy.html    # App-specific privacy
    ├── parkmemory-terms.html      # App-specific terms
    ├── parkmemory-compliance.html # App-specific compliance
    └── parkmemory-support.html    # App-specific support
└── DESIGN_SYSTEM.md          # Component naming and visual system guide
```

See [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) and [DESIGN_SYSTEM.md](DESIGN_SYSTEM.md) for detailed documentation.

## 🚀 Deployment

### Cloudflare Pages (Recommended)

#### Option 1: Git Integration (Automatic Deployment)
1. Connect your GitHub repository to Cloudflare Pages
2. Configure build settings:
   - **Build command**: (leave empty)
   - **Build output directory**: `.` (root)
   - **Root directory**: `/`
3. Deploy automatically on every push to `main`

#### Option 2: Direct Upload
1. Go to Cloudflare Pages dashboard
2. Create new project
3. Upload the entire project folder
4. Set custom domain (e.g., `edentv.us`)

### Custom Domain Setup
1. In Cloudflare Pages, go to your project
2. Navigate to "Custom domains"
3. Add your domain (e.g., `edentv.us`)
4. Update DNS records as instructed

## 🎨 Customization

### Design System
Use `DESIGN_SYSTEM.md` when adding or editing pages. New reusable components should use:

- `site-*` for global regions such as header, footer, hero, and section shell
- `ds-*` for reusable primitives such as cards, buttons, icons, and badges
- `page-*` for one-off page composition

Legacy classes remain in markup until the whole site is migrated away from them.

### Updating Colors
Edit design-system tokens in `css/styles.css`:

```css
:root {
    --color-page: #090a0d;
    --color-ink: #fff8ef;
    --color-gold: #f0c86a;
    --color-seafoam: #61d5c8;
    /* ... */
}
```

### Adding New Pages
1. Create HTML file in appropriate folder
2. Copy navigation and footer from existing pages
3. Update all navigation menus across the site
4. Follow link structure in PROJECT_STRUCTURE.md

### Modifying Content
- **Homepage hero**: Edit `index.html` hero section
- **App features**: Update `pages/apps.html`
- **Legal docs**: Modify files in `legal/` folder
- **App-specific docs**: Update files in `docs/` folder

## 📱 Portfolio Overview

The public portfolio is generated from a source-verified inventory of the local
Codehub workspace and the studio's GitHub repositories. It currently includes 21 projects grouped as Apple-platform
software, Android, web products, and AI/data/design tools. Status labels are
deliberately specific: live, current build, prototype, release preparation, or
in development.

Run `python3 scripts/build_portfolio.py` after changing the verified inventory.
Run `python3 scripts/build_documents.py` after changing product documents or
their routing indexes. This rebuilds the category hubs, canonical/structured
metadata, sitemap, and `assets/document-index.json`. Run it after regenerating
the portfolio too, so generated metadata stays current.

The Documents & Support library searches the 11 HTML product documents locally
in the browser. Category indexes, navigation, and repeated quick links are not
search results. Keep section IDs stable because search links and external
bookmarks use them. Search state can be shared with `?q=location&type=support`.
Browsing still works without JavaScript or when the index cannot load.

Edit the visible “Last reviewed” date only after reviewing a document; the build
preserves it and emits a machine-readable date. The sitemap deliberately omits
modification dates rather than using a build timestamp. Canonicals use the
extensionless URLs served by Cloudflare Pages; existing `.html` links remain
valid. Downloads are not currently part of this HTML library. If added, provide
an HTML summary with file type and size and explicitly add content extraction.

Check the generated library with `python3 -m unittest discover -s tests -v`.
For browser checks, serve the repo at port 8765 and run
`node tests/document_search.browser.cjs` with Playwright available on `NODE_PATH`
and Chrome installed. Override the server with `DOCUMENT_TEST_URL`.

## 🔗 Key Pages

- **Homepage**: Modern landing page with cycling feature cards and portfolio overview
- **Apps**: Source-verified project catalog with explicit lifecycle status
- **Documents & Support**: Searchable product policies and support library
- **Legal**: Privacy, terms, compliance, and support
- **About**: Studio mission and portfolio statistics

## 🛠️ Technical Details

### Technologies
- Pure HTML5, CSS3, JavaScript (no frameworks)
- Responsive design with CSS Grid and Flexbox
- Modern animations and transitions
- Mobile-first approach

### Browser Support
- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

### Performance Features
- Optimized animations with `will-change`
- Efficient DOM manipulation
- Lazy loading for images
- Minimal dependencies

## 📝 Legal & Compliance

Public documentation is maintained in two places:
- **Platform-wide**: `/legal/` folder
- **App-specific**: `/docs/` folder

Only products with maintained public documents appear in the documentation
index. A product may publish privacy, terms, App Store review, or support pages
as applicable; every product does not automatically receive every document type.

## 🎯 About EdenTV

EdenTV is a design studio responsible for creating software and media across multiple platforms. Our portfolio spans iOS and Android mobile applications, full-stack web platforms, data processing tools, and educational resources. Every project showcased on this website is designed, developed, and maintained by the EdenTV team.

### Platform Expertise
- **Mobile Development**: iOS (SwiftUI), Android (Kotlin), macOS
- **Web Development**: React, Firebase, Node.js, Flask
- **Data & Analytics**: Python, Pandas, ETL pipelines
- **Technologies**: Cloud services (Firebase, CloudKit), AI integration (Gemini), Real-time systems

### Stay Connected
Contact us at `contact@edentv.us` for project inquiries and collaborations.

## 💼 Contact & Support

- **General Inquiries**: contact@edentv.us
- **Support**: support@edentv.us
- **Privacy Questions**: privacy@edentv.us
- **Legal**: legal@edentv.us

## 📜 License

© 2026 EdenTV. All rights reserved.

---

Built with ❤️ by EdenTV Creator Studio
