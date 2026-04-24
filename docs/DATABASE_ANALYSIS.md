# PHÂN TÍCH THIẾT KẾ CƠ SỞ DỮ LIỆU
## Hệ thống Quản lý Dịch vụ Cho thuê Kho Lưu trữ Hàng Hóa

**Phiên bản:** 1.0  
**Ngày cập nhật:** 23/04/2026  
**Nhóm 12 - Lập trình Python**

---

## 1. TỔNG QUAN THIẾT KẾ

### 1.1 Triết lý thiết kế

- **Chuẩn hóa:** Database được chuẩn hóa đến dạng chuẩn 3 (3NF) để tránh dư thừa dữ liệu
- **Toàn vẹn dữ liệu:** Sử dụng foreign keys, constraints để đảm bảo tính nhất quán
- **Hiệu năng:** Indexes cho các trường tìm kiếm thường xuyên
- **Mở rộng:** Thiết kế module, dễ thêm tính năng mới
- **Backup & Recovery:** Hỗ trợ backup SQLite đơn giản

### 1.2 Công nghệ

| Thành phần | Lựa chọn | Lý do |
|------------|----------|-------|
| DBMS | SQLite 3 | Nhẹ, không cần server, phù hợp ứng dụng desktop |
| ORM | SQLAlchemy 2.0+ | Pythonic, hỗ trợ async, migration dễ dàng |
| Migration | Alembic | Quản lý version schema, rollback an toàn |

---

## 2. SƠ ĐỒ ER (ENTITY-RELATIONSHIP)

```
┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
│   KhachHang     │       │    HopDong      │       │    ViTri        │
├─────────────────┤       ├─────────────────┤       ├─────────────────┤
│ PK ma_khach_hang│◄──────│ FK ma_khach_hang│       │ PK ma_vi_tri    │
│    ho_ten       │   1   │ PK ma_hop_dong  │   1   │ FK ma_kho       │
│    loai_khach   │   *   │ FK ma_vi_tri    │──────►│    khu_vuc      │
│    so_dien_thoai│       │    ngay_bat_dau │       │    hang         │
│    email        │       │    ngay_ket_thuc│       │    tang         │
│    dia_chi      │       │    gia_thue     │       │    dien_tich    │
│    ma_so_thue   │       │    tien_coc     │       │    gia_thue     │
│    ngay_dang_ky │       │    dieu_khoan   │       │    trang_thai   │
│    trang_thai   │       │    trang_thai   │       └─────────────────┘
└─────────────────┘       └────────┬────────┘
         │                        │
         │ 1                      │ 1
         │ *                      │ *
         ▼                        ▼
┌─────────────────┐       ┌─────────────────┐
│   ThanhToan     │       │   HangHoa       │
├─────────────────┤       ├─────────────────┤
│ PK ma_thanh_toan│       │ PK ma_hang_hoa  │
│ FK ma_hop_dong  │       │ FK ma_hop_dong  │
│    loai_phi     │       │    ten_hang     │
│    so_tien      │       │    loai_hang    │
│    ngay_thanh_toan│     │    so_luong     │
│    phuong_thuc  │       │    don_vi       │
│    trang_thai   │       │    trong_luong  │
│    ghi_chu      │       │    kich_thuoc   │
└─────────────────┘       │    ngay_nhap    │
                          │    ngay_xuat    │
                          │    trang_thai   │
                          │    ghi_chu      │
                          └─────────────────┘

┌─────────────────┐       ┌─────────────────┐
│      Kho        │       │  NhanVien       │
├─────────────────┤       ├─────────────────┤
│ PK ma_kho       │       │ PK ma_nhan_vien │
│    ten_kho      │       │    ho_ten       │
│    dia_chi      │       │    email        │
│    dien_tich    │       │    so_dien_thoai│
│    suc_chua     │       │    vai_tro      │
│    da_su_dung   │       │    tai_khoan    │
│    trang_thai   │       │    mat_khau     │
│    ngay_tao     │       │    trang_thai   │
└─────────────────┘       │    ngay_tao     │
                          └─────────────────┘

┌─────────────────┐       ┌─────────────────┐
│   BaoCao        │       │   SystemLog     │
├─────────────────┤       ├─────────────────┤
│ PK ma_bao_cao   │       │ PK ma_log       │
│    loai_bao_cao │       │    thoi_gian    │
│    ngay_tao     │       │    nguoi_thuc_hien│
│    nguoi_tao    │       │    hanh_dong    │
│    du_lieu      │       │    ban_ghi      │
│    trang_thai   │       │    gia_tri_cu   │
│    file_path    │       │    gia_tri_moi  │
└─────────────────┘       └─────────────────┘
```

---

## 3. CHI TIẾT CÁC BẢNG

### 3.1 Bảng `khach_hang` (Customers)

Lưu trữ thông tin khách hàng đăng ký thuê kho.

| Cột | Kiểu dữ liệu | Ràng buộc | Mô tả |
|-----|-------------|-----------|-------|
| `ma_khach_hang` | VARCHAR(20) | PK, NOT NULL | Mã khách hàng duy nhất (KH001, KH002...) |
| `ho_ten` | VARCHAR(200) | NOT NULL | Họ tên cá nhân hoặc tên công ty |
| `loai_khach` | ENUM | NOT NULL, DEFAULT 'ca_nhan' | 'ca_nhan' hoặc 'doanh_nghiep' |
| `so_dien_thoai` | VARCHAR(20) | NOT NULL | Số điện thoại liên hệ |
| `email` | VARCHAR(100) | UNIQUE | Email liên hệ |
| `dia_chi` | TEXT | NOT NULL | Địa chỉ liên hệ |
| `ma_so_thue` | VARCHAR(20) | NULL | Mã số thuế (nếu là doanh nghiệp) |
| `ngay_dang_ky` | DATE | NOT NULL, DEFAULT CURRENT_DATE | Ngày đăng ký |
| `trang_thai` | ENUM | NOT NULL, DEFAULT 'hoat_dong' | 'hoat_dong', 'tam_khoa', 'da_xoa' |
| `ngay_tao` | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Thời điểm tạo bản ghi |
| `ngay_cap_nhat` | DATETIME | NULL | Thời điểm cập nhật cuối |

**Indexes:**
- `idx_khach_hang_so_dien_thoai` (so_dien_thoai)
- `idx_khach_hang_email` (email)
- `idx_khach_hang_trang_thai` (trang_thai)
- `idx_khach_hang_ho_ten` (ho_ten) - fulltext search

**Sample data:**
```sql
INSERT INTO khach_hang VALUES (
  'KH001', 'Nguyễn Văn A', 'ca_nhan', '0901234567', 
  'nguyenvana@email.com', '123 Đường ABC, Quận 1, TP.HCM', 
  NULL, '2026-04-01', 'hoat_dong', CURRENT_TIMESTAMP, NULL
);
```

---

### 3.2 Bảng `kho` (Warehouses)

Lưu trữ thông tin các kho hàng.

| Cột | Kiểu dữ liệu | Ràng buộc | Mô tả |
|-----|-------------|-----------|-------|
| `ma_kho` | VARCHAR(20) | PK, NOT NULL | Mã kho duy nhất (KHO001, KHO002...) |
| `ten_kho` | VARCHAR(200) | NOT NULL | Tên kho |
| `dia_chi` | TEXT | NOT NULL | Địa chỉ kho |
| `dien_tich` | DECIMAL(12,2) | NOT NULL | Tổng diện tích (m²) |
| `suc_chua` | DECIMAL(12,2) | NOT NULL | Sức chứa tối đa (m³ hoặc kg) |
| `da_su_dung` | DECIMAL(12,2) | NOT NULL, DEFAULT 0 | Diện tích/volume đã sử dụng |
| `trang_thai` | ENUM | NOT NULL, DEFAULT 'hoat_dong' | 'hoat_dong', 'bao_tri', 'ngung' |
| `ngay_tao` | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Thời điểm tạo |
| `ngay_cap_nhat` | DATETIME | NULL | Thời điểm cập nhật cuối |

**Indexes:**
- `idx_kho_ten_kho` (ten_kho)
- `idx_kho_trang_thai` (trang_thai)

**Computed field:**
- `ty_le_lap_day` = (da_su_dung / suc_chua) * 100

---

### 3.3 Bảng `vi_tri` (Storage Locations)

Lưu trữ chi tiết các vị trí lưu trữ trong kho.

