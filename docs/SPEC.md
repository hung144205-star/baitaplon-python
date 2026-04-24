# PHÂN TÍCH VÀ ĐẶC TẢ KỸ THUẬT
## Phần mềm Quản lý Dịch vụ Cho Thuê Kho Lưu Trữ Hàng Hóa

---

## 1. TỔNG QUAN HỆ THỐNG

### 1.1 Mục tiêu
Xây dựng hệ thống phần mềm quản lý toàn diện dịch vụ cho thuê kho lưu trữ hàng hóa, hỗ trợ:
- Quản lý thông tin khách hàng và hợp đồng thuê kho
- Quản lý kho hàng và vị trí lưu trữ
- Theo dõi nhập/xuất hàng hóa
- Báo cáo thống kê doanh thu và tình trạng kho

### 1.2 Phạm vi
- Quản lý khách hàng đăng ký thuê kho
- Quản lý danh sách kho và vị trí lưu trữ
- Quản lý hợp đồng thuê (tạo mới, gia hạn, chấm dứt)
- Theo dõi hàng hóa nhập/xuất kho
- Thanh toán và quản lý công nợ
- Báo cáo thống kê

### 1.3 Đối tượng sử dụng
| Vai trò | Chức năng chính |
|---------|----------------|
| Quản trị viên | Quản lý toàn bộ hệ thống, nhân viên, cấu hình |
| Nhân viên kho | Quản lý nhập/xuất hàng, kiểm kê |
| Nhân viên kinh doanh | Quản lý khách hàng, hợp đồng |
| Kế toán | Thanh toán, báo cáo doanh thu |

---

## 2. PHÂN TÍCH CHỨC NĂNG

### 2.1 Module Quản lý Khách hàng

#### 2.1.1 Chức năng
- **Thêm khách hàng mới**: Lưu trữ thông tin cá nhân/doanh nghiệp
- **Cập nhật thông tin**: Sửa đổi thông tin khi có thay đổi
- **Xóa khách hàng**: Chỉ khi không còn hợp đồng đang hoạt động
- **Tìm kiếm khách hàng**: Theo mã, tên, SĐT, email
- **Xem lịch sử thuê**: Danh sách hợp đồng và giao dịch

#### 2.1.2 Thông tin khách hàng
| Trường | Kiểu dữ liệu | Mô tả |
|--------|-------------|-------|
| ma_khach_hang | String (PK) | Mã định danh duy nhất |
| ho_ten | String | Họ tên/Tên công ty |
| loai_khach | Enum | Cá nhân/Doanh nghiệp |
| so_dien_thoai | String | Số điện thoại liên hệ |
| email | String | Email liên hệ |
| dia_chi | String | Địa chỉ liên hệ |
| ma_so_thue | String | Mã số thuế (nếu là doanh nghiệp) |
| ngay_dang_ky | Date | Ngày đăng ký |
| trang_thai | Enum | Hoạt động/Tạm khóa |

### 2.2 Module Quản lý Kho hàng

#### 2.2.1 Chức năng
- **Thêm kho mới**: Định nghĩa kho và sức chứa
- **Phân vùng lưu trữ**: Chia kho thành các khu vực, vị trí
- **Theo dõi sức chứa**: Cập nhật tình trạng lấp đầy
- **Bảo trì kho**: Lịch sử sửa chữa, bảo dưỡng

#### 2.2.2 Thông tin kho hàng
| Trường | Kiểu dữ liệu | Mô tả |
|--------|-------------|-------|
| ma_kho | String (PK) | Mã kho |
| ten_kho | String | Tên kho |
| dia_chi | String | Địa chỉ kho |
| dien_tich | Float | Tổng diện tích (m²) |
| suc_chua | Float | Sức chứa tối đa (m³ hoặc kg) |
| da_su_dung | Float | Diện tích/volume đã sử dụng |
| trang_thai | Enum | Hoạt động/Bảo trì/Ngừng |

