# CẤU TRÚC THƯ MỤC SRC/

## Tổng quan kiến trúc

Project sử dụng **3-Layer Architecture (Presentation - Business - Data)**:

```
src/
├── models/          # Data Layer - SQLAlchemy ORM models
├── services/        # Business Layer - Logic xử lý nghiệp vụ
├── gui/             # Presentation Layer - Giao diện PyQt6
├── database/        # Data Layer - Kết nối database
├── utils/          # Utility Layer - Hàm helper, validators
├── data/           # Database files
├── templates/       # Template files (PDF)
├── main.py         # Entry point
├── app.py          # Application class
└── main_window.py  # Main window
```

---

## 1. THƯ MỤC GỐC `src/`

### 1.1 `src/models/` - Data Layer - Database Models

**Mục đích:** Định nghĩa các SQLAlchemy ORM (cơ chế Object-Relational Mapping- Cho phép bạn tương tác với cơ sở dữ liệu quan hệ bằng cách sử dụng các lớp và đối tượng Python thay vì viết các câu lệnh SQL trực tiếp) models tương ứng với các bảng trong database.

**Nhiệm vụ:** 
- Khai báo cấu trúc bảng (columns, relationships)
- Định nghĩa các ràng buộc (constraints)
- Kế thừa từ `BaseModel` để có các methods chung

**Các file tiêu biểu:**

#### `src/models/base.py`
- **Mục đích:** Định nghĩa `BaseModel` - class cơ sở cho tất cả models
- **Cách dùng:** Tất cả models kế thừa từ `BaseModel` để có:
  - `ngay_tao`, `ngay_cap_nhat` - tự động theo dõi thời gian
  - `to_dict()` - chuyển model thành dictionary
  - `to_json()` - chuyển model thành JSON string

```python
class BaseModel(Base):
    __abstract__ = True
    ngay_tao = Column(DateTime, nullable=False, default=datetime.now)
    ngay_cap_nhat = Column(DateTime, onupdate=datetime.now)
```

#### `src/models/khach_hang.py`
- **Mục đích:** Model cho bảng `khach_hang` (Khách hàng thuê kho)
- **Cách dùng:**
```python
from src.models import KhachHang

kh = KhachHang(ma_khach_hang="KH20250603001", ho_ten="Nguyễn Văn A")
```

#### `src/models/enums.py`
- **Mục đích:** Định nghĩa các enumerations (một kiểu dữ liệu đặc biệt trong lập trình, cho phép bạn định nghĩa một tập hợp các hằng số có tên (named constants). Mỗi giá trị trong enum đại diện cho một trạng thái hoặc lựa chọn cụ thể) dùng chung
- **Ví dụ:** `LoaiKhachEnum`, `TrangThaiKHEnum`, `TrangThaiKhoEnum`

---

### 1.2 `src/services/` - Business Layer - Service Classes

**Mục đích:** Chứa logic nghiệp vụ, làm việc giữa GUI và Database.

**Nhiệm vụ:**
- Thực hiện CRUD operations
- Validation nghiệp vụ
- Xử lý transaction
- Business logic đặc thù

**Các file tiêu biểu:**

#### `src/services/base_service.py`
- **Mục đích:** Class cơ sở cho tất cả services
- **Cách dùng:** Các service kế thừa `BaseService` để có:
  - Quản lý session tự động
  - Hỗ trợ transaction context manager
  - Property `session` để truy cập database

```python
class KhachHangService(BaseService[KhachHang]):
    def get_by_id(self, ma_khach_hang: str) -> Optional[KhachHang]:
        return self.session.query(KhachHang).filter(...).first()
```

#### `src/services/khach_hang_service.py`
- **Mục đích:** Xử lý nghiệp vụ liên quan đến Khách hàng
- **Cách dùng:**
```python
service = KhachHangService()
khach_hang = service.create({
    'ho_ten': 'Nguyễn Văn A',
    'loai_khach': LoaiKhachEnum.CA_NHAN,
    'so_dien_thoai': '0901234567',
    'dia_chi': '123 Đường ABC'
})
```

#### `src/services/auth/` - Authentication Services
- **`auth_service.py`**: Xử lý đăng nhập, đăng xuất
- **`auth_middleware.py`**: Middleware kiểm tra quyền
- **`authorization_service.py`**: Quản lý phân quyền

#### `src/services/pdf/`
- **`pdf_generation_service.py`**: Tạo báo cáo PDF

