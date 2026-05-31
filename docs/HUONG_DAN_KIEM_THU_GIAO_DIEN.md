# HƯỚNG DẪN KIỂM THỬ GIAO DIỆN CHƯƠNG TRÌNH

## 1. Các chức năng cần kiểm thử

Chương trình quản lý kho hàng có các chức năng chính sau:

Quản lý Kho hàng: Thêm, sửa, xóa, tìm kiếm và lọc kho hàng. Hiển thị thống kê tổng số kho, số kho đang hoạt động, tỷ lệ lấp đầy trung bình. Lọc kho theo trạng thái (Hoạt động, Bảo trì, Ngừng). Xuất dữ liệu kho ra file Excel.

Quản lý Khách hàng: Thêm, sửa, xóa, tìm kiếm và lọc khách hàng. Lọc theo loại khách hàng (Cá nhân, Doanh nghiệp) và trạng thái (Hoạt động, Tạm khóa).

Quản lý Hợp đồng: Thêm, sửa, xóa, tìm kiếm và lọc hợp đồng thuê kho. Hiển thị thống kê số hợp đồng theo trạng thái (Hiệu lực, Sắp hết hạn, Hết hạn, Chấm dứt). Cập nhật trạng thái hợp đồng. Xuất hợp đồng ra Excel và PDF.

Quản lý Vị trí: Thêm, sửa, xóa vị trí lưu trữ trong kho. Xem danh sách vị trí theo kho.

Quản lý Hàng hóa: Thêm, xuất nhập hàng hóa. Theo dõi tồn kho và lịch sử xuất nhập.

Quản lý Thanh toán: Theo dõi và quản lý các khoản thanh toán.

Báo cáo: Xem báo cáo tổng quan, báo cáo hàng tồn kho, báo cáo doanh thu.

## 2. Dữ liệu kiểm thử

### 2.1 Chức năng Quản lý Kho hàng

Mẫu dữ liệu 1 (Hợp lệ): Tên kho là "Kho Bình Tân", địa chỉ là "123 Đường số 5, Quận Bình Tân, TP.HCM", diện tích là 1500, sức chứa là 8000, trạng thái là "Hoạt động". Kết quả mong đợi: Lưu thành công, hiển thị trong danh sách với mã KHO tự động sinh.

Mẫu dữ liệu 2 (Không hợp lệ): Tên kho để trống, địa chỉ là "456 Đường Test", diện tích là 0, sức chứa là -500. Kết quả mong đợi: Hiển thị thông báo lỗi "Trường 'ten_kho' là bắt buộc" hoặc "Diện tích phải lớn hơn 0".

Mẫu dữ liệu 3 (Không hợp lệ): Tên kho là "Kho A", địa chỉ là "789 Đường Invalid", diện tích là abc (không phải số). Kết quả mong đợi: Hiển thị thông báo lỗi "Diện tích phải là số".

### 2.2 Chức năng Quản lý Khách hàng

Mẫu dữ liệu 1 (Hợp lệ): Họ tên là "Nguyễn Văn An", số điện thoại là "0901234567", email là "an.nguyen@email.com", loại khách là "Cá nhân", địa chỉ là "12 Nguyễn Trãi, Quận 1, TP.HCM". Kết quả mong đợi: Lưu thành công, hiển thị trong danh sách.

Mẫu dữ liệu 2 (Không hợp lệ): Họ tên để trống, số điện thoại là "12345", email là "invalid-email". Kết quả mong đợi: Hiển thị thông báo lỗi validation.

Mẫu dữ liệu 3 (Không hợp lệ): Số điện thoại là "abcdefghij", email là "@invalid.com". Kết quả mong đợi: Hiển thị thông báo lỗi "Số điện thoại không hợp lệ" hoặc "Email không hợp lệ".

### 2.3 Chức năng Quản lý Hợp đồng

Mẫu dữ liệu 1 (Hợp lệ): Mã khách hàng là "KH001", mã vị trí là "KHO001-A-01-01-001", ngày bắt đầu là "01/01/2026", ngày kết thúc là "31/12/2026", giá thuê là 5000000, tiền cọc là 10000000, phương thức thanh toán là "hàng tháng". Kết quả mong đợi: Lưu thành công, hiển thị trong danh sách với mã HD tự động sinh theo tháng.

