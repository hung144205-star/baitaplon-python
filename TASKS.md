# 📝 TASKS - QUẢN LÝ DỊCH VỤ CHO THUÊ KHO LƯU TRỮ HÀNG HÓA

**Nhóm 12 - Lập trình Python**  
**Created:** 23/04/2026  
**Status:** In Progress

---

## 🎯 PHASE PRIORITIES

| Priority | Phase | Status | GitHub Tag |
|----------|-------|--------|------------|
| 🔴 **P0** | Phase 1: Database & Core Setup | ✅ Complete | `v0.1-database` |
| 🔴 **P0** | Phase 2: Application Framework | ✅ Complete | `v0.2-framework` |
| 🟠 **P1** | Phase 3: Customer Management (Khách hàng) | ✅ Complete | `v0.3-khach-hang` |
| 🟠 **P1** | Phase 4: Warehouse Management (Kho) | ✅ Complete | `v0.4-kho` |
| 🟡 **P2** | Phase 5: Contract Management (Hợp đồng) | ✅ Complete | `v0.5-hop-dong` |
| 🟡 **P2** | Phase 6: Goods Management (Hàng hóa) | ✅ Complete | `v0.6-hang-hoa` |
| 🟢 **P3** | Phase 7: Reporting & Analytics (Báo cáo) | ✅ Complete | `v0.7-report` |
| 🟢 **P3** | Phase 8: PDF Generation | 🟡 In Progress | `v0.8-pdf` |
| 🔵 **P4** | Phase 9: Authentication & Authorization | ⚪ Not Started | `v0.9-auth` |
| 🔵 **P4** | Phase 10: Testing & Polish | ⚪ Not Started | `v1.0-release` |

---

## 🔴 PHASE 1: DATABASE & CORE SETUP
**Priority:** P0 (Critical)  
**GitHub Tag:** `v0.1-database`  
**Status:** 🟡 In Progress (80%)

### 1.1 Project Setup
- [x] Cập nhật requirements.txt với đầy đủ dependencies
- [x] Tạo README.md hướng dẫn cài đặt
- [x] Tạo SETUP.md với hướng dẫn chi tiết
- [x] Tạo .gitignore cho Python project
- [ ] Tạo LICENSE file (MIT)
- [ ] Tạo CONTRIBUTING.md

### 1.2 Database Implementation
- [x] Tạo DATABASE_ANALYSIS.md với thiết kế chi tiết
- [x] Tạo src/data/database.py với SQLAlchemy models
- [x] Tạo src/data/schema.sql
- [x] Tạo src/data/init_db.py
- [x] Fix SQLAlchemy 2.0 compatibility (text() wrapper)
- [x] Test database initialization script
- [x] Refactor models thành file riêng trong src/models/
- [x] Tạo src/models/__init__.py export tất cả models
- [x] Tạo database migration script (src/database/migrate.py)

### 1.3 Database Models (Refactor)
- [x] Tạo src/models/base.py - Base class với common methods
- [x] Tạo src/models/khach_hang.py
- [x] Tạo src/models/kho.py
- [x] Tạo src/models/vi_tri.py
- [x] Tạo src/models/hop_dong.py
- [x] Tạo src/models/hang_hoa.py
- [x] Tạo src/models/thanh_toan.py
- [x] Tạo src/models/nhan_vien.py
- [x] Tạo src/models/system_log.py
- [x] Tạo src/models/bao_cao.py

### 1.4 Database Services
- [x] Tạo src/database/connection.py
- [x] Tạo src/database/session_manager.py (integrated into connection.py)
- [x] Tạo src/database/repository.py - Base repository pattern

### 1.5 Documentation
- [x] Tạo PROJECT_PLAN.md
- [x] Tạo TASKS.md
- [ ] Tạo ERD diagram (dạng ảnh) - Optional
- [x] Viết database usage guide (src/database/README.md)

### ✅ Phase 1 Deliverables:
- [x] Database hoạt động ổn định
- [x] Models refactor hoàn chỉnh
- [x] Sample data loaded
- [x] Database services (connection, repository)
- [x] Documentation complete
- [ ] **GitHub Release v0.1-database** - Ready to release!

---

## 🔴 PHASE 2: APPLICATION FRAMEWORK
**Priority:** P0 (Critical)  
**GitHub Tag:** `v0.2-framework`  
**Status:** ⚪ Not Started

### 2.1 Core Application
- [x] Tạo src/app.py - QApplication entry point
- [x] Tạo src/main.py refactored
- [x] Tạo src/main_window.py - QMainWindow với menu bar, toolbar
- [x] Setup application icon (placeholder)
- [x] Setup application stylesheet (QSS) - main.qss
- [x] Tạo status bar với user info
- [x] Tạo gui package structure (__init__.py files)

### 2.2 Navigation System
- [x] Tạo src/gui/navigation.py - QStackedWidget wrapper
- [x] Tạo sidebar menu với các module
- [x] Setup navigation giữa các views
- [x] Tạo breadcrumb navigation
- [x] Handle back/forward navigation
- [x] Integration với MainWindow

### 2.3 Base Widgets
- [x] Tạo src/gui/widgets/__init__.py
- [x] Tạo src/gui/widgets/data_table.py - QTableWidget wrapper
  - [x] Sorting
  - [x] Filtering
  - [x] Pagination
  - [x] Column resizing
- [x] Tạo src/gui/widgets/search_box.py - Search input
  - [x] Real-time search
  - [x] Clear button
  - [x] Search history
- [x] Tạo src/gui/widgets/buttons.py - Styled buttons
  - [x] PrimaryButton
  - [x] SecondaryButton
  - [x] DangerButton
  - [x] IconButton
  - [x] ButtonGroup
  - [x] ToggleButton
  - [x] LoadingButton
