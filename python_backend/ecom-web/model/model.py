from sqlmodel import Field,SQLModel
from typing import Optional
from datetime import datetime
from enum import Enum

class UserRole(str,Enum):
    admin:str = "admin"
    user:str = "user"

class User(SQLModel):
    user_name:str = Field(nullable=False,index=True,unique=True) 
    password:str = Field(nullable=False)
    role: UserRole
     
    

    
class SignUpUser(User,table = True):
    signup_user_id:Optional[int] = Field(primary_key=True,default=None)
    first_name:str = Field(nullable=False)
    last_name:str = Field(nullable=False) 
    email:str = Field(index=True,nullable=False,unique=True)
    created_at:datetime = Field(default_factory=datetime.now)
    confirm_password:str = Field(nullable=False)

    def get_user_fullname(self) -> str:
        return f"The user fullname is ${self.first_name} ${self.last_name}"
    
    def get_user_email(self) -> str:
        return self.email
    
    def check_password_matches(self) -> bool:
        if(self.password == self.confirm_password):
            return True
        else:
            return False
        
    def check_user_role(self) -> bool:
        if (self.role == UserRole.admin):
            print("you are admin")
            return True
        else:
            print("you are user")
            return False

        
class LoginUser(User,table = True):
    login_user_id:int | None = Field(primary_key=True,default=None)
    login_at:datetime = Field(default_factory=datetime.now)
    logged_in:bool = Field(default=False)

    def check_user_is_login(self) -> bool:
        return self.logged_in 
    
class Size(str,Enum):
    LARGE:str = "large"
    SMALL:str = "small"
    MEDIUM:str = "medium"
    EXTRALARGE:str = "extralarge"
    EXTRAEXTRALARGE:str = "extraextralarge"

class Product(SQLModel,table=True):
    product_id:int | None = Field(primary_key=True,default=None)
    product_name:str = Field(index=True,unique=True)
    product_description:str
    product_price:int = Field(index=True)
    product_slug:str = Field(index=True)
    product_quantity:int
    product_size:Size
    

class ProductCart(SQLModel,table = True):
    cart_product_id:int | None = Field(primary_key=True,default=None)
    user_id:int | None = Field(foreign_key="loginuser.login_user_id",default=None)
    product_id:int | None = Field(foreign_key="product.product_id",default=None) 

class Image(SQLModel,table=True):
    image_id:int | None = Field(primary_key=True,default=None)
    file_name:str
    data:bytes 
    product_id:int | None = Field(foreign_key="product.product_id",index=True,default=None)


class Category(SQLModel,table=True):
    category_id:int | None = Field(primary_key=True,default=None)
    category_name:str = Field(index=True)
    category_description:str
    product_id:int | None = Field(foreign_key="product.product_id",default=None)
    

class CategoryProductAssociation(SQLModel,table = True):
    category_id:int | None = Field(primary_key=True,foreign_key="category.category_id",default=None)
    product_id:int | None = Field(primary_key=True,foreign_key="product.product_id",default=None) 

class OrderStatus(str,Enum):
    PENDING:str = "pending"
    SUCCESS:str = "success"
    DELIVERED:str = "delivered"

class Order(SQLModel,table = True):
    order_id:int | None = Field(primary_key=True,default=None)
    order_date:datetime = Field(default_factory=datetime.now)
    order_status:OrderStatus
    user_id:int | None = Field(foreign_key="loginuser.login_user_id")

class OrderItem(SQLModel,table = True):
    order_item_id:int | None = Field(primary_key=True,default=None)
    order_quantity:int
    order_price:int
    order_subtotal:int
    product_id:int | None = Field(foreign_key="product.product_id",default=None)
    order_id:int | None = Field(foreign_key="order.order_id",default=None)


class Rating(int,Enum):
    ONE_STAR:int = 1
    TWO_STAR:int = 2
    THREE_STAR:int = 3
    FOUR_STAR:int = 4
    FIVE_STAR:int = 5


class Review(SQLModel,table=True):
    review_id:int | None = Field(primary_key=True,default=None)
    review_comment:str
    review_date:datetime = Field(default_factory=datetime.now)
    product_id:int | None = Field(foreign_key="product.product_id",default=None)
    user_id:int | None = Field(foreign_key="loginuser.login_user_id",default=None)
    review_rating:Rating


class Address(SQLModel):
    address_id:int | None = Field(primary_key=True,default=None)
    address_name :str = Field(index=True)
    user_id:int | None = Field(foreign_key="loginuser.login_user_id",default=None)
    order_id:int | None = Field(foreign_key="order.order_id",default=None)

class PaymentMethod(str,Enum):
    COD:str = "cash on delivery"

class Payment(SQLModel,table = True):
    payment_id:int | None = Field(primary_key=True,default=None)
    payment_method:PaymentMethod
    order_id:int | None = Field(foreign_key="order.order_id",default=None)
    user_id:int | None = Field(foreign_key="loginuser.login_user_id",default=None)

class OrderHistory(SQLModel,table = True):
    order_history_id:int | None =  Field(primary_key=True,default=None)
    order_id:int | None = Field(foreign_key="order.order_id",default=None)
    user_id:int | None = Field(foreign_key="loginuser.login_user_id",default=None)
    order_date:datetime = Field(default_factory=datetime.now)
    order_status:OrderStatus 
