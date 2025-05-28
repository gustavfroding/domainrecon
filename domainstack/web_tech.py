import aiohttp
from bs4 import BeautifulSoup

async def inspect_https_site(domain):
    url = f"https://{domain}"
    headers = {
        "User-Agent": "domainrecon/0.1"
    }
    try:
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(url, timeout=8, ssl=False) as resp:
                status = resp.status
                server = resp.headers.get("Server", "")
                powered_by = resp.headers.get("X-Powered-By", "")
                html = await resp.text()

                tech = None
                if "wp-content" in html:
                    tech = "WordPress"
                elif "__REACT_DEVTOOLS_GLOBAL_HOOK__" in html:
                    tech = "React"
                elif "<div id=\"app\"" in html.lower() and "vue" in html.lower():
                    tech = "Vue"
                elif "ng-version" in html:
                    tech = "Angular"

                return True, status, server, powered_by, tech
    except Exception as e:
        return False, None, None, None, f"SSL fel: {e}"
