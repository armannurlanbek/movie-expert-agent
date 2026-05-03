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

### Example 1: Top 10 action movies
**User input**
`дай мне топ 10 экшн фильмов`

**Tool call**
- `get_top_movies_by_genre({'genre': 'Action', 'limit': 10})`

**Final answer (excerpt)**
- The agent returns a Russian-language top-10 list, including `The Dark Knight`, `The Lord of the Rings: The Return of the King`, `Inception`, and `The Matrix`.

### Example 2: Spider-Man list + top 2 comparison
**User input**
`дай мне лист фильмов про человека паука и потом сделай поиск по топ 2 из них и сравни`

**Tool calls**
- `search_movie_list({'search_query': 'Spider-Man'})`
- `search_movie({'title': 'Spider-Man: No Way Home', 'plot': 'short'})`
- `search_movie({'title': 'Spider-Man', 'plot': 'short'})`

**Final answer (excerpt)**
- Returns a Russian-language list of Spider-Man movies.
- Adds a side-by-side comparison of `Spider-Man: No Way Home` and `Spider-Man` (2002) with rating, runtime, genres, awards, and box office.

### Example 3: Memory check
**Earlier user input**
`Привет меня зовут Арман`

**Later user input**
`Как меня зовут и что я тебя спрашивал?`

**Agent final answer**
`Вас зовут Арман, и вы спрашивали о рекомендациях топ-10 экшн-фильмов. Позже вы запросили список фильмов про Человека-Паука и сравнение двух из них.`

## Notes
- This project is a terminal-based chatbot (`agent.py`).
- Tool implementations and tool schema are in `tools.py`.
- The local CSV is used for genre-based ranking only.

Git link: https://github.com/armannurlanbek/movie-expert-agent
