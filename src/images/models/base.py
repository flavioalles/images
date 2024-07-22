import uuid

from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, DateTime, UUID
from sqlalchemy.sql import func


DeclarativeBase = declarative_base()


class Base(DeclarativeBase):
    """
    Base class defining the min. attributes for all models.

    This class should be inherited by other models to provide common attributes and operations.

    Attributes:
        __abstract__ (bool): Indicates whether the class is abstract or not.
        id (UUID): The primary key of the model, represented as a UUID.
        created (DateTime): The timestamp when the model was created.
        updated (DateTime): The timestamp when the model was last updated.
    """

    __abstract__ = True

    # NOTE: For pagination reasons, id becoming an auto-incrementing integer is ideal -
    # since it would avoid reading (best case scenatio - i.e. contiguous ID's/no deletions)
    # OFFSET rows from the database.
    # TODO: Drop use of UUID for id (implement auto-incremeting integers).
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        index=True,
        nullable=False,
    )
    created = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    updated = Column(
        DateTime(timezone=True),
        default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