#### 2.2.3 Vị trí lưu trữ (chi tiết)
| Trường | Kiểu dữ liệu | Mô tả |
|--------|-------------|-------|
| ma_vi_tri | String (PK) | Mã vị trí (vd: K01-A-01-01) |
| ma_kho | String (FK) | Kho chứa |
| khu_vuc | String | Khu vực trong kho |
| hang | String | Hàng/Zone |
| tang | Integer | Tầng |
| dien_tich | Float | Diện tích vị trí |
| gia_thue | Float | Giá thuê/đơn vị diện tích/tháng |
| trang_thai | Enum | Trống/Đã thuê/Bảo trì |

### 2.3 Module Quản lý Hợp đồng

#### 2.3.1 Chức năng
- **Tạo hợp đồng mới**: Đăng ký thuê kho/vị trí
- **Gia hạn hợp đồng**: Kéo dài thời gian thuê
- **Chấm dứt hợp đồng**: Kết thúc trước hạn hoặc hết hạn
- **Theo dõi thanh toán**: Công nợ, đã thanh toán

#### 2.3.2 Thông tin hợp đồng
| Trường | Kiểu dữ liệu | Mô tả |
|--------|-------------|-------|
| ma_hop_dong | String (PK) | Mã hợp đồng |
| ma_khach_hang | String (FK) | Khách hàng thuê |
| ma_vi_tri | String (FK) | Vị trí thuê |
| ngay_bat_dau | Date | Ngày bắt đầu thuê |
| ngay_ket_thuc | Date | Ngày kết thúc |
| gia_thue | Float | Giá thuê thỏa thuận |
| tien_coc | Float | Tiền đặt cọc |
| dieu_khoan | Text | Các điều khoản đặc biệt |
| trang_thai | Enum | Hiệu lực/Hết hạn/Chấm dứt |

### 2.4 Module Quản lý Hàng hóa

#### 2.4.1 Chức năng
- **Nhập hàng vào kho**: Ghi nhận hàng hóa mới
- **Xuất hàng khỏi kho**: Ghi nhận hàng rời kho
- **Kiểm kê định kỳ**: Đối chiếu thực tế với hệ thống
- **Theo dõi tồn kho**: Số lượng, vị trí hiện tại

#### 2.4.2 Thông tin hàng hóa
| Trường | Kiểu dữ liệu | Mô tả |
|--------|-------------|-------|
| ma_hang_hoa | String (PK) | Mã hàng hóa |
| ma_hop_dong | String (FK) | Hợp đồng chứa hàng |
| ten_hang | String | Tên hàng hóa |
| loai_hang | String | Loại hàng (thực phẩm, điện tử, v.v.) |
| so_luong | Integer | Số lượng |
| don_vi | String | Đơn vị tính |
| trong_luong | Float | Trọng lượng (kg) |
| kich_thuoc | String | Kích thước (DxRxC) |
| ngay_nhap | DateTime | Thời điểm nhập kho |
| ngay_xuat | DateTime | Thời điểm xuất kho (nếu có) |
| trang_thai | Enum | Trong kho/Đã xuất |

### 2.5 Module Thanh toán

#### 2.5.1 Chức năng
- **Tạo hóa đơn**: Tự động tính tiền thuê định kỳ
- **Ghi nhận thanh toán**: Tiền mặt/Chuyển khoản
- **Theo dõi công nợ**: Số tiền chưa thanh toán
- **Phí phạt**: Trễ hạn, vi phạm hợp đồng

#### 2.5.2 Thông tin thanh toán
| Trường | Kiểu dữ liệu | Mô tả |
|--------|-------------|-------|
| ma_thanh_toan | String (PK) | Mã giao dịch |
| ma_hop_dong | String (FK) | Hợp đồng thanh toán |
| loai_phi | Enum | Tiền cọc/Thuê tháng/Phí phạt |
| so_tien | Float | Số tiền |
| ngay_thanh_toan | Date | Ngày thanh toán |
| phuong_thuc | Enum | Tiền mặt/Chuyển khoản |
| trang_thai | Enum | Đã thanh toán/Chưa thanh toán |

### 2.6 Module Báo cáo

