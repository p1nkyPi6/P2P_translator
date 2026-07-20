from abc import ABC, abstractmethod
from typing import Any

class _IInputStrategy(ABC):
    @abstractmethod
    def returnFrame(self) -> Any:
        pass