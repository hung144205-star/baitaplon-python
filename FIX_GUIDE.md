# 🔧 Quick Fix Guide

## ✅ Lỗi đã fix:
- ✅ Added `SessionLocal` to database exports
- ✅ Compatible với tất cả services

## 📦 Cài đặt dependencies BẮT BUỘC:

### Option 1: Cài tất cả (khuyến nghị)
```bash
cd /home/hieu/Documents/baitaplon/nhom12/hung/baitaplon-python
pip install -r requirements.txt
```

### Option 2: Cài từng cái
```bash
# Bắt buộc
pip install PyQt6 sqlalchemy python-dateutil

# Optional (cho export Excel)
pip install pandas openpyxl
```

## 🚀 Chạy demo sau khi cài:

```bash
python3 main_demo.py
```

## ✅ Test nhanh import:

```bash
python3 -c "from src.database import SessionLocal; print('✅ OK')"
```

Nếu không có lỗi là đã thành công!
