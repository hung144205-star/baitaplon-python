# Yêu Cầu Chức Năng

## 1. Quản lý khách hàng

### 1.1 Mô tả
Module quản lý toàn bộ thông tin khách hàng đăng ký sử dụng dịch vụ cho thuê kho. Hệ thống cho phép thêm mới, cập nhật, xóa và tìm kiếm khách hàng theo nhiều tiêu chí. Hỗ trợ phân loại khách hàng cá nhân và doanh nghiệp.

### 1.2 Chi tiết chức năng

#### Thêm mới khách hàng
- Nhập thông tin cơ bản: mã khách hàng, họ tên/tên công ty, loại khách hàng
- Nhập thông tin liên hệ: số điện thoại, email, địa chỉ
- Nhập thông tin pháp lý: mã số thuế (đối với doanh nghiệp)
- Tự động tạo mã khách hàng nếu không nhập
- Validate dữ liệu: kiểm tra email hợp lệ, SĐT đúng định dạng
- Kiểm tra trùng lặp: không cho phép trùng SĐT hoặc email

#### Cập nhật thông tin khách hàng
- Tìm kiếm khách hàng cần cập nhật theo mã hoặc tên
- Hiển thị thông tin hiện tại để chỉnh sửa
- Cho phép cập nhật: thông tin liên hệ, địa chỉ, trạng thái
- Không cho phép sửa: mã khách hàng, ngày đăng ký
- Ghi log thay đổi: lưu lịch sử chỉnh sửa

#### Xóa khách hàng
- Tìm kiếm và chọn khách hàng cần xóa
- Kiểm tra điều kiện: chỉ xóa khi không còn hợp đồng đang hoạt động
- Cảnh báo xác nhận trước khi xóa
- Xóa mềm (soft delete): chuyển trạng thái sang "Đã xóa" thay vì xóa cứng
- Giữ lại lịch sử giao dịch để tham khảo

#### Tìm kiếm khách hàng
- Tìm theo mã khách hàng: chính xác hoặc gần đúng
- Tìm theo tên: tìm kiếm tương đối
- Tìm theo SĐT: tìm chính xác hoặc chứa số
- Tìm theo loại khách: lọc Cá nhân / Doanh nghiệp
- Tìm theo trạng thái: Hoạt động / Tạm khóa / Đã xóa
- Hiển thị kết quả dạng danh sách với phân trang

---

## 2. Quản lý kho hàng

### 2.1 Mô tả
Module quản lý danh sách kho hàng và vị trí lưu trữ trong từng kho. Cho phép định nghĩa kho mới, phân chia khu vực, theo dõi sức chứa và tình trạng sử dụng của từng vị trí.

### 2.2 Chi tiết chức năng

#### Thêm kho mới
- Nhập thông tin kho: mã kho, tên kho, địa chỉ
- Xác định thông số: tổng diện tích (m²), sức chứa tối đa
- Định nghĩa cấu trúc: số khu vực, số hàng, số tầng
- Tự động tạo các vị trí lưu trữ dựa trên cấu trúc
- Thiết lập giá thuê cơ bản cho từng loại vị trí

#### Cập nhật thông tin kho
- Sửa thông tin cơ bản: tên, địa chỉ
- Cập nhật trạng thái: Hoạt động / Bảo trì / Ngừng sử dụng
- Không cho phép sửa: mã kho, cấu trúc đã tạo (nếu có vị trí đang thuê)
- Theo dõi lịch sử bảo trì

#### Quản lý vị trí lưu trữ
- Xem danh sách vị trí theo khu vực, hàng, tầng
- Cập nhật thông tin từng vị trí: diện tích, giá thuê
- Theo dõi trạng thái: Trống / Đã thuê / Bảo trì / Không sử dụng
- Tìm vị trí trống theo yêu cầu: diện tích tối thiểu, vị trí mong muốn

#### Theo dõi sức chứa kho
- Hiển thị tổng quan: tổng diện tích, đã sử dụng, còn trống
- Tính tỷ lệ lấp đầy theo phần trăm
- Biểu đồ trực quan: màu xanh (trống), đỏ (đã thuê), vàng (bảo trì)
- Cảnh báo khi tỷ lệ lấp đầy > 90%

#### Báo cáo tình trạng kho
- Danh sách vị trí theo trạng thái
- Thống kê số lượng vị trí trống/đã thuê/bảo trì
- Lịch sử bảo trì và sửa chữa

---

## 3. Quản lý hợp đồng thuê

### 3.1 Mô tả
Module quản lý toàn bộ vòng đời hợp đồng thuê kho từ khởi tạo đến kết thúc. Hỗ trợ tạo hợp đồng mới, gia hạn, chấm dứt trước hạn và quản lý thanh toán.

### 3.2 Chi tiết chức năng

#### Tạo hợp đồng thuê kho
- Chọn khách hàng từ danh sách hoặc thêm mới nhanh
- Chọn vị trí lưu trữ: tìm vị trí trống phù hợp yêu cầu
- Thiết lập thời hạn: ngày bắt đầu, ngày kết thúc
- Tính toán giá thuê: dựa trên vị trí, thời hạn, giảm giá (nếu có)
- Thu tiền đặt cọc: theo quy định (thường 1-3 tháng)
- Ghi chú điều khoản đặc biệt (nếu có)
- Tự động tạo mã hợp đồng theo quy tắc: HD + Năm + Số thứ tự
- In hợp đồng mẫu để ký kết