Mẫu dữ liệu 2 (Không hợp lệ): Ngày kết thúc trước ngày bắt đầu (ngày bắt đầu 01/01/2026, ngày kết thúc 01/01/2025). Kết quả mong đợi: Hiển thị thông báo lỗi "Ngày kết thúc phải sau ngày bắt đầu".

Mẫu dữ liệu 3 (Không hợp lệ): Giá thuê là 0 hoặc âm. Kết quả mong đợi: Hiển thị thông báo lỗi "Giá thuê phải lớn hơn 0".

### 2.4 Chức năng Quản lý Vị trí

Mẫu dữ liệu 1 (Hợp lệ): Mã kho là "KHO001", khu vực là "A", hàng là "01", tầng là 1, diện tích là 50, chiều cao là 3.5, giá thuê là 150000. Kết quả mong đợi: Lưu thành công, tự động sinh mã vị trí.

Mẫu dữ liệu 2 (Không hợp lệ): Diện tích là 0, giá thuê là -100. Kết quả mong đợi: Hiển thị thông báo lỗi.

### 2.5 Chức năng Tìm kiếm và Lọc

Mẫu dữ liệu 1: Nhập từ khóa tìm kiếm là "Kho Bình" vào ô tìm kiếm trên giao diện Quản lý Kho. Kết quả mong đợi: Hiển thị các kho có tên hoặc địa chỉ chứa "Kho Bình".

Mẫu dữ liệu 2: Chọn bộ lọc trạng thái là "Hoạt động" trên giao diện Quản lý Kho. Kết quả mong đợi: Chỉ hiển thị các kho có trạng thái Hoạt động.

Mẫu dữ liệu 3: Nhập từ khóa tìm kiếm không tồn tại như "KhoKhongTonTai12345". Kết quả mong đợi: Thông báo "Tìm thấy: 0 kho" hoặc danh sách trống.

### 2.6 Chức năng Quản lý Hàng hóa

Mẫu dữ liệu 1 (Hợp lệ): Tên hàng là "Laptop Dell XPS 15", loại hàng là "Điện tử", số lượng là 10, đơn vị là "cái", giá trị là 25000000, mã hợp đồng là "HD001". Kết quả mong đợi: Lưu thành công, hiển thị trong danh sách với mã HH tự động sinh theo định dạng HHXXXXX.

Mẫu dữ liệu 2 (Không hợp lệ): Tên hàng để trống, số lượng là 0, giá trị là -500000. Kết quả mong đợi: Hiển thị thông báo lỗi "Thiếu trường bắt buộc: ten_hang" hoặc "Số lượng phải lớn hơn 0".

Mẫu dữ liệu 3 (Không hợp lệ): Số lượng là "abc" (không phải số), mã hợp đồng là "HD999999" (không tồn tại). Kết quả mong đợi: Hiển thị thông báo lỗi "Số lượng phải là số" hoặc "Không tìm thấy hợp đồng".

### 2.7 Chức năng Quản lý Thanh toán

Mẫu dữ liệu 1 (Hợp lệ): Mã hợp đồng là "HD001", kỳ thanh toán là "01/2026", số tiền là 5000000, ngày đến hạn là "15/01/2026", ngày thanh toán để trống (chưa thanh toán). Kết quả mong đợi: Lưu thành công, hiển thị trong danh sách với trạng thái "Chưa thanh toán".

Mẫu dữ liệu 2 (Hợp lệ): Mã hợp đồng là "HD001", kỳ thanh toán là "01/2026", số tiền là 5000000, ngày đến hạn là "15/01/2026", ngày thanh toán là "10/01/2026". Kết quả mong đợi: Lưu thành công, hiển thị với trạng thái "Đã thanh toán" và cập nhật tổng tiền đã thanh toán.

Mẫu dữ liệu 3 (Không hợp lệ): Số tiền là 0 hoặc để trống. Kết quả mong đợi: Hiển thị thông báo lỗi "Số tiền phải lớn hơn 0".

## 3. Cách chạy chương trình và kiểm thử

Bước 1: Mở chương trình bằng cách chạy file main.py trong thư mục gốc của project. Giao diện chính sẽ hiển thị với các tab điều hướng cho từng chức năng.

