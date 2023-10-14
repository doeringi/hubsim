from abc import ABC, abstractmethod


class AbstractObserver(ABC):
    @abstractmethod
    def observe(self) -> str:
        raise NotImplementedError('Abstract method "observe" must be implemented')
