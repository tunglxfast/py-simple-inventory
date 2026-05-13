from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.area import Area


def list_areas(db: Session, include_inactive: bool = False) -> list[Area]:
    stmt = select(Area).order_by(Area.name)
    if not include_inactive:
        stmt = stmt.where(Area.is_active.is_(True))
    return list(db.scalars(stmt))


def get_area(db: Session, area_id: int) -> Area | None:
    return db.get(Area, area_id)


def get_by_name(db: Session, name: str) -> Area | None:
    return db.scalar(select(Area).where(Area.name == name))


def create_area(db: Session, name: str, description: str | None = None) -> Area:
    area = Area(name=name.strip(), description=description or None)
    db.add(area)
    db.flush()
    return area


def update_area(
    db: Session,
    area: Area,
    name: str,
    description: str | None,
    is_active: bool,
) -> Area:
    area.name = name.strip()
    area.description = description or None
    area.is_active = is_active
    db.flush()
    return area

