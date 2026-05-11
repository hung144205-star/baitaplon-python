# Tài Liệu Mô Tả Sơ Đồ ERD

## Quản Lý Dịch Vụ Cho Thuê Kho Lưu Trữ Hàng Hóa

---

## 1. Tổng Quan

Sơ đồ ERD (Entity-Relationship Diagram) mô tả cấu trúc cơ sở dữ liệu của hệ thống **Quản Lý Kho Lưu Trữ**, thể hiện:

- 7 bảng chính (entities)
- Các cột (columns) và kiểu dữ liệu
- Khóa chính (Primary Key) và khóa ngoại (Foreign Key)
- Mối quan hệ giữa các bảng (1:N)
- Ràng buộc NOT NULL và DEFAULT

---

## 2. Sơ Đồ Mối Quan Hệ

```
┌──────────────┐       ┌──────────────┐       ┌──────────────┐
│     KHO      │───────│    VI_TRI    │───────│   HOP_DONG   │
│  (1 kho)     │  1:N  │  (N vị trí)  │  1:N  │ (N hợp đồng) │
└──────────────┘       └──────────────┘       └───────┬──────┘
                                                      │
                         ┌────────────────────────────┤
                         │                            │
                    ┌────┴────┐                ┌────┴────┐
                    │HANG_HOA │                │THANH_TOAN│
                    │(N hàng) │                │(N thanh toán)│
                    └─────────┘                └──────────┘
                         │
                    ┌────┴────┐
                    │KHACH_HANG│
                    │(1 khách) │
                    └─────────┘
```

---

## 3. Chi Tiết Từng Bảng

### 3.1 `nhan_vien` - Nhân Viên

| Trường | Kiểu | Ràng buộc | Mô tả |
|--------|------|-----------|-------|
| ma_nhan_vien | VARCHAR(20) | **PK**, NOT NULL | Mã nhân viên |
| ho_ten | VARCHAR(200) | NOT NULL | Họ tên |
| email | VARCHAR(100) | UNIQUE, NOT NULL | Email (đăng nhập) |
| so_dien_thoai | VARCHAR(20) | - | Số điện thoại |
| vai_tro | VARCHAR(20) | NOT NULL | Vai trò: QUAN_TRI, KINH_DOANH, KHO, KE_TOAN |
| tai_khoan | VARCHAR(50) | UNIQUE, NOT NULL | Tài khoản đăng nhập |
| mat_khau | VARCHAR(255) | NOT NULL | Mật khẩu (bcrypt hash) |
| trang_thai | VARCHAR(20) | NOT NULL | HOAT_DONG / NGUNG_HOAT_DONG |
| lan_dang_nhap_cuoi | VARCHAR(50) | - | Lần đăng nhập cuối |

**Ghi chú:** Bảng nhan_vien chỉ dùng để xác thực người dùng, không tham gia vào các mối quan hệ nghiệp vụ chính.

---

### 3.2 `kho` - Kho Hàng

| Trường | Kiểu | Ràng buộc | Mô tả |
|--------|------|-----------|-------|
| ma_kho | VARCHAR(20) | **PK**, NOT NULL | Mã kho |
| ten_kho | VARCHAR(200) | NOT NULL | Tên kho |
| dia_chi | VARCHAR(500) | NOT NULL | Địa chỉ |
| dien_tich | FLOAT | NOT NULL | Diện tích (m²) |
| suc_chua | FLOAT | NOT NULL | Sức chứa (m³) |
| da_su_dung | FLOAT | NOT NULL, DEFAULT 0 | Diện tích đã sử dụng |
| trang_thai | VARCHAR(20) | NOT NULL | HOAT_DONG / BAO_TRI / NGUNG |
| ngay_tao | DATETIME | NOT NULL | Ngày tạo (từ BaseModel) |
| ngay_cap_nhat | DATETIME | - | Ngày cập nhật (từ BaseModel) |

---

