# Mô Tả Thiết Kế Giao Diện Người Dùng (GUI)

**Đề tài:** Quản Lý Dịch Vụ Cho Thuê Kho Lưu Trữ Hàng Hóa
**Nhóm thực hiện:** Nhóm 12 - Lập trình Python
**Ngày cập nhật:** 15/05/2026

---

## Mục lục

1. Tổng quan kiến trúc giao diện
2. Hệ thống điều hướng và bố cục chính
3. Chi tiết các màn hình chức năng
4. Hệ thống Form nhập liệu
5. Dialog và Wizard
6. Widget tái sử dụng
7. Hệ thống Stylesheet (QSS)

---

## 1. Tổng quan kiến trúc giao diện

Giao diện người dùng được xây dựng trên nền tảng PyQt6 và tổ chức theo mô hình thành phần phân cấp, với toàn bộ mã nguồn nằm trong thư mục `src/gui/`. Thư mục này được phân chia thành năm nhóm chính: `views/` chứa các màn hình chức năng, `forms/` chứa các biểu mẫu nhập liệu dạng hộp thoại, `dialogs/` chứa các hộp thoại dùng chung, `widgets/` chứa các thành phần giao diện tái sử dụng, và `wizards/` chứa các wizard đa bước. Kiến trúc tổng thể tuân theo mô hình ba lớp, trong đó tầng giao diện gọi đến tầng Service để xử lý nghiệp vụ và tầng Service gọi đến tầng Database thông qua SQLAlchemy ORM. Sơ đồ dưới đây mô tả cấu trúc tổng thể của `MainWindow`:

```
+-----------------------------------------------------------------------------+
|                          MainWindow (src/main_window.py)                     |
|  +------------------+  +--------------------------------------------------+  |
|  |  SidebarMenu     |  |  NavigationPanel                                 |  |
|  |  (Điều hướng)    |  |  +--------------------------------------------+ |  |
|  |                   |  |  | BreadcrumbWidget (Đường dẫn)                | |  |
|  |  - Dashboard      |  |  +--------------------------------------------+ |  |
|  |  - Khách hàng     |  |  +--------------------------------------------+ |  |
|  |  - Kho hàng       |  |  | QStackedWidget (Nội dung)                   | |  |
|  |  - Vị trí         |  |  |  DashboardView / KhachHangView              | |  |
|  |  - Hợp đồng       |  |  |  KhoView / ViTriView                       | |  |
|  |  - Hàng hóa       |  |  |  HopDongView / HangHoaView                 | |  |
|  |  - Thanh toán     |  |  |  ThanhToanView / BaoCaoView                | |  |
|  |  - Báo cáo        |  |  |  SettingsView / HelpView / UserView        | |  |
|  |  - Cài đặt        |  |  +--------------------------------------------+ |  |
|  |  - Trợ giúp       |  +--------------------------------------------------+  |
|  +------------------+                                                        |
|  +----------------------------------------------------------------------+    |
|  | StatusBar: [Module hiện tại] | [Người dùng] | [Thời gian thực]       |    |
|  +----------------------------------------------------------------------+    |
+-----------------------------------------------------------------------------+
```

Chương trình khởi động qua `main.py`, gọi `MainApp.main()` trong `src/main_app.py`. Đầu tiên, `LoginView` xuất hiện dưới dạng cửa sổ modal để xác thực người dùng. Sau khi đăng nhập thành công, `MainWindow` được hiển thị với giao diện chính hoàn chỉnh bao gồm thanh menu, thanh công cụ, khu vực trung tâm và thanh trạng thái.

---

## 2. Hệ thống điều hướng và bố cục chính

`MainWindow` kế thừa từ `QMainWindow` với kích thước mặc định 1280x800 pixel và được căn giữa màn hình khi khởi động. Cửa sổ quản lý bốn thành phần cấu trúc chính: thanh menu (`MenuBar`) với các mục Tệp tin, các module chức năng, Cài đặt và Trợ giúp; thanh công cụ (`ToolBar`) chứa các nút truy cập nhanh; khu vực trung tâm chứa `NavigationPanel`; và thanh trạng thái (`StatusBar`) hiển thị module đang hoạt động, tên người dùng hiện tại và thời gian thực được cập nhật qua `QTimer`.

