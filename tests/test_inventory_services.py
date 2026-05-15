from datetime import date

import pytest

from app.models.stock import StockDocumentType
from app.repositories import stock_repository
from app.schemas.stock import StockLineData
from app.services import area_service, product_service, stock_service
from app.services.exceptions import BusinessError


def seed_product_and_area(db):
    product = product_service.create_product(db, "SP001", "Áo sơ mi", "Cái")
    area = area_service.create_area(db, "Kho chính")
    return product, area


def line(product_id: int, quantity: int, note: str | None = None) -> StockLineData:
    return StockLineData(product_id=product_id, quantity=quantity, note=note)


def test_product_delete_sets_inactive(db_session):
    product, _ = seed_product_and_area(db_session)

    product_service.delete_product(db_session, product.id)

    products = product_service.list_products(db_session)
    all_products = product_service.list_products(db_session, include_inactive=True)
    assert products == []
    assert all_products[0].is_active is False


def test_create_product_reports_inactive_duplicate(db_session):
    product, _ = seed_product_and_area(db_session)
    product_service.delete_product(db_session, product.id)

    with pytest.raises(BusinessError, match="ngưng hoạt động"):
        product_service.create_product(db_session, "SP001", "Áo khác", "Cái")


def test_create_area_reports_inactive_duplicate(db_session):
    _, area = seed_product_and_area(db_session)
    area_service.update_area(db_session, area.id, area.name, area.description, False)

    with pytest.raises(BusinessError, match="ngưng hoạt động"):
        area_service.create_area(db_session, area.name)


def test_stock_in_and_out_changes_inventory(db_session):
    product, area = seed_product_and_area(db_session)

    stock_service.create_stock_document(
        db_session,
        StockDocumentType.IN.value,
        [line(product.id, 10)],
        date.today(),
        area.id,
        "Nhập đầu",
        "Admin",
        "",
    )
    stock_service.create_stock_document(
        db_session,
        StockDocumentType.OUT.value,
        [line(product.id, 4)],
        date.today(),
        area.id,
        "Xuất",
        "Admin",
        "",
    )

    stock = stock_repository.get_stock_by_product_ids(db_session, [product.id])
    assert stock[product.id] == 6


def test_stock_out_blocks_negative_inventory(db_session):
    product, area = seed_product_and_area(db_session)

    with pytest.raises(BusinessError):
        stock_service.create_stock_document(
            db_session,
            StockDocumentType.OUT.value,
            [line(product.id, 1)],
            date.today(),
            area.id,
            "Xuất",
            "Admin",
            "",
        )


def test_stock_document_rejects_inactive_area(db_session):
    product, area = seed_product_and_area(db_session)
    area_service.update_area(db_session, area.id, area.name, area.description, False)

    with pytest.raises(BusinessError, match="Khu vực đã bị ngưng hoạt động"):
        stock_service.create_stock_document(
            db_session,
            StockDocumentType.IN.value,
            [line(product.id, 1)],
            date.today(),
            area.id,
            "Nhập",
            "Admin",
            "",
        )


def test_stock_document_rejects_missing_product(db_session):
    _, area = seed_product_and_area(db_session)

    with pytest.raises(BusinessError, match="Không tìm thấy sản phẩm ID 999"):
        stock_service.create_stock_document(
            db_session,
            StockDocumentType.IN.value,
            [line(999, 1)],
            date.today(),
            area.id,
            "Nhập",
            "Admin",
            "",
        )


def test_stock_document_rejects_inactive_product(db_session):
    product, area = seed_product_and_area(db_session)
    product_service.delete_product(db_session, product.id)

    with pytest.raises(BusinessError, match=rf"Sản phẩm Áo sơ mi \(ID {product.id}\).*ngưng hoạt động"):
        stock_service.create_stock_document(
            db_session,
            StockDocumentType.IN.value,
            [line(product.id, 1)],
            date.today(),
            area.id,
            "Nhập",
            "Admin",
            "",
        )


def test_reset_inventory_creates_adjust_in_and_out(db_session):
    product_a, area = seed_product_and_area(db_session)
    product_b = product_service.create_product(db_session, "SP002", "Quần jean", "Cái")
    stock_service.create_stock_document(
        db_session,
        StockDocumentType.IN.value,
        [
            line(product_a.id, 5),
            line(product_b.id, 10),
        ],
        date.today(),
        area.id,
        "Nhập",
        "Admin",
        "",
    )

    adjust_in_count, adjust_out_count = stock_service.reset_inventory(
        db_session,
        {product_a.id: 8, product_b.id: 3},
    )

    stock = stock_repository.get_stock_by_product_ids(db_session, [product_a.id, product_b.id])
    documents = stock_service.list_documents(db_session)
    assert adjust_in_count == 1
    assert adjust_out_count == 1
    assert stock[product_a.id] == 8
    assert stock[product_b.id] == 3
    assert {document.type for document in documents} >= {
        StockDocumentType.ADJUST_IN.value,
        StockDocumentType.ADJUST_OUT.value,
    }


def test_reset_inventory_rejects_negative_quantity(db_session):
    product, _ = seed_product_and_area(db_session)

    with pytest.raises(BusinessError):
        stock_service.reset_inventory(db_session, {product.id: -1})


def test_reset_inventory_reports_missing_product_id(db_session):
    seed_product_and_area(db_session)

    with pytest.raises(BusinessError, match="Không tìm thấy sản phẩm ID 999"):
        stock_service.reset_inventory(db_session, {999: 0})


def test_reset_inventory_reports_inactive_product_name_and_id(db_session):
    product, _ = seed_product_and_area(db_session)
    product_service.delete_product(db_session, product.id)

    with pytest.raises(BusinessError, match=rf"Sản phẩm Áo sơ mi \(ID {product.id}\).*ngưng hoạt động"):
        stock_service.reset_inventory(db_session, {product.id: 0})
