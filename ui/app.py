"""Tkinter desktop UI for warehouse management."""

from __future__ import annotations

import tkinter as tk
from datetime import datetime
from tkinter import filedialog, messagebox, ttk
from typing import Any

from app_paths import get_default_backup_dir
from services import ServiceError, WarehouseService
from ui.i18n import Translator


class WarehouseApp(tk.Tk):
    def __init__(self, service: WarehouseService) -> None:
        super().__init__()
        self.service = service
        self.tr = Translator()
        self.title(self.tr.t("app_title"))
        self.geometry("1200x760")
        self.minsize(960, 640)

        self._build_layout()
        self._create_pages()
        self.show_page("products")

    def _build_layout(self) -> None:
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        self.sidebar = ttk.Frame(self, padding=8)
        self.sidebar.grid(row=0, column=0, sticky="ns")

        self.content = ttk.Frame(self, padding=8)
        self.content.grid(row=0, column=1, sticky="nsew")
        self.content.columnconfigure(0, weight=1)
        self.content.rowconfigure(0, weight=1)

        lang_frame = ttk.Frame(self.sidebar)
        lang_frame.pack(fill="x", pady=(0, 12))
        ttk.Label(lang_frame, text=f"{self.tr.t('language')}:").pack(side="left")
        self.lang_var = tk.StringVar(value="vi")
        lang_select = ttk.Combobox(
            lang_frame, textvariable=self.lang_var, values=["vi", "en"], width=7, state="readonly"
        )
        lang_select.pack(side="left", padx=6)
        lang_select.bind("<<ComboboxSelected>>", self._on_language_change)

        self.nav_buttons: dict[str, ttk.Button] = {}

    def _create_pages(self) -> None:
        self.pages: dict[str, BasePage] = {
            "products": ProductsPage(self.content, self.service, self.tr),
            "import": MovementPage(self.content, self.service, self.tr, mode="import"),
            "export": MovementPage(self.content, self.service, self.tr, mode="export"),
            "hold": HoldPage(self.content, self.service, self.tr),
            "hold_manage": HoldManagementPage(self.content, self.service, self.tr),
            "sales": SalesPage(self.content, self.service, self.tr),
            "reports": ReportsPage(self.content, self.service, self.tr),
            "setup": SetupPage(self.content, self.service, self.tr),
        }

        for page in self.pages.values():
            page.grid(row=0, column=0, sticky="nsew")

        nav_order = [
            "products",
            "import",
            "export",
            "hold",
            "hold_manage",
            "sales",
            "reports",
            "setup",
        ]
        for key in nav_order:
            btn = ttk.Button(
                self.sidebar, text=self.tr.t(key), command=lambda k=key: self.show_page(k)
            )
            btn.pack(fill="x", pady=2)
            self.nav_buttons[key] = btn

    def show_page(self, key: str) -> None:
        page = self.pages[key]
        page.tkraise()
        page.refresh()

    def _on_language_change(self, _: Any) -> None:
        self.tr.set_language(self.lang_var.get())
        self.title(self.tr.t("app_title"))
        for key, btn in self.nav_buttons.items():
            btn.configure(text=self.tr.t(key))
        for page in self.pages.values():
            page.update_language()


class BasePage(ttk.Frame):
    def __init__(self, parent: tk.Widget, service: WarehouseService, tr: Translator) -> None:
        super().__init__(parent)
        self.service = service
        self.tr = tr

    def refresh(self) -> None:
        return

    def update_language(self) -> None:
        return

    def show_error(self, err: Exception) -> None:
        messagebox.showerror("Error", str(err))

    def show_info(self, msg: str) -> None:
        messagebox.showinfo("Info", msg)