| Cột | Kiểu dữ liệu | Ràng buộc | Mô tả |
|-----|-------------|-----------|-------|
| `ma_vi_tri` | VARCHAR(30) | PK, NOT NULL | Mã vị trí (vd: K01-A-01-01) |
| `ma_kho` | VARCHAR(20) | FK → kho.ma_kho, NOT NULL | Kho chứa |
| `khu_vuc` | VARCHAR(50) | NOT NULL | Khu vực trong kho (A, B, C...) |
| `hang` | VARCHAR(10) | NOT NULL | Hàng/Zone |
| `tang` | INTEGER | NOT NULL, DEFAULT 1 | Tầng |
| `dien_tich` | DECIMAL(10,2) | NOT NULL | Diện tích vị trí (m²) |
| `gia_thue` | DECIMAL(12,2) | NOT NULL | Giá thuê/m²/tháng |
| `suc_chua` | DECIMAL(10,2) | NULL | Sức chứa vị trí (m³/kg) |
| `trang_thai` | ENUM | NOT NULL, DEFAULT 'trong' | 'trong', 'da_thue', 'bao_tri' |
| `ngay_tao` | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Thời điểm tạo |
| `ngay_cap_nhat` | DATETIME | NULL | Thời điểm cập nhật cuối |

**Indexes:**
- `idx_vi_tri_ma_kho` (ma_kho)
- `idx_vi_tri_trang_thai` (trang_thai)
- `idx_vi_tri_khu_vuc` (khu_vuc, hang, tang)

**Foreign Keys:**
- `FK_vi_tri_kho`: FOREIGN KEY (ma_kho) REFERENCES kho(ma_kho) ON DELETE RESTRICT

**Sample data:**
```sql
INSERT INTO vi_tri VALUES (
  'K01-A-01-01', 'KHO001', 'A', '01', 1, 50.00, 150000, 100, 
  'trong', CURRENT_TIMESTAMP, NULL
);
```

---

### 3.4 Bảng `hop_dong` (Contracts)

Lưu trữ thông tin hợp đồng thuê kho.

| Cột | Kiểu dữ liệu | Ràng buộc | Mô tả |
|-----|-------------|-----------|-------|
| `ma_hop_dong` | VARCHAR(20) | PK, NOT NULL | Mã hợp đồng (HD20260401001) |
| `ma_khach_hang` | VARCHAR(20) | FK → khach_hang.ma_khach_hang, NOT NULL | Khách hàng thuê |
| `ma_vi_tri` | VARCHAR(30) | FK → vi_tri.ma_vi_tri, NOT NULL | Vị trí thuê |
| `ngay_bat_dau` | DATE | NOT NULL | Ngày bắt đầu thuê |
| `ngay_ket_thuc` | DATE | NOT NULL | Ngày kết thúc |
| `gia_thue` | DECIMAL(12,2) | NOT NULL | Giá thuê thỏa thuận (VNĐ/tháng) |
| `tien_coc` | DECIMAL(12,2) | NOT NULL, DEFAULT 0 | Tiền đặt cọc |
| `phuong_thuc_thanh_toan` | ENUM | DEFAULT 'hang_thang' | 'hang_thang', 'hang_quy', 'nam' |
| `dieu_khoan` | TEXT | NULL | Các điều khoản đặc biệt |
| `trang_thai` | ENUM | NOT NULL, DEFAULT 'hieu_luc' | 'hieu_luc', 'het_han', 'cham_dut', 'gia_han' |
| `ly_do_cham_dut` | TEXT | NULL | Lý do chấm dứt (nếu có) |
| `ngay_cham_dut` | DATE | NULL | Ngày chấm dứt thực tế |
| `ngay_tao` | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Thời điểm tạo |
| `ngay_cap_nhat` | DATETIME | NULL | Thời điểm cập nhật cuối |

**Indexes:**
- `idx_hop_dong_ma_khach_hang` (ma_khach_hang)
- `idx_hop_dong_ma_vi_tri` (ma_vi_tri)
- `idx_hop_dong_ngay_ket_thuc` (ngay_ket_thuc) - cho cảnh báo hết hạn
- `idx_hop_dong_trang_thai` (trang_thai)

**Foreign Keys:**
- `FK_hop_dong_khach_hang`: FOREIGN KEY (ma_khach_hang) REFERENCES khach_hang(ma_khach_hang)
- `FK_hop_dong_vi_tri`: FOREIGN KEY (ma_vi_tri) REFERENCES vi_tri(ma_vi_tri)

**Sample data:**
```sql
INSERT INTO hop_dong VALUES (
  'HD20260401001', 'KH001', 'K01-A-01-01', '2026-04-01', '2027-04-01',
  7500000, 15000000, 'hang_thang', 'Miễn phí 1 tháng đầu', 
  'hieu_luc', NULL, NULL, CURRENT_TIMESTAMP, NULL
);
```

---

### 3.5 Bảng `hang_hoa` (Goods/Inventory)

Lưu trữ thông tin hàng hóa trong kho.

| Cột | Kiểu dữ liệu | Ràng buộc | Mô tả |
|-----|-------------|-----------|-------|
| `ma_hang_hoa` | VARCHAR(30) | PK, NOT NULL | Mã hàng hóa (HH20260401001) |
| `ma_hop_dong` | VARCHAR(20) | FK → hop_dong.ma_hop_dong, NOT NULL | Hợp đồng chứa hàng |
| `ten_hang` | VARCHAR(200) | NOT NULL | Tên hàng hóa |
| `loai_hang` | VARCHAR(100) | NOT NULL | Loại hàng (thực phẩm, điện tử, v.v.) |
| `so_luong` | INTEGER | NOT NULL, DEFAULT 0 | Số lượng |
| `don_vi` | VARCHAR(20) | NOT NULL | Đơn vị tính (cái, thùng, kg, v.v.) |
| `trong_luong` | DECIMAL(10,2) | NULL | Trọng lượng (kg) |
| `kich_thuoc` | VARCHAR(50) | NULL | Kích thước (DxRxC cm) |
| `gia_tri` | DECIMAL(12,2) | NULL | Giá trị hàng hóa (VNĐ) |
| `ngay_nhap` | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Thời điểm nhập kho |
| `ngay_xuat` | DATETIME | NULL | Thời điểm xuất kho |
| `trang_thai` | ENUM | NOT NULL, DEFAULT 'trong_kho' | 'trong_kho', 'da_xuat', 'hu_hong' |
| `vi_tri_luu_tru` | VARCHAR(30) | NULL | Vị trí cụ thể trong kho |
| `ghi_chu` | TEXT | NULL | Ghi chú đặc biệt (hàng dễ vỡ, hạn sử dụng, v.v.) |
| `hinh_anh` | TEXT | NULL | Path/file name hình ảnh (JSON array) |
| `ngay_tao` | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Thời điểm tạo |
| `ngay_cap_nhat` | DATETIME | NULL | Thời điểm cập nhật cuối |

**Indexes:**
- `idx_hang_hoa_ma_hop_dong` (ma_hop_dong)
- `idx_hang_hoa_ten_hang` (ten_hang)
- `idx_hang_hoa_trang_thai` (trang_thai)
- `idx_hang_hoa_ngay_nhap` (ngay_nhap)

**Foreign Keys:**
- `FK_hang_hoa_hop_dong`: FOREIGN KEY (ma_hop_dong) REFERENCES hop_dong(ma_hop_dong) ON DELETE CASCADE

---

### 3.6 Bảng `thanh_toan` (Payments)

Lưu trữ thông tin thanh toán và hóa đơn.

| Cột | Kiểu dữ liệu | Ràng buộc | Mô tả |
|-----|-------------|-----------|-------|
| `ma_thanh_toan` | VARCHAR(30) | PK, NOT NULL | Mã thanh toán (TT20260401001) |
| `ma_hop_dong` | VARCHAR(20) | FK → hop_dong.ma_hop_dong, NOT NULL | Hợp đồng thanh toán |
| `loai_phi` | ENUM | NOT NULL | 'tien_coc', 'thue_thang', 'phu_phi', 'phi_phat' |
| `so_tien` | DECIMAL(12,2) | NOT NULL | Số tiền (VNĐ) |
| `ky_thanh_toan` | VARCHAR(20) | NULL | Kỳ thanh toán (04/2026, Q2/2026) |
| `ngay_den_han` | DATE | NOT NULL | Ngày đến hạn thanh toán |
| `ngay_thanh_toan` | DATE | NULL | Ngày thanh toán thực tế |
| `phuong_thuc` | ENUM | NOT NULL | 'tien_mat', 'chuyen_khoan', 'the' |
| `so_giao_dich` | VARCHAR(50) | NULL | Số giao dịch/ngân hàng |
| `trang_thai` | ENUM | NOT NULL, DEFAULT 'chua_thanh_toan' | 'da_thanh_toan', 'chua_thanh_toan', 'qua_han' |
| `phi_phat` | DECIMAL(12,2) | NOT NULL, DEFAULT 0 | Phí phạt trễ hạn |
| `ghi_chu` | TEXT | NULL | Ghi chú |
| `nguoi_thu` | VARCHAR(100) | NULL | Người thu (nhân viên) |
| `ngay_tao` | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Thời điểm tạo |
| `ngay_cap_nhat` | DATETIME | NULL | Thời điểm cập nhật cuối |

