from abc import ABC, abstractmethod
from dataclasses import dataclass

from src.images.models.database import Session


@dataclass
class BaseService(ABC):
    """
    Abstract base class for service classes.
    """

    session: Session = Session()

    @abstractmethod
    def create(self):
        """
        Abstract method for creating an entity.
        """
        pass

    @abstractmethod
    def update(self):
        """
        Abstract method for updating an entity.
        """
        pass

    @abstractmethod
    def get(self):
        """
        Abstract method for retrieving an entity.
        """
        pass

    @abstractmethod
    def list(self):
        """
        Abstract method for listing entities.
        """
        pass

    @abstractmethod
    def delete(self):
        """
        Abstract method for deleting an entity.
        """
        pass