class ProductsPage(BasePage):
    def __init__(self, parent: tk.Widget, service: WarehouseService, tr: Translator) -> None:
        super().__init__(parent, service, tr)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        form = ttk.Frame(self)
        form.grid(row=0, column=0, sticky="ew", pady=(0, 8))
        for i in range(7):
            form.columnconfigure(i, weight=1 if i in (1, 3, 5) else 0)

        self.lbl_sku = ttk.Label(form)
        self.lbl_sku.grid(row=0, column=0, padx=4)
        self.ent_sku = ttk.Entry(form)
        self.ent_sku.grid(row=0, column=1, sticky="ew", padx=4)

        self.lbl_name = ttk.Label(form)
        self.lbl_name.grid(row=0, column=2, padx=4)
        self.ent_name = ttk.Entry(form)
        self.ent_name.grid(row=0, column=3, sticky="ew", padx=4)

        self.lbl_unit = ttk.Label(form)
        self.lbl_unit.grid(row=0, column=4, padx=4)
        self.ent_unit = ttk.Entry(form)
        self.ent_unit.grid(row=0, column=5, sticky="ew", padx=4)

        self.btn_save = ttk.Button(form, command=self._save)
        self.btn_save.grid(row=0, column=6, padx=4)

        columns = ("sku", "name", "unit", "quantity")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col.upper())
            self.tree.column(col, anchor="center")
        self.tree.grid(row=1, column=0, sticky="nsew")
        self.update_language()

    def update_language(self) -> None:
        self.lbl_sku.configure(text=self.tr.t("sku"))
        self.lbl_name.configure(text=self.tr.t("name"))
        self.lbl_unit.configure(text=self.tr.t("unit"))
        self.btn_save.configure(text=self.tr.t("save"))

    def _save(self) -> None:
        try:
            self.service.create_product(
                sku=self.ent_sku.get(),
                name=self.ent_name.get(),
                unit=self.ent_unit.get(),
            )
            self.refresh()
            self.ent_sku.delete(0, tk.END)
            self.ent_name.delete(0, tk.END)
            self.ent_unit.delete(0, tk.END)
        except ServiceError as err:
            self.show_error(err)

    def refresh(self) -> None:
        for row in self.tree.get_children():
            self.tree.delete(row)
        for row in self.service.get_inventory():
            self.tree.insert("", tk.END, values=(row["sku"], row["name"], row["unit"], row["quantity"]))


class MovementPage(BasePage):
    def __init__(
        self,
        parent: tk.Widget,
        service: WarehouseService,
        tr: Translator,
        mode: str,
    ) -> None:
        super().__init__(parent, service, tr)
        self.mode = mode

        form = ttk.Frame(self, padding=8)
        form.pack(fill="x")
        for i in range(7):
            form.columnconfigure(i, weight=1 if i in (1, 3, 5) else 0)

        self.lbl_sku = ttk.Label(form)
        self.lbl_sku.grid(row=0, column=0, padx=4)
        self.ent_sku = ttk.Entry(form)
        self.ent_sku.grid(row=0, column=1, sticky="ew", padx=4)

        self.lbl_qty = ttk.Label(form)
        self.lbl_qty.grid(row=0, column=2, padx=4)
        self.ent_qty = ttk.Entry(form)
        self.ent_qty.grid(row=0, column=3, sticky="ew", padx=4)

        self.lbl_note = ttk.Label(form)
        self.lbl_note.grid(row=0, column=4, padx=4)
        self.ent_note = ttk.Entry(form)
        self.ent_note.grid(row=0, column=5, sticky="ew", padx=4)

        self.btn_save = ttk.Button(form, command=self._submit)
        self.btn_save.grid(row=0, column=6, padx=4)
        self.update_language()

    def update_language(self) -> None:
        self.lbl_sku.configure(text=self.tr.t("sku"))
        self.lbl_qty.configure(text=self.tr.t("quantity"))
        self.lbl_note.configure(text=self.tr.t("note"))
        self.btn_save.configure(text=self.tr.t("save"))

    def _submit(self) -> None:
        try:
            qty = int(self.ent_qty.get())
            if self.mode == "import":
                self.service.import_stock(self.ent_sku.get(), qty, self.ent_note.get())
            else:
                sale_code = self.service.export_stock(self.ent_sku.get(), qty, self.ent_note.get())
                self.show_info(f"Sale code: {sale_code}")
            self.ent_qty.delete(0, tk.END)
            self.ent_note.delete(0, tk.END)
        except ValueError:
            self.show_error(ValueError("Quantity must be integer"))
        except ServiceError as err:
            self.show_error(err)


class HoldPage(BasePage):
    def __init__(self, parent: tk.Widget, service: WarehouseService, tr: Translator) -> None:
        super().__init__(parent, service, tr)
        ttk.Label(self, text="SKU,Quantity per line").pack(anchor="w")
        self.txt_items = tk.Text(self, height=12)
        self.txt_items.pack(fill="x", pady=4)

        note_frame = ttk.Frame(self)
        note_frame.pack(fill="x", pady=4)
        self.lbl_note = ttk.Label(note_frame)
        self.lbl_note.pack(side="left")
        self.ent_note = ttk.Entry(note_frame)
        self.ent_note.pack(side="left", fill="x", expand=True, padx=8)

        self.btn_save = ttk.Button(self, command=self._create_hold)
        self.btn_save.pack(anchor="w", pady=4)
        self.update_language()

    def update_language(self) -> None:
        self.lbl_note.configure(text=self.tr.t("note"))
        self.btn_save.configure(text=self.tr.t("save"))

    def _create_hold(self) -> None:
        items = []
        for line in self.txt_items.get("1.0", tk.END).splitlines():
            line = line.strip()
            if not line:
                continue
            sku, qty = [part.strip() for part in line.split(",", maxsplit=1)]
            items.append({"sku": sku, "quantity": int(qty)})
        try:
            code = self.service.create_hold(items, note=self.ent_note.get())
            self.show_info(f"Hold created: {code}")
            self.txt_items.delete("1.0", tk.END)
            self.ent_note.delete(0, tk.END)
        except Exception as err:  # noqa: BLE001
            self.show_error(err)