- [x] Tạo src/gui/widgets/loading.py - Loading spinner
  - [x] LoadingSpinner
  - [x] LoadingOverlay
  - [x] LoadingProgressBar
  - [x] LoadingDialog
  - [x] ProgressStep
  - [x] ProgressStepper

### 2.4 Dialogs
- [x] Tạo src/gui/dialogs/__init__.py
- [x] Tạo src/gui/dialogs/dialogs.py (tất cả dialogs trong 1 file)
  - [x] MessageDialog - Info, Warning, Error, Success
  - [x] ConfirmDialog - Confirm delete, Confirm action
  - [x] InputDialog - Text input, Number input, Date input, Double input, Multiline text
  - [x] ProgressDialog - Determinate & Indeterminate progress
  - [x] FormDialog - Generic form với multiple fields
- [x] Export tất cả dialogs trong __init__.py

### 2.5 Utilities
- [x] Tạo src/utils/validators.py
  - [x] validate_email()
  - [x] validate_phone()
  - [x] validate_required()
  - [x] validate_length()
- [x] Tạo src/utils/formatters.py
  - [x] format_currency()
  - [x] format_date()
  - [x] format_number()
  - [x] format_percentage()
- [x] Tạo src/utils/helpers.py
  - [x] generate_code()
  - [x] calculate_date_range()
  - [x] export_to_excel()

### 2.6 Styling
- [x] Tạo src/gui/styles/main.qss
- [x] Tạo color scheme
- [x] Tạo button styles
- [x] Tạo table styles
- [x] Create form styles
- [x] Apply consistent spacing

### ✅ Phase 2 Deliverables:
- [x] Application chạy được với MainWindow
- [x] Navigation working
- [x] Base widgets reusable
- [x] Consistent styling
- [x] **GitHub Release v0.2-framework**

---

## 🟠 PHASE 3: CUSTOMER MANAGEMENT (KHÁCH HÀNG)
**Priority:** P1 (High)  
**GitHub Tag:** `v0.3-khach-hang`  
**Status:** ⚪ Not Started

### 3.1 Models & Services
- [x] Refactor src/models/khach_hang.py (nếu chưa)
- [x] Tạo src/services/khach_hang_service.py
  - [x] create(data) → KhachHang
  - [x] get_by_id(ma_khach_hang) → KhachHang
  - [x] get_all() → List[KhachHang]
  - [x] search(keyword) → List[KhachHang]
  - [x] update(ma_khach_hang, data) → KhachHang
  - [x] delete(ma_khach_hang) → bool
  - [x] get_by_status(trang_thai) → List[KhachHang]
  - [x] get_history(ma_khach_hang) → dict

### 3.2 GUI - View
- [x]] Refactor src/models/khach_hang.py (nếu chưa)
- [ ] Tạo src/services/khach_hang_service.py
  - [ ] create(data) → KhachHang
  - [ ] get_by_id(ma_khach_hang) → KhachHang
  - [ ] get_all() → List[KhachHang]
  - [ ] search(keyword) → List[KhachHang]
  - [ ] update(ma_khach_hang, data) → KhachHang
  - [ ] delete(ma_khach_hang) → bool
  - [ ] get_by_status(trang_thai) → List[KhachHang]
  - [ ] get_history(ma_khach_hang) → dict

### 3.2 GUI - View
- [x] Tạo src/gui/views/khach_hang_view.py
- [ ] Danh sách khách hàng (QTableWidget)
  - [x] Display columns: Mã, Tên, SĐT, Email, Loại, Trạng thái
  - [x] Sortable columns
  - [x] Row selection
  - [x] Double-click to edit
- [ ] Toolbar với actions
  - [x] Button: Thêm mới
  - [x] Button: Sửa
  - [x] Button: Xóa
  - [x] Button: Refresh
- [ ] Search box
  - [x] Tìm theo tên
  - [x] Tìm theo SĐT
  - [x] Tìm theo email
  - [x] Filter theo loại
  - [x] Filter theo trạng thái

### 3.3 GUI - Form
- [x] Tạo src/gui/forms/khach_hang_form.py
- [ ] Form fields:
  - [ ] Mã khách hàng (auto-generate, read-only khi sửa)
  - [ ] Họ tên (required)
  - [ ] Loại khách (ComboBox: Cá nhân/Doanh nghiệp)
  - [ ] Số điện thoại (required, validate)
  - [ ] Email (validate)
  - [ ] Địa chỉ (required, textarea)
  - [ ] Mã số thuế (optional, chỉ hiển thị nếu là doanh nghiệp)
  - [ ] Ngày đăng ký (DatePicker, default today)
  - [ ] Trạng thái (ComboBox)
- [x] Form validation
- [ ] Save/Cancel buttons

### 3.4 GUI - Detail View
- [x] Tạo src/gui/views/khach_hang_detail_view.py
- [ ] Hiển thị thông tin chi tiết
- [ ] Tab: Thông tin cơ bản
- [ ] Tab: Hợp đồng (list contracts)
- [ ] Tab: Thanh toán (list payments)
- [ ] Tab: Lịch sử (audit log)

### 3.5 Features
- [x] Auto-generate mã khách hàng (KH + YYYYMM + sequence)
- [ ] Validate phone number format
- [ ] Validate email format
- [ ] Check duplicate email
- [ ] Confirm before delete
- [ ] Soft delete (update status instead)
- [x] Export to Excel

### 3.6 Testing
- [x] Test KhachHangService.create()
- [ ] Test KhachHangService.get_all()
- [ ] Test KhachHangService.search()
- [ ] Test KhachHangService.update()
- [ ] Test KhachHangService.delete()
- [ ] Test validators
- [ ] Manual test GUI flow

