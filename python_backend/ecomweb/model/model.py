from sqlmodel import Field,SQLModel
from pydantic import BaseModel
from typing import Optional
from datetime import datetime,timedelta
from enum import Enum

class UserRole(str,Enum):
    admin:str = "admin"
    user:str = "user"

class UserBase(SQLModel):
    username:str = Field(nullable=False,index=True,unique=True) 
    password:str = Field(nullable=False)
    role: UserRole
    
class UserCreate(UserBase):
    firstname:str
    lastname:str
    email:str
    confirm_password:str

class User(UserBase, table = True):
    user_id:int | None = Field(primary_key=True, default=None)
    firstname:str = Field(nullable=False)
    lastname:str = Field(nullable=False) 
    email:str = Field(index=True,nullable=False,unique=True)
    created_at:datetime = Field(default_factory=datetime.now)
    confirm_password:str = Field(nullable=False)
    logged_in:bool = Field(default=False)
    def get_user_fullname(self) -> str:
        return f"The user fullname is ${self.firstname} ${self.lastname}"
    
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
    

class UserRead(SQLModel):
    user_id:int
    username:str
    email:str
    created_at:datetime
    
class UserUpdate(SQLModel):
    email:str | None = None 
    username:str | None = None
    password:str | None = None
    firstname:str | None = None
    lastname:str | None = None 
    
class Size(str,Enum):
    LARGE:str = "large"
    SMALL:str = "small"
    MEDIUM:str = "medium"

class ProductBase(SQLModel):
    product_name:str
    product_description:str
    product_price:int
    product_slug:str
    
    
class Product(ProductBase,table=True):
    product_id:int | None = Field(primary_key=True,default=None)
    

class ProductCreate(ProductBase):
    pass



class ProductRead(ProductBase):
    pass

class CartBase(SQLModel):
    total_cart_products:int
    product_total:int
    product_size:Size

class Cart(CartBase,table = True):
    cart_id:int | None = Field(primary_key=True,default=None)
    user_id:int | None = Field(foreign_key="user.user_id",default=None)
    product_id:int | None = Field(foreign_key="product.product_id",default=None) 

class CartCreate(CartBase):
    pass    

class CartUpdate(CartBase):
    pass

class CartRead(CartBase):
    cart_id:int
    user_id:int
    product_id:int


class CategoryBase(SQLModel):
    category_name:str
    category_description:str

class Category(CategoryBase,table=True):
    category_id:int | None = Field(primary_key=True,default=None)

class CategoryCreate(CategoryBase):
    pass

class CategoryRead(CategoryBase):
    pass




class CategoryProductAssociation(SQLModel,table = True):
    category_id:int | None = Field(primary_key=True,foreign_key="category.category_id",default=None)
    product_id:int | None = Field(primary_key=True,foreign_key="product.product_id",default=None) 

class OrderStatus(str,Enum):
    PENDING:str = "pending"
    CANCELLED:str = "cancelled"
    DELIVERED:str = "delivered"

class OrderBase(SQLModel):
    order_status:OrderStatus
    customer_name:str
    customer_email:str


class Order(OrderBase,table = True):
    order_id:int | None = Field(primary_key=True,default=None)
    user_id:int | None = Field(foreign_key="user.user_id",default=None)

class OrderCreate(OrderBase):
    pass

class OrderUpdate(SQLModel):
    order_status:OrderStatus

class OrderRead(OrderBase):
    pass
    

class Rating(int,Enum):
    ONE_STAR:int = 1
    TWO_STAR:int = 2
    THREE_STAR:int = 3
    FOUR_STAR:int = 4
    FIVE_STAR:int = 5

class ReviewBase(SQLModel):
    review_comment:str
    review_rating:Rating

class Review(ReviewBase,table=True):
    review_id:int | None = Field(primary_key=True,default=None)
    review_date:datetime = Field(default_factory=datetime.now)
    product_id:int | None = Field(foreign_key="product.product_id",default=None)
    user_id:int | None = Field(foreign_key="user.user_id",default=None)


class AddressBase(SQLModel):
    address_name :str


class Address(AddressBase,table = True):
    address_id:int | None = Field(primary_key=True,default=None)
    user_id:int | None = Field(foreign_key="user.user_id",default=None)
    order_id:int | None = Field(foreign_key="order.order_id",default=None)

class AddressCreate(AddressBase):
    pass

class OrderItemBase(SQLModel):
    total_cart_products:int
    product_total:int
    product_size:Size

class OrderItem(OrderItemBase,table =True):
    orderitem_id:int | None = Field(primary_key=True,default=None)
    order_id:int | None = Field(foreign_key="order.order_id",default=None)
    user_id:int | None = Field(foreign_key="user.user_id",default=None)
    product_id:int | None = Field(foreign_key="product.product_id",default=None)

class OrderItemCreate(OrderBase):
    pass

class PaymentMethod(str,Enum):
    COD:str = "cash on delivery"

class PaymentBase(SQLModel):
    payment_method:PaymentMethod

class Payment(PaymentBase,table = True):
    payment_id:int | None = Field(primary_key=True,default=None)
    user_id:int | None = Field(foreign_key="user.user_id",default=None)
    order_id:int | None = Field(foreign_key="order.order_id",default=None)

class PaymentCreate(PaymentBase):
    pass

class Token(SQLModel):
    access_token:str
    token_type:str
    refresh_token:str
    expires_in:int | timedelta

class TokenData(SQLModel):
    username:str | None = None
    user_id:int | None = None

