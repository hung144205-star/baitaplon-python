# YÊU CẦU HỆ THỐNG
Phần mềm quản lý dịch vụ cho thuê kho lưu trữ hàng hóa

## 1. PHÂN TÍCH CHỨC NĂNG

### 1.1 Quản lý khách hàng
Mô tả: Hệ thống cho phép quản lý toàn bộ thông tin khách hàng đăng ký sử dụng dịch vụ cho thuê kho, bao gồm cá nhân và doanh nghiệp.

Chi tiết:
- Thêm mới khách hàng với thông tin: mã khách hàng, họ tên/tên công ty, loại khách hàng, số điện thoại, email, địa chỉ, mã số thuế
- Cập nhật thông tin khách hàng: thông tin liên hệ, địa chỉ, trạng thái (không cho phép sửa mã khách hàng, ngày đăng ký)
- Xóa khách hàng: chỉ khi không còn hợp đồng đang hoạt động, sử dụng xóa mềm (chuyển trạng thái sang "Đã xóa")
- Tìm kiếm khách hàng theo: mã khách hàng, tên, số điện thoại, email, loại khách hàng, trạng thái
- Xem lịch sử giao dịch: danh sách hợp đồng và thanh toán của khách hàng

### 1.2 Quản lý kho hàng
Mô tả: Hệ thống cho phép quản lý danh sách kho hàng và vị trí lưu trữ, theo dõi sức chứa và tình trạng sử dụng.

Chi tiết:
- Thêm kho mới với thông tin: mã kho, tên kho, địa chỉ, tổng diện tích, sức chứa tối đa, tự động tạo các vị trí lưu trữ
- Cập nhật thông tin kho: tên, địa chỉ, trạng thái (hoạt động/bảo trì/ngừng), không cho phép sửa cấu trúc nếu có vị trí đang thuê
- Quản lý vị trí lưu trữ: cập nhật diện tích, giá thuê, trạng thái (trống/đã thuê/bảo trì), tìm vị trí trống theo yêu cầu
- Theo dõi sức chứa kho: hiển thị tổng diện tích, đã sử dụng, còn trống, tính tỷ lệ lấp đầy, cảnh báo khi > 90%
- Báo cáo tình trạng kho: danh sách vị trí theo trạng thái, thống kê số lượng, lịch sử bảo trì

### 1.3 Quản lý hợp đồng thuê
Mô tả: Hệ thống cho phép quản lý toàn bộ vòng đời hợp đồng thuê kho từ khởi tạo đến kết thúc.

Chi tiết:
- Tạo hợp đồng mới: chọn khách hàng, chọn vị trí lưu trữ, thiết lập thời hạn (ngày bắt đầu/kết thúc), tính toán giá thuê, thu tiền đặt cọc, tự động tạo mã hợp đồng, in hợp đồng mẫu
- Gia hạn hợp đồng: cảnh báo hợp đồng sắp hết hạn (trước 30 ngày), chọn thời hạn gia hạn, cập nhật giá thuê mới, tạo phụ lục gia hạn
- Chấm dứt hợp đồng: xử lý hết hạn tự động, chấm dứt trước hạn (ghi lý do, tính phạt nếu có), kiểm tra công nợ, hoàn trả tiền cọc, giải phóng vị trí, lập biên bản bàn giao
- Quản lý thanh toán: tạo hóa đơn định kỳ, ghi nhận thanh toán (tiền mặt/chuyển khoản), theo dõi công nợ, tính phí phạt trễ hạn, in hóa đơn/biên lai

### 1.4 Quản lý hàng hóa
Mô tả: Hệ thống cho phép theo dõi hàng hóa của khách hàng trong kho, quản lý nhập/xuất và kiểm kê.

