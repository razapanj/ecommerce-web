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
    EXTRALARGE:str = "extralarge"
    EXTRAEXTRALARGE:str = "extraextralarge"

class ProductBase(SQLModel):
    product_name:str
    product_description:str
    product_price:int
    product_slug:str
    product_quantity:int
    product_size:Size

class Product(ProductBase,table=True):
    product_id:int | None = Field(primary_key=True,default=None)
    

class ProductCreate(ProductBase):
    pass



class ProductRead(ProductBase):
    pass

    

class ProductCart(SQLModel,table = True):
    cart_product_id:int | None = Field(primary_key=True,default=None)
    user_id:int | None = Field(foreign_key="user.user_id",default=None)
    product_id:int | None = Field(foreign_key="product.product_id",default=None) 

class Image(SQLModel,table=True):
    image_id:int | None = Field(primary_key=True,default=None)
    file_name:str
    data:bytes 
    product_id:int | None = Field(foreign_key="product.product_id",index=True,default=None)

class ImageRead(SQLModel):
    file_name:str
    data:bytes
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

class SubCategoriesBase(SQLModel):
    sub_category_name:str

class SubCategories(SubCategoriesBase,table=True):
    sub_categories_id:int | None = Field(primary_key=True,default=None)
    category_id:int | None = Field(foreign_key="category.category_id",default=None)

class SubCategoryCreate(SubCategoriesBase):
    category_id:int

class SubCategoryRead(SubCategoriesBase):
    pass


class CategoryProductAssociation(SQLModel,table = True):
    sub_categories_id:int | None = Field(primary_key=True,foreign_key="subcategories.sub_categories_id",default=None)
    product_id:int | None = Field(primary_key=True,foreign_key="product.product_id",default=None) 

class OrderStatus(str,Enum):
    PENDING:str = "pending"
    SUCCESS:str = "success"
    DELIVERED:str = "delivered"

class OrderBase(SQLModel):
    order_status:OrderStatus



class Order(OrderBase,table = True):
    order_id:int | None = Field(primary_key=True,default=None)
    order_date:datetime = Field(default_factory=datetime.now)
    user_id:int | None = Field(foreign_key="user.user_id")

class OrderCreate(OrderBase):
    user_id:int
class OrderUpdate(OrderBase):
    pass

class OrderRead(OrderBase):
    order_date:datetime
    user_id:int

class OrderItemBase(SQLModel):
    order_quantity:int
    order_price:int
    order_subtotal:int
    

class OrderItem(OrderItemBase,table = True):
    order_item_id:int | None = Field(primary_key=True,default=None)
    product_id:int | None = Field(foreign_key="product.product_id",default=None)
    order_id:int | None = Field(foreign_key="order.order_id",default=None)

class OrderItemCreate(OrderItemBase):
    product_id:int
    order_id:int

class OrderItemRead(OrderItemBase):
    product_id:int
    order_id:int


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



class Address(SQLModel):
    address_id:int | None = Field(primary_key=True,default=None)
    address_name :str = Field(index=True)
    user_id:int | None = Field(foreign_key="user.user_id",default=None)
    order_id:int | None = Field(foreign_key="order.order_id",default=None)

class PaymentMethod(str,Enum):
    COD:str = "cash on delivery"

class Payment(SQLModel,table = True):
    payment_id:int | None = Field(primary_key=True,default=None)
    payment_method:PaymentMethod
    order_id:int | None = Field(foreign_key="order.order_id",default=None)
    user_id:int | None = Field(foreign_key="user.user_id",default=None)


class Token(SQLModel):
    access_token:str
    token_type:str
    refresh_token:str
    expires_in:int | timedelta

class TokenData(SQLModel):
    username:str | None = None
    user_id:int | None = None

