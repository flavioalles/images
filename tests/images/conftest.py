import pytest

from src.images.services.image import ImageService


@pytest.fixture(scope="function")
def image_service():
    service = ImageService()
    yield service
    service.session.rollback()