**Indexes:**
- `idx_thanh_toan_ma_hop_dong` (ma_hop_dong)
- `idx_thanh_toan_ngay_den_han` (ngay_den_han) - cho cảnh báo quá hạn
- `idx_thanh_toan_trang_thai` (trang_thai)

**Foreign Keys:**
- `FK_thanh_toan_hop_dong`: FOREIGN KEY (ma_hop_dong) REFERENCES hop_dong(ma_hop_dong)

---

### 3.7 Bảng `nhan_vien` (Employees/Users)

Lưu trữ thông tin nhân viên và tài khoản đăng nhập.

| Cột | Kiểu dữ liệu | Ràng buộc | Mô tả |
|-----|-------------|-----------|-------|
| `ma_nhan_vien` | VARCHAR(20) | PK, NOT NULL | Mã nhân viên (NV001, NV002...) |
| `ho_ten` | VARCHAR(200) | NOT NULL | Họ tên nhân viên |
| `email` | VARCHAR(100) | UNIQUE, NOT NULL | Email đăng nhập |
| `so_dien_thoai` | VARCHAR(20) | NULL | Số điện thoại |
| `vai_tro` | ENUM | NOT NULL | 'quan_tri', 'kinh_doanh', 'kho', 'ke_toan' |
| `tai_khoan` | VARCHAR(50) | UNIQUE, NOT NULL | Tên đăng nhập |
| `mat_khau` | VARCHAR(255) | NOT NULL | Mật khẩu (bcrypt hash) |
| `trang_thai` | ENUM | NOT NULL, DEFAULT 'hoat_dong' | 'hoat_dong', 'khoa' |
| `ngay_tao` | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Thời điểm tạo |
| `ngay_cap_nhat` | DATETIME | NULL | Thời điểm cập nhật cuối |
| `lan_dang_nhap_cuoi` | DATETIME | NULL | Lần đăng nhập cuối |

**Indexes:**
- `idx_nhan_vien_tai_khoan` (tai_khoan)
- `idx_nhan_vien_email` (email)
- `idx_nhan_vien_vai_tro` (vai_tro)

**Permissions by role:**
| Vai trò | Quyền hạn |
|---------|-----------|
| `quan_tri` | Toàn bộ hệ thống, quản lý nhân viên |
| `kinh_doanh` | Quản lý khách hàng, hợp đồng, xem báo cáo |
| `kho` | Quản lý nhập/xuất hàng, kiểm kê |
| `ke_toan` | Quản lý thanh toán, báo cáo tài chính |

---

### 3.8 bảng `system_log` (Audit Log)

Ghi log các thao tác quan trọng trong hệ thống.

| Cột | Kiểu dữ liệu | Ràng buộc | Mô tả |
|-----|-------------|-----------|-------|
| `ma_log` | INTEGER | PK, AUTOINCREMENT | ID tự tăng |
| `thoi_gian` | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Thời điểm thực hiện |
| `ma_nhan_vien` | VARCHAR(20) | FK → nhan_vien.ma_nhan_vien | Người thực hiện |
| `hanh_dong` | ENUM | NOT NULL | 'THEM', 'SUA', 'XOA', 'DANG_NHAP', 'DANG_XUAT' |
| `ban_ghi` | VARCHAR(100) | NOT NULL | Tên bảng/bản ghi (khach_hang:KH001) |
| `gia_tri_cu` | TEXT | NULL | Dữ liệu cũ (JSON) |
| `gia_tri_moi` | TEXT | NULL | Dữ liệu mới (JSON) |
| `ip_address` | VARCHAR(45) | NULL | Địa chỉ IP |
| `ghi_chu` | TEXT | NULL | Ghi chú thêm |

**Indexes:**
- `idx_system_log_thoi_gian` (thoi_gian)
- `idx_system_log_ma_nhan_vien` (ma_nhan_vien)
- `idx_system_log_hanh_dong` (hanh_dong)
- `idx_system_log_ban_ghi` (ban_ghi)

---

### 3.9 Bảng `bao_cao` (Reports)

Lưu trữ thông tin các báo cáo đã tạo.

| Cột | Kiểu dữ liệu | Ràng buộc | Mô tả |
|-----|-------------|-----------|-------|
| `ma_bao_cao` | VARCHAR(30) | PK, NOT NULL | Mã báo cáo (BC20260401001) |
| `loai_bao_cao` | ENUM | NOT NULL | 'doanh_thu', 'lap_day', 'cong_no', 'ton_kho' |
| `ngay_bat_dau` | DATE | NOT NULL | Ngày bắt đầu kỳ báo cáo |
| `ngay_ket_thuc` | DATE | NOT NULL | Ngày kết thúc kỳ báo cáo |
| `ngay_tao` | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Thời điểm tạo |
| `nguoi_tao` | VARCHAR(20) | FK → nhan_vien.ma_nhan_vien | Người tạo báo cáo |
| `du_lieu` | TEXT | NULL | Dữ liệu báo cáo (JSON) |
| `file_path` | VARCHAR(500) | NULL | Đường dẫn file xuất (PDF/Excel) |
| `trang_thai` | ENUM | NOT NULL, DEFAULT 'hoan_thanh' | 'dang_tao', 'hoan_thanh', 'that_bai' |
| `ghi_chu` | TEXT | NULL | Ghi chú |

**Indexes:**
- `idx_bao_cao_loai_bao_cao` (loai_bao_cao)
- `idx_bao_cao_ngay_tao` (ngay_tao)

---

## 4. CÁC QUAN HỆ (RELATIONSHIPS)

### 4.1 Quan hệ 1-N (One-to-Many)

| Cha | Con | Foreign Key | ON DELETE | ON UPDATE |
|-----|-----|-------------|-----------|-----------|
| khach_hang | hop_dong | ma_khach_hang | RESTRICT | CASCADE |
| kho | vi_tri | ma_kho | RESTRICT | CASCADE |
| vi_tri | hop_dong | ma_vi_tri | RESTRICT | CASCADE |
| hop_dong | hang_hoa | ma_hop_dong | CASCADE | CASCADE |
| hop_dong | thanh_toan | ma_hop_dong | RESTRICT | CASCADE |
| nhan_vien | system_log | ma_nhan_vien | SET NULL | CASCADE |
| nhan_vien | bao_cao | nguoi_tao | SET NULL | CASCADE |

### 4.2 Business Rules cho Relationships

1. **Khách hàng → Hợp đồng:**
   - Không được xóa khách hàng nếu còn hợp đồng đang hiệu lực
   - Một khách hàng có thể có nhiều hợp đồng (lưu trữ nhiều vị trí)

2. **Kho → Vị trí:**
   - Không được xóa kho nếu còn vị trí trong đó
   - Khi xóa kho, phải xóa/vô hiệu hóa tất cả vị trí trước

3. **Vị trí → Hợp đồng:**
   - Một vị trí chỉ có 1 hợp đồng hiệu lực tại một thời điểm
   - Khi hợp đồng chấm dứt, vị trí trở lại trạng thái 'trong'

4. **Hợp đồng → Hàng hóa:**
   - Khi xóa hợp đồng, tất cả hàng hóa thuộc hợp đồng đó bị xóa (CASCADE)
   - Hàng hóa phải thuộc về một hợp đồng đang hiệu lực

5. **Hợp đồng → Thanh toán:**
   - Không được xóa hợp đồng nếu còn thanh toán chưa hoàn tất
   - Lịch sử thanh toán phải được giữ lại để đối chiếu

---

## 5. INDEXES & PERFORMANCE

### 5.1 Indexes cho tìm kiếm thường xuyên

```sql
-- Customers
CREATE INDEX idx_khach_hang_so_dien_thoai ON khach_hang(so_dien_thoai);
CREATE INDEX idx_khach_hang_email ON khach_hang(email);
CREATE INDEX idx_khach_hang_trang_thai ON khach_hang(trang_thai);

-- Contracts
CREATE INDEX idx_hop_dong_ma_khach_hang ON hop_dong(ma_khach_hang);
CREATE INDEX idx_hop_dong_ma_vi_tri ON hop_dong(ma_vi_tri);
CREATE INDEX idx_hop_dong_ngay_ket_thuc ON hop_dong(ngay_ket_thuc);
CREATE INDEX idx_hop_dong_trang_thai ON hop_dong(trang_thai);

-- Payments
CREATE INDEX idx_thanh_toan_ma_hop_dong ON thanh_toan(ma_hop_dong);
CREATE INDEX idx_thanh_toan_ngay_den_han ON thanh_toan(ngay_den_han);
CREATE INDEX idx_thanh_toan_trang_thai ON thanh_toan(trang_thai);

-- Goods
CREATE INDEX idx_hang_hoa_ma_hop_dong ON hang_hoa(ma_hop_dong);
CREATE INDEX idx_hang_hoa_trang_thai ON hang_hoa(trang_thai);
CREATE INDEX idx_hang_hoa_ngay_nhap ON hang_hoa(ngay_nhap);

-- Logs
CREATE INDEX idx_system_log_thoi_gian ON system_log(thoi_gian);
CREATE INDEX idx_system_log_hanh_dong ON system_log(hanh_dong);
```

