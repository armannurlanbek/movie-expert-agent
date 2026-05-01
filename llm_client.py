from openai import OpenAI
import os
from dotenv import load_dotenv
from agents import Agent, Runner
from openai.types.responses import response

load_dotenv()

client = OpenAI()
def chat(messages, tools=None) -> response:
    response = client.responses.create(
        model = "gpt-5.4",
        tools = tools,
        input = messages,
    )

    return response.output_text