Bước 2: Chọn chức năng cần kiểm thử từ menu điều hướng bên trái. Ví dụ: Click vào "Quản lý Kho hàng" để vào giao diện quản lý kho.

Bước 3: Với chức năng Thêm mới, click nút "Thêm" trên thanh công cụ. Điền dữ liệu mẫu vào form. Nhấn nút "Lưu" để kiểm tra.

Bước 4: Chụp ảnh màn hình kết quả bằng cách nhấn phím Print Screen hoặc sử dụng công cụ chụp màn hình. Lưu ảnh với tên mô tả rõ ràng, ví dụ: "kho_them_moi_thanh_cong.png" hoặc "kho_them_moi_loi_validation.png".

Bước 5: Với chức năng Sửa, chọn một bản ghi từ danh sách, click nút "Sửa". Thay đổi thông tin và lưu. Chụp ảnh trước và sau khi sửa.

Bước 6: Với chức năng Xóa, chọn một bản ghi, click nút "Xóa". Xác nhận xóa trên hộp thoại. Chụp ảnh kết quả.

Bước 7: Với chức năng Tìm kiếm, nhập từ khóa vào ô tìm kiếm. Quan sát kết quả lọc real-time. Chụp ảnh kết quả tìm kiếm.

## 4. Mẫu báo cáo kết quả kiểm thử

### 4.1 Chức năng Thêm Kho hàng

Mẫu dữ liệu 1

Thành phần và giá trị: Tên kho là "Kho Bình Tân", Địa chỉ là "123 Đường số 5, Quận Bình Tân, TP.HCM", Diện tích là 1500, Sức chứa là 8000, Trạng thái là "Hoạt động".

Thực hiện: Người dùng nhấn nút "Thêm", điền đầy đủ thông tin vào form, nhấn nút "Lưu".

Kết quả mong đợi: Hệ thống lưu thông tin kho và hiển thị thông báo thành công. Kho mới xuất hiện trong danh sách với mã KHO tự động sinh.

Kết quả thực tế: Hệ thống lưu thành công, hiển thị thông báo "Đã thêm kho thành công", kho mới xuất hiện trong danh sách với mã KHO001.

Hình ảnh minh họa: (Chèn ảnh chụp màn hình tại đây - ảnh thể hiện form nhập liệu và kết quả thành công)

Mẫu dữ liệu 2

Thành phần và giá trị: Tên kho để trống, Địa chỉ là "456 Đường Test", Diện tích là 0, Sức chứa là 8000.

Thực hiện: Người dùng nhấn nút "Thêm", để trống tên kho, nhập diện tích là 0, nhấn nút "Lưu".

Kết quả mong đợi: Hệ thống hiển thị thông báo lỗi validation, không lưu dữ liệu.

Kết quả thực tế: Hệ thống hiển thị thông báo "Trường 'ten_kho' là bắt buộc" tại ô tên kho và "Diện tích phải lớn hơn 0" tại ô diện tích. Dữ liệu không được lưu.

Hình ảnh minh họa: (Chèn ảnh chụp màn hình tại đây - ảnh thể hiện thông báo lỗi validation)

### 4.2 Chức năng Tìm kiếm Kho hàng

Mẫu dữ liệu 1

Thành phần và giá trị: Từ khóa tìm kiếm là "Kho Bình".

Thực hiện: Người dùng nhập "Kho Bình" vào ô tìm kiếm, quan sát kết quả lọc real-time.

Kết quả mong đợi: Hệ thống hiển thị các kho có tên hoặc địa chỉ chứa "Kho Bình". Thông tin hiển thị bao gồm mã kho, tên kho, địa chỉ.

Kết quả thực tế: Hệ thống hiển thị 2 kho có tên chứa "Kho Bình" trong danh sách. Thông tin được hiển thị đầy đủ theo các cột trong bảng.

Hình ảnh minh họa: (Chèn ảnh chụp màn hình tại đây - ảnh thể hiện kết quả tìm kiếm)

Mẫu dữ liệu 2

Thành phần và giá trị: Từ khóa tìm kiếm là "KhoKhongTonTai12345".

Thực hiện: Người dùng nhập chuỗi không tồn tại vào ô tìm kiếm.

