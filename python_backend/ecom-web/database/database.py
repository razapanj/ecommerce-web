import os 
from dotenv import find_dotenv,load_dotenv
from sqlmodel import create_engine,Session,SQLModel

load_dotenv(find_dotenv())

DATABSE_URL = os.environ["DATABASE_URL"]
engine = create_engine(DATABSE_URL,echo=True)


def get_session():
    with Session(engine) as session:
        yield session 


def create_all_tables():
    SQLModel.metadata.create_all(engine)
    return "Tables created"


def drop_all_tables():
    SQLModel.metadata.drop_all(engine)
    return "Tables dropped"