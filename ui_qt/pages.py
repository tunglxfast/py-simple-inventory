from __future__ import annotations

from pathlib import Path
from typing import Any

from PySide6.QtCore import QDate, Qt
from PySide6.QtWidgets import (
    QAbstractItemView,
    QComboBox,
    QDateEdit,
    QFileDialog,
    QFormLayout,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QTableWidget,
    QTableWidgetItem,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from app_paths import get_default_backup_dir
from services import WarehouseService
from ui.i18n import Translator


class BasePage(QWidget):
    def __init__(self, service: WarehouseService, tr: Translator, title_key: str) -> None:
        super().__init__()
        self.service = service
        self.tr = tr
        self.title_key = title_key

        root = QVBoxLayout(self)
        root.setContentsMargins(12, 12, 12, 12)
        root.setSpacing(10)

        self.title_label = QLabel()
        self.title_label.setStyleSheet("font-size: 18px; font-weight: 600;")
        root.addWidget(self.title_label)

        self.card = QFrame()
        self.card.setFrameShape(QFrame.StyledPanel)
        self.card_layout = QVBoxLayout(self.card)
        self.card_layout.setContentsMargins(12, 12, 12, 12)
        self.card_layout.setSpacing(8)
        root.addWidget(self.card)

        root.addStretch(1)
        self.update_language()

    def update_language(self) -> None:
        self.title_label.setText(self.tr.t(self.title_key))

    def refresh(self) -> None:
        return

    def show_error(self, message: str) -> None:
        QMessageBox.critical(self, self.tr.t("error_title"), message)

    def show_info(self, message: str) -> None:
        QMessageBox.information(self, self.tr.t("info_title"), message)


class ProductsPage(BasePage):
    def __init__(self, service: WarehouseService, tr: Translator) -> None:
        super().__init__(service, tr, "products")
        form_row = QHBoxLayout()
        self.sku_input = QLineEdit()
        self.sku_input.setPlaceholderText("SKU")
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Name")
        self.unit_input = QLineEdit()
        self.unit_input.setPlaceholderText("Unit")
        self.save_btn = QPushButton()
        self.save_btn.clicked.connect(self._create_product)
        self.update_btn = QPushButton("Update")
        self.update_btn.clicked.connect(self._update_product)
        form_row.addWidget(self.sku_input, 2)
        form_row.addWidget(self.name_input, 3)
        form_row.addWidget(self.unit_input, 1)
        form_row.addWidget(self.save_btn)
        form_row.addWidget(self.update_btn)
        self.card_layout.addLayout(form_row)

        self.inventory_table = QTableWidget(0, 4)
        self.inventory_table.setHorizontalHeaderLabels(["SKU", "Name", "Unit", "Quantity"])
        self.inventory_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.inventory_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.inventory_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.inventory_table.itemSelectionChanged.connect(self._fill_form_from_selected)
        self.inventory_table.horizontalHeader().setStretchLastSection(True)
        self.card_layout.addWidget(self.inventory_table)

        self.summary_label = QLabel()
        self.summary_label.setWordWrap(True)
        self.card_layout.addWidget(self.summary_label)
        self.update_language()

    def update_language(self) -> None:
        super().update_language()
        self.save_btn.setText(self.tr.t("save"))
        self.sku_input.setPlaceholderText(self.tr.t("sku"))
        self.name_input.setPlaceholderText(self.tr.t("name"))
        self.unit_input.setPlaceholderText(self.tr.t("unit"))
        self.update_btn.setText(self.tr.t("update"))

    def refresh(self) -> None:
        try:
            rows = self.service.get_inventory()
            self.inventory_table.setRowCount(0)
            for row_data in rows:
                row = self.inventory_table.rowCount()
                self.inventory_table.insertRow(row)
                self.inventory_table.setItem(row, 0, QTableWidgetItem(str(row_data["sku"])))
                self.inventory_table.setItem(row, 1, QTableWidgetItem(str(row_data["name"])))
                self.inventory_table.setItem(row, 2, QTableWidgetItem(str(row_data["unit"])))
                self.inventory_table.setItem(row, 3, QTableWidgetItem(str(row_data["quantity"])))
            self.summary_label.setText(self.tr.t("current_products").format(count=len(rows)))
        except Exception as err:  # noqa: BLE001
            self.show_error(str(err))

    def _create_product(self) -> None:
        try:
            self.service.create_product(
                sku=self.sku_input.text().strip(),
                name=self.name_input.text().strip(),
                unit=self.unit_input.text().strip(),
            )
            self._clear_form()
            self.refresh()
        except Exception as err:  # noqa: BLE001
            self.show_error(str(err))

    def _update_product(self) -> None:
        try:
            self.service.update_product(
                sku=self.sku_input.text().strip(),
                name=self.name_input.text().strip(),
                unit=self.unit_input.text().strip(),
            )
            self._clear_form()
            self.refresh()
        except Exception as err:  # noqa: BLE001
            self.show_error(str(err))

    def _fill_form_from_selected(self) -> None:
        selected_rows = self.inventory_table.selectionModel().selectedRows()
        if not selected_rows:
            return
        row = selected_rows[0].row()
        sku_item = self.inventory_table.item(row, 0)
        name_item = self.inventory_table.item(row, 1)
        unit_item = self.inventory_table.item(row, 2)
        self.sku_input.setText(sku_item.text() if sku_item else "")
        self.name_input.setText(name_item.text() if name_item else "")
        self.unit_input.setText(unit_item.text() if unit_item else "")

    def _clear_form(self) -> None:
        self.sku_input.clear()
        self.name_input.clear()
        self.unit_input.clear()


class MovementPage(BasePage):
    def __init__(self, service: WarehouseService, tr: Translator, mode: str) -> None:
        super().__init__(service, tr, mode)
        self.mode = mode

        self.form = QFormLayout()
        self.sku_input = QLineEdit()
        self.qty_input = QSpinBox()
        self.qty_input.setRange(1, 1_000_000_000)
        self.note_input = QLineEdit()
        self.form.addRow("SKU", self.sku_input)
        self.form.addRow("Quantity", self.qty_input)
        self.form.addRow("Note", self.note_input)

        self.submit_btn = QPushButton()
        self.submit_btn.clicked.connect(self._submit)

        self.result_label = QLabel()
        self.result_label.setWordWrap(True)

        self.card_layout.addLayout(self.form)
        self.card_layout.addWidget(self.submit_btn)
        self.card_layout.addWidget(self.result_label)
        self.update_language()

    def update_language(self) -> None:
        super().update_language()
        self.submit_btn.setText(self.tr.t("save"))
        self.sku_input.setPlaceholderText(self.tr.t("sku"))
        self.note_input.setPlaceholderText(self.tr.t("note"))

    def _submit(self) -> None:
        try:
            sku = self.sku_input.text().strip()
            if not sku:
                raise ValueError(self.tr.t("sku_required"))
            qty = int(self.qty_input.value())
            note = self.note_input.text().strip()

            if self.mode == "import":
                self.service.import_stock(sku, qty, note)
                self.result_label.setText(self.tr.t("imported_units").format(qty=qty, sku=sku))
            else:
                sale_code = self.service.export_stock(sku, qty, note)
                self.result_label.setText(self.tr.t("sale_code_msg").format(code=sale_code))

            self.note_input.clear()
        except Exception as err:  # noqa: BLE001
            self.show_error(str(err))


class HoldPage(BasePage):
    def __init__(self, service: WarehouseService, tr: Translator) -> None:
        super().__init__(service, tr, "hold")

        self.hint_label = QLabel(self.tr.t("hold_hint"))
        self.hint_label.setWordWrap(True)
        self.card_layout.addWidget(self.hint_label)

        self.table = QTableWidget(0, 2)
        self.table.setHorizontalHeaderLabels(["SKU", "Quantity"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.card_layout.addWidget(self.table)

        actions = QHBoxLayout()
        self.add_row_btn = QPushButton()
        self.add_row_btn.clicked.connect(self._add_row)
        self.remove_row_btn = QPushButton()
        self.remove_row_btn.clicked.connect(self._remove_selected_rows)
        actions.addWidget(self.add_row_btn)
        actions.addWidget(self.remove_row_btn)
        actions.addStretch(1)
        self.card_layout.addLayout(actions)

        self.note_input = QLineEdit()
        self.note_input.setPlaceholderText(self.tr.t("note"))
        self.card_layout.addWidget(self.note_input)

        self.create_btn = QPushButton()
        self.create_btn.clicked.connect(self._create_hold)
        self.card_layout.addWidget(self.create_btn)

        self.update_language()
        self._add_row()

    def update_language(self) -> None:
        super().update_language()
        self.create_btn.setText(self.tr.t("save"))
        self.note_input.setPlaceholderText(self.tr.t("note"))
        self.add_row_btn.setText(self.tr.t("add_row"))
        self.remove_row_btn.setText(self.tr.t("remove_row"))
        self.hint_label.setText(self.tr.t("hold_hint"))

    def _add_row(self) -> None:
        row = self.table.rowCount()
        self.table.insertRow(row)
        self.table.setItem(row, 0, QTableWidgetItem(""))

        spin = QSpinBox()
        spin.setRange(1, 1_000_000_000)
        spin.setValue(1)
        self.table.setCellWidget(row, 1, spin)

    def _remove_selected_rows(self) -> None:
        selected = sorted({idx.row() for idx in self.table.selectedIndexes()}, reverse=True)
        for row in selected:
            self.table.removeRow(row)
        if self.table.rowCount() == 0:
            self._add_row()

    def _create_hold(self) -> None:
        try:
            items: list[dict[str, Any]] = []
            for row in range(self.table.rowCount()):
                sku_item = self.table.item(row, 0)
                sku = sku_item.text().strip() if sku_item else ""
                if not sku:
                    continue
                qty_widget = self.table.cellWidget(row, 1)
                qty = int(qty_widget.value()) if isinstance(qty_widget, QSpinBox) else 0
                items.append({"sku": sku, "quantity": qty})

            if not items:
                raise ValueError(self.tr.t("at_least_one_row"))

            code = self.service.create_hold(items, note=self.note_input.text().strip())
            self.show_info(self.tr.t("hold_created").format(code=code))
            self.note_input.clear()
            self.table.setRowCount(0)
            self._add_row()
        except Exception as err:  # noqa: BLE001
            self.show_error(str(err))


class HoldManagementPage(BasePage):
    def __init__(self, service: WarehouseService, tr: Translator) -> None:
        super().__init__(service, tr, "hold_manage")
        self.selected_code: str | None = None

        top_row = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_btn = QPushButton()
        self.search_btn.clicked.connect(self.refresh)
        top_row.addWidget(self.search_input, 1)
        top_row.addWidget(self.search_btn)
        self.card_layout.addLayout(top_row)

        self.session_table = QTableWidget(0, 4)
        self.session_table.setHorizontalHeaderLabels(["Code", "Status", "Created At", "Note"])
        self.session_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.session_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.session_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.session_table.itemSelectionChanged.connect(self._load_selected_session)
        self.session_table.horizontalHeader().setStretchLastSection(True)
        self.card_layout.addWidget(self.session_table)

        self.items_table = QTableWidget(0, 5)
        self.items_table.setHorizontalHeaderLabels(["SKU", "Name", "Held", "Returned", "Return Now"])
        self.items_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.items_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.items_table.horizontalHeader().setStretchLastSection(True)
        self.card_layout.addWidget(self.items_table)

        actions = QHBoxLayout()
        self.finalize_btn = QPushButton()
        self.finalize_btn.clicked.connect(self._finalize_selected)
        actions.addWidget(self.finalize_btn)
        actions.addStretch(1)
        self.card_layout.addLayout(actions)
        self.update_language()

    def update_language(self) -> None:
        super().update_language()
        self.search_input.setPlaceholderText(self.tr.t("search"))
        self.search_btn.setText(self.tr.t("refresh"))
        self.finalize_btn.setText(self.tr.t("finalize"))

    def refresh(self) -> None:
        try:
            sessions = self.service.get_hold_sessions(self.search_input.text().strip())
            self.session_table.setRowCount(0)
            for row_data in sessions:
                row = self.session_table.rowCount()
                self.session_table.insertRow(row)
                self.session_table.setItem(row, 0, QTableWidgetItem(str(row_data["code"])))
                self.session_table.setItem(row, 1, QTableWidgetItem(str(row_data["status"])))
                self.session_table.setItem(row, 2, QTableWidgetItem(str(row_data["created_at"])))
                self.session_table.setItem(row, 3, QTableWidgetItem(str(row_data.get("note") or "")))
            self.items_table.setRowCount(0)
            self.selected_code = None
        except Exception as err:  # noqa: BLE001
            self.show_error(str(err))

    def _load_selected_session(self) -> None:
        selected_rows = self.session_table.selectionModel().selectedRows()
        if not selected_rows:
            return
        row = selected_rows[0].row()
        code_item = self.session_table.item(row, 0)
        if code_item is None:
            return
        code = code_item.text().strip()
        if not code:
            return
        try:
            details = self.service.get_hold_details(code)
            self.selected_code = code
            self.items_table.setRowCount(0)
            for item in details["items"]:
                table_row = self.items_table.rowCount()
                self.items_table.insertRow(table_row)
                self.items_table.setItem(table_row, 0, QTableWidgetItem(str(item["sku"])))
                self.items_table.setItem(table_row, 1, QTableWidgetItem(str(item["name"])))
                self.items_table.setItem(table_row, 2, QTableWidgetItem(str(item["quantity"])))
                self.items_table.setItem(table_row, 3, QTableWidgetItem(str(item["returned_quantity"])))

                remaining = max(0, int(item["quantity"]) - int(item["returned_quantity"]))
                spin = QSpinBox()
                spin.setRange(0, remaining)
                spin.setValue(0)
                self.items_table.setCellWidget(table_row, 4, spin)
        except Exception as err:  # noqa: BLE001
            self.show_error(str(err))

    def _finalize_selected(self) -> None:
        if not self.selected_code:
            QMessageBox.warning(self, self.tr.t("warning_title"), self.tr.t("select_hold_first"))
            return
        try:
            confirm = QMessageBox.question(
                self,
                self.tr.t("confirm_finalize_title"),
                self.tr.t("confirm_finalize_msg"),
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No,
            )
            if confirm != QMessageBox.Yes:
                return
            returns: list[dict[str, Any]] = []
            for row in range(self.items_table.rowCount()):
                sku_item = self.items_table.item(row, 0)
                if sku_item is None:
                    continue
                sku = sku_item.text().strip()
                widget = self.items_table.cellWidget(row, 4)
                qty = int(widget.value()) if isinstance(widget, QSpinBox) else 0
                if qty > 0:
                    returns.append({"sku": sku, "quantity": qty})

            sale_code = self.service.finalize_hold(self.selected_code, returns)
            self.show_info(self.tr.t("finalized_with_sale").format(code=sale_code))
            self.refresh()
        except Exception as err:  # noqa: BLE001
            self.show_error(str(err))


class SalesPage(BasePage):
    def __init__(self, service: WarehouseService, tr: Translator) -> None:
        super().__init__(service, tr, "sales")
        self.sales_table = QTableWidget(0, 5)
        self.sales_table.setHorizontalHeaderLabels(["Code", "Hold Session", "Created At", "Items", "Note"])
        self.sales_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.sales_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.sales_table.horizontalHeader().setStretchLastSection(True)
        self.card_layout.addWidget(self.sales_table)

    def refresh(self) -> None:
        try:
            sales = self.service.get_sales()
            self.sales_table.setRowCount(0)
            for row_data in sales:
                row = self.sales_table.rowCount()
                self.sales_table.insertRow(row)
                items_text = "; ".join(
                    f"{item['sku']} x {item['quantity']}" for item in row_data.get("items", [])
                )
                self.sales_table.setItem(row, 0, QTableWidgetItem(str(row_data["code"])))
                self.sales_table.setItem(row, 1, QTableWidgetItem(str(row_data["hold_session_id"] or "")))
                self.sales_table.setItem(row, 2, QTableWidgetItem(str(row_data["created_at"])))
                self.sales_table.setItem(row, 3, QTableWidgetItem(items_text))
                self.sales_table.setItem(row, 4, QTableWidgetItem(str(row_data.get("note") or "")))
        except Exception as err:  # noqa: BLE001
            self.show_error(str(err))


class ReportsPage(BasePage):
    def __init__(self, service: WarehouseService, tr: Translator) -> None:
        super().__init__(service, tr, "reports")

        date_row = QHBoxLayout()
        self.from_label = QLabel()
        self.from_date = QDateEdit()
        self.from_date.setCalendarPopup(True)
        self.from_date.setDisplayFormat("yyyy-MM-dd")
        self.to_label = QLabel()
        self.to_date = QDateEdit()
        self.to_date.setCalendarPopup(True)
        self.to_date.setDisplayFormat("yyyy-MM-dd")
        today = QDate.currentDate()
        self.from_date.setDate(today)
        self.to_date.setDate(today)
        self.load_btn = QPushButton()
        self.load_btn.clicked.connect(self._load_report)
        date_row.addWidget(self.from_label)
        date_row.addWidget(self.from_date)
        date_row.addWidget(self.to_label)
        date_row.addWidget(self.to_date)
        date_row.addWidget(self.load_btn)
        date_row.addStretch(1)
        self.card_layout.addLayout(date_row)

        self.inventory_title = QLabel(self.tr.t("inventory_title"))
        self.card_layout.addWidget(self.inventory_title)
        self.inventory_table = QTableWidget(0, 4)
        self.inventory_table.setHorizontalHeaderLabels(["SKU", "Name", "Unit", "Quantity"])
        self.inventory_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.inventory_table.horizontalHeader().setStretchLastSection(True)
        self.card_layout.addWidget(self.inventory_table)

        self.summary_title = QLabel(self.tr.t("stock_summary_title"))
        self.card_layout.addWidget(self.summary_title)
        self.summary_table = QTableWidget(0, 6)
        self.summary_table.setHorizontalHeaderLabels(
            ["SKU", "Name", "Opening", "Import", "Export", "Closing"]
        )
        self.summary_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.summary_table.horizontalHeader().setStretchLastSection(True)
        self.card_layout.addWidget(self.summary_table)
        self.update_language()

    def update_language(self) -> None:
        super().update_language()
        self.from_label.setText(self.tr.t("from_date"))
        self.to_label.setText(self.tr.t("to_date"))
        self.load_btn.setText(self.tr.t("load_report"))
        self.inventory_title.setText(self.tr.t("inventory_title"))
        self.summary_title.setText(self.tr.t("stock_summary_title"))

    def refresh(self) -> None:
        try:
            inventory = self.service.get_inventory()
            self.inventory_table.setRowCount(0)
            for row_data in inventory:
                row = self.inventory_table.rowCount()
                self.inventory_table.insertRow(row)
                self.inventory_table.setItem(row, 0, QTableWidgetItem(str(row_data["sku"])))
                self.inventory_table.setItem(row, 1, QTableWidgetItem(str(row_data["name"])))
                self.inventory_table.setItem(row, 2, QTableWidgetItem(str(row_data["unit"])))
                self.inventory_table.setItem(row, 3, QTableWidgetItem(str(row_data["quantity"])))
            self._load_report()
        except Exception as err:  # noqa: BLE001
            self.show_error(str(err))

    def _load_report(self) -> None:
        try:
            from_date = self.from_date.date().toString("yyyy-MM-dd")
            to_date = self.to_date.date().toString("yyyy-MM-dd")
            rows = self.service.get_report(from_date, to_date)
            self.summary_table.setRowCount(0)
            for row_data in rows:
                row = self.summary_table.rowCount()
                self.summary_table.insertRow(row)
                self.summary_table.setItem(row, 0, QTableWidgetItem(str(row_data["sku"])))
                self.summary_table.setItem(row, 1, QTableWidgetItem(str(row_data["name"])))
                self.summary_table.setItem(row, 2, QTableWidgetItem(str(row_data["opening"])))
                self.summary_table.setItem(row, 3, QTableWidgetItem(str(row_data["import"])))
                self.summary_table.setItem(row, 4, QTableWidgetItem(str(row_data["export"])))
                self.summary_table.setItem(row, 5, QTableWidgetItem(str(row_data["closing"])))
        except Exception as err:  # noqa: BLE001
            self.show_error(str(err))


class SetupPage(BasePage):
    def __init__(self, service: WarehouseService, tr: Translator) -> None:
        super().__init__(service, tr, "setup")

        import_row = QHBoxLayout()
        self.file_input = QLineEdit()
        self.pick_file_btn = QPushButton("...")
        self.pick_file_btn.clicked.connect(self._pick_file)
        import_row.addWidget(self.file_input, 1)
        import_row.addWidget(self.pick_file_btn)
        self.card_layout.addWidget(QLabel(self.tr.t("initial_stock_file")))
        self.card_layout.addLayout(import_row)

        import_actions = QHBoxLayout()
        self.preview_btn = QPushButton()
        self.preview_btn.clicked.connect(self._preview)
        self.import_btn = QPushButton()
        self.import_btn.clicked.connect(self._import)
        import_actions.addWidget(self.preview_btn)
        import_actions.addWidget(self.import_btn)
        import_actions.addStretch(1)
        self.card_layout.addLayout(import_actions)

        self.preview_text = QTextEdit()
        self.preview_text.setReadOnly(True)
        self.preview_text.setMinimumHeight(140)
        self.card_layout.addWidget(self.preview_text)

        reset_row = QHBoxLayout()
        self.reset_token_input = QLineEdit()
        self.reset_mode = QComboBox()
        self.reset_mode.addItems(["full", "safe"])
        self.reset_btn = QPushButton()
        self.reset_btn.clicked.connect(self._reset)
        reset_row.addWidget(QLabel(self.tr.t("reset_token")))
        reset_row.addWidget(self.reset_token_input)
        reset_row.addWidget(self.reset_mode)
        reset_row.addWidget(self.reset_btn)
        self.card_layout.addLayout(reset_row)

        backup_row = QHBoxLayout()
        self.dest_input = QLineEdit(str(get_default_backup_dir()))
        self.pick_dest_btn = QPushButton("...")
        self.pick_dest_btn.clicked.connect(self._pick_dest)
        self.backup_btn = QPushButton()
        self.backup_btn.clicked.connect(self._backup)
        self.restore_btn = QPushButton()
        self.restore_btn.clicked.connect(self._restore)
        backup_row.addWidget(self.dest_input, 1)
        backup_row.addWidget(self.pick_dest_btn)
        backup_row.addWidget(self.backup_btn)
        backup_row.addWidget(self.restore_btn)
        self.card_layout.addWidget(QLabel(self.tr.t("destination")))
        self.card_layout.addLayout(backup_row)

        self.update_language()

    def update_language(self) -> None:
        super().update_language()
        self.preview_btn.setText(self.tr.t("preview"))
        self.import_btn.setText(self.tr.t("import_initial"))
        self.reset_btn.setText(self.tr.t("reset_db"))
        self.backup_btn.setText(self.tr.t("backup"))
        self.restore_btn.setText(self.tr.t("restore"))

    def _pick_file(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self, self.tr.t("select_file"), "", "Excel/CSV (*.xlsx *.xlsm *.csv)"
        )
        if path:
            self.file_input.setText(path)

    def _pick_dest(self) -> None:
        path = QFileDialog.getExistingDirectory(self, self.tr.t("select_destination"))
        if path:
            self.dest_input.setText(path)

    def _preview(self) -> None:
        try:
            rows = self.service.import_initial_stock_from_excel(
                self.file_input.text().strip(), preview_only=True
            )
            self.preview_text.setPlainText("\n".join(str(row) for row in rows))
        except Exception as err:  # noqa: BLE001
            self.show_error(str(err))

    def _import(self) -> None:
        try:
            rows = self.service.import_initial_stock_from_excel(
                self.file_input.text().strip(), preview_only=False
            )
            self.show_info(self.tr.t("imported_rows").format(count=len(rows)))
        except Exception as err:  # noqa: BLE001
            self.show_error(str(err))

    def _reset(self) -> None:
        try:
            confirm = QMessageBox.question(
                self,
                self.tr.t("confirm_reset_title"),
                self.tr.t("confirm_reset_msg"),
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No,
            )
            if confirm != QMessageBox.Yes:
                return
            self.service.reset_database(
                mode=self.reset_mode.currentText().strip(),
                confirm_token=self.reset_token_input.text().strip(),
            )
            self.show_info(self.tr.t("db_reset_completed"))
        except Exception as err:  # noqa: BLE001
            self.show_error(str(err))

    def _backup(self) -> None:
        try:
            output = self.service.backup_db(self.dest_input.text().strip())
            self.show_info(self.tr.t("backup_created").format(path=output))
        except Exception as err:  # noqa: BLE001
            self.show_error(str(err))

    def _restore(self) -> None:
        backup_file, _ = QFileDialog.getOpenFileName(
            self, self.tr.t("select_backup_db"), "", "SQLite (*.db)"
        )
        if not backup_file:
            return

        confirm_1 = QMessageBox.warning(
            self,
            self.tr.t("confirm_restore_title"),
            self.tr.t("confirm_restore_msg"),
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if confirm_1 != QMessageBox.Yes:
            return

        file_name = Path(backup_file).name
        confirm_2 = QMessageBox.question(
            self,
            self.tr.t("confirm_backup_file_title"),
            self.tr.t("confirm_backup_file_msg").format(filename=file_name),
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if confirm_2 != QMessageBox.Yes:
            return

        try:
            self.service.restore_db(backup_file)
            self.show_info(self.tr.t("restore_completed_restart"))
        except Exception as err:  # noqa: BLE001
            self.show_error(str(err))
