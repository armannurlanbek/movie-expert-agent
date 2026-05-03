from openai import OpenAI
import os
from dotenv import load_dotenv
import json
import requests


load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
imdb_key = os.getenv("IMDB_KEY")

def search_movie(title: str, plot: str):
    try:
        if plot == "short":
            response = requests.get(f'http://www.omdbapi.com/?t={title}&apikey={imdb_key}')
        elif plot == "full":
            response = requests.get(f'http://www.omdbapi.com/?t={title}&plot=full&apikey={imdb_key}')
        
        response.raise_for_status()

        data = response.json()

        if data.get("Response") == "False":
            return f"Movie not found: {data.get('Error', 'Unknown error')}"

        return json.dumps(data)
    
    except requests.exceptions.RequestException as e:
        return f"Network error when searching for '{title}': {str(e)}"
    except Exception as e:
        return f"Unexpected error: {str(e)}"

def search_movie_list(search_query: str):
    try:
        response = requests.get(f'http://www.omdbapi.com/?s={search_query}&apikey={imdb_key}')

        response.raise_for_status()

        data = response.json()
        if data.get("Response") == "False":
            return f"Movie not found: {data.get('Error', 'Unknown error')}"

        return json.dumps(data)
    
    except requests.exceptions.RequestException as e:
        return f"Network error when searching for '{search_query}': {str(e)}"
    except Exception as e:
        return f"Unexpected error: {str(e)}"

tools = [
    {
        "type": "function",
        "name": "search_movie",
        "description": (
            "Find a movie by title using the OMDb API. "
            "Returns JSON with movie metadata. "
            "Use plot='short' unless the user explicitly wants a long plot summary, then use plot='full'."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "Movie title to look up.",
                },
                "plot": {
                    "type": "string",
                    "enum": ["short", "full"],
                    "description": "Plot detail level: 'short' (default) or 'full'.",
                },
            },
            "required": ["title", "plot"],
        },
    },
    {
        "type": "function",
        "name": "search_movie_list",
        "description": (
            "Give multiple movie results for a user query using the OMDb search endpoint. "
            "This is not exact title lookup; it returns a list of matching results."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "search_query": {
                    "type": "string",
                    "description": "Free-text query to get a list of matching movies.",
                }
            },
            "required": ["search_query"],
        },
    },
]

tool_registry = {
    "search_movie": search_movie,
    "search_movie_list": search_movie_list
}

input_list = []

while True:
    user_input = input("Ask a question...")
    input_list.append({"role": "user", "content": f"{user_input}"})
    while True:

        response = client.responses.create(
            model = "gpt-4o-mini",
            instructions = "You are a movie expert. Answer questions about movies",
            input = input_list,
            tools = tools
        )
        input_list += response.output


        tool_calls = [item for item in response.output if item.type == "function_call"]

        if not tool_calls:
            break

        for item in tool_calls:
            if item.name == "search_movie":
                title = json.loads(item.arguments)["title"]
                plot = json.loads(item.arguments)["plot"]
                movie = search_movie(title, plot)

                input_list.append({
                    "type": "function_call_output",

                    "call_id": item.call_id,
                    "output": movie
                })
    
    print("Final answer: " + response.output_text)

    if len(input_list) > 11:
        # oldest_messages = input_list[0:4]
        # sum_response = client.responses.create(
        #     model = "gpt-4o-mini",
        #     instructions = f"You are AI agent summarizer. Your task is to summarize the oldest 5 messages into one summarized message.",
        #     input = f"Summarize these messages: {oldest_messages}"
        # )

        # del input_list[0:4]
        # input_list.insert(0, {"role": "user", "content": f"Summary of earlier conversation: {sum_response.output_text}"})

        user_indices = [i for i, m in enumerate(input_list) 
                if isinstance(m, dict) and m.get("role") == "user"]

        if len(user_indices) >= 3:
            cut_at = user_indices[2]  # keep last 2 turns intact
            messages_to_summarize = input_list[:cut_at]
            messages_to_keep = input_list[cut_at:]

            sum_response = client.responses.create(
                model = "gpt-4o-mini",
                instructions = f"You are AI agent summarizer. Your task is to summarize the oldest 5 messages into one summarized message.",
                input = f"Summarize these messages: {messages_to_summarize}"
        )
            summary_msg = {"role": "user", "content": f"Summary of earlier conversation: {sum_response.output_text}"}
            input_list[:] = [summary_msg] + messages_to_keep
