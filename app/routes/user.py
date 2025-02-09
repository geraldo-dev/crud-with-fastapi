from fastapi import APIRouter, Depends, HTTPException
from http import HTTPStatus
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserResponse, UserUpdatePartial
from app.crud.user import get_user, get_users, create_user, delete_user, update_user_partial, check_email
from app.database import get_db
from app.models.user import User

router: APIRouter = APIRouter()


@router.get('/', status_code=HTTPStatus.OK, response_model=list[UserResponse])
def list_users(skip: int = 0, limit: int = 10, db: Session = Depends(dependency=get_db)) -> list[User]:
    return get_users(db=db, skip=skip, limit=limit)


@router.get('/{user_id}', status_code=HTTPStatus.OK,  response_model=UserResponse)
def read_user(user_id: int, db: Session = Depends(dependency=get_db)) -> User:
    user: User | None = get_user(user_id=user_id, db=db)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    return user


@router.post('/', status_code=HTTPStatus.CREATED,  response_model=UserResponse, summary='criar usuario')
def create_new_user(user: UserCreate, db: Session = Depends(dependency=get_db)) -> User:
    existing_user: User | bool = check_email(db, user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail='O email já está em uso')

    return create_user(db=db, user=user)


@router.delete('/{user_id}', status_code=HTTPStatus.OK)
def destroy(user_id: int, db: Session = Depends(dependency=get_db)) -> dict[str, str]:
    success: bool = delete_user(db=db, user_id=user_id)
    if not success:
        raise HTTPException(status_code=404, detail='User not foud')
    return {'message': 'User deleted'}


@router.put('/{user_id}', status_code=HTTPStatus.OK,  response_model=UserResponse)
def update_user_field(user_id: int, updated_data: UserUpdatePartial, db: Session = Depends(dependency=get_db)):

    user: User | bool = get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')

    existing_user: User | bool = check_email(db, email=str(updated_data.email))

    if existing_user:
        raise HTTPException(
            status_code=400, detail="O email já está em uso.")

    update_user: User | None = update_user_partial(
        db, user_id, update_date=updated_data.dict(exclude_unset=True))

    if not update_user:
        raise HTTPException(status_code=400, detail='Update failed')
    return update_user