### 5.2 Composite Indexes cho queries phức tạp

```sql
-- Tìm hợp đồng theo khách hàng và trạng thái
CREATE INDEX idx_hop_dong_kh_trang_thai ON hop_dong(ma_khach_hang, trang_thai);

-- Tìm thanh toán theo hợp đồng và trạng thái
CREATE INDEX idx_thanh_toan_hd_trang_thai ON thanh_toan(ma_hop_dong, trang_thai);

-- Tìm hàng hóa theo hợp đồng và trạng thái
CREATE INDEX idx_hang_hoa_hd_trang_thai ON hang_hoa(ma_hop_dong, trang_thai);

-- Tìm vị trí theo kho và trạng thái
CREATE INDEX idx_vi_tri_kho_trang_thai ON vi_tri(ma_kho, trang_thai);
```

---

## 6. CÁC VIEW HỮU ÍCH

### 6.1 View: Hợp đồng sắp hết hạn (30 ngày)

```sql
CREATE VIEW v_hop_dong_sap_het_han AS
SELECT 
    hd.ma_hop_dong,
    hd.ma_khach_hang,
    kh.ho_ten AS ten_khach_hang,
    hd.ma_vi_tri,
    hd.ngay_bat_dau,
    hd.ngay_ket_thuc,
    hd.gia_thue,
    hd.trang_thai,
    julianday(hd.ngay_ket_thuc) - julianday('now') AS so_ngay_con_lai
FROM hop_dong hd
JOIN khach_hang kh ON hd.ma_khach_hang = kh.ma_khach_hang
WHERE hd.trang_thai = 'hieu_luc'
  AND hd.ngay_ket_thuc <= date('now', '+30 days')
  AND hd.ngay_ket_thuc >= date('now')
ORDER BY hd.ngay_ket_thuc ASC;
```

### 6.2 View: Công nợ chưa thanh toán

```sql
CREATE VIEW v_cong_no_chua_thanh_toan AS
SELECT 
    tt.ma_thanh_toan,
    tt.ma_hop_dong,
    hd.ma_khach_hang,
    kh.ho_ten AS ten_khach_hang,
    tt.loai_phi,
    tt.so_tien,
    tt.phi_phat,
    tt.so_tien + tt.phi_phat AS tong_cong,
    tt.ngay_den_han,
    julianday('now') - julianday(tt.ngay_den_han) AS so_ngay_qua_han,
    tt.trang_thai
FROM thanh_toan tt
JOIN hop_dong hd ON tt.ma_hop_dong = hd.ma_hop_dong
JOIN khach_hang kh ON hd.ma_khach_hang = kh.ma_khach_hang
WHERE tt.trang_thai IN ('chua_thanh_toan', 'qua_han')
ORDER BY tt.ngay_den_han ASC;
```

### 6.3 View: Tỷ lệ lấp đầy kho

```sql
CREATE VIEW v_ty_le_lap_day_kho AS
SELECT 
    k.ma_kho,
    k.ten_kho,
    k.dien_tich,
    k.suc_chua,
    SUM(v.dien_tich) AS da_su_dung,
    ROUND((SUM(v.dien_tich) * 100.0 / k.suc_chua), 2) AS ty_le_lap_day_phan_tram
FROM kho k
LEFT JOIN vi_tri v ON k.ma_kho = v.ma_kho AND v.trang_thai = 'da_thue'
WHERE k.trang_thai = 'hoat_dong'
GROUP BY k.ma_kho, k.ten_kho, k.dien_tich, k.suc_chua;
```

### 6.4 View: Doanh thu theo tháng

```sql
CREATE VIEW v_doanh_thu_theo_thang AS
SELECT 
    strftime('%Y-%m', ngay_thanh_toan) AS thang,
    loai_phi,
    COUNT(*) AS so_giao_dich,
    SUM(so_tien) AS tong_tien,
    SUM(phi_phat) AS tong_phi_phat,
    SUM(so_tien + phi_phat) AS tong_doanh_thu
FROM thanh_toan
WHERE trang_thai = 'da_thanh_toan'
GROUP BY strftime('%Y-%m', ngay_thanh_toan), loai_phi
ORDER BY thang DESC;
```

### 6.5 View: Lịch sử khách hàng

```sql
CREATE VIEW v_lich_su_khach_hang AS
SELECT 
    kh.ma_khach_hang,
    kh.ho_ten,
    kh.so_dien_thoai,
    COUNT(DISTINCT hd.ma_hop_dong) AS tong_hop_dong,
    COUNT(DISTINCT CASE WHEN hd.trang_thai = 'hieu_luc' THEN hd.ma_hop_dong END) AS hop_dong_dang_hieu_luc,
    SUM(CASE WHEN tt.trang_thai = 'da_thanh_toan' THEN tt.so_tien ELSE 0 END) AS tong_da_thanh_toan,
    SUM(CASE WHEN tt.trang_thai IN ('chua_thanh_toan', 'qua_han') THEN tt.so_tien ELSE 0 END) AS tong_cong_no
FROM khach_hang kh
LEFT JOIN hop_dong hd ON kh.ma_khach_hang = hd.ma_khach_hang
LEFT JOIN thanh_toan tt ON hd.ma_hop_dong = tt.ma_hop_dong
WHERE kh.trang_thai = 'hoat_dong'
GROUP BY kh.ma_khach_hang, kh.ho_ten, kh.so_dien_thoai;
```

---

## 7. CÁC TRIGGER (TỰ ĐỘNG HÓA)

### 7.1 Trigger: Cập nhật trạng thái vị trí khi tạo hợp đồng

```sql
CREATE TRIGGER trg_cap_nhat_vi_tri_khi_tao_hop_dong
AFTER INSERT ON hop_dong
BEGIN
    UPDATE vi_tri 
    SET trang_thai = 'da_thue',
        ngay_cap_nhat = CURRENT_TIMESTAMP
    WHERE ma_vi_tri = NEW.ma_vi_tri;
    
    UPDATE kho 
    SET da_su_dung = da_su_dung + (
        SELECT dien_tich FROM vi_tri WHERE ma_vi_tri = NEW.ma_vi_tri
    ),
    ngay_cap_nhat = CURRENT_TIMESTAMP
    WHERE ma_kho = (
        SELECT ma_kho FROM vi_tri WHERE ma_vi_tri = NEW.ma_vi_tri
    );
END;
```

### 7.2 Trigger: Giải phóng vị trí khi hợp đồng chấm dứt

```sql
CREATE TRIGGER trg_giai_phong_vi_tri_khi_cham_dut
AFTER UPDATE OF trang_thai ON hop_dong
WHEN OLD.trang_thai IN ('hieu_luc', 'gia_han') 
  AND NEW.trang_thai IN ('het_han', 'cham_dut')
BEGIN
    UPDATE vi_tri 
    SET trang_thai = 'trong',
        ngay_cap_nhat = CURRENT_TIMESTAMP
    WHERE ma_vi_tri = NEW.ma_vi_tri;
    
    UPDATE kho 
    SET da_su_dung = da_su_dung - (
        SELECT dien_tich FROM vi_tri WHERE ma_vi_tri = NEW.ma_vi_tri
    ),
    ngay_cap_nhat = CURRENT_TIMESTAMP
    WHERE ma_kho = (
        SELECT ma_kho FROM vi_tri WHERE ma_vi_tri = NEW.ma_vi_tri
    );
END;
```

### 7.3 Trigger: Tự động đánh dấu thanh toán quá hạn

```sql
CREATE TRIGGER trg_danh_dau_qua_han
AFTER UPDATE OF trang_thai ON thanh_toan
WHEN NEW.ngay_den_han < date('now') 
  AND NEW.trang_thai = 'chua_thanh_toan'
BEGIN
    UPDATE thanh_toan 
    SET trang_thai = 'qua_han',
        phi_phat = phi_phat + (so_tien * 0.001 * (julianday('now') - julianday(ngay_den_han))),
        ngay_cap_nhat = CURRENT_TIMESTAMP
    WHERE ma_thanh_toan = NEW.ma_thanh_toan
      AND trang_thai = 'chua_thanh_toan';
END;
```

