import re
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, user: UserCreate):
    hashed_password = user.password + 'dgakdsgdadpda'  # subtitua por um hashing real
    db_user = User(name=user.name, email=user.email,
                   hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
        return True
    return False


def update_user_partial(db: Session, user_id: int, update_date: dict):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        return None

    # atualiza apenas campos recebidos
    for key, value in update_date.items():
        if hasattr(db_user, key):
            setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)
    return db_user
