# Movie Expert Agent

A Python CLI movie assistant powered by OpenAI Responses API, OMDb API, and a local IMDb dataset (`imdb_top_1000.csv`).

## Implementation Variant
Variant 3 - custom framework (coefficient 1.2)

Implemented without LangChain:
- agent loop with printed reasoning
- memory (conversation history + summarization)
- tool dispatch
- 

## Installation
1. `pip install -r requirements.txt`
2. Copy `.env.example` to `.env` and fill in your keys
3. Place `imdb_top_1000.csv` in the project folder
4. `python agent.py`

## Environment Variables
- `OPENAI_API_KEY` - your OpenAI API key
- `IMDB_KEY` - your OMDb API key

## Tools
- `search_movie` - search one movie by title (OMDb API)
- `search_movie_list` - search a list of movies (OMDb API)
- `get_top_movies_by_genre` - get top movies by genre from Kaggle CSV

## Dialogue Examples

The following examples are taken from the actual run in `dialogue_test.md`.
The file `dialogue_test.md` contains a copy-paste transcript of the dialogue session.

### Example 1: Top 10 action movies + compare top 2
**User input**
`Please give me top 10 action movies and then search up top 2 and compare them`

**Tool calls**
- `get_top_movies_by_genre({'genre': 'action', 'limit': 10})`
- `search_movie({'title': 'The Dark Knight', 'plot': 'full'})`
- `search_movie({'title': 'The Lord of the Rings: The Return of the King', 'plot': 'full'})`

**Final answer (excerpt)**
- Top list includes: `The Dark Knight`, `The Lord of the Rings: The Return of the King`, `Inception`, `The Matrix`, and others.
- Comparison includes runtime, genre, director, cast, IMDb rating, awards, and box office.

### Example 2: Spider-Man movie list
**User input**
`Give me list of spider man movies`

**Tool call**
- `search_movie_list({'search_query': 'Spider-Man'})`

**Final answer (excerpt)**
- `Spider-Man: No Way Home` (2021)
- `Spider-Man` (2002)
- `Spider-Man: Homecoming` (2017)
- `Spider-Man 2` (2004)
- `Spider-Man: Into the Spider-Verse` (2018)
- `The Amazing Spider-Man` (2012)
- `Spider-Man 3` (2007)
- `Spider-Man: Far From Home` (2019)
- `The Amazing Spider-Man 2` (2014)
- `Spider-Man: Across the Spider-Verse` (2023)

### Example 3: Memory check
**Earlier user input**
`Hello my name is Arman`

**Later user input**
`what is my name and what we talked about in this chat?`

**Agent final answer**
`Your name is Arman, and in this chat, we discussed movies, particularly focusing on a list of Spider-Man films.`

## Notes
- This project is a terminal-based chatbot (`agent.py`).
- Tool implementations and tool schema are in `tools.py`.
- The local CSV is used for genre-based ranking only.
