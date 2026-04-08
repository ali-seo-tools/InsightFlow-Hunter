import asyncio
from playwright.async_api import async_playwright

async def universal_power_hunter(niche, location, limit=10):
    leads_list = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        # Power Search Query
        search_url = f"https://www.google.com/search?q=intitle:{niche}+{location}+website"
        await page.goto(search_url)
        
        # Links Extracting
        links = await page.eval_on_selector_all("a", "elements => elements.map(e => e.href)")
        unique_links = list(set([l for l in links if "http" in l and "google" not in l]))[:limit]
        
        for link in unique_links:
            try:
                await page.goto(link, timeout=10000)
                content = await page.content()
                
                # Tracking Audit Logic
                ga4 = "Found ✅" if "gtag" in content else "Missing ❌"
                gtm = "Found ✅" if "googletagmanager" in content else "Missing ❌"
                
                leads_list.append({"Website": link, "GA4 Status": ga4, "GTM Status": gtm})
            except:
                continue
                
        await browser.close()
        return leads_list
