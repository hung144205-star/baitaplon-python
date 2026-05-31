# Mô Tả Thiết Kế Modules Chi Tiết

**Đề tài:** Quản Lý Dịch Vụ Cho Thuê Kho Lưu Trữ Hàng Hóa **Ngày cập nhật:** 10/05/2026

---

## 1. Kiến trúc tổng thể

Chương trình tổ chức theo mô hình ba lớp với sáu module chính. Sơ đồ quan hệ giữa các module:
```
              +-----------+
              | main_app  |
              +-----+-----+
                    |
    +---------------+---------------+
    |               |               |
+---v----+  +------v----+  +------v----+
|  gui   |  | services  |  |   utils   |
| (PyQt6)|->| (nghiệp   |  | (export,  |
| views  |  |  vụ)      |  |  alert)   |
+--------+  +------+----+  +-----------+
                    |
           +-------v----+    +---------+
           | models     |    |templates|
           | (ORM)      |    | (PDF)   |
           +-------+----+    +---------+
                   |
           +-------v----+
           | database   |
           | (SQLite)   |
           +------------+
```

## 2. Module Models (src/models/)

Module định nghĩa các lớp ORM kế thừa `BaseModel` (ngay_tao, ngay_cap_nhat, to_dict, to_json). `enums.py` chứa mười enum chuẩn hóa trạng thái: `TrangThaiHDEnum` (HIEU_LUC, HET_HAN, CHAM_DUT, GIA_HAN), `TrangThaiTTEnum` (DA_THANH_TOAN, CHUA_THANH_TOAN, QUA_HAN), `TrangThaiViTriEnum` (TRONG, DA_THUE, BAO_TRI), `TrangThaiKhoEnum` (HOAT_DONG, BAO_TRI, NGUNG), `LoaiKhachEnum` (CA_NHAN, DOANH_NGHIEP), `VaiTroNhanVienEnum` (QUAN_TRI, KINH_DOANH, KHO, KE_TOAN) cùng các enum hàng hóa, phí và nhật ký. Danh sách mười một model:

| Model | File | Vai trò |
|---|---|---|
| KhachHang | khach_hang.py | Thông tin cá nhân/doanh nghiệp, MST |
| Kho | kho.py | Diện tích, sức chứa, địa chỉ |
| ViTri | vi_tri.py | Vị trí Khu vực-Hàng-Tầng, giá thuê |
| HopDong | hop_dong.py | Thời hạn, giá thuê, tiền cọc |
| HangHoa | hang_hoa.py | Số lượng, trọng lượng, giá trị |
| LoaiHang | loai_hang.py | Danh mục phân loại hàng |
| ThanhToan | thanh_toan.py | Kỳ hạn, số tiền, trạng thái |
| NhanVien | nhan_vien.py | Vai trò, băm mật khẩu bcrypt |
| SystemLog | system_log.py | Nhật ký thao tác |
| BaoCao | bao_cao.py | Báo cáo đã lưu |
| BaseModel | base.py | Lớp cơ sở |

## 3. Module Database (src/database/)

`DatabaseConnection` là singleton quản lý một engine SQLAlchemy cho tệp `data/warehouse.db`. `session_scope()` là context manager tự động commit/rollback. `BaseRepository[T]` triển khai CRUD generic (create, get_by_id, get_all phân trang, update, delete, count, exists). `SoftDeleteRepository[T]` xóa mềm qua cập nhật `trang_thai`. `TimestampRepository[T]` tự động quản lý `ngay_tao` và `ngay_cap_nhat`. `migrate.py` nâng cấp cấu trúc cơ sở dữ liệu.

## 4. Module Services (src/services/)

`BaseService` là lớp trừu tượng cung cấp context manager `transaction()`. `TransactionContext` singleton cho phép nhiều service chia sẻ session qua `@transactional`. `PDFGenerationService` tại `pdf/pdf_generation_service.py` tạo hợp đồng, hóa đơn, báo cáo PDF qua ReportLab. Mười service chính:

| Service | File | Chức năng |
|---|---|---|
| AuthService | auth/auth_service.py | Đăng nhập, bcrypt, khóa sau 5 lần sai |
| AuthorizationService | auth/authorization_service.py | RBAC bốn vai trò |
| KhachHangService | khach_hang_service.py | CRUD, sinh mã KH+ngày+STT, xóa mềm |
| KhoService | kho_service.py | CRUD, tỷ lệ lấp đầy, cảnh báo quá tải |
| ViTriService | vi_tri_service.py | CRUD, sinh mã Kho-Vùng-Hàng-Tầng |
| HopDongService | hop_dong_service.py | CRUD, gia hạn, chấm dứt, tính phạt |
| HangHoaService | hang_hoa_service.py | Nhập/xuất, cảnh báo tồn dưới 10 |
| ThanhToanService | thanh_toan_service.py | Thanh toán, lịch định kỳ |
| ReportService | report_service.py | Dashboard, doanh thu, tổng hợp |
| UserService | users/user_service.py | Quản lý nhân viên, phân quyền |

## 5. Module GUI (src/gui/)

`MainWindow` chứa `SidebarMenu` trái, `BreadcrumbWidget`, `QStackedWidget` chuyển mười hai view, và `StatusBar`. Các form nhập liệu (`KhachHangForm`, `KhoForm`, `HopDongForm`, `HangHoaForm`, `ThanhToanForm`, `ViTriForm`, `UserForm`, `LoaiHangForm`, `PhieuNhapForm`, `PhieuXuatForm`) là `QDialog` có kiểm tra dữ liệu. Hai wizard ba bước (`RenewalWizard` gia hạn, `TerminationWizard` chấm dứt). Widget `DataTable`, `SearchBox`, `Charts` (Matplotlib), `LoadingWidget` và `Buttons` được tái sử dụng khắp các view. Giao diện tạo kiểu qua tệp QSS `main.qss`.
## 6. Module Utils (src/utils/)

| Tệp | Chức năng |
|---|---|
| validators.py | Kiểm tra email, SĐT, số dương, ngày |
| formatters.py | Định dạng tiền VNĐ, ngày tháng |
| helpers.py | Hàm tiện ích đa năng |
| export_service.py | Xuất Excel qua Pandas+OpenPyXL |
| hop_dong_alert.py | Cảnh báo hợp đồng quá hạn, sắp hết hạn |
| inventory_service.py | Kiểm tra tồn kho thấp |

## 7. Module Templates (src/templates/)

Ba tệp HTML mẫu: `contract_template.html` (hợp đồng thuê kho với thông tin khách hàng, vị trí, điều khoản, chữ ký), `invoice_template.html` (hóa đơn thanh toán với dịch vụ, thuế, tổng tiền), `report_template.html` (báo cáo tổng hợp số liệu, biểu đồ, khuyến nghị).

## 8. Tổng kết

| Module | Thư mục | Tệp | Vai trò |
|---|---|---|---|
| models | src/models/ | 13 | Thực thể ORM, enum |
| database | src/database/ | 5 | Kết nối SQLite, Repository |
| services | src/services/ | 15 | Logic nghiệp vụ, PDF, phân quyền |
| gui | src/gui/ | 34 | Giao diện PyQt6 |
| utils | src/utils/ | 7 | Tiện ích, xuất Excel, cảnh báo |
| templates | src/templates/ | 3 | Mẫu HTML xuất PDF |
