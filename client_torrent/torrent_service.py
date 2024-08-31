from client_torrent.abstract_client import AbstractClient


class TorrentService:
    def __init__(self, client: AbstractClient):
        self.client = client

    def add_torrent(self, url):
        self.client.add_torrent(url)

    def list_torrents(self) -> str:
        torrents = self.client.get_torrents()
        if not torrents:
            return "<b> You have nothing downloading at this moment ☹️ </b>"
        return "\n".join([
            f"<b>{torrent.id}.</b> {torrent.name} 🎬\n"
            f"<i>Status:</i> {torrent.status}\n"
            f"<i>Progress:</i> <b>{torrent.percent_done * 100:.2f}%</b>"
            for torrent in torrents
        ])
