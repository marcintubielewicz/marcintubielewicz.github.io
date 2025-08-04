# Modern Developer Portfolio Website
A lightweight, responsive portfolio built with **FastAPI**, **Jinja2** and **Tailwind CSS**.  
FastAPI is used only to pre‑render Jinja templates locally and export a fully static site, so the final build has **zero backend dependencies** and can be deployed to **GitHub Pages** in seconds.

## ✨ Features 
- **Minimal design** with Tailwind CSS  
- **Dark / Light mode** toggle (preference stored in `localStorage`)  
- **Mobile‑first** responsive layout  
- **Fast load times** via CDN assets  
- **SEO‑ready**: descriptive meta tags, `sitemap.xml`, `robots.txt`  
- **Accessibility** by default (semantic HTML + ARIA)  
- **Static export** ready for GitHub Pages

## 🛠 Tech Stack
- **Backend**: FastAPI + Jinja2
- **Stylizacja**: Tailwind CSS (CDN)
- **Deployment**: GitHub Pages (static HTML files)
- **Icons**: SVG (inline)
- **Fonts**: Inter (Google Fonts)

## 📁 Project Structure
```text
.
|---- main.py           # FastAPI routes
|---- render_static.py  # Static-site generator
|---- templates/        # Jinja2 templates
|    |---- base.html
|    |---- about.html
|    |---- cv.html
|    |---- projects.html
|    |---- contact.htsm
|    |____ 404.html
|---- static/
|    |____ images/      # Images, favicons, css overrides
|---- site/             # Generated static html files (output)
|---- requirements.txt
|____ README.md     
```

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone <repository-url>
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Start a local dev server
```bash
uvicorn main:app --reload
```
alternatively run:
```bash
python main.py
```
Use browser and go to **http://loalhost:8000** 

### 4. Generate static HTML files
```bash
python render_static.py
```
The static files will occur in 'site/' folder and are ready for publishing

## 🌐 Deploying on GitHub Pages
### Manual Deployment
1. **Generate statis HTML files**
   ```bash
   python render_sttaic.py
   ```
2. **Create and push the github branch**
   ```bash
   git checkout --orphan [new_branch_name]   
   ```

3. **Configuration**
   ```bash
   git --work-tree=site add -A
   git commit -m "Deploy $(date +%F_%T)"
   git push -f origin [new_branch_name]
   ```
   Go to GitHub Settings/ Pages
   In 'Build and deployment' section choose 'Deploy from branch' option
   Set [new_branch_name] and /root folder,then save 
   
   


