from abc import ABC, abstractmethod
from typing import Dict


class ApiClient(ABC):
    @abstractmethod
    def get(self, url: str, params: Dict[str, str]) -> dict:
        pass
