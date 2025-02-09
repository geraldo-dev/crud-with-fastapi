from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate


def check_email(db: Session, email: str):
    # Validate if the email sent is already in use by another user
    db_user: User | None = db.query(User).filter(User.email == email).first()
    if not db_user:
        return False
    return db_user


def get_user(db: Session, user_id: int) -> User | bool:
    user: User | None = db.query(User).filter(User.id == user_id).first()
    if not user:
        return False
    return user


def get_users(db: Session, skip: int = 0, limit: int = 10) -> list[User]:
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, user: UserCreate) -> User:
    hashed_password: str = user.password + \
        'dgakdsgdadpda'  # subtitua por um hashing real
    db_user: User = User(name=user.name, email=user.email,
                         hashed_password=hashed_password)
    db.add(instance=db_user)
    db.commit()
    db.refresh(instance=db_user)
    return db_user


def delete_user(db: Session, user_id: int) -> bool:
    db_user: User | None = db.query(User).filter(User.id == user_id).first()
    if db_user:
        db.delete(instance=db_user)
        db.commit()
        return True
    return False


def update_user_partial(db: Session, user_id: int, update_date: dict[str, str]) -> User | bool:
    db_user: User | None = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        return False

    # update only received fields
    for key, value in update_date.items():
        if hasattr(db_user, key):
            setattr(db_user, key, value)

    db.commit()
    db.refresh(instance=db_user)
    return db_user
