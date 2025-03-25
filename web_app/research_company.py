#!/usr/bin/env python3

import logging
import sys

logging.basicConfig(filename=f'log_{sys.argv[3]}.txt', filemode='w', level=logging.INFO)
logger = logging.getLogger(__name__)

import asyncio
import json
import subprocess
from string import Template
from typing import List, Optional, TypedDict

from browser_use import Agent, Controller
from browser_use.browser.browser import Browser, BrowserConfig
from browser_use.browser.context import BrowserContext, BrowserContextConfig
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from pydantic import BaseModel

CHROME_BROWSER_PATH = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
MIN_WAIT_PAGE_LOAD_TIME = 2.0
MAX_WAIT_PAGE_LOAD_TIME = 6.0
WAIT_BETWEEN_ACTIONS = 1.0
VIEWPORT_EXPANSION = 300
LLM_PROVIDER = ['OpenAI', 'Anthropic', 'Google'][0]
LLM_TEMPERATURE = 0.1
MAX_STEPS_FAILURE = 2

# fmt: off
PROMPT_TRIPADVISOR = 'Go to "https://www.tripadvisor.com". Search for "$company" (if there are multiple matches, know that is located in: $location), then click on the "Reviews" tab. Find out: #1. How many reviews there are; #2. What the average review score is; #3. How many reviewers rated it Excellent / Very good / Average / Poor / Terrible;  #4. Read the first 3 reviews (be sure to click on the "Read more" link for each review first, if there is one) and summarize each one in about five sentences, ignoring the management response (if any).'

PROMPT_GOOGLEMAPS = 'Go to "https://google.com/maps". Search for "$company ($location)", then click on the "Reviews" tab. Take a screenshot and save it as "screenshot.png". Find out: #1. How many reviews there are in total; #2. What the average review score is.; #3. Read the first 3 reviews (be sure to click on the "More" link for each review first, if there is one) and summarize each one (just the reviewer written comments) in about five sentences.'

PROMPT_TEST = 'Go to "https://www.example.com". Take a screenshot and save it as "screenshot.png".'
# fmt: on

load_dotenv()


class TripAdvisorResult(BaseModel):
    class TripAdvisorReviewsDistribution(TypedDict):
        Excellent: int
        Very_good: int
        Average: int
        Poor: int
        Terrible: int

    total_num_reviews: int
    average_review_score: float
    reviews_score_distribution: TripAdvisorReviewsDistribution
    customer_reviews: List[str]


class GoogleMapsResult(BaseModel):
    class GoogleMapsReviewsDistribution(TypedDict):
        _5_stars: int
        _4_stars: int
        _3_stars: int
        _2_stars: int
        _1_stars: int

    total_num_reviews: int
    average_review_score: float
    customer_reviews: List[str]
    reviews_score_distribution: Optional[GoogleMapsReviewsDistribution]


def generate_research_data_mock(company, location, info_provider):
    """Generate mock research data for the given company"""
    if info_provider == 1:
        info_provider = 'TripAdvisor'
        info = {
            "Average Reviews Score": 4.5,
            "Reviews Scores Distrib": {
                "5_stars": 41,
                "4_stars": 32,
                "3_stars": 12,
                "2_stars": 5,
                "1_stars": 10,
            },
            "Sample Reviews": [
                "Great experience with this company!",
                "Good service but a bit pricey.",
                "Would recommend to others.",
            ],
        }
    elif info_provider == 2:
        info_provider = 'Google Maps'
        info = {
            "Average Reviews Score": 5.6,
            "Reviews Scores Distrib": {
                "5_stars": 31,
                "4_stars": 22,
                "3_stars": 12,
                "2_stars": 15,
                "1_stars": 20,
            },
            "Sample Reviews": [
                "Excellent customer service.",
                "The staff was very helpful.",
                "Quick response to our inquiry.",
            ],
        }
    else:
        print(f"ERROR: Unrecognized info_provider => {info_provider}")
        sys.exit(3)
    logger.info('DONE!')
    result = {
        "Company": company,
        "Location": location,
        "InfoProvider": info_provider,
        "Info": info,
    }
    print(json.dumps(result, indent=2))


