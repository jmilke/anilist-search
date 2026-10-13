# AniList Advanced Filter (Mobile Web App)

A lightweight, standalone mobile-first web app that brings AniList's desktop advanced tag & genre filtering to mobile devices.

## Features
- **3-State Tag Chips**: Tap 1× to Include (Green `+`), Tap 2× to Exclude (Red `-`), Tap 3× to Clear.
- **Instant Search**: Type to filter through all ~450+ AniList tags and genres in real time.
- **Category Filter**: Filter tags by Themes, Cast, Setting, Demographics, or Genres.
- **Minimum Tag Rank Slider**: Customize the tag confidence threshold (0% to 100%, default 18%).
- **Additional Filters**: Title search, media type (Anime / Manga), Format, Season, Year, Status, Country of Origin, and Sorting.
- **One-Tap AniList Launch**: Generates the exact query string and opens AniList directly in your browser.
- **Mobile / PWA Ready**: Formatted with safe-area insets, dark theme, and standalone web app meta tags.

## How to Use on Your Phone

### Option A: Free 1-Minute Host (GitHub Pages / Vercel / Netlify)
1. Upload `index.html` to a new GitHub repository (e.g. `anilist-search`).
2. Go to **Settings > Pages** and set source to `main` branch.
3. Open your GitHub Pages link on your phone in Safari / Chrome.
4. Tap **Share / Menu** -> **"Add to Home Screen"**. It will now open as a fullscreen app icon.

### Option B: Local Network Testing
From this directory, run:
```bash
npx serve .
# or
python3 -m http.server 8080
```
Then visit `http://<your-mac-ip>:8080` on your phone connected to the same Wi-Fi.
