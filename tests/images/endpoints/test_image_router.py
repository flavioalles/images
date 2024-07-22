import json
import pytest

from src.images.models.image import Image


class TestCreateImageEndpoint:
    """
    Test class for the create image endpoint.
    """

    resource: str = "/api/submit"

    def test_when_create_image_is_successful(self, test_app, image_service):
        """
        Test case for creating an image successfully.

        Args:
            test_app: The test client for the application.
            image_service: The image service.

        Returns:
            None
        """
        assert image_service.session.query(Image).count() == 0

        with open("tests/images/fixtures/large.image.jpg", "rb") as image_file:
            response = test_app.post(
                self.resource,
                files={"image_file": ("image.jpg", image_file, "image/jpeg")},
            )

        assert image_service.session.query(Image).count() == 1

        an_image = image_service.session.query(Image).one()

        assert response.status_code == 201
        assert response.json()["id"] == str(an_image.id)
        assert response.json()["created"] == an_image.created.strftime(
            "%Y-%m-%dT%H:%M:%S.%fZ"
        )
        assert response.json()["updated"] == an_image.updated.strftime(
            "%Y-%m-%dT%H:%M:%S.%fZ"
        )
        assert response.json()["checksum"] == str(an_image.checksum)
        assert response.json()["status"] == str(an_image.status.value)
