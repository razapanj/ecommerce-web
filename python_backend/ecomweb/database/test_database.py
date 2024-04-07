import os
from dotenv import find_dotenv,load_dotenv
from sqlmodel import create_engine,Session,SQLModel
from ecomweb.settings.setting import TEST_DATABASE_URL
load_dotenv(find_dotenv())

test_conn_str = str(TEST_DATABASE_URL)
engine = create_engine(test_conn_str,echo=True)


def get_test_session():
    with Session(engine) as session:
        yield session 


def test_create_all_tables():
    SQLModel.metadata.create_all(engine)
    return "Tables created"


def test_drop_all_tables():
    SQLModel.metadata.drop_all(engine)
    return "Tables dropped"