### 3.3 `vi_tri` - Vị Trí Lưu Trữ

| Trường | Kiểu | Ràng buộc | Mô tả |
|--------|------|-----------|-------|
| ma_vi_tri | VARCHAR(30) | **PK**, NOT NULL | Mã vị trí |
| ma_kho | VARCHAR(20) | **FK**, NOT NULL | Mã kho chứa |
| khu_vuc | VARCHAR(50) | NOT NULL | Khu vực (A, B, C...) |
| hang | VARCHAR(10) | NOT NULL | Hàng (1-10) |
| tang | INTEGER | NOT NULL, DEFAULT 1 | Tầng (1-5) |
| dien_tich | FLOAT | NOT NULL | Diện tích (m²) |
| gia_thue | FLOAT | NOT NULL | Giá thuê |
| suc_chua | FLOAT | - | Sức chứa |
| trang_thai | VARCHAR(20) | NOT NULL | TRONG / DA_THUE / BAO_TRI |
| ngay_tao | DATETIME | NOT NULL | Ngày tạo |
| ngay_cap_nhat | DATETIME | - | Ngày cập nhật |

**Khóa ngoại:**
- `ma_kho` → `kho.ma_kho` (ON DELETE RESTRICT)

---

### 3.4 `khach_hang` - Khách Hàng

| Trường | Kiểu | Ràng buộc | Mô tả |
|--------|------|-----------|-------|
| ma_khach_hang | VARCHAR(20) | **PK**, NOT NULL | Mã khách hàng |
| ho_ten | VARCHAR(200) | NOT NULL | Họ tên |
| loai_khach | VARCHAR(20) | NOT NULL | CA_NHAN / DOANH_NGHIEP |
| so_dien_thoai | VARCHAR(20) | NOT NULL | Số điện thoại |
| email | VARCHAR(100) | UNIQUE | Email |
| dia_chi | VARCHAR(500) | NOT NULL | Địa chỉ |
| ma_so_thue | VARCHAR(20) | - | Mã số thuế (doanh nghiệp) |
| ngay_dang_ky | DATE | NOT NULL | Ngày đăng ký |
| trang_thai | VARCHAR(20) | NOT NULL | HOAT_DONG / TAM_KHOA / DA_XOA |
| ngay_tao | DATETIME | NOT NULL | Ngày tạo |
| ngay_cap_nhat | DATETIME | - | Ngày cập nhật |

---

### 3.5 `hop_dong` - Hợp Đồng Thuê

| Trường | Kiểu | Ràng buộc | Mô tả |
|--------|------|-----------|-------|
| ma_hop_dong | VARCHAR(20) | **PK**, NOT NULL | Mã hợp đồng |
| ma_khach_hang | VARCHAR(20) | **FK**, NOT NULL | Mã khách hàng |
| ma_vi_tri | VARCHAR(30) | **FK**, NOT NULL | Mã vị trí thuê |
| ngay_bat_dau | DATE | NOT NULL | Ngày bắt đầu |
| ngay_ket_thuc | DATE | NOT NULL | Ngày kết thúc |
| gia_thue | FLOAT | NOT NULL | Giá thuê |
| tien_coc | FLOAT | NOT NULL, DEFAULT 0 | Tiền cọc |
| phuong_thuc_thanh_toan | VARCHAR(20) | - | Hình thức thanh toán |
| dieu_khoan | TEXT | - | Điều khoản hợp đồng |
| trang_thai | VARCHAR(20) | NOT NULL | HIEU_LUC / HET_HAN / CHAM_DUT / GIA_HAN |
| ly_do_cham_dut | TEXT | - | Lý do chấm dứt |
| ngay_cham_dut | DATE | - | Ngày chấm dứt |
| ngay_tao | DATETIME | NOT NULL | Ngày tạo |
| ngay_cap_nhat | DATETIME | - | Ngày cập nhật |

