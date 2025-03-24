import base64

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

SYSTEM_PROMPT = '''Analyze the image provided and based on the relative lengths of the barchart of review scores (the number of reviews that have been given from 1 to 5 stars), determine the distribution (i.e. percentages) of the review scores.

Check your initial answer against each of the YELLOW bar lengths for 1 through 5 stars, and revise your estimated distribution if necessary.

Finally output in the following (example) JSON format:
{
    "5_stars": 47,
    "4_stars": 30,
    "3_stars": 8,
    "2_stars": 5,
    "1_star": 10
}'''

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

llm = ChatOpenAI(model='gpt-4o', temperature=0.0)
response = llm.invoke([SystemMessage(SYSTEM_PROMPT), message])
print(response.content)
