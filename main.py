from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import os

app = FastAPI()

templates = Jinja2Templates(directory="templates")

if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

projects_data = [
    {
        "title": "Portfolio Website",
        "description": "Lightweight portfolio website built with FastAPI and Jinja2",
        "technologies": ["FastAPI", "Jinja2", "Tailwind CSS"],
        "github_url": "https://github.com/username/portfolio-website",
        "demo_url": None,
    }
]


@app.get("/", response_class=HTMLResponse)
async def about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})


@app.get("/projects", response_class=HTMLResponse)
async def projects(request: Request):
    return templates.TemplateResponse(
        "projects.html", {"request": request, "projects": projects_data}
    )


@app.get("/contact", response_class=HTMLResponse)
async def contact(request: Request):
    return templates.TemplateResponse("contact.html", {"request": request})


@app.get("/cv", response_class=HTMLResponse)
async def cv(request: Request):
    return templates.TemplateResponse("cv.html", {"request": request})


@app.exception_handler(404)
async def not_found(request: Request, exc: Exception):
    return templates.TemplateResponse("404.html", {"request": request})


def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


if __name__ == "__main__":
    import uvicorn
    import socket

    def find_free_port(start_port: int = 8000, end_port: int = 9000):
        for port in range(start_port, end_port + 1):
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                try:
                    s.bind(("", port))
                    return port
                except OSError:
                    continue
        raise RuntimeError(f"No free port found in range {start_port}-{end_port}")

    port = find_free_port()
    uvicorn.run(app, host="0.0.0.0", port=port)