async def generate_research_data(company, location, info_provider):
    if False:  # [[DEBUG]]
        company, location = 'Blue Mermaid Restaurant', 'Jefferson St, San Francisco, CA'
        # company, location = 'Fogo Brazilian Steakhouse', 'S. 3rd St, San Francisco, CA'
        # company, location = 'Eight Am', 'Columbus Ave, San Francisco, CA'

    browser = Browser(
        config=BrowserConfig(
            # browser_instance_path=CHROME_BROWSER_PATH,
            chrome_instance_path=CHROME_BROWSER_PATH,
            new_context_config=BrowserContextConfig(
                minimum_wait_page_load_time=MIN_WAIT_PAGE_LOAD_TIME,
                maximum_wait_page_load_time=MAX_WAIT_PAGE_LOAD_TIME,
                wait_between_actions=WAIT_BETWEEN_ACTIONS,
                viewport_expansion=VIEWPORT_EXPANSION,
            ),
        )
    )

    match LLM_PROVIDER:
        case 'OpenAI':
            llm = ChatOpenAI(model='gpt-4o', temperature=LLM_TEMPERATURE)
        case 'Anthropic':
            llm = ChatAnthropic(
                model_name='claude-3-7-sonnet-latest',
                temperature=LLM_TEMPERATURE,
                timeout=60,
                stop=None,
            )
        case 'Google':
            llm = ChatGoogleGenerativeAI(model='gemini-2.0-flash', temperature=LLM_TEMPERATURE)
        case _:
            print(f"ERROR: Invalid LLM Provider => {LLM_PROVIDER}")
            sys.exit(4)

    match info_provider:
        case 0:
            template = Template(PROMPT_TEST)
            controller = Controller()
        case 1:
            template = Template(PROMPT_TRIPADVISOR)
            controller = Controller(output_model=TripAdvisorResult)
        case 2:
            template = Template(PROMPT_GOOGLEMAPS)
            controller = Controller(output_model=GoogleMapsResult)
        case _:
            print(f"ERROR: Invalid info_provide => {info_provider}")
            sys.exit(4)

    @controller.action('Take a screenshot and save it as file_name')
    async def take_screenshot(file_name: str, browser: BrowserContext):
        page = await browser.get_current_page()
        await page.screenshot(path=file_name)
        logger.info(f'Saved screenshot of {page.url} to {file_name}')
        return f'Successfully took screenshot and saved as {file_name}'

    task = template.substitute({'company': company, 'location': location})

    agent = Agent(
        llm=llm,
        browser=browser,
        task=task,
        controller=controller,
        max_failures=MAX_STEPS_FAILURE,
    )
    history = await agent.run()
    final_result_str = history.final_result()
    # final_result_str = '''{"total_num_reviews": 1810, "average_review_score": "4.6", "customer_reviews": ["I went here twice, once on a whim and the second time with determination to try the French toast while on vacation. I\u2019ve been to lots of little brunch places in my life and I think this ranks as my top homey place. It\u2019s not anything special \u2026"], "reviews_score_distribution": {"_5_stars": 0, "_4_stars": 0, "_3_stars": 0, "_2_stars": 0, "_1_stars": 0}}'''  # [[DEBUG]]

    if info_provider == 2:
        final_result_str = get_gmaps_reviews_distrib(final_result_str)

    print(final_result_str)


def get_gmaps_reviews_distrib(final_result_str: str | None):
    if not final_result_str:
        return
    final_result_dict = json.loads(final_result_str)

    if not final_result_dict:
        return

    result = subprocess.run(
        [sys.executable, 'get_gmaps_reviews_distrib.py', 'screenshot.png'],
        capture_output=True,
        text=True,
    )
    json_str = result.stdout
    if not json_str:
        print(f'ERROR: get_gmaps_reviews_distrib.py => {json_str}')
        return final_result_str

    final_result_dict['reviews_score_distribution'] = json.loads(json_str)
    return json.dumps(final_result_dict)


async def main():
    if len(sys.argv) < 4:
        print(f"ERROR: Not enough arguments => {len(sys.argv) - 1}")
        sys.exit(1)

    company_name = sys.argv[1]
    company_loc = sys.argv[2]
    try:
        info_provider = int(sys.argv[3])
    except:
        print(f"ERROR: Argument #3 must be an int => {sys.argv[3]}")
        sys.exit(2)
    # research_data = generate_research_data_mock(company_name, company_loc, info_provider)
    research_data = await generate_research_data(company_name, company_loc, info_provider)


if __name__ == "__main__":
    asyncio.run(main())
