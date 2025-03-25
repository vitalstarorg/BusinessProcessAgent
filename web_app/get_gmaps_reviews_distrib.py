import base64
import json
import subprocess
import sys

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI


async def get_gmaps_reviews_distrib(screenshot_fpath: str):

    proc = subprocess.run(['python', 'crop_screenshot.py', screenshot_fpath])
    image_path = "screenshot_crop.png"
    with open(image_path, "rb") as image_file:
        image_data = base64.b64encode(image_file.read()).decode("utf-8")

    message = HumanMessage(
        content=[
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/png;base64,{image_data}"},
            },
        ],
    )

    BARCHART_SYSTEM_PROMPT = '''Analyze the image provided and based on the relative lengths of the barchart of review scores (the number of reviews that have been given from 1 to 5 stars), determine the distribution (i.e. percentages) of the review scores. Check your initial answer against each of the YELLOW bar lengths for 1 through 5 stars, and revise your estimated distribution if necessary. Finally output in the following (example) JSON format: {"_5_stars": 47, "_4_stars": 30, "_3_stars": 8, "_2_stars": 5, "_1_stars": 10}'''

    llm = ChatOpenAI(model='gpt-4o', temperature=0.0)
    response = await llm.ainvoke([SystemMessage(BARCHART_SYSTEM_PROMPT), message])

    def trim_to_braces(s):
        # Find the first '{' from the left
        left_index = s.find('{')
        # Find the last '}' from the right
        right_index = s.rfind('}')

        # If either brace isn't found, return an empty string (or handle as needed)
        if left_index == -1 or right_index == -1 or left_index > right_index:
            return ''

        # Return the substring from the first '{' to the last '}'
        return s[left_index : right_index + 1]

    if isinstance(response.content, str):
        json_str = trim_to_braces(response.content)
        print(json_str)


async def main():
    await get_gmaps_reviews_distrib(sys.argv[1])

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
