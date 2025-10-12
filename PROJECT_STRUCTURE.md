# EdenTV Website Project Structure

## 📁 Directory Organization

### Core Website Pages
```
├── index.html              # Homepage with hero and overview
├── apps.html               # Mobile applications showcase
├── podcasts.html           # Podcast series and episodes
├── multimedia.html         # Video and creative projects
├── developer-docs.html     # Main developer documentation hub
└── about.html              # Company information and story
```

### Platform Legal Documentation
```
├── privacy-policy.html          # Platform-wide privacy policy
├── terms-of-service.html        # Platform terms of service
├── app-store-compliance.html    # App Store compliance documentation
└── support.html                 # General support and help center
```

### App-Specific Documentation
```
docs/
├── parkmemory-privacy.html      # ParkMemoryHub privacy policy
├── parkmemory-terms.html        # ParkMemoryHub terms of service
├── parkmemory-compliance.html   # ParkMemoryHub App Store compliance
└── parkmemory-support.html      # ParkMemoryHub support documentation
```

### Core Assets
```
├── styles.css              # Main stylesheet with all page styles
├── script.js               # Interactive functionality and animations
└── README.md               # Project documentation
```

## 🗑️ Optional/Removable Files

The following files are part of the **Dynamic Content System** and are **optional**:
- `admin.html` - Admin panel for content management
- `content-api.js` - Cloudflare Worker API for dynamic content
- `dynamic-content.js` - Client-side dynamic content loader
- `update-api.js` - Programmatic content update script

**When to keep them:**
- If you're using Cloudflare Workers for dynamic content updates
- If you need remote content management without redeploying

**When to remove them:**
- If you prefer static content (recommended for simplicity)
- If you're only using Cloudflare Pages without Workers

## 🏗️ Architecture

### Page Hierarchy
```
Homepage (index.html)
├── Apps (apps.html)
│   └── ParkMemoryHub Details
│
├── Podcasts (podcasts.html)
│   └── Episode Listings
│
├── Multimedia (multimedia.html)
│   └── Project Gallery
│
├── Developer Docs (developer-docs.html)
│   ├── Platform Documentation
│   └── App-Specific Docs (docs/*)
│       ├── Privacy Policy
│       ├── Terms of Service
│       ├── App Store Compliance
│       └── Support Documentation
│
└── About (about.html)
    ├── Mission & Values
    ├── Company Story
    └── Contact Information
```

### Footer Links (Consistent Across All Pages)
```
Platform:
- Apps → apps.html
- Podcasts → podcasts.html
- Multimedia → multimedia.html
- About → about.html

Legal:
- Privacy Policy → privacy-policy.html
- Terms of Service → terms-of-service.html
- App Store Compliance → app-store-compliance.html

Connect:
- Support → mailto:support@edentv.us
- Help Center → support.html
```

## 🎨 Styling Structure

### CSS Organization
```
styles.css
├── Reset & Base Styles
├── CSS Variables (colors, spacing, animations)
├── Typography
├── Layout Components
│   ├── Navbar
│   ├── Hero Section
│   ├── Footer
│   └── Containers
├── Interactive Components
│   ├── Buttons
│   ├── Cards
│   ├── Animations
│   └── Cycling Cards
├── Page-Specific Styles
│   ├── Apps Page
│   ├── Podcasts Page
│   ├── Multimedia Page
│   ├── Developer Docs
│   └── About Page
└── Responsive Design (@media queries)
```

## 🔧 JavaScript Functionality

### script.js Features
```
├── Smooth Scrolling (anchor links & TOC)
├── Mobile Menu Toggle
├── Navbar Scroll Effects
├── Active Navigation Highlighting
├── Intersection Observer (animations)
├── Cycling Card Animation
├── Parallax Effects
├── Back to Top Button
└── TOC Section Highlighting
```

## 📱 Responsive Breakpoints

- **Desktop:** 1200px+
- **Tablet:** 768px - 1199px
- **Mobile:** < 768px

## 🚀 Deployment

### Cloudflare Pages (Static Site)
- Automatic deployment from GitHub
- Custom domain: `edentv.us`
- All HTML, CSS, JS files served directly

### Optional: Cloudflare Workers (Dynamic Content)
- Only needed if using `content-api.js`
- Route: `edentv.us/api/*`
- Environment variable: `API_KEY`

## 📝 Content Management

### Static Content (Recommended)
1. Edit HTML files directly
2. Commit changes to Git
3. Push to GitHub
4. Cloudflare Pages auto-deploys

### Dynamic Content (Optional)
1. Use `admin.html` for content updates
2. API Key authentication required
3. Updates via `content-api.js` Worker
4. No redeployment needed

## ✅ Best Practices

### File Naming
- Use kebab-case for all files: `developer-docs.html`
- Keep names descriptive and clear
- App-specific docs prefixed with app name: `parkmemory-*`

### Code Organization
- One feature per section/component
- Consistent indentation (4 spaces)
- Comments for complex functionality
- Semantic HTML5 elements

### Content Guidelines
- Short paragraphs (2-3 sentences max)
- Bullet points for features/lists
- Headings in logical hierarchy (h1 → h2 → h3)
- Clear calls-to-action

## 🔍 Quick Reference

### Adding a New App
1. Add app details to `apps.html`
2. Create app showcase section
3. Create docs folder: `docs/newapp-*`
4. Link from `developer-docs.html`
5. Update navigation if needed

### Adding Legal Documentation
1. Create HTML file: `new-policy.html`
2. Use existing legal page as template
3. Add navigation and footer
4. Link from footer across all pages

### Updating Styles
1. Edit `styles.css`
2. Use existing CSS variables
3. Follow mobile-first approach
4. Test on multiple screen sizes

## 📞 Support

For questions about the project structure or making changes:
- Email: support@edentv.us
- Documentation: This file
- Reference: Any existing page as template