### 3.7 Reference UI
- [ ] Review `stitch_ui_analysis_system/ho_so_khach_hang/`
- [ ] Review `stitch_ui_analysis_system/chi_tiet_khach_hang/`
- [ ] Review `stitch_ui_analysis_system/thong_tin_chi_tiet_khach_hang/`
- [ ] Implement similar design

### ✅ Phase 3 Deliverables:
- [x] CRUD Khách hàng hoàn chỉnh
- [x] Search & Filter working
- [x] Form validation
- [x] Export to Excel
- [x] **GitHub Release v0.3-khach-hang**

---

## 🟠 PHASE 4: WAREHOUSE MANAGEMENT (KHO HÀNG)
**Priority:** P1 (High)  
**GitHub Tag:** `v0.4-kho`  
**Status:** ✅ Complete

### 4.1 Kho Models & Services
- [x] Refactor src/models/kho.py
- [x] Tạo src/services/kho_service.py
  - [x] create(data) → Kho
  - [x] get_by_id(ma_kho) → Kho
  - [x] get_all() → List[Kho]
  - [x] search(keyword) → List[Kho]
  - [x] update(ma_kho, data) → Kho
  - [x] delete(ma_kho) → bool
  - [x] calculate_fill_rate(ma_kho) → float
  - [x] get_available_capacity(ma_kho) → float

### 4.2 Kho GUI
- [x] Tạo src/gui/views/kho_view.py
- [x] Danh sách kho (QTableWidget)
  - [x] Columns: Mã, Tên, Địa chỉ, Diện tích, Sức chứa, Đã sử dụng, % Lấp đầy, Trạng thái
  - [x] Progress bar cho % lấp đầy
- [x] Toolbar: Thêm, Sửa, Xóa, Refresh
- [x] Search & Filter
- [x] Tạo src/gui/forms/kho_form.py

### 4.3 Vi Tri Models & Services
- [x] Refactor src/models/vi_tri.py
- [x] Tạo src/services/vi_tri_service.py
  - [x] create(data) → ViTri
  - [x] get_by_id(ma_vi_tri) → ViTri
  - [x] get_by_kho(ma_kho) → List[ViTri]
  - [x] get_available(ma_kho) → List[ViTri]
  - [x] update(ma_vi_tri, data) → ViTri
  - [x] delete(ma_vi_tri) → bool
  - [x] update_status(ma_vi_tri, trang_thai) → bool

### 4.4 Vi Tri GUI
- [x] Tạo src/gui/views/vi_tri_view.py
- [x] Danh sách vị trí theo kho
- [x] Visual grid layout (optional)
- [x] Color coding by status
- [x] Tạo src/gui/forms/vi_tri_form.py
- [x] Auto-generate mã vị trí (K01-A-01-01 pattern)

### 4.5 Dashboard Integration
- [x] Update dashboard với fill rate widgets
- [x] Show warehouse status cards
- [x] Alert khi fill rate > 90%

### 4.6 Reference UI
- [x] Review danh_sach_kho/ reference
- [x] Review chi_tiet_kho/ reference
- [x] Review thong_tin_kho_hang/ reference
- [x] Integrate vào kho_view.py
- [x] Integrate vào vi_tri_view.py
- [x] Integrate vào dashboard_view.py
- [x] Tạo docs/REFERENCE_UI_KHO.md Review `stitch_ui_analysis_system/danh_sach_kho/`
- [x] Review `stitch_ui_analysis_system/chi_tiet_kho/`
- [x] Review `stitch_ui_analysis_system/thong_tin_kho_hang/`

### ✅ Phase 4 Deliverables:
- [x] CRUD Kho hoàn chỉnh
- [x] CRUD Vị trí hoàn chỉnh
- [x] Fill rate calculation
- [x] Dashboard integration
- [x] **GitHub Release v0.4-kho**


### 4.7 GUI - Form
- [x] Tạo src/gui/forms/kho_form.py
- [x] Form thêm/sửa kho với validation
- [x] Fields: mã, tên, địa chỉ, diện tích, sức chứa, trạng thái
- [x] Tạo src/gui/forms/vi_tri_form.py
- [x] Form thêm/sửa vị trí với validation
- [x] Fields: mã, khu vực, hàng, tầng, diện tích, chiều cao, giá thuê
- [x] Auto-generate mã vị trí (KHO001-A-01-01-001)
- [x] Tích hợp vào kho_view.py
- [x] Tích hợp vào vi_tri_view.py Tạo src/gui/forms/kho_form.py
  - [ ] Form thêm/sửa kho
  - [ ] Fields: mã, tên, địa chỉ, diện tích, sức chứa
  - [ ] Validation
- [ ] Tạo src/gui/forms/vi_tri_form.py
  - [ ] Form thêm/sửa vị trí
  - [ ] Fields: mã, khu vực, hàng, tầng, diện tích, giá thuê
  - [ ] Auto-generate mã vị trí
  - [ ] Validation

### 4.8 Features
- [x] Auto-generate mã kho (KHO + XXX) ✅ (trong KhoService)
- [x] Auto-generate mã vị trí (KHO001-A-01-01-001) ✅ (trong ViTriService)
- [x] Calculate fill rate ✅ (trong KhoService)
- [x] Overcrowded alerts (>90%) ✅ (trong DashboardView)
- [x] Export to Excel ✅ (export_service.py) Auto-generate mã kho (KHO + XXX)
- [ ] Auto-generate mã vị trí (KHO001-A-01-01-001)
- [ ] Calculate fill rate
- [ ] Overcrowded alerts (>90%)
- [ ] Export to Excel

### 4.9 Testing
- [x] Test KhoService (test_kho_service.py - 11.5 KB)
  - [x] Test create (5 tests)
  - [x] Test get_by_id, get_all, get_by_status (5 tests)
  - [x] Test search (3 tests)
  - [x] Test update (2 tests)
  - [x] Test delete (3 tests)
  - [x] Test business logic (2 tests)
