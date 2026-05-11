# Tài Liệu Mô Tả Sơ Đồ Class Diagram

## Quản Lý Dịch Vụ Cho Thuê Kho Lưu Trữ Hàng Hóa

---

## 1. Tổng Quan

Sơ đồ class diagram mô tả kiến trúc hệ thống **Quản Lý Kho Lưu Trữ**, thể hiện:

- Các thực thể (entities) trong hệ thống
- Thuộc tính và kiểu dữ liệu của từng class
- Mối quan hệ giữa các class (inheritance, association)
- Các enum types định nghĩa trạng thái

---

## 2. Kiến Trúc BaseModel

```
BaseModel (Abstract)
├── ngay_tao: DateTime
├── ngay_cap_nhat: DateTime
├── to_dict(): dict
```

**Mục đích:** Là base class cho tất cả models, cung cấp:
- 2 columns chung: `ngay_tao`, `ngay_cap_nhat`
- Method `to_dict()` chuyển đổi model sang dictionary

---

## 3. Các Models Chính

### 3.1 Kho (Warehouse)

| Thuộc tính | Kiểu | Mô tả |
|-----------|------|-------|
| ma_kho | String(20) PK | Mã kho |
| ten_kho | String(200) | Tên kho |
| dia_chi | String(500) | Địa chỉ |
| dien_tich | Float | Diện tích (m²) |
| suc_chua | Float | Sức chứa (m³) |
| da_su_dung | Float | Diện tích đã sử dụng |
| trang_thai | TrangThaiKhoEnum | Trạng thái kho |

**Properties:**
- `ty_le_lap_day`: Tỷ lệ lấp đầy (%) = (da_su_dung / suc_chua) × 100
- `dung_tich_con_lai`: Sức chứa còn lại

**Enum sử dụng:** `TrangThaiKhoEnum` { HOAT_DONG, BAO_TRI, NGUNG }

---

### 3.2 ViTri (Storage Position)

| Thuộc tính | Kiểu | Mô tả |
|-----------|------|-------|
| ma_vi_tri | String(30) PK | Mã vị trí |
| ma_kho | String(20) FK | Mã kho cha |
| khu_vuc | String(50) | Khu vực (A, B, C...) |
| hang | String(10) | Hàng (1-10) |
| tang | Integer | Tầng (1-5) |
| dien_tich | Float | Diện tích (m²) |
| gia_thue | Float | Giá thuê |
| suc_chua | Float | Sức chứa |
| trang_thai | TrangThaiViTriEnum | Trạng thái |

**Enum sử dụng:** `TrangThaiViTriEnum` { TRONG, DA_THUE, BAO_TRI }

---

### 3.3 KhachHang (Customer)

| Thuộc tính | Kiểu | Mô tả |
|-----------|------|-------|
| ma_khach_hang | String(20) PK | Mã khách hàng |
| ho_ten | String(200) | Họ tên |
| loai_khach | LoaiKhachEnum | Loại khách hàng |
| so_dien_thoai | String(20) | Số điện thoại |
| email | String(100) | Email (unique) |
| dia_chi | String(500) | Địa chỉ |
| ma_so_thue | String(20) | Mã số thuế |
| ngay_dang_ky | Date | Ngày đăng ký |
| trang_thai | TrangThaiKHEnum | Trạng thái |

**Enum sử dụng:**
- `LoaiKhachEnum` { CA_NHAN, DOANH_NGHIEP }
- `TrangThaiKHEnum` { HOAT_DONG, TAM_KHOA, DA_XOA }

---

### 3.4 HopDong (Contract)

| Thuộc tính | Kiểu | Mô tả |
|-----------|------|-------|
| ma_hop_dong | String(20) PK | Mã hợp đồng |
| ma_khach_hang | String(20) FK | Mã khách hàng |
| ma_vi_tri | String(30) FK | Mã vị trí thuê |
| ngay_bat_dau | Date | Ngày bắt đầu |
| ngay_ket_thuc | Date | Ngày kết thúc |
| gia_thue | Float | Giá thuê |
| tien_coc | Float | Tiền cọc |
| phuong_thuc_thanh_toan | String | Hình thức thanh toán |
| dieu_khoan | Text | Điều khoản hợp đồng |
| trang_thai | TrangThaiHDEnum | Trạng thái |
| ly_do_cham_dut | Text | Lý do chấm dứt |
| ngay_cham_dut | Date | Ngày chấm dứt |

**Enum sử dụng:** `TrangThaiHDEnum` { HIEU_LUC, HET_HAN, CHAM_DUT, GIA_HAN }

