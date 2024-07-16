from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Configuration settings for the images API.

    Attributes:
        app_name (str): The name of the application.
        description (str): A description of the API service.
        database_url (str): The URL of the database.
    """

    app_name: str = "images"
    description: str = "An API providing a service that handles image uploads."
    database_url: str = Field(
        ..., env="DATABASE_URL", description="Database connection URL."
    )