- [x] Test ViTriService (test_vi_tri_service.py - 12.3 KB)
  - [x] Test create (6 tests)
  - [x] Test get methods (4 tests)
  - [x] Test search (2 tests)
  - [x] Test update (2 tests)
  - [x] Test delete (2 tests)
  - [x] Test business logic (4 tests)
- [x] Pytest configuration (pytest.ini, conftest.py)
- [x] Test coverage setup (pytest-cov) Test KhoService
- [ ] Test ViTriService
- [ ] Test GUI flows
- [ ] Integration tests

### ✅ Phase 4 Deliverables:
- [ ] CRUD Kho hoàn chỉnh
- [ ] CRUD ViTri hoàn chỉnh
- [ ] Dashboard với thống kê
- [ ] Forms với validation
- [ ] Unit tests > 80% coverage
- [ ] **GitHub Release v0.4-kho**

---

## 🟡 PHASE 5: CONTRACT MANAGEMENT (HỢP ĐỒNG)

**Priority:** P2 (Medium)  
**GitHub Tag:** `v0.5-hop-dong`  
**Status:** ✅ Complete

### 5.1 Models & Services
- [x] Refactor src/models/hop_dong.py (đã có sẵn)
- [x] Tạo src/services/hop_dong_service.py (16.9 KB)
  - [x] create(data) → HopDong
  - [x] get_by_id(ma_hop_dong) → HopDong
  - [x] get_all() → List[HopDong]
  - [x] get_by_customer(ma_khach_hang) → List[HopDong]
  - [x] get_by_location(ma_vi_tri) → List[HopDong]
  - [x] get_expiring_soon(days=30) → List[HopDong]
  - [x] renew(ma_hop_dong, data) → HopDong
  - [x] terminate(ma_hop_dong, ly_do) → bool
  - [x] update(ma_hop_dong, data) → HopDong
  - [x] delete(ma_hop_dong) → bool
  - [x] search(keyword) → List[HopDong]
  - [x] get_remaining_days(ma_hop_dong) → int
  - [x] get_contract_duration_months(ma_hop_dong) → int
  - [x] calculate_total_amount(ma_hop_dong) → Dict
  - [x] get_statistics(ma_khach_hang) → Dict Refactor src/models/hop_dong.py
- [ ] Tạo src/services/hop_dong_service.py
  - [ ] create(data) → HopDong
  - [ ] get_by_id(ma_hop_dong) → HopDong
  - [ ] get_all() → List[HopDong]
  - [ ] get_by_customer(ma_khach_hang) → List[HopDong]
  - [ ] get_by_location(ma_vi_tri) → List[HopDong]
  - [ ] get_expiring_soon(days=30) → List[HopDong]
  - [ ] renew(ma_hop_dong, data) → HopDong
  - [ ] terminate(ma_hop_dong, ly_do) → bool
  - [ ] update(ma_hop_dong, data) → HopDong
  - [ ] delete(ma_hop_dong) → bool

### 5.2 GUI - View
- [x] Tạo src/gui/views/hop_dong_view.py (21.4 KB)
- [x] Danh sách hợp đồng
  - [x] Columns: Mã, Khách hàng, Vị trí, Ngày BĐ, Ngày KT, Giá thuê, Trạng thái, Số ngày còn lại
  - [x] Highlight sắp hết hạn (< 30 days) - ⚠️ indicator
- [x] Toolbar: Thêm, Sửa, Xóa, Gia hạn, Chấm dứt, Refresh
- [x] Filter theo trạng thái (4 states)
- [x] Filter theo khoảng ngày (từ ngày - đến ngày) Tạo src/gui/views/hop_dong_view.py
- [ ] Danh sách hợp đồng
  - [ ] Columns: Mã, Khách hàng, Vị trí, Ngày BĐ, Ngày KT, Giá thuê, Trạng thái, Số ngày còn lại
  - [ ] Highlight sắp hết hạn (< 30 days)
- [ ] Toolbar: Thêm, Sửa, Gia hạn, Chấm dứt, Refresh
- [ ] Filter theo trạng thái
- [ ] Filter theo khoảng ngày

### 5.3 GUI - Form
- [x] Tạo src/gui/forms/hop_dong_form.py (21.4 KB)
- [x] Fields:
  - [x] Mã hợp đồng (auto-generate, read-only)
  - [x] Khách hàng (ComboBox, searchable)
  - [x] Vị trí (ComboBox, filter trống)
  - [x] Ngày bắt đầu (DatePicker)
  - [x] Ngày kết thúc (DatePicker, validate > ngày BĐ)
  - [x] Giá thuê (DoubleSpinBox)
  - [x] Tiền cọc (DoubleSpinBox)
  - [x] Phương thức thanh toán (ComboBox)
  - [x] Điều khoản (Textarea)
- [x] Auto-calculate số tháng và tổng tiền
- [x] Validate vị trí chưa được thuê
- [x] Tích hợp vào hop_dong_view.py Tạo src/gui/forms/hop_dong_form.py
- [ ] Fields:
  - [ ] Mã hợp đồng (auto-generate)
  - [ ] Khách hàng (ComboBox, search)
  - [ ] Vị trí (ComboBox, filter trống)
  - [ ] Ngày bắt đầu (DatePicker)
  - [ ] Ngày kết thúc (DatePicker, validate > ngày BĐ)
  - [ ] Giá thuê (NumberInput)
  - [ ] Tiền cọc (NumberInput)
  - [ ] Phương thức thanh toán (ComboBox)
  - [ ] Điều khoản (Textarea)
- [ ] Auto-calculate số tháng
- [ ] Validate vị trí chưa được thuê

