#Tools for agent
from agents import function_tool


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


@function_tool
def search_movie_list(query: str):
    return None

@function_tool
def compare_movies(title1: str, title2: str):
    return None

@function_tool
def get_movies_by_genre(genre: str):
    return None

@function_tool
def filter_by_rating(min_rating:int):
    return Non


