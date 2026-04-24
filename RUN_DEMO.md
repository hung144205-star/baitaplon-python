# 🚀 Hướng Dẫn Chạy Demo

## 📋 Yêu cầu hệ thống

- Python 3.8+
- PyQt6
- Các thư viện trong `requirements.txt`

---

## 🔧 Cài đặt

### 1. Cài đặt dependencies:

```bash
cd /home/hieu/Documents/baitaplon/nhom12/hung/baitaplon-python

pip install -r requirements.txt
```

### 2. Cài đặt thêm (nếu chưa có):

```bash
# PyQt6
pip install PyQt6

# dateutil (cho tính toán ngày)
pip install python-dateutil

# SQLAlchemy (database)
pip install sqlalchemy

# Excel export (optional)
pip install pandas openpyxl
```

---

## 🎯 Chạy Demo

### Option 1: Chạy demo chính (khuyến nghị)

```bash
python main_demo.py
```

**Demo này bao gồm:**
- ✅ Tab Khách Hàng (Phase 3)
- ✅ Tab Kho Hàng (Phase 4) với 3 sub-modules
- ✅ Tab Hợp Đồng (Phase 5)
- ✅ Tab Hàng Hóa (Phase 6)
- ✅ Tab Báo Cáo (Phase 7)

### Option 2: Chạy từng module riêng

```bash
# Phase 3 - Customer Management
python -c "from src.gui.views import KhachHangView; from PyQt6.QtWidgets import QApplication, QMainWindow; import sys; app = QApplication(sys.argv); win = QMainWindow(); win.setCentralWidget(KhachHangView()); win.show(); sys.exit(app.exec())"

# Phase 4 - Kho View
python -c "from src.gui.views import KhoView; from PyQt6.QtWidgets import QApplication, QMainWindow; import sys; app = QApplication(sys.argv); win = QMainWindow(); win.setCentralWidget(KhoView()); win.show(); sys.exit(app.exec())"

# Phase 4 - Vi Tri View
python -c "from src.gui.views import ViTriView; from PyQt6.QtWidgets import QApplication, QMainWindow; import sys; app = QApplication(sys.argv); win = QMainWindow(); win.setCentralWidget(ViTriView()); win.show(); sys.exit(app.exec())"

# Phase 4 - Dashboard
python -c "from src.gui.views import DashboardView; from PyQt6.QtWidgets import QApplication, QMainWindow; import sys; app = QApplication(sys.argv); win = QMainWindow(); win.setCentralWidget(DashboardView()); win.show(); sys.exit(app.exec())"

# Phase 5 - Hop Dong View
python -c "from src.gui.views import HopDongView; from PyQt6.QtWidgets import QApplication, QMainWindow; import sys; app = QApplication(sys.argv); win = QMainWindow(); win.setCentralWidget(HopDongView()); win.show(); sys.exit(app.exec())"

# Phase 6 - Hang Hoa View
python -c "from src.gui.views import HangHoaView; from PyQt6.QtWidgets import QApplication, QMainWindow; import sys; app = QApplication(sys.argv); win = QMainWindow(); win.setCentralWidget(HangHoaView()); win.show(); sys.exit(app.exec())"
```

### Option 3: Chạy tests

```bash
# Chạy tất cả tests
pytest tests/ -v

# Chạy tests với coverage
pytest tests/ --cov=src --cov-report=html

# Xem coverage report
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
start htmlcov\\index.html  # Windows
```

---

## 🎨 Giao diện Demo

### Main Dashboard:
```
┌─────────────────────────────────────────────────────────────┐
│           🏢 HỆ THỐNG QUẢN LÝ KHO                           │
│           Demo giao diện các Phase đã hoàn thành            │
├─────────────────────────────────────────────────────────────┤
│  [👥 Khách Hàng] [🏭 Kho Hàng] [📋 Hợp Đồng] [📦 Hàng Hóa]  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  🏭 Danh Sách Kho                                    │   │
│  │  Xem và quản lý danh sách kho                        │   │
│  │           [Mở]                                       │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  📍 Vị Trí Lưu Trữ                                   │   │
│  │  Quản lý vị trí trong kho                            │   │
│  │           [Mở]                                       │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  📊 Dashboard Kho                                    │   │
│  │  Thống kê và biểu đồ kho hàng                        │   │
│  │           [Mở]                                       │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

---

## 📊 Các Module Available:

### Phase 3 - Customer Management (👥)
- ✅ Danh sách khách hàng
- ✅ Form thêm/sửa khách hàng
- ✅ Tìm kiếm & filter
- ✅ Statistics bar

### Phase 4 - Warehouse Management (🏭)
- ✅ Danh sách kho
- ✅ Danh sách vị trí
- ✅ Dashboard với thống kê
- ✅ Forms cho kho & vị trí
- ✅ Export Excel

### Phase 5 - Contract Management (📋)
- ✅ Danh sách hợp đồng
- ✅ Form thêm/sửa hợp đồng
- ✅ Detail view với 4 tabs
- ✅ Renewal & Termination wizards
- ✅ Alerts cho hợp đồng sắp hết hạn

### Phase 6 - Goods Management (📦)
- ✅ Danh sách hàng hóa
- ✅ Form thêm/sửa hàng hóa
- ✅ Import/Export forms
- ✅ Inventory alerts
- ✅ Stock level tracking

### Phase 7 - Reports (📊)
- ✅ Dashboard tổng hợp
- ✅ Statistics từ tất cả modules
- ✅ Export reports

---

## ⚠️ Lưu ý

### Database:
- Demo sẽ kết nối với database cấu hình trong `src/database.py`
- Nếu chưa có database, cần chạy migrations hoặc tạo tables trước

### Data:
- Để xem demo đẹp, nên có data mẫu trong database
- Có thể insert data mẫu bằng script trong `scripts/seed_data.py` (nếu có)

### Images:
- Một số views có thể yêu cầu images
- Đảm bảo thư mục `data/images/` tồn tại

---

## 🐛 Troubleshooting

### Lỗi: "No module named 'PyQt6'"
```bash
pip install PyQt6
```

### Lỗi: "No module named 'src'"
```bash
# Đảm bảo đang ở trong thư mục project
cd /home/hieu/Documents/baitaplon/nhom12/hung/baitaplon-python

# Hoặc thêm path
export PYTHONPATH=/home/hieu/Documents/baitaplon/nhom12/hung/baitaplon-python:$PYTHONPATH
```

### Lỗi database connection:
```bash
# Kiểm tra file cấu hình database
cat src/database.py

# Đảm bảo database file tồn tại (nếu dùng SQLite)
ls -la data/*.db
```

### Lỗi import services:
```bash
# Kiểm tra các file service tồn tại
ls -la src/services/
```

---

## 📞 Support

Nếu gặp vấn đề khi chạy demo:
1. Kiểm tra error message trong console
2. Đảm bảo đã cài đủ dependencies
3. Kiểm tra database connection
4. Restart application

---

**Chúc anh test vui vẻ! 🎉**