`NavigationPanel` được xây dựng từ `src/gui/navigation.py` và là widget trung tâm điều phối việc chuyển đổi giữa các màn hình. Nó tích hợp ba thành phần chính: `SidebarMenu` hiển thị danh sách nút điều hướng dọc cho từng module với biểu tượng và nhãn; `BreadcrumbWidget` hiển thị đường dẫn điều hướng dạng breadcrumb cho phép người dùng nhấp vào các mục trước đó để quay lại; và `QStackedWidget` chứa tất cả các view và chỉ hiển thị một view tại một thời điểm. `NavigationManager` là bộ điều phối trung tâm với lịch sử điều hướng dạng ngăn xếp hỗ trợ thao tác tiến và lùi.

| Thành phần | Lớp | Tệp nguồn | Chức năng |
|---|---|---|---|
| Sidebar | `SidebarMenu` | navigation.py | Danh sách nút module dọc, phát tín hiệu khi chọn |
| Breadcrumb | `BreadcrumbWidget` | navigation.py | Hiển thị đường dẫn, cho phép nhấp để quay lại |
| Bộ điều phối | `NavigationManager` | navigation.py | Quản lý chuyển view và lịch sử tiến/lùi |
| Bộ chứa | `QStackedWidget` | navigation.py | Chứa toàn bộ view, hiển thị một view tại một thời điểm |

---

## 3. Chi tiết các màn hình chức năng

### 3.1 Màn hình Đăng nhập (LoginView)

`LoginView` trong `src/gui/views/auth/login_view.py` là màn hình đầu tiên người dùng nhìn thấy khi khởi động chương trình. Giao diện bao gồm hai trường nhập liệu cho tên đăng nhập và mật khẩu, một hộp kiểm "Ghi nhớ đăng nhập", và hai nút Đăng nhập và Hủy. `LoginView` phát tín hiệu `login_successful` kèm thông tin người dùng khi xác thực thành công và `login_cancelled` khi người dùng hủy. Cơ chế ghi nhớ đăng nhập lưu tên người dùng vào tệp JSON ẩn trong `~/.baitaplon/remember_me.json`. Hàm `show_login_dialog` bọc `LoginView` trong một `QDialog` modal để dễ dàng tích hợp.

### 3.2 Màn hình Dashboard (DashboardView)

`DashboardView` trong `src/gui/views/dashboard_view.py` là màn hình đầu tiên sau khi đăng nhập, cung cấp cái nhìn tổng quan trực quan về toàn bộ hệ thống. Phía trên cùng là bốn thẻ chỉ số tổng quan hiển thị tổng số kho, số kho đang hoạt động, tổng số vị trí và số vị trí trống. Bên dưới là một thanh tiến trình thể hiện tỷ lệ lấp đầy trung bình với mã màu xanh khi dưới 50%, cam khi từ 50% đến 75% và đỏ khi trên 75%. Kế tiếp là một biểu đồ tròn (`PieChartCanvas`) phân bổ trạng thái kho và một biểu đồ cột (`FillRateBarChart`) so sánh tỷ lệ lấp đầy giữa các kho. Phần cuối giao diện có bảng danh sách kho chi tiết và khu vực cảnh báo các kho có tỷ lệ lấp đầy trên 90% kèm nút xem chi tiết. Dashboard sử dụng `QTimer` để tự động làm mới dữ liệu sau mỗi 30 giây.

### 3.3 Màn hình Quản lý Khách hàng (KhachHangView và KhachHangDetailView)

`KhachHangView` trong `src/gui/views/khach_hang_view.py` là giao diện quản lý khách hàng chính với tiêu đề, thanh lọc gồm ô tìm kiếm (`SearchBox`), bộ lọc loại khách hàng và trạng thái, cùng bảng dữ liệu (`DataTableWithToolbar`) hiển thị các cột mã khách hàng, họ tên, loại, số điện thoại, email và trạng thái. Các thao tác thêm, sửa, xóa được thực hiện qua các nút trên thanh công cụ của bảng dữ liệu.

