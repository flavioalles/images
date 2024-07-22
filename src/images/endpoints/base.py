from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, validator


class Base(BaseModel):
    """
    Represents the base output data for any model that descendes from Base.

    Attributes:
        id (UUID): The unique identifier of the object.
        created (datetime): The datetime when the object was created.
        updated (datetime): The datetime when the object was last updated.
    """

    id: UUID
    created: datetime
    updated: datetime
