# Hướng dẫn Khởi tạo Database

## 📋 Yêu cầu

- Python 3.10+
- pip (Python package manager)

## 🔧 Cài đặt Dependencies

Trước khi khởi tạo database, cần cài đặt các thư viện cần thiết:

```bash
# Di chuyển vào thư mục project
cd /home/hieu/Documents/baitaplon/nhom12/hung/baitaplon-python

# Cài đặt dependencies từ requirements.txt
pip install -r requirements.txt
```

Nếu không có pip, cài đặt trước:

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install python3-pip

# macOS
brew install python3

# Windows
# pip đi kèm với Python installer
```

## 🚀 Khởi tạo Database

### Cách 1: Sử dụng Python script (Khuyến nghị)

```bash
cd /home/hieu/Documents/baitaplon/nhom12/hung/baitaplon-python

# Chạy script khởi tạo
python -m src.data.init_db
```

Hoặc:

```bash
python src/data/init_db.py
```

### Cách 2: Sử dụng SQLite CLI

```bash
cd /home/hieu/Documents/baitaplon/nhom12/hung/baitaplon-python

# Tạo database từ schema SQL
sqlite3 data/warehouse.db < src/data/schema.sql
```

## ✅ Kết quả

Sau khi khởi tạo thành công:

- File database: `data/warehouse.db`
- 9 bảng dữ liệu được tạo
- 20+ indexes cho performance
- 3 views hữu ích
- Dữ liệu mẫu (admin user, 1 kho, 2 vị trí, 1 khách hàng)

## 🔑 Thông tin đăng nhập mặc định

```
Username: admin
Password: admin123
```

⚠️ **Quan trọng**: Vui lòng đổi mật khẩu sau khi đăng nhập lần đầu!

## 📁 Cấu trúc thư mục Data

```
data/
├── warehouse.db          # File database SQLite
└── backups/              # Thư mục chứa backup
    └── .gitkeep
```

## 🔄 Backup Database

Script backup tự động (chạy hàng ngày):

```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
cp data/warehouse.db data/backups/warehouse_$DATE.db

# Xóa backup cũ hơn 30 ngày
find data/backups -name "warehouse_*.db" -mtime +30 -delete
```

## 🐛 Xử lý sự cố

### Lỗi: "No module named 'sqlalchemy'"

```bash
pip install -r requirements.txt
```

### Lỗi: "database is locked"

Đảm bảo không có process nào khác đang truy cập database:

```bash
# Kiểm tra process đang mở file
lsof data/warehouse.db

# Hoặc đơn giản là restart terminal
```

### Lỗi: "no such table"

Chạy lại script khởi tạo:

```bash
python -m src.data.init_db
```

### Reset database (Xóa toàn bộ và tạo mới)

```bash
# Xóa database cũ
rm data/warehouse.db

# Tạo mới
python -m src.data.init_db
```

## 📊 Kiểm tra database

Sử dụng SQLite CLI để kiểm tra:

```bash
sqlite3 data/warehouse.db

# Xem danh sách bảng
.tables

# Xem schema của bảng
.schema khach_hang

# Xem dữ liệu mẫu
SELECT * FROM khach_hang;
SELECT * FROM kho;
SELECT * FROM vi_tri;

# Thoát
.exit
```

## 📖 Tài liệu tham khảo

- [DATABASE_ANALYSIS.md](../docs/DATABASE_ANALYSIS.md) - Thiết kế database chi tiết
- [TECH_STACK.md](../docs/TECH_STACK.md) - Công nghệ sử dụng

---

**Nhóm 12 - Lập trình Python**  
**Cập nhật:** 23/04/2026
