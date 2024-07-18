import os.path
import uuid
from dataclasses import dataclass
from typing import Any

from PIL import Image as PILImage
from sqlalchemy.exc import (
    DataError,
    IntegrityError,
    InvalidRequestError,
    OperationalError,
)

from src.images.models.image import Image, ImageStatus
from src.images.services.base import BaseService
from src.images.services.exceptions import ClientError, ConflictError, ServerError
from src.images.utils.image import resize


@dataclass
class TmpImage:
    """
    A temporary image entity.

    Temporary as in (1) the image is not yet persisted to the database (and, hence, has not
    been processed) and (2) is persisted in temporary storage.

    Attributes:
        filename (str): The name of the temporary image file.
        headers (dict[Any, Any]): The headers associated with the image. TODO: Add correct type hints.
        content_type (str): The content type of the image.
    """

    path: str
    headers: dict[Any, Any]  # TODO: Add correct type hints.
    content_type: str


@dataclass
class ImageService(BaseService):
    """A service for managing images."""

    # TODO: make each come from a config file - while maintaining default values.
    base_path: str = "data/images"
    image_width: int = 1500

    def create(self, uploaded_image: TmpImage) -> Image:
        """
        Create a new image.

        Parameters:
            uploaded_image (TmpImage): The uploaded image object.

        Returns:
            Image: The newly created image.

        Raises:
            ClientError: If there is a data error or an invalid password is provided.
            ConflictError: If there is a conflict error.
            ServerError: If there is an invalid request or operational error.
        """
        try:
            # NOTE: Explicitly setting id - instead of relying on the default value -
            # to ensure that the id is set before the image is processed (since it is
            # used as the prefix for the file name (see self._process)).
            image = Image(id=uuid.uuid4())
            # TODO: process asynchronously.
            image = self._process(image, uploaded_image)
            self.session.add(image)
            self.session.flush()
            self.session.commit()
        except DataError as exc:
            self.session.rollback()
            raise ClientError(message=str(exc))
        except IntegrityError as exc:
            self.session.rollback()
            raise ConflictError(message=str(exc))
        except (InvalidRequestError, OperationalError) as exc:
            self.session.rollback()
            raise ServerError(message=str(exc))

        return image

    def update(self):
        """Update an existing image."""
        raise NotImplementedError()

    def get(self):
        """Get an image by ID."""
        raise NotImplementedError()

    def list(self):
        """List all images."""
        raise NotImplementedError()

    def delete(self):
        """Delete an image."""
        raise NotImplementedError()

    def _process(self, image: Image, uploaded_image: TmpImage) -> Image:
        """
        Process an image - i.e. resize and set Image.path.

        Args:
            image (Image): The original image object.
            uploaded_image (TmpImage): The temporary image object.

        Returns:
            Image: The processed image object.
        """
        # TODO: Create self.base_path if non-existent?
        output_image_path = (
            f"{self.base_path}/{image.id}.{os.path.basename(uploaded_image.path)}"
        )
        with PILImage.open(uploaded_image.path) as input_image:
            output_image = resize(
                input_image,
                self.image_width,
            )
            output_image.save(output_image_path)

        image.path = output_image_path

        return image
