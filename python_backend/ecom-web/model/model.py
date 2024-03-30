from sqlmodel import Field,SQLModel
from typing import Optional
from datetime import datetime
from enum import Enum

class UserRole(str,Enum):
    admin = "admin"
    user = "user"

class User(SQLModel):
    user_id:Optional[int] = Field(primary_key=True,default=None)
    user_name:str = Field(nullable=False,index=True,unique=True) 
    password:str = Field(nullable=False)
    role: UserRole
     
    def get_user_id(self):
        return self.user_id

    
class SignUpUser(User,table = True):
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

        
class LoginUsers(User,table = True):
    login_at:datetime = Field(default_factory=datetime.now)
    logged_in:bool = Field(default=False)

    def check_user_is_login(self) -> bool:
        return self.logged_in 
    
class Size(str,Enum):
    LARGE = "large"
    SMALL = "small"
    MEDIUM = "medium"
    EXTRALARGE = "extralarge"
    EXTRAEXTRALARGE = "extraextralarge"

class Product(SQLModel):
    product_id:Optional[int] = Field(primary_key=True,default=None)
    product_name:str = Field(index=True,unique=True)
    product_description:str
    product_price:int = Field(index=True)
    product_slug:str = Field(index=True)
    product_quantity:int
    product_size:Size
    

class Image(SQLModel):
    image_id:Optional[int] = Field(primary_key=True,default=None)
    file_name:str
    data:bytes 
    product_id:int = Field(foreign_key="product.product_id",index=True)


class ProductAll(Product,table = True):
    pass

class ProductCart(Product,table = True):
    pass

class Category(SQLModel,table=True):
    category_id:int | None = Field(primary_key=True,default=None)
    category_name:str = Field(index=True)
    category_description:str
    product_id:int | None = Field(foreign_key="product.product_id")
    

class CategoryProductAssociation(SQLModel,table = True):
    category_id:int | None = Field(foreign_key="category.category_id")
    product_id:int | None = Field(foreign_key="product.product_id") 

class OrderStatus(SQLModel):
    PENDING = "pending"
    SUCCESS = "success"
    DELIVERED = "delivered"

class Order(SQLModel):
    order_id:int | None = Field(primary_key=True,default=None)
    order_date:datetime = Field(default_factory=datetime.now)
    order_status:OrderStatus
    user_id:int | None = Field(foreign_key="user.user_id")

class OrderItem(SQLModel):
    order_item_id:int | None = Field(primary_key=True,default=None)
    order_quantity:int
    order_price:int
    order_subtotal:int
    product_id:int | None = Field(foreign_key="product.product_id")
    order_id:int | None = Field(foreign_key="order.order_id")


class Rating(int,Enum):
    ONE_STAR = 1
    TWO_STAR = 2
    THREE_STAR = 3
    FOUR_STAR = 4
    FIVE_STAR = 5


class Review(SQLModel,table=True):
    review_id:int | None = Field(primary_key=True,default=None)
    review_comment:str
    review_date:datetime = Field(default_factory=datetime.now)
    product_id:int | None = Field(foreign_key="product.product_id")
    user_id:int | None = Field(foreign_key="user.user_id")
    review_rating:Rating


class Address(SQLModel):
    address_id:int | None = Field(primary_key=True,default=None)
    address_name :str = Field(index=True)
    user_id:int | None = Field(foreign_key="user.user_id")
    order_id:int | None = Field(foreign_key="order.order_id")

class PaymentMethod(str,Enum):
    COD = "cash on delivery"

class Payment(SQLModel):
    payment_id:int | None = Field(primary_key=True,default=None)
    payment_method:PaymentMethod
    order_id:int | None = Field(foreign_key="order.order_id")
    user_id:int | None = Field(foreign_key="user.user_id")

class OrderHistory(SQLModel):
    order_id:int | None = Field(foreign_key="order.order_id")
    user_id:int | None = Field(foreign_key="user.user_id")
    order_date:datetime = Field(default_factory=datetime.now)
    order_status:OrderStatus 