---

### 1.3 `src/gui/` - Presentation Layer - Giao diện PyQt6

**Mục đích:** Chứa tất cả UI components của ứng dụng.

**Nhiệm vụ:**
- Hiển thị dữ liệu cho người dùng
- Thu thập input từ người dùng
- Xử lý events và signals

**Cấu trúc con:**
```
src/gui/
├── views/       # Main view widgets
├── forms/       # Form dialogs
├── widgets/     # Reusable widgets
├── dialogs/     # Reusable dialogs (MessageDialog, etc.)
├── wizards/     # Wizard dialogs (Renewal, Termination)
├── styles/      # QSS stylesheets
└── navigation.py # Navigation system
```

#### `src/gui/views/` - Main Views

**Mục đích:** Các màn hình chính của ứng dụng.

**File tiêu biểu:**

##### `src/gui/views/dashboard_view.py`
- **Mục đích:** Dashboard tổng quan với thống kê kho
- **Cách dùng:** Được load khi khởi động app, hiển thị:
  - Thẻ metrics (tổng kho, kho hoạt động, vị trí...)
  - Biểu đồ trạng thái kho (pie chart)
  - Biểu đồ tỷ lệ lấp đầy (bar chart)
  - Cảnh báo kho quá tải
- **Cách hoạt động:** Tự động refresh mỗi 30 giây

##### `src/gui/views/khach_hang_view.py`
- **Mục đích:** View quản lý khách hàng (danh sách, thêm, sửa, xóa)

##### `src/gui/views/hop_dong_view.py`
- **Mục đích:** View quản lý hợp đồng thuê kho

##### `src/gui/views/kho_view.py`
- **Mục đích:** View quản lý kho hàng

##### `src/gui/views/bao_cao_view.py`
- **Mục đích:** View hiển thị báo cáo thống kê

---

#### `src/gui/forms/` - Form Dialogs

**Mục đích:** Dialog forms để nhập liệu (thêm/sửa).

**File tiêu biểu:**

##### `src/gui/forms/khach_hang_form.py`
- **Mục đích:** Form nhập liệu thông tin khách hàng
- **Cách dùng:**
```python
from src.gui.forms import show_khach_hang_form

accepted, data = show_khach_hang_form(parent, khach_hang=None)  # Thêm mới
accepted, data = show_khach_hang_form(parent, khach_hang=existing_kh)  # Sửa
if accepted:
    print(data)  # {'ho_ten': '...', 'loai_khach': ..., ...}
```

##### `src/gui/forms/hop_dong_form.py`, `kho_form.py`, `thanh_toan_form.py`
- Tương tự, các form cho các module khác

---

#### `src/gui/widgets/` - Reusable Widgets

**Mục đích:** Các widgets dùng chung, có thể tái sử dụng.

**File tiêu biểu:**

##### `src/gui/widgets/data_table.py`
- **Mục đích:** Enhanced QTableWidget với features:
  - Sorting (click header để sort)
  - Searching/Filtering
  - Pagination
  - Row selection
  - Context menu
  - Export support
- **Cách dùng:**
```python
self.table = DataTable()
self.table.set_data(data_list, headers)
self.table.row_selected.connect(self._on_row_selected)
self.table.row_double_clicked.connect(self._on_row_double_clicked)
```

##### `src/gui/widgets/charts.py`
- **Mục đích:** Custom chart widgets (PieChartCanvas, FillRateBarChart)
- **Cách dùng:** Sử dụng matplotlib để vẽ biểu đồ

##### `src/gui/widgets/buttons.py`
- **Mục đích:** Custom button widgets đồng bộ style

##### `src/gui/widgets/search_box.py`
- **Mục đích:** Search box widget với debounce

##### `src/gui/widgets/loading.py`
- **Mục đích:** Loading spinner overlay widget

---

#### `src/gui/dialogs/` - Dialogs

**Mục đích:** Các dialog dùng chung (Message, Confirmation...).

##### `src/gui/dialogs/dialogs.py`
- **Mục đích:** Chứa `MessageDialog` class với các helper methods:
  - `MessageDialog.info(parent, title, message)`
  - `MessageDialog.error(parent, title, message)`
  - `MessageDialog.warning(parent, title, message)`
  - `MessageDialog.confirm(parent, title, message)`

---

#### `src/gui/wizards/` - Wizard Dialogs

