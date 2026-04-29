# Changelog - Quản Lý Kho Lưu Trữ

Tất cả thay đổi quan trọng của dự án sẽ được ghi chép trong file này.

Format dựa trên [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [1.0.0] - 2026-04-29 - 🎉 Release đầu tiên

### Added
- **Quản lý Dashboard**
  - Tổng quan hệ thống với biểu đồ thống kê
  - Cảnh báo hợp đồng sắp hết hạn
  - Thống kê doanh thu theo tháng
  - Alerts cho tồn kho thấp và công nợ

- **Quản lý Khách hàng**
  - CRUD đầy đủ cho khách hàng
  - Phân loại: Cá nhân / Doanh nghiệp
  - Trạng thái: Hoạt động / Tạm khóa / Đã xóa
  - Tìm kiếm và lọc nâng cao
  - Lịch sử giao dịch

- **Quản lý Kho hàng**
  - CRUD đầy đủ cho kho
  - Theo dõi diện tích và sức chứa
  - Tính tỷ lệ lấp đầy tự động
  - Trạng thái: Hoạt động / Bảo trì / Ngừng

- **Quản lý Vị trí lưu trữ**
  - CRUD cho vị trí trong kho
  - Quản lý theo Khu vực, Hàng, Tầng
  - Trạng thái: Trống / Đã thuê / Bảo trì
  - Tính giá thuê theo vị trí

- **Quản lý Hợp đồng**
  - Tạo hợp đồng thuê kho
  - Gia hạn hợp đồng
  - Chấm dứt hợp đồng
  - Cảnh báo sắp hết hạn (30 ngày)
  - In hợp đồng ra PDF
  - Lịch sử hợp đồng

- **Quản lý Hàng hóa**
  - Nhập hàng vào kho
  - Xuất hàng từ kho
  - Theo dõi tồn kho theo thời gian thực
  - Cảnh báo tồn kho thấp
  - In phiếu nhập/xuất kho
  - Lịch sử xuất nhập hàng

- **Quản lý Thanh toán**
  - Theo dõi công nợ khách hàng
  - Cập nhật trạng thái thanh toán
  - Lịch sử thanh toán đầy đủ
  - In phiếu thanh toán

- **Báo cáo & Xuất file**
  - Xuất báo cáo PDF (hợp đồng, phiếu thanh toán, phiếu kho)
  - Xuất báo cáo Excel
  - Dashboard thống kê

- **Xác thực & Phân quyền**
  - Đăng nhập với tài khoản
  - Phân quyền: Admin / User
  - Session management (8 giờ timeout)
  - Remember me functionality
  - Activity log

- **Cài đặt**
  - Thông tin công ty
  - Cấu hình hệ thống
  - Quản lý người dùng
  - Sao lưu và phục hồi database

- **Trợ giúp**
  - Hướng dẫn sử dụng chi tiết
  - Danh sách phím tắt
  - Thông tin về ứng dụng

- **Testing**
  - Unit tests cho Models
  - Unit tests cho Services
  - Unit tests cho Validators
  - Unit tests cho Formatters
  - Integration tests cho Database operations

### Changed
- Refactor database models thành các file riêng biệt
- Tối ưu hóa cấu trúc project
- Cập nhật UI với PyQt6
- Sử dụng SQLAlchemy 2.0+ với async support đã sẵn sàng
- Tối ưu queries cho performance

### Fixed
- Bug liên quan đến enum values trong SQLAlchemy
- Bug khi khách hàng có hợp đồng đang hoạt động không thể xóa
- Bug cảnh báo hợp đồng sắp hết hạn
- Bug hiển thị ngày tháng

### Technical
- Python 3.10+
- PyQt6 6.4+
- SQLAlchemy 2.0+
- ReportLab 4.0+
- Pandas 2.0+

---

## [0.12.0] - 2026-04-23 - Phase 12: Help & Settings

### Added
- Help View với hướng dẫn sử dụng chi tiết
- Phím tắt trong Help View
- About dialog với thông tin nhóm phát triển
- Settings View với 4 tabs:
  - Thông tin công ty
  - Cấu hình hệ thống
  - Quản lý người dùng
  - Sao lưu & Phục hồi

---

## [0.11.0] - 2026-04-23 - Phase 11: Settings

### Added
- Settings View GUI hoàn chỉnh
- User Management trong Settings
- Backup/Restore functionality

---

## [0.9.0] - 2026-04-22 - Phase 9: Authentication

### Added
- Login View với form đăng nhập
- Auth Service với password hashing
- Authorization Service với role-based access
- Session management
- Auto-logout sau 8 giờ
- Remember me functionality

---

## [0.8.0] - 2026-04-21 - Phase 8: Reporting & PDF

### Added
- Report Service với dashboard statistics
- PDF Generation Service
- Dashboard Main View
- Summary report generation
- Export functions

---

## [0.7.0] - 2026-04-20 - Phase 7: Payment

### Added
- ThanhToan Model
- ThanhToanService
- ThanhToan View
- Payment form
- Payment tracking

---

## [0.6.0] - 2026-04-19 - Phase 6: Goods Management

### Added
- HangHoa Model
- HangHoaService
- HangHoa View
- Receipt/Purchase form
- Dispense form
- Goods tracking

---

## [0.5.0] - 2026-04-18 - Phase 5: Contract Management

### Added
- HopDong Model
- HopDongService
- HopDong View
- Contract form
- Renewal wizard
- Termination wizard

---

## [0.4.0] - 2026-04-17 - Phase 4: Warehouse Management

### Added
- Kho Model
- ViTri Model
- KhoService
- ViTriService
- Kho View
- ViTri View
- Position management

---

## [0.3.0] - 2026-04-16 - Phase 3: Customer Management

### Added
- KhachHang Model
- KhachHangService
- KhachHang View
- Customer form
- Customer detail view

---

## [0.2.0] - 2026-04-15 - Phase 2: Application Framework

### Added
- MainWindow với navigation
- Sidebar menu
- Base widgets (buttons, tables, search box)
- Loading widgets
- Dialog system
- Form dialogs
- Styling (QSS)
- Validators
- Formatters

---

## [0.1.0] - 2026-04-14 - Phase 1: Database & Core Setup

### Added
- Database models (KhachHang, Kho, ViTri, HopDong, HangHoa, ThanhToan, NhanVien)
- Database connection và session management
- Repository pattern
- Base model với common methods
- init_db.py script
- requirements.txt
- README.md
- SETUP.md
- TASKS.md

---

## [Unreleased] - Development

[Thêm các thay đổi chưa release ở đây]
