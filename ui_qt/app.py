from __future__ import annotations

import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QSplitter,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from services import ServiceError, WarehouseService
from ui.i18n import Translator
from ui_qt.pages import (
    HoldManagementPage,
    HoldPage,
    MovementPage,
    ProductsPage,
    ReportsPage,
    SalesPage,
    SetupPage,
)


class MainWindow(QMainWindow):
    NAV_ORDER = [
        "products",
        "import",
        "export",
        "hold",
        "hold_manage",
        "sales",
        "reports",
        "setup",
    ]

    def __init__(self, service: WarehouseService) -> None:
        super().__init__()
        self.service = service
        self.tr = Translator()
        self.current_key = "products"

        self.setMinimumSize(960, 640)
        self.resize(1240, 780)

        self.pages: dict[str, QWidget] = {}
        self.page_indexes: dict[str, int] = {}

        self._build_ui()
        self._create_pages()
        self._update_language()
        self.show_page("products")

    def _build_ui(self) -> None:
        root = QWidget()
        self.setCentralWidget(root)

        outer = QHBoxLayout(root)
        outer.setContentsMargins(8, 8, 8, 8)

        splitter = QSplitter(Qt.Horizontal)
        outer.addWidget(splitter)

        sidebar = QWidget()
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(8, 8, 8, 8)
        sidebar_layout.setSpacing(8)

        lang_row = QHBoxLayout()
        self.lang_label = QLabel()
        self.lang_select = QComboBox()
        self.lang_select.addItems(["vi", "en"])
        self.lang_select.setCurrentText("vi")
        self.lang_select.currentTextChanged.connect(self._on_language_change)
        lang_row.addWidget(self.lang_label)
        lang_row.addWidget(self.lang_select)
        sidebar_layout.addLayout(lang_row)

        self.nav_list = QListWidget()
        self.nav_list.currentRowChanged.connect(self._on_nav_selected)
        sidebar_layout.addWidget(self.nav_list, 1)

        self.refresh_btn = QPushButton("Refresh")
        self.refresh_btn.clicked.connect(self._refresh_current_page)
        sidebar_layout.addWidget(self.refresh_btn)

        self.stack = QStackedWidget()

        splitter.addWidget(sidebar)
        splitter.addWidget(self.stack)
        splitter.setSizes([230, 1010])

    def _create_pages(self) -> None:
        self.pages = {
            "products": ProductsPage(self.service, self.tr),
            "import": MovementPage(self.service, self.tr, "import"),
            "export": MovementPage(self.service, self.tr, "export"),
            "hold": HoldPage(self.service, self.tr),
            "hold_manage": HoldManagementPage(self.service, self.tr),
            "sales": SalesPage(self.service, self.tr),
            "reports": ReportsPage(self.service, self.tr),
            "setup": SetupPage(self.service, self.tr),
        }

        self.nav_list.clear()
        self.page_indexes.clear()
        for idx, key in enumerate(self.NAV_ORDER):
            self.page_indexes[key] = idx
            self.nav_list.addItem(QListWidgetItem())
            self.stack.addWidget(self.pages[key])

    def _update_language(self) -> None:
        self.setWindowTitle(self.tr.t("app_title") + " (PySide6)")
        self.lang_label.setText(f"{self.tr.t('language')}:")
        self.refresh_btn.setText(self.tr.t("refresh"))

        for idx, key in enumerate(self.NAV_ORDER):
            item = self.nav_list.item(idx)
            item.setText(self.tr.t(key))

        for page in self.pages.values():
            update = getattr(page, "update_language", None)
            if callable(update):
                update()

    def _on_language_change(self, language: str) -> None:
        self.tr.set_language(language)
        self._update_language()

    def _on_nav_selected(self, row: int) -> None:
        if row < 0 or row >= len(self.NAV_ORDER):
            return
        key = self.NAV_ORDER[row]
        self.show_page(key)

    def show_page(self, key: str) -> None:
        self.current_key = key
        self.stack.setCurrentIndex(self.page_indexes[key])
        self._refresh_current_page()

    def _refresh_current_page(self) -> None:
        page = self.pages[self.current_key]
        refresh = getattr(page, "refresh", None)
        if callable(refresh):
            try:
                refresh()
            except ServiceError as err:
                QMessageBox.critical(self, self.tr.t("error_title"), str(err))
            except Exception as err:  # noqa: BLE001
                QMessageBox.critical(self, self.tr.t("error_title"), str(err))


def run_qt_app(service: WarehouseService) -> int:
    app = QApplication.instance() or QApplication(sys.argv)
    window = MainWindow(service)
    window.show()
    return app.exec()