**Mục đích:** Multi-step wizard dialogs cho các nghiệp vụ phức tạp.

##### `src/gui/wizards/renewal_wizard.py`
- **Mục đích:** Wizard gia hạn hợp đồng (multi-step)

##### `src/gui/wizards/termination_wizard.py`
- **Mục đích:** Wizard chấm dứt hợp đồng

---

#### `src/gui/navigation.py` - Navigation System

**Mục đích:** Quản lý navigation giữa các views.

**Cách hoạt động:**
- `NavigationPanel` chứa sidebar + stacked widget
- `NavigationManager` theo dõi view hiện tại
- Signals: `view_changed` khi chuyển view

---

### 1.4 `src/database/` - Data Layer - Database Connection

**Mục đích:** Quản lý kết nối đến SQLite database.

**File tiêu biểu:**

#### `src/database/connection.py`
- **Mục đích:** Singleton pattern để quản lý database connection
- **Cách dùng:**
```python
from src.database import get_session, session_scope

# Cách 1: Direct session
session = get_session()
results = session.query(KhachHang).all()
session.close()

# Cách 2: Context manager (recommended)
with session_scope() as session:
    session.add(new_khach_hang)
    # auto-commit on success, auto-rollback on error
```
- **Đặc điểm:**
  - Singleton `DatabaseConnection` - chỉ có 1 engine instance
  - SQLite với `check_same_thread=False`
  - Connection pooling với `pool_pre_ping`

#### `src/database/repository.py`
- **Mục đích:** Generic repository pattern (optional, có thể đã có)

#### `src/database/migrate.py`
- **Mục đích:** Database migration scripts

---

### 1.5 `src/utils/` - Utility Layer

**Mục đích:** Các hàm helper và utilities (là các module, hàm hoặc lớp dùng chung cung cấp các tiện ích hỗ trợ, giúp thực hiện các tác vụ phổ biến, lặp đi lặp lại mà không thuộc về logic chính của ứng dụng) dùng chung.

**File tiêu biểu:**

#### `src/utils/validators.py`
- **Mục đích:** Validation functions cho dữ liệu
- **Cách dùng:**
```python
from src.utils.validators import validate_email, validate_phone, ValidationResult

result = validate_email("test@example.com")
if result.is_valid:
    print("Email hợp lệ")
else:
    print(result.message)  # "Email không đúng định dạng"

result = validate_phone("0901234567")
```
- **Các validators có sẵn:**
  - `validate_email()` - Email format
  - `validate_phone()` - Vietnamese phone
  - `validate_required()` - Required field
  - `validate_length()` - String length
  - `validate_number()` - Number range
  - `validate_date()` - Date format
  - `validate_currency()` - Tiền tệ
  - `validate_password()` - Password strength

#### `src/utils/formatters.py`
- **Mục đích:** Format data cho display (currency, date, number...)
```python
from src.utils.formatters import format_currency, format_date

formatted = format_currency(1000000)  # "1.000.000 đ"
```

#### `src/utils/helpers.py`
- **Mục đích:** Các hàm helper đa dụng
- **`generate_code()`** - Tạo mã tự động (KH, HD, HH...)
- **`get_data_dir()`** - Lấy đường dẫn thư mục data

#### `src/utils/export_service.py`
- **Mục đích:** Export dữ liệu ra Excel/PDF

---

### 1.6 `src/data/` - Database Files

**Mục đích:** Chứa database file SQLite và scripts khởi tạo.

**File tiêu biểu:**

#### `src/data/database.py`
- **Mục đích:** Định nghĩa đường dẫn database, có thể chứa schema info

#### `src/data/init_db.py`
- **Mục đích:** Script initialize database
- **Cách dùng:**
```bash
python src/data/init_db.py
```

---

### 1.7 Các file ở thư mục gốc

#### `src/main.py`
- **Mục đích:** Entry point chính của ứng dụng
- **Cách dùng:**
```bash
python main.py
```

#### `src/app.py`
- **Mục đích:** Application class (QApplication subclass)
- **Đặc điểm:**
  - Setup stylesheet
  - Setup fonts
  - Tạo MainWindow

#### `src/main_window.py`
- **Mục đích:** Main application window (QMainWindow)
- **Đặc điểm:**
  - Menu bar với các module
  - Toolbar với shortcuts
  - Status bar (hiển thị thời gian, user info)
  - Central widget (NavigationPanel)

