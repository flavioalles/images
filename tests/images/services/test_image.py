import os

import pytest
from PIL import Image as PILImage

from src.images.models.image import Image, ImageStatus
from src.images.services.image import ImageService
from src.images.utils.image import sha256_checksum


class TestCreateImageService:
    """
    Test class for the create image service.
    """

    def test_successful_image_service_create_with_large_image(
        self, image_service, large_image
    ):
        """
        Test method for the create image service for an image that is wider than
        ImageService.image_width.
        """
        assert image_service.session.query(Image).count() == 0

        image = image_service.create(large_image)

        assert image_service.session.query(Image).count() == 1
        assert (
            image.path
            == f"{image_service.base_path}/{image.id}.{os.path.basename(large_image.path)}"
        )
        assert image.checksum == sha256_checksum(image.path)
        assert image.status == ImageStatus.DONE
        assert image.created is not None
        assert image.updated is not None
        assert os.path.exists(image.path)

        with PILImage.open(image.path) as img:
            assert img.size[0] == image_service.image_width

    def test_successful_image_service_create_with_small_image(
        self, image_service, small_image
    ):
        """
        Test method for the create image service for an image that is narrower than
        ImageService.image_width.
        """
        assert image_service.session.query(Image).count() == 0

        image = image_service.create(small_image)

        assert image_service.session.query(Image).count() == 1
        assert (
            image.path
            == f"{image_service.base_path}/{image.id}.{os.path.basename(small_image.path)}"
        )
        assert image.checksum == sha256_checksum(image.path)
        assert image.status == ImageStatus.DONE
        assert image.created is not None
        assert image.updated is not None
        assert os.path.exists(image.path)

        with PILImage.open(image.path) as img:
            assert img.size[0] == image_service.image_width


class TestUpdateImageService:
    """
    Test class for the update image service.
    """

    def test_update_image_service(self, image_service):
        """
        Test method for the update image service.
        """
        with pytest.raises(NotImplementedError):
            image_service.update()


class TestGetImageService:
    """
    Test class for the get image service.
    """

    def test_get_image_service(self, image_service):
        """
        Test method for the get image service.
        """
        with pytest.raises(NotImplementedError):
            image_service.get()


class TestListImageService:
    """
    Test class for the list image service.
    """

    def test_list_image_service(self, image_service, large_image, small_image):
        """
        Test method for the list image service.
        """
        large_image = image_service.create(large_image)
        small_image = image_service.create(small_image)

        the_list = image_service.list()

        assert the_list.count() == 2

        first = the_list.first()
        last = the_list.all()[-1]

        assert first.id == large_image.id
        assert first.path == large_image.path
        assert first.checksum == large_image.checksum
        assert first.status == large_image.status

        assert last.id == small_image.id
        assert last.path == small_image.path
        assert last.checksum == small_image.checksum
        assert last.status == small_image.status


class TestDeleteImageService:
    """
    Test class for the delete image service.
    """

    def test_delete_image_service(self, image_service):
        """
        Test method for the delete image service.
        """
        with pytest.raises(NotImplementedError):
            image_service.delete()
