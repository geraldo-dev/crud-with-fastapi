from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserResponse
from app.crud.user import get_user, get_users, create_user
from app.database import get_db


router = APIRouter()


@router.get('/', response_model=list[UserResponse])
def list_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_users(db=db, skip=skip, limit=limit)


@router.get('/:id', response_model=UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = get_user(user_id=user_id, db=db)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    return user


@router.post('/', response_model=UserResponse)
def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db=db, user=user)
