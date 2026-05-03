import os
import json
import requests
import pandas as pd
from dotenv import load_dotenv


# Load environment config used by API-backed tools.
load_dotenv()

# Preload local IMDB dataset and external API key.
df = pd.read_csv("imdb_top_1000.csv")
imdb_key = os.getenv("IMDB_KEY")


def search_movie(title: str, plot: str):
    # Exact-title OMDb lookup with optional full plot.
    try:
        if plot == "short":
            response = requests.get(f"http://www.omdbapi.com/?t={title}&apikey={imdb_key}")
        elif plot == "full":
            response = requests.get(f"http://www.omdbapi.com/?t={title}&plot=full&apikey={imdb_key}")

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
    # OMDb keyword search that can return multiple matches.
    try:
        response = requests.get(f"http://www.omdbapi.com/?s={search_query}&apikey={imdb_key}")

        response.raise_for_status()

        data = response.json()
        if data.get("Response") == "False":
            return f"Movie not found: {data.get('Error', 'Unknown error')}"

        return json.dumps(data)

    except requests.exceptions.RequestException as e:
        return f"Network error when searching for '{search_query}': {str(e)}"
    except Exception as e:
        return f"Unexpected error: {str(e)}"


def get_top_movies_by_genre(genre: str, limit: int = 5):
    # Filter local dataset by genre and rank by rating.
    try:
        filtered = df[df["Genre"].str.contains(genre, case=False, na=False)].copy()

        if filtered.empty:
            return json.dumps(
                {
                    "genre": genre,
                    "count": 0,
                    "movies": [],
                    "message": f"No movies found for genre '{genre}'.",
                }
            )

        filtered = filtered.sort_values("IMDB_Rating", ascending=False)
        filtered = filtered.head(limit)

        result = filtered[
            ["Series_Title", "Released_Year", "Genre", "IMDB_Rating", "Director", "Overview"]
        ]

        return result.to_json(orient="records", force_ascii=True)
    except Exception as e:
        return f"Error: {str(e)}"


# Tool definitions exposed to the OpenAI Responses API.
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
    {
        "type": "function",
        "name": "get_top_movies_by_genre",
        "description": (
            "The tool returns multiple top-rated movies for the user's genre query. "
            "It is not title search; it filters the local dataset by genre and ranks by IMDB_Rating."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "genre": {
                    "type": "string",
                    "description": "Genre string to match in the Genre column.",
                },
                "limit": {
                    "type": "integer",
                    "description": "Max number of movies to return. Defaults to 5.",
                    "minimum": 1,
                },
            },
            "required": ["genre"],
        },
    },
]


# Runtime map from tool name to Python callable.
tool_registry = {
    "search_movie": search_movie,
    "search_movie_list": search_movie_list,
    "get_top_movies_by_genre": get_top_movies_by_genre,
}
