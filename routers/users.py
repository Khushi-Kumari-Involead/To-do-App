from typing import Annotated, Optional
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from fastapi import APIRouter, Depends, HTTPException, status
from models import Users
from database import SessionLocal
from .auth import get_current_user
from passlib.context import CryptContext

router = APIRouter(
    prefix='/user',
    tags=['user']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

class UserVerification(BaseModel):
    password: str
    new_pass: str = Field(min_length=6)

class UpdateUserRequest(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None


@router.get("/", status_code=status.HTTP_200_OK)
async def get_user_info(user: user_dependency, db: db_dependency):
    """
     This function is doing -- This functions enables the user to check their own information
     Args: user, db

     Returns: user information (if the authentication is successful,
                    raises HTTP exception if not authenticated)
      
    """
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    return db.query(Users).filter(Users.id == user.get('id')).first()

@router.put("/password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user: user_dependency,
                           db: db_dependency,
                           user_verification: UserVerification):
    """
     This function is doing -- This function enables the user to change their password 
     Args: user, db, password, user-verification

     Returns: "Password successfully changed"(if authentication is successful
                                                if not, raises exception)
      
    """
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication failed")
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()
    
    if not bcrypt_context.verify(user_verification.password, user_model.hashed_password):
        raise HTTPException(status_code=401, detail="Your password is incorrect")
    user_model.hashed_password = bcrypt_context.hash(user_verification.new_pass)
    db.add(user_model)
    db.commit()
    return {'message': "password successfully changed"}

@router.put("/edit_user", status_code=status.HTTP_200_OK)
async def update_user(
    user: user_dependency,
    db: db_dependency,
    update_user_request: UpdateUserRequest
):
    """
     This function is doing -- This function enables the user to edit their information 
     Args: user, db, update_user-request(basemodel)

     Returns: "profile updated successfully"(If authentication is successful, if not, raises
                                            exception)
    """
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not authenticated"
        )

    user_model = db.query(Users).filter(Users.id == user.get("id")).first()

    if not user_model:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if update_user_request.username is not None:
        user_model.username = update_user_request.username
    if update_user_request.email is not None:
        user_model.email = update_user_request.email
    if update_user_request.first_name is not None:
        user_model.first_name = update_user_request.first_name
    if update_user_request.last_name is not None:
        user_model.last_name = update_user_request.last_name
    db.add(user_model)
    db.commit()
    db.refresh(user_model)
    return {"message": "Profile updated successfully"}

@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user: user_dependency,
                       db: db_dependency):
    """
     This function is doing -- This function enables the user to delete their profile 
     Args: user, db

     Returns: "User deleted successfully"(if authentication successfull, otherwise raises HTTP Exception)
      
    """

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    db.query(Users).filter(Users.id == user.get('id')).delete()
    db.commit()
    return {'message': "User deleted successfully"}