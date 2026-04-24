# 📚 Project Analysis - Business Logic & Class Architecture

## 🏗️ Tổng quan hệ thống

**Tên:**管理系统 Kho Lưu Trữ Hàng Hóa  
**Ngôn ngữ:** Python 3.10+  
**Framework UI:** PyQt6  
**Database:** SQLite  
**ORM:** SQLAlchemy  

---

## 📦 Cấu trúc thư mục

```
src/
├── __init__.py
├── main_window.py      # Main window class
├── app.py              # Application entry point
│
├── models/             # Database models (ORM layer)
│   ├── base.py         # Base class with common columns
│   ├── khach_hang.py   # Customer model
│   ├── kho.py          # Warehouse model
│   ├── vi_tri.py       # Storage location model
│   ├── hop_dong.py     # Contract model
│   ├── hang_hoa.py     # Goods model
│   ├── thanh_toan.py   # Payment model
│   ├── nhan_vien.py    # Employee model
│   ├── system_log.py   # System log model
│   └── bao_cao.py      # Report model
│
├── services/           # Business logic layer
│   ├── khach_hang_service.py
│   ├── kho_service.py
│   ├── vi_tri_service.py
│   ├── hop_dong_service.py
│   ├── hang_hoa_service.py
│   ├── thanh_toan_service.py
│   ├── nhan_vien_service.py
│   └── report_service.py
│
├── gui/                # GUI layer
│   ├── views/          # View classes (screens)
│   │   ├── khach_hang_view.py
│   │   ├── kho_view.py
│   │   ├── vi_tri_view.py
│   │   ├── hop_dong_view.py
│   │   ├── hang_hoa_view.py
│   │   └── dashboard_view.py
│   │
│   ├── forms/          # Dialog forms for CRUD
│   │   ├── khach_hang_form.py
│   │   ├── kho_form.py
│   │   ├── vi_tri_form.py
│   │   ├── hop_dong_form.py
│   │   ├── hang_hoa_form.py
│   │   └── ...
│   │
│   ├── widgets/        # Reusable UI components
│   │   ├── data_table.py       # DataTableWithToolbar
│   │   ├── buttons.py
│   │   ├── search_box.py
│   │   └── loading.py
│   │
│   ├── dialogs/        # Dialog windows
│   │   └── dialogs.py          # MessageDialog, ConfirmDialog
│   │
│   └── navigation.py   # Navigation logic
│
└── utils/              # Utility functions
    ├── validators.py       # Input validation
    ├── formatters.py       # Data formatting
    ├── helpers.py          # Helper functions
    └── export_service.py   # Excel export service
```

---

## 🗄️ Database Models

### 1. **KhachHang** (Customer)

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| ma_khach_hang | VARCHAR(20) | PRIMARY KEY | Customer ID |
| ho_ten | VARCHAR(200) | NOT NULL | Full name |
| loai_khach | ENUM | NOT NULL | CA_NHAN / DOANH_NGHIEP |
| so_dien_thoai | VARCHAR(20) | NOT NULL | Phone |
| email | VARCHAR(100) | UNIQUE | Email |
| dia_chi | VARCHAR(500) | NOT NULL | Address |
| ma_so_thue | VARCHAR(20) | | Tax code |
| ngay_dang_ky | DATE | NOT NULL | Registration date |
| trang_thai | ENUM | NOT NULL | HOAT_DONG / TAM_KHOA / DA_XOA |
| ngay_tao | DATETIME | DEFAULT CURRENT_TIMESTAMP | Created |
| ngay_cap_nhat | DATETIME | | Updated |

**Relationships:**
- `khach_hangs (1) ↔ (N) hop_dongs`

---

