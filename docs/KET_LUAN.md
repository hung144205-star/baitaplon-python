# KẾT LUẬN

## Nội dung đạt được

Đề tài đã hoàn thành việc xây dựng chương trình quản lý kho hàng với các chức năng cơ bản theo yêu cầu đặt ra. Hệ thống quản lý được sáu đối tượng chính gồm Kho, Khách hàng, Hợp đồng, Vị trí lưu trữ, Hàng hóa và Thanh toán. Giao diện người dùng được thiết kế thân thiện với PyQt6, hỗ trợ đầy đủ thao tác CRUD cho từng module. Phần kiểm thử đã hoàn thành 49 test cases với kết quả 100% passed, đảm bảo chất lượng mã nguồn cho các chức năng cốt lõi. Tài liệu kỹ thuật được biên soạn đầy đủ bao gồm sơ đồ lớp, sơ đồ cơ sở dữ liệu, mô tả thiết kế GUI và hướng dẫn kiểm thử.

## Hạn chế

Một số chức năng nâng cao chưa được triển khai đầy đủ như thống kê báo cáo chi tiết, xuất dữ liệu ra file Excel, hay tính năng tự động nhắc nhở hợp đồng sắp hết hạn. Phần kiểm thử giao diện vẫn còn hạn chế về số lượng test case, chưa bao phủ hết các kịch bản người dùng. Hệ thống hiện tại chỉ hỗ trợ cơ sở dữ liệu SQLite, chưa tích hợp được các hệ quản trị cơ sở dữ liệu lớn hơn như PostgreSQL hay MySQL. Ngoài ra, việc xử lý đồng thời nhiều người dùng truy cập cùng lúc chưa được tối ưu hóa.

## Kế hoạch phát triển

Giai đoạn tiếp theo sẽ tập trung bổ sung module báo cáo thống kê với các biểu đồ trực quan về tình trạng kho, doanh thu và công nợ. Hệ thống sẽ được nâng cấp hỗ trợ xuất báo cáo ra định dạng PDF và Excel để phục vụ công tác quản lý. Việc mở rộng khả năng kết nối đa cơ sở dữ liệu cũng nằm trong kế hoạch phát triển dài hạn nhằm đáp ứng nhu cầu triển khai thực tế. Cuối cùng, team sẽ mở rộng thêm các bộ test cho giao diện người dùng và tích hợp CI/CD để đảm bảo chất lượng mã nguồn liên tục.