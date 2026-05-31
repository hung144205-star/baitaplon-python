# Giới Thiệu Các Module/Thư Viện Python Được Sử Dụng Trong Đề Tài

**Đề tài:** Quản Lý Dịch Vụ Cho Thuê Kho Lưu Trữ Hàng Hóa  
**Nhóm thực hiện:** Nhóm 12 - Lập trình Python  
**Ngày cập nhật:** 10/05/2026

---

## Giới thiệu tổng quan

Dự án "Quản Lý Dịch Vụ Cho Thuê Kho Lưu Trữ Hàng Hóa" được xây dựng bằng ngôn ngữ Python phiên bản 3.10 trở lên. Toàn bộ hệ thống sử dụng tổng cộng 10 thư viện và 3 công cụ hỗ trợ phát triển, được phân chia thành các nhóm chức năng sau: nhóm giao diện người dùng (PyQt6), nhóm cơ sở dữ liệu (SQLAlchemy, SQLite), nhóm xuất báo cáo (ReportLab, Pandas, OpenPyXL), nhóm vẽ biểu đồ (Matplotlib, NumPy), nhóm xử lý hình ảnh (Pillow), nhóm tiện ích xử lý ngày tháng và bảo mật (python-dateutil, bcrypt), và nhóm phát triển và kiểm thử (Pytest, pytest-cov, Black). Mỗi thư viện đóng một vai trò cụ thể trong kiến trúc tổng thể của hệ thống, được trình bày chi tiết trong các phần dưới đây.

---

## 1. PyQt6 — Framework Giao Diện Người Dùng

### Thông tin thư viện

PyQt6 (Python Qt6) là bộ wrapper Python cho framework Qt6, phiên bản yêu cầu từ 6.4.0 trở lên. Trang chủ của thư viện tại địa chỉ https://www.riverbankcomputing.com/software/pyqt/.

### Vai trò trong đề tài

PyQt6 là thư viện cốt lõi xây dựng toàn bộ giao diện người dùng đồ họa (GUI) cho ứng dụng desktop. Thư viện này cung cấp đầy đủ các thành phần để tạo một ứng dụng desktop chuyên nghiệp, từ cửa sổ chính, thanh menu, thanh công cụ, cho đến các hộp thoại, bảng dữ liệu và biểu đồ tương tác.

### Ứng dụng cụ thể

Bảng dưới đây mô tả các thành phần của PyQt6 được sử dụng trong dự án, file áp dụng và chức năng tương ứng.

| Thành phần PyQt6 | File áp dụng | Chức năng |
|---|---|---|
| QApplication | src/app.py, src/main_app.py | Khởi tạo ứng dụng, quản lý vòng đời sự kiện |
| QMainWindow | src/main_window.py | Cửa sổ chính với menu bar, toolbar, status bar |
| QStackedWidget | src/gui/navigation.py | Chuyển đổi giữa các view (Dashboard, Khách hàng, Kho...) |
| QTableView / QTableWidget | src/gui/widgets/data_table.py | Hiển thị dữ liệu dạng bảng cho tất cả các module |
| QDialog | src/gui/dialogs/, src/gui/forms/ | Cửa sổ hội thoại MessageDialog, ConfirmDialog, InputDialog, FormDialog |
| QWizard | src/gui/wizards/ | Wizard 3 bước gia hạn và chấm dứt hợp đồng |
| QPushButton / QToolButton | src/gui/widgets/buttons.py | Các nút bấm tùy chỉnh |
| QLineEdit / QDateEdit / QComboBox | Tất cả các form | Nhập liệu thông tin khách hàng, hợp đồng, hàng hóa |
| QTabWidget | Các file detail_view.py | Tab chi tiết gồm Thông tin, Hợp đồng, Thanh toán, Lịch sử |
| QTimer | src/main_app.py | Kiểm tra session timeout, tự động đăng xuất |
| QComboBox | src/gui/widgets/search_box.py | Tìm kiếm và lọc dữ liệu |
| FigureCanvasQTAgg | src/gui/widgets/charts.py | Tích hợp biểu đồ matplotlib vào giao diện PyQt6 |
| QSS (Qt Style Sheets) | src/gui/styles/main.qss | Tùy chỉnh giao diện màu sắc, font chữ, hiệu ứng |

Đoạn code dưới đây từ file `src/app.py` minh họa cách khởi tạo ứng dụng PyQt6.

