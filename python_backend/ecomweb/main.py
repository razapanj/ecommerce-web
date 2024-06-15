from fastapi import FastAPI,Depends,UploadFile,File,Request,Response
from fastapi.middleware.cors import CORSMiddleware
from ecomweb.database.database import create_all_tables,get_session 
from ecomweb.model.model import *
from ecomweb.service.service import *
from contextlib import asynccontextmanager
from sqlmodel import Session
from typing import Annotated
from fastapi import HTTPException
from datetime import timedelta
from ecomweb.settings.setting import *
from ecomweb.middlewares.middleware import authorize
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Creating tables..")
    create_all_tables()
    yield
    
app = FastAPI(lifespan=lifespan,title="ecommerce api with sqlmodel",version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/signup",response_model=UserRead)
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

@app.post("/api/login",response_model=Token)
def login_user(request:Response,session:Annotated[Session,Depends(get_session)],form_data:OAuth2PasswordRequestForm = Depends()):
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
    request.set_cookie(key="access_token",value=access_token)
    request.set_cookie(key="refresh_token",value=refresh_token)
    return Token(access_token=access_token,refresh_token=refresh_token,expires_in=access_token_expire_time,token_type="bearer")

@app.get("/logout/{user_id}")
def logout_user(response:Response,request:Request,session:Annotated[Session,Depends(get_session)],user:Annotated[User,Depends(get_current_user)],):
    user_loggedout = service_logout_user(session,user.user_id,response,request)
    return user_loggedout

@app.patch("/updateuser")
def update_user(session:Annotated[Session,Depends(get_session)],user_update:UserUpdate,user:Annotated[User,Depends(get_current_user)]):
    user = get_user_by_id(session,user.user_id)
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


@app.post("/addproduct",response_model=ProductRead)
def add_product(session:Annotated[Session, Depends(get_session)], product_data:ProductCreate,user:Annotated[User,Depends(isadmin)]):
    product_info = Product.model_validate(product_data)
    product = product_add(session, product_info,user)
    return product

@app.get("/getproduct",response_model=ProductRead)
def get_product_from_id(session:Annotated[Session, Depends(get_session)], product_id:int,user:Annotated[User,Depends(get_current_user)]):
    product = get_product_by_id(session,product_id)
    return product  

@app.get("/getproducts",response_model=list[ProductRead])
def get_products(session:Annotated[Session, Depends(get_session)],user:Annotated[User,Depends(get_current_user)]):
    product = get_all_products(session)
    return product

@app.post("/createcategory",response_model=CategoryRead)
def create_category(session:Annotated[Session,Depends(get_session)],category_data:CategoryCreate,user:Annotated[User,Depends(isadmin)]):
    category_info = Category.model_validate(category_data)
    category = service_create_category(session, category_info)
    return category


@app.post("/productcategoryassociation",response_model=CategoryProductAssociation)
def create_productsubcategoryassociation(session:Annotated[Session,Depends(get_session)],category_product_association_data:CategoryProductAssociation,user:Annotated[User,Depends(isadmin)]) -> CategoryProductAssociation:
    category_product_association_info = CategoryProductAssociation.model_validate(category_product_association_data)
    category_product_association = service_create_productsubcategoryassociation(session, category_product_association_info) 
    return category_product_association

@app.get("/getproductbycategory/{category_id}",response_model=list[ProductRead])
def get_product_from_category(session:Annotated[Session,Depends(get_session)],category_id):
    return service_get_product_from_category(session,category_id)

@app.post("/createorder")
def create_order(order_data:OrderCreate,address_data:AddressCreate,payment_data:PaymentCreate,user:Annotated[User , Depends(get_current_user)],session:Annotated[Session, Depends(get_session)]) -> OrderRead:
    
    order_info = Order.model_validate(order_data)
    order = service_create_order(session, order_info,user)
    service_create_address(session,address_data,order.order_id,user)
    service_create_payment(session,user,order.order_id,payment_data)
    return order

@app.patch("/updateorder")
def update_order(order_update:OrderUpdate,order_id, user:Annotated[User, Depends(get_current_user)], session:Annotated[Session, Depends(get_session)]):
    order = service_get_order_by_id(session,order_id)
    if order:
        order_data = order_update.model_dump(exclude_unset = True)
        order.sqlmodel_update(order_data)
        session.add(order)
        session.commit()
        session.refresh(order)
        if order.order_status == "cancelled" or order.order_status == "delivered":
            return service_order_update(session,user,order_id)
        return order 

@app.delete("/deleteorder")
def delete_order(order_id, user:Annotated[User, Depends(get_current_user)], session:Annotated[Session, Depends(get_session)]):
    deleted_order = service_delete_order(session,order_id)
    return deleted_order

@app.get("/getorder/{order_id}")
def get_order_by_id(order_id:int,session:Annotated[Session,Depends(get_session)],user:Annotated[User,Depends(get_current_user)]):
    order = service_get_order_by_id(session,order_id)
    return order

@app.post("/addtocart",response_model=CartRead)
def add_to_cart(product_id:int,cart_info:CartCreate,session:Annotated[Session,Depends(get_session)],user:Annotated[User, Depends(get_current_user)]):
    cart_data = Cart.model_validate(cart_info)
    cart = service_add_to_cart(session,cart_data,user,product_id)
    return cart

@app.get("/getproductfromcart",response_model=list[ProductRead])
def get_product_from_cart(session:Annotated[Session,Depends(get_session)],user:Annotated[User, Depends(get_current_user)]):
    return service_get_product_from_cart(session,user)

@app.delete("/deletepayment")
def delete_payment(session:Annotated[Session,Depends(get_session)],order_id:int):
    return service_delete_payment(session,order_id)

@app.delete("/deleteorderitem")
def delete_order_item(session:Annotated[Session,Depends(get_session)],order_id:int):
    return service_delete_order_item(session,order_id)