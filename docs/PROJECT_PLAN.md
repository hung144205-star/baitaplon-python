# 📋 KẾ HOẠCH TRIỂN KHAI PROJECT
## Quản Lý Dịch Vụ Cho Thuê Kho Lưu Trữ Hàng Hóa

**Nhóm 12 - Lập trình Python**  
**Phiên bản:** 1.0  
**Ngày:** 23/04/2026

---

## 🎯 TỔNG QUAN

### Mục tiêu
Xây dựng ứng dụng desktop hoàn chỉnh quản lý dịch vụ cho thuê kho lưu trữ hàng hóa với:
- Giao diện PyQt6 hiện đại, dễ sử dụng
- Database SQLite với SQLAlchemy ORM
- Đầy đủ CRUD operations cho các module
- Báo cáo PDF chuyên nghiệp
- Unit tests覆盖 các chức năng chính

### Tech Stack (từ TECH_STACK.md)

| Thành phần | Công nghệ | Phiên bản |
|------------|-----------|-----------|
| Ngôn ngữ | Python | 3.10+ |
| GUI Framework | PyQt6 | 6.4+ |
| Database | SQLite | 3.x |
| ORM | SQLAlchemy | 2.0+ |
| Báo cáo PDF | ReportLab | 3.6+ |
| Testing | pytest | 7.x+ |
| Code Format | black | 23.0+ |

---

## 📁 CẤU TRÚC PROJECT

```
baitaplon-python/
├── main.py                     # Entry point
├── requirements.txt            # Dependencies
├── README.md                   # Hướng dẫn
├── SETUP.md                    # Cài đặt
├── .gitignore
│
├── src/                        # Mã nguồn chính
│   ├── __init__.py
│   ├── app.py                  # QApplication chính
│   ├── main_window.py          # QMainWindow
│   │
│   ├── gui/                    # Giao diện PyQt6
│   │   ├── __init__.py
│   │   ├── widgets/            # Custom widgets
│   │   │   ├── __init__.py
│   │   │   ├── data_table.py   # Bảng dữ liệu
│   │   │   ├── search_box.py   # Tìm kiếm
│   │   │   └── buttons.py      # Button styles
│   │   │
│   │   ├── dialogs/            # Dialog windows
│   │   │   ├── __init__.py
│   │   │   ├── confirm_dialog.py
│   │   │   └── message_dialog.py
│   │   │
│   │   ├── forms/              # Form nhập liệu
│   │   │   ├── __init__.py
│   │   │   ├── khach_hang_form.py
│   │   │   ├── kho_form.py
│   │   │   ├── hop_dong_form.py
│   │   │   └── thanh_toan_form.py
│   │   │
│   │   └── views/              # Các màn hình chính
│   │       ├── __init__.py
│   │       ├── dashboard_view.py
│   │       ├── khach_hang_view.py
│   │       ├── kho_view.py
│   │       ├── hop_dong_view.py
│   │       ├── hang_hoa_view.py
│   │       ├── thanh_toan_view.py
│   │       └── bao_cao_view.py
│   │
│   ├── models/                 # Database models (SQLAlchemy)
│   │   ├── __init__.py
│   │   ├── khach_hang.py
│   │   ├── kho.py
│   │   ├── vi_tri.py
│   │   ├── hop_dong.py
│   │   ├── hang_hoa.py
│   │   ├── thanh_toan.py
│   │   ├── nhan_vien.py
│   │   └── base.py
│   │
│   ├── services/               # Business logic
│   │   ├── __init__.py
│   │   ├── khach_hang_service.py
│   │   ├── kho_service.py
│   │   ├── hop_dong_service.py
│   │   ├── hang_hoa_service.py
│   │   ├── thanh_toan_service.py
│   │   ├── auth_service.py
│   │   └── bao_cao_service.py
│   │
│   ├── database/               # Database connection (refactor từ data/)
│   │   ├── __init__.py
│   │   ├── connection.py       # SQLAlchemy engine/session
│   │   └── init_db.py          # Khởi tạo database
│   │
│   └── utils/                  # Tiện ích
│       ├── __init__.py
│       ├── validators.py       # Validate dữ liệu
│       ├── formatters.py       # Format số, ngày tháng
│       ├── pdf_generator.py    # Tạo PDF báo cáo
│       └── helpers.py          # Helper functions
│
├── data/                       # Dữ liệu ứng dụng
│   ├── warehouse.db            # File SQLite
│   ├── backups/                # Backup database
│   └── README.md
│
├── docs/                       # Tài liệu
│   ├── DATABASE_ANALYSIS.md
│   ├── TECH_STACK.md
│   ├── SPEC.md
│   ├── YEU_CAU_CHUC_NANG.md
│   ├── PROJECT_PLAN.md         # File này
│   └── ...
│
├── stitch_ui_analysis_system/  # UI templates tham khảo
│   └── ...
│
├── tests/                      # Unit tests
│   ├── __init__.py
│   ├── conftest.py             # pytest fixtures
│   ├── test_models/
│   │   ├── __init__.py
│   │   ├── test_khach_hang.py
│   │   └── test_hop_dong.py
│   │
│   ├── test_services/
│   │   ├── __init__.py
│   │   ├── test_khach_hang_service.py
│   │   └── test_hop_dong_service.py
│   │
│   └── test_utils/
│       ├── __init__.py
│       ├── test_validators.py
│       └── test_formatters.py
│
└── logs/                       # Logs
    └── ...
```