#### Gia hạn hợp đồng
- Tìm hợp đồng sắp hết hạn (cảnh báo trước 30 ngày)
- Chọn thời hạn gia hạn: 1 tháng, 3 tháng, 6 tháng, 1 năm
- Cập nhật giá thuê mới (nếu có điều chỉnh)
- Tạo phụ lục hợp đồng gia hạn
- Cập nhật ngày kết thúc mới

#### Chấm dứt hợp đồng
- Trường hợp hết hạn: tự động chuyển trạng thái
- Trường hợp chấm dứt trước hạn: ghi nhận lý do, tính phạt (nếu có)
- Kiểm tra công nợ: đảm bảo đã thanh toán đầy đủ
- Hoàn trả tiền cọc (nếu không vi phạm)
- Giải phóng vị trí lưu trữ: chuyển trạng thái vị trí sang "Trống"
- Lập biên bản bàn giao kho

#### Quản lý thanh toán
- Tạo hóa đơn định kỳ: hàng tháng hoặc theo thỏa thuận
- Ghi nhận thanh toán: tiền mặt, chuyển khoản, thẻ
- Theo dõi công nợ: các khoản chưa thanh toán
- Tính phí phạt: trễ hạn (theo %/ngày)
- In hóa đơn, biên lai
- Báo cáo doanh thu theo hợp đồng

---

## 4. Quản lý hàng hóa

### 4.1 Mô tả
Module theo dõi hàng hóa của khách hàng trong kho. Quản lý việc nhập hàng vào kho, xuất hàng khỏi kho, và kiểm kê định kỳ để đảm bảo an toàn và chính xác.

### 4.2 Chi tiết chức năng

#### Nhập hàng vào kho
- Xác định hợp đồng: hàng của khách hàng nào
- Nhập thông tin hàng: tên hàng, loại hàng, số lượng
- Ghi nhận đặc điểm: trọng lượng, kích thước, tình trạng
- Chụp ảnh/Tải lên hình ảnh hàng hóa (nếu cần)
- Ghi chú đặc biệt: hàng dễ vỡ, cần bảo quản đặc biệt
- Tạo mã hàng hoặc dùng mã của khách
- Ghi nhận thời điểm nhập, người nhận
- In phiếu nhập kho

#### Xuất hàng khỏi kho
- Tìm kiếm hàng theo mã hoặc tên
- Xác nhận chủ hàng (hợp đồng) có quyền xuất
- Nhập số lượng xuất: toàn bộ hoặc một phần
- Ghi nhận lý do xuất: trả hàng, chuyển kho, tiêu thụ
- Ghi nhận thời điểm xuất, người giao
- Cập nhật tồn kho
- In phiếu xuất kho

#### Theo dõi tồn kho
- Xem danh sách hàng hóa theo hợp đồng/khách hàng
- Thống kê: tổng số lượng, loại hàng, giá trị ước tính
- Tìm kiếm: theo tên, loại, vị trí lưu trữ
- Lọc: hàng nhập gần đây, hàng tồn lâu
- Cảnh báo hàng tồn quá lâu (nếu cần)

#### Kiểm kê định kỳ
- Lập kế hoạch kiểm kê: định kỳ hoặc đột xuất
- Tạo danh sách kiểm kê theo vị trí/khách hàng
- Đối chiếu thực tế với sổ sách
- Ghi nhận chênh lệch (nếu có)
- Lập biên bản kiểm kê
- Điều chỉnh sổ sách nếu cần (có xác nhận)

---

## 5. Báo cáo thống kê

### 5.1 Mô tả
Module tổng hợp dữ liệu từ các module khác để tạo báo cáo phục vụ quản lý. Hỗ trợ báo cáo doanh thu, tình trạng sử dụng kho, và cảnh báo các vấn đề cần chú ý.

### 5.2 Chi tiết chức năng

#### Báo cáo doanh thu
- **Theo ngày**: Tổng thu các khoản trong ngày (cọc, thuê, phạt)
- **Theo tháng**: Doanh thu từng tháng, so sánh tháng trước
- **Theo năm**: Tổng kết năm, xu hướng
- **Theo khách hàng**: Top khách hàng doanh thu cao
- **Xuất định dạng**: PDF, Excel, hiển thị màn hình

#### Báo cáo tỷ lệ lấp đầy kho
- **Tổng quan tất cả kho**: % lấp đầy trung bình
- **Chi tiết theo kho**: Biểu đồ từng khu vực
- **Theo thời gian**: Xu hướng sử dụng (tăng/giảm)
- **Dự báo**: Ước tính thời điểm đầy kho

#### Cảnh báo hợp đồng sắp hết hạn
- **Danh sách cảnh báo**: Hợp đồng hết hạn trong 30 ngày tới
- **Phân loại**: Theo khách hàng, theo kho
- **Xuất danh sách**: Gửi nhân viên kinh doanh liên hệ gia hạn

#### Báo cáo khách hàng tiềm năng
- **Khách hàng mới**: Số lượng đăng ký mới trong kỳ
- **Khách hàng quay lại**: Khách cũ thuê thêm/tiếp tục
- **Khách hàng rời bỏ**: Khách không gia hạn
- **Phân tích**: Lý do rời bỏ (nếu có thông tin)

#### Báo cáo tài chính khác
- **Công nợ phải thu**: Danh sách khách chưa thanh toán
- **Tiền cọc giữ**: Tổng tiền cọc đang giữ
- **Chi phí bảo trì**: Chi phí duy trì kho
- **Lợi nhuận**: Doanh thu - Chi phí (ước tính)

---

**Ghi chú:** Các chức năng có thể được điều chỉnh, bổ sung trong quá trình phát triển dựa trên yêu cầu thực tế.