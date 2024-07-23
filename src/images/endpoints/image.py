import logging
import os
import shutil
import tempfile

from fastapi import APIRouter, HTTPException, status, UploadFile, File, Query, Response
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

    path: str
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
        path=image.path,
        status=image.status,
        checksum=image.checksum,
        created=image.created,
        updated=image.updated,
    )


@router.get("/list", status_code=status.HTTP_200_OK)
async def list_images(
    response: Response,
    page: int = Query(1, gt=0, alias="page", description="The page number"),
    limit: int = Query(
        10,
        gt=0,
        lt=100,
        alias="limit",
        description="The maximum number of images per page",
    ),
) -> list[Image]:
    """
    Retrieve a list of images - always ordered by creation time (ASC).

    Args:
        response (Response): The FastAPI response object.
        page (int): The page number.
        limit (int): The maximum number of images per page.

    Returns:
        list[Image]: A list of Image objects representing images within the parameters
            of the request.

    Raises:
        HTTPException: If there is a bad request or internal server error.
    """
    try:
        logger.info(
            f"Listing images as per page ({page}) and limit ({limit}) parameters"
        )
        result = ImageService().list(offset=(page - 1) * limit, limit=limit)
    except ClientError as exc:
        logger.error(f"Failed to list images: {exc.message}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=exc.message)
    except ServerError as exc:
        logger.error(f"Failed to list images: {exc.message}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=exc.message
        )

    # NOTE: To simplify client logic, no error is raised (i.e. 404) if no images are found.
    logger.info(
        f"Images listed for request (page={page} & limit={limit}): {result.query.count()}"
    )

    response.headers["X-Page"] = str(page)
    response.headers["X-Page-Size"] = str(limit)
    response.headers["X-Total-Count"] = str(result.total)
    response.headers["X-Total-Pages"] = str((result.total - 1) // limit + 1)

    return [
        Image(
            id=image.id,
            path=image.path,
            status=image.status,
            checksum=image.checksum,
            created=image.created,
            updated=image.updated,
        )
        for image in result.query
    ]
