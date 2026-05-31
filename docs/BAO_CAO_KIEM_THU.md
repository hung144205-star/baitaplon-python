# BÁO CÁO KẾT QUẢ KIỂM THỬ CHƯƠNG TRÌNH

## Tổng quan

Chương trình quản lý kho hàng được kiểm thử với 49 test cases, chia thành 2 nhóm chức năng chính. Kết quả: **49/49 tests passed (100%)**.

## Nhóm kiểm thử 1: KhoService (13 tests)

Nhóm này kiểm thử các chức năng CRUD và nghiệp vụ của module quản lý kho hàng.

**Chức năng tạo kho (5 tests):** Kiểm tra việc tạo kho mới với dữ liệu hợp lệ, tự động sinh mã kho, và xử lý lỗi khi thiếu trường bắt buộc hoặc dữ liệu không hợp lệ như diện tích bằng 0 hoặc sức chứa âm. Tất cả các test đều pass.

**Chức năng truy xuất kho (5 tests):** Kiểm tra việc lấy thông tin kho theo mã, lấy danh sách tất cả các kho với phân trang, và lọc kho theo trạng thái hoạt động. Kết quả cho thấy các function get_by_id, get_all với pagination và lọc theo trạng thái đều hoạt động đúng.

**Chức năng tìm kiếm (3 tests):** Kiểm tra khả năng tìm kiếm kho theo tên và địa chỉ. Hệ thống tìm kiếm chính xác các kho có tên hoặc địa chỉ chứa từ khóa tìm kiếm, và trả về kết quả rỗng khi không tìm thấy.

**Chức năng cập nhật và xóa (5 tests):** Kiểm tra việc cập nhật thông tin kho, xóa kho không có vị trí, và từ chối xóa kho đang có vị trí lưu trữ. Chức năng update hoạt động đúng khi cập nhật tên và diện tích kho. Việc xóa kho thành công khi không có vị trí liên kết, và hệ thống correctly reject khi cố xóa kho đang có vị trí.

**Nghiệp vụ tính toán (2 tests):** Kiểm tra việc tính tỷ lệ lấp đầy và dung tích khả dụng của kho. Kết quả cho thấy tỷ lệ lấp đầy ban đầu là 0 với kho mới, và hệ thống trả về đầy đủ thông tin bao gồm tổng diện tích, diện tích đã sử dụng, diện tích còn lại và số vị trí trống.

## Nhóm kiểm thử 2: Validators (36 tests)

Nhóm này kiểm thử các function kiểm tra dữ liệu đầu vào của hệ thống.

**Kiểm tra email (4 tests):** Function validate_email xử lý đúng các email hợp lệ như user@example.com, đúng khi reject các email không hợp lệ như thiếu @ hoặc domain, và hiển thị thông báo lỗi "không được để trống" khi email rỗng hoặc "quá dài" khi vượt quá 250 ký tự.

**Kiểm tra số điện thoại (4 tests):** Function validate_phone hỗ trợ các định dạng số điện thoại Việt Nam 10-11 số, correctly reject các số quá ngắn hoặc quá dài, và xử lý được các trường hợp có khoảng trắng hoặc dấu + ở đầu.

**Kiểm tra trường bắt buộc (2 tests):** Function validate_required correctly accept các giá trị hợp lệ như số 0 hoặc chuỗi rỗng "", và reject các giá trị rỗng như None, chuỗi whitespace-only, list rỗng và dict rỗng.

**Kiểm tra độ dài (4 tests):** Function validate_length kiểm tra giới hạn min/max của chuỗi, hiển thị thông báo "ít nhất X ký tự" khi quá ngắn và "không được vượt quá X ký tự" khi quá dài, và skip validation cho non-string values.

**Kiểm tra số (4 tests):** Function validate_number chấp nhận các giá trị số hợp lệ bao gồm cả string số, kiểm tra min/max values và hiển thị thông báo lỗi tương ứng, correctly reject các giá trị không phải số.

**Kiểm tra tiền tệ (3 tests):** Function validate_currency kiểm tra giá trị tiền tệ không âm, reject nếu là số âm hoặc có nhiều hơn 2 chữ số thập phân.

**Kiểm tra mật khẩu (5 tests):** Function validate_password yêu cầu mật khẩu có ít nhất 6 ký tự, chứa ít nhất một chữ cái và một số. Hệ thống correctly reject các mật khẩu không đạt yêu cầu và hiển thị thông báo lỗi phù hợp.

**Kiểm tra form tổng hợp (3 tests):** Function validate_form xử lý form với nhiều trường, trả về trạng thái is_valid và dictionary errors, correctly identify các trường không hợp lệ trong form.

## Kết luận

Tất cả 49 test cases đều passed, cho thấy các chức năng cốt lõi của hệ thống bao gồm quản lý kho hàng và kiểm tra dữ liệu đầu vào hoạt động đúng đắn. Các test kiểm tra cả trường hợp thành công (happy path) và trường hợp lỗi (error handling), đảm bảo hệ thống xử lý đúng với dữ liệu hợp lệ và hiển thị thông báo lỗi phù hợp khi có vấn đề.