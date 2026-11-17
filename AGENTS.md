# FIX4U

Static marketing website (English + Simplified Chinese) for a phone/computer repair, trade-in, and used-device business.

## Cursor Cloud specific instructions

- This is a zero-dependency static site: plain HTML with inlined CSS and a small amount of inline vanilla JS. There is no package manager, build step, lint config, or test suite.
- Serve the site for development from the repo root with a static file server, e.g. `python3 -m http.server 8000` (Python 3 is preinstalled). Then open `http://localhost:8000/` (English) or `http://localhost:8000/index-zh.html` (Chinese).
- All CSS/JS is inlined in each HTML file; there is no bundler or hot reload. After editing an HTML file, just refresh the browser.
- Images live in `images/` and are referenced by relative path, so the server must be started from the repo root for them to resolve.
