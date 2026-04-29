# Quản Lý Dịch Vụ Cho Thuê Kho Lưu Trữ Hàng Hóa

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/Python-3.10+-green)
![PyQt6](https://img.shields.io/badge/PyQt6-6.4+-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)

## Giới thiệu

**Quản Lý Kho Lưu Trữ** là phần mềm quản lý kho hàng hiện đại, được phát triển bằng Python và PyQt6. Phần mềm hỗ trợ đầy đủ các chức năng quản lý kho, khách hàng, hợp đồng, hàng hóa và thanh toán.

## ✨ Tính năng chính

### 📊 Quản lý Dashboard
- Tổng quan hệ thống với biểu đồ thống kê
- Cảnh báo hợp đồng sắp hết hạn
- Thống kê doanh thu theo tháng

### 👥 Quản lý Khách hàng
- Thêm/Sửa/Xóa khách hàng
- Phân loại khách hàng (Cá nhân / Doanh nghiệp)
- Lịch sử giao dịch với khách hàng
- Tìm kiếm và lọc nâng cao

### 🏭 Quản lý Kho hàng
- Quản lý nhiều kho với thông tin chi tiết
- Theo dõi diện tích và sức chứa
- Tính tỷ lệ lấp đầy tự động
- Quản lý vị trí lưu trữ (Khu vực, Hàng, Tầng)

### 📄 Quản lý Hợp đồng
- Tạo và quản lý hợp đồng thuê kho
- Gia hạn và chấm dứt hợp đồng
- Cảnh báo hợp đồng sắp hết hạn
- In hợp đồng ra file

### 📦 Quản lý Hàng hóa
- Nhập/Xuất hàng hóa
- Theo dõi tồn kho theo thời gian thực
- Cảnh báo tồn kho thấp
- In phiếu nhập/xuất kho

### 💰 Quản lý Thanh toán
- Theo dõi công nợ khách hàng
- Cập nhật trạng thái thanh toán
- Lịch sử thanh toán
- In phiếu thanh toán

### 📈 Báo cáo
- Xuất báo cáo PDF
- Xuất báo cáo Excel
- Dashboard thống kê
- Biểu đồ trực quan

### 🔐 Bảo mật
- Đăng nhập với tài khoản và mật khẩu
- Phân quyền người dùng (Admin / User)
- Session management
- Activity log

### ⚙️ Cài đặt
- Thông tin công ty
- Cấu hình hệ thống
- Quản lý người dùng
- Sao lưu và phục hồi database

## 👥 Thành viên nhóm

| Họ tên | Vai trò |
|--------|---------|
| Đoàn Mạnh Hùng | Trưởng nhóm |
| Lương Hán Hải | Thành viên |
| Nguyễn Đồng Thanh | Thành viên |

## 🛠️ Công nghệ sử dụng

| Công nghệ | Mô tả |
|-----------|-------|
| **Python 3.10+** | Ngôn ngữ lập trình chính |
| **PyQt6 6.4+** | Framework giao diện người dùng |
| **SQLAlchemy 2.0+** | ORM cho tương tác database |
| **SQLite 3.x** | Hệ quản trị cơ sở dữ liệu |
| **ReportLab 4.0+** | Thư viện xuất PDF |
| **Pandas 2.0+** | Thư viện xuất Excel |
| **bcrypt 4.0+** | Mã hóa mật khẩu |

## 📁 Cấu trúc project

```
baitaplon-python/
├── src/                     # Mã nguồn chính
│   ├── models/              # Database models
│   ├── services/            # Business logic
│   ├── gui/                 # Giao diện PyQt6
│   │   ├── views/           # Main views
│   │   ├── forms/           # Form dialogs
│   │   ├── dialogs/         # Reusable dialogs
│   │   ├── widgets/         # Reusable widgets
│   │   └── styles/          # QSS stylesheets
│   ├── database/            # Database connection
│   └── utils/               # Utilities (validators, formatters)
├── tests/                  # Unit tests
│   ├── test_models/         # Model tests
│   ├── test_services/       # Service tests
│   ├── test_utils/          # Utility tests
│   └── test_integration/    # Integration tests
├── data/                   # Database và logs
├── docs/                   # Tài liệu
├── scripts/                 # Scripts hỗ trợ
├── main.py                  # Entry point
├── requirements.txt         # Python dependencies
├── README.md               # Hướng dẫn tổng quan
├── SETUP.md                # Hướng dẫn cài đặt chi tiết
└── TASKS.md               # Danh sách công việc
```

## 🚀 Cài đặt

### Yêu cầu hệ thống
- Python 3.10 hoặc cao hơn
- SQLite 3.x
- RAM: 4GB trở lên
- Disk: 500MB trống

### Các bước cài đặt

1. **Clone repository:**
```bash
git clone <repository-url>
cd nhom12/baitaplon-python
```

2. **Tạo virtual environment:**
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. **Cài đặt dependencies:**
```bash
pip install -r requirements.txt
```

4. **Khởi tạo database:**
```bash
python src/data/init_db.py
```

5. **Chạy ứng dụng:**
```bash
python main.py
```

## 🎮 Hướng dẫn sử dụng

### Đăng nhập
- **Tài khoản mặc định:** `admin`
- **Mật khẩu mặc định:** `admin123`

### Phím tắt

| Phím tắt | Chức năng |
|----------|-----------|
| `Ctrl + D` | Mở Dashboard |
| `Ctrl + K` | Mở Quản lý Khách hàng |
| `Ctrl + O` | Mở Quản lý Kho hàng |
| `Ctrl + H` | Mở Quản lý Hợp đồng |
| `Ctrl + G` | Mở Quản lý Hàng hóa |
| `Ctrl + T` | Mở Quản lý Thanh toán |
| `Ctrl + B` | Mở Báo cáo |
| `Ctrl + Q` | Thoát ứng dụng |
| `Ctrl + S` | Lưu (trong form nhập liệu) |
| `Ctrl + N` | Tạo mới |
| `Ctrl + F` | Tìm kiếm |
| `Enter` | Xem chi tiết / Sửa |
| `Delete` | Xóa (sau khi chọn) |
| `Escape` | Đóng cửa sổ / Hủy |

### Quy trình nghiệp vụ

#### 1. Thêm Khách hàng mới
1. Vào **Khách hàng** → nhấn **+ Thêm Khách hàng**
2. Điền thông tin: Họ tên, SĐT, Email, Địa chỉ
3. Nhấn **Lưu**

#### 2. Tạo Hợp đồng thuê kho
1. Vào **Hợp đồng** → nhấn **+ Tạo Hợp đồng**
2. Chọn **Khách hàng** và **Vị trí** thuê
3. Điền thông tin: Ngày bắt đầu, Ngày kết thúc, Giá thuê
4. Nhấn **Lưu**

#### 3. Nhập Hàng hóa
1. Vào **Hàng hóa** → nhấn **+ Nhập Hàng**
2. Chọn **Kho** và **Vị trí** lưu trữ
3. Nhập thông tin hàng hóa
4. Nhấn **Lưu**

#### 4. Thanh toán
1. Vào **Thanh toán** → nhấn **+ Tạo Thanh toán**
2. Chọn **Hợp đồng** cần thanh toán
3. Nhập số tiền và ngày thanh toán
4. Nhấn **Lưu**

## 🧪 Testing

Chạy tất cả tests:
```bash
pytest tests/ -v
```

Chạy với coverage:
```bash
pytest tests/ --cov=src --cov-report=html
```

Chạy tests cho một module cụ thể:
```bash
pytest tests/test_services/ -v
```

## 📝 Changelog

Xem [CHANGELOG.md](./CHANGELOG.md) để biết chi tiết các thay đổi.

## 📄 License

Dự án này được phát triển cho mục đích học tập trong khuôn khổ môn **Lập trình Python**.

## 📞 Liên hệ

- **Email:** nhom12@example.edu.vn
- **GitHub:** https://github.com/your-repo

---

© 2024 Nhóm 12 - Lập trình Python. Mọi quyền được bảo lưu.
