import os 
from dotenv import find_dotenv,load_dotenv
from ecomweb.model.model import *
from sqlmodel import create_engine,Session,SQLModel
from ecomweb.settings.setting import DATABASE_URL

conn_str = str(DATABASE_URL)
engine = create_engine(conn_str,echo=True,pool_recycle=300, connect_args={"sslmode": "require"})


def get_session():
    with Session(engine) as session:
        yield session 

def create_all_tables():
    SQLModel.metadata.create_all(engine)
    


def drop_all_tables():
    SQLModel.metadata.drop_all(engine)
    return "Tables dropped"




