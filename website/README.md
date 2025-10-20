# 🌐 MiraiAI Website

Beautiful, modern showcase website for the MiraiAI Mental Health Support Bot.

## 📁 Structure

```
website/
├── index.html          # Main HTML file
├── assets/
│   ├── css/
│   │   └── style.css   # Styling
│   ├── js/
│   │   └── script.js   # JavaScript functionality
│   └── images/         # Images (add your own)
└── README.md           # This file
```

## ✨ Features

### Sections Included:
1. **Hero Section** - Eye-catching introduction with CTA buttons
2. **About Section** - Key features and benefits
3. **Team Section (DTL)** - Design, Technology, Leadership breakdown
4. **How It Works** - 3-step process explanation
5. **Results Section** - Features, use cases, and performance metrics
6. **Bot Connection** - Direct Telegram bot integration
7. **Footer** - Links and emergency resources

### Design Features:
- 🎨 Modern gradient design
- 📱 Fully responsive (mobile, tablet, desktop)
- ⚡ Smooth animations and transitions
- 🌙 Dark theme optimized for readability
- 🎯 Clear call-to-actions
- ♿ Accessible and user-friendly

## 🚀 How to Use

### Local Development:
1. Open `index.html` in your browser
2. No build process needed - pure HTML/CSS/JS

### Deploy to GitHub Pages:
```bash
# From MiraiAi root directory
git add website/
git commit -m "Add showcase website"
git push origin main

# Then enable GitHub Pages in repo settings
# Source: main branch, /website folder
```

### Deploy to Netlify/Vercel:
1. Drag and drop the `website` folder
2. Or connect your GitHub repo
3. Set build directory to `website`
4. Deploy!

## 🔧 Customization

### Update Bot Username:
Edit `index.html` and replace `@Mirai_Ai_bot` with your bot's username.

### Change Colors:
Edit `assets/css/style.css` and modify the CSS variables:
```css
:root {
    --primary: #6366f1;      /* Main color */
    --secondary: #8b5cf6;    /* Secondary color */
    --accent: #ec4899;       /* Accent color */
}
```

### Add Images:
1. Place images in `assets/images/`
2. Update `<img>` tags in `index.html`

### Add Team Members:
Edit the team section in `index.html` to add real team member info.

## 📊 Sections Breakdown

### 1. Hero Section
- Main headline with gradient text
- Subtitle explaining the bot
- Two CTA buttons (Try Bot, Learn More)
- Stats showcase (24/7, Privacy, AI-Powered)

### 2. About Section
- 4 feature cards:
  - Empathetic Support
  - Complete Privacy
  - Advanced AI
  - Instant Response

### 3. Team Section (DTL)
- **Design**: UI/UX, accessibility
- **Technology**: AI, Python, Cloud
- **Leadership**: Vision, strategy, advocacy

### 4. How It Works
- 3-step process
- Tech stack showcase
- Simple, clear explanation

### 5. Results Section
- Key Features list
- Use Cases list
- Performance metrics
- User testimonial

### 6. Bot Connection
- Direct Telegram link
- Feature highlights
- QR code placeholder
- Multiple CTAs

### 7. Footer
- Quick links
- Resources
- Emergency contacts
- Copyright info

## 🎨 Design System

### Colors:
- Primary: Indigo (#6366f1)
- Secondary: Purple (#8b5cf6)
- Accent: Pink (#ec4899)
- Background: Dark slate (#0f172a)

### Typography:
- Font: Inter (Google Fonts)
- Weights: 300, 400, 600, 700, 800

### Spacing:
- Sections: 6rem padding
- Cards: 2rem padding
- Gaps: 1.5-3rem

## 📱 Responsive Breakpoints

- Desktop: > 768px
- Tablet: 768px
- Mobile: < 768px

## 🔗 Links to Update

Before deploying, update these links:
1. Bot username in all Telegram links
2. GitHub repo link in footer
3. Add real QR code image
4. Add team member photos (optional)
5. Update testimonials with real feedback

## 🚀 Performance

- No external dependencies (except Google Fonts)
- Lightweight CSS and JS
- Fast load times
- Optimized animations

## 📄 License

Part of the MiraiAI project. See main repository for license details.

## 💡 Tips

1. **Add Analytics**: Insert Google Analytics or Plausible code
2. **SEO**: Add meta tags for better search visibility
3. **Images**: Add screenshots of bot conversations
4. **Testimonials**: Collect real user feedback
5. **Blog**: Add a blog section for mental health tips

## 🆘 Support

For issues or questions about the website:
- Check the main MiraiAI repository
- Open an issue on GitHub
- Contact the development team

---

Built with 💙 for mental health support
