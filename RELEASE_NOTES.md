# Release Notes - Version 1.0.0 🎉

**Ngày phát hành:** 29/04/2026  
**Nhóm phát triển:** Nhóm 12 - Lập trình Python

---

## 🎉 Thông báo Release

Đây là phiên bản **1.0.0** - phiên bản đầu tiên hoàn chỉnh của phần mềm **Quản Lý Kho Lưu Trữ Hàng Hóa**!

## ✨ Tính năng nổi bật

### 📊 Dashboard toàn diện
- Biểu đồ thống kê doanh thu, khách hàng, kho hàng
- Cảnh báo thông minh (hợp đồng hết hạn, tồn kho thấp, công nợ)
- Tổng quan hoạt động kinh doanh

### 👥 Quản lý Khách hàng
- Hệ thống khách hàng đầy đủ (CRUD)
- Phân loại: Cá nhân / Doanh nghiệp
- Lịch sử giao dịch chi tiết

### 🏭 Quản lý Kho & Vị trí
- Quản lý nhiều kho với thông tin chi tiết
- Vị trí lưu trữ thông minh (Khu vực, Hàng, Tầng)
- Theo dõi tỷ lệ lấp đầy tự động

### 📄 Quản lý Hợp đồng
- Tạo, gia hạn, chấm dứt hợp đồng
- In hợp đồng ra PDF
- Cảnh báo sắp hết hạn

### 📦 Quản lý Hàng hóa
- Nhập/Xuất hàng hóa
- Theo dõi tồn kho thời gian thực
- In phiếu nhập/xuất kho

### 💰 Quản lý Thanh toán
- Theo dõi công nợ
- Cập nhật trạng thái thanh toán
- In phiếu thanh toán

### 🔐 Bảo mật
- Đăng nhập với tài khoản
- Phân quyền Admin/User
- Session management 8 giờ
- Activity log

### ⚙️ Tiện ích
- Xuất báo cáo PDF
- Xuất báo cáo Excel
- Sao lưu/Phục hồi database
- Hướng dẫn sử dụng chi tiết

## 📋 Yêu cầu hệ thống

| Thành phần | Yêu cầu |
|------------|---------|
| Python | 3.10+ |
| RAM | 4GB+ |
| Disk | 500MB+ |
| OS | Windows / macOS / Linux |

## 🚀 Hướng dẫn cài đặt nhanh

```bash
# 1. Clone repository
git clone <url>
cd nhom12/baitaplon-python

# 2. Tạo virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 3. Cài đặt dependencies
pip install -r requirements.txt

# 4. Khởi tạo database
python src/data/init_db.py

# 5. Chạy ứng dụng
python main.py
```

## 🔑 Tài khoản mặc định

| Tài khoản | Mật khẩu | Quyền |
|-----------|----------|-------|
| admin | admin123 | Full Access |

## 🧪 Testing

```bash
# Chạy tất cả tests
pytest tests/ -v

# Chạy với coverage report
pytest tests/ --cov=src --cov-report=html
```

## 📝 Known Issues

Không có known issues trong phiên bản này.

## 🐛 Báo lỗi

Nếu phát hiện lỗi, vui lòng báo cáo qua:
- Email: nhom12@example.edu.vn
- GitHub Issues

## 📄 License

Dự án được phát triển cho mục đích học tập.

---

**Cảm ơn các thầy/cô và các bạn đã quan tâm đến dự án của Nhóm 12!** 🙏

---

_Ngày phát hành: 29/04/2026_  
_Nhóm 12 - Lập trình Python_
