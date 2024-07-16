import pytest

from src.images.services.image import ImageService


class TestCreateImageService:
    """
    Test class for the create image service.
    """

    def test_create_image_service(self, image_service):
        """
        Test method for the create image service.
        """
        with pytest.raises(NotImplementedError):
            image_service.create()


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

    def test_list_image_service(self, image_service):
        """
        Test method for the list image service.
        """
        with pytest.raises(NotImplementedError):
            image_service.list()


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
