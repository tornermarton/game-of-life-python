from abc import ABC, abstractmethod


class View(ABC):
    @abstractmethod
    def update(self) -> None:
        pass

    @abstractmethod
    def draw(self) -> None:
        pass


class Clickable(ABC):
    @abstractmethod
    def click(self) -> None:
        pass
