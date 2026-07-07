from locust import task, between
from locust_plugins.users.playwright import PlaywrightUser, pw

# Real browser sessions actually clicking and navigating wasscetutor.com


class RealUserSession(PlaywrightUser):
    host = "https://wasscetutor.com"
    wait_time = between(2, 5)
    headless = True  # set False locally if you want to watch it click around

    @task
    @pw
    async def browse_and_click(self, page):
        # Load real homepage
        await page.goto("/")
        await page.wait_for_load_state("networkidle")

        # Try to find and click a real nav link (adjust selector to your actual UI)
        try:
            link = page.get_by_role("link").first
            await link.click(timeout=5000)
            await page.wait_for_load_state("networkidle")
        except Exception:
            pass

        await page.wait_for_timeout(1000)

    @task
    @pw
    async def visit_dashboard(self, page):
        await page.goto("/dashboard")
        await page.wait_for_load_state("networkidle")
        await page.wait_for_timeout(1000)
