# Tech Stack - Quản Lý Dịch Vụ Cho Thuê Kho Lưu Trữ Hàng Hóa

## 1. TỔNG QUAN

| Thành phần | Công nghệ | Phiên bản | Lý do lựa chọn |
|------------|-----------|-----------|----------------|
| Ngôn ngữ lập trình | Python | 3.10+ | Dễ học, thư viện phong phú, cộng đồng lớn |
| GUI Framework | PyQt6 | 6.4+ | Hiện đại, đa nền tảng, giao diện chuyên nghiệp |
| Database | SQLite | 3.x | Nhẹ, nhúng trong ứng dụng, không cần cài đặt server |
| ORM | SQLAlchemy | 2.0+ | Trừu tượng hóa database, dễ bảo trì |
| Báo cáo | ReportLab | 3.6+ | Xuất PDF chuyên nghiệp |
| Testing | pytest | 7.x+ | Framework test mạnh mẽ, dễ sử dụng |

## 2. CHI TIẾT CÔNG NGHỆ

### 2.1 Python 3.10+
- **Vai trò**: Ngôn ngữ lập trình chính
- **Tính năng sử dụng**:
  - Type hints (gợi ý kiểu dữ liệu)
  - Dataclasses (định nghĩa model đơn giản)
  - f-strings (xuất chuỗi tiện lợi)
  - Match/case (Python 3.10+, thay thế if-elif)
- **Yêu cầu cài đặt**: Python 3.10 hoặc cao hơn

### 2.2 PyQt6 6.4+
- **Vai trò**: Xây dựng giao diện người dùng đồ họa (GUI)
- **Ưu điểm**:
  - Hiện đại, thay thế PyQt5
  - Hỗ trợ Windows, macOS, Linux
  - Widgets phong phú (bảng, form, dialog, v.v.)
  - Hỗ trợ style/theme dễ dàng
  - Signals/Slots cho xử lý sự kiện
- **Thành phần chính sử dụng**:
  - `QMainWindow`: Cửa sổ chính ứng dụng
  - `QTableWidget`: Hiển thị danh sách dữ liệu
  - `QFormLayout`: Form nhập liệu
  - `QDialog`: Cửa sổ dialog
  - `QMessageBox`: Thông báo
  - `QComboBox`, `QLineEdit`, `QDateEdit`: Input controls
  - `QPushButton`, `QToolBar`: Tương tác người dùng
  - `QStackedWidget`: Chuyển đổi giữa các màn hình

### 2.3 SQLite 3.x
- **Vai trò**: Cơ sở dữ liệu nhúng
- **Ưu điểm**:
  - Không cần cài đặt server riêng
  - Database lưu trong file đơn giản
  - Phù hợp ứng dụng desktop đơn người dùng
  - Nhẹ, nhanh với dữ liệu vừa phải
- **Hạn chế**:
  - Không hỗ trợ đa người dùng đồng thời tốt
  - Giới hạn concurrency
- **Đề xuất**: Nếu cần đa người dùng hoặc mở rộng web sau này, chuyển sang PostgreSQL

### 2.4 SQLAlchemy 2.0+
- **Vai trò**: Object-Relational Mapping (ORM)
- **Chức năng**:
  - Ánh xạ Python classes ↔ Database tables
  - Truy vấn database bằng Python syntax
  - Quản lý transactions
  - Migration database (kết hợp Alembic)
- **Lợi ích**:
  - Không viết SQL thủ công
  - Dễ bảo trì, refactor
  - Hỗ trợ nhiều database (SQLite, PostgreSQL, MySQL)

### 2.5 ReportLab 3.6+
- **Vai trò**: Tạo file PDF báo cáo, hóa đơn
- **Ứng dụng**:
  - Xuất hóa đơn thanh toán
  - Báo cáo doanh thu PDF
  - Hợp đồng thuê kho (nếu cần)

### 2.6 pytest 7.x+
- **Vai trò**: Framework kiểm thử đơn vị (unit testing)
- **Tính năng**:
  - Fixtures cho setup/teardown
  - Parametrize cho test nhiều case
  - Coverage reporting (kết hợp pytest-cov)
  - Mocking (kết hợp unittest.mock)

## 3. CẤU TRÚC PROJECT

```
baitaplon-python/
├── main.py                    # Entry point
├── requirements.txt           # Danh sách dependencies
├── README.md                  # Hướng dẫn
├── .gitignore                 # Loại trừ file
│
├── src/                       # Mã nguồn chính
│   ├── __init__.py
│   ├── app.py                 # QApplication chính
│   ├── main_window.py         # QMainWindow
│   │
│   ├── gui/                   # Giao diện PyQt6
│   │   ├── __init__.py
│   │   ├── widgets/           # Custom widgets
│   │   ├── dialogs/           # Dialog windows
│   │   ├── forms/             # Form nhập liệu
│   │   └── views/             # Các màn hình chính
│   │
│   ├── models/                # Database models (SQLAlchemy)
│   │   ├── __init__.py
│   │   ├── khach_hang.py
│   │   ├── kho_hang.py
│   │   ├── hop_dong.py
│   │   ├── hang_hoa.py
│   │   └── thanh_toan.py
│   │
│   ├── services/              # Business logic
│   │   ├── __init__.py
│   │   ├── khach_hang_service.py
│   │   ├── kho_hang_service.py
│   │   ├── hop_dong_service.py
│   │   ├── hang_hoa_service.py
│   │   └── thanh_toan_service.py
│   │
│   ├── database/              # Database connection
│   │   ├── __init__.py
│   │   ├── connection.py      # SQLAlchemy engine/session
│   │   └── init_db.py         # Khởi tạo database
│   │
│   └── utils/                 # Tiện ích
│       ├── __init__.py
│       ├── validators.py      # Validate dữ liệu
│       ├── formatters.py      # Format số, ngày tháng
│       └── pdf_generator.py   # Tạo PDF
│
├── data/                      # Dữ liệu ứng dụng
│   ├── quanlykho.db           # File SQLite
│   └── backups/               # Backup database
│
├── docs/                      # Tài liệu
│   ├── YEU_CAU_CHUC_NANG.md
│   ├── SPEC.md
│   └── TECH_STACK.md          # File này
│
└── tests/                     # Unit tests
    ├── __init__.py
    ├── test_models/
    ├── test_services/
    └── test_gui/
```

