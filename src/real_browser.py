import asyncio
import base64
import json
import logging
from typing import List, Optional, TypedDict

from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from pydantic import BaseModel

from browser_use import Agent, Controller
from browser_use.browser.browser import Browser, BrowserConfig
from browser_use.browser.context import BrowserContext, BrowserContextConfig

load_dotenv()
logger = logging.getLogger(__name__)


class TripAdvisorResult(BaseModel):
    class TripAdvisorReviewsDistribution(TypedDict):
        Excellent: int
        Very_good: int
        Average: int
        Poor: int
        Terrible: int

    total_num_reviews: int
    average_review_score: str
    reviews_score_distribution: TripAdvisorReviewsDistribution
    customer_reviews: List[str]


class GoogleMapsResult(BaseModel):
    class GoogleMapsReviewsDistribution(TypedDict):
        _5_stars: int
        _4_stars: int
        _4_stars: int
        _2_stars: int
        _1_stars: int

    total_num_reviews: int
    average_review_score: str
    customer_reviews: List[str]
    reviews_score_distribution: Optional[GoogleMapsReviewsDistribution]


# controller = Controller()
controller = Controller(output_model=TripAdvisorResult)
# controller = Controller(output_model=GoogleMapsResult)


@controller.action('Take a screenshot and save it as file_name')
async def take_screenshot(file_name: str, browser: BrowserContext):
    page = await browser.get_current_page()
    # file_name = f'{sum(ord(c) for c in page.url) % 0xFFF:03X}.png'
    await page.screenshot(path=file_name)
    logger.info(f'Saved screenshot of {page.url} to {file_name}')
    return f'Successfully took screenshot and saved as {file_name}'
    # return ActionResult(extracted_content='Success')


async def main():
    browser = Browser(
        config=BrowserConfig(
            # _force_keep_browser_alive=True,
            browser_instance_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
            extra_browser_args=[
                # '--profile-directory="Default"',
                # '--proxy-server="https=http://"
            ],
            # cdp_url='wss://'
            # cdp_url='wss://'
            new_context_config=BrowserContextConfig(
                minimum_wait_page_load_time=2.0,
                maximum_wait_page_load_time=7,
                user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
            ),
        )
    )

    llm = ChatOpenAI(model='gpt-4o', temperature=0.0)
    # llm = ChatAnthropic(
    #     model_name='claude-3-7-sonnet-latest', temperature=0.0, timeout=60, stop=None
    # )
    # llm = ChatGoogleGenerativeAI(model='gemini-2.0-flash', temperature=0.0)

    company, location = 'Blue Mermaid Restaurant', 'Jefferson St, San Francisco, CA'
    # company, location = 'Fogo Brazilian Steakhouse', 'S. 3rd St, San Francisco, CA'
    # company, location = 'Eight Am', 'Columbus Ave, San Francisco, CA'

    # company = 'Spirit Airlines'
    # company = 'United Airlines'
    # company = 'EVA Air'
    # company = 'Ryanair'

    # fmt: off
    tasks = [
        f'Go to "https://www.example.com". Take a screenshot and save it as "screenshot.png".',
        f'Go to "https://httpbin.io". Take a screenshot.',
        f'Go to "https://www.tripadvisor.com". Search for "{company}", which is located on ({location}), then click on the "Reviews" tab selector. Find out how many reviews there are for it.',
        f'Go to "https://www.tripadvisor.com". Search for "{company}", which is located on ({location}), then click on the "Reviews" tab. Find out: #1. How many reviews there are; #2. What the average review score is; #3. How many reviewers rated it Excellent / Very good / Average / Poor / Terrible;  #4. Read the first three reviews (clicking on "Read more" if necessary to see the full review) and summarize each one, ignoring the management response (if any).',
        f'Go to "https://google.com/maps". Search for "{company} ({location})", then click on the "Reviews" tab. Take a screenshot and save it as "screenshot.png".',
        f'Go to "https://google.com/maps". Search for "{company} ({location})", then click on the "Reviews" tab. Take a screenshot and save it as "screenshot.png". Find out: #1. How many reviews there are in total; #2. What the average review score is.; #3. Read the first three reviews (clicking on "More" if necessary to see the full review) and summarize each one.',
        f'Go to "www.dnb.com/business-directory.html". Search for "{company}". Click on "Financial Statements". Find out their Net Income.',
    ]
    # fmt: on

    agent = Agent(
        llm=llm,
        browser=browser,
        task=tasks[3],
        controller=controller,
        max_failures=2,
    )
    history = await agent.run()
    final_result_str = history.final_result()
    logger.info(final_result_str)

    # Tasks: 4, 5
    # final_result_str = await get_gmaps_reviews_distrib(final_result_str)
    # logger.info(final_result_str)


async def get_gmaps_reviews_distrib(final_result_str: str | None):
    if not final_result_str:
        return
    final_result_dict = json.loads(final_result_str)

    if not final_result_dict:
        return

    proc = await asyncio.create_subprocess_exec(
        'python',
        'get_gmaps_reviews_distrib.py',
        'screenshot.png',
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    json_str, stderr = await proc.communicate()
    if not json_str:
        return

    # logger.info(json_str)
    final_result_dict['reviews_score_distribution'] = json.loads(json_str)
    return json.dumps(final_result_dict)


if __name__ == '__main__':
    asyncio.run(main())
