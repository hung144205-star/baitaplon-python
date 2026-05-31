# Mô Tả Các Chức Năng Của Chương Trình

**Đề tài:** Quản Lý Dịch Vụ Cho Thuê Kho Lưu Trữ Hàng Hóa
**Nhóm thực hiện:** Nhóm 12 - Lập trình Python
**Ngày cập nhật:** 10/05/2026

---

## Mục lục

1. [Kiến trúc tổng quan hệ thống](#1-kiến-trúc-tổng-quan-hệ-thống)
2. [Chức năng Đăng nhập và Bảo mật](#2-chức-năng-đăng-nhập-và-bảo-mật)
3. [Chức năng Dashboard tổng quan](#3-chức-năng-dashboard-tổng-quan)
4. [Chức năng Quản lý Khách hàng](#4-chức-năng-quản-lý-khách-hàng)
5. [Chức năng Quản lý Kho](#5-chức-năng-quản-lý-kho)
6. [Chức năng Quản lý Vị trí lưu trữ](#6-chức-năng-quản-lý-vị-trí-lưu-trữ)
7. [Chức năng Quản lý Hợp đồng](#7-chức-năng-quản-lý-hợp-đồng)
8. [Chức năng Quản lý Hàng hóa](#8-chức-năng-quản-lý-hàng-hóa)
9. [Chức năng Quản lý Thanh toán](#9-chức-năng-quản-lý-thanh-toán)
10. [Chức năng Báo cáo và Thống kê](#10-chức-năng-báo-cáo-và-thống-kê)
11. [Chức năng Quản lý Người dùng](#11-chức-năng-quản-lý-người-dùng)
12. [Chức năng Cài đặt Hệ thống](#12-chức-năng-cài-đặt-hệ-thống)
13. [Chức năng Trợ giúp và Hướng dẫn](#13-chức-năng-trợ-giúp-và-hướng-dẫn)
14. [Chức năng Xuất dữ liệu](#14-chức-năng-xuất-dữ-liệu)
15. [Chức năng Cảnh báo Thông minh](#15-chức-năng-cảnh-báo-thông-minh)
16. [Sơ đồ Quy trình Nghiệp vụ Tổng thể](#16-sơ-đồ-quy-trình-nghiệp-vụ-tổng-thể)

---

## 1. Kiến trúc tổng quan hệ thống

Chương trình được thiết kế theo kiến trúc ba lớp (three-tier architecture) bao gồm tầng giao diện (PyQt6), tầng nghiệp vụ (Service Layer) và tầng dữ liệu (SQLAlchemy ORM + SQLite). Tầng giao diện chứa các view, form, dialog và widget trong thư mục src/gui/. Tầng nghiệp vụ chứa các service xử lý logic như AuthService, KhachHangService, KhoService, HopDongService, HangHoaService, ThanhToanService, ReportService, PDFGenerationService, UserService và InventoryService. Tầng dữ liệu sử dụng SQLAlchemy ORM kết nối SQLite với Repository Pattern tại src/database/.

Sơ đồ kiến trúc hệ thống:

```
+-----------------------------------------------------------+
|              Tầng Giao diện (GUI Layer)                     |
| PyQt6: Views, Forms, Dialogs, Wizards, Widgets, QSS        |
+---------------------------+-------------------------------+
                            |
+---------------------------v-------------------------------+
|              Tầng Nghiệp vụ (Service Layer)                 |
| Auth, KhachHang, Kho, HopDong, HangHoa,                   |
| ThanhToan, Report, PDF, User, Inventory                    |
+---------------------------+-------------------------------+
                            |
       +--------------------+--------------------+
       |                    |                    |
+------v---------+ +--------v--------+ +--------v---------+
| SQLAlchemy ORM | | ReportLab (PDF) | | Validators       |
| SQLite + Repo  | | Pandas (Excel)  | | Formatters       |
| Migrate        | |                  | | Export Service   |
+----------------+ +-----------------+ +------------------+
```

---

## 2. Chức năng Đăng nhập và Bảo mật

Triển khai tại src/gui/views/auth/login_view.py và src/services/auth/auth_service.py. Khi khởi động chương trình, màn hình đăng nhập xuất hiện với hai trường nhập Tên đăng nhập và Mật khẩu cùng hộp kiểm Ghi nhớ đăng nhập. Luồng xử lý: Người dùng nhập thông tin, hệ thống kiểm tra dữ liệu không được để trống. AuthService.login(username, password) kiểm tra tài khoản tồn tại và đang hoạt động, kiểm tra số lần đăng nhập sai (tối đa 5 lần, nếu quá sẽ khóa 30 phút), xác minh mật khẩu bằng bcrypt. Nếu đúng, hệ thống tạo session token và chuyển đến MainWindow. Cơ chế Ghi nhớ đăng nhập lưu tên đăng nhập vào tệp JSON trong thư mục ẩn ~/.baitaplon/remember_me.json. Tài khoản mặc định là admin/admin123. Chức năng đổi mật khẩu thông qua ChangePasswordDialog tại src/gui/dialogs/change_password_dialog.py.

---

## 3. Chức năng Dashboard tổng quan

Triển khai tại src/gui/views/dashboard_view.py và src/gui/widgets/charts.py. Dashboard là màn hình đầu tiên sau đăng nhập, cung cấp cái nhìn tổng quan hệ thống.

| Thành phần | Mô tả | Dữ liệu hiển thị |
|---|---|---|
| Bốn chỉ số tổng quan | Ô thông tin nhanh đầu trang | Tổng số kho, Số kho đang hoạt động, Tổng vị trí, Vị trí trống |
| Thanh tỷ lệ lấp đầy | Thanh tiến trình | Phần trăm lấp đầy trung bình (xanh <50%, cam 50-75%, đỏ >75%) |
| Biểu đồ tròn | Phân bổ trạng thái kho | Tỷ lệ Hoạt động, Bảo trì, Ngừng |
| Biểu đồ cột | So sánh tỷ lệ lấp đầy | Từng kho với phần trăm tương ứng |
| Bảng thống kê kho | Danh sách chi tiết | Tên, Địa chỉ, Diện tích, Sức chứa, Tỷ lệ lấp đầy |
| Khu vực cảnh báo | Cảnh báo kho quá tải | Kho có tỷ lệ >90%, kèm nút Xem chi tiết |

Dashboard tự động làm mới dữ liệu sau mỗi 30 giây qua QTimer.

---

## 4. Chức năng Quản lý Khách hàng

Triển khai tại src/gui/views/khach_hang_view.py, khach_hang_detail_view.py và src/services/khach_hang_service.py. Bảng dữ liệu hiển thị: Mã KH, Họ tên, Loại, SĐT, Email, Trạng thái.

| Chức năng | Mô tả | Phương thức xử lý |
|---|---|---|
| Xem danh sách | Bảng dữ liệu tất cả khách hàng | load_data() từ KhachHangService.get_all() |
| Thêm mới | Form nhập: Họ tên, Loại (Cá nhân/Doanh nghiệp), SĐT, Email, Địa chỉ, MST | KhachHangForm + create() |
| Sửa | Cập nhật thông tin khách hàng | KhachHangForm + update() |
| Xóa | Xóa mềm (soft-delete) có xác nhận | delete() |
| Chi tiết | Giao diện 4 tab: Thông tin, Hợp đồng, Thanh toán, Lịch sử | KhachHangDetailView |
| Tìm kiếm | Theo tên, SĐT hoặc email | SearchBox + search() |
| Lọc | Theo Loại khách và Trạng thái | _apply_filters() |
| Xuất Excel | Danh sách ra file Excel | _on_export_clicked() |

---

## 5. Chức năng Quản lý Kho

Triển khai tại src/gui/views/kho_view.py và src/services/kho_service.py. Bảng dữ liệu hiển thị: Mã kho, Tên kho, Địa chỉ, Diện tích (m2), Sức chứa (m3), Diện tích đã dùng, Tỷ lệ lấp đầy (%), Số vị trí, Trạng thái.

| Chức năng | Mô tả |
|---|---|
| Thêm kho mới | KhoForm nhập tên, địa chỉ, diện tích, sức chứa |
| Sửa kho | Cập nhật thông tin qua KhoForm |
| Xóa kho | Xóa có xác nhận, kiểm tra ràng buộc |
| Thống kê | Tổng số kho, Số kho Hoạt động, Tỷ lệ lấp đầy trung bình |
| Tính tỷ lệ lấp đầy | Tự động tính phần trăm diện tích đã dùng |
| Tìm kiếm | Theo tên, mã hoặc địa chỉ |
| Lọc | Theo trạng thái: Tất cả, Hoạt động, Bảo trì, Ngừng |
| Xuất Excel | Danh sách kho ra Excel |

Quy trình thêm kho: Người dùng nhấn Thêm kho, KhoForm hiển thị, nhập dữ liệu, kiểm tra hợp lệ (tên không trống, diện tích và sức chứa phải dương), gọi KhoService.create(), lưu database, làm mới bảng.

---

## 6. Chức năng Quản lý Vị trí lưu trữ

Triển khai tại src/gui/views/vi_tri_view.py và src/services/vi_tri_service.py. Vị trí được tổ chức theo ba cấp: Khu vực (Zone), Hàng (Rack), Tầng (Shelf). Bảng dữ liệu hiển thị: Mã vị trí, Khu vực, Hàng, Tầng, Diện tích, Giá thuê/tháng, Trạng thái (Trống/Đã thuê/Bảo trì).

| Chức năng | Mô tả |
|---|---|
| Thêm vị trí | ViTriForm nhập thông tin trong kho cụ thể |
| Sửa vị trí | Cập nhật thông tin |
| Xóa vị trí | Xóa có xác nhận |
| Thống kê | Tổng vị trí, Vị trí trống, Vị trí đã thuê, Tỷ lệ trống |
| Lọc | Theo Trống, Đã thuê, Bảo trì |
| Tìm kiếm | Theo mã vị trí hoặc khu vực |
| Xuất Excel | Danh sách vị trí ra Excel |

Khi chọn một kho từ danh sách, các vị trí thuộc kho đó tự động tải và hiển thị. Mỗi vị trí có giá thuê riêng dùng để tính chi phí hợp đồng.

---

## 7. Chức năng Quản lý Hợp đồng

Module phức tạp nhất, triển khai tại hop_dong_view.py, hop_dong_detail_view.py, hop_dong_form.py, renewal_wizard.py, termination_wizard.py và hop_dong_service.py. Hợp đồng có các trạng thái: Hiệu lực, Hết hạn, Chấm dứt, Gia hạn.

| Chức năng | Mô tả |
|---|---|
| Tạo hợp đồng | HopDongForm: chọn khách hàng, vị trí, nhập ngày, giá thuê, tiền cọc, phương thức thanh toán |
| Sửa hợp đồng | Cập nhật thông tin |
| Xóa hợp đồng | Xóa có xác nhận |
| Chi tiết | 4 tab: Thông tin, Hàng hóa, Thanh toán, Lịch sử |
| Gia hạn | Wizard 3 bước: Xem thông tin, Nhập số tháng gia hạn và giá mới, Xác nhận |
| Chấm dứt | Wizard 3 bước: Chọn lý do, Tính tiền phạt, Xác nhận |
| Cập nhật trạng thái | Thay đổi trạng thái, xử lý riêng cho chấm dứt |
| Tìm kiếm | Theo mã HĐ, tên KH hoặc vị trí |
| Lọc | Theo trạng thái, khoảng thời gian |
| Xuất Excel | Danh sách hợp đồng ra Excel |
| Xuất PDF | Từng hợp đồng ra file PDF |

Quy trình tạo hợp đồng: Người dùng nhấn Tạo Hợp đồng, HopDongForm hiển thị lần lượt chọn Khách hàng (QComboBox), chọn Vị trí trống (QListWidget), nhập Ngày (QDateEdit), nhập Giá thuê và Tiền cọc (QDoubleSpinBox), chọn Phương thức thanh toán (QComboBox). Hệ thống kiểm tra: ngày kết thúc phải sau ngày bắt đầu, giá thuê và tiền cọc dương, vị trí còn trống. Nếu hợp lệ, HopDongService.create() tự động tạo mã hợp đồng, cập nhật vị trí thành Đã thuê, tạo lịch thanh toán định kỳ.

Quy trình gia hạn (RenewalWizard 3 bước): Trang 1 hiển thị thông tin hợp đồng hiện tại. Trang 2 nhập số tháng gia hạn (mặc định 12) và giá thuê mới, tự động tính ngày kết thúc mới và tổng tiền. Trang 3 tóm tắt thay đổi và yêu cầu xác nhận, sau đó gọi HopDongService.renew().

Quy trình chấm dứt (TerminationWizard 3 bước): Trang 1 chọn lý do (Khách hàng yêu cầu, Vi phạm, Không thanh toán, Lý do khác) và ghi chú. Trang 2 chọn mức phạt (theo tháng tiền thuê hoặc % tiền cọc), tự động tính tiền phạt và tiền hoàn lại. Trang 3 tóm tắt và xác nhận, sau đó gọi HopDongService.terminate(), cập nhật vị trí thành Trống.

---

## 8. Chức năng Quản lý Hàng hóa

Triển khai tại src/gui/views/hang_hoa_view.py và src/services/hang_hoa_service.py. Bảng dữ liệu hiển thị: Mã hàng, Tên hàng, Loại hàng, Số lượng, Đơn vị tính, Giá trị, Trạng thái (Trong kho/Đã xuất), Hợp đồng.

| Chức năng | Mô tả |
|---|---|
| Thêm hàng hóa | HangHoaForm nhập tên, loại, số lượng, đơn vị, giá trị, hợp đồng |
| Nhập hàng | Nhập hàng vào vị trí lưu trữ cụ thể |
| Xuất hàng | Xuất hàng với ghi chú lý do |
| Sửa hàng hóa | Cập nhật thông tin |
| Xóa hàng hóa | Xóa có xác nhận |
| Quản lý loại hàng | Thêm, sửa, xóa danh mục loại hàng qua LoaiHangForm |
| Cập nhật trạng thái | Trong kho/Đã xuất |
| Cảnh báo tồn thấp | Tự động cảnh báo khi số lượng dưới 10 |
| Thống kê | Tổng mặt hàng, Tổng số lượng, Sắp hết, Tổng giá trị |
| Tìm kiếm | Theo tên hoặc loại hàng |
| Lọc | Theo Hợp đồng, Loại hàng, Trạng thái |
| Xuất Excel | Danh sách ra Excel |

---

## 9. Chức năng Quản lý Thanh toán

Triển khai tại src/gui/views/thanh_toan_view.py và src/services/thanh_toan_service.py. Bảng dữ liệu hiển thị: Mã thanh toán, Hợp đồng, Kỳ thanh toán, Số tiền, Ngày đến hạn, Ngày thanh toán, Trạng thái (Đã thanh toán/Chưa thanh toán/Quá hạn).

| Chức năng | Mô tả |
|---|---|
| Tạo thanh toán | ThanhToanForm tạo phiếu thanh toán cho hợp đồng |
| Sửa thanh toán | Cập nhật thông tin |
| Xóa thanh toán | Xóa có xác nhận |
| Tự động lịch thanh toán | Khi tạo hợp đồng mới, tự động tạo các kỳ thanh toán định kỳ |
| Mark quá hạn | Tự động đánh dấu quá hạn dựa trên ngày hiện tại |
| Thống kê công nợ | Tổng hóa đơn, Đã thanh toán, Còn nợ (gồm nợ quá hạn) |
| Tìm kiếm | Theo mã hợp đồng hoặc tên khách hàng |
| Lọc | Đã thanh toán, Chưa thanh toán, Quá hạn |
| Xuất Excel | Danh sách ra Excel |

---

## 10. Chức năng Báo cáo và Thống kê

Triển khai tại src/gui/views/bao_cao_view.py kết nối với src/services/report_service.py và src/gui/widgets/charts.py.

| Thành phần | Mô tả |
|---|---|
| Bốn chỉ số tóm tắt | Doanh thu tháng, Hợp đồng đang hoạt động, Hợp đồng sắp hết hạn, Tổng khách hàng |
| Biểu đồ doanh thu | Biểu đồ cột doanh thu theo tháng |
| Hợp đồng gần đây | 10 hợp đồng mới nhất |
| Tải lại dữ liệu | Làm mới số liệu |
| Xuất Excel | Báo cáo tóm tắt ra Excel |

Xuất báo cáo PDF qua PDFGenerationService với ba loại:

| Loại PDF | Nội dung |
|---|---|
| Hợp đồng thuê kho | Thông tin hợp đồng, khách hàng, vị trí, điều khoản, chữ ký |
| Hóa đơn thanh toán | Thông tin hóa đơn, dịch vụ, thuế, tổng thanh toán, ngân hàng |
| Báo cáo tổng hợp | Số liệu KH, kho, hợp đồng, doanh thu, cảnh báo, khuyến nghị |

---

## 11. Chức năng Quản lý Người dùng

Triển khai tại src/gui/views/users/user_view.py và src/services/users/user_service.py. Dành cho quản trị viên quản lý tài khoản nhân viên. Bảng dữ liệu hiển thị: Mã NV, Họ tên, Email, SĐT, Vai trò, Trạng thái.

| Chức năng | Mô tả | Yêu cầu quyền |
|---|---|---|
| Xem danh sách | Hiển thị tất cả nhân viên | Xem danh sách |
| Thêm người dùng | UserForm tạo tài khoản mới | create_user |
| Sửa thông tin | Cập nhật và phân quyền | edit_user |
| Vô hiệu hóa | Ngừng hoạt động tài khoản | delete_user |

Ma trận phân quyền bốn vai trò:

| Vai trò | Quyền hạn |
|---|---|
| Quản trị | Toàn quyền tất cả chức năng |
| Kinh doanh | Quản lý KH, hợp đồng, báo cáo |
| Kho | Quản lý kho, vị trí, hàng hóa |
| Kế toán | Quản lý thanh toán, xem báo cáo |

---

## 12. Chức năng Cài đặt Hệ thống

Triển khai tại src/gui/views/settings_view.py. Giao diện dạng thẻ (card-based) với bốn nhóm thiết lập:

| Nhóm cài đặt | Các thiết lập |
|---|---|
| Hiển thị | Số mục/trang, Xác nhận khi xóa, Gợi ý di chuột, Tự động làm mới |
| Thông báo | Cảnh báo hàng sắp hết, Cảnh báo hợp đồng hết hạn, Số ngày cảnh báo |
| Dữ liệu | Tự động sao lưu, Đường dẫn thư mục sao lưu |
| Tài khoản | Thông tin người dùng, Nút Đổi mật khẩu |

Các thao tác: Lưu cài đặt ghi lại thiết lập hiện tại. Khôi phục mặc định đưa về giá trị ban đầu (có xác nhận). Đổi mật khẩu mở ChangePasswordDialog.

---

## 13. Chức năng Trợ giúp và Hướng dẫn

Triển khai tại src/gui/views/help_view.py với ba tab. Tab "Hướng dẫn sử dụng" cung cấp hướng dẫn chi tiết cho sáu chức năng chính: Đăng nhập, Quản lý Khách hàng, Quản lý Kho, Quản lý Hợp đồng, Nhập/Xuất Hàng hóa và Thanh toán, kèm giải thích các trạng thái và thuật ngữ. Tab "Phím tắt" hiển thị danh sách phím tắt (Điều hướng: Ctrl + chữ cái mở module; Thao tác: Ctrl+S lưu, Ctrl+F tìm, Ctrl+N tạo mới; Bảng: Enter xem chi tiết, Delete xóa, Escape đóng). Tab "Về chúng tôi" giới thiệu phần mềm, công nghệ sử dụng và thành viên nhóm.

---

## 14. Chức năng Xuất dữ liệu

Hỗ trợ hai định dạng PDF và Excel, triển khai tại src/services/pdf/pdf_generation_service.py và src/utils/export_service.py.

Xuất PDF dùng ReportLab hỗ trợ font tiếng Việt (DejaVu Sans, Arial, Tahoma), gồm: hợp đồng thuê kho (thông tin hợp đồng, khách hàng, vị trí, điều khoản), hóa đơn thanh toán (dịch vụ, thuế, ngân hàng), báo cáo tổng hợp (số liệu, cảnh báo, khuyến nghị). File lưu tại data/exports/pdf/.

Xuất Excel dùng Pandas và OpenPyXL, gồm: danh sách kho, danh sách vị trí, Dashboard (ba sheet: Kho, Vị trí, Tổng hợp). File có định dạng chuyên nghiệp (font, căn chỉnh, viền, màu sắc), lưu tại data/exports/ với timestamp tự động.

Bảng tổng hợp các chức năng xuất:

| Chức năng xuất | Định dạng | Dữ liệu xuất |
|---|---|---|
| Xuất hợp đồng | PDF | Thông tin hợp đồng, khách hàng, vị trí, điều khoản |
| Xuất hóa đơn | PDF | Thông tin hóa đơn, dịch vụ, thuế, ngân hàng |
| Xuất báo cáo tổng hợp | PDF | Số liệu thống kê, cảnh báo, khuyến nghị |
| Xuất danh sách kho | Excel | Thông tin các kho |
| Xuất danh sách vị trí | Excel | Thông tin các vị trí lưu trữ |
| Xuất Dashboard | Excel | 3 sheet: Kho, Vị trí, Tổng hợp |
| Xuất danh sách khách hàng | Excel | Thông tin khách hàng |
| Xuất danh sách hợp đồng | Excel | Thông tin hợp đồng |
| Xuất danh sách thanh toán | Excel | Thông tin thanh toán |
| Xuất danh sách hàng hóa | Excel | Thông tin hàng hóa |

---

## 15. Chức năng Cảnh báo Thông minh

Triển khai tại src/utils/hop_dong_alert.py và src/services/inventory_service.py. Ba loại cảnh báo hợp đồng theo mức ưu tiên:

| Mức ưu tiên | Điều kiện | Loại cảnh báo |
|---|---|---|
| Cao | Hợp đồng đã quá hạn | Overdue alert |
| Cao | Hợp đồng còn dưới 7 ngày | Expiring soon |
| Trung bình | Hợp đồng còn 7-30 ngày | Expiring soon |
| Thấp | Hợp đồng còn trên 30 ngày | Cảnh báo nhẹ |

HopDongAlertService cung cấp phương thức truy vấn hợp đồng sắp hết hạn, hết hạn hôm nay, đã quá hạn; tổng hợp và phân loại cảnh báo theo ưu tiên. Hỗ trợ xuất báo cáo cảnh báo ra tệp văn bản và các phương thức gửi email/SMS (chờ triển khai). Cảnh báo tồn kho: hàng dưới 10 đơn vị được đánh dấu "sắp hết". Dashboard cảnh báo kho có tỷ lệ lấp đầy trên 90% (quá tải) kèm nút Xem chi tiết.

---

## 16. Sơ đồ Quy trình Nghiệp vụ Tổng thể

```
                          BAT DAU
                             |
                             v
              +-------------------------------+
              |        DANG NHAP               |
              | AuthService.xac thuc           |
              | Tao session token              |
              +-------------------------------+
                             |
                             v
              +-------------------------------+
              |  QUAN LY KHACH HANG            |
              | Them moi, cap nhat, tim kiem   |
              | Phan loai: Ca nhan/Doanh nghiep|
              +-------------------------------+
                             |
                             v
              +-------------------------------+
              |  QUAN LY KHO & VI TRI          |
              | Them kho, tao vi tri luu tru   |
              | Khu vuc - Hang - Tang          |
              +-------------------------------+
                             |
                             v
              +-------------------------------+
              |  TAO HOP DONG THUE             |
              | Chon KH + Vi tri + Ngay + Gia |
              | Tu dong tao lich thanh toan   |
              | Cap nhat vi tri: Da thue     |
              +-------------------------------+
                             |
           +-----------------+-----------------+
           |                 |                 |
           v                 v                 v
+----------------+ +--------------+ +----------------+
| NHAP/XUAT HANG | | THANH TOAN  | | GIA HAN/CHAM  |
| Nhap vao vi tri| | Tao phieu   | | DUT (Wizard)   |
| Xuat khoi kho | | Theo doi no | | 3 buoc         |
| Canh bao ton   | | Phat hien   | | Tinh tien phat |
| kho thap       | | qua han     | |                |
+----------------+ +--------------+ +----------------+
           |                 |                 |
           +-----------------+-----------------+
                             |
                             v
              +-------------------------------+
              |  BAO CAO & THONG KE            |
              | Dashboard, Bieu do, Xuat PDF   |
              | Xuat Excel                     |
              +-------------------------------+
                             |
                             v
              +-------------------------------+
              |  CANH BAO & THEO DOI           |
              | HD sap het han, Kho qua tai    |
              | Hang sap het, Cong no qua han  |
              +-------------------------------+
                             |
                             v
              +-------------------------------+
              |  KET THUC HOP DONG             |
              | Het han / Cham dut             |
              | Cap nhat vi tri: Trong        |
              | Luu lich su                    |
              +-------------------------------+
                             |
                             v
                          KET THUC
```

---

## Bảng Tổng Kết Các Chức Năng

| STT | Module | View chính | Service chính |
|---|---|---|---|
| 1 | Đăng nhập & Bảo mật | LoginView | AuthService |
| 2 | Dashboard | DashboardView | KhoService, ViTriService |
| 3 | Quản lý Khách hàng | KhachHangView | KhachHangService |
| 4 | Quản lý Kho | KhoView | KhoService |
| 5 | Quản lý Vị trí | ViTriView | ViTriService |
| 6 | Quản lý Hợp đồng | HopDongView | HopDongService |
| 7 | Quản lý Hàng hóa | HangHoaView | HangHoaService |
| 8 | Quản lý Thanh toán | ThanhToanView | ThanhToanService |
| 9 | Báo cáo & Thống kê | BaoCaoView | ReportService |
| 10 | Quản lý Người dùng | UserView | UserService |
| 11 | Cài đặt Hệ thống | SettingsView | — |
| 12 | Trợ giúp | HelpView | — |

| STT | Chức năng hỗ trợ | File triển khai | Mô tả |
|---|---|---|---|
| 1 | Xuất PDF | pdf_generation_service.py | Hợp đồng, hóa đơn, báo cáo tổng hợp |
| 2 | Xuất Excel | export_service.py | Danh sách và số liệu thống kê |
| 3 | Cảnh báo hợp đồng | hop_dong_alert.py | Phân loại và theo dõi cảnh báo |
| 4 | Kiểm tra tồn kho | inventory_service.py | Cảnh báo tồn kho thấp |
| 5 | Wizard gia hạn | renewal_wizard.py | Gia hạn hợp đồng 3 bước |
| 6 | Wizard chấm dứt | termination_wizard.py | Chấm dứt hợp đồng 3 bước |
| 7 | Chi tiết khách hàng | khach_hang_detail_view.py | 4 tab thông tin |
| 8 | Chi tiết hợp đồng | hop_dong_detail_view.py | 4 tab thông tin |
| 9 | Tìm kiếm | search_box.py | Tìm kiếm toàn bộ module |
| 10 | Bảng dữ liệu | data_table.py | Bảng tùy chỉnh với toolbar |

---

## Tài liệu tham khảo

1. PyQt6 Documentation: https://www.riverbankcomputing.com/static/Docs/PyQt6/
2. SQLAlchemy 2.0 Documentation: https://docs.sqlalchemy.org/en/20/
3. ReportLab User Guide: https://www.reportlab.com/docs/reportlab-userguide.pdf
4. pandas Documentation: https://pandas.pydata.org/docs/
5. Matplotlib Documentation: https://matplotlib.org/stable/contents.html
6. bcrypt Documentation: https://pypi.org/project/bcrypt/
7. pytest Documentation: https://docs.pytest.org/
