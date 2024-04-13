from fastapi import FastAPI,Depends,UploadFile,File
from ecomweb.database.database import create_all_tables,get_session 
from ecomweb.model.model import *
from ecomweb.service.service import *
from contextlib import asynccontextmanager
from sqlmodel import Session
from typing import Annotated
from fastapi import HTTPException
from datetime import timedelta
from ecomweb.settings.setting import *
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Creating tables..")
    create_all_tables()
    yield

    
app = FastAPI(lifespan=lifespan,title="ecommerce api with sqlmodel",version="0.1.0")

@app.post("/signup",response_model=UserRead)
def signup_users(session:Annotated[Session,Depends(get_session)],user_data:UserCreate) -> User:
    """
        This function is used to signup a new user.

        arguments:
            session: The database session.
            user_data: The user data to signup.

        returns:
            The newly created user object.
    """
    user_data.password = get_hash_password(user_data.password)
    user_data.confirm_password = get_hash_password(user_data.confirm_password)
    user = User.model_validate(user_data)
    return service_signup(session,user)

@app.post("/login",response_model=Token)
def login_user(session:Annotated[Session,Depends(get_session)],form_data:OAuth2PasswordRequestForm = Depends()):
    """
        This function is used to login a user.

        arguments:
            session: The database session.
            form_data: The login form data.

        returns:
            The access token and refresh token.
    """
    user = authenticate_user(session,form_data.username,form_data.password)
    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expire_time = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub":user.username},expires_delta=access_token_expire_time)

    refresh_token_expire_time = timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    refresh_token = create_refresh_token(data={"id":user.user_id}, expires_delta=refresh_token_expire_time)

    return Token(access_token=access_token,refresh_token=refresh_token,expires_in=access_token_expire_time,token_type="bearer")

@app.patch("/updateuser")
def update_user(session:Annotated[Session,Depends(get_session)],user_update:UserUpdate,user_id:int):
    user = get_user_by_id(session,user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    user_data = user_update.model_dump(exclude_unset = True)
    user.sqlmodel_update(user_data)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@app.delete("/deleteuser")
def delete_user(session:Annotated[Session, Depends(get_session)], user_id:int):
    user = get_user_by_id(session, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(user)
    session.commit()
    return {
        "message":"User deleted"
    }

@app.post("/uploadimage")
async def upload_image(session:Annotated[Session,Depends(get_session)],product_id:int,image:UploadFile = File(...)):
    image_data = await image.read()
    db_image = Image(file_name=image.filename,data= image_data,product_id=product_id)
    session.add(db_image)
    session.commit()
    session.refresh(db_image)
    return {"message":"Image uploaded"}

@app.get("/getimage", response_model=list[ImageRead])
def get_image_for_product(session:Annotated[Session, Depends(get_session)], product_id:int):
    image = get_image(session, product_id)
    return image


@app.post("/addproduct",response_model=ProductRead)
def add_product(session:Annotated[Session, Depends(get_session)], product_data:ProductCreate):
    product_info = Product.model_validate(product_data)
    product = product_add(session, product_info)
    return product

@app.get("/getproduct",response_model=ProductRead)
def get_product_from_id(session:Annotated[Session, Depends(get_session)], product_id:int):
    product = get_product_by_id(session,product_id)
    return product  

@app.get("/getproducts",response_model=list[ProductRead])
def get_products(session:Annotated[Session, Depends(get_session)]):
    product = get_all_products(session)
    return product


