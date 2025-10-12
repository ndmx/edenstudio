# EdenTV Creator Studio

A modern, responsive website for EdenTV - showcasing apps, podcasts, multimedia content, and providing essential developer documentation for App Store compliance.

## 🌟 Features

- **Modern Design**: Clean, professional interface with smooth animations
- **Responsive Layout**: Fully responsive across all devices
- **Developer Documentation**: Complete privacy policy, terms of service, and App Store compliance pages
- **Portfolio Showcase**: Display apps, podcasts, and multimedia content
- **Contact & Support**: Multiple contact methods and support channels
- **SEO Optimized**: Proper meta tags and semantic HTML structure

## 📁 Project Structure

```text
edentv.us/
├── index.html              # Main landing page
├── styles.css              # Main stylesheet
├── script.js               # JavaScript functionality
├── privacy-policy.html     # Privacy policy page
├── terms-of-service.html   # Terms of service page
├── app-store-compliance.html # App Store compliance documentation
├── support.html            # Contact and support page
└── README.md              # This file
```

## 🚀 Deployment to Cloudflare

### Option 1: Cloudflare Pages (Recommended)

1. **Connect Repository**:
   - Go to Cloudflare Dashboard → Pages
   - Click "Create a project"
   - Connect your Git repository or upload files

2. **Build Settings**:
   - Build command: (leave empty for static site)
   - Build output directory: `/` (root)
   - Root directory: `/` (leave default)

3. **Custom Domain**:
   - Add your domain `edentv.us`
   - Cloudflare will provide SSL certificate automatically

### Option 2: Direct Upload

1. **Zip the files**:
   ```bash
   zip -r edentv-site.zip .
   ```

2. **Upload to Cloudflare**:
   - Go to Cloudflare Dashboard → Pages
   - Choose "Direct upload"
   - Upload the zip file

## 📱 Pages Overview

### Main Page (`index.html`)
- Hero section with branding
- Featured apps section
- Podcasts, multimedia, and documentation sections
- About section with company stats
- Contact footer

### Documentation Pages
- **Privacy Policy**: Comprehensive privacy policy compliant with GDPR, CCPA, and App Store requirements
- **Terms of Service**: Legal terms covering user conduct, liability, and dispute resolution
- **App Store Compliance**: Detailed compliance information for Apple App Store submissions
- **Support**: Contact information, FAQ, and troubleshooting guides

## 🎨 Customization

### Colors
The site uses CSS custom properties for easy theming:
```css
--primary-color: #6366f1;     /* Main brand color */
--secondary-color: #06b6d4;   /* Accent color */
--text-primary: #111827;      /* Primary text */
--bg-primary: #ffffff;        /* Background */
```

### Content Updates
- Update app information in the "Apps" section
- Modify contact details in footer and support page
- Add new portfolio items to respective sections
- Update legal documents as needed

## 📧 Contact Information

Update these email addresses in the code:
- General Support: `support@edentv.us`
- Privacy/Legal: `privacy@edentv.us`
- Business: `business@edentv.us`
- Technical: `dev@edentv.us`

## 🔧 Technical Details

- **Framework**: Vanilla HTML/CSS/JavaScript
- **Fonts**: Inter (Google Fonts)
- **Icons**: Unicode emojis (fallback-friendly)
- **Responsive**: Mobile-first design
- **Performance**: Optimized images and minimal dependencies

## 📋 App Store Submission Checklist

Before submitting apps to the App Store, ensure:

1. **Privacy Policy** is published and linked
2. **Terms of Service** are available
3. **Support URL** points to this website
4. **App Privacy Details** match the privacy policy
5. **Contact Information** is accurate

## 🚀 Future Enhancements

Potential additions:
- Blog/news section
- User testimonials
- App download counters
- Social media integration
- Newsletter signup
- Analytics integration
- Multi-language support

## 📄 License

This website template is provided as-is for EdenTV use. Customize and modify as needed for your requirements.

---

**EdenTV** - Creating tomorrow's digital experiences today.
