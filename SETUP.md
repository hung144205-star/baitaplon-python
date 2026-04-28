# Hướng Dẫn Cài Đặt & Triển Khai

## Mục Lục
1. [Yêu Cầu Hệ Thống](#1-yêu-cầu-hệ-thống)
2. [Cài Đặt Trên Windows](#2-cài-đặt-trên-windows)
3. [Cài Đặt Trên macOS](#3-cài-đặt-trên-macos)
4. [Cài Đặt Trên Linux (Ubuntu)](#4-cài-đặt-trên-linux-ubuntu)
5. [Khởi Tạo Database](#5-khởi-tạo-database)
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
# Mở Command Prompt (CMD) hoặc PowerShell
# Di chuyển đến thư mục muốn lưu project
cd Documents

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

### Bước 2.4: Kiểm Tra Cài Đặt
```bash
# Kiểm tra Python
python --version
# Output: Python 3.11.x

# Kiểm tra các package đã cài
pip list
# Output sẽ hiển thị: PyQt6, SQLAlchemy, pandas, v.v...
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

## 5. Khởi Tạo Database

### 5.1: Chạy Script Khởi Tạo
```bash
# Di chuyển vào thư mục project (đã làm ở trên)
cd baitaplon-python

# Kích hoạt môi trường ảo (nếu chưa)
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate

# Chạy script khởi tạo database
python -m src.data.init_db
```

### 5.2: Kết Quả Mong Đợi
```
==================================================
QUẢN LÝ DỊCH VỤ CHO THUÊ KHO LƯU TRỮ HÀNG HÓA
==================================================

Đang khởi tạo database...

✓ Database engine created
✓ Models imported
✓ Tables created
✓ Indexes created
✓ Sample data loaded

Database initialized successfully!
Database location: /path/to/project/data/warehouse.db

Default login credentials:
   Username: admin
   Password: admin123
```

### 5.3: Tài Khoản Mặc Định
| Tài khoản | Mật khẩu | Vai trò |
|-----------|----------|---------|
| admin | admin123 | Quản trị viên |

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

### 6.2: Chạy Với PyQt6 Development Mode
```bash
# Linux/macOS - Hiển thị lỗi chi tiết
QT_DEBUG=1 python main.py

# Windows - Chạy từ PowerShell
$env:QT_DEBUG="1"
python main.py
```

### 6.3: Các Lệnh Hữu Ích
```bash
# Deactivate môi trường ảo (khi không sử dụng)
deactivate

# Xóa database và tạo lại (nếu cần)
rm data/warehouse.db
python -m src.data.init_db

# Cập nhật code từ GitHub
git pull origin main
pip install -r requirements.txt  # Cập nhật dependencies nếu có thay đổi
```

---

## 7. Xử Lý Sự Cố

### Lỗi: "No module named 'PyQt6'"
```bash
# Cài đặt lại PyQt6
pip uninstall PyQt6
pip install PyQt6==6.6.1
```

### Lỗi: "Database is locked"
```bash
# Windows: Tắt các chương trình khác đang truy cập database
# Đóng tất cả cửa sổ ứng dụng và chạy lại
```

### Lỗi: "Permission denied" (Linux/macOS)
```bash
# Cấp quyền cho script
chmod +x main.py

# Nếu database không ghi được
chmod 777 data/
chmod 666 data/warehouse.db
```

### Lỗi: bcrypt hash error khi đăng nhập
```bash
# Database có thể chưa được tạo đúng
# Xóa database cũ và tạo lại
rm -f data/warehouse.db
python -m src.data.init_db
```

### Lỗi: ModuleNotFoundError khi import
```bash
# Đảm bảo đang trong virtual environment
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate

# Cài đặt lại dependencies
pip install -r requirements.txt
```

### Lỗi màn hình trắng khi chạy GUI (Linux)
```bash
# Cài đặt thêm các thư viện GUI
sudo apt install -y libxkbcommon-x11-0 libxcb-icccm4 libxcb-image0 libxcb-keysyms1 libxcb-randr0 libxcb-render-util0 libxcb-xinerama0 libxcb-cursor0
```

---

## 8. Cấu Trúc Project

```
baitaplon-python/
├── main.py                 # Entry point - Chạy ứng dụng
├── requirements.txt        # Danh sách dependencies
├── README.md               # Tài liệu tổng quan
├── SETUP.md                # Hướng dẫn cài đặt (file này)
│
├── src/
│   ├── main_app.py         # Main application (GUI)
│   ├── main_window.py      # Main window
│   ├── app.py              # QApplication setup
│   │
│   ├── models/             # SQLAlchemy models
│   │   ├── khach_hang.py
│   │   ├── kho.py
│   │   ├── hop_dong.py
│   │   ├── hang_hoa.py
│   │   ├── thanh_toan.py
│   │   └── nhan_vien.py
│   │
│   ├── services/           # Business logic
│   │   ├── khach_hang_service.py
│   │   ├── kho_service.py
│   │   ├── hop_dong_service.py
│   │   └── auth/
│   │
│   ├── gui/                # Giao diện PyQt6
│   │   ├── views/          # Main views
│   │   ├── forms/          # Form dialogs
│   │   ├── widgets/        # Reusable widgets
│   │   └── dialogs/       # Dialog boxes
│   │
│   ├── database/           # Database utilities
│   ├── utils/              # Helpers, validators
│   └── templates/          # HTML templates cho PDF
│
├── data/                   # Database và dữ liệu
│   ├── warehouse.db        # SQLite database
│   └── exports/            # Các file export
│
├── docs/                   # Tài liệu thiết kế
│
├── tests/                  # Unit tests
│
└── venv/                   # Virtual environment (không commit lên Git)
```

---

## Thông Tin Liên Hệ

### Nhóm 12 - Lập trình Python
- **Trưởng nhóm:** Đoàn Mạnh Hùng
- **Thành viên:** Lương Hán Hải, Nguyễn Đồng Thanh

### GitHub Repository
```
https://github.com/hung144205-star/baitaplon-python
```

### Báo Lỗi
Nếu gặp lỗi trong quá trình cài đặt, vui lòng tạo issue trên GitHub với:
- Hệ điều hành và phiên bản
- Phiên bản Python (`python --version`)
- Nội dung lỗi đầy đủ (copy toàn bộ terminal output)
- Các bước đã thực hiện trước khi gặp lỗi

---

**Cập nhật lần cuối:** 28/04/2026
**Phiên bản:** 1.0.0
