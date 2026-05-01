# Warehouse Management App – SPEC (for Codex)

---

## 1. PROJECT OVERVIEW

Build a desktop warehouse management application using:

* Python
* Tkinter (UI)
* SQLite (local database)

The app manages inventory for clothing/shoes (SKU includes size).

---

## 2. CORE PRINCIPLES

1. products.quantity MUST always equal sum of ledger
2. NEVER update stock directly without ledger
3. HOLD = EXPORT (temporary)
4. RETURN = IMPORT
5. SALE = final record only (no stock change)

---

## 3. DATABASE SCHEMA

### 3.1 products

```sql
CREATE TABLE products (
    sku TEXT PRIMARY KEY,
    name TEXT,
    unit TEXT,
    quantity INTEGER DEFAULT 0
);
```

---

### 3.2 ledger (source of truth)

```sql
CREATE TABLE ledger (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sku TEXT,
    change INTEGER,
    type TEXT,              -- IMPORT / EXPORT
    ref_type TEXT,          -- HOLD / RETURN / SALE / IMPORT
    ref_id INTEGER,
    created_at TEXT
);
```

---

### 3.3 hold_sessions

```sql
CREATE TABLE hold_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT UNIQUE,
    status TEXT,            -- OPEN / DONE
    created_at TEXT,
    note TEXT
);
```

---

### 3.4 hold_items

```sql
CREATE TABLE hold_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id INTEGER,
    sku TEXT,
    quantity INTEGER,
    status TEXT,            -- HOLD / RETURNED
    FOREIGN KEY(session_id) REFERENCES hold_sessions(id)
);
```

---

### 3.5 sales

```sql
CREATE TABLE sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT UNIQUE,
    hold_session_id INTEGER,
    created_at TEXT,
    note TEXT
);
```

---

### 3.6 sale_items

```sql
CREATE TABLE sale_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sale_id INTEGER,
    sku TEXT,
    quantity INTEGER,
    FOREIGN KEY(sale_id) REFERENCES sales(id)
);
```

---

## 4. BUSINESS LOGIC

---

### 4.1 IMPORT STOCK

INPUT:

* sku
* quantity

PROCESS:

* increase products.quantity
* insert ledger (IMPORT)

---

### 4.2 EXPORT DIRECT

PROCESS:

* decrease products.quantity
* insert ledger (EXPORT)
* create sales record

---

### 4.3 HOLD (TRY ITEMS)

INPUT:

* multiple SKUs

PROCESS:

1. create hold_session (OPEN)
2. insert hold_items (status = HOLD)
3. for each item:

   * decrease products.quantity
   * insert ledger:
     type = EXPORT
     ref_type = HOLD

---

### 4.4 FINALIZE HOLD

INPUT:

* selected RETURN quantities

PROCESS:

STEP 1: RETURN ITEMS

* update hold_items → RETURNED
* increase products.quantity
* insert ledger:
  type = IMPORT
  ref_type = RETURN

STEP 2: CALCULATE SOLD

* sold = hold - return

STEP 3: CREATE SALE

* insert sales
* insert sale_items

STEP 4:

* update hold_session → DONE

IMPORTANT:

* NO ledger entry for SALE

---

## 5. UI REQUIREMENTS (Tkinter)

---

### 5.1 Main layout

* Sidebar menu
* Content area

---

### 5.2 Screens

#### Products

* Table (Treeview)
* Add/Edit product

---

#### Import

* Select SKU
* Input quantity
* Save

---

#### Export

* Same as import but subtract

---

#### HOLD

* Select multiple items
* Create HOLD

---

#### HOLD Management

* Search HOLD by code
* Open session
* Select RETURN quantities
* Finalize

---

#### Sales

* View sales history

---

#### Reports

* Inventory list
* Import/Export report
* Stock summary

---

#### Backup

* Backup DB file
* Restore DB file

---

## 6. REPORT REQUIREMENTS

---

### 6.1 Inventory

Columns:

* STT
* SKU
* Name
* Unit
* Quantity

---

### 6.2 Stock Summary (date range)

For each SKU:

* Opening
* Import
* Export
* Closing

---

## 7. SERVICE FUNCTIONS

```python
create_product()
import_stock()
export_stock()
create_hold()
finalize_hold()
get_inventory()
get_sales()
get_report()
backup_db()
restore_db()
```