Kết quả mong đợi: Hệ thống hiển thị thông báo "Tìm thấy: 0 kho" hoặc danh sách trống.

Kết quả thực tế: Hệ thống hiển thị nhãn thông tin "Tìm thấy: 0 kho" phía dưới bảng dữ liệu. Danh sách trống.

Hình ảnh minh họa: (Chèn ảnh chụp màn hình tại đây - ảnh thể hiện kết quả tìm không thấy)

### 4.3 Chức năng Thêm Hợp đồng

Mẫu dữ liệu 1

Thành phần và giá trị: Mã khách hàng là "KH001", Mã vị trí là "KHO001-A-01-01-001", Ngày bắt đầu là "01/01/2026", Ngày kết thúc là "31/12/2026", Giá thuê là 5000000, Tiền cọc là 10000000, Phương thức thanh toán là "hàng tháng".

Thực hiện: Người dùng nhấn nút "Thêm Hợp đồng", điền đầy đủ thông tin vào form, nhấn nút "Lưu".

Kết quả mong đợi: Hệ thống lưu hợp đồng với mã tự động theo định dạng HDYYYYMMXXXX, hiển thị thông báo thành công, hợp đồng xuất hiện trong danh sách.

Kết quả thực tế: Hệ thống lưu thành công với mã "HD202601001", hiển thị thông báo "Đã thêm hợp đồng thành công", hợp đồng xuất hiện trong danh sách với trạng thái "Hiệu lực".

Hình ảnh minh họa: (Chèn ảnh chụp màn hình tại đây)

Mẫu dữ liệu 2

Thành phần và giá trị: Ngày bắt đầu là "01/01/2026", Ngày kết thúc là "01/01/2025" (trước ngày bắt đầu).

Thực hiện: Người dùng nhập ngày kết thúc trước ngày bắt đầu, nhấn nút "Lưu".

Kết quả mong đợi: Hệ thống hiển thị thông báo lỗi "Ngày kết thúc phải sau ngày bắt đầu".

Kết quả thực tế: Hệ thống hiển thị thông báo lỗi validation tại ô ngày kết thúc. Dữ liệu không được lưu.

Hình ảnh minh họa: (Chèn ảnh chụp màn hình tại đây)

### 4.4 Chức năng Nhập Hàng hóa

Mẫu dữ liệu 1

Thành phần và giá trị: Tên hàng là "Laptop Dell XPS 15", Loại hàng là "Điện tử", Số lượng là 10, Đơn vị là "cái", Giá trị là 25000000, Mã hợp đồng là "HD001".

Thực hiện: Người dùng nhấn nút "Nhập kho", điền đầy đủ thông tin vào form phiếu nhập, nhấn nút "Lưu".

Kết quả mong đợi: Hệ thống lưu hàng hóa với mã tự động sinh, cập nhật số lượng tồn kho, hiển thị thông báo thành công. Hàng hóa xuất hiện trong danh sách với trạng thái "Trong kho".

Kết quả thực tế: Hệ thống lưu thành công, hiển thị thông báo "Đã nhập hàng thành công", hàng hóa xuất hiện trong danh sách với trạng thái "Trong kho", số lượng tồn kho tăng lên 10.

Hình ảnh minh họa: (Chèn ảnh chụp màn hình tại đây - ảnh thể hiện form nhập kho và kết quả thành công)

Mẫu dữ liệu 2

Thành phần và giá trị: Tên hàng là "Laptop Dell XPS 15", Số lượng là 0, Giá trị là 25000000.

Thực hiện: Người dùng nhập số lượng là 0, nhấn nút "Lưu".

Kết quả mong đợi: Hệ thống hiển thị thông báo lỗi "Số lượng phải lớn hơn 0". Dữ liệu không được lưu.

Kết quả thực tế: Hệ thống hiển thị thông báo lỗi tại ô số lượng. Dữ liệu không được lưu.

Hình ảnh minh họa: (Chèn ảnh chụp màn hình tại đây - ảnh thể hiện thông báo lỗi validation)

### 4.5 Chức năng Xuất Hàng hóa

Mẫu dữ liệu 1

Thành phần và giá trị: Hàng hóa đang có số lượng tồn kho là 10. Số lượng xuất là 3.

