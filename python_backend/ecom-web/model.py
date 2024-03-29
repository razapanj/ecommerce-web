from sqlmodel import Field,SQLModel
from typing import Optional
from datetime import datetime
from enum import Enum

class UserRole(str,Enum):
    admin = "admin"
    user = "user"

class Users(SQLModel):
    user_id:Optional[int] = Field(primary_key=True,default=None)
    user_name:str = Field(nullable=False,index=True,unique=True) 
    password:str = Field(nullable=False)
    role: UserRole
     
    def get_user_id(self):
        return self.user_id

    
class UserSignup(Users):
    first_name:str = Field(nullable=False)
    last_name:str = Field(nullable=False) 
    email:str = Field(index=True,nullable=False,unique=True)
    created_at:datetime = Field(default_factory=datetime.now())
    confirm_password = Field(nullable=False)

    def get_user_fullname(self):
        return f"The user fullname is ${self.first_name} ${self.last_name}"
    
    def get_user_email(self):
        return self.email
    
    def check_password_matches(self):
        if(self.password == self.confirm_password):
            return True
        else:
            return False
        
class UserLogin(Users):
    login_time:datetime = Field(default_factory=datetime.now()) 


    

