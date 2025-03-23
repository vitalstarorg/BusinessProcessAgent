import asyncio
import base64

from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig


async def main():
    browser_config = BrowserConfig(
        headless=False,
        proxy="",
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