class HoldManagementPage(BasePage):
    def __init__(self, parent: tk.Widget, service: WarehouseService, tr: Translator) -> None:
        super().__init__(parent, service, tr)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)

        top = ttk.Frame(self)
        top.grid(row=0, column=0, sticky="ew")
        top.columnconfigure(1, weight=1)
        self.lbl_search = ttk.Label(top)
        self.lbl_search.grid(row=0, column=0, padx=4)
        self.ent_search = ttk.Entry(top)
        self.ent_search.grid(row=0, column=1, sticky="ew", padx=4)
        self.btn_search = ttk.Button(top, command=self.refresh)
        self.btn_search.grid(row=0, column=2, padx=4)

        self.sessions = ttk.Treeview(self, columns=("code", "status", "created_at"), show="headings", height=6)
        for col in ("code", "status", "created_at"):
            self.sessions.heading(col, text=col.upper())
            self.sessions.column(col, anchor="center")
        self.sessions.grid(row=1, column=0, sticky="ew", pady=4)
        self.sessions.bind("<<TreeviewSelect>>", self._load_selected)

        bottom = ttk.Frame(self)
        bottom.grid(row=2, column=0, sticky="nsew")
        bottom.columnconfigure(0, weight=1)
        bottom.rowconfigure(1, weight=1)

        ttk.Label(bottom, text="RETURN lines: SKU,Quantity").grid(row=0, column=0, sticky="w")
        self.txt_returns = tk.Text(bottom, height=6)
        self.txt_returns.grid(row=1, column=0, sticky="nsew", pady=4)
        self.btn_finalize = ttk.Button(bottom, command=self._finalize)
        self.btn_finalize.grid(row=2, column=0, sticky="w")
        self.update_language()

    def update_language(self) -> None:
        self.lbl_search.configure(text=self.tr.t("search"))
        self.btn_search.configure(text=self.tr.t("refresh"))
        self.btn_finalize.configure(text=self.tr.t("finalize"))

    def refresh(self) -> None:
        for row in self.sessions.get_children():
            self.sessions.delete(row)
        sessions = self.service.get_hold_sessions(self.ent_search.get())
        for s in sessions:
            self.sessions.insert("", tk.END, iid=str(s["id"]), values=(s["code"], s["status"], s["created_at"]))

    def _load_selected(self, _: Any) -> None:
        selected = self.sessions.selection()
        if not selected:
            return
        item = self.sessions.item(selected[0])
        code = item["values"][0]
        details = self.service.get_hold_details(code)
        lines = []
        for row in details["items"]:
            lines.append(f"{row['sku']},0")
        self.txt_returns.delete("1.0", tk.END)
        self.txt_returns.insert("1.0", "\n".join(lines))

    def _finalize(self) -> None:
        selected = self.sessions.selection()
        if not selected:
            self.show_error(ValueError("Select a hold session first"))
            return
        code = self.sessions.item(selected[0])["values"][0]
        returns = []
        for line in self.txt_returns.get("1.0", tk.END).splitlines():
            line = line.strip()
            if not line:
                continue
            sku, qty = [p.strip() for p in line.split(",", maxsplit=1)]
            returns.append({"sku": sku, "quantity": int(qty)})
        try:
            sale_code = self.service.finalize_hold(code, returns)
            self.show_info(f"Finalized with sale: {sale_code}")
            self.refresh()
        except Exception as err:  # noqa: BLE001
            self.show_error(err)


