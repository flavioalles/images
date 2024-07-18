import glob
import os
import shutil
import tempfile

import pytest
from sqlalchemy import create_engine

from src.images.models.base import DeclarativeBase
from src.images.models.database import Session
from src.images.services.image import ImageService, TmpImage
from src.images.settings.base import Settings


engine = create_engine(Settings().database_url)


@pytest.fixture(scope="session")
def database_engine():
    """
    Returns the SQLAlchemy engine object.

    :return: SQLAlchemy engine object.
    """
    return engine


@pytest.fixture(scope="session", autouse=True)
def database_setup(database_engine):
    """Create all tables before the test session and drop them after."""
    DeclarativeBase.metadata.create_all(bind=database_engine)
    yield
    DeclarativeBase.metadata.drop_all(bind=database_engine)


@pytest.fixture(scope="function", autouse=True)
def database_setup_and_teardown(database_engine):
    """Clean the database before and after each test."""
    session = Session()
    yield
    # Drop all data after each test
    for table in reversed(DeclarativeBase.metadata.sorted_tables):
        session.execute(table.delete())
    session.commit()


@pytest.fixture(scope="function")
def image_service():
    service = ImageService(base_path=tempfile.gettempdir())
    yield service
    service.session.rollback()


@pytest.fixture(scope="function")
def large_image(image_service):
    with (
        open("tests/images/fixtures/large.image.jpg", "rb") as original,
        tempfile.NamedTemporaryFile(
            prefix="large.image.", suffix=".jpg", delete=False, mode="wb"
        ) as tmp,
    ):
        shutil.copyfileobj(original, tmp)
        tmp_image = TmpImage(
            path=tmp.name,
            headers={"Content-Length": 100, "Content-Type": "image/jpeg"},
            content_type="image/jpeg",
        )

    yield tmp_image

    for path in glob.glob(
        os.path.join(image_service.base_path, f"*{os.path.basename(tmp.name)}")
    ):
        try:
            os.remove(path)
        except FileNotFoundError as e:
            pass
