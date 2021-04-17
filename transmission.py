from dataclasses import dataclass
from transmission_rpc import Client
from cfg import TRANSMISSION


@dataclass()
class TransmissionBroker:
    conn = Client(**TRANSMISSION)

    @classmethod
    def add_torrents(cls, data: tuple) -> list:
        response = []
        for url in data:
            response.append(cls.conn.add_torrent(url))
        return response

    @classmethod
    def list_torrents(cls):
        return "\n".join([f'{torrent.id}, {torrent.name}, '
                          f'{torrent.status}, '
                          f'{torrent.percentDone * 100}'
                          for torrent in cls.conn.get_torrents()])

    def status_torrents(self):
        pass