**Khóa ngoại:**
- `ma_khach_hang` → `khach_hang.ma_khach_hang` (ON DELETE CASCADE)
- `ma_vi_tri` → `vi_tri.ma_vi_tri` (ON DELETE CASCADE)

---

### 3.6 `hang_hoa` - Hàng Hóa

| Trường | Kiểu | Ràng buộc | Mô tả |
|--------|------|-----------|-------|
| ma_hang_hoa | VARCHAR(30) | **PK**, NOT NULL | Mã hàng hóa |
| ma_hop_dong | VARCHAR(20) | **FK**, NOT NULL | Mã hợp đồng |
| ten_hang | VARCHAR(200) | NOT NULL | Tên hàng |
| loai_hang | VARCHAR(100) | NOT NULL | Loại hàng |
| so_luong | INTEGER | NOT NULL, DEFAULT 0 | Số lượng |
| don_vi | VARCHAR(20) | NOT NULL | Đơn vị tính |
| trong_luong | FLOAT | - | Trọng lượng (kg) |
| kich_thuoc | VARCHAR(50) | - | Kích thước |
| gia_tri | FLOAT | - | Giá trị |
| ngay_nhap | DATETIME | NOT NULL | Ngày nhập kho |
| ngay_xuat | DATETIME | - | Ngày xuất kho |
| trang_thai | VARCHAR(20) | NOT NULL | Trong kho / Da xuat |
| vi_tri_luu_tru | VARCHAR(30) | - | Vị trí lưu trữ |
| ghi_chu | TEXT | - | Ghi chú |
| hinh_anh | TEXT | - | JSON array của đường dẫn ảnh |
| ngay_tao | DATETIME | NOT NULL | Ngày tạo |
| ngay_cap_nhat | DATETIME | - | Ngày cập nhật |

**Khóa ngoại:**
- `ma_hop_dong` → `hop_dong.ma_hop_dong` (ON DELETE CASCADE)

---

### 3.7 `thanh_toan` - Thanh Toán

| Trường | Kiểu | Ràng buộc | Mô tả |
|--------|------|-----------|-------|
| ma_thanh_toan | VARCHAR(30) | **PK**, NOT NULL | Mã thanh toán |
| ma_hop_dong | VARCHAR(20) | **FK**, NOT NULL | Mã hợp đồng |
| loai_phi | VARCHAR(20) | NOT NULL | TIEN_COC / THUE_THANG / PHU_PHI / PHI_PHAT |
| so_tien | FLOAT | NOT NULL | Số tiền |
| ky_thanh_toan | VARCHAR(20) | - | Kỳ thanh toán |
| ngay_den_han | DATE | NOT NULL | Ngày đến hạn |
| ngay_thanh_toan | DATE | - | Ngày thanh toán thực tế |
| phuong_thuc | VARCHAR(20) | NOT NULL | Phương thức thanh toán |
| so_giao_dich | VARCHAR(50) | - | Số giao dịch ngân hàng |
| trang_thai | VARCHAR(20) | NOT NULL | DA_THANH_TOAN / CHUA_THANH_TOAN / QUA_HAN |
| phi_phat | FLOAT | NOT NULL, DEFAULT 0 | Phí phạt nếu quá hạn |
| nguoi_thu | VARCHAR(100) | - | Người thu tiền |
| ghi_chu | TEXT | - | Ghi chú |
| ngay_tao | DATETIME | NOT NULL | Ngày tạo |
| ngay_cap_nhat | DATETIME | - | Ngày cập nhật |

**Khóa ngoại:**
- `ma_hop_dong` → `hop_dong.ma_hop_dong` (ON DELETE CASCADE)

---

## 4. Mối Quan Hệ Chi Tiết

### 4.1 `kho` → `vi_tri` (1:N)

```
kho.ma_kho ──────► vi_tri.ma_kho
   (1)              (N)
```

| Ràng buộc | Giá trị |
|-----------|---------|
| Từ | kho.ma_kho |
| Đến | vi_tri.ma_kho |
| Loại | 1:N |
| ON DELETE | RESTRICT |

