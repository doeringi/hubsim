from abc import ABC, abstractmethod


class AbstractReflector(ABC):
    @abstractmethod
    def reflect():
        raise NotImplementedError('Abstract method "reflect" must be implemented')