---

## 📅 LỘ TRÌNH TRIỂN KHAI (5 TUẦN)

### Tuần 1: Setup & Database (23/04 - 30/04)

#### ✅ Đã hoàn thành:
- [x] Cập nhật requirements.txt
- [x] Tạo DATABASE_ANALYSIS.md
- [x] Tạo database với SQLAlchemy
- [x] Tạo schema.sql
- [x] Script init_db.py
- [x] Fix lỗi SQLAlchemy 2.0 compatibility

#### 🔄 Đang làm:
- [ ] Refactor models thành từng file riêng
- [ ] Tạo base model class

#### 📋 Còn lại:
- [ ] Tạo database connection module
- [ ] Viết unit tests cho models
- [ ] Documentation cho database layer

**Deliverables:**
- ✅ Database hoạt động ổn định
- ✅ 9 models SQLAlchemy
- ✅ Sample data
- 📝 Unit tests cơ bản

---

### Tuần 2: GUI Framework & Khách hàng (01/05 - 07/05)

#### Mục tiêu:
- Setup PyQt6 application framework
- Implement CRUD Khách hàng hoàn chỉnh

#### Tasks:

**2.1. Application Framework**
- [ ] Tạo `src/app.py` - QApplication chính
- [ ] Tạo `src/main_window.py` - MainWindow với menu, toolbar
- [ ] Tạo `src/gui/widgets/` - Custom widgets cơ bản
  - [ ] DataTable widget (QTableWidget wrapper)
  - [ ] SearchBox widget
  - [ ] Styled buttons
- [ ] Tạo `src/gui/dialogs/` - Dialog chung
  - [ ] ConfirmDialog
  - [ ] MessageDialog
- [ ] Setup QStackedWidget cho navigation

**2.2. Module Khách hàng**
- [ ] Tạo `src/models/khach_hang.py`
- [ ] Tạo `src/services/khach_hang_service.py`
  - [ ] create()
  - [ ] read() / get_all() / search()
  - [ ] update()
  - [ ] delete()
- [ ] Tạo `src/gui/forms/khach_hang_form.py`
- [ ] Tạo `src/gui/views/khach_hang_view.py`
  - [ ] Danh sách khách hàng (table)
  - [ ] Form thêm/sửa
  - [ ] Tìm kiếm, lọc
  - [ ] Xóa với confirm
- [ ] Reference UI: `stitch_ui_analysis_system/ho_so_khach_hang/`

**2.3. Testing**
- [ ] Test services layer
- [ ] Test form validation
- [ ] Manual test GUI

**Deliverables:**
- ✅ Application chạy được với MainWindow
- ✅ Module Khách hàng hoàn chỉnh (CRUD)
- ✅ Navigation giữa các màn hình
- 📝 Unit tests cho KhachHang service

---

### Tuần 3: Kho & Vị trí (08/05 - 14/05)

#### Mục tiêu:
- Implement CRUD Kho hàng
- Implement CRUD Vị trí lưu trữ
- Hiển thị tỷ lệ lấp đầy

