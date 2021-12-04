from fastapi.testclient import TestClient
from app.database import get_db
import pytest
from app.main import app

from app.database import Base

from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


#####TEST DATABASE #######
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


#####TEST DATABASE  END  #######


# client = TestClient(app)


@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    # denne lager databasetabellene
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(session):
    # run our code, before we return our test. Se tutorial, 15:39:30
    def override_get_db():

        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    # run our code after test finishes
    # Base.metadata.drop_all(bind=engine)
