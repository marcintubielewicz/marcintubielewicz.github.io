import asyncio
import shutil
from pathlib import Path
from datetime import datetime

import aiofiles
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

from fastapi.testclient import TestClient
from main import app, projects_data


class StaticSiteGenerator:
    def __init__(self, output_dir: str = "site"):
        self.output_dir = Path(output_dir)
        self.client = TestClient(app)

    async def setup_output_directory(self):
        if self.output_dir.exists():
            shutil.rmtree(self.output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        logger.info("Created output directory: %s", self.output_dir)

    async def copy_static_files(self):
        static_src = Path("static")
        if static_src.exists():
            static_dest = self.output_dir / "static"
            shutil.copytree(static_src, static_dest)
            logger.info("Copied static files to: %s", static_dest)
        else:
            logger.info("No static directory found, skipping...")

    async def render_route(self, route_path: str, output_filename: str):
        try:
            response = self.client.get(route_path)
            if response.status_code == 200:
                output_path = self.output_dir / output_filename

                async with aiofiles.open(output_path, "w", encoding="utf-8") as f:
                    await f.write(response.text)

                logger.info("Rendered %s --> %s", route_path, output_filename)
                return True
            else:
                logger.info(
                    "Failed to render %s: HTTP %s", route_path, response.status_code
                )
                return False
        except Exception as e:
            logger.info("Error rendering %s: %s", route_path, e)
            return False

    async def render_404_page(self):
        try:
            response = self.client.get("/non-existent-page")
            if response.status_code == 404:
                output_path = self.output_dir / "404.html"

                async with aiofiles.open(output_path, "w", encoding="utf-8") as f:
                    await f.write(response.text)

                logger.info("Rendered 404 page -> 404.html")
                return True
            else:
                logger.info(
                    "Unexpected status code for 404 page: %s", response.status_code
                )
                return False
        except Exception as e:
            logger.info("Error rendering 404 page: %s", e)
            return False

    async def create_cname_file(self, domain: str = None):
        if domain:
            cname_path = self.output_dir / "CNAME"
            async with aiofiles.open(cname_path, "w") as f:
                await f.write(domain)
            logger.info("Created CNAME file for domain: %s", domain)

    async def create_nojekyll_file(self):
        nojekyll_path = self.output_dir / ".nojekyll"
        async with aiofiles.open(nojekyll_path, "w") as f:
            await f.write("")
        logger.info("Created .nojekyll file")

    async def generate_sitemap(self):
        base_url = "https://marcintubielewicz.github.io"
        current_date = datetime.now().strftime("%Y-%m-%d")

        sitemap_content = f"""<?xml version="1.0" encoding="UTF-8"?>
                            <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
                                <url>
                                    <loc>{base_url}/</loc>
                                    <lastmod>{current_date}</lastmod>
                                    <changefreq>monthly</changefreq>
                                    <priority>1.0</priority>
                                </url>
                                <url>
                                    <loc>{base_url}/cv</loc>
                                    <lastmod>{current_date}</lastmod>
                                    <changefreq>monthly</changefreq>
                                    <priority>0.8</priority>
                                </url>
                                <url>
                                    <loc>{base_url}/projects</loc>
                                    <lastmod>{current_date}</lastmod>
                                    <changefreq>weekly</changefreq>
                                    <priority>0.9</priority>
                                </url>
                                <url>
                                    <loc>{base_url}/contact</loc>
                                    <lastmod>{current_date}</lastmod>
                                    <changefreq>monthly</changefreq>
                                    <priority>0.7</priority>
                                </url>
                            </urlset>"""

        sitemap_path = self.output_dir / "sitemap.xml"
        async with aiofiles.open(sitemap_path, "w", encoding="utf-8") as f:
            await f.write(sitemap_content)
        logger.info("Generated sitemap.xml")

    async def generate_robots_txt(self):
        """Generate robots.txt file."""
        robots_content = """User-agent: *
                        Allow: /

                        Sitemap: https://marcintubielewicz.github.io/sitemap.xml
                        """

        robots_path = self.output_dir / "robots.txt"
        async with aiofiles.open(robots_path, "w") as f:
            await f.write(robots_content)
        logger.info("Generated robots.txt")

    async def generate_site(self, custom_domain: str = None):
        logger.info(
            """Starting static site generation...
            Found %s projects to include""",
            len(projects_data),
        )

        await self.setup_output_directory()
        await self.copy_static_files()

        routes = [
            ("/", "index.html"),
            ("/cv", "cv.html"),
            ("/projects", "projects.html"),
            ("/contact", "contact.html"),
        ]

        success_count = 0
        for route_path, output_filename in routes:
            if await self.render_route(route_path, output_filename):
                success_count += 1

        if await self.render_404_page():
            success_count += 1

        await self.create_nojekyll_file()
        await self.generate_sitemap()
        await self.generate_robots_txt()

        if custom_domain:
            await self.create_cname_file(custom_domain)

        total_pages = len(routes) + 1  # +1 for 404 page
        logger.info(
            """\nGeneration Summary:
                    Successfully rendered: %s/%s pages
                    Output directory: %s
                    Total files: %s
                    """,
            success_count,
            total_pages,
            self.output_dir.absolute(),
            len(list(self.output_dir.rglob("*"))),
        )

        if success_count == total_pages:
            logger.info(
                """\nStatic site generation completed successfully!
                        Ready for deployment to GitHub Pages!
                        \nNext steps:
                        1. Copy contents of '%s' to your gh-pages branch
                        2. Push to GitHub
                        3. Enable GitHub Pages in repository settings
                        """,
                self.output_dir,
            )
        else:
            logger.info("\nSome pages failed to render. Check the errors above.")

        return success_count == total_pages


async def main():
    generator = StaticSiteGenerator()

    # Optional: Set custom domain
    # custom_domain = "your-domain.com"
    custom_domain = None

    success = await generator.generate_site(custom_domain)

    if not success:
        exit(1)


if __name__ == "__main__":
    asyncio.run(main())
