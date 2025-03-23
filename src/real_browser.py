import asyncio
import subprocess

from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI

from browser_use import Agent
from browser_use.browser.browser import Browser, BrowserConfig, BrowserContextConfig


async def main():
    browser = Browser(
        config=BrowserConfig(
            _force_keep_browser_alive=True,
            browser_instance_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
            extra_browser_args=[
                # '--profile-directory="Default"',
                # '--proxy-server="https=http://"
            ],
            # cdp_url='wss://'
            # cdp_url='wss://'
            # new_context_config=BrowserContextConfig(
            #     minimum_wait_page_load_time=1.0,
            #     maximum_wait_page_load_time=7,
            #     user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
            # ),
        )
    )

    # llm = ChatAnthropic(
    #     model_name='claude-3-7-sonnet-20250219', temperature=0.0, timeout=30, stop=None
    # )
    # llm = ChatOpenAI(model='gpt-4o')
    llm = ChatGoogleGenerativeAI(model='gemini-2.0-flash')

    # company = 'Blue Mermaid Restaurant (Jefferson St, San Francisco, CA)'
    # company = 'Fogo Brazilian Steakhouse (S. 3rd St, San Francisco, CA)'
    company = 'Eight Am (Columbus Ave, San Francisco, CA)'
    # company = 'Spirit Airlines'
    # company = 'United Airlines'
    # company = 'EVA Air'
    # company = 'Ryanair'

    browser_context = await browser.new_context()

    agent = Agent(
        # task='Go to https://www.example.com',
        # task='Go to "https://arh.antoinevastel.com/bots/areyouheadless"',
        # task=f'Go to www.tripadvisor.com . Search for "{company}". Tell how many reviews there are for it.',
        # task=f'Go to www.tripadvisor.com . Search for "{company}". Tell me: #1. How many reviews there are; #2. What the average review score is; #3. How many reviewers rated it Excellent / Very good / Average / Poor / Terrible;  #4. Read the first three reviews in full and summarize each one.',
        # task=f'Go to www.dnb.com/business-directory.html . Search for "{company}". Click on "Financial Statements". Tell me the Net Income.',
        task=f'Go to "https://google.com/maps". Search for "{company}", then click on the "Reviews" tab selector. Tell me: #1. How many reviews there are in total; #2. What the average review score is.',
        llm=llm,
        browser=browser,
        browser_context=browser_context,  # Pass the browser context to the agent
    )
    await agent.run()

    screenshot_path = "browser_screenshot.png"
    page = await browser_context.get_current_page()
    await page.screenshot(path=screenshot_path)
    print(f"Screenshot saved to {screenshot_path}")

    await browser_context.close()
    await browser.close()

    proc = await asyncio.create_subprocess_exec(
        'python', 'crop_screenshot.py', screenshot_path
    )
    await proc.communicate()


if __name__ == '__main__':
    asyncio.run(main())
