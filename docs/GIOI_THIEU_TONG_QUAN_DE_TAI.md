# GIỚI THIỆU TỔNG QUAN ĐỀ TÀI

## Quản Lý Dịch Vụ Cho Thuê Kho Lưu Trữ Hàng Hóa

---

## 1. Đặt vấn đề

Trong bối cảnh nền kinh tế thị trường phát triển mạnh mẽ như hiện nay, nhu cầu lưu trữ và quản lý hàng hóa ngày càng trở nên cấp thiết đối với các doanh nghiệp thuộc mọi quy mô. Các doanh nghiệp sản xuất, thương mại và logistics đều phải đối mặt với bài toán quản lý kho bãi một cách hiệu quả nhằm tối ưu hóa chi phí vận hành và nâng cao năng lực cạnh tranh. Tuy nhiên, việc quản lý kho hàng theo phương pháp thủ công thông qua sổ sách giấy tờ hoặc các bảng tính đơn giản thường dẫn đến nhiều hạn chế như sai sót trong ghi chép, khó khăn trong tra cứu thông tin, thiếu khả năng cảnh báo các vấn đề phát sinh, và đặc biệt là không đáp ứng được yêu cầu về tính thời gian thực trong bối cảnh kinh doanh hiện đại.

Xuất phát từ thực tế đó, đề tài "Quản Lý Dịch Vụ Cho Thuê Kho Lưu Trữ Hàng Hóa" được hình thành với mục tiêu xây dựng một hệ thống phần mềm hiện đại, toàn diện, giúp các doanh nghiệp có thể quản lý toàn bộ quy trình cho thuê kho lưu trữ một cách chuyên nghiệp và hiệu quả. Hệ thống không chỉ đáp ứng các nhu cầu cơ bản về quản lý kho hàng mà còn tích hợp nhiều tính năng thông minh như cảnh báo tự động, xuất báo cáo chuyên nghiệp và hỗ trợ ra quyết định dựa trên dữ liệu thống kê trực quan.

---

## 2. Mục tiêu của đề tài

Đề tài hướng đến việc xây dựng một hệ thống phần mềm quản lý kho lưu trữ hàng hóa với đầy đủ các chức năng nghiệp vụ cốt lõi, bao gồm quản lý khách hàng, quản lý kho hàng và vị trí lưu trữ, quản lý hợp đồng thuê kho, quản lý hàng hóa nhập xuất và quản lý thanh toán. Hệ thống được thiết kế với giao diện trực quan, thân thiện với người dùng, cho phép người dùng dễ dàng thao tác và nhanh chóng làm quen. Bên cạnh đó, hệ thống còn tích hợp khả năng cảnh báo thông minh đối với các vấn đề quan trọng như hợp đồng sắp hết hạn, tồn kho thấp hay công nợ quá hạn, giúp người quản lý chủ động trong công tác điều hành. Ngoài ra, hệ thống cũng cung cấp khả năng xuất báo cáo dưới nhiều định dạng khác nhau như PDF và Excel, phục vụ cho công tác báo cáo và phân tích kinh doanh.

---

## 3. Đối tượng sử dụng

Hệ thống được xây dựng hướng đến hai nhóm đối tượng người dùng chính. Nhóm thứ nhất là quản trị viên, những người có toàn quyền truy cập và quản lý tất cả các chức năng của hệ thống, bao gồm quản lý người dùng, cấu hình hệ thống và thực hiện sao lưu dữ liệu. Nhóm thứ hai là nhân viên, những người được phân quyền sử dụng các chức năng nghiệp vụ cụ thể phù hợp với vai trò và trách nhiệm của mình trong tổ chức. Sự phân quyền rõ ràng này không chỉ đảm bảo an toàn dữ liệu mà còn giúp tổ chức hoạt động một cách có trật tự và hiệu quả.

---

## 4. Phạm vi của đề tài

Đề tài tập trung vào việc phát triển một ứng dụng desktop hoàn chỉnh với đầy đủ các module chức năng. Module quản lý khách hàng cho phép thực hiện các thao tác thêm, sửa, xóa thông tin khách hàng, phân loại khách hàng theo nhóm cá nhân hoặc doanh nghiệp, theo dõi trạng thái hoạt động và lịch sử giao dịch. Module quản lý kho hàng cung cấp khả năng quản lý thông tin chi tiết của từng kho bao gồm diện tích, sức chứa và tỷ lệ lấp đầy, cùng với việc quản lý vị trí lưu trữ theo cấu trúc khu vực, hàng, tầng một cách linh hoạt. Module quản lý hợp đồng cho phép tạo mới, gia hạn và chấm dứt hợp đồng thuê kho, kèm theo khả năng cảnh báo thông minh và in hợp đồng ra file PDF. Module quản lý hàng hóa hỗ trợ đầy đủ quy trình nhập kho và xuất kho, theo dõi tồn kho theo thời gian thực và in các chứng từ liên quan. Module quản lý thanh toán giúp theo dõi công nợ của khách hàng, cập nhật trạng thái thanh toán và in phiếu thanh toán. Ngoài ra, hệ thống còn có module báo cáo và thống kê với khả năng xuất dữ liệu ra các định dạng phổ biến, module xác thực và phân quyền người dùng, cùng với module cài đặt cho phép cấu hình thông tin công ty, quản lý người dùng và thực hiện sao lưu phục hồi dữ liệu.