### 2. **Kho** (Warehouse)

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| ma_kho | VARCHAR(20) | PRIMARY KEY | Warehouse ID |
| ten_kho | VARCHAR(200) | NOT NULL | Warehouse name |
| dia_chi | TEXT | NOT NULL | Address |
| dien_tich | DECIMAL | NOT NULL | Area (m²) |
| suc_chua | DECIMAL | NOT NULL | Capacity |
| da_su_dung | DECIMAL | NOT NULL | Used capacity |
| trang_thai | ENUM | NOT NULL | HOAT_DONG / BAO_TRI / NGUNG |
| ngay_tao | DATETIME | DEFAULT CURRENT_TIMESTAMP | Created |
| ngay_cap_nhat | DATETIME | | Updated |

**Relationships:**
- `kho (1) ↔ (N) vi_tri`

---

### 3. **ViTri** (Storage Location)

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| ma_vi_tri | VARCHAR(30) | PRIMARY KEY | Location ID |
| ma_kho | VARCHAR(20) | FK, NOT NULL | Warehouse ID |
| khu_vuc | VARCHAR(50) | NOT NULL | Zone |
| hang | VARCHAR(10) | NOT NULL | Row |
| tang | INTEGER | NOT NULL | Floor |
| dien_tich | DECIMAL | NOT NULL | Area |
| gia_thue | DECIMAL | NOT NULL | Rental price |
| suc_chua | DECIMAL | | Capacity |
| trang_thai | ENUM | NOT NULL | TRONG / DA_THUE / BAO_TRI |
| ngay_tao | DATETIME | DEFAULT CURRENT_TIMESTAMP | Created |
| ngay_cap_nhat | DATETIME | | Updated |

**Relationships:**
- `vi_tri (N) ↔ (1) hop_dong`

---

### 4. **HopDong** (Contract)

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| ma_hop_dong | VARCHAR(20) | PRIMARY KEY | Contract ID |
| ma_khach_hang | VARCHAR(20) | FK, NOT NULL | Customer ID |
| ma_vi_tri | VARCHAR(30) | FK, NOT NULL | Location ID |
| ngay_bat_dau | DATE | NOT NULL | Start date |
| ngay_ket_thuc | DATE | NOT NULL | End date |
| gia_thue | DECIMAL | NOT NULL | Rental price |
| tien_coc | DECIMAL | NOT NULL | Deposit |
| phuong_thuc_thanh_toan | VARCHAR(20) | | THANH_TOAN / HANG_THANG / HANG_QUY... |
| dieu_khoan | TEXT | | Terms |
| trang_thai | ENUM | NOT NULL | HIEN_LUC / HET_HAN / CHAM_DUT / GIA_HAN |
| ly_do_cham_dut | TEXT | | Reason |
| ngay_cham_dut | DATE | | Termination date |
| ngay_tao | DATETIME | DEFAULT CURRENT_TIMESTAMP | Created |
| ngay_cap_nhat | DATETIME | | Updated |

**Relationships:**
- `hop_dong (1) ↔ (N) hang_hoa`
- `hop_dong (1) ↔ (N) thanh_toan`

---

### 5. **HangHoa** (Goods)

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| ma_hang_hoa | VARCHAR(30) | PRIMARY KEY | Goods ID |
| ma_hop_dong | VARCHAR(20) | FK, NOT NULL | Contract ID |
| ten_hang | VARCHAR(200) | NOT NULL | Goods name |
| loai_hang | VARCHAR(100) | NOT NULL | Category |
| so_luong | INTEGER | NOT NULL | Quantity |
| don_vi | VARCHAR(20) | NOT NULL | Unit |
| trong_luong | DECIMAL | | Weight |
| kich_thuoc | VARCHAR(50) | | Dimensions |
| gia_tri | DECIMAL | | Value |
| ngay_nhap | DATETIME | DEFAULT CURRENT_TIMESTAMP | Entry date |
| ngay_xuat | DATETIME | | Exit date |
| trang_thai | ENUM | NOT NULL | TRONG_KHO / DA_XUAT / HU_HONG |
| vi_tri_luu_tru | VARCHAR(30) | | Storage location |
| ghi_chu | TEXT | | Note |
| hinh_anh | TEXT | | Image path |
| ngay_tao | DATETIME | DEFAULT CURRENT_TIMESTAMP | Created |
| ngay_cap_nhat | DATETIME | | Updated |