Thực hiện: Người dùng chọn hàng hóa từ danh sách, nhấn nút "Xuất kho", nhập số lượng xuất là 3, nhấn nút "Xác nhận".

Kết quả mong đợi: Hệ thống cập nhật số lượng tồn kho còn 7, hiển thị thông báo thành công. Trạng thái hàng hóa thay đổi nếu số lượng về 0.

Kết quả thực tế: Hệ thống cập nhật số lượng tồn kho từ 10 xuống 7, hiển thị thông báo "Đã xuất hàng thành công". Lịch sử xuất nhập được ghi nhận.

Hình ảnh minh họa: (Chèn ảnh chụp màn hình tại đây - ảnh thể hiện form xuất kho và kết quả)

Mẫu dữ liệu 2

Thành phần và giá trị: Hàng hóa đang có số lượng tồn kho là 5. Số lượng xuất là 10 (nhiều hơn tồn kho).

Thực hiện: Người dùng nhập số lượng xuất là 10, nhấn nút "Xác nhận".

Kết quả mong đợi: Hệ thống hiển thị thông báo lỗi "Số lượng không đủ". Dữ liệu không được lưu.

Kết quả thực tế: Hệ thống hiển thị thông báo lỗi "Số lượng không đủ" tại ô số lượng xuất. Số lượng tồn kho vẫn giữ nguyên là 5.

Hình ảnh minh họa: (Chèn ảnh chụp màn hình tại đây - ảnh thể hiện thông báo lỗi số lượng không đủ)

### 4.6 Chức năng Thêm Thanh toán

Mẫu dữ liệu 1

Thành phần và giá trị: Mã hợp đồng là "HD001", Kỳ thanh toán là "01/2026", Số tiền là 5000000, Ngày đến hạn là "15/01/2026", Ngày thanh toán để trống.

Thực hiện: Người dùng nhấn nút "Thêm thanh toán", điền đầy đủ thông tin, nhấn nút "Lưu".

Kết quả mong đợi: Hệ thống lưu thông tin thanh toán, hiển thị thông báo thành công. Thanh toán xuất hiện trong danh sách với trạng thái "Chưa thanh toán".

Kết quả thực tế: Hệ thống lưu thành công, hiển thị thông báo "Đã thêm thanh toán thành công", thanh toán xuất hiện trong danh sách với trạng thái "Chưa thanh toán", cập nhật tổng tiền còn nợ.

Hình ảnh minh họa: (Chèn ảnh chụp màn hình tại đây - ảnh thể hiện form thêm thanh toán và kết quả)

Mẫu dữ liệu 2

Thành phần và giá trị: Mã hợp đồng là "HD001", Kỳ thanh toán là "01/2026", Số tiền là 0, Ngày đến hạn là "15/01/2026".

Thực hiện: Người dùng nhập số tiền là 0, nhấn nút "Lưu".

Kết quả mong đợi: Hệ thống hiển thị thông báo lỗi "Số tiền phải lớn hơn 0".

Kết quả thực tế: Hệ thống hiển thị thông báo lỗi tại ô số tiền. Dữ liệu không được lưu.

Hình ảnh minh họa: (Chèn ảnh chụp màn hình tại đây - ảnh thể hiện thông báo lỗi validation)

### 4.7 Chức năng Cập nhật Trạng thái Thanh toán

Mẫu dữ liệu 1

Thành phần và giá trị: Thanh toán đang có trạng thái "Chưa thanh toán", người dùng nhập ngày thanh toán là "10/01/2026".

Thực hiện: Người dùng chọn thanh toán từ danh sách, nhấn nút "Cập nhật", nhập ngày thanh toán thực tế, nhấn nút "Lưu".

Kết quả mong đợi: Hệ thống cập nhật trạng thái thành "Đã thanh toán", cập nhật tổng tiền đã thanh toán và còn nợ.

Kết quả thực tế: Hệ thống cập nhật trạng thái thành "Đã thanh toán", cập nhật tổng tiền đã thanh toán tăng thêm 5000000, còn nợ giảm xuống.

Hình ảnh minh họa: (Chèn ảnh chụp màn hình tại đây - ảnh thể hiện cập nhật trạng thái thành công)