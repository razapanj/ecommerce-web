from sqlmodel import select,Session
from ecomweb.model.model import *
from fastapi import HTTPException
# Services for user

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

def get_user_by_role(session:Session, role:str) -> User:
    """
    This function is used to get a user by role.

    :param session: An instance of the session object used to interact with the database.
    :type session: Session
    :param role: The role of the user to retrieve.
    :type role: str

    :return: The user object corresponding to the provided role, or None if not found.
    :rtype: User or None
    """
    if not role:
        return None

    user = session.exec(select(User).where(User.role == role)).one()
    if user is None:
        raise HTTPException(status_code=404, detail="user not found!")
    return user

