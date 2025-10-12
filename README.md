# EdenTV Creator Studio Website

A modern, responsive website showcasing EdenTV's mobile applications, with comprehensive developer documentation and legal compliance materials.

## 🌟 Features

- **Responsive Design**: Optimized for all devices (desktop, tablet, mobile)
- **Modern UI**: Clean interface with smooth animations and transitions
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
└── docs/
    ├── parkmemory-privacy.html    # App-specific privacy
    ├── parkmemory-terms.html      # App-specific terms
    ├── parkmemory-compliance.html # App-specific compliance
    └── parkmemory-support.html    # App-specific support
```

See [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) for detailed documentation.

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

### Updating Colors
Edit CSS custom properties in `css/styles.css`:

```css
:root {
    --primary-color: #6366f1;
    --primary-dark: #4f46e5;
    --text-primary: #1a202c;
    --text-secondary: #4a5568;
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

## 📱 Current Apps

### ParkMemoryHub
- **Status**: Available
- **Platform**: iOS 18+
- **Description**: Family memory sharing and preservation platform
- **Documentation**: Full legal and compliance documentation in `docs/` folder

## 🔗 Key Pages

- **Homepage**: Modern landing page with cycling feature cards
- **Apps**: Showcase of mobile applications
- **Developer Docs**: Complete documentation hub
- **Legal**: Privacy, terms, compliance, and support

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

All legal documentation is maintained in two places:
- **Platform-wide**: `/legal/` folder
- **App-specific**: `/docs/` folder

Each app has its own set of legal documents:
- Privacy Policy
- Terms of Service
- App Store Compliance
- Support Documentation

## 🎯 Future Plans

### In Development
- **Podcasts**: Audio content and conversations
- **Multimedia**: Visual content and tutorials
- **Additional Apps**: More innovative applications

### Stay Updated
Contact us at `contact@edentv.us` for updates on new features and releases.

## 💼 Contact & Support

- **General Inquiries**: contact@edentv.us
- **Support**: support@edentv.us
- **Privacy Questions**: privacy@edentv.us
- **Legal**: legal@edentv.us

## 📜 License

© 2024 EdenTV. All rights reserved.

---

Built with ❤️ by EdenTV Creator Studio
