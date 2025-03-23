import asyncio
import base64

from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig


async def main():
    browser_config = BrowserConfig(
        headless=False,
        # proxy="https=http://4a2c95f7e7dbafd7dee53c029bba07f9dc148f60:@api.zenrows.com:8001",
        proxy="https=http://brd-customer-hl_b414dc3e-zone-datacenter_proxy1:e97biz27iakn@brd.superproxy.io:33335",
    )
    # async with AsyncWebCrawler() as crawler:
    async with AsyncWebCrawler(config=browser_config) as crawler:
        result = await crawler.arun(
            # url="https://docs.crawl4ai.com",
            # url="https://www.example.com",
            # url="https://www.expedia.com",
            url="https://www.tripadvisor.com",
            config=CrawlerRunConfig(
                # screenshot=True,
            ),
        )
        if result.screenshot:
            with open("page.png", "wb") as f:
                f.write(base64.b64decode(result.screenshot))
        if result.markdown:
            print(result.markdown)
            with open("page.md", "w") as f:
                f.write(result.markdown)
        # breakpoint()  # fmt: skip


if __name__ == "__main__":
    asyncio.run(main())
