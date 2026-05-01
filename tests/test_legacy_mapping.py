from __future__ import annotations

from services import ValidationError


def test_parse_legacy_initial_rows_ignores_employee_block_and_reads_item_block(service):
    rows = [
        ["STT", "MÃ NV", "TÊN NV", "", "", "", "", "STT", "MÃ HÀNG", "TÊN HÀNG HÓA", "ĐVT", "TỒN", "MA_NV", "MA_VT", "SL"],
        [1, "NV01", "A", "", "", "", "", 1, "DP.S", "Đồng phục size S", "Bộ", 66, "NV01", "DP.S", 1],
        [2, "NV02", "B", "", "", "", "", 2, "GIAY.30", "Giày size 30", "Đôi", 10, "NV02", "GIAY.30", 2],
    ]

    parsed = service._parse_legacy_initial_rows(rows)
    assert parsed == [
        {"sku": "DP.S", "name": "Đồng phục size S", "unit": "Bộ", "quantity": 66},
        {"sku": "GIAY.30", "name": "Giày size 30", "unit": "Đôi", "quantity": 10},
    ]


def test_parse_legacy_initial_rows_by_header_not_fixed_position(service):
    rows = [
        ["MÃ HÀNG", "GHI CHÚ", "ĐVT", "TÊN HÀNG HÓA", "TỒN"],
        ["DP.S", "", "Bộ", "Đồng phục size S", 66],
    ]
    parsed = service._parse_legacy_initial_rows(rows)
    assert parsed == [
        {"sku": "DP.S", "name": "Đồng phục size S", "unit": "Bộ", "quantity": 66}
    ]


def test_parse_legacy_initial_rows_duplicate_sku_raises(service):
    rows = [
        ["h"],
        [None, None, None, None, None, None, None, None, "DP.S", "A", "Bộ", 1],
        [None, None, None, None, None, None, None, None, "DP.S", "A", "Bộ", 2],
    ]
    try:
        service._parse_legacy_initial_rows(rows)
        assert False, "Expected ValidationError"
    except ValidationError:
        assert True


def test_parse_legacy_transaction_rows_maps_nhap_lieu_columns(service):
    rows = [
        [],
        [],
        [],
        ["STT", "NV ĐỀ XUẤT", "NGÀY", "KHU VỰC", "DIỄN GIẢI", "NHẬP", "XUẤT", "SOLUONG", "GHI CHÚ", "TRẢ BILL", "ĐỊA CHỈ", "ĐIỆN THOẠI"],
        [1, "THY", "18/3", "MN SAO MAI 12", "XUYẾN", "GIAY.30", "", 1, "", "", "", ""],
        [2, "THY", "18/3", "TÂN TIẾN", "NGUYỄN CHÍ HIẾU", "", "DP.7", 2, "ghi chú", "x", "addr", "0909"],
    ]

    parsed = service._parse_legacy_transaction_rows(rows)
    assert len(parsed) == 2
    assert parsed[0]["direction"] == "IMPORT"
    assert parsed[0]["sku"] == "GIAY.30"
    assert parsed[0]["employee_name"] == "THY"
    assert parsed[1]["direction"] == "EXPORT"
    assert parsed[1]["sku"] == "DP.7"
    assert parsed[1]["quantity"] == 2


def test_parse_legacy_transaction_rows_by_header_not_fixed_position(service):
    rows = [
        ["DIỄN GIẢI", "XUẤT", "NGÀY", "SOLUONG", "NV ĐỀ XUẤT", "KHU VỰC", "NHẬP"],
        ["abc", "", "18/3", 3, "THY", "KV1", "GIAY.31"],
    ]
    parsed = service._parse_legacy_transaction_rows(rows)
    assert len(parsed) == 1
    assert parsed[0]["direction"] == "IMPORT"
    assert parsed[0]["sku"] == "GIAY.31"
    assert parsed[0]["quantity"] == 3
    assert parsed[0]["employee_name"] == "THY"


def test_reset_database_clears_stock_transactions(service):
    service.create_product("DP.S", "Dong phuc S", "Bo")
    with service.db.transaction() as conn:
        conn.execute(
            """
            INSERT INTO stock_transactions (
                transaction_code, employee_name, transaction_date, area, description,
                sku, quantity, direction, note, bill_return, address, phone, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                "LEGACY-00001",
                "THY",
                "2026-03-18",
                "KHU A",
                "TEST",
                "DP.S",
                1,
                "IMPORT",
                "",
                "",
                "",
                "",
                "2026-03-18T00:00:00Z",
            ),
        )

    service.reset_database(mode="safe", confirm_token="RESET")
    with service.db.connection() as conn:
        c = conn.execute("SELECT COUNT(*) AS c FROM stock_transactions").fetchone()["c"]
    assert c == 0
