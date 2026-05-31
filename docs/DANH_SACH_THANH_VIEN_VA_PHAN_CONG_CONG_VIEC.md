# DANH SÁCH THÀNH VIÊN VÀ PHÂN CÔNG CÔNG VIỆC

## Quản Lý Dịch Vụ Cho Thuê Kho Lưu Trữ Hàng Hóa

---

## 1. Danh sách thành viên nhóm

Nhóm phát triển đề tài gồm ba thành viên, trong đó Đoàn Mạnh Hùng giữ vai trò trưởng nhóm, Nguyễn Đồng Thanh và Lương Hán Hải là các thành viên trong nhóm. Thông tin chi tiết về từng thành viên được trình bày trong bảng dưới đây.

| STT | Họ và tên | Vai trò | Mã số sinh viên |
|:---:|-----------|---------|:---------------:|
| 1 | Đoàn Mạnh Hùng | Trưởng nhóm | |
| 2 | Nguyễn Đồng Thanh | Thành viên | |
| 3 | Lương Hán Hải | Thành viên | |

---

## 2. Phân công công việc

Dự án được phát triển theo kiến trúc ba lớp và được chia thành nhiều module chức năng độc lập. Mỗi module bao gồm các thành phần model (tầng dữ liệu), service (tầng nghiệp vụ) và view/form (tầng giao diện). Việc phân công công việc được thực hiện dựa trên năng lực và sở trường của từng thành viên, đảm bảo sự cân bằng về khối lượng công việc và tính liên kết giữa các module. Chi tiết phân công được trình bày trong bảng dưới đây.

| Thành viên | Module phụ trách | Công việc chi tiết |
|------------|------------------|---------------------|
| Đoàn Mạnh Hùng | Quản lý Kho hàng và Vị trí lưu trữ | Xây dựng model Kho và ViTri với đầy đủ các trường thông tin như diện tích, sức chứa, trạng thái hoạt động. Phát triển KhoService và ViTriService xử lý các nghiệp vụ liên quan đến kho hàng và vị trí lưu trữ. Xây dựng giao diện quản lý kho, quản lý vị trí cùng các form nhập liệu tương ứng. |
| Đoàn Mạnh Hùng | Quản lý Thanh toán | Xây dựng model ThanhToan phục vụ theo dõi các giao dịch thanh toán. Phát triển ThanhToanService với các chức năng theo dõi công nợ, cập nhật trạng thái thanh toán và xử lý lịch sử thanh toán. Xây dựng giao diện quản lý thanh toán và form thanh toán. |
| Đoàn Mạnh Hùng | Dashboard và Báo cáo | Xây dựng module Dashboard với các biểu đồ thống kê trực quan về doanh thu, khách hàng và kho hàng. Phát triển các cảnh báo thông minh về hợp đồng sắp hết hạn, tồn kho thấp và công nợ quá hạn. |
| Nguyễn Đồng Thanh | Quản lý Khách hàng | Xây dựng model KhachHang với khả năng phân loại khách hàng theo nhóm cá nhân và doanh nghiệp, theo dõi trạng thái hoạt động. Phát triển KhachHangService xử lý các nghiệp vụ thêm, sửa, xóa và tìm kiếm khách hàng. Xây dựng giao diện quản lý khách hàng, form nhập liệu và màn hình chi tiết khách hàng kèm lịch sử giao dịch. |
| Nguyễn Đồng Thanh | Xác thực và Phân quyền | Xây dựng hệ thống xác thực người dùng với cơ chế mã hóa mật khẩu bằng bcrypt. Phát triển AuthorizationService với cơ chế phân quyền dựa trên vai trò Admin và User. Xây dựng giao diện đăng nhập, cơ chế quản lý session với thời gian timeout 8 giờ và chức năng ghi nhớ đăng nhập. |
| Nguyễn Đồng Thanh | Báo cáo và Xuất file | Phát triển ReportService phục vụ thống kê dữ liệu tổng quan. Xây dựng PDF Generation Service sử dụng ReportLab để xuất các báo cáo hợp đồng, phiếu thanh toán và phiếu kho ra định dạng PDF. Xây dựng chức năng xuất báo cáo ra file Excel sử dụng Pandas. |
| Nguyễn Đồng Thanh | Cài đặt và Trợ giúp | Xây dựng giao diện Cài đặt với các tab quản lý thông tin công ty, cấu hình hệ thống, quản lý người dùng và sao lưu phục hồi dữ liệu. Xây dựng màn hình Trợ giúp với hướng dẫn sử dụng chi tiết, danh sách phím tắt và thông tin về ứng dụng. |
| Lương Hán Hải | Quản lý Hợp đồng | Xây dựng model HopDong với đầy đủ thông tin về hợp đồng thuê kho. Phát triển HopDongService xử lý các nghiệp vụ tạo mới, gia hạn và chấm dứt hợp đồng. Xây dựng giao diện quản lý hợp đồng, form hợp đồng, wizard gia hạn và wizard chấm dứt hợp đồng. Tích hợp cảnh báo thông minh cho hợp đồng sắp hết hạn trong vòng 30 ngày. |
| Lương Hán Hải | Quản lý Hàng hóa | Xây dựng model HangHoa và LoaiHang phục vụ quản lý hàng hóa trong kho. Phát triển HangHoaService và InventoryService xử lý các nghiệp vụ nhập kho, xuất kho và theo dõi tồn kho theo thời gian thực. Xây dựng giao diện quản lý hàng hóa, form nhập hàng, form xuất hàng và tích hợp cảnh báo tồn kho thấp. |
| Lương Hán Hải | Lịch sử và Phiếu chứng từ | Xây dựng HopDongHistoryService phục vụ theo dõi lịch sử thay đổi của hợp đồng. Phát triển các chức năng in phiếu nhập kho, phiếu xuất kho và phiếu thanh toán ra định dạng PDF. Xây dựng module lịch sử xuất nhập hàng hóa. |

---

## 3. Công việc chung

Bên cạnh các công việc được phân công riêng, cả ba thành viên trong nhóm đều tham gia vào các công việc chung sau đây. Việc xây dựng cơ sở dữ liệu và các model ban đầu được thực hiện bởi toàn bộ nhóm, bao gồm thiết kế schema, định nghĩa các mối quan hệ giữa các bảng và viết script khởi tạo dữ liệu. Công tác kiểm thử được phân chia theo module mà mỗi thành viên phụ trách, mỗi người viết unit test cho các service và model của module mình, đồng thời cả nhóm cùng tham gia viết integration test cho các thao tác cơ sở dữ liệu. Hoạt động viết tài liệu cũng là trách nhiệm chung, trong đó mỗi thành viên viết tài liệu kỹ thuật cho phần việc của mình, và trưởng nhóm chịu trách nhiệm tổng hợp, biên tập và hoàn thiện tài liệu tổng thể của dự án. Ngoài ra, các hoạt động sửa lỗi, tối ưu hóa hiệu năng và cải tiến giao diện được thực hiện bởi tất cả các thành viên trong suốt quá trình phát triển dự án.

---

*Tài liệu được biên soạn bởi Nhóm 12 - Lập trình Python*

*Ngày cập nhật: 2026*