`KhachHangDetailView` trong `src/gui/views/khach_hang_detail_view.py` hiển thị thông tin chi tiết của một khách hàng qua giao diện bốn tab. Tab "Thông tin" trình bày hồ sơ khách hàng chi tiết cùng các thống kê như tổng hợp đồng, tổng thanh toán và công nợ. Tab "Hợp đồng" liệt kê các hợp đồng của khách hàng trong một `DataTable`. Tab "Thanh toán" hiển thị lịch sử thanh toán. Tab "Lịch sử" dành cho nhật ký giao dịch.

### 3.4 Màn hình Quản lý Kho hàng (KhoView)

`KhoView` trong `src/gui/views/kho_view.py` cung cấp giao diện quản lý danh sách kho hàng với tiêu đề, thanh thống kê ba chỉ số (tổng kho, kho hoạt động, tỷ lệ lấp đầy trung bình), thanh tìm kiếm và lọc theo trạng thái, và bảng dữ liệu hiển thị các cột mã kho, tên kho, địa chỉ, diện tích, sức chứa, diện tích đã dùng, tỷ lệ lấp đầy, số vị trí và trạng thái. `KhoView` hỗ trợ đầy đủ thêm, sửa, xóa, xuất Excel và kết nối với `KhoService` để thao tác dữ liệu.

### 3.5 Màn hình Quản lý Vị trí lưu trữ (ViTriView)

`ViTriView` trong `src/gui/views/vi_tri_view.py` quản lý các vị trí lưu trữ trong kho với tiêu đề, thanh thống kê (tổng vị trí, vị trí trống, vị trí đã thuê, tỷ lệ trống), bộ chọn kho (`QComboBox`) để lọc vị trí, thanh tìm kiếm và lọc trạng thái, cùng bảng dữ liệu hiển thị các cột mã vị trí, khu vực, hàng, tầng, diện tích, giá thuê và trạng thái. Khi người dùng chọn một kho từ danh sách, các vị trí thuộc kho đó tự động được tải và hiển thị.

### 3.6 Màn hình Quản lý Hợp đồng (HopDongView và HopDongDetailView)

`HopDongView` trong `src/gui/views/hop_dong_view.py` là màn hình phức tạp nhất, quản lý toàn bộ vòng đời hợp đồng thuê kho. Giao diện gồm tiêu đề, thanh thống kê bốn chỉ số (tổng hợp đồng, đang hiệu lực, sắp hết hạn, đã hết hạn), thanh lọc với ô tìm kiếm, bộ lọc trạng thái và khoảng thời gian, nút cập nhật trạng thái, và bảng dữ liệu hiển thị các cột mã hợp đồng, khách hàng, vị trí, ngày bắt đầu, ngày kết thúc, giá thuê, tiền cọc, trạng thái và số ngày còn lại. `HopDongView` cung cấp thêm nút xuất PDF cho từng hợp đồng và tích hợp hai wizard gia hạn và chấm dứt.

`HopDongDetailView` trong `src/gui/views/hop_dong_detail_view.py` là một `QDialog` hiển thị chi tiết hợp đồng qua bốn tab. Tab "Thông tin" trình bày đầy đủ thông tin hợp đồng, khách hàng, vị trí, ngày tháng và tài chính. Tab "Hàng hóa" liệt kê hàng hóa trong hợp đồng kèm tổng giá trị. Tab "Thanh toán" hiển thị lịch thanh toán với tổng số đã thanh toán và còn lại. Tab "Lịch sử" hiển thị dòng thời gian các sự kiện liên quan đến hợp đồng.

### 3.7 Màn hình Quản lý Hàng hóa (HangHoaView)

`HangHoaView` trong `src/gui/views/hang_hoa_view.py` quản lý hàng hóa lưu trữ trong kho với tiêu đề, thanh thống kê (tổng mặt hàng, tổng số lượng, sắp hết, tổng giá trị), thanh lọc với bộ lọc hợp đồng, loại hàng và trạng thái, ô tìm kiếm, và bảng dữ liệu hiển thị các cột mã hàng, tên hàng, loại hàng, số lượng, đơn vị tính, giá trị, trạng thái và hợp đồng. Các hàng hóa có số lượng dưới mười được đánh dấu cảnh báo bằng màu đỏ.

### 3.8 Màn hình Quản lý Thanh toán (ThanhToanView)