---

## 8. VALIDATION RULES

* Cannot export if stock < quantity
* HOLD cannot be edited after creation
* All stock changes must go through ledger
* Data must remain consistent

---

## 9. TEST CASES

1. HOLD then RETURN all → stock unchanged
2. HOLD then partial RETURN → correct stock
3. EXPORT → stock decreases
4. IMPORT → stock increases
5. Reports match ledger

---

## 10. OUTPUT EXPECTATION

Generate:

* Full Python project
* Tkinter UI
* SQLite integration
* Modular structure:

  * database/
  * services/
  * ui/

Code must be:

* clean
* readable
* modular
* runnable

---

## 11. INITIAL STOCK IMPORT (EXCEL)

---

### 11.1 PURPOSE

Allow user to import initial inventory from Excel file.

This is ONLY allowed when:

* products table is empty
  OR
* all products.quantity = 0

---

### 11.2 EXCEL FORMAT (REQUIRED)

Columns:

* STT (ignored)
* MÃ HÀNG → sku
* TÊN HÀNG HÓA → name
* ĐVT → unit
* TỒN → quantity

Example:

| SKU  | NAME             | UNIT | QUANTITY |
| ---- | ---------------- | ---- | -------- |
| DP.S | Đồng phục size S | Bộ   | 66       |

---

### 11.3 VALIDATION RULES

Before import:

1. Check database state:

```sql
SELECT COUNT(*) FROM products WHERE quantity > 0
```

IF result > 0:
→ BLOCK import
→ show error: "Database must be empty or reset before import"

---

2. Validate Excel:

* sku must not be empty
* quantity must be >= 0
* no duplicate sku

---

### 11.4 IMPORT PROCESS

For each row:

1. Insert into products:

```sql
INSERT INTO products (sku, name, unit, quantity)
VALUES (?, ?, ?, ?)
```

---

2. Insert into ledger:

```sql
change = +quantity
type = IMPORT
ref_type = INIT
```

---

### 11.5 RESULT

After import:

* products.quantity is initialized
* ledger fully reflects initial stock
* system ready for operations

---

## 12. RESET FUNCTION (IMPORTANT)

---

### 12.1 PURPOSE

Allow user to reset entire system to initial state.

Used before re-importing initial stock.

---

### 12.2 RESET OPTIONS

---

#### OPTION A: FULL RESET (recommended)

Delete all data:

```sql
DELETE FROM products;
DELETE FROM ledger;
DELETE FROM hold_items;
DELETE FROM hold_sessions;
DELETE FROM sales;
DELETE FROM sale_items;
```

---

#### OPTION B: SAFE RESET (alternative)

Keep products but reset quantity:

```sql
UPDATE products SET quantity = 0;
DELETE FROM ledger;
DELETE FROM hold_items;
DELETE FROM hold_sessions;
DELETE FROM sales;
DELETE FROM sale_items;
```

---

### 12.3 UI REQUIREMENT

* Button: "Reset Database"
* Confirmation dialog:
  "This will delete ALL data. Continue?"

---

### 12.4 SAFETY RULE

* Require confirmation (YES / NO)
* Optional: require typing "RESET"

---

## 13. SERVICE FUNCTIONS (UPDATED)

```python
import_initial_stock_from_excel(file_path)

validate_initial_import()

reset_database(mode="full")  # or "safe"
```

---

## 14. UI ADDITION

---

### New menu: "Setup"

Includes:

* Import Initial Stock
* Reset Database

---

### Import screen:

* Button: Select Excel file
* Button: Import
* Show preview before confirm

---

### Reset screen:

* Button: Reset
* Confirmation dialog

---

## 15. TEST CASES (ADDED)

1. Import when DB empty → success
2. Import when stock exists → blocked
3. Reset → DB cleared
4. Import after reset → success
5. Ledger reflects initial stock correctly

---

---

## 16. IMPORTANT NOTES & BEST PRACTICES

---

### 16.1 DATA CONSISTENCY (CRITICAL)

* `products.quantity` MUST always equal:

```
SUM(ledger.change)
```

* NEVER update `products.quantity` directly without inserting into `ledger`

* If inconsistency is detected:

  * system should log warning
  * optional: provide "Recalculate Stock" function

---