Chi tiết:
- Nhập hàng vào kho: xác định hợp đồng, nhập thông tin hàng (tên, loại, số lượng, trọng lượng, kích thước), ghi nhận tình trạng, tải hình ảnh, ghi chú đặc biệt, tạo mã hàng, ghi nhận thời điểm nhập, in phiếu nhập kho
- Xuất hàng khỏi kho: tìm kiếm hàng theo mã/tên, xác nhận chủ hàng có quyền xuất, nhập số lượng xuất (toàn bộ/một phần), ghi nhận lý do xuất, ghi nhận thời điểm xuất, cập nhật tồn kho, in phiếu xuất kho
- Theo dõi tồn kho: xem danh sách hàng theo hợp đồng/khách hàng, thống kê tổng số lượng/loại hàng/giá trị, tìm kiếm/lọc hàng, cảnh báo hàng tồn quá lâu
- Kiểm kê định kỳ: lập kế hoạch kiểm kê, tạo danh sách kiểm kê, đối chiếu thực tế với sổ sách, ghi nhận chênh lệch, lập biên bản kiểm kê, điều chỉnh sổ sách

### 1.5 Báo cáo thống kê
Mô tả: Hệ thống cho phép tổng hợp dữ liệu từ các module để tạo báo cáo phục vụ công tác quản lý.

Chi tiết:
- Báo cáo doanh thu: theo ngày (tổng thu các khoản), theo tháng (doanh thu từng tháng, so sánh), theo năm (tổng kết, xu hướng), theo khách hàng (top doanh thu cao), xuất PDF/Excel
- Báo cáo tỷ lệ lấp đầy kho: tổng quan tất cả kho, chi tiết theo khu vực, theo thời gian (xu hướng sử dụng), dự báo thời điểm đầy kho
- Cảnh báo hợp đồng sắp hết hạn: danh sách hết hạn trong 30 ngày tới, phân loại theo khách hàng/kho, xuất danh sách liên hệ gia hạn
- Báo cáo khách hàng: khách hàng mới, khách hàng quay lại, khách hàng rời bỏ, phân tích lý do
- Báo cáo tài chính: công nợ phải thu, tiền cọc đang giữ, chi phí bảo trì, lợi nhuận ước tính

## 2. YÊU CẦU PHI CHỨC NĂNG

### 2.1 Hiệu năng
- Thời gian phản hồi tìm kiếm: ≤ 2 giây với cơ sở dữ liệu 10.000 bản ghi
- Thời gian tải danh sách khách hàng: ≤ 1 giây
- Hỗ trợ đồng thời 20 người dùng (nếu triển khai multi-user)

### 2.2 Độ tin cậy
- Tỷ lệ lỗi hệ thống: < 0.1%
- Dữ liệu được backup tự động hàng ngày
- Khả năng phục hồi sau sự cố: ≤ 15 phút

### 2.3 Bảo mật
- Xác thực đăng nhập bằng tài khoản/mật khẩu
- Phân quyền truy cập theo vai trò (quản trị viên, nhân viên kho, nhân viên kinh doanh, kế toán)
- Mã hóa mật khẩu người dùng
- Ghi log các thao tác quan trọng (thêm, sửa, xóa dữ liệu)

### 2.4 Khả năng sử dụng
- Giao diện tiếng Việt, trực quan, dễ sử dụng
- Menu rõ ràng, phân cấp hợp lý
- Có hướng dẫn sử dụng tích hợp
- Thời gian đào tạo nhân viên mới: ≤ 2 giờ

### 2.5 Khả năng bảo trì
- Mã nguồn được comment đầy đủ bằng tiếng Việt
- Kiến trúc module, dễ mở rộng tính năng
- Có unit test cho các hàm nghiệp vụ chính
- Tài liệu kỹ thuật đầy đủ

### 2.6 Tính khả chuyển
- Chạy được trên Windows 10/11, macOS 10.14+, Linux
- Không phụ thuộc vào phiên bản hệ điều hành cụ thể
- Dễ dàng chuyển đổi cơ sở dữ liệu (SQLite sang PostgreSQL)