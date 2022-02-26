from abc import ABC, abstractmethod

from .model import Batch


class AbstractRepository(ABC):
    @abstractmethod
    def add(self, batch: Batch):
        raise NotImplementedError

    @abstractmethod
    def get(self, reference) -> Batch:
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    pass
