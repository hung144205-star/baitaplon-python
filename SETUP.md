# Hướng Dẫn Cài Đặt & Triển Khai

## Mục Lục
1. [Yêu Cầu Hệ Thống](#1-yêu-cầu-hệ-thống)
2. [Cài Đặt Trên Windows](#2-cài-đặt-trên-windows)
3. [Cài Đặt Trên macOS](#3-cài-đặt-trên-macos)
4. [Cài Đặt Trên Linux (Ubuntu)](#4-cài-đặt-trên-linux-ubuntu)
5. [Khởi Tạo & Reset Database](#5-khởi-tạo--reset-database)
6. [Chạy Ứng Dụng](#6-chạy-ứng-dụng)
7. [Xử Lý Sự Cố](#7-xử-lý-sự-cố)
8. [Cấu Trúc Project](#8-cấu-trúc-project)

---

## 1. Yêu Cầu Hệ Thống

### Phần cứng tối thiểu
- **CPU:** Intel Core i3 / AMD Ryzen 3 (hoặc tương đương)
- **RAM:** 4 GB
- **Ổ cứng:** 500 MB trống
- **Màn hình:** Độ phân giải 1280x720 trở lên

### Phần mềm
- **Python:** 3.10 hoặc 3.11 (khuyến nghị: 3.11)
- **Git:** Phiên bản mới nhất
- **Hệ điều hành:** Windows 10+, macOS 10.14+, hoặc Ubuntu 20.04+

### Cài đặt Python
#### Windows
1. Tải Python từ [python.org](https://www.python.org/downloads/)
2. Chọn phiên bản **Python 3.11.x**
3. **QUAN TRỌNG:** Tick chọn ✅ "Add Python to PATH"
4. Click "Install Now"

#### macOS
```bash
# Sử dụng Homebrew
brew install python@3.11
```

#### Linux (Ubuntu)
```bash
sudo apt update
sudo apt install python3.11 python3.11-venv python3-pip git
```

---

## 2. Cài Đặt Trên Windows

### Bước 2.1: Clone Project
```bash
# Mở Terminal (CMD hoặc PowerShell)
# Di chuyển đến thư mục muốn lưu
cd %USERPROFILE%\Documents

# Clone repository
git clone https://github.com/hung144205-star/baitaplon-python.git

# Di chuyển vào thư mục project
cd baitaplon-python
```

### Bước 2.2: Tạo Virtual Environment
```bash
# Tạo môi trường ảo
python -m venv venv

# Kích hoạt môi trường ảo
venv\Scripts\activate

# Khi thấy (venv) ở đầu dòng lệnh = đã kích hoạt thành công
```

### Bước 2.3: Cài Đặt Dependencies
```bash
# Nâng cấp pip
pip install --upgrade pip

# Cài đặt tất cả thư viện
pip install -r requirements.txt
```

### Bước 2.4: Cài Đặt PyQt6
```bash
# PyQt6 đã có trong requirements.txt
# Nếu cần cài thủ công:
pip install PyQt6
```

---

## 3. Cài Đặt Trên macOS

### Bước 3.1: Clone Project
```bash
# Mở Terminal
# Di chuyển đến thư mục muốn lưu
cd ~/Documents

# Clone repository
git clone https://github.com/hung144205-star/baitaplon-python.git

# Di chuyển vào thư mục project
cd baitaplon-python
```

### Bước 3.2: Tạo Virtual Environment
```bash
# Tạo môi trường ảo
python3 -m venv venv

# Kích hoạt môi trường ảo
source venv/bin/activate

# Khi thấy (venv) ở đầu dòng lệnh = đã kích hoạt thành công
```

### Bước 3.3: Cài Đặt Dependencies
```bash
# Nâng cấp pip
pip install --upgrade pip

# Cài đặt tất cả thư viện
pip install -r requirements.txt
```

### Bước 3.4: Cài Đặt PyQt6 (macOS)
```bash
# PyQt6 cần Xcode command line tools
xcode-select --install

# Cài PyQt6 qua pip (đã có trong requirements.txt)
```

---

## 4. Cài Đặt Trên Linux (Ubuntu)

### Bước 4.1: Cài Đặt Các Gói Hệ Thống
```bash
sudo apt update
sudo apt install -y python3.11 python3.11-venv python3-pip git libgl1-mesa-glx libglib2.0-0
```

### Bước 4.2: Clone Project
```bash
# Di chuyển đến thư mục home
cd ~

# Clone repository
git clone https://github.com/hung144205-star/baitaplon-python.git

# Di chuyển vào thư mục project
cd baitaplon-python
```

### Bước 4.3: Tạo Virtual Environment
```bash
# Tạo môi trường ảo
python3 -m venv venv

# Kích hoạt môi trường ảo
source venv/bin/activate

# Khi thấy (venv) ở đầu dòng lệnh = đã kích hoạt thành công
```

### Bước 4.4: Cài Đặt Dependencies
```bash
# Nâng cấp pip
pip install --upgrade pip

# Cài đặt tất cả thư viện
pip install -r requirements.txt
```

---

## 5. Khởi Tạo & Reset Database

### 5.1: Khởi Tạo Database (Lần đầu tiên)

**Yêu cầu:** Đã cài đặt dependencies và kích hoạt virtual environment.

```bash
# Di chuyển vào thư mục project
cd baitaplon-python

# Kích hoạt môi trường ảo
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate

# Chạy script khởi tạo database
python -m src.data.init_db
```

### 5.2: Reset Database (Xóa và tạo lại)

Thực hiện khi:
- Database bị lỗi
- Muốn xóa dữ liệu và tạo lại từ đầu
- Quên mật khẩu admin và cần tạo lại

```bash
# Di chuyển vào thư mục project
cd baitaplon-python

# Kích hoạt môi trường ảo
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate

# BƯỚC 1: Xóa database cũ
rm data/warehouse.db

# BƯỚC 2: Tạo database mới
python -m src.data.init_db
```

### 5.3: Kết Quả Mong Đợi

```
============================================================
KHỞI TẠO DATABASE - QUẢN LÝ KHO LƯU TRỮ
============================================================
📦 Kết nối database: sqlite:////path/to/project/data/warehouse.db
📝 Đang tạo các bảng...
✅ Database đã được tạo thành công!
📇 Đang tạo indexes...
✅ Indexes đã được tạo!
👁️ Đang tạo views...
✅ Views đã được tạo!
📊 Đang tạo dữ liệu mẫu...
✅ Dữ liệu mẫu đã được tạo!

📋 Thông tin đăng nhập mặc định:
   Username: admin
   Password: admin123
   ⚠️  Vui lòng đổi mật khẩu sau khi đăng nhập!

============================================================
✅ HOÀN THÀNH KHỞI TẠO DATABASE!
============================================================
```

### 5.4: Tài Khoản Mặc Định

| Tài khoản | Mật khẩu | Vai trò |
|-----------|----------|----------|
| admin | admin123 | Quản trị viên |

### 5.5: Xử Lý Lỗi Đăng Nhập

**Triệu chứng:** Đăng nhập đúng password `admin123` nhưng bị báo sai

**Nguyên nhân:** Database cũ được tạo với mã hóa không tương thích

**Cách khắc phục:**
```bash
# Xóa database cũ
rm data/warehouse.db

# Tạo database mới với mã hóa đúng cho máy hiện tại
python -m src.data.init_db
```

---

## 6. Chạy Ứng Dụng

### 6.1: Chạy Bình Thường
```bash
# Đảm bảo đang ở trong thư mục project
cd baitaplon-python

# Kích hoạt môi trường ảo
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate

# Chạy ứng dụng
python main.py
```

### 6.2: Kiểm Tra Database Có Dữ Liệu
```bash
# Chạy script kiểm tra
python -c "
from src.data.database import init_db
from sqlalchemy import text

engine, Session = init_db()
session = Session()
result = session.execute(text('SELECT COUNT(*) FROM nhan_vien'))
count = result.scalar()
print(f'Số nhân viên trong DB: {count}')
session.close()
"
```

---

## 7. Xử Lý Sự Cố

### Lỗi "Module not found"
```bash
# Cài lại dependencies
pip install -r requirements.txt
```

### Lỗi "Permission denied" khi chạy init_db (Linux)
```bash
# Phân quyền cho thư mục data
chmod 755 data/
chmod 644 data/warehouse.db 2>/dev/null || true
```

### Lỗi PyQt6 không tìm thấy
```bash
# Cài lại PyQt6
pip install PyQt6
```

### Lỗi kết nối database
```bash
# Xóa và tạo lại database
rm data/warehouse.db
python -m src.data.init_db
```

---

## 8. Cấu Trúc Project

```
baitaplon-python/
├── main.py              # File chạy chính
├── main.py              # Entry point
├── requirements.txt     # Danh sách thư viện Python
├── SETUP.md             # Hướng dẫn cài đặt (file này)
├── README.md            # Tài liệu tổng quan
├── TASKS.md             # Danh sách công việc
│
├── src/
│   ├── main_app.py      # Ứng dụng chính (PyQt6)
│   ├── main_window.py   # Main window & navigation
│   ├── data/
│   │   ├── database.py  # Database initialization
│   │   └── warehouse.db # SQLite database file
│   ├── models/          # SQLAlchemy models
│   ├── services/        # Business logic layer
│   ├── gui/             # PyQt6 UI components
│   │   ├── views/       # Main view screens
│   │   ├── forms/       # Dialog forms
│   │   ├── widgets/     # Reusable widgets
│   │   └── dialogs/     # Dialog windows
│   └── utils/           # Utility functions
│
├── data/                # Data files
│   ├── warehouse.db     # SQLite database
│   └── exports/         # Exported files (PDF, Excel)
│
├── tests/               # Unit tests
├── docs/                # Documentation
└── scripts/             # Utility scripts
```

---

## Liên Hệ & Hỗ Trợ

- **Nhóm:** Nhóm 12 - Lập trình Python
- **Thành viên:** Đoàn Mạnh Hùng, Lương Hán Hải, Nguyễn Đồng Thanh
- **GitHub:** https://github.com/hung144205-star/baitaplon-python