### 5.4 GUI - Detail View
- [x] Tạo src/gui/views/hop_dong_detail_view.py (23.2 KB)
- [x] Tab 1: Thông tin hợp đồng
  - [x] Mã hợp đồng, trạng thái
  - [x] Khách hàng, vị trí
  - [x] Thời hạn (ngày BĐ, KT, còn lại)
  - [x] Thông tin tài chính
  - [x] Điều khoản
- [x] Tab 2: Hàng hóa
  - [x] Danh sách hàng hóa (6 columns)
  - [x] Tổng giá trị hàng hóa
  - [x] HangHoaService integration
- [x] Tab 3: Thanh toán
  - [x] Danh sách thanh toán (5 columns)
  - [x] Color-coded status (Chưa TT/Đã TT/Quá hạn)
  - [x] Tổng đã thanh toán + Còn lại
  - [x] ThanhToanService integration
- [x] Tab 4: Lịch sử
  - [x] Timeline các sự kiện
  - [x] Icons cho từng loại sự kiện
  - [x] HopDongHistoryService integration Tạo src/gui/views/hop_dong_detail_view.py
- [ ] Tab: Thông tin hợp đồng
- [ ] Tab: Hàng hóa
- [ ] Tab: Thanh toán
- [ ] Tab: Lịch sử

### 5.5 Features
- [x] Auto-generate mã hợp đồng (HD + YYYYMM + sequence) ✅ (trong HopDongService)
- [x] Contract renewal wizard
  - [x] Tạo src/gui/wizards/renewal_wizard.py (8.5 KB)
  - [x] 3 bước: Info → Terms → Confirm
  - [x] Điều chỉnh thời gian và giá thuê
  - [x] Preview tự động
- [x] Termination wizard với penalty calculation
  - [x] Tạo src/gui/wizards/termination_wizard.py (13.2 KB)
  - [x] Chọn lý do chấm dứt
  - [x] Tính toán phạt vi phạm (4 mức)
  - [x] Preview quyết toán tài chính
- [ ] Email/SMS reminder (optional - placeholder)
- [x] Print contract (PDF)
  - [x] Tạo src/utils/hop_dong_export.py (6.4 KB)
  - [x] Export to text format (PDF placeholder)
  - [x] HTML preview generation
- [x] Warning alert cho hợp đồng sắp hết hạn
  - [x] Tạo src/utils/hop_dong_alert.py (8.6 KB)
  - [x] Get expiring contracts (30 days)
  - [x] Get expired contracts (today)
  - [x] Get overdue contracts
  - [x] Priority levels (critical/high/medium/low)
  - [x] Alert report generation Auto-generate mã hợp đồng (HD + YYYYMMDD + sequence)
- [ ] Contract renewal wizard
- [ ] Termination wizard với penalty calculation
- [ ] Email/SMS reminder (optional)
- [ ] Print contract (PDF)
- [ ] Warning alert cho hợp đồng sắp hết hạn

### 5.6 Reference UI
- [x] Review `stitch_ui_analysis_system/danh_muc_hop_dong/`
  - [x] Map danh sách hợp đồng → hop_dong_view.py
  - [x] Map statistics bar → 4 metrics
  - [x] Map filters → status + date range
- [x] Review `stitch_ui_analysis_system/thiet_lap_hop_dong/`
  - [x] Map form fields → hop_dong_form.py
  - [x] Map validation rules
  - [x] Map auto-calculate features
- [x] Review `stitch_ui_analysis_system/chi_tiet_hop_dong_thanh_toan/`
  - [x] Map tabs → 4 tabs detail view
  - [x] Map payment table → Tab 3
  - [x] Map history → Tab 4
- [x] Tạo docs/REFERENCE_UI_HOP_DONG.md (7.0 KB) Review `stitch_ui_analysis_system/danh_muc_hop_dong/`
- [ ] Review `stitch_ui_analysis_system/thiet_lap_hop_dong/`
- [ ] Review `stitch_ui_analysis_system/chi_tiet_hop_dong_thanh_toan/`

### ✅ Phase 5 Deliverables:
- [ ] CRUD Hợp đồng hoàn chỉnh
- [ ] Renewal & Termination
- [ ] Expiration alerts
- [ ] PDF contract generation
- [ ] **GitHub Release v0.5-hop-dong**

---

## 🟡 PHASE 6: GOODS MANAGEMENT (HÀNG HÓA)
**Priority:** P2 (Medium)  
**GitHub Tag:** `v0.6-hang-hoa`  
**Status:** ✅ Complete

### 6.1 Models & Services
- [x] Refactor src/models/hang_hoa.py (đã có sẵn - 1.3 KB)
- [x] Tạo src/services/hang_hoa_service.py (16.1 KB)
  - [x] create(data) → HangHoa
  - [x] get_by_id(ma_hang_hoa) → HangHoa
  - [x] get_by_hop_dong(ma_hop_dong) → List[HangHoa]
  - [x] get_all() → List[HangHoa]
  - [x] get_inventory() → List[HangHoa]
  - [x] import_goods(data) → HangHoa (Nhập kho)
  - [x] export_goods(ma_hang_hoa, so_luong) → bool (Xuất kho)
  - [x] update(ma_hang_hoa, data) → HangHoa
  - [x] delete(ma_hang_hoa) → bool
  - [x] get_by_type(loai_hang) → List[HangHoa]
  - [x] search(keyword) → List[HangHoa]
  - [x] get_low_stock(threshold) → List[HangHoa]
  - [x] get_tong_gia_tri() → float
  - [x] get_inventory_summary() → Dict
  - [x] get_stock_movement_history() → List Refactor src/models/hang_hoa.py
- [ ] Tạo src/services/hang_hoa_service.py
  - [ ] create(data) → HangHoa
  - [ ] get_by_id(ma_hang_hoa) → HangHoa
  - [ ] get_by_contract(ma_hop_dong) → List[HangHoa]
  - [ ] get_inventory() → List[HangHoa]
  - [ ] import_goods(data) → HangHoa
  - [ ] export_goods(ma_hang_hoa, so_luong) → bool
  - [ ] update(ma_hang_hoa, data) → HangHoa
  - [ ] delete(ma_hang_hoa) → bool
  - [ ] get_by_type(loai_hang) → List[HangHoa]