### 16.2 LEDGER IS SOURCE OF TRUTH

* All stock movements MUST go through `ledger`

* Types:

  * IMPORT
  * EXPORT

* ref_type examples:

  * INIT
  * IMPORT
  * EXPORT
  * HOLD
  * RETURN

* Reports MUST be generated from `ledger`, not from `products`

---

### 16.3 HOLD RULES

* HOLD is a temporary export

* HOLD MUST:

  * reduce stock immediately
  * create ledger entry (EXPORT)

* HOLD sessions:

  * cannot be edited after creation
  * must be finalized (DONE)

* HOLD items:

  * only statuses: HOLD, RETURNED

---

### 16.4 RETURN RULES

* RETURN MUST:

  * increase stock
  * create ledger entry (IMPORT)

* RETURN is only allowed within a HOLD session

---

### 16.5 SALE RULES

* SALE represents final sold items

* SALE:

  * DOES NOT affect stock directly
  * is derived from HOLD - RETURN

* Every HOLD session when finalized MUST create a SALE record

---

### 16.6 NO DIRECT DATA EDIT

* Do NOT allow:

  * manual editing of stock quantity
  * deleting ledger records
  * editing past transactions

* If needed:

  * create adjustment transaction instead

---

### 16.7 EXCEL IMPORT SAFETY

* Only allow initial import when:

  * database is empty OR
  * all stock = 0

* Prevent:

  * duplicate import
  * invalid data types

* Always validate before inserting

---

### 16.8 RESET SAFETY

* Reset must:

  * clear ledger
  * clear HOLD data
  * clear SALES data

* Require:

  * user confirmation
  * optional password or keyword

---

### 16.9 ERROR HANDLING

* All DB operations should:

  * use transactions (BEGIN / COMMIT / ROLLBACK)

* If any step fails:

  * rollback entire operation

Example:

```
BEGIN;
-- insert ledger
-- update product
COMMIT;
```

---

### 16.10 PERFORMANCE

* Create indexes:

```sql
CREATE INDEX idx_ledger_sku ON ledger(sku);
CREATE INDEX idx_ledger_date ON ledger(created_at);
CREATE INDEX idx_hold_session ON hold_items(session_id);
```

* Avoid full table scans for reports

---

### 16.11 SCALABILITY

* Even though current system:

  * 1 user
  * 1 warehouse

Design should allow:

* multiple users
* user tracking (created_by)
* future permissions

---

### 16.12 AUDIT & DEBUGGING

* Never delete historical data

* Use ledger + sales + hold to trace issues

* To debug stock mismatch:

  1. check ledger
  2. recalculate stock
  3. compare with products table

---

### 16.13 UI/UX NOTES

* Always show:

  * current stock when selecting SKU

* Prevent:

  * exporting more than available stock

* For HOLD:

  * show remaining quantities clearly

---

### 16.14 BACKUP BEST PRACTICE

* Backup should:

  * copy SQLite file
  * include timestamp

* Restore should:

  * replace DB file
  * reload app

---

### 16.15 CODE QUALITY REQUIREMENTS

* Use modular structure:

  * database/
  * services/
  * ui/

* Separate:

  * business logic
  * UI logic
  * DB access

* Avoid:

  * writing SQL directly inside UI code

---

## 17. STOCK AUDIT (INVENTORY RECONCILIATION)

---

### 17.1 PURPOSE

Allow user to perform stock audit by comparing actual inventory with system inventory.

---

### 17.2 INPUT METHODS

#### Method 1: Excel Import

* Same format as initial stock import

#### Method 2: Manual Input (UI)

* User enters:

  * SKU
  * Actual quantity

---

### 17.3 DATABASE TABLES

#### stock_audit_sessions

```sql
CREATE TABLE stock_audit_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT UNIQUE,
    created_at TEXT,
    note TEXT
);
```

---

#### stock_audit_items

```sql
CREATE TABLE stock_audit_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id INTEGER,
    sku TEXT,
    system_qty INTEGER,
    actual_qty INTEGER,
    diff INTEGER,
    FOREIGN KEY(session_id) REFERENCES stock_audit_sessions(id)
);
```

---

### 17.4 PROCESS

STEP 1: Create audit session

STEP 2: Load data (Excel or UI)

STEP 3: For each SKU:

