from abc import abstractmethod, ABC


class Steppable(ABC):
    @abstractmethod
    def step(self) -> None:
        pass