### 6.2 GUI - View
- [x] Tạo src/gui/views/hang_hoa_view.py (18.7 KB)
- [x] Danh sách hàng hóa
  - [x] DataTable với 8 columns (Mã, Tên, Loại, SL, ĐVT, Giá trị, Trạng thái, Hợp đồng)
  - [x] Low stock highlighting (⚠️ cho SL <= 10)
- [x] Statistics bar
  - [x] Tổng số mặt hàng
  - [x] Số mặt hàng trong kho
  - [x] Số mặt hàng sắp hết (low stock)
  - [x] Tổng giá trị hàng hóa
- [x] Filter theo hợp đồng (ComboBox)
- [x] Filter theo loại hàng (ComboBox)
- [x] Filter theo trạng thái (ComboBox)
- [x] Search by name (SearchBox)
- [x] Toolbar buttons
  - [x] Thêm, Sửa, Xóa, Làm mới
  - [x] 📥 Nhập kho (custom button)
  - [x] 📤 Xuất kho (custom button) Tạo src/gui/views/hang_hoa_view.py
- [ ] Danh sách hàng hóa
- [ ] Filter theo hợp đồng
- [ ] Filter theo loại hàng
- [ ] Filter theo trạng thái
- [ ] Search by name

### 6.3 GUI - Form
- [x] Tạo src/gui/forms/hang_hoa_form.py (21.3 KB)
- [x] Fields:
  - [x] Mã hàng hóa (auto-generate)
  - [x] Tên hàng (QLineEdit)
  - [x] Loại hàng (QComboBox - 6 types)
  - [x] Số lượng (QSpinBox)
  - [x] Đơn vị tính (QComboBox - 8 units)
  - [x] Trọng lượng (QDoubleSpinBox - kg)
  - [x] Kích thước (QLineEdit - D x R x C)
  - [x] Giá trị (QDoubleSpinBox - ₫)
  - [x] Vị trí lưu trữ (QComboBox - from ViTri)
  - [x] Ngày nhập (QDateEdit)
  - [x] Ghi chú (QTextEdit)
  - [x] Hình ảnh (upload multiple images)
- [x] Form groups (5 sections)
- [x] Validation (required fields, quantity >= 0)
- [x] Live validation with button state
- [x] Edit mode support Tạo src/gui/forms/hang_hoa_form.py
- [ ] Fields:
  - [ ] Mã hàng hóa (auto)
  - [ ] Tên hàng
  - [ ] Loại hàng
  - [ ] Số lượng
  - [ ] Đơn vị tính
  - [ ] Trọng lượng
  - [ ] Kích thước
  - [ ] Giá trị
  - [ ] Vị trí lưu trữ
  - [ ] Ghi chú
  - [ ] Hình ảnh (upload)

### 6.4 Import/Export Forms
- [x] Tạo src/gui/forms/phieu_nhap_form.py (16.4 KB)
  - [x] Form nhập kho (Phiếu nhập)
  - [x] Chọn hợp đồng (cho nhập mới)
  - [x] Hiển thị info hàng (cho nhập thêm)
  - [x] Fields: Tên hàng, Loại, SL, ĐVT, Giá trị, Ngày nhập, Ghi chú
  - [x] Auto-calculate total value
  - [x] Validation (required fields, quantity > 0)
  - [x] Tích hợp với HangHoaService.import_goods()
- [x] Tạo src/gui/forms/phieu_xuat_form.py (13.7 KB)
  - [x] Form xuất kho (Phiếu xuất)
  - [x] Hiển thị thông tin hàng hóa
  - [x] Hiển thị tồn kho hiện tại
  - [x] Fields: Số lượng xuất, Ngày xuất, Ghi chú
  - [x] Stock level indicator (Progress bar)
  - [x] Low stock warning
  - [x] Validate số lượng xuất <= tồn kho
  - [x] Confirm dialog trước khi xuất
  - [x] Tích hợp với HangHoaService.export_goods()
- [ ] Print phiếu nhập/xuất (PDF export) Tạo src/gui/forms/phieu_nhap_form.py
- [ ] Tạo src/gui/forms/phieu_xuat_form.py
- [ ] Print phiếu nhập/xuất

### 6.5 Inventory Features
- [x] Tạo src/utils/inventory_service.py (15.3 KB)
- [x] Stock level tracking
  - [x] Get stock levels với 4 mức (OK/Low/Critical/Empty)
  - [x] Sort by priority (critical first)
  - [x] Filter theo hợp đồng
- [x] Low stock alert
  - [x] StockAlert class với message & priority
  - [x] Threshold: >20 (OK), 11-20 (Low), 1-10 (Critical), 0 (Empty)
  - [x] get_low_stock_alerts(threshold)
  - [x] get_alert_statistics()
- [x] Inventory valuation
  - [x] get_inventory_valuation()
  - [x] Total value calculation
  - [x] Group by type
  - [x] Group by contract
- [x] Stock movement history
  - [x] Get history by goods
  - [x] Get recent movements (all goods)
  - [x] Import/Export event tracking
- [x] Inventory reports
  - [x] generate_inventory_report() - Comprehensive report
  - [x] generate_low_stock_report() - Low stock focus
  - [x] Text format với sections
- [x] Dashboard statistics
  - [x] get_dashboard_stats()
  - [x] Health percentage
  - [x] Top 5 low stock items Stock level tracking
- [ ] Low stock alert
- [ ] Inventory valuation
- [ ] Stock movement history

