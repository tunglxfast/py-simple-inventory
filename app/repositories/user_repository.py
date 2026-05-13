from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User


def get_by_username(db: Session, username: str) -> User | None:
    return db.scalar(select(User).where(User.username == username))


def create_user(db: Session, username: str, password_hash: str) -> User:
    user = User(username=username.strip(), password_hash=password_hash)
    db.add(user)
    db.flush()
    return user

