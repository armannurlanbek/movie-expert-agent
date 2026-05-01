from openai import OpenAI
import os
from dotenv import load_dotenv
from agents import Agent, Runner
from openai.types.responses import response

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

tools = [
    {
        "type": "function",
        "name": "search_movie",
        "description": "Search for a movie by title",
        "parameters": {
            "type": "object",
            "properties": {"title": {"type": "string"}},
            "required": ["title"]
        }
    }
]

def search_movie(title: str):
    return f"{title}: one of the best movies of all time maaan"

input_list = [
    {"role": "user", "content": "Search up the titanic movie using search_movie tool"}
]


response = client.responses.create(
    model = "gpt-4o-mini",   
    instructions = "You are a movie expert. You are given a question about movies and you need to answer it.",   
    input = input_list,
    tools = tools, 
    )

input_list += response.output

for item in response.output:
    if item == "function_call":
        if item.name == "search_movie":
            title = json.loads(item.arguments)["sign"]
            movie = search_movie(title)

            input_list.append({
                "type": "function_call_output",
                "call_id": item.call_id,
                "output": movie,
            })

print("Final output: ")
print(input_list)
print(response.model_dump_json(indent=2))
print(response.output_text)



