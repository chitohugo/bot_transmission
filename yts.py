from dataclasses import dataclass
import requests


@dataclass
class YtsApi:
    url: str = "https://yts.mx/api/v2/list_movies.json"

    @classmethod
    def search_custom(cls, title) -> list:
        """
        :param title:
        :return: list of movies.
        sort_by by default "title", quality by default "720p"
        """

        response = []
        kwargs = {
            "query_term": title,
            "sort_by": "title",
            "quality": "720p"
        }
        movies = requests.get(cls.url, params=kwargs).json()

        if not movies["data"]["movie_count"]:
            return [{"message": "Not encounter!"}]

        for movie in movies["data"]["movies"]:
            data = {"Title": movie["title"],
                    "Year": movie["year"]}
            for torrent in movie["torrents"]:
                url = torrent["url"]
                data.update({"Torrent": url})

            response.append(data)
        return response


# if __name__ == '__main__':
#     s = YtsApi()
#     movies = s.search_custom("titanic")
#     print(movies)