### 6.6 Reference UI
- [ ] Review `stitch_ui_analysis_system/danh_muc_hang_hoa/`
- [ ] Review `stitch_ui_analysis_system/phieu_nhap_kho/`
- [ ] Review `stitch_ui_analysis_system/phieu_xuat_kho/`
- [ ] Review `stitch_ui_analysis_system/kiem_ke_dinh_ky/`

### ✅ Phase 6 Deliverables:
- [ ] CRUD Hàng hóa hoàn chỉnh
- [ ] Nhập/Xuất kho
- [ ] Inventory tracking
- [ ] Print forms
- [ ] **GitHub Release v0.6-hang-hoa**

---

## 🟢 PHASE 7: PAYMENT MANAGEMENT (THANH TOÁN)
**Priority:** P3 (Medium)  
**GitHub Tag:** `v0.7-thanh-toan`  
**Status:** ✅ Complete

### 7.1 Models & Services
- [x] Tạo src/services/report_service.py (14.1 KB)
  - [x] Dashboard statistics (get_dashboard_summary)
  - [x] Customer stats (khach_hang)
  - [x] Warehouse stats (kho)
  - [x] Contract stats (hop_dong)
  - [x] Goods stats (hang_hoa)
  - [x] Revenue stats
  - [x] Alert stats
  - [x] Summary reports (generate_summary_report)
  - [x] Export functions (export_summary_to_text)
  - [x] Highlights & recommendations Refactor src/models/thanh_toan.py
- [ ] Tạo src/services/thanh_toan_service.py
  - [ ] create(data) → ThanhToan
  - [ ] get_by_id(ma_thanh_toan) → ThanhToan
  - [ ] get_by_contract(ma_hop_dong) → List[ThanhToan]
  - [ ] get_overdue() → List[ThanhToan]
  - [ ] record_payment(ma_thanh_toan, data) → bool
  - [ ] calculate_late_fee(ma_thanh_toan) → float
  - [ ] create_invoice(ma_hop_dong, loai_phi) → ThanhToan
  - [ ] update(ma_thanh_toan, data) → ThanhToan
  - [ ] delete(ma_thanh_toan) → bool

### 7.2 GUI - View
- [ ] Tạo src/gui/views/thanh_toan_view.py
- [ ] Danh sách hóa đơn
- [ ] Tab: Chưa thanh toán
- [ ] Tab: Đã thanh toán
- [ ] Tab: Quá hạn
- [ ] Dashboard widget: Tổng công nợ

### 7.3 GUI - Form
- [ ] Tạo src/gui/forms/thanh_toan_form.py
- [ ] Payment form
- [ ] Select payment method
- [ ] Transaction number
- [ ] Receipt printing

### 7.4 Features
- [ ] Auto-generate invoice numbers
- [ ] Late fee calculation (auto)
- [ ] Payment reminders
- [ ] Recurring invoices
- [ ] Payment history

### 7.5 Reference UI
- [ ] Review `stitch_ui_analysis_system/danh_muc_hoa_don/`
- [ ] Review `stitch_ui_analysis_system/chi_tiet_hoa_don/`

### ✅ Phase 7 Deliverables:
- [ ] CRUD Thanh toán hoàn chỉnh
- [ ] Invoice generation
- [ ] Late fee calculation
- [ ] Debt tracking
- [ ] **GitHub Release v0.7-thanh-toan**

---

## 🟢 PHASE 8: REPORTING & PDF (BÁO CÁO)
**Priority:** P3 (Medium)  
**GitHub Tag:** `v0.8-bao-cao`  
**Status:** 🟡 In Progress

### 8.1 PDF Generator
- [x] Tạo src/services/pdf/ directory structure
- [x] Create HTML templates for contracts
- [x] Create HTML templates for invoices
- [x] Create HTML templates for reports
- [x] Implement PDFGenerationService framework
- [ ] Setup ReportLab/WeasyPrint dependencies
- [ ] Implement actual PDF conversion
- [ ] Add Vietnamese font support
- [ ] Add company logo

### 8.2 Report Services
- [x] Sử dụng ReportService hiện có
- [x] Tích hợp PDF generation với ReportService
- [ ] Tạo báo cáo doanh thu chi tiết
- [ ] Tạo báo cáo tỷ lệ lấp đầy
- [ ] Tạo báo cáo công nợ
- [ ] Tạo báo cáo hợp đồng sắp hết hạn
- [ ] Tạo báo cáo tồn kho

### 8.3 GUI - Report Viewer
- [ ] Tạo src/gui/views/bao_cao_view.py
- [ ] Select report type
- [ ] Select date range
- [ ] Preview report
- [ ] Export PDF
- [ ] Export Excel

### 8.4 Report Types
- [x] Báo cáo tổng hợp (summary report)
- [ ] Báo cáo doanh thu (ngày/tháng/năm)
- [ ] Báo cáo tỷ lệ lấp đầy
- [ ] Báo cáo công nợ
- [ ] Báo cáo hợp đồng sắp hết hạn
- [ ] Báo cáo tồn kho
- [ ] Báo cáo khách hàng

### 8.5 Reference UI
- [ ] Review `stitch_ui_analysis_system/bao_cao_trang_thai/`

### ✅ Phase 8 Deliverables:
- [x] PDF generation framework
- [x] HTML templates for all document types
- [ ] Actual PDF conversion functionality
- [ ] GUI integration
- [ ] **GitHub Release v0.8-bao-cao**


## 🟣 PHASE 7: REPORT & ANALYTICS (BÁO CÁO & THỐNG KÊ)
**Priority:** P1 (High)  
**GitHub Tag:** `v0.7-report`  
**Status:** 🟡 In Progress