#### Tasks:

**3.1. Module Kho**
- [ ] Tạo `src/models/kho.py`
- [ ] Tạo `src/services/kho_service.py`
  - [ ] CRUD operations
  - [ ] calculate_fill_rate()
- [ ] Tạo `src/gui/forms/kho_form.py`
- [ ] Tạo `src/gui/views/kho_view.py`
  - [ ] Danh sách kho
  - [ ] Chi tiết kho
  - [ ] Form thêm/sửa
- [ ] Reference UI: `stitch_ui_analysis_system/danh_sach_kho/`

**3.2. Module Vị trí**
- [ ] Tạo `src/models/vi_tri.py`
- [ ] Tạo `src/services/vi_tri_service.py`
  - [ ] CRUD operations
  - [ ] find_available()
- [ ] Tạo `src/gui/forms/vi_tri_form.py`
- [ ] Tạo `src/gui/views/vi_tri_view.py`
  - [ ] Danh sách vị trí theo kho
  - [ ] Form thêm/sửa
  - [ ] Hiển thị trạng thái (trống/đã thuê)
- [ ] Reference UI: `stitch_ui_analysis_system/chi_tiet_kho/`

**3.3. Dashboard**
- [ ] Tạo `src/gui/views/dashboard_view.py`
  - [ ] Thống kê tổng quan
  - [ ] Tỷ lệ lấp đầy các kho
  - [ ] Hợp đồng sắp hết hạn
  - [ ] Công nợ nổi bật

**3.4. Testing**
- [ ] Test Kho service
- [ ] Test ViTri service
- [ ] Test dashboard calculations

**Deliverables:**
- ✅ Module Kho hoàn chỉnh
- ✅ Module Vị trí hoàn chỉnh
- ✅ Dashboard hiển thị thống kê
- 📝 Unit tests

---

### Tuần 4: Hợp đồng & Hàng hóa (15/05 - 21/05)

#### Mục tiêu:
- Implement CRUD Hợp đồng thuê
- Implement CRUD Hàng hóa
- Link hợp đồng với vị trí & khách hàng

#### Tasks:

**4.1. Module Hợp đồng**
- [ ] Tạo `src/models/hop_dong.py`
- [ ] Tạo `src/services/hop_dong_service.py`
  - [ ] CRUD operations
  - [ ] create_contract() - tự động tạo mã
  - [ ] renew_contract()
  - [ ] terminate_contract()
  - [ ] get_expiring_soon()
- [ ] Tạo `src/gui/forms/hop_dong_form.py`
  - [ ] Chọn khách hàng (dropdown)
  - [ ] Chọn vị trí (dropdown, filter theo trạng thái)
  - [ ] Tính toán giá thuê
  - [ ] Ngày bắt đầu/kết thúc
- [ ] Tạo `src/gui/views/hop_dong_view.py`
  - [ ] Danh sách hợp đồng
  - [ ] Chi tiết hợp đồng
  - [ ] Filter theo trạng thái
  - [ ] Cảnh báo hợp đồng sắp hết hạn
- [ ] Reference UI: `stitch_ui_analysis_system/danh_muc_hop_dong/`, `thiet_lap_hop_dong/`

**4.2. Module Hàng hóa**
- [ ] Tạo `src/models/hang_hoa.py`
- [ ] Tạo `src/services/hang_hoa_service.py`
  - [ ] CRUD operations
  - [ ] import_goods() - nhập kho
  - [ ] export_goods() - xuất kho
  - [ ] get_inventory() - tồn kho
- [ ] Tạo `src/gui/forms/hang_hoa_form.py`
  - [ ] Form nhập liệu hàng hóa
  - [ ] Upload hình ảnh (optional)
- [ ] Tạo `src/gui/views/hang_hoa_view.py`
  - [ ] Danh sách hàng theo hợp đồng
  - [ ] Tìm kiếm hàng hóa
  - [ ] Thống kê tồn kho
- [ ] Reference UI: `stitch_ui_analysis_system/danh_muc_hang_hoa/`

**4.3. Phiếu nhập/xuất**
- [ ] Tạo `src/gui/forms/phieu_nhap_form.py`
- [ ] Tạo `src/gui/forms/phieu_xuat_form.py`
- [ ] Reference UI: `stitch_ui_analysis_system/phieu_nhap_kho/`, `phieu_xuat_kho/`