`ThanhToanView` trong `src/gui/views/thanh_toan_view.py` quản lý các khoản thanh toán với tiêu đề, thanh tóm tắt hiển thị tổng số hóa đơn, tổng tiền đã thanh toán và tổng tiền chưa thanh toán, ô tìm kiếm, bộ lọc trạng thái, và bảng dữ liệu hiển thị các cột mã thanh toán, hợp đồng, kỳ thanh toán, số tiền, ngày đến hạn, ngày thanh toán và trạng thái.

### 3.9 Màn hình Báo cáo và Thống kê (BaoCaoView)

`BaoCaoView` trong `src/gui/views/bao_cao_view.py` tổng hợp dữ liệu từ nhiều module với tiêu đề và nút làm mới, bốn thẻ chỉ số tóm tắt (doanh thu tháng, hợp đồng đang hoạt động, hợp đồng sắp hết hạn, tổng khách hàng), biểu đồ cột doanh thu theo tháng (`BarChartCanvas`), và bảng mười hợp đồng gần đây nhất. `BaoCaoView` cung cấp nút xuất báo cáo ra Excel và kết nối với `ReportService` cùng `HopDongService`.

### 3.10 Màn hình Cài đặt Hệ thống (SettingsView)

`SettingsView` trong `src/gui/views/settings_view.py` sử dụng thiết kế dạng thẻ (card-based) trong vùng cuộn (`QScrollArea`) với bốn thẻ cài đặt. Thẻ "Hiển thị" quản lý số mục trên trang, xác nhận khi xóa, gợi ý di chuột và tự động làm mới. Thẻ "Thông báo" quản lý cảnh báo hàng sắp hết, cảnh báo hợp đồng hết hạn và số ngày cảnh báo. Thẻ "Dữ liệu" quản lý tự động sao lưu và đường dẫn thư mục sao lưu. Thẻ "Tài khoản" hiển thị thông tin người dùng và nút đổi mật khẩu. Thanh hành động phía dưới chứa nút Lưu và Khôi phục mặc định.

| Thẻ | Các thiết lập | Loại điều khiển |
|---|---|---|
| Hiển thị | Số mục/trang, Xác nhận khi xóa, Gợi ý di chuột, Tự động làm mới | SpinBox, Checkbox |
| Thông báo | Cảnh báo hàng sắp hết, Cảnh báo HĐ hết hạn, Số ngày cảnh báo | Checkbox, SpinBox |
| Dữ liệu | Tự động sao lưu, Đường dẫn thư mục sao lưu | Checkbox, TextInput |
| Tài khoản | Thông tin người dùng, Đổi mật khẩu | Label, Button |

### 3.11 Màn hình Trợ giúp (HelpView)

`HelpView` trong `src/gui/views/help_view.py` tổ chức thông tin qua ba tab. Tab "Hướng dẫn sử dụng" chứa các nhóm hướng dẫn chi tiết cho từng chức năng chính với định dạng HTML phong phú. Tab "Phím tắt" hiển thị bảng danh sách phím tắt toàn ứng dụng. Tab "Về chúng tôi" giới thiệu thông tin phần mềm, công nghệ sử dụng và thành viên nhóm.

### 3.12 Màn hình Quản lý Người dùng (UserView)

`UserView` trong `src/gui/views/users/user_view.py` dành cho quản trị viên quản lý tài khoản nhân viên với bảng dữ liệu hiển thị các cột mã nhân viên, họ tên, email, số điện thoại, vai trò và trạng thái. Các thao tác thêm, sửa, vô hiệu hóa được bảo vệ bởi decorator `require_permission` kiểm tra quyền của người dùng hiện tại.

---

## 4. Hệ thống Form nhập liệu

Các form nhập liệu đều kế thừa từ `QDialog` và tuân theo một mẫu thiết kế chung gồm layout dạng lưới chứa các trường nhập liệu, nút Lưu và Hủy ở phía dưới, cùng tín hiệu `_saved` phát ra kèm đối tượng dữ liệu khi lưu thành công.