### 7.4 Trigger: Ghi log khi sửa/xóa dữ liệu quan trọng

```sql
CREATE TRIGGER trg_log_sua_khach_hang
AFTER UPDATE ON khach_hang
BEGIN
    INSERT INTO system_log (ma_nhan_vien, hanh_dong, ban_ghi, gia_tri_cu, gia_tri_moi, ghi_chu)
    VALUES (
        (SELECT tai_khoan FROM nhan_vien WHERE rowid = last_insert_rowid()),
        'SUA',
        'khach_hang:' || OLD.ma_khach_hang,
        json_object('ho_ten', OLD.ho_ten, 'so_dien_thoai', OLD.so_dien_thoai, 'email', OLD.email),
        json_object('ho_ten', NEW.ho_ten, 'so_dien_thoai', NEW.so_dien_thoai, 'email', NEW.email),
        'Cập nhật thông tin khách hàng'
    );
END;
```

---

## 8. SCRIPT KHỞI TẠO DATABASE

### 8.1 File: `src/data/database.py`

```python
"""
Khởi tạo và quản lý kết nối database
"""
from sqlalchemy import create_engine, Column, String, Integer, Float, Date, DateTime, Text, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import enum

Base = declarative_base()

# Enums
class LoaiKhachEnum(enum.Enum):
    CA_NHAN = 'ca_nhan'
    DOANH_NGHIEP = 'doanh_nghiep'

class TrangThaiKHEnum(enum.Enum):
    HOAT_DONG = 'hoat_dong'
    TAM_KHOA = 'tam_khoa'
    DA_XOA = 'da_xoa'

class TrangThaiKhoEnum(enum.Enum):
    HOAT_DONG = 'hoat_dong'
    BAO_TRI = 'bao_tri'
    NGUNG = 'ngung'

class TrangThaiViTriEnum(enum.Enum):
    TRONG = 'trong'
    DA_THUE = 'da_thue'
    BAO_TRI = 'bao_tri'

class TrangThaiHDEnum(enum.Enum):
    HIEU_LUC = 'hieu_luc'
    HET_HAN = 'het_han'
    CHAM_DUT = 'cham_dut'
    GIA_HAN = 'gia_han'

class LoaiPhiEnum(enum.Enum):
    TIEN_COC = 'tien_coc'
    THUE_THANG = 'thue_thang'
    PHU_PHI = 'phu_phi'
    PHI_PHAT = 'phi_phat'

class TrangThaiTTEnum(enum.Enum):
    DA_THANH_TOAN = 'da_thanh_toan'
    CHUA_THANH_TOAN = 'chua_thanh_toan'
    QUA_HAN = 'qua_han'

class VaiTroNVEuum(enum.Enum):
    QUAN_TRI = 'quan_tri'
    KINH_DOANH = 'kinh_doanh'
    KHO = 'kho'
    KE_TOAN = 'ke_toan'

class HanhDongLogEnum(enum.Enum):
    THEM = 'THEM'
    SUA = 'SUA'
    XOA = 'XOA'
    DANG_NHAP = 'DANG_NHAP'
    DANG_XUAT = 'DANG_XUAT'

# Models
class KhachHang(Base):
    __tablename__ = 'khach_hang'
    
    ma_khach_hang = Column(String(20), primary_key=True)
    ho_ten = Column(String(200), nullable=False)
    loai_khach = Column(Enum(LoaiKhachEnum), nullable=False, default=LoaiKhachEnum.CA_NHAN)
    so_dien_thoai = Column(String(20), nullable=False)
    email = Column(String(100), unique=True)
    dia_chi = Column(Text, nullable=False)
    ma_so_thue = Column(String(20))
    ngay_dang_ky = Column(Date, nullable=False, default=datetime.now().date())
    trang_thai = Column(Enum(TrangThaiKHEnum), nullable=False, default=TrangThaiKHEnum.HOAT_DONG)
    ngay_tao = Column(DateTime, nullable=False, default=datetime.now)
    ngay_cap_nhat = Column(DateTime, onupdate=datetime.now)
    
    hop_dongs = relationship("HopDong", back_populates="khach_hang")

class Kho(Base):
    __tablename__ = 'kho'
    
    ma_kho = Column(String(20), primary_key=True)
    ten_kho = Column(String(200), nullable=False)
    dia_chi = Column(Text, nullable=False)
    dien_tich = Column(Float, nullable=False)
    suc_chua = Column(Float, nullable=False)
    da_su_dung = Column(Float, nullable=False, default=0)
    trang_thai = Column(Enum(TrangThaiKhoEnum), nullable=False, default=TrangThaiKhoEnum.HOAT_DONG)
    ngay_tao = Column(DateTime, nullable=False, default=datetime.now)
    ngay_cap_nhat = Column(DateTime, onupdate=datetime.now)
    
    vi_tris = relationship("ViTri", back_populates="kho")

class ViTri(Base):
    __tablename__ = 'vi_tri'
    
    ma_vi_tri = Column(String(30), primary_key=True)
    ma_kho = Column(String(20), ForeignKey('kho.ma_kho'), nullable=False)
    khu_vuc = Column(String(50), nullable=False)
    hang = Column(String(10), nullable=False)
    tang = Column(Integer, nullable=False, default=1)
    dien_tich = Column(Float, nullable=False)
    gia_thue = Column(Float, nullable=False)
    suc_chua = Column(Float)
    trang_thai = Column(Enum(TrangThaiViTriEnum), nullable=False, default=TrangThaiViTriEnum.TRONG)
    ngay_tao = Column(DateTime, nullable=False, default=datetime.now)
    ngay_cap_nhat = Column(DateTime, onupdate=datetime.now)
    
    kho = relationship("Kho", back_populates="vi_tris")
    hop_dongs = relationship("HopDong", back_populates="vi_tri")

class HopDong(Base):
    __tablename__ = 'hop_dong'
    
    ma_hop_dong = Column(String(20), primary_key=True)
    ma_khach_hang = Column(String(20), ForeignKey('khach_hang.ma_khach_hang'), nullable=False)
    ma_vi_tri = Column(String(30), ForeignKey('vi_tri.ma_vi_tri'), nullable=False)
    ngay_bat_dau = Column(Date, nullable=False)
    ngay_ket_thuc = Column(Date, nullable=False)
    gia_thue = Column(Float, nullable=False)
    tien_coc = Column(Float, nullable=False, default=0)
    phuong_thuc_thanh_toan = Column(String(20), default='hang_thang')
    dieu_khoan = Column(Text)
    trang_thai = Column(Enum(TrangThaiHDEnum), nullable=False, default=TrangThaiHDEnum.HIEU_LUC)
    ly_do_cham_dut = Column(Text)
    ngay_cham_dut = Column(Date)
    ngay_tao = Column(DateTime, nullable=False, default=datetime.now)
    ngay_cap_nhat = Column(DateTime, onupdate=datetime.now)
    
    khach_hang = relationship("KhachHang", back_populates="hop_dongs")
    vi_tri = relationship("ViTri", back_populates="hop_dongs")
    hang_hoas = relationship("HangHoa", back_populates="hop_dong", cascade="all, delete-orphan")
    thanh_toans = relationship("ThanhToan", back_populates="hop_dong")

class HangHoa(Base):
    __tablename__ = 'hang_hoa'
    
    ma_hang_hoa = Column(String(30), primary_key=True)
    ma_hop_dong = Column(String(20), ForeignKey('hop_dong.ma_hop_dong'), nullable=False)
    ten_hang = Column(String(200), nullable=False)
    loai_hang = Column(String(100), nullable=False)
    so_luong = Column(Integer, nullable=False, default=0)
    don_vi = Column(String(20), nullable=False)
    trong_luong = Column(Float)
    kich_thuoc = Column(String(50))
    gia_tri = Column(Float)
    ngay_nhap = Column(DateTime, nullable=False, default=datetime.now)
    ngay_xuat = Column(DateTime)
    trang_thai = Column(String(20), nullable=False, default='trong_kho')
    vi_tri_luu_tru = Column(String(30))
    ghi_chu = Column(Text)
    hinh_anh = Column(Text)
    ngay_tao = Column(DateTime, nullable=False, default=datetime.now)
    ngay_cap_nhat = Column(DateTime, onupdate=datetime.now)
    
    hop_dong = relationship("HopDong", back_populates="hang_hoas")

class ThanhToan(Base):
    __tablename__ = 'thanh_toan'
    
    ma_thanh_toan = Column(String(30), primary_key=True)
    ma_hop_dong = Column(String(20), ForeignKey('hop_dong.ma_hop_dong'), nullable=False)
    loai_phi = Column(Enum(LoaiPhiEnum), nullable=False)
    so_tien = Column(Float, nullable=False)
    ky_thanh_toan = Column(String(20))
    ngay_den_han = Column(Date, nullable=False)
    ngay_thanh_toan = Column(Date)
    phuong_thuc = Column(String(20), nullable=False)
    so_giao_dich = Column(String(50))
    trang_thai = Column(Enum(TrangThaiTTEnum), nullable=False, default=TrangThaiTTEnum.CHUA_THANH_TOAN)
    phi_phat = Column(Float, nullable=False, default=0)
    ghi_chu = Column(Text)
    nguoi_thu = Column(String(100))
    ngay_tao = Column(DateTime, nullable=False, default=datetime.now)
    ngay_cap_nhat = Column(DateTime, onupdate=datetime.now)
    
    hop_dong = relationship("HopDong", back_populates="thanh_toans")

class NhanVien(Base):
    __tablename__ = 'nhan_vien'
    
    ma_nhan_vien = Column(String(20), primary_key=True)
    ho_ten = Column(String(200), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    so_dien_thoai = Column(String(20))
    vai_tro = Column(Enum(VaiTroNVEuum), nullable=False)
    tai_khoan = Column(String(50), unique=True, nullable=False)
    mat_khau = Column(String(255), nullable=False)
    trang_thai = Column(String(20), nullable=False, default='hoat_dong')
    ngay_tao = Column(DateTime, nullable=False, default=datetime.now)
    ngay_cap_nhat = Column(DateTime, onupdate=datetime.now)
    lan_dang_nhap_cuoi = Column(DateTime)

class SystemLog(Base):
    __tablename__ = 'system_log'
    
    ma_log = Column(Integer, primary_key=True, autoincrement=True)
    thoi_gian = Column(DateTime, nullable=False, default=datetime.now)
    ma_nhan_vien = Column(String(20), ForeignKey('nhan_vien.ma_nhan_vien'))
    hanh_dong = Column(Enum(HanhDongLogEnum), nullable=False)
    ban_ghi = Column(String(100), nullable=False)
    gia_tri_cu = Column(Text)
    gia_tri_moi = Column(Text)
    ip_address = Column(String(45))
    ghi_chu = Column(Text)

class BaoCao(Base):
    __tablename__ = 'bao_cao'
    
    ma_bao_cao = Column(String(30), primary_key=True)
    loai_bao_cao = Column(String(50), nullable=False)
    ngay_bat_dau = Column(Date, nullable=False)
    ngay_ket_thuc = Column(Date, nullable=False)
    ngay_tao = Column(DateTime, nullable=False, default=datetime.now)
    nguoi_tao = Column(String(20), ForeignKey('nhan_vien.ma_nhan_vien'))
    du_lieu = Column(Text)
    file_path = Column(String(500))
    trang_thai = Column(String(20), nullable=False, default='hoan_thanh')
    ghi_chu = Column(Text)

# Database initialization
def init_db(database_url='sqlite:///data/warehouse.db'):
    """Khởi tạo database và tạo các bảng"""
    engine = create_engine(database_url, echo=False)
    Base.metadata.create_all(engine)
    return engine

def get_session(engine):
    """Tạo session để làm việc với database"""
    Session = sessionmaker(bind=engine)
    return Session()
```