---

## 5. Công nghệ sử dụng

Hệ thống được xây dựng dựa trên ngôn ngữ lập trình Python từ phiên bản 3.10 trở lên, một trong những ngôn ngữ lập trình phổ biến và mạnh mẽ nhất hiện nay. Giao diện người dùng được phát triển bằng PyQt6 phiên bản 6.4 trở lên, một framework GUI hiện đại kế thừa từ Qt, mang lại trải nghiệm người dùng mượt mà và chuyên nghiệp. Về mặt lưu trữ dữ liệu, hệ thống sử dụng SQLAlchemy 2.0 làm ORM (Object-Relational Mapping) kết hợp với SQLite làm hệ quản trị cơ sở dữ liệu, đảm bảo tính linh hoạt trong thao tác dữ liệu và dễ dàng triển khai. Đối với khả năng xuất báo cáo, hệ thống sử dụng ReportLab 4.0 để tạo các file PDF chuyên nghiệp và Pandas 2.0 kết hợp với OpenPyXL để xuất dữ liệu ra file Excel. Thư viện Matplotlib và NumPy được sử dụng để vẽ các biểu đồ thống kê trực quan trên dashboard. Bảo mật hệ thống được đảm bảo thông qua thư viện bcrypt để mã hóa mật khẩu người dùng. Cuối cùng, Pillow được sử dụng để xử lý các hình ảnh như logo công ty và hình ảnh hàng hóa.

---

## 6. Kiến trúc hệ thống

Hệ thống được thiết kế theo kiến trúc ba lớp (three-tier architecture) bao gồm tầng giao diện người dùng, tầng nghiệp vụ và tầng dữ liệu. Tầng giao diện người dùng chịu trách nhiệm hiển thị và tương tác với người dùng thông qua các cửa sổ, form nhập liệu và bảng dữ liệu được xây dựng bằng PyQt6. Tầng nghiệp vụ đóng vai trò trung gian, xử lý tất cả các logic nghiệp vụ của hệ thống thông qua các service module được tổ chức theo từng lĩnh vực chức năng riêng biệt. Tầng dữ liệu quản lý việc tương tác với cơ sở dữ liệu thông qua các model được định nghĩa bằng SQLAlchemy, kết hợp với repository pattern để tách biệt logic truy xuất dữ liệu khỏi logic nghiệp vụ. Kiến trúc này không chỉ giúp hệ thống dễ dàng bảo trì và mở rộng mà còn đảm bảo tính tách biệt rõ ràng giữa các thành phần, tạo điều kiện thuận lợi cho việc phát triển và kiểm thử.

---

## 7. Đội ngũ phát triển

Đề tài được thực hiện bởi nhóm sinh viên với sự phân công công việc rõ ràng. Đoàn Mạnh Hùng đảm nhận vai trò trưởng nhóm, chịu trách nhiệm điều phối công việc chung, phát triển các module quản lý kho hàng, vị trí lưu trữ và quản lý thanh toán. Lương Hán Hải phụ trách phát triển các module quản lý hợp đồng, quản lý hàng hóa và các wizard nghiệp vụ phức tạp. Nguyễn Đồng Thanh đảm nhận phát triển module quản lý khách hàng, module xác thực và phân quyền, module báo cáo và xuất file, cùng với module cài đặt hệ thống.

---

## 8. Kết luận

Với sự kết hợp giữa công nghệ hiện đại, kiến trúc phần mềm chặt chẽ và quy trình phát triển bài bản, đề tài "Quản Lý Dịch Vụ Cho Thuê Kho Lưu Trữ Hàng Hóa" hứa hẹn sẽ mang đến một giải pháp quản lý kho hàng toàn diện, đáp ứng được nhu cầu thực tế của các doanh nghiệp trong thời đại số. Hệ thống không chỉ giải quyết các bài toán nghiệp vụ cốt lõi mà còn cung cấp các tính năng thông minh hỗ trợ công tác quản lý và ra quyết định, góp phần nâng cao hiệu quả kinh doanh và tối ưu hóa chi phí vận hành cho người sử dụng.

---

*Tài liệu được biên soạn bởi Nhóm 12 - Lập trình Python*

*Ngày cập nhật: 2026*