---

## 2. Luồng dữ liệu (Data Flow)

```
┌─────────────────────────────────────────────────────────────────┐
│                         GUI Layer                                │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐  │
│  │ Views       │  │ Forms       │  │ Widgets                 │  │
│  │ - Dashboard │  │ - KhachHang │  │ - DataTable             │  │
│  │ - KhoView   │  │ - HopDong   │  │ - Charts                │  │
│  │ - ...       │  │ - ...       │  │ - SearchBox             │  │
│  └──────┬──────┘  └──────┬──────┘  └───────────┬─────────────┘  │
└─────────┼────────────────┼────────────────────┼─────────────────┘
          │ Submit         │ Input              │ Events/Signals
          ▼                ▼                    ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Service Layer                               │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ KhachHangService, KhoService, HopDongService,        ...     ││
│  │ - CRUD operations                                          ││
│  │ - Business validation                                      ││
│  │ - Transaction management                                   ││
│  └──────────────────────────────┬──────────────────────────────┘│
└─────────────────────────────────┼───────────────────────────────┘
                                  │ Session management
                                  ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Database Layer                             │
│  ┌────────────────────┐    ┌───────────────────────────────────┐│
│  │ DatabaseConnection  │    │ Repository                       ││
│  │ (Singleton)         │◄──►│ (Data access pattern)             ││
│  └─────────┬───────────┘    └───────────────────────────────────┘│
└────────────┼──────────────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      SQLite Database                            │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐             │
│  │khach_hang│  │   kho   │  │ vi_tri  │  │hop_dong │  ...        │
│  └─────────┘  └─────────┘  └─────────┘  └─────────┘             │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. Ví dụ luồng xử lý Thêm Khách hàng

```
1. User click "Thêm KH" → signal emitted
         │
         ▼
2. View mở form: show_khach_hang_form(parent)
         │
         ▼
3. User điền form → validation (validators.py)
         │
         ▼
4. User click "Lưu" → emit accepted_with_data signal
         │
         ▼
5. View nhận data → gọi KhachHangService.create(data)
         │
         ▼
6. Service.validate_data() → kiểm tra business rules
         │
         ▼
7. Service tạo model instance → session.add()
         │
         ▼
8. session.commit() → database
         │
         ▼
9. View refresh → table.update()
```

---

## 4. Quick Reference

| Module | Import | Mục đích |
|--------|--------|----------|
| Models | `from src.models import KhachHang` | Database entities |
| Services | `from src.services import KhachHangService` | Business logic |
| Views | `from src.gui.views import DashboardView` | UI screens |
| Forms | `from src.gui.forms import show_khach_hang_form` | Input dialogs |
| Database | `from src.database import get_session` | DB connection |
| Validators | `from src.utils.validators import validate_email` | Validation |
| Dialogs | `from src.gui.dialogs import MessageDialog` | Message boxes |

---

## 5. Cách thêm 1 module mới (ví dụ: Quản lý Nhân viên)

**Bước 1:** Tạo Model (`src/models/nhan_vien.py`)
```python
from .base import BaseModel
from sqlalchemy import Column, String, Enum

class NhanVien(BaseModel):
    __tablename__ = 'nhan_vien'
    ma_nhan_vien = Column(String(20), primary_key=True)
    ho_ten = Column(String(200), nullable=False)
    # ...
```

**Bước 2:** Tạo Service (`src/services/nhan_vien_service.py`)
```python
from src.services.base_service import BaseService

class NhanVienService(BaseService[NhanVien]):
    def get_by_id(self, ma_nhan_vien: str):
        return self.session.query(NhanVien).filter(...).first()
```

**Bước 3:** Tạo View (`src/gui/views/nhan_vien_view.py`)
```python
from PyQt6.QtWidgets import QWidget

class NhanVienView(QWidget):
    def __init__(self):
        super().__init__()
        self.service = NhanVienService()
        # setup UI...
```

**Bước 4:** Tạo Form (`src/gui/forms/nhan_vien_form.py`)
```python
from PyQt6.QtWidgets import QDialog

class NhanVienForm(QDialog):
    # ... form implementation
```

**Bước 5:** Đăng ký trong MainWindow
```python
# Trong main_window.py
from src.gui.views.nhan_vien_view import NhanVienView

# Thêm vào module_views dict
module_views = {
    # ...
    "ql_nhan_vien": NhanVienView,
}
```