---

### 3.5 HangHoa (Goods)

| Thuộc tính | Kiểu | Mô tả |
|-----------|------|-------|
| ma_hang_hoa | String(30) PK | Mã hàng hóa |
| ma_hop_dong | String(20) FK | Mã hợp đồng |
| ten_hang | String(200) | Tên hàng |
| loai_hang | String(100) | Loại hàng |
| so_luong | Integer | Số lượng |
| don_vi | String(20) | Đơn vị tính |
| trong_luong | Float | Trọng lượng (kg) |
| kich_thuoc | String(50) | Kích thước |
| gia_tri | Float | Giá trị |
| ngay_nhap | DateTime | Ngày nhập kho |
| ngay_xuat | DateTime | Ngày xuất kho |
| trang_thai | String(20) | Trạng thái |
| vi_tri_luu_tru | String(30) | Vị trí lưu trữ |

**Enum sử dụng:** `TrangThaiHHEnum` { TRONG_KHO, DA_XUAT }

---

### 3.6 ThanhToan (Payment)

| Thuộc tính | Kiểu | Mô tả |
|-----------|------|-------|
| ma_thanh_toan | String(30) PK | Mã thanh toán |
| ma_hop_dong | String(20) FK | Mã hợp đồng |
| loai_phi | LoaiPhiEnum | Loại phí |
| so_tien | Float | Số tiền |
| ky_thanh_toan | String(20) | Kỳ thanh toán |
| ngay_den_han | Date | Ngày đến hạn |
| ngay_thanh_toan | Date | Ngày thanh toán |
| phuong_thuc | String(20) | Phương thức |
| so_giao_dich | String(50) | Số giao dịch |
| trang_thai | TrangThaiTTEnum | Trạng thái |
| phi_phat | Float | Phí phạt |
| nguoi_thu | String(100) | Người thu |
| ghi_chu | Text | Ghi chú |

**Enum sử dụng:**
- `LoaiPhiEnum` { TIEN_COC, THUE_THANG, PHU_PHI, PHI_PHAT }
- `TrangThaiTTEnum` { DA_THANH_TOAN, CHUA_THANH_TOAN, QUA_HAN }

---

### 3.7 NhanVien (Employee)

| Thuộc tính | Kiểu | Mô tả |
|-----------|------|-------|
| ma_nhan_vien | String(20) PK | Mã nhân viên |
| ho_ten | String(200) | Họ tên |
| email | String(100) | Email (unique) |
| so_dien_thoai | String(20) | SĐT |
| vai_tro | VaiTroNhanVienEnum | Vai trò |
| tai_khoan | String(50) | Tài khoản đăng nhập |
| mat_khau | String(255) | Mật khẩu (bcrypt hash) |
| trang_thai | TrangThaiNhanVienEnum | Trạng thái |
| lan_dang_nhap_cuoi | String(50) | Lần đăng nhập cuối |

**Enum sử dụng:**
- `VaiTroNhanVienEnum` { QUAN_TRI, KINH_DOANH, KHO, KE_TOAN }
- `TrangThaiNhanVienEnum` { HOAT_DONG, NGUNG_HOAT_DONG }

---

## 4. Mối Quan Hệ (Relationships)

```
┌──────────────┐         ┌──────────────┐
│     Kho      │─────────│    ViTri     │
│  (1 warehouse)│ 1:N   │ (N positions)│
└──────────────┘         └──────────────┘
                                │
                                │ N
                                ▼
┌──────────────┐         ┌──────────────┐
│  KhachHang   │─────────│   HopDong    │
│  (1 customer) │ 1:N    │  (N contracts)│
└──────────────┘         └──────────────┘
                                  │
                    ┌─────────────┴─────────────┐
                    │ N                       │ N
                    ▼                         ▼
           ┌──────────────┐          ┌──────────────┐
           │   HangHoa    │          │  ThanhToan   │
           │  (N goods)   │          │ (N payments) │
           └──────────────┘          └──────────────┘
```

### Chi Tiết Các Associations

| Từ | Đến | Loại | Mô tả |
|----|-----|------|-------|
| Kho | ViTri | 1:N | Một kho có nhiều vị trí lưu trữ |
| KhachHang | HopDong | 1:N | Một khách hàng có thể thuê nhiều kho qua nhiều hợp đồng |
| ViTri | HopDong | 1:N | Mỗi vị trí có thể được thuê bởi nhiều hợp đồng (theo thời gian) |
| HopDong | HangHoa | 1:N | Mỗi hợp đồng có thể lưu trữ nhiều hàng hóa |
| HopDong | ThanhToan | 1:N | Mỗi hợp đồng có nhiều lần thanh toán |

