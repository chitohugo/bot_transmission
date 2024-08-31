from abc import ABC, abstractmethod

class AbstractClient(ABC):
    @abstractmethod
    def add_torrent(self, url: str):
        pass

    @abstractmethod
    def get_torrents(self):
        pass
