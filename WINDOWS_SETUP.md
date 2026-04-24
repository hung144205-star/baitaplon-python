# 🪟 Windows Setup Guide

## 📁 Đường dẫn project trên Windows

Thay thế đường dẫn Linux:
```
/home/hieu/Documents/baitaplon/nhom12/hung/baitaplon-python
```

Bằng đường dẫn Windows, ví dụ:
```
C:\Users\<YourName>\Documents\baitaplon\nhom12\hung\baitaplon-python
```

Hoặc:
```
D:\Projects\baitaplon-python
```

---

## 🔧 Cài đặt trên Windows

### 1. Cài Python 3.8+

Download từ: https://www.python.org/downloads/

✅ **Quan trọng:** Tick vào "Add Python to PATH" khi cài đặt!

### 2. Clone hoặc copy project

```powershell
# Tạo thư mục
mkdir C:\Users\<YourName>\Documents\baitaplon\nhom12\hung
cd C:\Users\<YourName>\Documents\baitaplon\nhom12\hung

# Copy project vào đây
```

### 3. Tạo virtual environment

```powershell
# Trong thư mục project
cd baitaplon-python

# Tạo venv
python -m venv venv

# Activate venv
.\venv\Scripts\Activate.ps1

# Nếu gặp lỗi execution policy:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 4. Cài dependencies

```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Chạy demo

```powershell
python main_demo.py
```

---

## 📝 Các files cần update path

### **1. SETUP.md**
Thay dòng 6:
```markdown
# ❌ Linux
cd /home/hieu/Documents/baitaplon/nhom12/hung/baitaplon-python

# ✅ Windows
cd C:\Users\<YourName>\Documents\baitaplon\nhom12\hung\baitaplon-python
```

### **2. data/README.md**
Thay các dòng 14, 39, 54:
```markdown
# ❌ Linux
cd /home/hieu/Documents/baitaplon/nhom12/hung/baitaplon-python

# ✅ Windows
cd C:\Users\<YourName>\Documents\baitaplon\nhom12\hung\baitaplon-python
```

### **3. tests/README.md**
Thay dòng 13:
```markdown
# ❌ Linux
cd /home/hieu/Documents/baitaplon/nhom12/hung/baitaplon-python

# ✅ Windows
cd C:\Users\<YourName>\Documents\baitaplon\nhom12\hung\baitaplon-python
```

### **4. RUN_DEMO.md**
Thay các dòng 16, 188, 191:
```markdown
# ❌ Linux
cd /home/hieu/Documents/baitaplon/nhom12/hung/baitaplon-python
export PYTHONPATH=/home/hieu/Documents/baitaplon/nhom12/hung/baitaplon-python:$PYTHONPATH

# ✅ Windows
cd C:\Users\<YourName>\Documents\baitaplon\nhom12\hung\baitaplon-python
# Không cần set PYTHONPATH trên Windows
```

### **5. FIX_GUIDE.md**
Thay dòng 11:
```markdown
# ❌ Linux
cd /home/hieu/Documents/baitaplon/nhom12/hung/baitaplon-python

# ✅ Windows
cd C:\Users\<YourName>\Documents\baitaplon\nhom12\hung\baitaplon-python
```

---

## ⚙️ Cấu hình database

Database file sẽ tự động tạo trong thư mục `data/`:
```
data/warehouse.db
```

Trên Windows, path sẽ là:
```
C:\Users\<YourName>\Documents\baitaplon\nhom12\hung\baitaplon-python\data\warehouse.db
```

---

## 🐛 Troubleshooting

### Lỗi: "python is not recognized"

```powershell
# Kiểm tra Python đã cài chưa
python --version

# Nếu chưa có trong PATH, dùng:
py --version
```

### Lỗi: "Activate.ps1 cannot be loaded"

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Lỗi: "No module named 'PyQt6'"

```powershell
pip install PyQt6
```

### Lỗi: Database connection

Kiểm tra file `src/database/connection.py`:
```python
# Đường dẫn database sẽ tự động adjust theo OS
DB_PATH = os.path.join(project_root, 'data', 'warehouse.db')
```

---

## ✅ Checklist sau khi transfer

- [ ] Cài Python 3.8+
- [ ] Copy project sang Windows
- [ ] Tạo virtual environment
- [ ] Cài dependencies (`pip install -r requirements.txt`)
- [ ] Update paths trong documentation
- [ ] Chạy thử `python main_demo.py`
- [ ] Test tạo khách hàng mới
- [ ] Test sửa khách hàng
- [ ] Test các modules khác

---

## 📞 Support

Nếu gặp vấn đề:
1. Kiểm tra Python version: `python --version`
2. Kiểm tra venv đã activate: `(venv)` xuất hiện trong terminal
3. Reinstall dependencies: `pip install -r requirements.txt --force-reinstall`
4. Clear cache: Xóa thư mục `__pycache__` trong toàn project

---

**Chúc code vui vẻ trên Windows! 🎉**