class SalesPage(BasePage):
    def __init__(self, parent: tk.Widget, service: WarehouseService, tr: Translator) -> None:
        super().__init__(parent, service, tr)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        self.btn_refresh = ttk.Button(self, command=self.refresh)
        self.btn_refresh.grid(row=0, column=0, sticky="w")
        self.tree = ttk.Treeview(
            self,
            columns=("code", "hold_session_id", "created_at", "items"),
            show="headings",
        )
        for col in ("code", "hold_session_id", "created_at", "items"):
            self.tree.heading(col, text=col.upper())
            self.tree.column(col, anchor="center")
        self.tree.grid(row=1, column=0, sticky="nsew")
        self.update_language()

    def update_language(self) -> None:
        self.btn_refresh.configure(text=self.tr.t("refresh"))

    def refresh(self) -> None:
        for row in self.tree.get_children():
            self.tree.delete(row)
        for sale in self.service.get_sales():
            items_text = "; ".join(f"{it['sku']} x {it['quantity']}" for it in sale["items"])
            self.tree.insert(
                "",
                tk.END,
                values=(sale["code"], sale["hold_session_id"], sale["created_at"], items_text),
            )


class ReportsPage(BasePage):
    def __init__(self, parent: tk.Widget, service: WarehouseService, tr: Translator) -> None:
        super().__init__(parent, service, tr)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)

        top = ttk.Frame(self)
        top.grid(row=0, column=0, sticky="ew", pady=4)
        for i in range(7):
            top.columnconfigure(i, weight=1 if i in (1, 3) else 0)

        today = datetime.now().strftime("%Y-%m-%d")
        self.lbl_from = ttk.Label(top)
        self.lbl_from.grid(row=0, column=0)
        self.ent_from = ttk.Entry(top)
        self.ent_from.insert(0, today)
        self.ent_from.grid(row=0, column=1, sticky="ew", padx=4)

        self.lbl_to = ttk.Label(top)
        self.lbl_to.grid(row=0, column=2)
        self.ent_to = ttk.Entry(top)
        self.ent_to.insert(0, today)
        self.ent_to.grid(row=0, column=3, sticky="ew", padx=4)

        self.btn_load = ttk.Button(top, command=self._load_summary)
        self.btn_load.grid(row=0, column=4, padx=4)

        ttk.Label(self, text="Inventory").grid(row=1, column=0, sticky="w")
        self.inventory_tree = ttk.Treeview(
            self,
            columns=("sku", "name", "unit", "quantity"),
            show="headings",
            height=8,
        )
        for col in ("sku", "name", "unit", "quantity"):
            self.inventory_tree.heading(col, text=col.upper())
            self.inventory_tree.column(col, anchor="center")
        self.inventory_tree.grid(row=2, column=0, sticky="nsew", pady=4)

        ttk.Label(self, text="Stock Summary").grid(row=3, column=0, sticky="w")
        self.summary_tree = ttk.Treeview(
            self,
            columns=("sku", "opening", "import", "export", "closing"),
            show="headings",
            height=8,
        )
        for col in ("sku", "opening", "import", "export", "closing"):
            self.summary_tree.heading(col, text=col.upper())
            self.summary_tree.column(col, anchor="center")
        self.summary_tree.grid(row=4, column=0, sticky="nsew", pady=4)

        self.update_language()

    def update_language(self) -> None:
        self.lbl_from.configure(text=self.tr.t("from_date"))
        self.lbl_to.configure(text=self.tr.t("to_date"))
        self.btn_load.configure(text=self.tr.t("load_report"))

    def refresh(self) -> None:
        for row in self.inventory_tree.get_children():
            self.inventory_tree.delete(row)
        for row in self.service.get_inventory():
            self.inventory_tree.insert(
                "", tk.END, values=(row["sku"], row["name"], row["unit"], row["quantity"])
            )
        self._load_summary()

    def _load_summary(self) -> None:
        try:
            rows = self.service.get_report(self.ent_from.get().strip(), self.ent_to.get().strip())
            for row in self.summary_tree.get_children():
                self.summary_tree.delete(row)
            for row in rows:
                self.summary_tree.insert(
                    "",
                    tk.END,
                    values=(
                        row["sku"],
                        row["opening"],
                        row["import"],
                        row["export"],
                        row["closing"],
                    ),
                )
        except Exception as err:  # noqa: BLE001
            self.show_error(err)


