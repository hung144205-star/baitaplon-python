# 🚀 Hướng dẫn Cài đặt và Khởi tạo

## Bước 1: Cài đặt Python Dependencies

```bash
cd /home/hieu/Documents/baitaplon/nhom12/hung/baitaplon-python

# Cài đặt tất cả dependencies
pip install -r requirements.txt
```

### Nếu không có pip:

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install python3-pip python3-venv
```

**macOS:**
```bash
brew install python3
```

**Windows:**
- Tải Python từ https://python.org (bao gồm pip)

### Khuyến nghị: Sử dụng Virtual Environment

```bash
# Tạo virtual environment
python -m venv venv

# Kích hoạt
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Cài đặt dependencies
pip install -r requirements.txt
```

## Bước 2: Khởi tạo Database

```bash
# Cách 1: Sử dụng Python script (Khuyến nghị)
python -m src.data.init_db

# Cách 2: Sử dụng SQLite CLI (nếu có)
sqlite3 data/warehouse.db < src/data/schema.sql
```

## Bước 3: Chạy ứng dụng

```bash
python main.py
```

## 📁 Cấu trúc Project sau khi cài đặt

```
baitaplon-python/
├── main.py                    # Entry point
├── requirements.txt           # Dependencies
├── README.md                  # Hướng dẫn
│
├── src/                       # Mã nguồn
│   ├── __init__.py
│   ├── main.py                # Application entry
│   └── data/                  # Data layer
│       ├── __init__.py
│       ├── database.py        # SQLAlchemy models
│       ├── init_db.py         # Database initialization
│       └── schema.sql         # SQL schema
│
├── data/                      # Dữ liệu ứng dụng
│   ├── warehouse.db           # SQLite database (tạo sau khi init)
│   ├── README.md              # Hướng dẫn database
│   └── backups/               # Backup folder
│
└── docs/                      # Tài liệu
    ├── DATABASE_ANALYSIS.md   # Thiết kế database
    ├── TECH_STACK.md          # Công nghệ
    ├── SPEC.md                # Đặc tả
    └── ...
```

## 🔑 Thông tin đăng nhập mặc định

```
Username: admin
Password: admin123
```

⚠️ **Đổi mật khẩu ngay sau khi đăng nhập lần đầu!**

## 📦 Các lệnh hữu ích

```bash
# Chạy tests (khi có)
pytest tests/

# Format code
black src/

# Kiểm tra database
sqlite3 data/warehouse.db ".tables"

# Backup database
cp data/warehouse.db data/backups/warehouse_$(date +%Y%m%d).db
```

## 🐛 Xử lý sự cố

Xem chi tiết trong `data/README.md`

---

**Nhóm 12 - Lập trình Python**  
**Cập nhật:** 23/04/2026