### 8.2 File: `src/data/schema.sql`

```sql
-- Schema SQL cho hệ thống Quản lý Kho Lưu trữ
-- Phiên bản: 1.0
-- Ngày: 23/04/2026

-- Enable foreign keys
PRAGMA foreign_keys = ON;

-- Bảng khách hàng
CREATE TABLE khach_hang (
    ma_khach_hang VARCHAR(20) PRIMARY KEY,
    ho_ten VARCHAR(200) NOT NULL,
    loai_khach VARCHAR(20) NOT NULL DEFAULT 'ca_nhan' CHECK (loai_khach IN ('ca_nhan', 'doanh_nghiep')),
    so_dien_thoai VARCHAR(20) NOT NULL,
    email VARCHAR(100) UNIQUE,
    dia_chi TEXT NOT NULL,
    ma_so_thue VARCHAR(20),
    ngay_dang_ky DATE NOT NULL DEFAULT (date('now')),
    trang_thai VARCHAR(20) NOT NULL DEFAULT 'hoat_dong' CHECK (trang_thai IN ('hoat_dong', 'tam_khoa', 'da_xoa')),
    ngay_tao DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ngay_cap_nhat DATETIME
);

-- Bảng kho
CREATE TABLE kho (
    ma_kho VARCHAR(20) PRIMARY KEY,
    ten_kho VARCHAR(200) NOT NULL,
    dia_chi TEXT NOT NULL,
    dien_tich DECIMAL(12,2) NOT NULL,
    suc_chua DECIMAL(12,2) NOT NULL,
    da_su_dung DECIMAL(12,2) NOT NULL DEFAULT 0,
    trang_thai VARCHAR(20) NOT NULL DEFAULT 'hoat_dong' CHECK (trang_thai IN ('hoat_dong', 'bao_tri', 'ngung')),
    ngay_tao DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ngay_cap_nhat DATETIME
);

-- Bảng vị trí
CREATE TABLE vi_tri (
    ma_vi_tri VARCHAR(30) PRIMARY KEY,
    ma_kho VARCHAR(20) NOT NULL,
    khu_vuc VARCHAR(50) NOT NULL,
    hang VARCHAR(10) NOT NULL,
    tang INTEGER NOT NULL DEFAULT 1,
    dien_tich DECIMAL(10,2) NOT NULL,
    gia_thue DECIMAL(12,2) NOT NULL,
    suc_chua DECIMAL(10,2),
    trang_thai VARCHAR(20) NOT NULL DEFAULT 'trong' CHECK (trang_thai IN ('trong', 'da_thue', 'bao_tri')),
    ngay_tao DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ngay_cap_nhat DATETIME,
    FOREIGN KEY (ma_kho) REFERENCES kho(ma_kho) ON DELETE RESTRICT
);

-- Bảng hợp đồng
CREATE TABLE hop_dong (
    ma_hop_dong VARCHAR(20) PRIMARY KEY,
    ma_khach_hang VARCHAR(20) NOT NULL,
    ma_vi_tri VARCHAR(30) NOT NULL,
    ngay_bat_dau DATE NOT NULL,
    ngay_ket_thuc DATE NOT NULL,
    gia_thue DECIMAL(12,2) NOT NULL,
    tien_coc DECIMAL(12,2) NOT NULL DEFAULT 0,
    phuong_thuc_thanh_toan VARCHAR(20) DEFAULT 'hang_thang',
    dieu_khoan TEXT,
    trang_thai VARCHAR(20) NOT NULL DEFAULT 'hieu_luc' CHECK (trang_thai IN ('hieu_luc', 'het_han', 'cham_dut', 'gia_han')),
    ly_do_cham_dut TEXT,
    ngay_cham_dut DATE,
    ngay_tao DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ngay_cap_nhat DATETIME,
    FOREIGN KEY (ma_khach_hang) REFERENCES khach_hang(ma_khach_hang),
    FOREIGN KEY (ma_vi_tri) REFERENCES vi_tri(ma_vi_tri)
);

-- Bảng hàng hóa
CREATE TABLE hang_hoa (
    ma_hang_hoa VARCHAR(30) PRIMARY KEY,
    ma_hop_dong VARCHAR(20) NOT NULL,
    ten_hang VARCHAR(200) NOT NULL,
    loai_hang VARCHAR(100) NOT NULL,
    so_luong INTEGER NOT NULL DEFAULT 0,
    don_vi VARCHAR(20) NOT NULL,
    trong_luong DECIMAL(10,2),
    kich_thuoc VARCHAR(50),
    gia_tri DECIMAL(12,2),
    ngay_nhap DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ngay_xuat DATETIME,
    trang_thai VARCHAR(20) NOT NULL DEFAULT 'trong_kho' CHECK (trang_thai IN ('trong_kho', 'da_xuat', 'hu_hong')),
    vi_tri_luu_tru VARCHAR(30),
    ghi_chu TEXT,
    hinh_anh TEXT,
    ngay_tao DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ngay_cap_nhat DATETIME,
    FOREIGN KEY (ma_hop_dong) REFERENCES hop_dong(ma_hop_dong) ON DELETE CASCADE
);

-- Bảng thanh toán
CREATE TABLE thanh_toan (
    ma_thanh_toan VARCHAR(30) PRIMARY KEY,
    ma_hop_dong VARCHAR(20) NOT NULL,
    loai_phi VARCHAR(20) NOT NULL CHECK (loai_phi IN ('tien_coc', 'thue_thang', 'phu_phi', 'phi_phat')),
    so_tien DECIMAL(12,2) NOT NULL,
    ky_thanh_toan VARCHAR(20),
    ngay_den_han DATE NOT NULL,
    ngay_thanh_toan DATE,
    phuong_thuc VARCHAR(20) NOT NULL,
    so_giao_dich VARCHAR(50),
    trang_thai VARCHAR(20) NOT NULL DEFAULT 'chua_thanh_toan' CHECK (trang_thai IN ('da_thanh_toan', 'chua_thanh_toan', 'qua_han')),
    phi_phat DECIMAL(12,2) NOT NULL DEFAULT 0,
    ghi_chu TEXT,
    nguoi_thu VARCHAR(100),
    ngay_tao DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ngay_cap_nhat DATETIME,
    FOREIGN KEY (ma_hop_dong) REFERENCES hop_dong(ma_hop_dong)
);

-- Bảng nhân viên
CREATE TABLE nhan_vien (
    ma_nhan_vien VARCHAR(20) PRIMARY KEY,
    ho_ten VARCHAR(200) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    so_dien_thoai VARCHAR(20),
    vai_tro VARCHAR(20) NOT NULL CHECK (vai_tro IN ('quan_tri', 'kinh_doanh', 'kho', 'ke_toan')),
    tai_khoan VARCHAR(50) UNIQUE NOT NULL,
    mat_khau VARCHAR(255) NOT NULL,
    trang_thai VARCHAR(20) NOT NULL DEFAULT 'hoat_dong',
    ngay_tao DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ngay_cap_nhat DATETIME,
    lan_dang_nhap_cuoi DATETIME
);

-- Bảng system log
CREATE TABLE system_log (
    ma_log INTEGER PRIMARY KEY AUTOINCREMENT,
    thoi_gian DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ma_nhan_vien VARCHAR(20),
    hanh_dong VARCHAR(20) NOT NULL CHECK (hanh_dong IN ('THEM', 'SUA', 'XOA', 'DANG_NHAP', 'DANG_XUAT')),
    ban_ghi VARCHAR(100) NOT NULL,
    gia_tri_cu TEXT,
    gia_tri_moi TEXT,
    ip_address VARCHAR(45),
    ghi_chu TEXT,
    FOREIGN KEY (ma_nhan_vien) REFERENCES nhan_vien(ma_nhan_vien) ON DELETE SET NULL
);

-- Bảng báo cáo
CREATE TABLE bao_cao (
    ma_bao_cao VARCHAR(30) PRIMARY KEY,
    loai_bao_cao VARCHAR(50) NOT NULL,
    ngay_bat_dau DATE NOT NULL,
    ngay_ket_thuc DATE NOT NULL,
    ngay_tao DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    nguoi_tao VARCHAR(20),
    du_lieu TEXT,
    file_path VARCHAR(500),
    trang_thai VARCHAR(20) NOT NULL DEFAULT 'hoan_thanh',
    ghi_chu TEXT,
    FOREIGN KEY (nguoi_tao) REFERENCES nhan_vien(ma_nhan_vien) ON DELETE SET NULL
);

-- Indexes
CREATE INDEX idx_khach_hang_so_dien_thoai ON khach_hang(so_dien_thoai);
CREATE INDEX idx_khach_hang_email ON khach_hang(email);
CREATE INDEX idx_khach_hang_trang_thai ON khach_hang(trang_thai);

CREATE INDEX idx_kho_ten_kho ON kho(ten_kho);
CREATE INDEX idx_kho_trang_thai ON kho(trang_thai);

CREATE INDEX idx_vi_tri_ma_kho ON vi_tri(ma_kho);
CREATE INDEX idx_vi_tri_trang_thai ON vi_tri(trang_thai);
CREATE INDEX idx_vi_tri_khu_vuc ON vi_tri(khu_vuc, hang, tang);

CREATE INDEX idx_hop_dong_ma_khach_hang ON hop_dong(ma_khach_hang);
CREATE INDEX idx_hop_dong_ma_vi_tri ON hop_dong(ma_vi_tri);
CREATE INDEX idx_hop_dong_ngay_ket_thuc ON hop_dong(ngay_ket_thuc);
CREATE INDEX idx_hop_dong_trang_thai ON hop_dong(trang_thai);
CREATE INDEX idx_hop_dong_kh_trang_thai ON hop_dong(ma_khach_hang, trang_thai);

CREATE INDEX idx_hang_hoa_ma_hop_dong ON hang_hoa(ma_hop_dong);
CREATE INDEX idx_hang_hoa_ten_hang ON hang_hoa(ten_hang);
CREATE INDEX idx_hang_hoa_trang_thai ON hang_hoa(trang_thai);
CREATE INDEX idx_hang_hoa_ngay_nhap ON hang_hoa(ngay_nhap);
CREATE INDEX idx_hang_hoa_hd_trang_thai ON hang_hoa(ma_hop_dong, trang_thai);

CREATE INDEX idx_thanh_toan_ma_hop_dong ON thanh_toan(ma_hop_dong);
CREATE INDEX idx_thanh_toan_ngay_den_han ON thanh_toan(ngay_den_han);
CREATE INDEX idx_thanh_toan_trang_thai ON thanh_toan(trang_thai);
CREATE INDEX idx_thanh_toan_hd_trang_thai ON thanh_toan(ma_hop_dong, trang_thai);

CREATE INDEX idx_nhan_vien_tai_khoan ON nhan_vien(tai_khoan);
CREATE INDEX idx_nhan_vien_email ON nhan_vien(email);
CREATE INDEX idx_nhan_vien_vai_tro ON nhan_vien(vai_tro);

CREATE INDEX idx_system_log_thoi_gian ON system_log(thoi_gian);
CREATE INDEX idx_system_log_ma_nhan_vien ON system_log(ma_nhan_vien);
CREATE INDEX idx_system_log_hanh_dong ON system_log(hanh_dong);
CREATE INDEX idx_system_log_ban_ghi ON system_log(ban_ghi);

CREATE INDEX idx_bao_cao_loai_bao_cao ON bao_cao(loai_bao_cao);
CREATE INDEX idx_bao_cao_ngay_tao ON bao_cao(ngay_tao);

-- Views
CREATE VIEW v_hop_dong_sap_het_han AS
SELECT 
    hd.ma_hop_dong,
    hd.ma_khach_hang,
    kh.ho_ten AS ten_khach_hang,
    hd.ma_vi_tri,
    hd.ngay_bat_dau,
    hd.ngay_ket_thuc,
    hd.gia_thue,
    hd.trang_thai,
    julianday(hd.ngay_ket_thuc) - julianday('now') AS so_ngay_con_lai
FROM hop_dong hd
JOIN khach_hang kh ON hd.ma_khach_hang = kh.ma_khach_hang
WHERE hd.trang_thai = 'hieu_luc'
  AND hd.ngay_ket_thuc <= date('now', '+30 days')
  AND hd.ngay_ket_thuc >= date('now')
ORDER BY hd.ngay_ket_thuc ASC;

CREATE VIEW v_cong_no_chua_thanh_toan AS
SELECT 
    tt.ma_thanh_toan,
    tt.ma_hop_dong,
    hd.ma_khach_hang,
    kh.ho_ten AS ten_khach_hang,
    tt.loai_phi,
    tt.so_tien,
    tt.phi_phat,
    tt.so_tien + tt.phi_phat AS tong_cong,
    tt.ngay_den_han,
    julianday('now') - julianday(tt.ngay_den_han) AS so_ngay_qua_han,
    tt.trang_thai
FROM thanh_toan tt
JOIN hop_dong hd ON tt.ma_hop_dong = hd.ma_hop_dong
JOIN khach_hang kh ON hd.ma_khach_hang = kh.ma_khach_hang
WHERE tt.trang_thai IN ('chua_thanh_toan', 'qua_han')
ORDER BY tt.ngay_den_han ASC;

CREATE VIEW v_ty_le_lap_day_kho AS
SELECT 
    k.ma_kho,
    k.ten_kho,
    k.dien_tich,
    k.suc_chua,
    COALESCE(SUM(v.dien_tich), 0) AS da_su_dung,
    ROUND((COALESCE(SUM(v.dien_tich), 0) * 100.0 / k.suc_chua), 2) AS ty_le_lap_day_phan_tram
FROM kho k
LEFT JOIN vi_tri v ON k.ma_kho = v.ma_kho AND v.trang_thai = 'da_thue'
WHERE k.trang_thai = 'hoat_dong'
GROUP BY k.ma_kho, k.ten_kho, k.dien_tich, k.suc_chua;

-- Insert admin user (password: admin123 - bcrypt hash)
INSERT INTO nhan_vien (ma_nhan_vien, ho_ten, email, vai_tro, tai_khoan, mat_khau)
VALUES ('NV001', 'Administrator', 'admin@warehouse.local', 'quan_tri', 'admin', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYILp92S.0i');
```