**Nghiệp vụ:** Một kho có nhiều vị trí lưu trữ. Không cho phép xóa kho nếu còn vị trí.

---

### 4.2 `khach_hang` → `hop_dong` (1:N)

```
khach_hang.ma_khach_hang ──────► hop_dong.ma_khach_hang
        (1)                            (N)
```

| Ràng buộc | Giá trị |
|-----------|---------|
| Từ | khach_hang.ma_khach_hang |
| Đến | hop_dong.ma_khach_hang |
| Loại | 1:N |
| ON DELETE | CASCADE |

**Nghiệp vụ:** Một khách hàng có thể thuê nhiều vị trí qua nhiều hợp đồng. Khi xóa khách hàng, xóa tất cả hợp đồng liên quan.

---

### 4.3 `vi_tri` → `hop_dong` (1:N)

```
vi_tri.ma_vi_tri ──────► hop_dong.ma_vi_tri
      (1)                    (N)
```

| Ràng buộc | Giá trị |
|-----------|---------|
| Từ | vi_tri.ma_vi_tri |
| Đến | hop_dong.ma_vi_tri |
| Loại | 1:N |
| ON DELETE | CASCADE |

**Nghiệp vụ:** Mỗi vị trí có thể được thuê bởi nhiều hợp đồng (theo thời gian khác nhau).

---

### 4.4 `hop_dong` → `hang_hoa` (1:N)

```
hop_dong.ma_hop_dong ──────► hang_hoa.ma_hop_dong
        (1)                        (N)
```

| Ràng buộc | Giá trị |
|-----------|---------|
| Từ | hop_dong.ma_hop_dong |
| Đến | hang_hoa.ma_hop_dong |
| Loại | 1:N |
| ON DELETE | CASCADE |

**Nghiệp vụ:** Mỗi hợp đồng có thể lưu trữ nhiều hàng hóa. Khi xóa hợp đồng, xóa tất cả hàng hóa liên quan.

---

### 4.5 `hop_dong` → `thanh_toan` (1:N)

```
hop_dong.ma_hop_dong ──────► thanh_toan.ma_hop_dong
        (1)                        (N)
```

| Ràng buộc | Giá trị |
|-----------|---------|
| Từ | hop_dong.ma_hop_dong |
| Đến | thanh_toan.ma_hop_dong |
| Loại | 1:N |
| ON DELETE | CASCADE |

**Nghiệp vụ:** Mỗi hợp đồng có nhiều lần thanh toán (tiền cọc, thuê tháng, phí phạt...). Khi xóa hợp đồng, xóa tất cả thanh toán liên quan.

---

## 5. Ràng Buộc Chung (Constraints)

### 5.1 NOT NULL Columns

| Bảng | Columns |
|------|---------|
| nhan_vien | ma_nhan_vien, ho_ten, email, vai_tro, tai_khoan, mat_khau |
| kho | ma_kho, ten_kho, dia_chi, dien_tich, suc_chua, da_su_dung |
| vi_tri | ma_vi_tri, ma_kho, khu_vuc, hang, tang, dien_tich, gia_thue |
| khach_hang | ma_khach_hang, ho_ten, loai_khach, so_dien_thoai, dia_chi, ngay_dang_ky |
| hop_dong | ma_hop_dong, ma_khach_hang, ma_vi_tri, ngay_bat_dau, ngay_ket_thuc, gia_thue |
| hang_hoa | ma_hang_hoa, ma_hop_dong, ten_hang, loai_hang, so_luong, don_vi, ngay_nhap |
| thanh_toan | ma_thanh_toan, ma_hop_dong, loai_phi, so_tien, ngay_den_han, phuong_thuc |

### 5.2 UNIQUE Columns

| Bảng | Columns |
|------|---------|
| nhan_vien | email, tai_khoan |
| khach_hang | email |

### 5.3 DEFAULT Values