## 4. CÀI ĐẶT MÔI TRƯỜNG

### 4.1 Yêu cầu hệ thống
- **OS**: Windows 10/11, macOS 10.14+, hoặc Linux
- **Python**: 3.10 trở lên
- **RAM**: Tối thiểu 4GB
- **Disk**: 500MB trống

### 4.2 Cài đặt dependencies

```bash
# Tạo virtual environment (khuyến nghị)
python -m venv venv

# Kích hoạt environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Cài đặt packages
pip install -r requirements.txt
```

### 4.3 File requirements.txt

```
# Core
PyQt6>=6.4.0

# Database
SQLAlchemy>=2.0.0

# PDF Generation
reportlab>=3.6.0

# Utilities
python-dateutil>=2.8.0

# Development & Testing
pytest>=7.0.0
pytest-cov>=4.0.0
black>=23.0.0          # Code formatter
```

## 5. WORKFLOW PHÁT TRIỂN

### 5.1 Quy trình làm việc
1. **Khởi tạo database**: `python -m src.database.init_db`
2. **Chạy ứng dụng**: `python main.py`
3. **Test**: `pytest tests/`
4. **Format code**: `black src/`

### 5.2 Pattern thiết kế
- **MVC/MVP**: Tách Model (data), View (GUI), Presenter (logic)
- **Repository Pattern**: Tách database access ra khỏi business logic
- **Service Layer**: Xử lý nghiệp vụ phức tạp

## 6. MÔ HÌNH DỮ LIỆU (ORM)

### 6.1 Ví dụ Model SQLAlchemy

```python
# src/models/khach_hang.py
from sqlalchemy import Column, String, DateTime, Enum
from sqlalchemy.orm import declarative_base
from datetime import datetime
import enum

Base = declarative_base()

class LoaiKhach(enum.Enum):
    CA_NHAN = "Cá nhân"
    DOANH_NGHIEP = "Doanh nghiệp"

class KhachHang(Base):
    __tablename__ = 'khach_hang'
    
    ma_khach_hang = Column(String(20), primary_key=True)
    ho_ten = Column(String(100), nullable=False)
    loai_khach = Column(Enum(LoaiKhach), default=LoaiKhach.CA_NHAN)
    so_dien_thoai = Column(String(15))
    email = Column(String(100))
    dia_chi = Column(String(200))
    ngay_dang_ky = Column(DateTime, default=datetime.now)
```

### 6.2 Ví dụ GUI với PyQt6

```python
# src/gui/views/khach_hang_view.py
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, 
    QTableWidget, QTableWidgetItem, 
    QPushButton, QLabel
)

class KhachHangView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Tiêu đề
        title = QLabel("Quản lý Khách hàng")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(title)
        
        # Bảng dữ liệu
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            "Mã KH", "Họ tên", "SĐT", "Email", "Loại"
        ])
        layout.addWidget(self.table)
        
        # Nút chức năng
        btn_layout = QHBoxLayout()
        self.btn_them = QPushButton("Thêm mới")
        self.btn_sua = QPushButton("Sửa")
        self.btn_xoa = QPushButton("Xóa")
        btn_layout.addWidget(self.btn_them)
        btn_layout.addWidget(self.btn_sua)
        btn_layout.addWidget(self.btn_xoa)
        layout.addLayout(btn_layout)
```

## 7. KẾ HOẠCH TRIỂN KHAI

| Giai đoạn | Thời gian | Nội dung | Tech Stack sử dụng |
|-----------|-----------|----------|-------------------|
| 1 | Tuần 1 | Setup project, Database schema, Models | SQLAlchemy, SQLite |
| 2 | Tuần 2 | GUI cơ bản (MainWindow, Menu), Khách hàng CRUD | PyQt6, Models |
| 3 | Tuần 3 | Kho hàng, Vị trí, Hợp đồng | PyQt6, SQLAlchemy |
| 4 | Tuần 4 | Hàng hóa, Thanh toán, Báo cáo | PyQt6, ReportLab |
| 5 | Tuần 5 | Hoàn thiện, Testing, Polish | pytest, PyQt6 |

## 8. TÀI LIỆU THAM KHẢO

- [PyQt6 Documentation](https://www.riverbankcomputing.com/static/Docs/PyQt6/)
- [SQLAlchemy 2.0 Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/)
- [SQLite Documentation](https://www.sqlite.org/docs.html)
- [ReportLab User Guide](https://www.reportlab.com/docs/reportlab-userguide.pdf)
- [pytest Documentation](https://docs.pytest.org/)

---