---

## 9. CÁC MẪU TRUY VẤN THƯỜNG DÙNG

### 9.1 Tìm kiếm khách hàng

```sql
-- Tìm theo tên (fuzzy search)
SELECT * FROM khach_hang 
WHERE ho_ten LIKE '%Nguyễn%' 
  AND trang_thai = 'hoat_dong';

-- Tìm theo số điện thoại
SELECT * FROM khach_hang 
WHERE so_dien_thoai = '0901234567';

-- Tìm theo email
SELECT * FROM khach_hang 
WHERE email = 'customer@email.com';
```

### 9.2 Quản lý hợp đồng

```sql
-- Lấy tất cả hợp đồng của khách hàng
SELECT hd.*, vt.ten_kho, vt.ma_vi_tri
FROM hop_dong hd
JOIN vi_tri vt ON hd.ma_vi_tri = vt.ma_vi_tri
WHERE hd.ma_khach_hang = 'KH001'
ORDER BY hd.ngay_tao DESC;

-- Hợp đồng sắp hết hạn trong 30 ngày
SELECT * FROM v_hop_dong_sap_het_han;

-- Hợp đồng đang hiệu lực theo kho
SELECT hd.*, kh.ho_ten, vt.ma_vi_tri
FROM hop_dong hd
JOIN khach_hang kh ON hd.ma_khach_hang = kh.ma_khach_hang
JOIN vi_tri vt ON hd.ma_vi_tri = vt.ma_vi_tri
WHERE hd.trang_thai = 'hieu_luc'
  AND vt.ma_kho = 'KHO001';
```