class SetupPage(BasePage):
    def __init__(self, parent: tk.Widget, service: WarehouseService, tr: Translator) -> None:
        super().__init__(parent, service, tr)

        self.columnconfigure(0, weight=1)
        file_frame = ttk.Frame(self)
        file_frame.grid(row=0, column=0, sticky="ew", pady=4)
        file_frame.columnconfigure(1, weight=1)

        self.lbl_file = ttk.Label(file_frame)
        self.lbl_file.grid(row=0, column=0, padx=4)
        self.ent_file = ttk.Entry(file_frame)
        self.ent_file.grid(row=0, column=1, sticky="ew", padx=4)
        self.btn_file = ttk.Button(file_frame, text="...", command=self._pick_file)
        self.btn_file.grid(row=0, column=2, padx=4)

        action_frame = ttk.Frame(self)
        action_frame.grid(row=1, column=0, sticky="ew", pady=4)
        self.btn_preview = ttk.Button(action_frame, command=self._preview)
        self.btn_preview.pack(side="left", padx=4)
        self.btn_import = ttk.Button(action_frame, command=self._import)
        self.btn_import.pack(side="left", padx=4)

        self.preview_text = tk.Text(self, height=12)
        self.preview_text.grid(row=2, column=0, sticky="nsew", pady=4)

        reset_frame = ttk.Frame(self)
        reset_frame.grid(row=3, column=0, sticky="ew", pady=4)
        self.lbl_reset = ttk.Label(reset_frame)
        self.lbl_reset.pack(side="left", padx=4)
        self.ent_reset = ttk.Entry(reset_frame)
        self.ent_reset.pack(side="left", padx=4)
        self.reset_mode = tk.StringVar(value="full")
        ttk.Combobox(
            reset_frame,
            textvariable=self.reset_mode,
            values=["full", "safe"],
            width=8,
            state="readonly",
        ).pack(side="left", padx=4)
        self.btn_reset = ttk.Button(reset_frame, command=self._reset)
        self.btn_reset.pack(side="left", padx=4)

        backup_frame = ttk.Frame(self)
        backup_frame.grid(row=4, column=0, sticky="ew", pady=4)
        backup_frame.columnconfigure(1, weight=1)
        self.lbl_dest = ttk.Label(backup_frame)
        self.lbl_dest.grid(row=0, column=0, padx=4)
        self.ent_dest = ttk.Entry(backup_frame)
        self.ent_dest.insert(0, str(get_default_backup_dir()))
        self.ent_dest.grid(row=0, column=1, sticky="ew", padx=4)
        ttk.Button(backup_frame, text="...", command=self._pick_dest).grid(row=0, column=2)
        self.btn_backup = ttk.Button(backup_frame, command=self._backup)
        self.btn_backup.grid(row=0, column=3, padx=4)
        self.btn_restore = ttk.Button(backup_frame, command=self._restore)
        self.btn_restore.grid(row=0, column=4, padx=4)

        self.update_language()

    def update_language(self) -> None:
        self.lbl_file.configure(text=self.tr.t("file"))
        self.btn_preview.configure(text=self.tr.t("preview"))
        self.btn_import.configure(text=self.tr.t("import_initial"))
        self.lbl_reset.configure(text=self.tr.t("confirm_reset"))
        self.btn_reset.configure(text=self.tr.t("reset_db"))
        self.lbl_dest.configure(text=self.tr.t("destination"))
        self.btn_backup.configure(text=self.tr.t("backup"))
        self.btn_restore.configure(text=self.tr.t("restore"))

    def _pick_file(self) -> None:
        path = filedialog.askopenfilename(filetypes=[("Excel/CSV", "*.xlsx *.xlsm *.csv")])
        if path:
            self.ent_file.delete(0, tk.END)
            self.ent_file.insert(0, path)

    def _pick_dest(self) -> None:
        path = filedialog.askdirectory()
        if path:
            self.ent_dest.delete(0, tk.END)
            self.ent_dest.insert(0, path)

    def _preview(self) -> None:
        try:
            rows = self.service.import_initial_stock_from_excel(self.ent_file.get().strip(), preview_only=True)
            self.preview_text.delete("1.0", tk.END)
            self.preview_text.insert("1.0", "\n".join(str(row) for row in rows))
        except Exception as err:  # noqa: BLE001
            self.show_error(err)

    def _import(self) -> None:
        try:
            rows = self.service.import_initial_stock_from_excel(self.ent_file.get().strip(), preview_only=False)
            self.show_info(f"Imported {len(rows)} rows")
        except Exception as err:  # noqa: BLE001
            self.show_error(err)

    def _reset(self) -> None:
        try:
            self.service.reset_database(mode=self.reset_mode.get(), confirm_token=self.ent_reset.get().strip())
            self.show_info("Database reset completed")
        except Exception as err:  # noqa: BLE001
            self.show_error(err)

    def _backup(self) -> None:
        try:
            output = self.service.backup_db(self.ent_dest.get().strip())
            self.show_info(f"Backup created: {output}")
        except Exception as err:  # noqa: BLE001
            self.show_error(err)

    def _restore(self) -> None:
        backup_file = filedialog.askopenfilename(filetypes=[("SQLite", "*.db")])
        if not backup_file:
            return
        try:
            self.service.restore_db(backup_file)
            self.show_info("Restore completed. Restart app recommended.")
        except Exception as err:  # noqa: BLE001
            self.show_error(err)
