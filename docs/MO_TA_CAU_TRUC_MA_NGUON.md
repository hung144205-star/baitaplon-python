# Mô Tả Cấu Trúc Mã Nguồn Chương Trình và Giải Thích Ý Nghĩa Các File Mã Nguồn

**Đề tài:** Quản Lý Dịch Vụ Cho Thuê Kho Lưu Trữ Hàng Hóa
**Nhóm thực hiện:** Nhóm 12 - Lập trình Python
**Ngày cập nhật:** 10/05/2026

---

## Mục lục

1. [Tổng quan kiến trúc](#1-tổng-quan-kiến-trúc)
2. [Cấu trúc thư mục tổng thể](#2-cấu-trúc-thư-mục-tổng-thể)
3. [Tầng Mô hình (Models Layer)](#3-tầng-mô-hình-models-layer)
4. [Tầng Dịch vụ (Services Layer)](#4-tầng-dịch-vụ-services-layer)
5. [Tầng Giao diện (GUI Layer)](#5-tầng-giao-diện-gui-layer)
6. [Tầng Dữ liệu (Database Layer)](#6-tầng-dữ-liệu-database-layer)
7. [Tầng Tiện ích (Utils Layer)](#7-tầng-tiện-ích-utils-layer)
8. [Thư mục Kiểm thử (Tests)](#8-thư-mục-kiểm-thử-tests)
9. [Các file cấu hình và hỗ trợ](#9-các-file-cấu-hình-và-hỗ-trợ)

---

## 1. Tổng quan kiến trúc

Chương trình được thiết kế theo kiến trúc ba lớp (Three-tier Architecture) bao gồm tầng giao diện (Presentation Layer), tầng nghiệp vụ (Business Logic Layer) và tầng dữ liệu (Data Access Layer). Tầng giao diện sử dụng PyQt6 để xây dựng giao diện người dùng đồ họa (GUI) với các view, form, dialog, widget và wizard. Tầng nghiệp vụ chứa các service xử lý logic nghiệp vụ cho từng module chức năng như khách hàng, kho, hợp đồng, hàng hóa, thanh toán và báo cáo. Tầng dữ liệu sử dụng SQLAlchemy ORM kết nối với cơ sở dữ liệu SQLite, áp dụng Repository Pattern để truy xuất dữ liệu. Mỗi tầng chỉ giao tiếp với tầng liền kề thông qua các interface được định nghĩa rõ ràng, đảm bảo tính tách biệt và khả năng bảo trì của mã nguồn.

Sơ đồ kiến trúc tổng thể được thể hiện như sau:

```
+------------------------------------------------------------------+
|               Tầng Giao diện (GUI Layer)                          |
|  PyQt6: Views, Forms, Dialogs, Wizards, Widgets, QSS Stylesheets  |
+-------------------------------+----------------------------------+
                                |
+-------------------------------v----------------------------------+
|               Tầng Nghiệp vụ (Service Layer)                      |
|  AuthService, KhachHangService, KhoService, HopDongService,      |
|  HangHoaService, ThanhToanService, ReportService, UserService     |
+-------------------------------+----------------------------------+
                                |
        +-----------------------+-----------------------+
        |                       |                       |
+-------v--------+   +----------v----------+   +-------v---------+
| SQLAlchemy ORM |   | ReportLab (PDF)    |   | Validators      |
| SQLite + Repo  |   | Pandas (Excel)     |   | Formatters      |
| Migrate        |   | Export Services    |   | Helpers         |
+----------------+   +--------------------+   +-----------------+
```

---

## 2. Cấu trúc thư mục tổng thể

Dưới đây là cấu trúc thư mục của toàn bộ dự án, với các thư mục và file được tổ chức theo chức năng:

| Đường dẫn | Mô tả |
|---|---|
| `main.py` | Tập lệnh khởi động ứng dụng (thuần văn bản, nguyên mẫu ban đầu) |
| `src/` | Thư mục chứa toàn bộ mã nguồn chính của chương trình |
| `src/main.py` | File khởi động chính của ứng dụng (dòng lệnh, banner giới thiệu) |
| `src/app.py` | Điểm vào chính thức của ứng dụng PyQt6, khởi tạo QApplication, stylesheet, font chữ |
| `src/main_app.py` | Lớp MainApplication quản lý vòng đời ứng dụng, xác thực, session timeout |
| `src/main_window.py` | Cửa sổ chính với menu bar, toolbar, status bar, điều hướng trung tâm |
| `src/models/` | Định nghĩa các mô hình dữ liệu SQLAlchemy ORM |
| `src/services/` | Tầng nghiệp vụ với các service xử lý logic |
| `src/gui/` | Tầng giao diện người dùng PyQt6 |
| `src/database/` | Kết nối cơ sở dữ liệu, Repository Pattern, migration |
| `src/data/` | Khởi tạo dữ liệu, schema SQL, script seed |
| `src/utils/` | Các tiện ích: xác thực, định dạng, xuất Excel, cảnh báo |
| `src/templates/` | Mẫu HTML cho xuất PDF (hợp đồng, hóa đơn, báo cáo) |
| `tests/` | Thư mục chứa các bộ kiểm thử đơn vị và tích hợp |
| `data/` | Thư mục chứa cơ sở dữ liệu SQLite, file sao lưu, file xuất |
| `docs/` | Thư mục chứa tài liệu dự án |
| `scripts/` | Các tập lệnh hỗ trợ phát triển và tạo tài liệu |
| `requirements.txt` | Danh sách các thư viện Python phụ thuộc |
| `pytest.ini` | Cấu hình cho pytest |
| `README.md` | Hướng dẫn tổng quan về dự án |
| `CHANGELOG.md` | Lịch sử thay đổi phiên bản |
| `RELEASE_NOTES.md` | Ghi chú phát hành |

---

## 3. Tầng Mô hình (Models Layer)

Tầng mô hình nằm trong thư mục `src/models/` và định nghĩa các lớp ánh xạ đối tượng-quan hệ (ORM) sử dụng SQLAlchemy. Mỗi mô hình tương ứng với một bảng trong cơ sở dữ liệu SQLite. Tất cả các mô hình đều kế thừa từ `BaseModel`, một lớp cơ sở trừu tượng cung cấp các trường chung `ngay_tao` (ngày tạo), `ngay_cap_nhat` (ngày cập nhật) và các phương thức `to_dict()`, `to_json()`, `__repr__()`. Bảng dưới đây liệt kê chi tiết từng file mô hình:

| File | Lớp | Bảng | Mô tả |
|---|---|---|---|
| `base.py` | `BaseModel` | (trừu tượng) | Lớp cơ sở cho tất cả mô hình, cung cấp trường ngày tạo, ngày cập nhật và phương thức chuyển đổi dữ liệu |
| `enums.py` | (các Enum) | — | Định nghĩa các kiểu liệt kê dùng chung: trạng thái hợp đồng, trạng thái thanh toán, trạng thái vị trí, trạng thái kho, loại khách hàng, loại phí, trạng thái hàng hóa, vai trò nhân viên, hành động log |
| `khach_hang.py` | `KhachHang` | `khach_hang` | Lưu trữ thông tin khách hàng: mã KH, họ tên, loại KH (cá nhân/doanh nghiệp), SĐT, email, địa chỉ, mã số thuế, ngày đăng ký, trạng thái |
| `kho.py` | `Kho` | `kho` | Lưu trữ thông tin kho: mã kho, tên kho, địa chỉ, diện tích, sức chứa, diện tích đã sử dụng, trạng thái. Có thuộc tính tính toán tỷ lệ lấp đầy và dung tích còn lại |
| `vi_tri.py` | `ViTri` | `vi_tri` | Lưu trữ vị trí lưu trữ trong kho: mã vị trí, mã kho, khu vực, hàng, tầng, diện tích, giá thuê, sức chứa, trạng thái |
| `hop_dong.py` | `HopDong` | `hop_dong` | Lưu trữ hợp đồng thuê kho: mã hợp đồng, mã khách hàng, mã vị trí, ngày bắt đầu, ngày kết thúc, giá thuê, tiền cọc, phương thức thanh toán, điều khoản, lý do chấm dứt, trạng thái |
| `hang_hoa.py` | `HangHoa` | `hang_hoa` | Lưu trữ hàng hóa trong kho: mã hàng, mã hợp đồng, tên hàng, loại hàng, số lượng, đơn vị, trọng lượng, kích thước, giá trị, ngày nhập, ngày xuất, vị trí lưu trữ, trạng thái, ghi chú, hình ảnh |
| `thanh_toan.py` | `ThanhToan` | `thanh_toan` | Lưu trữ thanh toán: mã thanh toán, mã hợp đồng, loại phí, số tiền, kỳ thanh toán, ngày đến hạn, ngày thanh toán, phương thức, số giao dịch, trạng thái, phí phạt, ghi chú, người thu |
| `loai_hang.py` | `LoaiHang` | `loai_hang` | Lưu trữ danh mục loại hàng: mã loại, tên loại, mô tả, ghi chú |
| `nhan_vien.py` | `NhanVien` | `nhan_vien` | Lưu trữ nhân viên/người dùng: mã NV, họ tên, email, SĐT, vai trò, tài khoản, mật khẩu (mã hóa bcrypt), trạng thái, lần đăng nhập cuối |
| `system_log.py` | `SystemLog` | `system_log` | Lưu trữ nhật ký hệ thống: mã log, mã nhân viên, thời gian, hành động (thêm/sửa/xóa/đăng nhập/đăng xuất), bản ghi, giá trị cũ và mới (JSON), địa chỉ IP |
| `bao_cao.py` | `BaoCao` | `bao_cao` | Lưu trữ báo cáo: mã báo cáo, người tạo, loại báo cáo, ngày bắt đầu, ngày kết thúc, dữ liệu (JSON), đường dẫn file, trạng thái, ghi chú |
| `__init__.py` | — | — | File khởi tạo package, xuất tất cả mô hình và enum, thiết lập quan hệ giữa các mô hình (relationship) |

---

## 4. Tầng Dịch vụ (Services Layer)

Tầng dịch vụ nằm trong thư mục `src/services/` và chịu trách nhiệm xử lý toàn bộ logic nghiệp vụ của ứng dụng. Mỗi service tương ứng với một module chức năng và cung cấp các phương thức CRUD cũng như các thao tác nghiệp vụ phức tạp. Các service kế thừa từ `BaseService`, một lớp cơ sở cung cấp khả năng quản lý session và giao dịch (transaction).

Bảng dưới đây mô tả chi tiết từng file trong tầng dịch vụ:

| File | Lớp chính | Mô tả |
|---|---|---|
| `base_service.py` | `BaseService` | Lớp cơ sở trừu tượng cho tất cả service, quản lý session SQLAlchemy, hỗ trợ context manager và giao dịch (transaction) |
| `transaction_context.py` | `TransactionContext`, `transactional` | Quản lý giao dịch dùng chung cho nhiều service, đảm bảo tính nguyên tử (atomicity) qua decorator `@transactional` và đối tượng singleton `tx` |
| `auth/auth_service.py` | `AuthService` | Xác thực người dùng, kiểm tra tài khoản và mật khẩu (bcrypt), khóa tài khoản sau 5 lần sai, phân quyền dựa trên ma trận vai trò |
| `auth/authorization_service.py` | `AuthorizationService`, `Permission` | Kiểm soát truy cập dựa trên vai trò (RBAC) với ma trận quyền chi tiết cho từng module, lọc menu và nút theo quyền, kiểm tra quyền truy cập API |
| `auth/auth_middleware.py` | `AuthMiddleware` | Lớp trung gian xác thực, quản lý người dùng hiện tại, kiểm tra quyền truy cập view và button, hiển thị thông báo từ chối truy cập |
| `khach_hang_service.py` | `KhachHangService` | Quản lý khách hàng: CRUD, tìm kiếm, xóa mềm, kiểm tra email trùng, tạo mã KH tự động, xuất Excel, lấy lịch sử giao dịch |
| `kho_service.py` | `KhoService` | Quản lý kho: CRUD, tính tỷ lệ lấp đầy, thống kê vị trí theo trạng thái, cảnh báo kho quá tải, kiểm tra ràng buộc khi xóa |
| `vi_tri_service.py` | `ViTriService` | Quản lý vị trí lưu trữ: CRUD, tìm vị trí trống theo yêu cầu (diện tích, giá thuê), thống kê số lượng và tỷ lệ sử dụng |
| `hop_dong_service.py` | `HopDongService` | Quản lý hợp đồng: CRUD, gia hạn, chấm dứt, cập nhật trạng thái, tính ngày còn lại, thống kê, kiểm tra ràng buộc (không xóa nếu có thanh toán), tự động tạo mã HD |
| `hop_dong_history_service.py` | `HopDongHistoryService`, `HopDongHistory`, `EventType` | Theo dõi lịch sử hợp đồng: tổng hợp sự kiện từ nhiều bảng (tạo, gia hạn, chấm dứt, thanh toán, hàng hóa), thống kê lịch sử |
| `hang_hoa_service.py` | `HangHoaService` | Quản lý hàng hóa: CRUD, nhập hàng, xuất hàng (có khóa dòng), cảnh báo tồn thấp, tính tổng giá trị, thống kê tồn kho theo loại |
| `thanh_toan_service.py` | `ThanhToanService` | Quản lý thanh toán: CRUD, đánh dấu đã thanh toán, tự động phát hiện quá hạn, tính tổng đã thanh toán và còn nợ, tạo lịch thanh toán định kỳ tự động |
| `loai_hang_service.py` | `LoaiHangService` | Quản lý loại hàng: CRUD, tìm kiếm, tạo mã loại tự động, kiểm tra trùng lặp |
| `inventory_service.py` | `InventoryService`, `StockAlertLevel`, `StockAlert` | Kiểm kê tồn kho: theo dõi mức tồn, cảnh báo theo ngưỡng (OK/LOW/CRITICAL/EMPTY), định giá tồn kho, tạo báo cáo tồn kho, thống kê dashboard |
| `report_service.py` | `ReportService`, `ReportType` | Tổng hợp báo cáo: thống kê dashboard tổng quan, tạo báo cáo tóm tắt, xuất báo cáo ra file văn bản, tổng hợp dữ liệu từ nhiều service khác |
| `users/user_service.py` | `UserService` | Quản lý người dùng: CRUD nhân viên, thay đổi mật khẩu, phân quyền, tìm kiếm, tạo mã NV tự động, xác thực dữ liệu đầu vào |
| `pdf/pdf_generation_service.py` | `PDFGenerationService` | Tạo tài liệu PDF sử dụng ReportLab: hợp đồng thuê kho (thông tin hợp đồng, khách hàng, vị trí, điều khoản), hóa đơn thanh toán (thông tin hóa đơn, dịch vụ, thuế, tổng thanh toán), báo cáo tổng hợp (số liệu thống kê, cảnh báo, khuyến nghị). Hỗ trợ font tiếng Việt |

---

## 5. Tầng Giao diện (GUI Layer)

Tầng giao diện nằm trong thư mục `src/gui/` và được xây dựng hoàn toàn bằng PyQt6. Cấu trúc được tổ chức thành năm nhóm chính: views (các màn hình chính), forms (các biểu mẫu nhập liệu), dialogs (các hộp thoại dùng chung), widgets (các thành phần giao diện tái sử dụng) và wizards (các trình hướng dẫn nhiều bước).

### 5.1. Views

Các view là những màn hình chính của ứng dụng, mỗi view tương ứng với một module chức năng:

| File | Lớp | Mô tả |
|---|---|---|
| `views/auth/login_view.py` | `LoginView` | Màn hình đăng nhập với trường tên đăng nhập, mật khẩu, hộp kiểm ghi nhớ đăng nhập. Xác thực người dùng và chuyển đến màn hình chính khi thành công |
| `views/dashboard_view.py` | `DashboardView` | Trang tổng quan hệ thống: hiển thị bốn chỉ số chính (tổng kho, kho hoạt động, tổng vị trí, vị trí trống), thanh tỷ lệ lấp đầy, biểu đồ tròn phân bổ trạng thái kho, biểu đồ cột so sánh tỷ lệ lấp đầy, bảng thống kê kho chi tiết, khu vực cảnh báo kho quá tải. Tự động làm mới dữ liệu mỗi 30 giây |
| `views/khach_hang_view.py` | `KhachHangView` | Quản lý khách hàng: bảng dữ liệu khách hàng với thanh tìm kiếm, bộ lọc theo loại và trạng thái, thêm/sửa/xóa, xuất Excel |
| `views/khach_hang_detail_view.py` | `KhachHangDetailView` | Chi tiết khách hàng với bốn tab: Thông tin (thông tin cơ bản và thống kê), Hợp đồng (danh sách hợp đồng), Thanh toán (lịch sử thanh toán), Lịch sử (lịch sử giao dịch) |
| `views/kho_view.py` | `KhoView` | Quản lý kho: bảng dữ liệu kho với thanh thống kê (tổng kho, hoạt động, tỷ lệ lấp đầy trung bình), bộ lọc trạng thái, thêm/sửa/xóa, xuất Excel |
| `views/vi_tri_view.py` | `ViTriView` | Quản lý vị trí lưu trữ: chọn kho từ dropdown, bảng vị trí với thống kê (tổng, trống, đã thuê, tỷ lệ trống), bộ lọc trạng thái, thêm/sửa/xóa, xuất Excel |
| `views/hop_dong_view.py` | `HopDongView` | Quản lý hợp đồng: bảng hợp đồng với thống kê (tổng, hiệu lực, sắp hết hạn, hết hạn), tìm kiếm và lọc theo trạng thái, ngày tháng, thêm/sửa/xóa, cập nhật trạng thái, gia hạn, chấm dứt, xuất Excel và PDF |
| `views/hop_dong_detail_view.py` | `HopDongDetailView` | Chi tiết hợp đồng với bốn tab: Thông tin (thông tin hợp đồng, khách hàng, vị trí, tài chính), Hàng hóa (danh sách hàng hóa), Thanh toán (lịch sử thanh toán), Lịch sử (các sự kiện trong vòng đời hợp đồng) |
| `views/hang_hoa_view.py` | `HangHoaView` | Quản lý hàng hóa: bảng hàng hóa với thống kê (tổng mặt hàng, tổng số lượng, sắp hết, tổng giá trị), bộ lọc theo hợp đồng/loại/trạng thái, thêm/sửa/xóa, quản lý loại hàng, cập nhật trạng thái, xuất Excel |
| `views/thanh_toan_view.py` | `ThanhToanView` | Quản lý thanh toán: bảng thanh toán với thống kê (tổng hóa đơn, đã thanh toán, còn nợ), tìm kiếm và lọc theo trạng thái, thêm/sửa/xóa, xuất Excel |
| `views/bao_cao_view.py` | `BaoCaoView` | Báo cáo và thống kê: bốn chỉ số tóm tắt (doanh thu tháng, hợp đồng đang hoạt động, hợp đồng sắp hết hạn, tổng khách hàng), biểu đồ doanh thu theo tháng, danh sách 10 hợp đồng gần đây, xuất Excel |
| `views/settings_view.py` | `SettingsView` | Cài đặt hệ thống với bốn thẻ (card): Hiển thị (số mục/trang, xác nhận khi xóa, gợi ý, tự động làm mới), Thông báo (cảnh báo tồn thấp, hợp đồng hết hạn), Dữ liệu (tự động sao lưu, đường dẫn), Tài khoản (thông tin người dùng, đổi mật khẩu) |
| `views/help_view.py` | `HelpView` | Trợ giúp với ba tab: Hướng dẫn sử dụng (hướng dẫn chi tiết từng chức năng), Phím tắt (danh sách phím tắt toàn cục), Về chúng tôi (giới thiệu phần mềm, công nghệ, thành viên nhóm) |
| `views/users/user_view.py` | `UserView` | Quản lý người dùng (dành cho quản trị viên): bảng nhân viên, thêm/sửa/vô hiệu hóa tài khoản, kiểm tra quyền truy cập |

### 5.2. Forms

Các form là những hộp thoại nhập liệu cho từng đối tượng nghiệp vụ:

| File | Lớp | Mô tả |
|---|---|---|
| `forms/khach_hang_form.py` | `KhachHangForm` | Form nhập thông tin khách hàng: họ tên, loại KH, SĐT, email, địa chỉ, mã số thuế, trạng thái |
| `forms/kho_form.py` | `KhoForm` | Form nhập thông tin kho: tên kho, địa chỉ, diện tích, sức chứa, trạng thái |
| `forms/vi_tri_form.py` | `ViTriForm` | Form nhập thông tin vị trí: chọn kho, khu vực, hàng, tầng, diện tích, giá thuê, sức chứa, trạng thái |
| `forms/hop_dong_form.py` | `HopDongForm` | Form tạo hợp đồng: chọn khách hàng (QComboBox), chọn vị trí trống (QListWidget), nhập ngày bắt đầu/kết thúc, giá thuê, tiền cọc, phương thức thanh toán, điều khoản |
| `forms/hang_hoa_form.py` | `HangHoaForm` | Form nhập hàng hóa: tên hàng, loại hàng, số lượng, đơn vị tính, trọng lượng, kích thước, giá trị, chọn hợp đồng |
| `forms/thanh_toan_form.py` | `ThanhToanForm` | Form thanh toán: chọn hợp đồng, loại phí, số tiền, kỳ thanh toán, ngày đến hạn, phương thức, ghi chú |
| `forms/loai_hang_form.py` | `LoaiHangForm` | Form quản lý loại hàng: thêm, sửa, xóa danh mục loại hàng |
| `forms/phieu_nhap_form.py` | `PhieuNhapForm` | Form nhập kho: thông tin phiếu nhập hàng |
| `forms/phieu_xuat_form.py` | `PhieuXuatForm` | Form xuất kho: thông tin phiếu xuất hàng |
| `forms/users/user_form.py` | `UserForm` | Form người dùng: họ tên, email, SĐT, tài khoản, mật khẩu, vai trò, trạng thái |

### 5.3. Dialogs

Các hộp thoại dùng chung cho toàn ứng dụng:

| File | Lớp | Mô tả |
|---|---|---|
| `dialogs/dialogs.py` | `MessageDialog` | Hộp thoại thông báo: hỗ trợ bốn loại (info, warning, error, success) với biểu tượng và nút OK |
| `dialogs/dialogs.py` | `ConfirmDialog` | Hộp thoại xác nhận: hỗ trợ xác nhận thường và xác nhận nguy hiểm (xóa), tùy chỉnh tiêu đề và nút |
| `dialogs/dialogs.py` | `InputDialog` | Hộp thoại nhập liệu: hỗ trợ nhập văn bản (một hoặc nhiều dòng), số (nguyên/thập phân), ngày tháng |
| `dialogs/dialogs.py` | `ProgressDialog` | Hộp thoại tiến trình: hiển thị thanh tiến trình (xác định hoặc bất định) và nút hủy |
| `dialogs/dialogs.py` | `FormDialog` | Hộp thoại động: tự động tạo form dựa trên danh sách trường (văn bản, số, ngày, combobox, textarea) |
| `dialogs/change_password_dialog.py` | `ChangePasswordDialog` | Hộp thoại đổi mật khẩu: nhập mật khẩu cũ, mật khẩu mới, xác nhận mật khẩu, kiểm tra độ mạnh mật khẩu |

### 5.4. Widgets

Các thành phần giao diện tái sử dụng:

| File | Lớp | Mô tả |
|---|---|---|
| `widgets/data_table.py` | `DataTable` | Bảng dữ liệu nâng cao: sắp xếp theo cột, tìm kiếm, phân trang, chọn dòng, menu ngữ cảnh, lưu dữ liệu dòng trong vai trò người dùng |
| `widgets/data_table.py` | `DataTableWithToolbar` | Bảng dữ liệu kèm thanh công cụ: tìm kiếm, chọn cột, nút Thêm/Sửa/Xóa/Làm mới/Xuất Excel, điều khiển phân trang |
| `widgets/buttons.py` | `PrimaryButton`, `SecondaryButton`, `DangerButton`, `IconButton`, `ToggleButton`, `LoadingButton` | Bộ sưu tập nút bấm tùy chỉnh: nút chính (xanh), nút phụ (xám), nút nguy hiểm (đỏ), nút biểu tượng, nút bật/tắt, nút tải (có hiệu ứng loading) |
| `widgets/buttons.py` | `ButtonGroup` | Nhóm nút: sắp xếp các nút theo chiều ngang hoặc dọc, hỗ trợ thêm nhanh các loại nút |
| `widgets/search_box.py` | `SearchBox` | Hộp tìm kiếm: biểu tượng kính lúp, nút xóa, lịch sử tìm kiếm (20 từ khóa), tự động hoàn thành, gửi tín hiệu sau 300ms dừng gõ |
| `widgets/search_box.py` | `AdvancedSearchBox` | Tìm kiếm nâng cao: kết hợp SearchBox với các bộ lọc QComboBox động, gửi tín hiệu từ điển tìm kiếm |
| `widgets/charts.py` | `PieChartCanvas` | Biểu đồ tròn Matplotlib: hiển thị phân bổ dữ liệu với nhãn và tỷ lệ phần trăm |
| `widgets/charts.py` | `BarChartCanvas` | Biểu đồ cột: hỗ trợ chiều dọc và ngang, hiển thị nhãn giá trị trên cột |
| `widgets/charts.py` | `FillRateBarChart` | Biểu đồ tỷ lệ lấp đầy: biểu đồ cột ngang chuyên biệt cho kho, tự động tô màu theo phần trăm (xanh-vàng-đỏ) |
| `widgets/loading.py` | `LoadingSpinner`, `LoadingOverlay`, `LoadingProgressBar`, `LoadingDialog` | Bộ thành phần tải: spinner quay, lớp phủ toàn màn hình, thanh tiến trình (xác định/bất định), hộp thoại tải |
| `widgets/loading.py` | `ProgressStep`, `ProgressStepper` | Trình tự bước: hiển thị tiến trình nhiều bước với số thứ tự, đường kết nối, trạng thái hoàn thành |

### 5.5. Wizards

Các trình hướng dẫn nhiều bước cho thao tác phức tạp:

| File | Lớp | Mô tả |
|---|---|---|
| `wizards/renewal_wizard.py` | `RenewalWizard` | Trình hướng dẫn gia hạn hợp đồng ba bước: Trang 1 (RenewalIntroPage) hiển thị thông tin hợp đồng hiện tại; Trang 2 (RenewalTermsPage) nhập số tháng gia hạn và giá thuê mới, xem trước ngày kết thúc và tổng tiền; Trang 3 (RenewalConfirmPage) tóm tắt thay đổi và xác nhận |
| `wizards/termination_wizard.py` | `TerminationWizard` | Trình hướng dẫn chấm dứt hợp đồng ba bước: Trang 1 chọn lý do chấm dứt (khách yêu cầu, vi phạm, không thanh toán, lý do khác); Trang 2 chọn mức phạt (theo tháng hoặc % tiền cọc), tự động tính tiền phạt và tiền hoàn lại; Trang 3 tóm tắt và xác nhận |

### 5.6. Các file GUI khác

| File | Mô tả |
|---|---|
| `navigation.py` | Hệ thống điều hướng: NavigationHistory (quản lý lịch sử điều hướng), NavigationManager (quản lý QStackedWidget và tín hiệu chuyển view), BreadcrumbWidget (thanh điều hướng breadcrumb), SidebarMenu (menu bên trái), NavigationPanel (tích hợp tất cả thành phần điều hướng) |
| `styles/main.qss` | Tệp tin stylesheet QSS cho toàn bộ giao diện: định nghĩa màu sắc, font chữ, khoảng cách, hiệu ứng hover cho tất cả widget |
| `main.py` | File khởi tạo ứng dụng PyQt6 (đặt trong package gui) |
| `main_app.py` | Lớp MainApplication trong package gui |
| `main_window.py` | Lớp MainWindow trong package gui |

---

## 6. Tầng Dữ liệu (Database Layer)

Tầng dữ liệu nằm trong thư mục `src/database/` và `src/data/`, chịu trách nhiệm kết nối, quản lý và vận hành cơ sở dữ liệu:

| File | Lớp/Hàm | Mô tả |
|---|---|---|
| `database/connection.py` | `DatabaseConnection` | Quản lý kết nối SQLite sử dụng Singleton Pattern, tạo engine SQLAlchemy với `check_same_thread=False` và `pool_pre_ping=True`. Cung cấp `get_session()` để lấy session và `session_scope()` (context manager) để tự động commit/rollback/close |
| `database/repository.py` | `BaseRepository` | Lớp repository cơ sở với các thao tác CRUD generic: create, get_by_id, get_all, update, delete, count, exists |
| `database/repository.py` | `SoftDeleteRepository` | Repository mở rộng hỗ trợ xóa mềm: cập nhật trạng thái thành 'da_xoa' thay vì xóa thực, có phương thức lọc bản ghi đang hoạt động |
| `database/repository.py` | `TimestampRepository` | Repository mở rộng tự động quản lý ngày tạo và ngày cập nhật khi thực hiện CRUD |
| `database/migrate.py` | (CLI script) | Công cụ quản lý migration: init (tạo thư mục migration), create (tạo file migration mới với timestamp), upgrade (áp dụng migration), status (xem trạng thái). Migration files được lưu tại `migrations/versions/` |
| `database/README.md` | — | Tài liệu hướng dẫn chi tiết về tầng dữ liệu: cách sử dụng session_scope, repository pattern, models, migration, xử lý sự cố |
| `data/database.py` | `init_db()`, `create_indexes()`, `create_views()`, `create_sample_data()` | Khởi tạo cơ sở dữ liệu: tạo bảng từ SQLAlchemy models, tạo chỉ mục (hơn 20 chỉ mục cho các bảng), tạo view (hợp đồng sắp hết hạn, công nợ chưa thanh toán, tỷ lệ lấp đầy kho), tạo dữ liệu mẫu (tài khoản admin, một kho, hai vị trí, một khách hàng) |
| `data/init_db.py` | — | Tập lệnh khởi tạo cơ sở dữ liệu độc lập: có thể chạy bằng `python src/data/init_db.py`, gọi hàm main từ `src.data.database` |
| `data/schema.sql` | — | Định nghĩa schema cơ sở dữ liệu bằng SQL thuần: 11 bảng (khach_hang, kho, vi_tri, hop_dong, hang_hoa, loai_hang, thanh_toan, nhan_vien, system_log, bao_cao), chỉ mục, view và dữ liệu mẫu |

---

## 7. Tầng Tiện ích (Utils Layer)

Tầng tiện ích nằm trong thư mục `src/utils/` và cung cấp các hàm dùng chung cho toàn bộ ứng dụng:

| File | Mô tả |
|---|---|
| `validators.py` | Bộ xác thực dữ liệu: xác thực email (regex, độ dài), số điện thoại Việt Nam (các định dạng 0xx, 84xx, +84xx), trường bắt buộc, độ dài chuỗi, số (trong khoảng), ngày tháng, khoảng ngày, tiền tệ (số dương, tối đa 2 số thập phân), mật khẩu (tối thiểu 8 ký tự, có chữ và số). Hỗ trợ xác thực form tổng thể với từ điển lỗi chi tiết |
| `formatters.py` | Bộ định dạng dữ liệu: định dạng tiền tệ (vi_VN và en_US), số (số thập phân, phân cách hàng nghìn), phần trăm, ngày tháng (nhiều mẫu dd/MM/yyyy, yyyy-MM-dd), giờ, kích thước file (B, KB, MB, GB), số điện thoại Việt Nam, địa chỉ (kết hợp các thành phần), tên (thứ tự họ-tên), khoảng thời gian (giờ:phút), cắt chuỗi, viết hoa chữ cái đầu, slugify |
| `helpers.py` | Bộ hàm trợ giúp đa năng: tạo mã duy nhất (với tiền tố, ngày, chuỗi ngẫu nhiên), tạo UUID, lấy đường dẫn thư mục dự án, sao lưu file với timestamp, dọn dẹp sao lưu cũ, đọc/ghi file JSON, tính tuổi, tính khoảng ngày, chia an toàn (xử lý chia cho 0), kẹp số, nội suy, hợp nhất từ điển đệ quy, làm phẳng từ điển, nhóm danh sách, sắp xếp, tìm kiếm, phân trang |
| `export_service.py` | Dịch vụ xuất Excel sử dụng pandas và openpyxl: xuất danh sách kho, danh sách vị trí, dashboard (ba sheet: Kho, Vị trí, Tổng hợp). File có định dạng chuyên nghiệp (font, căn chỉnh, viền, màu sắc), lưu tại data/exports/ với timestamp tự động |
| `hop_dong_alert.py` | Cảnh báo hợp đồng thông minh: phát hiện hợp đồng sắp hết hạn (dưới 30 ngày, dưới 7 ngày, quá hạn), phân loại cảnh báo theo mức ưu tiên (cao/trung bình/thấp), tạo báo cáo cảnh báo dạng văn bản, hỗ trợ gửi email/SMS (chờ triển khai) |
| `hop_dong_export.py` | Xuất hợp đồng: tạo bản xem trước HTML của hợp đồng (với CSS định dạng chuyên nghiệp), tính tổng tiền thuê theo thời gian, xuất hợp đồng ra file văn bản |
| `inventory_service.py` | Dịch vụ kiểm kê tồn kho (phiên bản trong utils): theo dõi mức tồn kho, xác định ngưỡng cảnh báo (OK >20, LOW 11-20, CRITICAL 1-10, EMPTY 0), tạo báo cáo tồn kho và báo cáo hàng sắp hết, thống kê dashboard |

---

## 8. Thư mục Kiểm thử (Tests)

Thư mục `tests/` chứa các bộ kiểm thử đơn vị và tích hợp cho ứng dụng, sử dụng pytest:

| File | Mô tả |
|---|---|
| `conftest.py` | Cấu hình chung cho pytest: fixture, session database, dữ liệu mẫu cho kiểm thử |
| `test_hang_hoa_service.py` | Kiểm thử dịch vụ hàng hóa: CRUD, nhập hàng, xuất hàng, cảnh báo tồn thấp |
| `test_hop_dong_alert.py` | Kiểm thử cảnh báo hợp đồng: phát hiện hợp đồng sắp hết hạn, quá hạn, phân loại ưu tiên |
| `test_hop_dong_components.py` | Kiểm thử các thành phần hợp đồng: xác thực dữ liệu, tính toán, ràng buộc |
| `test_hop_dong_service.py` | Kiểm thử dịch vụ hợp đồng: CRUD, gia hạn, chấm dứt, tính toán tài chính |
| `test_inventory_service.py` | Kiểm thử dịch vụ kiểm kê: tồn kho, cảnh báo, định giá, báo cáo |
| `test_kho_service.py` | Kiểm thử dịch vụ kho: CRUD, tỷ lệ lấp đầy, thống kê, cảnh báo quá tải |
| `test_vi_tri_service.py` | Kiểm thử dịch vụ vị trí: CRUD, tìm kiếm vị trí trống, thống kê |
| `test_models/test_kho_model.py` | Kiểm thử mô hình kho: xác thực thuộc tính, tính toán tỷ lệ lấp đầy |
| `test_services/test_khach_hang_service.py` | Kiểm thử dịch vụ khách hàng (trong package test_services) |
| `test_services/test_vi_tri_service.py` | Kiểm thử dịch vụ vị trí (trong package test_services) |
| `test_utils/test_formatters.py` | Kiểm thử các hàm định dạng: tiền tệ, ngày tháng, số |
| `test_utils/test_validators.py` | Kiểm thử các hàm xác thực: email, SĐT, mật khẩu, form |
| `test_integration/test_database_operations.py` | Kiểm thử tích hợp cơ sở dữ liệu: thao tác CRUD phức hợp, transaction, ràng buộc |

---

## 9. Các file cấu hình và hỗ trợ

| File | Mô tả |
|---|---|
| `main.py` (thư mục gốc) | File khởi động ứng dụng đầu tiên. Hiện tại chỉ hiển thị banner giới thiệu dự án và thông báo đang phát triển. Trong tương lai sẽ gọi `src.app.main()` để khởi chạy giao diện PyQt6 |
| `requirements.txt` | Danh sách thư viện Python cần cài đặt: PyQt6 (giao diện), SQLAlchemy (ORM), ReportLab (PDF), pandas+openpyxl (Excel), bcrypt (mã hóa mật khẩu), python-dateutil (xử lý ngày tháng), matplotlib (biểu đồ), pytest (kiểm thử) |
| `pytest.ini` | Cấu hình cho pytest: thiết lập tham số mặc định, đường dẫn, tùy chọn đầu ra |
| `.gitignore` | Danh sách file/thư mục được git bỏ qua: `__pycache__/`, `venv/`, `data/*.db`, `*.pyc` |
| `README.md` | Hướng dẫn tổng quan về dự án: giới thiệu, tính năng, công nghệ, cài đặt, hướng dẫn sử dụng, kiểm thử |
| `CHANGELOG.md` | Nhật ký thay đổi phiên bản: ghi lại các cập nhật, sửa lỗi, tính năng mới |
| `RELEASE_NOTES.md` | Ghi chú phát hành cho từng phiên bản |
| `scripts/seed_data.py` | Tập lệnh tạo dữ liệu mẫu cho cơ sở dữ liệu |
| `scripts/generate_class_diagram.py` | Tập lệnh tự động tạo sơ đồ lớp UML từ mã nguồn |
| `scripts/write_docs.py` | Tập lệnh tự động tạo tài liệu từ mã nguồn |
| `scripts/fix_enum_cases.py` | Tập lệnh sửa lỗi định dạng enum trong cơ sở dữ liệu |

---

## Tổng kết

Dự án Quản Lý Dịch Vụ Cho Thuê Kho Lưu Trữ Hàng Hóa được tổ chức theo kiến trúc ba lớp với tổng cộng hơn 80 file mã nguồn Python. Tầng mô hình (Models) định nghĩa 11 bảng dữ liệu với các quan hệ và ràng buộc, sử dụng SQLAlchemy ORM và Repository Pattern. Tầng dịch vụ (Services) triển khai 12 service chính, 3 service hỗ trợ (auth, pdf, users) và các công cụ quản lý giao dịch, đảm bảo logic nghiệp vụ được tách biệt hoàn toàn khỏi giao diện. Tầng giao diện (GUI) sử dụng PyQt6 với hơn 40 class view, form, dialog, widget và wizard, cung cấp trải nghiệm người dùng chuyên nghiệp. Kiến trúc này đảm bảo tính mô-đun hóa cao, dễ bảo trì và mở rộng, phù hợp với các dự án phần mềm có quy mô trung bình.
