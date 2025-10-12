# EdenTV Website - Project Structure

## Directory Organization

```
edentv/
├── index.html                 # Homepage (root level for easy access)
├── css/
│   └── styles.css            # All website styling
├── js/
│   └── script.js             # All website JavaScript
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
│   └── parkmemory-support.html    # ParkMemoryHub support docs
├── README.md                 # Project documentation
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
- Currently contains ParkMemoryHub docs

## Link Structure

### From Root (`index.html`)
- Pages: `pages/[page].html`
- Legal: `legal/[document].html`
- CSS: `css/styles.css`
- JS: `js/script.js`

### From Pages (`pages/*.html`)
- Home: `../index.html`
- Other Pages: `[page].html` (same directory)
- Legal: `../legal/[document].html`
- App Docs: `../docs/[doc].html`
- CSS: `../css/styles.css`
- JS: `../js/script.js`

### From Legal (`legal/*.html`)
- Home: `../index.html`
- Pages: `../pages/[page].html`
- Other Legal: `[document].html` (same directory)
- CSS: `../css/styles.css`
- JS: `../js/script.js`

### From Docs (`docs/*.html`)
- Home: `../index.html`
- Pages: `../pages/[page].html`
- Legal: `../legal/[document].html`
- CSS: `../css/styles.css`
- JS: `../js/script.js`

## Content Status

### Live Content
- **Homepage**: Fully functional with dynamic cycling cards
- **Apps Page**: Features ParkMemoryHub with full details
- **Developer Docs**: Hub for all documentation with links to app-specific docs
- **About Page**: Company mission and information
- **Legal Documents**: Complete platform and app-specific legal documentation

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

### Adding New Apps
1. Create app documentation in `docs/` folder
2. Add app section to `pages/apps.html`
3. Link to new docs from `pages/developer-docs.html`
4. Create app-specific legal documents if needed

### Updating Styles
- All styles in `css/styles.css`
- Uses CSS custom properties for consistency
- Responsive design included

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
