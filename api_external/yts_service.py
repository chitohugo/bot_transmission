from typing import List, Dict, Optional

from api_external.api_client import ApiClient


class YtsApi:
    def __init__(self, api_client: ApiClient, url: str = "https://yts.mx/api/v2/list_movies.json"):
        self.api_client = api_client
        self.url = url

    def search_custom(self, title: str) -> List[Dict[str, Optional[str]]]:
        """
        Searches for movies based on the title and returns a list of dictionaries with movie details.

        :param title: Title of the movie to search for
        :return: List of dictionaries with movie details including title, year, and torrents.
        """
        kwargs = {
            "query_term": title,
            "sort_by": "title",
            "quality": "720p"
        }

        try:
            movies = self.api_client.get(self.url, params=kwargs)
        except Exception as e:
            return [{"message": f"Request failed: {str(e)}"}]

        movie_count = movies["data"].get("movie_count", 0)

        if movie_count == 0:
            return []

        response = []
        for movie in movies["data"].get("movies", []):
            data = {
                "title": movie.get("title"),
                "year": movie.get("year"),
                "torrents": [torrent.get("url") for torrent in movie.get("torrents", [])]
            }
            response.append(data)

        return response
