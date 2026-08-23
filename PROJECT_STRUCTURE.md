# EdenTV Website - Project Structure

## Directory Organization

```
edentv/
├── index.html                 # Homepage (root level for easy access)
├── css/
│   └── styles.css            # All website styling
├── js/
│   └── script.js             # All website JavaScript
├── assets/
│   ├── artwork/
│   │   ├── studio-pencil-paper.webp     # Homepage and About background
│   │   ├── apps-pencil-paper.webp       # Apps portfolio background
│   │   └── media-docs-pencil-paper.webp # Media and documentation background
│   └── brand/
│       └── etv-favicon.svg               # EdenTV Etv browser icon
├── pages/
│   ├── apps.html             # Apps showcase page
│   ├── podcasts.html         # Podcasts page (coming soon)
│   ├── multimedia.html       # Multimedia page (coming soon)
│   ├── developer-docs.html   # Developer documentation hub
│   └── about.html            # About EdenTV page
├── legal/
│   ├── privacy-policy.html   # Platform privacy policy
│   ├── terms-of-service.html # Platform terms of service
│   ├── app-store-compliance.html # App Store compliance
│   └── support.html          # Support & help documentation
├── docs/
│   ├── parkmemory-privacy.html    # ParkMemoryHub privacy policy
│   ├── parkmemory-terms.html      # ParkMemoryHub terms
│   ├── parkmemory-compliance.html # ParkMemoryHub App Store compliance
│   ├── parkmemory-support.html    # ParkMemoryHub support docs
│   ├── jxl-scheduler-*.html       # JxL Scheduler documents
│   └── pulsetrackr-*.html         # PulseTrackr documents
├── scripts/
│   ├── build_document_hubs.py     # Generate the four public doc indexes
│   └── build_portfolio.py         # Generate the source-verified portfolio
├── README.md                 # Project documentation
├── DESIGN_SYSTEM.md          # EdenTV component naming and visual system
└── PROJECT_STRUCTURE.md      # This file

```

## File Organization Logic

### Root Level
- `index.html` - Homepage stays at root for easy access and SEO

### `/css/` - Stylesheets
- All CSS files
- Currently single `styles.css` with all styling

### `/js/` - JavaScript
- All JavaScript files
- Currently single `script.js` with all functionality

### `/assets/` - Brand & Media Assets
- Brand marks, icons, reusable media, and optimized editorial artwork
- Current favicon is `assets/brand/etv-favicon.svg`
- Page artwork is stored as optimized WebP in `assets/artwork/`

### `/pages/` - Main Content Pages
- All main website pages (apps, podcasts, multimedia, docs, about)
- Pages that showcase platform content

### `/legal/` - Legal & Compliance
- Privacy policies
- Terms of service
- App Store compliance documentation
- Support resources

### `/docs/` - App-Specific Documentation
- Individual app documentation
- App-specific legal documents
- Currently contains ParkMemory Hub, JxL Scheduler, and PulseTrackr documents

## Link Structure

### From Root (`index.html`)
- Pages: `pages/[page].html`
- Legal: `legal/[document].html`
- CSS: `css/styles.css`
- JS: `js/script.js`
- Favicon: `assets/brand/etv-favicon.svg`

### From Pages (`pages/*.html`)
- Home: `../index.html`
- Other Pages: `[page].html` (same directory)
- Legal: `../legal/[document].html`
- App Docs: `../docs/[doc].html`
- CSS: `../css/styles.css`
- JS: `../js/script.js`
- Favicon: `../assets/brand/etv-favicon.svg`

### From Legal (`legal/*.html`)
- Home: `../index.html`
- Pages: `../pages/[page].html`
- Other Legal: `[document].html` (same directory)
- CSS: `../css/styles.css`
- JS: `../js/script.js`
- Favicon: `../assets/brand/etv-favicon.svg`

### From Docs (`docs/*.html`)
- Home: `../index.html`
- Pages: `../pages/[page].html`
- Legal: `../legal/[document].html`
- CSS: `../css/styles.css`
- JS: `../js/script.js`
- Favicon: `../assets/brand/etv-favicon.svg`

## Content Status

### Live Content
- **Homepage**: Fully functional with dynamic cycling cards and portfolio overview
- **Apps Page**: Source-verified showcase of 18 local projects with explicit lifecycle status
- **Developer Docs**: Hub for all documentation with links to app-specific docs
- **About Page**: Studio mission and portfolio statistics
- **Legal Documents**: Complete platform and app-specific legal documentation

### Portfolio Categories
1. **Apple platforms**: current SwiftUI iPhone and macOS projects
2. **Android**: the current Kotlin and Compose project
3. **Web products**: browser and full-stack projects with local source
4. **AI, data, and design tools**: research, analysis, simulation, and system work

### Coming Soon
- **Podcasts**: Page structure ready, content in development
- **Multimedia**: Page structure ready, content in development

## Deployment

This is a static website designed for Cloudflare Pages deployment:

1. Root directory contains `index.html` for main entry point
2. All assets properly organized in subdirectories
3. Relative paths used throughout for portability
4. No build process required - deploy as-is

### Cloudflare Pages Setup
1. Connect GitHub repository
2. Set build directory to root (`.`)
3. No build command needed
4. Deploy automatically on push to `main`

## Maintenance Notes

### Adding New Pages
1. Create HTML file in appropriate directory (`pages/`, `legal/`, or `docs/`)
2. Update navigation in all existing pages
3. Follow the link structure patterns above
4. Update this documentation

### Adding New Projects
1. Add project card to appropriate platform section in `pages/apps.html`
2. Include project icon, name, description, features, and tech badges
3. Add "Designed by edentv" badge
4. Update portfolio statistics in `index.html` and documentation
5. Create project-specific documentation in `docs/` folder if needed
6. Add subtle edentv branding footer to project's README

### Updating Styles
- All styles in `css/styles.css`
- Uses CSS custom properties and the EdenTV design-system tokens for consistency
- Responsive design included

### Updating Components
- Follow `DESIGN_SYSTEM.md`
- Use `site-*` for global regions such as header, hero, section, and footer
- Use `ds-*` for reusable primitives such as cards, buttons, icons, and badges
- Keep legacy classes in place until their CSS and JavaScript dependencies are removed

### Updating Functionality
- All JavaScript in `js/script.js`
- Includes null checks for page-specific elements
- Mobile menu, animations, and interactive features

## Best Practices

1. **Always use relative paths** - Makes deployment flexible
2. **Keep content honest** - Only showcase real, available features
3. **Maintain structure** - Files organized by purpose
4. **Update navigation consistently** - All pages should have same nav structure
5. **Test cross-page links** - Verify links work after moving files

## Quick Reference

- Homepage: `/index.html`
- Apps: `/pages/apps.html`
- Podcasts: `/pages/podcasts.html`
- Multimedia: `/pages/multimedia.html`
- Developer Docs: `/pages/developer-docs.html`
- About: `/pages/about.html`
- Privacy Policy (Platform): `/legal/privacy-policy.html`
- Privacy Policy (ParkMemoryHub): `/docs/parkmemory-privacy.html`
- Support: `/legal/support.html`