#### 2.6.1 Các loại báo cáo
| Báo cáo | Mô tả | Tần suất |
|---------|-------|----------|
| Doanh thu | Tổng thu theo ngày/tháng/năm | Ngày/Tháng |
| Tỷ lệ lấp đầy | % sức chứa kho đã sử dụng | Tuần/Tháng |
| Hợp đồng sắp hết hạn | Danh sách cần gia hạn | Tuần |
| Công nợ | Khách hàng chưa thanh toán | Tháng |
| Xuất nhập tồn | Biến động hàng hóa | Tháng |

---

## 3. THIẾT KẾ CƠ SỞ DỮ LIỆU

### 3.1 Sơ đồ ER (Entity-Relationship)

```
[KhachHang] 1---* [HopDong] *---1 [ViTri]
    |                           |
    |                           |
    *                           *
[ThanhToan]                 [Kho]
                               |
                               1
                               |
                          [HangHoa]
```

### 3.2 Mối quan hệ
- **Khách hàng - Hợp đồng**: 1 khách hàng có nhiều hợp đồng
- **Hợp đồng - Vị trí**: 1 vị trí có thể có nhiều hợp đồng (theo thời gian)
- **Hợp đồng - Thanh toán**: 1 hợp đồng có nhiều lần thanh toán
- **Hợp đồng - Hàng hóa**: 1 hợp đồng chứa nhiều loại hàng hóa
- **Kho - Vị trí**: 1 kho có nhiều vị trí lưu trữ

---

## 4. KIẾN TRÚC PHẦN MỀM

### 4.1 Mô hình kiến trúc
- **Mô hình**: 3-Layer Architecture (Presentation - Business - Data)
- **Giao diện**: Console (Command Line Interface)
- **Database**: SQLite

### 4.2 Cấu trúc thư mục
```
src/
├── main.py                 # Entry point
├── presentation/           # Tầng giao diện
│   ├── menu.py
│   └── views/
├── business/              # Tầng nghiệp vụ
│   ├── services/
│   └── models/
└── data/                  # Tầng dữ liệu
    ├── database.py
    └── repositories/
```

---

## 5. YÊU CẦU PHI CHỨC NĂNG

### 5.1 Hiệu năng
- Thời gian phản hồi tìm kiếm: ≤ 2 giây với 10,000 bản ghi
- Hỗ trợ đồng thời 20 người dùng

### 5.2 Bảo mật
- Xác thực đăng nhập
- Phân quyền theo vai trò
- Mã hóa mật khẩu

### 5.3 Độ tin cậy
- Backup dữ liệu định kỳ
- Ghi log thao tác quan trọng

### 5.4 Khả năng sử dụng
- Giao diện tiếng Việt
- Menu trực quan, dễ sử dụng
- Hướng dẫn sử dụng tích hợp

---

## 6. CÔNG NGHỆ SỬ DỤNG

| Thành phần | Công nghệ |
|------------|-----------|
| Ngôn ngữ | Python 3.8+ |
| Database | SQLite |
| Giao diện | Console (CLI) |
| Thư viện hỗ trợ | colorama, tabulate, reportlab |
| Testing | pytest |
| Version Control | Git |

---

## 7. KẾ HOẠCH TRIỂN KHAI

### Giai đoạn 1: Thiết lập (Tuần 1)
- [ ] Thiết kế database schema
- [ ] Tạo cấu trúc project
- [ ] Setup connection database

### Giai đoạn 2: Core Modules (Tuần 2-3)
- [ ] Module Quản lý Khách hàng
- [ ] Module Quản lý Kho hàng
- [ ] Module Quản lý Hợp đồng

### Giai đoạn 3: Nghiệp vụ (Tuần 4)
- [ ] Module Quản lý Hàng hóa
- [ ] Module Thanh toán
- [ ] Báo cáo thống kê

### Giai đoạn 4: Hoàn thiện (Tuần 5)
- [ ] Giao diện console hoàn chỉnh
- [ ] Testing và sửa lỗi
- [ ] Viết tài liệu hướng dẫn

---