**Relationships:**
- `hang_hoa (N) ↔ (1) hop_dong`

---

### 6. **ThanhToan** (Payment)

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| ma_thanh_toan | VARCHAR(20) | PRIMARY KEY | Payment ID |
| ma_hop_dong | VARCHAR(20) | FK, NOT NULL | Contract ID |
| ngay_thanh_toan | DATE | NOT NULL | Payment date |
| so_tien | DECIMAL | NOT NULL | Amount |
| phuong_thuc | VARCHAR(20) | | Payment method |
| ghi_chu | TEXT | | Note |
| trang_thai | VARCHAR(20) | NOT NULL | DA_THANH_TOAN / CHO_THANH_TOAN |
| ngay_tao | DATETIME | DEFAULT CURRENT_TIMESTAMP | Created |
| ngay_cap_nhat | DATETIME | | Updated |

**Relationships:**
- `thanh_toan (N) ↔ (1) hop_dong`

---

### 7. **NhanVien** (Employee)

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| ma_nhan_vien | VARCHAR(20) | PRIMARY KEY | Employee ID |
| ho_ten | VARCHAR(200) | NOT NULL | Full name |
| sdt | VARCHAR(20) | NOT NULL | Phone |
| email | VARCHAR(100) | UNIQUE | Email |
| chuc_vu | VARCHAR(50) | NOT NULL | Position |
| ngay_vao_lam | DATE | NOT NULL | Hire date |
| trang_thai | VARCHAR(20) | NOT NULL | HOAT_DONG / NGUNG_LAM |
| ngay_tao | DATETIME | DEFAULT CURRENT_TIMESTAMP | Created |
| ngay_cap_nhat | DATETIME | | Updated |

**Relationships:**
- `nhan_vien (1) ↔ (N) system_log`
- `nhan_vien (1) ↔ (N) bao_cao`

---

### 8. **SystemLog** (System Log)

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| ma_log | VARCHAR(20) | PRIMARY KEY | Log ID |
| ma_nhan_vien | VARCHAR(20) | FK, NOT NULL | Employee ID |
| action | VARCHAR(50) | NOT NULL | Action (CREATE/UPDATE/DELETE) |
| table_name | VARCHAR(50) | NOT NULL | Table name |
| record_id | VARCHAR(50) | | Record ID |
| old_value | TEXT | | Previous data |
| new_value | TEXT | | New data |
| ngay_thuc_hien | DATETIME | | Execution date |
| ngay_tao | DATETIME | DEFAULT CURRENT_TIMESTAMP | Created |

---

### 9. **BaoCao** (Report)

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| ma_bao_cao | VARCHAR(20) | PRIMARY KEY | Report ID |
| ma_nhan_vien | VARCHAR(20) | FK, NOT NULL | Employee ID |
| loai_bao_cao | VARCHAR(50) | NOT NULL | Report type |
| ngay_bat_dau | DATE | NOT NULL | Start date |
| ngay_ket_thuc | DATE | NOT NULL | End date |
| du_lieu | TEXT | | Data (JSON) |
| trang_thai | VARCHAR(20) | NOT NULL | DANG_LAM | DA_XONG |
| ngay_tao | DATETIME | DEFAULT CURRENT_TIMESTAMP | Created |

---

## 🔧 Business Logic Services

### **KhachHangService**

**Methods:**

| Method | Parameters | Return | Description |
|--------|------------|--------|-------------|
| `create(data)` | Dict | KhachHang | Create customer |
| `update(id, data)` | str, Dict | KhachHang | Update customer |
| `delete(id)` | str | bool | Soft delete customer |
| `get_by_id(id)` | str | Optional[KhachHang] | Get customer by ID |
| `search(keyword)` | str | List[KhachHang] | Search customers |
| `get_by_trang_thai(status)` | str | List[KhachHang] | Filter by status |
| `count_by_loai_khach()` | - | Dict[str, int] | Count by type |

**Business Rules:**
- Phone phải.unique
- Email must be unique
- Cannot delete customer with active contracts
- `ma_so_thue` required for DOANH_NGHIEP type

