import logging
import os
import shutil
import tempfile

from fastapi import APIRouter, HTTPException, status, UploadFile, File
from pydantic import BaseModel

from src.images.endpoints.base import Base
from src.images.models.image import ImageStatus
from src.images.services.exceptions import ClientError, ConflictError, ServerError
from src.images.services.image import ImageService, TmpImage


logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api",
    tags=["images"],
)


class Image(Base):
    """
    Represents an image.

    Attributes:
        status (ImageStatus): The status of the image.
        checksum (str): The checksum of the image.
    """

    status: ImageStatus
    checksum: str


@router.post("/submit", status_code=status.HTTP_201_CREATED)
async def create_image(image_file: UploadFile = File(...)) -> Image:
    """
    Create a new image from an uploaded file.

    Args:
        image_file (UploadFile): The uploaded image file.

    Returns:
        Image: The created image.

    Raises:
        HTTPException: If there is a conflict, bad request, or internal server error.
    """
    # TODO: assert content type.
    try:
        logger.info(f"Creating image from uploaded file: {image_file.filename}")
        prefix, suffix = os.path.splitext(os.path.basename(image_file.filename))
        with (
            tempfile.NamedTemporaryFile(
                prefix=f"{prefix}.", suffix=suffix, delete=False, mode="wb"
            ) as tmp,
        ):
            shutil.copyfileobj(image_file.file, tmp)
            tmp_image = TmpImage(
                path=tmp.name,
                headers=image_file.headers,
                content_type=image_file.content_type,
            )

        image = ImageService().create(tmp_image)
    except ConflictError as exc:
        logger.error(f"Failed to create image: {exc.message}")
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=exc.message)
    except ClientError as exc:
        logger.error(f"Failed to create image: {exc.message}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=exc.message)
    except ServerError as exc:
        logger.error(f"Failed to create image: {exc.message}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=exc.message
        )

    logger.info(f"Image created: {image.id}")

    return Image(
        id=image.id,
        status=image.status,
        checksum=image.checksum,
        created=image.created,
        updated=image.updated,
    )
