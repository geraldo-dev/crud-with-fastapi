from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserResponse, UserUpdatePartial
from app.crud.user import get_user, get_users, create_user, delete_user, update_user_partial
from app.database import get_db

router = APIRouter()


@router.get('/', response_model=list[UserResponse])
def list_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_users(db=db, skip=skip, limit=limit)


@router.get('/{user_id}', response_model=UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = get_user(user_id=user_id, db=db)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    return user


@router.post('/', response_model=UserResponse)
def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db=db, user=user)


@router.delete('/{user_id}')
def destroy(user_id: int, db: Session = Depends(get_db)):
    success = delete_user(db=db, user_id=user_id)
    if not success:
        raise HTTPException(status_code=404, detail='User not foud')
    return {'message': 'User deleted'}


@router.put('/{user_id}', response_model=UserResponse)
def update_user_field(user_id: int, update_date: UserUpdatePartial, db: Session = Depends(get_db)):

    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')

    update_user = update_user_partial(
        db, user_id, update_date.dict(exclude_unset=True))
    if not update_user:
        raise HTTPException(status_code=400, detail='Update failed')
    return update_user
