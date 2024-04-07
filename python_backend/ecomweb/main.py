from fastapi import FastAPI,Depends
from ecomweb.database.database import create_all_tables,get_session 
from ecomweb.model.model import *
from contextlib import asynccontextmanager
from sqlmodel import Session
from typing import Annotated
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Creating tables..")
    create_all_tables()
    yield

    
app = FastAPI(lifespan=lifespan,title="ecommerce api with sqlmodel",version="0.1.0")