`KhachHangForm` trong `src/gui/forms/khach_hang_form.py` chứa các trường họ tên, loại khách hàng (cá nhân hoặc doanh nghiệp), số điện thoại, email, địa chỉ và mã số thuế chỉ hiện khi chọn loại Doanh nghiệp. Form sử dụng `src/utils/validators.py` để kiểm tra dữ liệu đầu vào hợp lệ.

`KhoForm` trong `src/gui/forms/kho_form.py` chứa các trường mã kho (tự động sinh, chỉ đọc), tên kho, địa chỉ, diện tích (`QDoubleSpinBox`), sức chứa (`QDoubleSpinBox`) và trạng thái (`QComboBox`). Form thực hiện kiểm tra ràng buộc theo thời gian thực và chỉ kích hoạt nút Lưu khi dữ liệu hợp lệ.

`HopDongForm` trong `src/gui/forms/hop_dong_form.py` là form phức tạp nhất với bộ chọn khách hàng (`QComboBox` có tìm kiếm), danh sách vị trí trống (`QListWidget` cho phép chọn nhiều), bộ chọn ngày bắt đầu và kết thúc (`QDateEdit`), trường giá thuê và tiền cọc (`QDoubleSpinBox`), bộ chọn phương thức thanh toán (`QComboBox`), và khu vực tóm tắt tự động tính thời gian thuê, tổng tiền thuê và tổng tiền bao gồm cọc. Form hỗ trợ tạo nhiều hợp đồng cùng lúc khi chọn nhiều vị trí.

`HangHoaForm` trong `src/gui/forms/hang_hoa_form.py` chứa bộ chọn hợp đồng, trường tên hàng và loại hàng, số lượng và đơn vị tính, trọng lượng và kích thước, giá trị, bộ chọn vị trí lưu trữ, nút tải ảnh và trường ghi chú.

`ThanhToanForm` trong `src/gui/forms/thanh_toan_form.py` chứa các trường mã thanh toán tự động sinh, hợp đồng (`QComboBox` tải từ database), số tiền (`QDoubleSpinBox`), ngày đến hạn (`QDateEdit`), ngày thanh toán chỉ kích hoạt khi trạng thái là Đã thanh toán, trạng thái, phương thức thanh toán và ghi chú. Khi chọn hợp đồng ở chế độ thêm mới, số tiền được tự động điền theo giá thuê của hợp đồng.

`UserForm` trong `src/gui/forms/users/user_form.py` dành cho việc tạo và sửa tài khoản nhân viên với các trường họ tên, email, số điện thoại, vai trò và trạng thái.

`ViTriForm` trong `src/gui/forms/vi_tri_form.py` quản lý thông tin vị trí lưu trữ với các trường mã vị trí, khu vực, hàng, tầng, diện tích và giá thuê.

---

## 5. Dialog và Wizard

`MessageDialog` trong `src/gui/dialogs/dialogs.py` hiển thị thông báo với bốn mức độ: thông tin, cảnh báo, lỗi và thành công, mỗi mức có thể gọi qua phương thức tĩnh tương ứng. `ConfirmDialog` yêu cầu xác nhận từ người dùng với các nút Xác nhận và Hủy, bao gồm phương thức `ask()` cho câu hỏi chung và `ask_delete()` cho thao tác xóa. `InputDialog` thu thập dữ liệu đầu vào với hỗ trợ nhiều kiểu: văn bản, số nguyên, số thực, ngày tháng và văn bản nhiều dòng. `ProgressDialog` hiển thị tiến trình xử lý ở hai chế độ: xác định với thanh tiến trình và bất định với hiệu ứng xoay vòng. `FormDialog` nhận danh sách định nghĩa trường và tự động sinh giao diện, trả về từ điển dữ liệu đầu vào.

`ChangePasswordDialog` trong `src/gui/dialogs/change_password_dialog.py` là dialog modal với ba trường mật khẩu cũ, mới và xác nhận, cùng các kiểm tra mật khẩu mới tối thiểu tám ký tự, phải khớp với xác nhận và khác mật khẩu cũ.

`RenewalWizard` trong `src/gui/wizards/renewal_wizard.py` là wizard ba bước kế thừa từ `QWizard`. Bước một hiển thị thông tin hợp đồng hiện tại. Bước hai cho phép nhập số tháng gia hạn và giá thuê mới với xem trước ngày kết thúc và tổng tiền. Bước ba tóm tắt toàn bộ thay đổi và yêu cầu xác nhận, sau đó phát tín hiệu `hop_dong_renewed`.