**4.4. Testing**
- [ ] Test HopDong service
- [ ] Test HangHoa service
- [ ] Test contract renewal logic
- [ ] Test inventory calculations

**Deliverables:**
- ✅ Module Hợp đồng hoàn chỉnh
- ✅ Module Hàng hóa hoàn chỉnh
- ✅ Phiếu nhập/xuất
- 📝 Unit tests

---

### Tuần 5: Thanh toán, Báo cáo & Hoàn thiện (22/05 - 28/05)

#### Mục tiêu:
- Implement Thanh toán & Hóa đơn
- Xuất báo cáo PDF
- Authentication & Authorization
- Testing & Polish

#### Tasks:

**5.1. Module Thanh toán**
- [ ] Tạo `src/models/thanh_toan.py`
- [ ] Tạo `src/services/thanh_toan_service.py`
  - [ ] CRUD operations
  - [ ] create_invoice() - tạo hóa đơn
  - [ ] record_payment() - ghi nhận thanh toán
  - [ ] calculate_late_fee() - tính phí phạt
  - [ ] get_overdue() - công nợ quá hạn
- [ ] Tạo `src/gui/forms/thanh_toan_form.py`
  - [ ] Form thanh toán
  - [ ] Chọn phương thức
  - [ ] In hóa đơn
- [ ] Tạo `src/gui/views/thanh_toan_view.py`
  - [ ] Danh sách hóa đơn
  - [ ] Công nợ chưa thanh toán
  - [ ] Lịch sử thanh toán theo hợp đồng
- [ ] Reference UI: `stitch_ui_analysis_system/danh_muc_hoa_don/`, `chi_tiet_hoa_don/`

**5.2. Báo cáo & PDF**
- [ ] Tạo `src/utils/pdf_generator.py`
  - [ ] generate_invoice_pdf()
  - [ ] generate_contract_pdf()
  - [ ] generate_report_pdf()
- [ ] Tạo `src/services/bao_cao_service.py`
  - [ ] generate_revenue_report()
  - [ ] generate_fill_rate_report()
  - [ ] generate_debt_report()
- [ ] Tạo `src/gui/views/bao_cao_view.py`
  - [ ] Chọn loại báo cáo
  - [ ] Chọn kỳ báo cáo
  - [ ] Xem trước
  - [ ] Xuất PDF
- [ ] Reference UI: `stitch_ui_analysis_system/bao_cao_trang_thai/`

**5.3. Authentication**
- [ ] Tạo `src/services/auth_service.py`
  - [ ] login()
  - [ ] logout()
  - [ ] check_permission()
- [ ] Tạo `src/gui/views/login_view.py`
  - [ ] Form đăng nhập
  - [ ] Remember me
- [ ] Phân quyền theo vai trò trong UI
  - [ ] Show/hide menu items theo role
  - [ ] Disable buttons không có quyền

**5.4. Testing & Polish**
- [ ] Viết unit tests cho remaining services
- [ ] Integration tests
- [ ] Fix bugs
- [ ] UI polish (styles, icons)
- [ ] Performance optimization
- [ ] User documentation

**5.5. Documentation**
- [ ] README.md hoàn chỉnh
- [ ] User manual
- [ ] API documentation
- [ ] Deployment guide

**Deliverables:**
- ✅ Module Thanh toán hoàn chỉnh
- ✅ Xuất báo cáo PDF
- ✅ Authentication & Authorization
- ✅ Unit tests > 80% coverage
- ✅ Documentation đầy đủ

---

## 📊 PHÂN CÔNG CÔNG VIỆC

| Thành viên | Vai trò | Responsibilities |
|------------|---------|------------------|
| **Đoàn Mạnh Hùng** (Trưởng nhóm) | Full-stack | Architecture, Database, Core modules (HopDong, Kho) |
| **Lương Hán Hải** | Backend + Database | Models, Services, Testing |
| **Nguyễn Đồng Thanh** | Frontend (PyQt6) | GUI, Forms, Views, Styling |

---

## 🎯 TIÊU CHÍ HOÀN THÀNH (DoD)

