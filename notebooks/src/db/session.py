from pathlib import Path
from typing import Union

from dotenv import dotenv_values
from sqlalchemy import URL, create_engine, engine
from sqlalchemy.orm import Session, sessionmaker


def get_engine(dotenv_path: Union[Path, str]) -> engine.Engine:
    """
    Create a database connection Engine.

    Parameters
    ----------
    dotenv_path : Union[Path, str]
        Path to the .env file

    Returns
    -------
    engine : sqlalchemy.engine.Engine
        Engine for database connection
    """
    config = dotenv_values(dotenv_path)

    url_object = URL.create(
        'postgresql+psycopg',
        username=config['JUPYTER_DB_USER'],
        password=config['JUPYTER_DB_PASSWORD'],  # plain (unescaped) text
        host=config.get('POSTGRES_HOST', 'postgres'),
        port=config.get('POSTGRES_PORT', '5432'),
        database=config.get('POSTGRES_DB', 'postgres'),
        query={'options': f'-c search_path={config.get("DATABASE_SCHEMA", "public")}'},
    )

    engine = create_engine(url_object)
    return engine


def get_sessionmaker(dotenv_path: Union[Path, str]) -> sessionmaker:
    """
    Create a sessionmaker for database connection.

    Parameters
    ----------
    dotenv_path : Union[Path, str]
        Path to the .env file

    Returns
    -------
    SessionLocal : sqlalchemy.orm.sessionmaker
        Sessionmaker for database connection
    """
    engine = get_engine(dotenv_path)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal


def get_session(dotenv_path: Union[Path, str]) -> Session:
    """
    Create a database connection Session.

    Parameters
    ----------
    dotenv_path : Union[Path, str]
        Path to the .env file

    Returns
    -------
    session : sqlalchemy.orm.Session
        Session for database connection
    """
    sessionmaker = get_sessionmaker(dotenv_path)
    session = sessionmaker()
    return session
