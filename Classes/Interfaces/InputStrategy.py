from abc import ABC, abstractmethod
from typing import Any

class InputStrategy(ABC):
    @abstractmethod
    def returnFrame(self) -> Any:
        pass