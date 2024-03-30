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

    
class LoginSignUp(Users,table = True):
    first_name:str = Field(nullable=False)
    last_name:str = Field(nullable=False) 
    email:str = Field(index=True,nullable=False,unique=True)
    created_at:datetime = Field(default_factory=datetime.now())
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
        if (self.role == "admin"):
            print("you are admin")
            return True
        else:
            print("you are user")
            return False

        
class LoginUsers(Users,table = True):
    login_id:Optional[int] = Field(primary_key=True,default=None) 
    login_at:datetime = Field(default_factory=datetime.now())
    logged_in:bool = Field(default=False)

    def check_user_is_login(self) -> bool:
        return self.logged_in 




    

