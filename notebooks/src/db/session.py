from pathlib import Path
from typing import Union

from dotenv import dotenv_values
from sqlalchemy import create_engine, engine, URL
from sqlalchemy.orm import sessionmaker, Session


def get_engine(dotenv_path: Union[Path, str]) -> engine.Engine:
    """
    データベース接続のためのEngineを作成する。

    Parameters
    ----------
    dotenv_path : Union[Path, str]
        .envファイルのパス
    
    Returns
    -------
    sqlalchemy.engine.Engine
        データベース接続のためのEngine
    """
    config = dotenv_values(dotenv_path)

    url_object = URL.create(
        'postgresql+psycopg',
        username=config['POSTGRES_USER'],
        password=config['POSTGRES_PASSWORD'],  # plain (unescaped) text
        host=config.get('POSTGRES_HOST', 'postgres'),
        port=config.get('POSTGRES_PORT', '5432'),
        database=config.get('POSTGRES_DB', 'postgres'),
        query={'options': f'-c search_path={config.get("POSTGRES_SCHEMA", "public")}'},
    )

    return create_engine(url_object)


def get_sessionmaker(dotenv_path: Union[Path, str]) -> sessionmaker:
    """
    データベース接続のためのsessionmakerを作成する。

    Parameters
    ----------
    dotenv_path : Union[Path, str]
        .envファイルのパス
    
    Returns
    -------
    SessionLocal : sqlalchemy.orm.sessionmaker
        データベース接続のためのSession
    """
    engine = get_engine(dotenv_path)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal


def get_session(dotenv_path: Union[Path, str]) -> Session:
    """
    データベース接続のためのSessionを作成する。

    Parameters
    ----------
    dotenv_path : Union[Path, str]
        .envファイルのパス
    
    Returns
    -------
    session : sqlalchemy.orm.Session
        データベース接続のためのSession
    """
    sessionmaker = get_sessionmaker(dotenv_path)
    session = sessionmaker()
    return session