### Cho mỗi module:
- [ ] Model SQLAlchemy với đầy đủ fields
- [ ] Service layer với CRUD + business logic
- [ ] GUI View với table + form
- [ ] Validation đầy đủ
- [ ] Error handling
- [ ] Unit tests (> 80% coverage)
- [ ] Documentation

### Cho toàn project:
- [ ] Tất cả modules hoạt động ổn định
- [ ] Navigation giữa các màn hình mượt mà
- [ ] Database migrations working
- [ ] PDF reports generated correctly
- [ ] Authentication working
- [ ] No critical bugs
- [ ] User documentation complete
- [ ] Code formatted with black
- [ ] All tests passing

---

## 🔧 CÔNG CỤ & QUY TRÌNH

### Development Workflow
```bash
# 1. Tạo branch mới cho feature
git checkout -b feature/ten-feature

# 2. Code & commit
git add .
git commit -m "feat: implement khach hang CRUD"

# 3. Chạy tests
pytest tests/ -v

# 4. Format code
black src/ tests/

# 5. Push & tạo PR
git push origin feature/ten-feature
```

### Testing
```bash
# Chạy tất cả tests
pytest tests/ -v

# Chạy với coverage
pytest tests/ --cov=src --cov-report=html

# Chạy specific test
pytest tests/test_services/test_khach_hang_service.py -v
```

### Code Quality
```bash
# Format code
black src/ tests/

# Check style
flake8 src/ tests/

# Type checking (nếu dùng mypy)
mypy src/
```

---

## 📈 THEO DÕI TIẾN ĐỘ

### Tuần 1 (23/04 - 30/04)
- **Mục tiêu:** Database hoàn chỉnh
- **Progress:** ██████████░░ 80%
- **Status:** ✅ On track

### Tuần 2 (01/05 - 07/05)
- **Mục tiêu:** GUI Framework + Khách hàng
- **Progress:** ░░░░░░░░░░ 0%
- **Status:** ⏳ Pending

### Tuần 3 (08/05 - 14/05)
- **Mục tiêu:** Kho & Vị trí
- **Progress:** ░░░░░░░░░░ 0%
- **Status:** ⏳ Pending

### Tuần 4 (15/05 - 21/05)
- **Mục tiêu:** Hợp đồng & Hàng hóa
- **Progress:** ░░░░░░░░░░ 0%
- **Status:** ⏳ Pending

### Tuần 5 (22/05 - 28/05)
- **Mục tiêu:** Thanh toán, Báo cáo, Hoàn thiện
- **Progress:** ░░░░░░░░░░ 0%
- **Status:** ⏳ Pending

---

## 🚨 RỦI RO & GIẢI PHÁP

| Rủi ro | Impact | Likelihood | Mitigation |
|--------|--------|------------|------------|
| PyQt6 learning curve | Cao | Cao | Dành thời gian study docs, tham khảo UI templates |
| SQLAlchemy 2.0 changes | Trung bình | Trung bình | Đọc kỹ docs, đã fix compatibility issues |
| Timeline quá chặt | Cao | Trung bình | Ưu tiên core features, cắt giảm nice-to-have |
| Bug integration | Trung bình | Cao | Viết tests sớm, integration test thường xuyên |
| Scope creep | Cao | Trung bình | Stick to requirements, không thêm feature ngoài scope |

---

## 📝 GHI CHÚ

### Ưu tiên implement:
1. **Core:** KhachHang, Kho, ViTri, HopDong
2. **Business:** HangHoa, ThanhToan
3. **Reporting:** BaoCao, PDF export
4. **Nice-to-have:** Dashboard charts, advanced search

### Tham khảo UI templates:
- Tất cả 17 screens trong `stitch_ui_analysis_system/`
- Ưu tiên screens liên quan đến module đang implement

### Database:
- File: `data/warehouse.db`
- Models: `src/models/`
- Services: `src/services/`
- Sample data: admin/admin123

---

## ✅ CHECKLIST KHỞI ĐỘNG

- [x] Database design hoàn chỉnh
- [x] Database implementation working
- [x] Requirements.txt updated
- [x] Project structure created
- [x] UI templates analyzed
- [ ] Models refactor (tách thành file riêng)
- [ ] First feature branch created
- [ ] CI/CD setup (optional)

---

**Let's build something amazing! 🚀**