`TerminationWizard` trong `src/gui/wizards/termination_wizard.py` cũng gồm ba bước. Bước một cho phép chọn lý do chấm dứt từ bốn tùy chọn và nhập ghi chú. Bước hai cung cấp hai phương thức tính phạt: theo số tháng tiền thuê hoặc theo phần trăm tiền cọc, với tính toán thời gian thực. Bước ba hiển thị tóm tắt toàn bộ quyết định chấm dứt để xác nhận lần cuối.

---

## 6. Widget tái sử dụng

`DataTable` trong `src/gui/widgets/data_table.py` là lớp bọc của `QTableWidget` với các tính năng sắp xếp theo cột khi nhấp vào tiêu đề, chọn hàng với hai tín hiệu `row_selected` và `row_double_clicked`, tìm kiếm nội bộ trên tất cả các cột hoặc cột cụ thể, menu ngữ cảnh tùy chỉnh và giao diện với màu xen kẽ hàng. `DataTableWithToolbar` kết hợp `DataTable` với thanh công cụ chứa ô tìm kiếm, bộ chọn cột, năm nút hành động (Thêm, Sửa, Xóa, Làm mới, Xuất) và điều khiển phân trang gồm chọn kích thước trang, nút Trước hoặc Sau và chỉ số trang hiện tại.

`SearchBox` trong `src/gui/widgets/search_box.py` cung cấp tìm kiếm thời gian thực với debounce cấu hình được qua `QTimer`, nút xóa văn bản, lịch sử tìm kiếm tích hợp `QCompleter` gợi ý tự động, và phát các tín hiệu `search_changed`, `search_submitted` và `cleared`. `AdvancedSearchBox` mở rộng `SearchBox` bằng cách thêm nhiều `QComboBox` lọc động.

`src/gui/widgets/charts.py` cung cấp bốn lớp biểu đồ dựa trên Matplotlib. `PieChartCanvas` hiển thị phân bổ dữ liệu dạng tròn với chú thích tự động. `BarChartCanvas` hiển thị biểu đồ cột so sánh hỗ trợ cả chiều dọc và chiều ngang. `FillRateBarChart` là biểu đồ cột ngang chuyên dụng cho tỷ lệ lấp đầy kho với mã màu xanh dưới 50%, cam từ 50% đến 75% và đỏ trên 75%. `ChartWidget` là widget bọc container để định kích thước và nhúng các canvas.

`LoadingWidget` trong `src/gui/widgets/loading.py` hiển thị hiệu ứng đang tải cho các thao tác bất đồng bộ, cho phép người dùng biết hệ thống đang xử lý dữ liệu.

`src/gui/widgets/buttons.py` định nghĩa sáu loại nút tùy chỉnh. `PrimaryButton` có màu xanh chủ đạo, `SecondaryButton` màu trung tính, `DangerButton` màu đỏ cho thao tác nguy hiểm. `IconButton` là `QToolButton` thu nhỏ phát tín hiệu `clicked_with_pos` kèm tọa độ màn hình. `ToggleButton` quản lý trạng thái Bật hoặc Tắt. `LoadingButton` có phương thức `set_loading` vô hiệu hóa nút và hiển thị trạng thái xử lý. `ButtonGroup` là widget chứa nhiều nút với các phương thức `add_primary`, `add_secondary` và `add_danger`.

| Widget | Tệp nguồn | Chức năng chính |
|---|---|---|
| DataTable | widgets/data_table.py | Bảng dữ liệu với sắp xếp, phân trang |
| DataTableWithToolbar | widgets/data_table.py | DataTable kèm thanh công cụ và phân trang |
| SearchBox | widgets/search_box.py | Tìm kiếm thời gian thực với debounce |
| AdvancedSearchBox | widgets/search_box.py | SearchBox kết hợp bộ lọc động |
| PieChartCanvas | widgets/charts.py | Biểu đồ tròn phân bổ dữ liệu |
| BarChartCanvas | widgets/charts.py | Biểu đồ cột so sánh giá trị |
| FillRateBarChart | widgets/charts.py | Biểu đồ tỷ lệ lấp đầy có mã màu |
| LoadingWidget | widgets/loading.py | Hiệu ứng đang tải |
| PrimaryButton | widgets/buttons.py | Nút chính màu xanh |
| SecondaryButton | widgets/buttons.py | Nút phụ màu trung tính |
| DangerButton | widgets/buttons.py | Nút nguy hiểm màu đỏ |
| IconButton | widgets/buttons.py | Nút biểu tượng thu nhỏ |
| ToggleButton | widgets/buttons.py | Nút bật tắt hai trạng thái |
| LoadingButton | widgets/buttons.py | Nút có trạng thái đang tải |
| ButtonGroup | widgets/buttons.py | Container nhóm nút |

