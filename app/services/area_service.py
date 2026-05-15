from sqlalchemy.orm import Session

from app.repositories import area_repository
from app.services.exceptions import BusinessError


def list_areas(db: Session, include_inactive: bool = False):
    return area_repository.list_areas(db, include_inactive=include_inactive)


def create_area(db: Session, name: str, description: str | None = None):
    if not name.strip():
        raise BusinessError("Tên khu vực không được để trống.")
    existing = area_repository.get_by_name(db, name.strip())
    if existing:
        raise_duplicate_area_name(existing.is_active)
    area = area_repository.create_area(db, name, description)
    db.commit()
    return area


def update_area(db: Session, area_id: int, name: str, description: str | None, is_active: bool):
    if not name.strip():
        raise BusinessError("Tên khu vực không được để trống.")
    area = area_repository.get_area(db, area_id)
    if not area:
        raise BusinessError("Không tìm thấy khu vực.")
    existing = area_repository.get_by_name(db, name.strip())
    if existing and existing.id != area_id:
        raise_duplicate_area_name(existing.is_active)
    area_repository.update_area(db, area, name, description, is_active)
    db.commit()
    return area


def raise_duplicate_area_name(is_active: bool) -> None:
    if is_active:
        raise BusinessError("Tên khu vực đã tồn tại.")
    raise BusinessError("Tên khu vực đã bị ngưng hoạt động. Bật xem inactive để cập nhật lại khu vực.")