### Inheritance

Tất cả các models kế thừa từ `BaseModel`:
- Kho, ViTri, KhachHang, HopDong, HangHoa, ThanhToan, NhanVien

---

## 5. Enums Trung Tâm

Tất cả enum types được định nghĩa tập trung trong `src/models/enums.py`:

| Enum | Giá trị | Sử dụng |
|------|---------|---------|
| TrangThaiHDEnum | HIEU_LUC, HET_HAN, CHAM_DUT, GIA_HAN | HopDong.trang_thai |
| TrangThaiTTEnum | DA_THANH_TOAN, CHUA_THANH_TOAN, QUA_HAN | ThanhToan.trang_thai |
| TrangThaiViTriEnum | TRONG, DA_THUE, BAO_TRI | ViTri.trang_thai |
| TrangThaiKhoEnum | HOAT_DONG, BAO_TRI, NGUNG | Kho.trang_thai |
| LoaiKhachEnum | CA_NHAN, DOANH_NGHIEP | KhachHang.loai_khach |
| TrangThaiKHEnum | HOAT_DONG, TAM_KHOA, DA_XOA | KhachHang.trang_thai |
| LoaiPhiEnum | TIEN_COC, THUE_THANG, PHU_PHI, PHI_PHAT | ThanhToan.loai_phi |
| TrangThaiHHEnum | TRONG_KHO, DA_XUAT | HangHoa (internal) |
| VaiTroNhanVienEnum | QUAN_TRI, KINH_DOANH, KHO, KE_TOAN | NhanVien.vai_tro |
| TrangThaiNhanVienEnum | HOAT_DONG, NGUNG_HOAT_DONG | NhanVien.trang_thai |
| HanhDongLogEnum | THEM, SUA, XOA, DANG_NHAP, DANG_XUAT | SystemLog |

---

## 6. Luồng Nghiệp Vụ Chính

### 6.1 Tạo Hợp Đồng Thuê Kho

```
1. KhachHang (tạo/cập nhật thông tin)
       │
       ▼
2. HopDong (tạo hợp đồng mới, liên kết KH + vị trí)
       │
       ▼
3. ViTri (cập nhật trạng_thai = DA_THUE)
       │
       ▼
4. ThanhToan (tạo thanh toán tiền cọc)
```

### 6.2 Nhập Hàng Hóa

```
1. HopDong (xác nhận đang hiệu lực)
       │
       ▼
2. HangHoa (nhập thông tin hàng hóa, liên kết HD)
       │
       ▼
3. Kho (cập nhật da_su_dung tăng)
```

### 6.3 Thanh Toán Định Kỳ

```
1. HopDong (kiểm tra trạng thái)
       │
       ▼
2. ThanhToan (tạo bản ghi thanh toán, cập nhật trạng thái)
       │
       ▼
3. ThanhToan (tính phi_phat nếu quá hạn)
```

---

## 7. Quy Tắc Đặt Tên

| Thành phần | Quy tắc | Ví dụ |
|-----------|---------|-------|
| Primary Key | ma_<ten>_id | ma_kho, ma_hop_dong |
| Foreign Key | ma_<ten> | ma_khach_hang, ma_vi_tri |
| Enum | TrangThai<Ten>Enum | TrangThaiHDEnum |
| Relationship | back_populates | hop_dongs, hang_hoas |

---

## 8. Tệp Tin Liên Quan

| Tệp | Mô tả |
|-----|-------|
| `src/models/base.py` | Định nghĩa BaseModel |
| `src/models/enums.py` | Tất cả enum definitions |
| `src/models/kho.py` | Kho model |
| `src/models/vi_tri.py` | ViTri model |
| `src/models/khach_hang.py` | KhachHang model |
| `src/models/hop_dong.py` | HopDong model |
| `src/models/hang_hoa.py` | HangHoa model |
| `src/models/thanh_toan.py` | ThanhToan model |
| `src/models/nhan_vien.py` | NhanVien model |

---

## 9. Sơ Đồ Mở Rộng (Draw.io)

Để chỉnh sửa sơ đồ:
1. Mở file `docs/class-diagram-warehouse.drawio.xml` bằng [app.diagrams.net](https://app.diagrams.net)
2. Hoặc sử dụng VS Code extension **Draw.io Integration**
3. Export sang PNG/PDF khi cần chia sẻ

---

*Cập nhật: 2026-05-10*
