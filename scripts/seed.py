from app.core.database import SessionLocal, initialize_database
from app.services import area_service, auth_service, product_service
from app.services.exceptions import BusinessError


def main() -> None:
    initialize_database()
    db = SessionLocal()
    try:
        auth_service.ensure_default_admin(db)
        for name in ["Kho chính", "Khu vực A", "Khu vực B"]:
            try:
                area_service.create_area(db, name)
            except BusinessError:
                pass
        samples = [
            ("SP001", "Áo sơ mi nam Oxford", "Cái"),
            ("SP002", "Váy hoa nữ xuân", "Cái"),
            ("SP003", "Quần jean slim fit", "Cái"),
        ]
        for code, name, unit in samples:
            try:
                product_service.create_product(db, code, name, unit)
            except BusinessError:
                pass
    finally:
        db.close()


if __name__ == "__main__":
    main()