### 9.3 Thanh toán & Công nợ

```sql
-- Công nợ chưa thanh toán
SELECT * FROM v_cong_no_chua_thanh_toan;

-- Lịch sử thanh toán của hợp đồng
SELECT * FROM thanh_toan
WHERE ma_hop_dong = 'HD20260401001'
ORDER BY ngay_tao DESC;

-- Doanh thu tháng này
SELECT 
    loai_phi,
    COUNT(*) AS so_giao_dich,
    SUM(so_tien) AS tong_tien
FROM thanh_toan
WHERE trang_thai = 'da_thanh_toan'
  AND strftime('%Y-%m', ngay_thanh_toan) = strftime('%Y-%m', 'now')
GROUP BY loai_phi;
```

### 9.4 Hàng hóa & Tồn kho

```sql
-- Tất cả hàng hóa trong hợp đồng
SELECT * FROM hang_hoa
WHERE ma_hop_dong = 'HD20260401001'
  AND trang_thai = 'trong_kho';

-- Hàng hóa sắp hết hạn (nếu có ghi chú hạn sử dụng)
SELECT * FROM hang_hoa
WHERE trang_thai = 'trong_kho'
  AND ghi_chu LIKE '%hạn sử dụng%';

-- Thống kê hàng hóa theo loại
SELECT loai_hang, COUNT(*) AS so_luong_loai
FROM hang_hoa
WHERE trang_thai = 'trong_kho'
GROUP BY loai_hang;
```

### 9.5 Báo cáo

```sql
-- Tỷ lệ lấp đầy tất cả kho
SELECT * FROM v_ty_le_lap_day_kho;

-- Doanh thu theo tháng
SELECT * FROM v_doanh_thu_theo_thang;

-- Top 10 khách hàng doanh thu cao nhất
SELECT 
    kh.ma_khach_hang,
    kh.ho_ten,
    SUM(tt.so_tien) AS tong_doanh_thu
FROM khach_hang kh
JOIN hop_dong hd ON kh.ma_khach_hang = hd.ma_khach_hang
JOIN thanh_toan tt ON hd.ma_hop_dong = tt.ma_hop_dong
WHERE tt.trang_thai = 'da_thanh_toan'
GROUP BY kh.ma_khach_hang, kh.ho_ten
ORDER BY tong_doanh_thu DESC
LIMIT 10;
```

---

## 10. BẢO MẬT & PHÂN QUYỀN

### 10.1 Mã hóa mật khẩu

- Sử dụng **bcrypt** với cost factor 12
- Password hash lưu trong bảng `nhan_vien.mat_khau`
- Độ dài tối đa: 255 ký tự

### 10.2 Phân quyền theo vai trò

| Chức năng | Quản trị | Kinh doanh | Kho | Kế toán |
|-----------|----------|------------|-----|---------|
| Quản lý nhân viên | ✅ | ❌ | ❌ | ❌ |
| Quản lý khách hàng | ✅ | ✅ | ❌ | ❌ |
| Quản lý hợp đồng | ✅ | ✅ | ❌ | ❌ |
| Nhập/Xuất hàng | ✅ | ❌ | ✅ | ❌ |
| Thanh toán | ✅ | ❌ | ❌ | ✅ |
| Xem báo cáo | ✅ | ✅ | ✅ | ✅ |
| Xuất báo cáo | ✅ | ✅ | ❌ | ✅ |
| Cấu hình hệ thống | ✅ | ❌ | ❌ | ❌ |

### 10.3 Audit log

Tất cả thao tác THEM, SỬA, XÓA trên các bảng quan trọng đều được ghi log:
- `khach_hang` - Thêm/sửa/xóa khách hàng
- `hop_dong` - Tạo/sửa/chấm dứt hợp đồng
- `thanh_toan` - Ghi nhận thanh toán, điều chỉnh
- `hang_hoa` - Nhập/xuất hàng
- `nhan_vien` - Quản lý tài khoản

---

## 11. SAO LƯU & PHỤC HỒI

### 11.1 Backup tự động

```bash
#!/bin/bash
# backup_database.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups/warehouse"
DB_FILE="data/warehouse.db"

# Create backup directory if not exists
mkdir -p $BACKUP_DIR

# Copy database file
cp $DB_FILE $BACKUP_DIR/warehouse_$DATE.db

# Keep only last 30 days of backups
find $BACKUP_DIR -name "warehouse_*.db" -mtime +30 -delete

echo "Backup completed: warehouse_$DATE.db"
```

### 11.2 Phục hồi

```bash
# Restore from backup
cp /backups/warehouse/warehouse_20260423_120000.db data/warehouse.db

# Verify integrity
sqlite3 data/warehouse.db "PRAGMA integrity_check;"
```

### 11.3 Vacuum database

```sql
-- Thu gọn database, tối ưu không gian
VACUUM;

-- Phân tích indexes
ANALYZE;
```

---

## 12. KẾ HOẠCH MỞ RỘNG

### 12.1 Giai đoạn 2 (nếu cần)

| Tính năng | Bảng mới/Ghi chú |
|-----------|-----------------|
| Multi-user với phân quyền chi tiết | Bảng `phan_quyen`, `chuc_nang` |
| Email notification | Bảng `email_queue`, `email_template` |
| SMS notification | Bảng `sms_queue`, `sms_provider` |
| Attachment/files | Bảng `attachments` (polymorphic) |
| Version history | Bảng `versions` cho từng entity |
| Dashboard metrics | Materialized views cho performance |

### 12.2 Migration sang PostgreSQL

Khi hệ thống cần scale:
- Sử dụng Alembic để migration schema
- Chuyển đổi data types phù hợp
- Update connection string trong config
- Test kỹ trước khi deploy production

---

## PHỤ LỤC

### A. Quy tắc đặt tên

- **Bảng:** Số nhiều, snake_case (khach_hang, hop_dong)
- **Cột:** snake_case, mô tả rõ nghĩa
- **Primary Key:** ma_<ten_bảng> (ma_khach_hang)
- **Foreign Key:** ma_<ten_bảng_tham_chieu>
- **Index:** idx_<ten_bảng>_<ten_cot>
- **View:** v_<mo_ta>
- **Trigger:** trg_<hanh_dong>_<ban_ghi>

### B. Data validation rules

| Trường | Rule |
|--------|------|
| so_dien_thoai | /^0[0-9]{9,10}$/ |
| email | Standard email regex |
| gia_thue, so_tien | >= 0 |
| dien_tich, suc_chua | > 0 |
| ngay_ket_thuc | > ngay_bat_dau |
| so_luong | >= 0 |

### C. Default values

| Trường | Default |
|--------|---------|
| trang_thai (khach_hang) | 'hoat_dong' |
| trang_thai (kho) | 'hoat_dong' |
| trang_thai (vi_tri) | 'trong' |
| trang_thai (hop_dong) | 'hieu_luc' |
| trang_thai (hang_hoa) | 'trong_kho' |
| trang_thai (thanh_toan) | 'chua_thanh_toan' |
| tien_coc | 0 |
| phi_phat | 0 |

---

