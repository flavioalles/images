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


class TestListImagesEndpoint:
    """
    Test class for the list images endpoint.
    """

    resource: str = "/api/list"

    def test_when_list_images_is_successful(self, test_app, image_service):
        """
        Test case for listing images successfully.

        Args:
            test_app: The test client for the application.
            image_service: The image service.

        Returns:
            None
        """
        assert image_service.session.query(Image).count() == 0

        for path in [
            "tests/images/fixtures/large.image.jpg",
            "tests/images/fixtures/small.image.jpg",
        ]:
            with open(path, "rb") as image_file:
                test_app.post(
                    "/api/submit",
                    files={"image_file": ("image.jpg", image_file, "image/jpeg")},
                )

        response = test_app.get(self.resource)

        expected_list = image_service.list()
        expected_large_image = expected_list.query.first()
        expected_small_image = expected_list.query.all()[-1]

        assert response.status_code == 200
        assert len(response.json()) == expected_list.query.count() == 2

        large_image = response.json()[0]
        small_image = response.json()[1]

        assert large_image["id"] == str(expected_large_image.id)
        assert large_image["created"] == expected_large_image.created.strftime(
            "%Y-%m-%dT%H:%M:%S.%fZ"
        )
        assert large_image["updated"] == expected_large_image.updated.strftime(
            "%Y-%m-%dT%H:%M:%S.%fZ"
        )
        assert large_image["checksum"] == expected_large_image.checksum
        assert large_image["status"] == expected_large_image.status.value

        assert small_image["id"] == str(expected_small_image.id)
        assert small_image["created"] == expected_small_image.created.strftime(
            "%Y-%m-%dT%H:%M:%S.%fZ"
        )
        assert small_image["updated"] == expected_small_image.updated.strftime(
            "%Y-%m-%dT%H:%M:%S.%fZ"
        )
        assert small_image["checksum"] == expected_small_image.checksum
        assert small_image["status"] == expected_small_image.status.value