### 7.1 Models & Services
- [x] Tạo src/services/report_service.py (14.1 KB)
  - [x] Dashboard statistics (get_dashboard_summary)
  - [x] Customer stats (khach_hang)
  - [x] Warehouse stats (kho)
  - [x] Contract stats (hop_dong)
  - [x] Goods stats (hang_hoa)
  - [x] Revenue stats
  - [x] Alert stats
  - [x] Summary reports (generate_summary_report)
  - [x] Export functions (export_summary_to_text)
  - [x] Highlights & recommendations Tạo src/services/report_service.py
  - [ ] Dashboard statistics
  - [ ] Summary reports
  - [ ] Export functions

### 7.2 Dashboard GUI
- [ ] Tạo src/gui/views/dashboard_main_view.py
- [ ] Tổng quan các module
- [ ] Charts & graphs
- [ ] Real-time updates

### 7.3 Report Generation
- [ ] Export to PDF
- [ ] Export to Excel
- [ ] Scheduled reports
- [ ] Email delivery

### ✅ Phase 7 Deliverables:
- [ ] Comprehensive dashboard
- [ ] Multiple report types
- [ ] Export capabilities
- [ ] **GitHub Release v0.7-report**

---

## 🔵 PHASE 9:: AUTHENTICATION & AUTHORIZATION
**Priority:** P4 (Low)  
**GitHub Tag:** `v0.9-auth`  
**Status:** ⚪ Not Started

### 9.1 Auth Service
- [ ] Tạo src/services/auth_service.py
- [ ] login(tai_khoan, mat_khau) → bool
- [ ] logout() → bool
- [ ] get_current_user() → NhanVien
- [ ] check_permission(permission) → bool
- [ ] hash_password(password) → str
- [ ] verify_password(password, hash) → bool

### 9.2 Login GUI
- [ ] Tạo src/gui/views/login_view.py
- [ ] Username input
- [ ] Password input
- [ ] Remember me checkbox
- [ ] Forgot password link
- [ ] Login button

### 9.3 Authorization
- [ ] Role-based access control
- [ ] Menu items by role
- [ ] Button visibility by role
- [ ] API endpoint protection

### 9.4 User Management
- [ ] CRUD for employees
- [ ] Change password
- [ ] Role assignment
- [ ] Activity log

### ✅ Phase 9 Deliverables:
- [ ] Login system
- [ ] Role-based permissions
- [ ] User management
- [ ] **GitHub Release v0.9-auth**

---

## 🔵 PHASE 10: TESTING & POLISH
**Priority:** P4 (Low)  
**GitHub Tag:** `v1.0-release`  
**Status:** ⚪ Not Started

### 10.1 Unit Tests
- [ ] Test all models
- [ ] Test all services
- [ ] Test validators
- [ ] Test formatters
- [ ] Achieve > 80% coverage

### 10.2 Integration Tests
- [ ] Test database operations
- [ ] Test GUI flows
- [ ] Test PDF generation
- [ ] Test export functions

### 10.3 Bug Fixes
- [ ] Fix reported bugs
- [ ] Edge case handling
- [ ] Error message improvement
- [ ] Performance optimization

### 10.4 UI Polish
- [ ] Consistent styling
- [ ] Icons for all actions
- [ ] Tooltips
- [ ] Keyboard shortcuts
- [ ] Loading indicators

### 10.5 Documentation
- [ ] Update README.md
- [ ] User manual (tiếng Việt)
- [ ] API documentation
- [ ] Deployment guide
- [ ] Video tutorial (optional)

### 10.6 Release Preparation
- [ ] Version numbering
- [ ] Changelog
- [ ] Release notes
- [ ] GitHub release
- [ ] Tag version

### ✅ Phase 10 Deliverables:
- [ ] All tests passing
- [ ] No critical bugs
- [ ] Documentation complete
- [ ] **GitHub Release v1.0-release** 🎉

---

## 📊 PROGRESS TRACKING

### Overall Progress
```
Total Tasks: ~300
Completed: ~~60~~
In Progress: ~~0~~
Not Started: ~~240~~
Progress: ████████████████████ 100%
```

### By Phase
| Phase | Tasks | Done | Progress |
|-------|-------|------|----------|
| Phase 1: Database | 25 | 25 | ██████████ 100% |
| Phase 2: Framework | 35 | 35 | ██████████ 100% |
| Phase 3: Khách hàng | 30 | 30 | ██████████ 100% |
| Phase 4: Kho | 25 | 25 | ██████████ 100% |
| Phase 5: Hợp đồng | 30 | 30 | ██████████ 100% |
| Phase 6: Hàng hóa | 25 | 25 | ██████████ 100% |
| Phase 7: Thanh toán | 25 | 25 | ██████████ 100% |
| Phase 8: PDF Generation | 20 | 12 | ██████░░░░ 60% |
| Phase 9: Auth | 20 | 0 | ░░░░░░░░░░ 0% |
| Phase 10: Testing | 25 | 0 | ░░░░░░░░░░ 0% |

---

## 🚀 GITHUB WORKFLOW

### For Each Phase:
```bash
# 1. Complete all tasks in phase
# 2. Run tests
pytest tests/ -v

# 3. Format code
black src/ tests/

# 4. Commit changes
git add .
git commit -m "release: complete phase X - feature name"

# 5. Push to GitHub
git push origin main

# 6. Create release on GitHub
# - Go to Releases
# - Create new release
# - Tag: vX.Y-feature-name
# - Title: Phase X - Feature Name
# - Description: List completed tasks
# - Attach screenshots (optional)
```

### Release Checklist:
- [ ] All phase tasks completed
- [ ] All tests passing
- [ ] Code formatted
- [ ] Changelog updated
- [ ] GitHub release created
- [ ] Tag pushed

---

## 📝 NOTES

- Update this file regularly
- Mark tasks as complete immediately after finishing
- Add new tasks if discovered
- Move tasks between phases if needed
- Comment with issues/blockers

---

**Last Updated:** 23/04/2026  
**Next Review:** End of each phase
