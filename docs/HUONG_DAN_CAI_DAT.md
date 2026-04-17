# 📚 Hướng Dẫn Cài Đặt và Chạy Demo

Tài liệu này hướng dẫn cách cài đặt môi trường và chạy các giao diện demo PyQt6 cho hệ thống **Quản lý dịch vụ cho thuê kho lưu trữ hàng hóa**.

---

## 📋 Yêu Cầu Hệ Thống

| Thành phần | Yêu cầu |
|------------|---------|
| **Hệ điều hành** | Windows 10/11, macOS 10.14+, hoặc Linux |
| **Python** | Phiên bản 3.10 trở lên |
| **RAM** | Tối thiểu 4GB |
| **Dung lượng trống** | 500MB |
| **Màn hình** | Độ phân giải tối thiểu 1280x720 |

---

## 🔧 Bước 1: Cài Đặt Python

### Windows
1. Truy cập: https://python.org/downloads
2. Tải Python 3.10+ (khuyến nghị Python 3.12)
3. Chạy installer, **tích chọn** "Add Python to PATH"
4. Click "Install Now"

### macOS
```bash
# Cài đặt Homebrew (nếu chưa có)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Cài Python
brew install python@3.12
```

### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install python3.12 python3.12-venv python3-pip
```

### Kiểm tra Python đã cài đặt
```bash
python --version
# hoặc
python3 --version
```

Kết quả mong đợi: `Python 3.10.x` hoặc cao hơn

---

## 📦 Bước 2: Clone Repository

### Cách 1: Clone bằng Git (khuyến nghị)
```bash
# Clone repository
git clone https://github.com/hung144205-star/baitaplon-python.git

# Di chuyển vào thư mục
cd baitaplon-python
```

### Cách 2: Tải ZIP
1. Truy cập: `https://github.com/hung144205-star/baitaplon-python`
2. Click nút **Code** → **Download ZIP**
3. Giải nén file ZIP
4. Mở terminal/command prompt trong thư mục đã giải nén

---

## 🎯 Bước 3: Cài Đặt Dependencies

### 3.1 Tạo Virtual Environment (khuyến nghị)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

> 💡 **Lưu ý:** Khi thấy `(venv)` ở đầu dòng lệnh là virtual environment đã được kích hoạt.

### 3.2 Cài Đặt Các Thư Viện

```bash
pip install -r requirements.txt
```

**Các thư viện sẽ được cài đặt:**

| Thư viện | Phiên bản | Mục đích |
|----------|-----------|----------|
| `PyQt6` | >=6.4.0 | Framework giao diện đồ họa |
| `SQLAlchemy` | >=2.0.0 | ORM cho database |
| `reportlab` | >=3.6.0 | Xuất báo cáo PDF |
| `pytest` | >=7.0.0 | Unit testing |
| `python-dateutil` | >=2.8.0 | Xử lý ngày tháng |

### 3.3 Kiểm Tra Cài Đặt

```bash
pip list
```

Đảm bảo có `PyQt6` trong danh sách đã cài đặt.

---

## 🚀 Bước 4: Chạy Demo

### 4.1 Cấu Trúc Thư Mục Demo

```
docs/demo_ui/
├── khachhang_demo.py    # Demo Quản lý khách hàng
├── khohang_demo.py      # Demo Quản lý kho hàng
└── hopdong_demo.py      # Demo Quản lý hợp đồng
```

### 4.2 Chạy Từng Demo

**Demo 1: Quản lý khách hàng**
```bash
cd docs/demo_ui
python khachhang_demo.py
```

**Demo 2: Quản lý kho hàng**
```bash
cd docs/demo_ui
python khohang_demo.py
```

**Demo 3: Quản lý hợp đồng**
```bash
cd docs/demo_ui
python hopdong_demo.py
```

> 💡 **Mẹo:** Chạy từng demo trong cửa sổ terminal riêng để có thể xem song song.

---

## 🎨 Bước 5: Tính Năng Demo

### Demo Khách Hàng (`khachhang_demo.py`)
- ✅ Danh sách khách hàng với bảng dữ liệu
- ✅ Stats cards (tổng KH, cá nhân, doanh nghiệp)
- ✅ Tìm kiếm và lọc
- ✅ Dialog thêm mới khách hàng
- ✅ Dialog chi tiết khách hàng (thông tin + lịch sử)

### Demo Kho Hàng (`khohang_demo.py`)
- ✅ Danh sách kho với tỷ lệ lấp đầy (capacity indicator)
- ✅ Stats cards (tổng kho, hoạt động, bảo trì)
- ✅ Dialog thêm mới kho
- ✅ Dialog chi tiết kho (3 tabs: Tổng quan, Vị trí, Lịch sử)