```text
diff = actual_qty - system_qty
```

STEP 4: Show preview table:

* SKU
* System quantity
* Actual quantity
* Difference

---

### 17.5 CONFIRMATION

User must confirm before applying changes.

---

### 17.6 APPLY CHANGES

For each item:

IF diff > 0:

* Increase stock
* Insert ledger:

  * type = IMPORT
  * ref_type = ADJUSTMENT

IF diff < 0:

* Decrease stock
* Insert ledger:

  * type = EXPORT
  * ref_type = ADJUSTMENT

---

### 17.7 FINAL RESULT

* products.quantity updated
* ledger reflects adjustment
* audit session stored for tracking

---

### 17.8 RULES

* Must NOT overwrite stock directly
* Must go through ledger
* Must allow preview before confirm

---

### 17.9 UI REQUIREMENTS

* Screen: "Stock Audit"

* Options:

  * Import Excel
  * Manual input

* Show comparison table before applying

* Button:

  * "Apply Adjustment"

---

### 17.10 TEST CASES

1. Actual > system → stock increases
2. Actual < system → stock decreases
3. No difference → no ledger entry
4. Audit session saved correctly

---

## 18. INVENTORY SNAPSHOT (OPTIONAL BUT RECOMMENDED)

---

### 18.1 PURPOSE

Store inventory state at a specific point in time for:

* auditing
* comparison
* historical reference

---

### 18.2 WHEN TO CREATE SNAPSHOT

Snapshots SHOULD be created:

* after stock audit
* before database reset
* optionally at end of day/month

Snapshots SHOULD NOT be created automatically for every report.

---

### 18.3 DATABASE TABLES

#### inventory_snapshots

```sql id="i9r8vb"
CREATE TABLE inventory_snapshots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT,
    created_at TEXT,
    note TEXT
);
```

---

#### snapshot_items

```sql id="3vbbns"
CREATE TABLE snapshot_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    snapshot_id INTEGER,
    sku TEXT,
    quantity INTEGER,
    FOREIGN KEY(snapshot_id) REFERENCES inventory_snapshots(id)
);
```

---

### 18.4 PROCESS

To create snapshot:

1. Insert snapshot record
2. Copy current inventory:

```sql id="ksc8zq"
INSERT INTO snapshot_items (snapshot_id, sku, quantity)
SELECT ?, sku, quantity FROM products;
```

---

### 18.5 RULES

* Snapshot is read-only
* Snapshot must not affect stock
* Snapshot is for reference only

---

### 18.6 USE CASES

* Compare stock before/after audit
* Recover historical data
* Debug inconsistencies

---

## 19. SNAPSHOT COMPARISON

---

### 19.1 PURPOSE

Compare inventory between two snapshots.

---

### 19.2 INPUT

* Snapshot A (older)
* Snapshot B (newer)

---

### 19.3 OUTPUT

Table:

* SKU
* Quantity in Snapshot A
* Quantity in Snapshot B
* Difference (B - A)

---

### 19.4 QUERY (SQLite)

```sql
SELECT 
    s.sku,
    COALESCE(a.quantity, 0) AS qty_a,
    COALESCE(b.quantity, 0) AS qty_b,
    COALESCE(b.quantity, 0) - COALESCE(a.quantity, 0) AS diff
FROM (
    SELECT sku FROM snapshot_items WHERE snapshot_id = ?
    UNION
    SELECT sku FROM snapshot_items WHERE snapshot_id = ?
) s
LEFT JOIN snapshot_items a 
    ON s.sku = a.sku AND a.snapshot_id = ?
LEFT JOIN snapshot_items b 
    ON s.sku = b.sku AND b.snapshot_id = ?
ORDER BY s.sku;
```

---

### 19.5 UI REQUIREMENTS

* Dropdown to select Snapshot A
* Dropdown to select Snapshot B
* Display comparison table

---

### 19.6 FEATURES

* Highlight differences:

  * positive → green
  * negative → red

* Filter:

  * show only changed items

* Sorting:

  * by difference

* Export to Excel

---

### 19.7 RULES

* Snapshots are read-only
* Comparison does not modify data

---

### 19.8 TEST CASES

1. Same snapshots → all diff = 0
2. New stock added → positive diff
3. Stock removed → negative diff
4. SKU exists in only one snapshot

---
