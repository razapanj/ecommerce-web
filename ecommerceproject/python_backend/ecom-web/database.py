import os 
from dotenv import find_dotenv,load_dotenv
from sqlmodel import create_engine,Session,SQLModel

find_dotenv(load_dotenv)

DATABSE_URL = os.environ["DATABASE_URL"]
engine = create_engine(DATABSE_URL)




def get_session():
    with Session(engine) as session:
        yield session 
