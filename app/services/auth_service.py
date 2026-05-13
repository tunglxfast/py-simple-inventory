from sqlalchemy.orm import Session

from app.core.security import hash_password, verify_password
from app.repositories import user_repository
from app.services.exceptions import BusinessError


def ensure_default_admin(db: Session) -> None:
    if user_repository.get_by_username(db, "admin"):
        return
    user_repository.create_user(db, "admin", hash_password("admin"))
    db.commit()


def authenticate(db: Session, username: str, password: str) -> bool:
    user = user_repository.get_by_username(db, username.strip())
    if not user or not user.is_active:
        return False
    return verify_password(password, user.password_hash)


def require_valid_login(username: str, password: str) -> None:
    if not username.strip() or not password:
        raise BusinessError("Vui lòng nhập tài khoản và mật khẩu.")