---

### **HopDongService**

**Methods:**

| Method | Parameters | Return | Description |
|--------|------------|--------|-------------|
| `create(data)` | Dict | HopDong | Create contract |
| `update(id, data)` | str, Dict | HopDong | Update contract |
| `delete(id)` | str | bool | Soft delete contract |
| `renew(id)` | str | HopDong | Renew contract |
| `terminate(id, ly_do)` | str, str | HopDong | Terminate contract |
| `get_by_khach_hang(ma_kh)` | str | List[HopDong] | Get contracts by customer |
| `get_by_trang_thai(status)` | str | List[HopDong] | Filter by status |
| `get_contracts_expiring_soon()` | - | List[HopDong] | Get contracts expiring in 30 days |

**Business Rules:**
- Contract start date < end date
- Location must be TRONG before contract creation
- Contract cannot be renewed if expired
- Contract can only be terminated if ACTIVE

---

### **KhoService**

**Methods:**

| Method | Parameters | Return | Description |
|--------|------------|--------|-------------|
| `create(data)` | Dict | Kho | Create warehouse |
| `update(id, data)` | str, Dict | Kho | Update warehouse |
| `delete(id)` | str | bool | Soft delete warehouse |
| `get_by_id(id)` | str | Optional[Kho] | Get warehouse by ID |
| `search(keyword)` | str | List[Kho] | Search warehouses |
| `get_by_trang_thai(status)` | str | List[Kho] | Filter by status |
| `get_available_capacity(ma_kho)` | str | float | Get available capacity |

---

### **ViTriService**

**Methods:**

| Method | Parameters | Return | Description |
|--------|------------|--------|-------------|
| `create(data)` | Dict | ViTri | Create location |
| `update(id, data)` | str, Dict | ViTri | Update location |
| `delete(id)` | str | bool | Soft delete location |
| `get_by_id(id)` | str | Optional[ViTri] | Get location by ID |
| `get_by_kho(ma_kho)` | str | List[ViTri] | Get locations by warehouse |
| `get_available_by_kho(ma_kho)` | str | List[ViTri] | Get available locations |
| `update_status(id, trang_thai)` | str, str | ViTri | Update location status |

---

### **HangHoaService**

**Methods:**

| Method | Parameters | Return | Description |
|--------|------------|--------|-------------|
| `create(data)` | Dict | HangHoa | Create goods |
| `update(id, data)` | str, Dict | HangHoa | Update goods |
| `delete(id)` | str | bool | Soft delete goods |
| `get_by_id(id)` | str | Optional[HangHoa] | Get goods by ID |
| `get_by_hop_dong(ma_hd)` | str | List[HangHoa] | Get goods by contract |
| `export_to_excel(output_path)` | str | bool | Export to Excel |

---

### **ThanhToanService**

**Methods:**

| Method | Parameters | Return | Description |
|--------|------------|--------|-------------|
| `create(data)` | Dict | ThanhToan | Create payment |
| `update(id, data)` | str, Dict | ThanhToan | Update payment |
| `get_by_hop_dong(ma_hd)` | str | List[ThanhToan] | Get payments by contract |
| `get_total_by_hop_dong(ma_hd)` | str | float | Get total paid |
| `get_unpaid_contracts()` | - | List[HopDong] | Get contracts with unpaid payments |

---

### **ReportService**

**Methods:**

| Method | Parameters | Return | Description |
|--------|------------|--------|-------------|
| `get_warehouse_summary(from_date, to_date)` | Date, Date | Dict | Summary of warehouse usage |
| `get_contract_summary(from_date, to_date)` | Date, Date | Dict | Summary of contracts |
| `get_payment_summary(from_date, to_date)` | Date, Date | Dict | Summary of payments |
| `generate_report(loai, from_date, to_date)` | str, Date, Date | Dict | Generate report data |
| `export_report(report_data, output_path)` | Dict, str | bool | Export report to Excel |

---

## 🎨 GUI Views

### **KhachHangView**

