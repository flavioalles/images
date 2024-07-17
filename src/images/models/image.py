from enum import Enum as PyEnum

from sqlalchemy import Column, Unicode, Enum
from sqlalchemy.orm import validates

from src.images.models.base import Base
from src.images.utils.image import sha256_checksum


class ImageStatus(PyEnum):
    """
    Enumeration class representing the status of an image.

    Possible values:
    - IN_PROGRESS: The image is currently being processed.
    - DONE: The image processing is complete.
    - CORRUPTED: The image is corrupted - i.e. checksum does not match image at path.
    """

    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"
    CORRUPTED = "CORRUPTED"


class Image(Base):
    """
    Represents an image entity.

    Attributes:
        __tablename__ (str): The name of the database table for images.
        path (str): The unique path to the image file.
        checksum (str): SHA-256 checksum of the image for integrity verification.
        status (ImageStatus): The processing status of the image.
    """

    __tablename__ = "images"

    path = Column(
        Unicode(255),
        unique=True,
        nullable=False,
        doc="The unique path to the image file.",
    )
    checksum = Column(
        Unicode(64),
        nullable=True,
        doc="SHA-256 checksum of the image for integrity verification.",
    )
    status = Column(
        Enum(ImageStatus),
        default=ImageStatus.IN_PROGRESS,
        nullable=False,
        doc="The processing status of the image.",
    )

    def __repr__(self):
        return f"<Image(id={self.id}, path={self.path}, checksum={self.checksum}, status={self.status})>"

    @validates("path")
    def _checksum(self, key, value):
        """
        Compute the checksum of the image.

        Parameters:
            key (str): The key of the attribute.
            value (str): The value of the attribute.

        Returns:
            str: The SHA-256 checksum of the image.
        """
        try:
            self.checksum = sha256_checksum(value)
        except Exception as exc:
            self.status = ImageStatus.CORRUPTED
        else:
            self.status = ImageStatus.DONE

        return value
