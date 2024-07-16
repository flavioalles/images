"""
This module sets up the database connection for the application using SQLAlchemy.

It creates an engine that connects to a database, and a sessionmaker that's bound to this engine.

The engine is configured with the connection string to the database.

The Session class is a sessionmaker that's bound to this engine. This class is used to create new Session objects which represent database transactions.

Example:
    To create a new Session object:
        session = Session()

    To close a Session object:
        session.close()

Attributes:
    engine (sqlalchemy.engine.Engine): The SQLAlchemy engine.
    Session (sqlalchemy.orm.session.sessionmaker): The SQLAlchemy sessionmaker.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.images.settings.base import Settings

settings = Settings()

engine = create_engine(settings.database_url)

Session = sessionmaker(bind=engine)