**Features:**
- Table with: ID, Name, Type, Phone, Email, Status
- Filter by: Type, Status
- Search by: Name, Phone, Email
- Buttons: Add, Edit, Delete, Export Excel
- Tables with pagination (20 items/page)

**Signals:**
- `khach_hang_selected(KhachHang)`
- `khach_hang_added(KhachHang)`
- `khach_hang_updated(KhachHang)`
- `khach_hang_deleted(str)`

---

### **HopDongView**

**Features:**
- Table with: Contract ID, Customer, Location, Start Date, End Date, Status
- Filter by: Customer, Location, Status
- Search by: Contract ID, Customer name
- Buttons: Add, Edit, Delete, Renew, Terminate, Export Excel
- Alert for contracts expiring in 30 days

**Special Features:**
- Renew contract (extend end date)
- Terminate contract (set status to CHAM_DUT)

---

### **DashboardView**

**Features:**
- Warehouse statistics (total, used, available)
- Contract statistics (total, active, expired)
- Payment statistics (total, pending)
- Charts (なければNone)

**Data Sources:**
- `KhoService.get_by_trang_thai()`
- `HopDongService.get_by_trang_thai()`
- `ThanhToanService.get_unpaid_contracts()`

---

## 🔐 Validation Logic

### **Validators (`src/utils/validators.py`)**

| Function | Purpose |
|----------|---------|
| `validate_email(email)` | Validate email format |
| `validate_phone(phone)` | Validate phone format (Vietnam) |
| `validate_required(value, field_name)` | Check required fields |
| `validate_date_range(start, end)` | Validate date range |
| `validate_contract_dates(start, end)` | Validate contract dates |

### **Form Validators**

Each form has `validate()` method:
1. Check required fields
2. Validate email format
3. Validate phone format
4. Check for duplicates

---

## 📤 Export Service

### **Export to Excel**

**File:** `src/utils/export_service.py`

**Functions:**

| Function | Description |
|----------|-------------|
| `export_to_excel(data, columns, output_path)` | Export list of dicts to Excel |
| `export_khach_hang(data, output_path)` | Export customers to Excel |
| `export_hop_dong(data, output_path)` | Export contracts to Excel |
| `export_hang_hoa(data, output_path)` | Export goods to Excel |

**Format:**
- .xlsx extension
- Header row with column names
- Auto-fitting columns

---

## 🔄 Workflow Overview

### **Create Customer Flow**

```
User clicks "Add" button
    ↓
KhachHangView._on_add_clicked()
    ↓
KhachHangForm.show() (modal dialog)
    ↓
User fills form and clicks "Save"
    ↓
KhachHangForm.validate()
    ↓
KhachHangForm._on_save()
    ↓
KhachHangService.create(form_data)
    ↓
Database insert
    ↓
Return KhachHang object
    ↓
KhachHangView.load_data() (refresh table)
```

### **Create Contract Flow**

```
User clicks "Add" button
    ↓
HopDongView._on_add_clicked()
    ↓
HopDongForm.show() (modal dialog)
    ↓
Form load: Available locations (TRANG state)
    ↓
User fills form and clicks "Save"
    ↓
HopDongService.create(form_data)
    ↓
Validate: Location must be TRANG
    ↓
Database insert
    ↓
Update location status to "DA_THUE"
    ↓
Return HopDong object
    ↓
HopDongView.load_data() (refresh table)
```

---

## 🏁 Summary

### **Architecture Pattern:**
- **MVC-like** (Model-View-Controller abstraction)
- **Service Layer** for business logic
- **DAO pattern** via SQLAlchemy ORM

### **Key Components:**
1. **Models** (9 tables)
2. **Services** (6+ services)
3. **Views** (5+ views)
4. **Forms** (5+ forms)
5. **Utils** (validators, formatters, helpers)

### **Database:**
- SQLite with 9 tables
- Foreign key relationships
- Enum types for status/lock fields

### **UI:**
- PyQt6-based
- Tabbed interface
- Modal dialogs for CRUD
- Data tables with filtering

---
