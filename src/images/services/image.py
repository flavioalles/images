from dataclasses import dataclass

from src.images.services.base import BaseService


@dataclass
class ImageService(BaseService):
    """A service for managing images."""

    def create(self):
        """Create a new image."""
        raise NotImplementedError()

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