### Demo Hợp Đồng (`hopdong_demo.py`)
- ✅ Danh sách hợp đồng với trạng thái
- ✅ Wizard 3 bước tạo hợp đồng mới
- ✅ Dialog gia hạn hợp đồng
- ✅ **Liên kết module**: Navigation bar chuyển đổi giữa các demo
- ✅ Link trong table: Xem chi tiết KH/Kho

---

## 🖱️ Cách Sử Dụng

### Chuyển Đổi Giữa Các Module

Từ bất kỳ demo nào, click vào **Navigation Bar** ở trên cùng:

```
┌─────────────────────────────────────────────────┐
│ 🏭 KhoSmart Pro │ Khách hàng │ Kho │ Hợp đồng │ ... │
└─────────────────────────────────────────────────┘
```

- Click **Khách hàng** → Mở demo khachhang_demo.py
- Click **Kho** → Mở demo khohang_demo.py
- Click **Hợp đồng** → Mở demo hopdong_demo.py

### Các Thao Tác Chính

| Thao tác | Cách thực hiện |
|----------|----------------|
| **Thêm mới** | Click nút "+ Thêm mới" (góc phải trên) |
| **Xem chi tiết** | Click icon 👁️ trong cột Thao tác |
| **Chỉnh sửa** | Click icon ✏️ trong cột Thao tác |
| **Tìm kiếm** | Nhập vào ô tìm kiếm (góc trái trên) |
| **Đóng ứng dụng** | Click X hoặc Alt+F4 |

---

## ❗ Xử Lý Lỗi Thường Gặp

### Lỗi 1: "ModuleNotFoundError: No module named 'PyQt6'"

**Nguyên nhân:** Chưa cài đặt thư viện PyQt6

**Cách fix:**
```bash
pip install PyQt6>=6.4.0
```

### Lỗi 2: "python: command not found" (Windows)

**Nguyên nhân:** Python chưa được thêm vào PATH

**Cách fix:**
- Mở lại installer Python
- Chọn "Modify" → Tích "Add Python to environment variables"
- Hoặc dùng `py` thay vì `python`:
```bash
py khachhang_demo.py
```

### Lỗi 3: "ImportError: cannot import name ..."

**Nguyên nhân:** Chạy file từ sai thư mục

**Cách fix:**
```bash
# Đảm bảo đang ở đúng thư mục
cd docs/demo_ui
python khachhang_demo.py
```

### Lỗi 4: Giao diện không hiển thị đúng (Linux)

**Nguyên nhân:** Thiếu Qt platform plugin

**Cách fix:**
```bash
# Ubuntu/Debian
sudo apt install python3-pyqt5

# Fedora
sudo dnf install python3-qt5
```

---

## 🎨 Design System

Các demo sử dụng **Notion-inspired Design System**:

| Yếu tố | Giá trị |
|--------|---------|
| **Primary Color** | `#0075de` (Notion Blue) |
| **Background** | `#f6f5f4` (Warm White) |
| **Text** | `rgba(0,0,0,0.95)` (Near Black) |
| **Font** | Inter, system fonts |
| **Border radius** | 4px (buttons), 12px (cards) |

Xem chi tiết tại: `docs/DESIGN.md`

---

## 📁 Các File Liên Quan

| File | Mô tả |
|------|-------|
| `requirements.txt` | Danh sách dependencies |
| `docs/DESIGN.md` | Design system tài liệu |
| `docs/demo_ui/*.py` | Code demo PyQt6 |
| `docs/YEU_CAU_CHUC_NANG.md` | Yêu cầu chức năng hệ thống |
| `docs/TECH_STACK.md` | Công nghệ sử dụng |

---

## 💡 Mẹo Sử Dụng

1. **Chạy nhiều demo song song**: Mở 3 terminal, chạy 3 file demo khác nhau
2. **Thay đổi dữ liệu mẫu**: Sửa trong hàm `load_sample_data()` của mỗi file
3. **Test responsive**: Kéo thay đổi kích thước cửa sổ để xem layout điều chỉnh
4. **Xem code**: Mở file `.py` bằng VS Code hoặc editor yêu thích để tham khảo

---

## 🆘 Hỗ Trợ

Nếu gặp vấn đề:
1. Kiểm tra lại các bước cài đặt
2. Đảm bảo Python version >= 3.10
3. Kiểm tra `pip list` để xem PyQt6 đã cài chưa
4. Liên hệ team phát triển

---

**Cập nhật:** 17/04/2026  
**Phiên bản:** 1.0
