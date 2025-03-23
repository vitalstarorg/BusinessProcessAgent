import asyncio
from playwright.async_api import async_playwright

SBR_WS_CDP = f'wss://'

async def run(pw):
    print(f'Connecting to Scraping Browser at {SBR_WS_CDP}')
    browser = await pw.chromium.connect_over_cdp(SBR_WS_CDP)
    try:
        print('Connected! Navigating...')
        return
        page = await browser.new_page()
        # await page.goto('https://example.com', timeout=2 * 60 * 1000)
        await page.goto('https://tripadvisor.com', timeout=2 * 60 * 1000)
        # print('Taking page screenshot to file page.png')
        # await page.screenshot(path='./page.png', full_page=True)
        print('Navigated! Scraping page content...')
        html = await page.content()
        print(html)
        # CAPTCHA solving: If you know you are likely to encounter a CAPTCHA on your target page, add the following few lines of code to get the status of Scraping Browser's automatic CAPTCHA solver
        # Note 1: If no captcha was found it will return not_detected status after detectTimeout
        # Note 2: Once a CAPTCHA is solved, if there is a form to submit, it will be submitted by default
        # client = await page.context.new_cdp_session(page)
        # solve_result = await client.send('Captcha.solve', { 'detectTimeout': 30*1000 })
        # status = solve_result['status']
        # print(f'Captcha solve status: {status}')
    finally:
        await browser.close()


async def main():
    playwright = await async_playwright().start()
    await run(playwright)
    # async with async_playwright() as playwright:
    #     await run(playwright)


if __name__ == '__main__':
    asyncio.run(main())