```python
app = QApplication(sys.argv)
app.setApplicationName("Quản Lý Kho Lưu Trữ")
app.setApplicationVersion("1.0.0")
with open("src/gui/styles/main.qss", "r", encoding="utf-8") as f:
    app.setStyleSheet(f.read())
```

---

## 2. SQLAlchemy — ORM và Tương Tác Cơ Sở Dữ Liệu

### Thông tin thư viện

SQLAlchemy là thư viện Object-Relational Mapping (ORM) cho Python, phiên bản yêu cầu từ 2.0.0 trở lên. Trang chủ tại https://www.sqlalchemy.org/.

### Vai trò trong đề tài

SQLAlchemy đóng vai trò ánh xạ các bảng trong cơ sở dữ liệu SQLite thành các lớp Python. Thay vì viết câu lệnh SQL thuần, lập trình viên có thể thao tác với database thông qua các đối tượng Python, giúp code trở nên trực quan và dễ bảo trì hơn.

### Ứng dụng cụ thể

Bảng dưới đây mô tả các thành phần SQLAlchemy được sử dụng và chức năng của chúng.

| Thành phần SQLAlchemy | File áp dụng | Chức năng |
|---|---|---|
| declarative_base | src/models/base.py | Tạo base class cho tất cả các model ORM |
| Column, String, Integer, Float, Date, DateTime, Enum, Text | src/models/*.py | Định nghĩa các cột trong database |
| ForeignKey, relationship | src/models/khach_hang.py, hop_dong.py,... | Định nghĩa quan hệ giữa các bảng (1-n, n-1) |
| create_engine | src/database/connection.py | Tạo kết nối đến database SQLite |
| sessionmaker, Session | src/database/connection.py, src/services/*.py | Quản lý phiên làm việc với database |
| Session, joinedload | src/database/repository.py | Repository pattern với CRUD generic |
| or_ | src/services/khach_hang_service.py, kho_service.py | Tạo câu truy vấn OR phức tạp |
| text | src/data/database.py, src/database/migrate.py | Thực thi câu lệnh SQL thuần (tạo view, index) |

Hệ thống bao gồm 9 model dữ liệu được định nghĩa bằng SQLAlchemy, bao gồm: KhachHang (khách hàng), Kho (kho hàng với diện tích và sức chứa), ViTri (vị trí lưu trữ trong kho theo khu vực, hàng, tầng), HopDong (hợp đồng thuê kho), HangHoa (hàng hóa lưu kho), ThanhToan (thanh toán và công nợ), NhanVien (nhân viên với phân quyền), SystemLog (audit log ghi lại mọi thao tác), và BaoCao (báo cáo). Ví dụ dưới đây từ file `src/models/khach_hang.py` minh họa cách định nghĩa một model.

```python
class KhachHang(BaseModel):
    __tablename__ = "khach_hang"
    ma_khach_hang = Column(String(20), primary_key=True)
    ho_ten = Column(String(200), nullable=False)
    loai_khach = Column(Enum(LoaiKhachEnum), default=LoaiKhachEnum.CA_NHAN)
```

Repository pattern được triển khai trong file `src/database/repository.py` với ba lớp. BaseRepository cung cấp các thao tác CRUD cơ bản gồm create, get_by_id, get_all, update, delete. SoftDeleteRepository kế thừa từ BaseRepository và hiện thực xóa mềm bằng cách đặt trạng thái thành "da_xoa" thay vì xóa vật lý. TimestampRepository tự động ghi nhận thời gian tạo và cập nhật cho mỗi bản ghi.

---

## 3. ReportLab — Tạo File PDF

### Thông tin thư viện

ReportLab là thư viện tạo file PDF chuyên nghiệp, phiên bản yêu cầu từ 4.0.0 trở lên. Trang chủ tại https://www.reportlab.com/.

### Vai trò trong đề tài

ReportLab được sử dụng để xuất các tài liệu PDF bao gồm hợp đồng thuê kho, hóa đơn thanh toán, phiếu nhập và xuất kho, cùng các báo cáo thống kê tổng hợp.

### Ứng dụng cụ thể

Bảng dưới đây mô tả các thành phần của ReportLab được sử dụng trong dự án.

| Thành phần ReportLab | File áp dụng | Chức năng |
|---|---|---|
| SimpleDocTemplate | src/services/pdf/pdf_generation_service.py | Tạo cấu trúc tài liệu PDF |
| Paragraph, Spacer, Table, TableStyle, Image, PageBreak | src/services/pdf/pdf_generation_service.py | Các thành phần layout trong PDF |
| getSampleStyleSheet, ParagraphStyle | src/services/pdf/pdf_generation_service.py | Định dạng văn bản và font chữ |
| colors | src/services/pdf/pdf_generation_service.py | Màu sắc cho bảng biểu |
| pagesizes (A4) | src/services/pdf/pdf_generation_service.py | Khổ giấy A4 cho tài liệu |
| pdfmetrics, TTFont | src/services/pdf/pdf_generation_service.py | Hỗ trợ font Unicode cho tiếng Việt |
| inch | src/services/pdf/pdf_generation_service.py | Đơn vị đo lường trong bố cục |

File `src/services/pdf/pdf_generation_service.py` định nghĩa ba hàm chính để tạo PDF. Hàm `generate_contract_pdf` nhận tham số hop_dong, khach_hang, vi_tri và output_path để tạo hợp đồng thuê kho đầy đủ điều khoản. Hàm `generate_invoice_pdf` nhận thanh_toan, hop_dong và output_path để tạo hóa đơn thanh toán. Hàm `generate_report_pdf` nhận data, report_type và output_path để tạo báo cáo thống kê.

---

## 4. Pandas & OpenPyXL — Xuất Dữ Liệu Excel

### Thông tin thư viện

Pandas (phiên bản từ 2.0.0) và OpenPyXL (phiên bản từ 3.1.0) là hai thư viện kết hợp để xuất dữ liệu ra file Excel. Trang chủ của Pandas tại https://pandas.pydata.org/ và của OpenPyXL tại https://openpyxl.readthedocs.io/.

### Vai trò trong đề tài

Hai thư viện này phối hợp để xuất dữ liệu từ hệ thống ra file Excel (.xlsx), phục vụ nhu cầu báo cáo và lưu trữ dữ liệu dưới dạng bảng tính có định dạng chuyên nghiệp.

### Ứng dụng cụ thể

Bảng dưới đây mô tả các thành phần được sử dụng.

| Thành phần | File áp dụng | Chức năng |
|---|---|---|
| pandas.DataFrame | src/utils/export_service.py | Chuyển đổi dữ liệu thành DataFrame để xuất Excel |
| pandas.ExcelWriter | src/utils/export_service.py | Ghi DataFrame vào file Excel |
| Workbook (openpyxl) | src/services/khach_hang_service.py | Tạo workbook Excel cho xuất khách hàng |
| Font, Alignment, Border, Side, PatternFill | src/services/khach_hang_service.py | Định dạng ô trong Excel (font, căn chỉnh, viền, màu nền) |

Hàm `export_to_excel` trong `src/utils/export_service.py` là hàm xuất dữ liệu tổng quát, nhận các tham số data, columns, sheet_name và filename. Hàm `export_khach_hang_to_excel` trong `src/services/khach_hang_service.py` xuất danh sách khách hàng ra Excel với định dạng chuyên nghiệp. Ngoài ra, các View như khach_hang_view, kho_view, hop_dong_view đều có phương thức `_on_export_excel` để xử lý sự kiện xuất Excel từ giao diện người dùng.

---

## 5. Matplotlib & NumPy — Vẽ Biểu Đồ

### Thông tin thư viện

Matplotlib (phiên bản từ 3.7.0) và NumPy (phiên bản từ 1.24.0) là hai thư viện vẽ biểu đồ và tính toán số học. Trang chủ của Matplotlib tại https://matplotlib.org/ và của NumPy tại https://numpy.org/.

### Vai trò trong đề tài

Matplotlib được sử dụng để vẽ các biểu đồ thống kê trực quan trên Dashboard, giúp người dùng nắm bắt nhanh tình hình kinh doanh thông qua biểu đồ cột doanh thu theo tháng, biểu đồ tròn phân bổ trạng thái, và biểu đồ thanh so sánh các chỉ số. NumPy hỗ trợ các tính toán số liệu nền tảng cho Matplotlib.

### Ứng dụng cụ thể

Bảng dưới đây mô tả các thành phần được sử dụng.

| Thành phần | File áp dụng | Chức năng |
|---|---|---|
| matplotlib.use('Agg') | src/gui/widgets/charts.py | Chọn backend không tương tác để tích hợp với PyQt6 |
| pyplot (plt) | src/gui/widgets/charts.py | Vẽ biểu đồ cột (bar chart) và biểu đồ tròn (pie chart) |
| FigureCanvasQTAgg | src/gui/widgets/charts.py | Tích hợp biểu đồ matplotlib vào widget PyQt6 |
| mpatches | src/gui/widgets/charts.py | Tạo chú thích (legend) cho biểu đồ |

File `src/gui/widgets/charts.py` định nghĩa ba lớp biểu đồ chính. Lớp `RevenueChart` là biểu đồ cột hiển thị doanh thu theo tháng. Lớp `PieChartWidget` là biểu đồ tròn hiển thị phân bổ trạng thái (ví dụ: tỷ lệ hợp đồng đang hiệu lực, hết hạn, chấm dứt). Lớp `BarChartWidget` là biểu đồ cột so sánh các chỉ số khác nhau.

---

## 6. Pillow (PIL) — Xử Lý Hình Ảnh

### Thông tin thư viện

Pillow (PIL Fork) là thư viện xử lý hình ảnh cho Python, phiên bản yêu cầu từ 10.0.0. Trang chủ tại https://python-pillow.org/.

### Vai trò trong đề tài

Pillow được khai báo trong requirements.txt với mục đích xử lý hình ảnh logo công ty và hình ảnh hàng hóa trong ứng dụng. Trong phiên bản hiện tại, model HangHoa tại file `src/models/hang_hoa.py` đã có trường `hinh_anh = Column(Text)` để lưu đường dẫn JSON của hình ảnh, sẵn sàng cho việc tích hợp Pillow vào các chức năng xử lý và hiển thị logo công ty trên hợp đồng PDF, lưu trữ và hiển thị hình ảnh hàng hóa, cũng như resize và tối ưu hình ảnh trước khi lưu vào database.

---

## 7. python-dateutil — Xử Lý Ngày Tháng

### Thông tin thư viện

python-dateutil là thư viện cung cấp các tiện ích xử lý ngày tháng nâng cao, phiên bản yêu cầu từ 2.8.0. Trang chủ tại https://dateutil.readthedocs.io/.

### Vai trò trong đề tài

Thư viện này cung cấp khả năng tính toán khoảng thời gian giữa các ngày theo đơn vị tháng và năm thông qua lớp `relativedelta`, một yêu cầu quan trọng trong quản lý hợp đồng thuê kho, thanh toán định kỳ và gia hạn hợp đồng.

### Ứng dụng cụ thể

Bảng dưới đây mô tả vị trí sử dụng `relativedelta` trong dự án.

| File áp dụng | Chức năng |
|---|---|
| src/services/hop_dong_service.py | Tính số tháng thuê từ ngày bắt đầu đến ngày kết thúc hợp đồng |
| src/services/thanh_toan_service.py | Tạo lịch thanh toán định kỳ hàng tháng hoặc hàng quý |
| src/gui/wizards/renewal_wizard.py | Tính ngày kết thúc mới khi gia hạn hợp đồng |
| src/gui/wizards/termination_wizard.py | Tính toán tiền phạt dựa trên thời gian còn lại của hợp đồng |
| src/utils/hop_dong_export.py | Tính tổng tiền thuê theo số tháng |
| src/gui/views/hop_dong_detail_view.py | Hiển thị thời hạn còn lại của hợp đồng |

Đoạn code dưới đây từ `src/services/hop_dong_service.py` minh họa cách sử dụng relativedelta.

```python
from dateutil.relativedelta import relativedelta

def get_contract_duration_months(self, hop_dong):
    delta = relativedelta(hop_dong.ngay_ket_thuc, hop_dong.ngay_bat_dau)
    return delta.years * 12 + delta.months

def generate_payment_schedule(self, hop_dong, frequency='monthly'):
    """Tạo lịch thanh toán tự động dựa trên relativedelta"""
```

---

## 8. bcrypt — Mã Hóa Mật Khẩu

### Thông tin thư viện

bcrypt là thư viện mã hóa mật khẩu một chiều với cơ chế salt tự động, phiên bản yêu cầu từ 4.0.0. Trang chủ tại https://pypi.org/project/bcrypt/.

### Vai trò trong đề tài

bcrypt được sử dụng để đảm bảo an toàn cho thông tin đăng nhập của người dùng thông qua cơ chế password hashing. Thư viện này có thể hash mật khẩu với gensalt, tạo salt ngẫu nhiên cho mỗi mật khẩu, và xác thực mật khẩu người dùng khi đăng nhập.

### Ứng dụng cụ thể

Tất cả các chức năng của bcrypt đều được triển khai trong file `src/services/auth/auth_service.py`. Cụ thể, phương thức `_hash_password` sử dụng `bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds=12))` để mã hóa mật khẩu với 12 rounds salt. Phương thức `verify_password` sử dụng `bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))` để kiểm tra mật khẩu người dùng nhập vào với hash đã lưu trong database. Hệ thống cũng có cơ chế fallback sang SHA-256 nếu bcrypt chưa được cài đặt.

Đoạn code dưới đây minh họa cách bcrypt được sử dụng.

```python
class AuthService:
    def _hash_password(self, password: str) -> str:
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds=12))
        return hashed.decode()

    def verify_password(self, password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(
            password.encode('utf-8'),
            hashed_password.encode('utf-8')
        )
```

---

## 9. Pytest & pytest-cov — Kiểm Thử

### Thông tin thư viện

Pytest (phiên bản từ 7.4.0) và pytest-cov (phiên bản từ 4.1.0) là framework kiểm thử tự động và công cụ đo lường mức độ bao phủ mã nguồn. Trang chủ tại https://pytest.org/.

### Vai trò trong đề tài

Pytest được sử dụng để viết và chạy các unit test và integration test, đảm bảo chất lượng và tính ổn định của mã nguồn. pytest-cov bổ sung tính năng đo lường mức độ bao phủ mã nguồn (code coverage) để đánh giá mức độ kiểm thử của dự án.

### Cấu trúc kiểm thử

Cây thư mục tests được tổ chức như sau.

```
tests/
  conftest.py                              Cấu hình chung và fixtures
  test_hang_hoa_service.py                 Test service hàng hóa
  test_hop_dong_alert.py                   Test cảnh báo hợp đồng
  test_hop_dong_components.py              Test component hợp đồng
  test_hop_dong_service.py                 Test service hợp đồng
  test_inventory_service.py                Test service tồn kho
  test_kho_service.py                      Test service kho
  test_vi_tri_service.py                   Test service vị trí
  test_integration/
    test_database_operations.py            Integration test database
  test_models/
    test_kho_model.py                      Test model Kho
  test_services/
    test_khach_hang_service.py             Test service khách hàng
    test_vi_tri_service.py                 Test service vị trí
  test_utils/
    test_formatters.py                     Test hàm định dạng
    test_validators.py                     Test hàm validate
```

### Cách chạy kiểm thử

Các lệnh dưới đây được sử dụng để chạy kiểm thử. Lệnh `pytest tests/ -v` chạy tất cả các test và hiển thị chi tiết. Lệnh `pytest tests/ --cov=src --cov-report=html` chạy test kèm báo cáo coverage dạng HTML. Lệnh `pytest tests/test_services/ -v` chạy test cho một module cụ thể.

---

## 10. Black — Định Dạng Mã Nguồn

### Thông tin thư viện

Black là công cụ định dạng mã nguồn Python tự động, phiên bản yêu cầu từ 23.0.0. Trang chủ tại https://black.readthedocs.io/.

### Vai trò trong đề tài

Black đảm bảo toàn bộ mã nguồn trong dự án có cùng phong cách trình bày, dễ đọc và dễ bảo trì. Lệnh `black .` được sử dụng để định dạng tất cả các file Python trong dự án. Lệnh `black --check .` được sử dụng để kiểm tra mà không thay đổi file.

---

## Tổng Kết

Bảng tổng kết dưới đây liệt kê tất cả các thư viện và công cụ sử dụng trong đề tài.

| STT | Thư viện / Công cụ | Phiên bản yêu cầu | Vai trò chính trong đề tài |
|---|---|---|---|
| 1 | PyQt6 | ≥ 6.4.0 | Xây dựng toàn bộ giao diện desktop (cửa sổ, form, bảng, hộp thoại) |
| 2 | SQLAlchemy | ≥ 2.0.0 | ORM kết nối và thao tác với cơ sở dữ liệu SQLite (9 models) |
| 3 | ReportLab | ≥ 4.0.0 | Xuất hợp đồng, hóa đơn, phiếu nhập/xuất ra file PDF |
| 4 | pandas | ≥ 2.0.0 | Xuất báo cáo thống kê ra file Excel |
| 5 | openpyxl | ≥ 3.1.0 | Định dạng file Excel (màu sắc, font chữ, viền, căn chỉnh) |
| 6 | matplotlib | ≥ 3.7.0 | Vẽ biểu đồ thống kê trên Dashboard (cột, tròn, thanh) |
| 7 | numpy | ≥ 1.24.0 | Hỗ trợ tính toán số liệu cho matplotlib |
| 8 | Pillow | ≥ 10.0.0 | Xử lý hình ảnh (logo công ty, hình ảnh hàng hóa) |
| 9 | python-dateutil | ≥ 2.8.0 | Tính toán ngày tháng hợp đồng, tạo lịch thanh toán |
| 10 | bcrypt | ≥ 4.0.0 | Mã hóa mật khẩu người dùng (12 rounds salt) |
| 11 | pytest | ≥ 7.4.0 | Kiểm thử tự động (unit test, integration test) |
| 12 | pytest-cov | ≥ 4.1.0 | Đo lường mức độ bao phủ mã nguồn |
| 13 | black | ≥ 23.0.0 | Định dạng mã nguồn Python tự động |

### Sơ đồ kiến trúc tổng quan

Sơ đồ dưới đây mô tả kiến trúc phân tầng của hệ thống và vị trí của từng thư viện trong kiến trúc đó.

```
                    +-----------------------------------+
                    |       PyQt6 (GUI Layer)           |
                    |  Views, Forms, Dialogs, Widgets,   |
                    |  Wizards, Charts (matplotlib)      |
                    +------------+----------------------+
                                 |
                    +------------v----------------------+
                    |        Services Layer              |
                    |  HopDongService, KhachHangService, |
                    |  KhoService, ThanhToanService...   |
                    |  bcrypt (auth), dateutil (dates)   |
                    +------------+----------------------+
                                 |
          +----------------------+----------------------+
          |                      |                      |
+---------v------+    +---------v------+    +----------v---------+
|   SQLAlchemy   |    |   ReportLab    |    |  Pandas + OpenPyXL |
|   (SQLite DB)  |    |  (PDF Export)  |    |  (Excel Export)    |
|   9 models     |    | Contract,      |    |  Customer lists,   |
|   Repository   |    | Invoice,       |    |  Reports,          |
|   pattern      |    | Report         |    |  Statistics        |
+----------------+    +----------------+    +--------------------+
                                 |
                    +------------v----------------------+
                    |       Utilities Layer              |
                    |  validators.py, formatters.py,     |
                    |  helpers.py, export_service.py,    |
                    |  Pillow (images), dateutil         |
                    +-----------------------------------+
```

### Luồng xử lý nghiệp vụ điển hình

Phần này mô tả quy trình xử lý khi người dùng tạo một hợp đồng thuê kho mới.

Bước đầu tiên, người dùng nhập liệu trên form PyQt6 thông qua HopDongForm tại file `src/gui/forms/hop_dong_form.py`. Tại đây, người dùng chọn khách hàng bằng QComboBox, chọn vị trí kho bằng QListWidget, nhập ngày tháng bằng QDateEdit, và nhập giá thuê bằng QDoubleSpinBox.

Sau khi người dùng xác nhận, dữ liệu được chuyển đến HopDongService.create thông qua file `src/services/hop_dong_service.py`. Service này thực hiện validate dữ liệu đầu vào, tự động sinh mã hợp đồng theo định dạng HDYYYYMMXXX, gọi dateutil.relativedelta để tính thời hạn hợp đồng, lưu xuống database qua SQLAlchemy Session, và cập nhật trạng thái vị trí thành "Đã thuê".

Tiếp theo, SQLAlchemy ORM tại `src/database/connection.py` thực hiện session.add(hop_dong) để thêm hợp đồng mới, session.commit() để lưu thay đổi vào database, và cập nhật trường vi_tri.trang_thai thành DA_THUE.

Cuối cùng, phản hồi kết quả được hiển thị qua MessageDialog của PyQt6. Nếu thành công, hệ thống hiển thị thông báo xanh. Nếu thất bại, hệ thống hiển thị lỗi đỏ.

---

## Tài liệu tham khảo

Các tài liệu tham khảo chính thức của từng thư viện được liệt kê dưới đây.

PyQt6 Documentation tại https://www.riverbankcomputing.com/static/Docs/PyQt6/

SQLAlchemy 2.0 Documentation tại https://docs.sqlalchemy.org/en/20/

ReportLab User Guide tại https://www.reportlab.com/docs/reportlab-userguide.pdf

pandas Documentation tại https://pandas.pydata.org/docs/

Matplotlib Documentation tại https://matplotlib.org/stable/contents.html

Pillow Documentation tại https://pillow.readthedocs.io/

python-dateutil Documentation tại https://dateutil.readthedocs.io/

bcrypt Documentation tại https://pypi.org/project/bcrypt/

pytest Documentation tại https://docs.pytest.org/

Black Documentation tại https://black.readthedocs.io/