---

## 7. Hệ thống Stylesheet (QSS)

Tệp `src/gui/styles/main.qss` định nghĩa hệ thống thiết kế nhất quán phong cách Notion cho toàn bộ ứng dụng. Màu nền tổng thể là trắng ấm `#f6f5f4` và màu chủ đạo là xanh Notion `#0075de` dùng cho nút chính, đường viền khi focus và các thành phần tương tác. Bảng dữ liệu có bo góc, màu xen kẽ hàng và tiêu đề được tô sáng. Thanh cuộn được tùy chỉnh với tay cầm bo tròn. Thanh tiến trình có màu xanh và tooltip xuất hiện trên nền tối `#31302e`. Các ID tùy chỉnh như `#dashboardWidget`, `#searchBox`, `#actionButton` và `#cardWidget` cho phép tạo kiểu cụ thể cho từng view.

Bảng tổng kết ánh xạ màn hình chức năng với tệp nguồn và service liên kết:

| Màn hình | Tệp nguồn | Service |
|---|---|---|
| Đăng nhập | views/auth/login_view.py | AuthService |
| Dashboard | views/dashboard_view.py | KhoService, ViTriService |
| Quản lý Khách hàng | views/khach_hang_view.py | KhachHangService |
| Chi tiết Khách hàng | views/khach_hang_detail_view.py | KhachHangService |
| Quản lý Kho hàng | views/kho_view.py | KhoService |
| Quản lý Vị trí | views/vi_tri_view.py | ViTriService |
| Quản lý Hợp đồng | views/hop_dong_view.py | HopDongService |
| Chi tiết Hợp đồng | views/hop_dong_detail_view.py | HopDongService, ThanhToanService, HangHoaService |
| Quản lý Hàng hóa | views/hang_hoa_view.py | HangHoaService |
| Quản lý Thanh toán | views/thanh_toan_view.py | ThanhToanService |
| Báo cáo Thống kê | views/bao_cao_view.py | ReportService, HopDongService |
| Cài đặt Hệ thống | views/settings_view.py | AuthService |
| Trợ giúp | views/help_view.py | — |
| Quản lý Người dùng | views/users/user_view.py | UserService |

Bảng tổng kết form và wizard:

| Thành phần | Tệp nguồn | Mục đích |
|---|---|---|
| KhachHangForm | forms/khach_hang_form.py | Thêm hoặc sửa khách hàng |
| KhoForm | forms/kho_form.py | Thêm hoặc sửa kho |
| ViTriForm | forms/vi_tri_form.py | Thêm hoặc sửa vị trí |
| HopDongForm | forms/hop_dong_form.py | Tạo hoặc sửa hợp đồng |
| HangHoaForm | forms/hang_hoa_form.py | Thêm hoặc sửa hàng hóa |
| ThanhToanForm | forms/thanh_toan_form.py | Tạo hoặc sửa thanh toán |
| UserForm | forms/users/user_form.py | Thêm hoặc sửa người dùng |
| LoaiHangForm | forms/loai_hang_form.py | Quản lý loại hàng |
| RenewalWizard | wizards/renewal_wizard.py | Gia hạn hợp đồng ba bước |
| TerminationWizard | wizards/termination_wizard.py | Chấm dứt hợp đồng ba bước |

---

*Tài liệu mô tả chi tiết thiết kế giao diện người dùng của chương trình Quản Lý Dịch Vụ Cho Thuê Kho Lưu Trữ Hàng Hóa, nhóm 12 - Lập trình Python.*
