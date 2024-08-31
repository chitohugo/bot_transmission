import os

from dotenv import load_dotenv
from transmission_rpc import Client

from client_torrent.abstract_client import AbstractClient

load_dotenv()


class TransmissionClient(AbstractClient):
    def __init__(self):
        self.user = os.getenv("TRANSMISSION_RPC_USERNAME")
        self.password = os.getenv("TRANSMISSION_RPC_PASSWORD")

        self.conn = Client(
            username=self.user,
            password=self.password,
            host='transmission',
        )

    def add_torrent(self, url: str):
        return self.conn.add_torrent(url)

    def get_torrents(self):
        return self.conn.get_torrents()
