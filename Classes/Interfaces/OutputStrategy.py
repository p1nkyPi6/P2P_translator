from abc import ABC, abstractmethod
from typing import Any

class OutputStrategy(ABC):
    @abstractmethod
    def printFrame(self) -> Any:
        pass