| Bảng | Column | Default |
|------|--------|---------|
| kho | da_su_dung | 0 |
| vi_tri | tang | 1 |
| hop_dong | tien_coc | 0 |
| hang_hoa | so_luong | 0 |
| thanh_toan | phi_phat | 0 |

---

## 6. Luồng Nghiệp Vụ Qua ERD

### 6.1 Tạo Hợp Đồng Mới

```
1. INSERT khach_hang (nếu chưa có)
2. INSERT hop_dong (ma_khach_hang, ma_vi_tri, ngay_bat_dau, ngay_ket_thuc, ...)
3. UPDATE vi_tri SET trang_thai = 'da_thue' WHERE ma_vi_tri = ...
4. INSERT thanh_toan (loai_phi = 'tien_coc', ...)
```

### 6.2 Nhập Hàng Hóa

```
1. INSERT hang_hoa (ma_hop_dong, ten_hang, so_luong, ngay_nhap, ...)
2. UPDATE kho SET da_su_dung = da_su_dung + ? WHERE ma_kho = ...
```

### 6.3 Thanh Toán Định Kỳ

```
1. INSERT thanh_toan (ma_hop_dong, loai_phi = 'thue_thang', ngay_den_han, ...)
2. Kiểm tra ngay_thanh_toan:
   - Nếu đúng hạn: trang_thai = 'da_thanh_toan'
   - Nếu quá hạn: trang_thai = 'qua_han', phi_phat = ?
```

### 6.4 Kết Thúc Hợp Đồng

```
1. UPDATE hop_dong SET trang_thai = 'het_han', ngay_cham_dut = ... WHERE ma_hop_dong = ...
2. UPDATE vi_tri SET trang_thai = 'trong' WHERE ma_vi_tri = ...
3. UPDATE kho SET da_su_dung = da_su_dung - ? WHERE ma_kho = ...
```

---

## 7. So Sánh ERD vs Class Diagram

| Khía cạnh | ERD | Class Diagram |
|-----------|-----|---------------|
| Mục đích | Thiết kế database | Thiết kế OOP |
| Thể hiện | Bảng, cột, kiểu SQL | Class, attributes, methods |
| Quan hệ | 1:1, 1:N, M:N | Association, Inheritance, Composition |
| Focus | Dữ liệu lưu trữ | Logic và hành vi |
| Models tương ứng | Database tables | BaseModel subclasses |

**Ví dụ mapping:**
- `kho` table ↔ `Kho` model
- `vi_tri.ma_kho` FK ↔ `ViTri.kho` relationship
- `BaseModel.ngay_tao` ↔ implicit in all tables

---

## 8. Tệp Tin Liên Quan

| Tệp | Mô tả |
|-----|-------|
| `src/models/base.py` | BaseModel định nghĩa ngay_tao, ngay_cap_nhat |
| `src/models/enums.py` | Enum definitions |
| `src/models/kho.py` | Kho model ↔ kho table |
| `src/models/vi_tri.py` | ViTri model ↔ vi_tri table |
| `src/models/khach_hang.py` | KhachHang model ↔ khach_hang table |
| `src/models/hop_dong.py` | HopDong model ↔ hop_dong table |
| `src/models/hang_hoa.py` | HangHoa model ↔ hang_hoa table |
| `src/models/thanh_toan.py` | ThanhToan model ↔ thanh_toan table |
| `src/models/nhan_vien.py` | NhanVien model ↔ nhan_vien table |
| `docs/class-diagram-warehouse.md` | Class diagram documentation |

---

## 9. Mở Rộng Sơ Đồ

Để chỉnh sửa ERD:
1. Mở file `docs/erd-warehouse.drawio.xml` bằng [app.diagrams.net](https://app.diagrams.net)
2. Hoặc sử dụng VS Code extension **Draw.io Integration**
3. Export sang PNG/PDF khi cần chia sẻ

---

*Cập nhật: 2026-05-10*
