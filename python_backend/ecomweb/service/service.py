from sqlmodel import select,Session
from ecomweb.model.model import *
from fastapi import HTTPException,Depends
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from ecomweb.settings.setting import ACCESS_TOKEN_EXPIRE_MINUTES,ALGORITHM,SECRET_KEY
from jose import jwt,JWTError
from passlib.context import CryptContext
from typing import Annotated
from datetime import datetime, timedelta,timezone
# Services for user
pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")
SECRET_KEYY = str(SECRET_KEY)
ALGORITHMM = str(ALGORITHM)

oauth_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def service_signup(session:Session,user:User):
    """
    This function is used to create a new user.

    :param session: An instance of the session object used to interact with the database.
    :type session: Session
    :param user: The user object to create.
    :type user: User

    :return: The created user object.
    :rtype: User
    """
    existing_user = session.exec(select(User).where(User.email == user.email)).first()
    if existing_user:
        return None
     
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def get_user_by_email(session:Session,email:str) -> User:
    """
    This function is used to get a user by email.

    :param session: An instance of the session object used to interact with the database.
    :type session: Session
    :param email: The email address of the user to retrieve.
    :type email: str

    :return: The user object corresponding to the provided email address, or None if not found.
    :rtype: User or None
    """
    if not email:
        return None
    user = session.exec(select(User).where(User.email == email)).one()
    if user is None:
        raise HTTPException(status_code=404,detail="user not found!")
    return user

def get_user_by_id(session:Session,user_id:int) -> User:
    """
    This function is used to get a user by id.

    :param session: An instance of the session object used to interact with the database.
    :type session: Session
    :param user_id: The id of the user to retrieve.
    :type user_id: int

    :return: The user object corresponding to the provided id, or None if not found.
    :rtype: User or None
    """
    if not user_id:
        return None
    
    user = session.exec(select(User).where(User.user_id == user_id)).one()
    if user is None:
        raise HTTPException(status_code=404,detail="user not found!")
    return user
def get_user_by_username(session:Session,username:str) -> User:
    """
    This function is used to get a user by username.

    :param session: An instance of the session object used to interact with the database.
    :type session: Session
    :param username: The username of the user to retrieve.
    :type username: str

    :return: The user object corresponding to the provided username, or None if not found.
    :rtype: User or None
    """
    if not username:
        return None
    
    user = session.exec(select(User).where(User.username == username)).one()
    if user is None:
        raise HTTPException(status_code=404, detail="user not found!")
    return user 


def verify_password(password, hashed_password) -> bool:
    """
    This function is used to verify a password against a hashed password.

    :param plain_password: The plain text password to verify.
    :type plain_password: str
    :param hashed_password: The hashed password to compare against.
    :type hashed_password: str

    :return: True if the password matches, False otherwise.
    :rtype: bool
    """
    return pwd_context.verify(password, hashed_password)

def get_hash_password(password) -> str:
    """
    This function is used to get the hash password of a plain text password.

    :param plain_password: The plain text password to hash.
    :type plain_password: str

    :return: The hashed password.
    :rtype: str
    """
    return pwd_context.hash(password)

def authenticate_user(session:Session, username:str, password:str) -> User:
    """
    This function is used to authenticate a user.

    :param session: An instance of the session object used to interact with the database.
    :type session: Session
    :param username: The username of the user to authenticate.
    :type username: str
    :param password: The password of the user to authenticate.
    :type password: str

    :return: The authenticated user object, or None if authentication fails.
    :rtype: User or None
    """
    user = get_user_by_username(session, username)
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user

def get_current_user(token:Annotated[str,Depends(oauth_scheme)],session:Session) -> User:
    """
    This function is used to get the current user from a token.

    :param token: The token to get the user from.
    :type token: str

    :return: The current user object, or None if the token is invalid.
    :rtype: User or None
    """
    credentials_exception = HTTPException(status_code=401, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})                 
    try:
        payload = jwt.decode(token,SECRET_KEYY,algorithms=[ALGORITHMM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)

    except JWTError:
        raise credentials_exception
    user = get_user_by_username(session,token_data.username)
    if user is None:
        raise credentials_exception
    return user

def create_access_token(data:dict, expires_delta:int | timedelta | None = None) -> str:
    """
    This function is used to create an access token.

    :param data: The data to encode in the token.
    :type data: dict
    :param expires_delta: The expiration time of the token.
    :type expires_delta: int | timedelta | None

    :return: The access token.
    :rtype: str
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEYY, algorithm=ALGORITHMM)
    return encoded_jwt

def create_refresh_token(data:dict, expires_delta:int | timedelta | None = None) -> str:
    """
    This function is used to create a refresh token.

    :param data: The data to encode in the token.
    :type data: dict
    :param expires_delta: The expiration time of the token.
    :type expires_delta: int | timedelta | None

    :return: The refresh token.
    :rtype: str
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(days=7)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEYY, algorithm=ALGORITHMM)
    return encoded_jwt

def validate_refresh_token(session:Session,refresh_token:str) -> TokenData:
    """
    This function is used to validate a refresh token.

    :param token: The refresh token to validate.
    :type token: str

    :return: The TokenData object if the token is valid, None otherwise.
    :rtype: TokenData or None
    """
    credentials_exception = HTTPException(status_code=401, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})                 
    try:
        payload = jwt.decode(refresh_token, SECRET_KEYY, algorithms=[ALGORITHMM])
        id = payload.get("id")
        username = payload.get("sub")
        if username is None:
            return None
        token_data = TokenData(user_id=id)
    except JWTError:
        raise credentials_exception
    user = get_user_by_id(token_data.user_id)
    if user is None:
        raise credentials_exception
    return user

def get_product_by_id(session:Session,product_id:int) -> Product:
    """
    
    """
    product = session.exec(select(Product).where(Product.product_id == product_id)).one()
    if product is None:
        raise HTTPException(status_code=404, detail="product not found!")
    return product

def get_all_products(session:Session) -> list[Product]:
    """

    """
    products = session.exec(select(Product)).all()
    return products

def product_add(session:Session, product:Product):
    """

    """
    existing_product = session.exec(select(Product).where(Product.product_name == product.product_name)).first()
    if existing_product:
        return None
    session.add(product)
    session.commit()
    session.refresh(product)
    return product

def get_image(session:Session, product_id:int) -> list[Image]:
    """

    """
    images = session.exec(select(Image).where(Image.product_id == product_id)).all()
    
    return images

def service_create_category(session:Session,category:Category) -> Category:
    """
    
    """
    existing_category = session.exec(select(Category).where(Category.category_name == category.category_name)).first()
    if existing_category:
        return None
    session.add(category)
    session.commit()
    session.refresh(category)
    return category