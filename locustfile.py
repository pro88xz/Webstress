import re
import random
from locust import HttpUser, task, between


class SiteVisitor(HttpUser):
    """Real user simulation: hits actual homepage + real static assets served by Vercel."""
    wait_time = between(2, 5)
    host = "https://wasscetutor.com"

    def on_start(self):
        self.asset_paths = []

    @task(3)
    def homepage(self):
        resp = self.client.get("/", name="/")
        if resp.status_code == 200 and not self.asset_paths:
            found = re.findall(r'(?:src|href)="(/assets/[^"]+\.(?:js|css))"', resp.text)
            self.asset_paths = list(set(found))

    @task(2)
    def load_assets(self):
        if self.asset_paths:
            path = random.choice(self.asset_paths)
            self.client.get(path, name="/assets/[bundle]")

    @task(1)
    def robots_and_sitemap(self):
        self.client.get("/robots.txt", name="/robots.txt")
        self.client.get("/sitemap.xml", name="/sitemap.xml")
