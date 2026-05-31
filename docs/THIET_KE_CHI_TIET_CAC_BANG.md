# Thiết Kế Chi Tiết Các Bảng Cơ Sở Dữ Liệu

**Đề tài:** Quản Lý Dịch Vụ Cho Thuê Kho Lưu Trữ Hàng Hóa
**Nhóm thực hiện:** Nhóm 12 - Lập trình Python
**Ngày cập nhật:** 10/05/2026

---

## Mục lục

1. [Tổng quan thiết kế cơ sở dữ liệu](#1-tổng-quan-thiết-kế-cơ-sở-dữ-liệu)
2. [Lớp cơ sở BaseModel](#2-lớp-cơ-sở-basemodel)
3. [Các kiểu liệt kê (Enums)](#3-các-kiểu-liệt-kê-enums)
4. [Bảng khach_hang (Khách hàng)](#4-bảng-khach_hang-khách-hàng)
5. [Bảng kho (Kho hàng)](#5-bảng-kho-kho-hàng)
6. [Bảng vi_tri (Vị trí lưu trữ)](#6-bảng-vi_tri-vị-trí-lưu-trữ)
7. [Bảng hop_dong (Hợp đồng thuê)](#7-bảng-hop_dong-hợp-đồng-thuê)
8. [Bảng hang_hoa (Hàng hóa)](#8-bảng-hang_hoa-hàng-hóa)
9. [Bảng loai_hang (Loại hàng)](#9-bảng-loai_hang-loại-hàng)
10. [Bảng thanh_toan (Thanh toán)](#10-bảng-thanh_toan-thanh-toán)
11. [Bảng nhan_vien (Nhân viên)](#11-bảng-nhan_vien-nhân-viên)
12. [Bảng system_log (Nhật ký hệ thống)](#12-bảng-system_log-nhật-ký-hệ-thống)
13. [Bảng bao_cao (Báo cáo)](#13-bảng-bao_cao-báo-cáo)
14. [Các chỉ mục (Indexes)](#14-các-chỉ-mục-indexes)
15. [Các view (Khung nhìn)](#15-các-view-khung-nhìn)
16. [Mối quan hệ giữa các bảng](#16-mối-quan-hệ-giữa-các-bảng)

---

## 1. Tổng quan thiết kế cơ sở dữ liệu

Cơ sở dữ liệu của hệ thống Quản Lý Dịch Vụ Cho Thuê Kho Lưu Trữ Hàng Hóa được thiết kế theo chuẩn 3NF (Third Normal Form), sử dụng SQLite làm hệ quản trị cơ sở dữ liệu và SQLAlchemy 2.0 làm ORM (Object-Relational Mapping). Hệ thống gồm 10 bảng dữ liệu, 3 khung nhìn (view) và hơn 20 chỉ mục (index) được tối ưu cho hiệu năng truy vấn. Cấu trúc đầy đủ của cơ sở dữ liệu được định nghĩa trong tệp tin `src/data/schema.sql` dưới dạng SQL thuần, và được ánh xạ sang các lớp ORM trong thư mục `src/models/`. Các bảng được tổ chức xoay quanh ba thực thể cốt lõi: khách hàng (khach_hang), kho hàng (kho kết hợp vi_tri) và hợp đồng (hop_dong). Từ hợp đồng, các nghiệp vụ phát sinh bao gồm hàng hóa (hang_hoa), thanh toán (thanh_toan) và các bảng hỗ trợ như nhân viên (nhan_vien), nhật ký hệ thống (system_log), loại hàng (loai_hang) và báo cáo (bao_cao).

Tệp tin cơ sở dữ liệu được lưu tại `data/warehouse.db` với cơ chế khóa ngoại (foreign keys) được bật thông qua lệnh `PRAGMA foreign_keys = ON`. Việc khởi tạo cơ sở dữ liệu được thực hiện thông qua tập lệnh `src/data/database.py`, tự động tạo bảng từ các định nghĩa SQLAlchemy models, tạo chỉ mục, tạo khung nhìn và chèn dữ liệu mẫu ban đầu.

---

## 2. Lớp cơ sở BaseModel

Tất cả các mô hình đều kế thừa từ lớp `BaseModel` được định nghĩa trong `src/models/base.py`. Lớp này là lớp trừu tượng (`__abstract__ = True`), không ánh xạ đến bảng nào trong cơ sở dữ liệu, mà chỉ cung cấp hai trường dùng chung và ba phương thức tiện ích cho tất cả các bảng.

Hai trường dùng chung mà BaseModel cung cấp:

| Tên trường | Kiểu dữ liệu | Mô tả |
|---|---|---|
| ngay_tao | DateTime | Thời điểm tạo bản ghi, tự động gán giá trị là thời điểm hiện tại (datetime.now) khi tạo mới |
| ngay_cap_nhat | DateTime | Thời điểm cập nhật bản ghi gần nhất, tự động cập nhật khi bản ghi được sửa đổi |

Ba phương thức tiện ích mà BaseModel cung cấp:

| Phương thức | Mô tả |
|---|---|
| to_dict() | Chuyển đổi bản ghi thành từ điển Python, tự động chuyển đổi các đối tượng datetime thành chuỗi ISO 8601 |
| to_json() | Chuyển đổi bản ghi thành chuỗi JSON có định dạng đẹp (indent = 2) |
| __repr__() | Trả về chuỗi biểu diễn ngắn gọn của bản ghi, hiển thị tên lớp và các trường chính |

Như vậy, mỗi bảng trong cơ sở dữ liệu đều có hai cột ngay_tao và ngay_cap_nhat được tự động quản lý, giúp theo dõi lịch sử thao tác trên từng bản ghi mà không cần lập trình thêm.

---

## 3. Các kiểu liệt kê (Enums)

Tệp tin `src/models/enums.py` tập trung định nghĩa tất cả các kiểu liệt kê được sử dụng xuyên suốt hệ thống. Việc tập trung các enum vào một file duy nhất giúp đảm bảo tính nhất quán và dễ bảo trì. Dưới đây là danh sách đầy đủ các enum:

| Tên Enum | Giá trị | Mô tả |
|---|---|---|
| TrangThaiHDEnum | HIEU_LUC, HET_HAN, CHAM_DUT, GIA_HAN | Trạng thái hợp đồng: Hiệu lực, Hết hạn, Chấm dứt, Gia hạn |
| TrangThaiTTEnum | DA_THANH_TOAN, CHUA_THANH_TOAN, QUA_HAN | Trạng thái thanh toán: Đã thanh toán, Chưa thanh toán, Quá hạn |
| TrangThaiViTriEnum | TRONG, DA_THUE, BAO_TRI | Trạng thái vị trí: Trống, Đã thuê, Bảo trì |
| TrangThaiKhoEnum | HOAT_DONG, BAO_TRI, NGUNG | Trạng thái kho: Hoạt động, Bảo trì, Ngừng |
| LoaiKhachEnum | CA_NHAN, DOANH_NGHIEP | Loại khách hàng: Cá nhân, Doanh nghiệp |
| TrangThaiKHEnum | HOAT_DONG, TAM_KHOA, DA_XOA | Trạng thái khách hàng: Hoạt động, Tạm khóa, Đã xóa |
| LoaiPhiEnum | TIEN_COC, THUE_THANG, PHU_PHI, PHI_PHAT | Loại phí: Tiền cọc, Thuê tháng, Phụ phí, Phí phạt |
| TrangThaiHHEnum | TRONG_KHO, DA_XUAT | Trạng thái hàng hóa: Trong kho, Đã xuất |
| VaiTroNhanVienEnum | QUAN_TRI, KINH_DOANH, KHO, KE_TOAN | Vai trò nhân viên: Quản trị, Kinh doanh, Kho, Kế toán |
| TrangThaiNhanVienEnum | HOAT_DONG, NGUNG_HOAT_DONG | Trạng thái nhân viên: Hoạt động, Ngừng hoạt động |
| HanhDongLogEnum | THEM, SUA, XOA, DANG_NHAP, DANG_XUAT | Hành động trong nhật ký: Thêm, Sửa, Xóa, Đăng nhập, Đăng xuất |

---

## 4. Bảng khach_hang (Khách hàng)

Bảng `khach_hang` lưu trữ thông tin của tất cả khách hàng sử dụng dịch vụ cho thuê kho, bao gồm cả khách hàng cá nhân và doanh nghiệp. Mỗi khách hàng có một mã duy nhất làm khóa chính. Bảng này có quan hệ một-nhiều với bảng `hop_dong`: một khách hàng có thể có nhiều hợp đồng thuê kho.

Các cột của bảng khach_hang:

| Tên cột | Kiểu dữ liệu | Ràng buộc | Giá trị mặc định | Mô tả |
|---|---|---|---|---|
| ma_khach_hang | String(20) | PRIMARY KEY | — | Mã khách hàng duy nhất, định dạng KH+YYYYMMDD+xxxx |
| ho_ten | String(200) | NOT NULL | — | Họ tên khách hàng (cá nhân) hoặc tên công ty (doanh nghiệp) |
| loai_khach | Enum | NOT NULL | CA_NHAN | Loại khách hàng: CA_NHAN hoặc DOANH_NGHIEP |
| so_dien_thoai | String(20) | NOT NULL | — | Số điện thoại liên hệ |
| email | String(100) | UNIQUE | — | Địa chỉ email, không được trùng với khách hàng khác |
| dia_chi | String(500) | NOT NULL | — | Địa chỉ liên hệ đầy đủ |
| ma_so_thue | String(20) | — | — | Mã số thuế (chỉ áp dụng cho doanh nghiệp) |
| ngay_dang_ky | Date | NOT NULL | date.today() | Ngày đăng ký trở thành khách hàng |
| trang_thai | Enum | NOT NULL | HOAT_DONG | Trạng thái khách hàng: HOAT_DONG, TAM_KHOA, DA_XOA |

Mã khách hàng được tạo tự động theo định dạng `KH` + `YYYYMMDD` (ngày hiện tại) + 4 chữ số ngẫu nhiên, ví dụ: `KH202604011234`. Việc xóa khách hàng chỉ là xóa mềm (soft delete) thông qua việc chuyển trạng thái sang `DA_XOA`, trừ khi khách hàng không còn hợp đồng đang hoạt động. Trường email được đánh chỉ mục duy nhất để đảm bảo không có hai khách hàng nào dùng chung một địa chỉ email.

---

## 5. Bảng kho (Kho hàng)

Bảng `kho` lưu trữ thông tin về các kho hàng vật lý mà hệ thống quản lý. Mỗi kho có một mã duy nhất, thông tin về vị trí địa lý, diện tích và sức chứa. Bảng này có quan hệ một-nhiều với bảng `vi_tri`: một kho có thể chứa nhiều vị trí lưu trữ.

Các cột của bảng kho:

| Tên cột | Kiểu dữ liệu | Ràng buộc | Giá trị mặc định | Mô tả |
|---|---|---|---|---|
| ma_kho | String(20) | PRIMARY KEY | — | Mã kho duy nhất |
| ten_kho | String(200) | NOT NULL | — | Tên kho hàng |
| dia_chi | String(500) | NOT NULL | — | Địa chỉ kho hàng |
| dien_tich | Float | NOT NULL | — | Tổng diện tích kho (m2) |
| suc_chua | Float | NOT NULL | — | Sức chứa tối đa (m3) |
| da_su_dung | Float | NOT NULL | 0 | Diện tích đã được sử dụng (m2), được cập nhật tự động |
| trang_thai | Enum | NOT NULL | HOAT_DONG | Trạng thái kho: HOAT_DONG, BAO_TRI, NGUNG |

Ngoài các cột trên, mô hình `Kho` còn cung cấp hai thuộc tính tính toán (computed properties). Thuộc tính `ty_le_lap_day` trả về tỷ lệ lấp đầy của kho dưới dạng phần trăm, được tính bằng `da_su_dung / suc_chua * 100`. Thuộc tính `dung_tich_con_lai` trả về dung tích còn trống của kho, được tính bằng `suc_chua - da_su_dung`. Kho không thể bị xóa nếu vẫn còn vị trí lưu trữ bên trong.

---

## 6. Bảng vi_tri (Vị trí lưu trữ)

Bảng `vi_tri` lưu trữ thông tin chi tiết về từng vị trí lưu trữ trong kho. Vị trí được tổ chức theo ba cấp: Khu vực (Zone), Hàng (Rack), Tầng (Shelf). Mỗi vị trí thuộc về một kho cụ thể thông qua khóa ngoại ma_kho. Bảng này có quan hệ nhiều-một với bảng `kho` (nhiều vị trí thuộc một kho) và quan hệ một-một với bảng `hop_dong` (một vị trí chỉ được thuê bởi một hợp đồng tại một thời điểm).

Các cột của bảng vi_tri:

| Tên cột | Kiểu dữ liệu | Ràng buộc | Giá trị mặc định | Mô tả |
|---|---|---|---|---|
| ma_vi_tri | String(30) | PRIMARY KEY | — | Mã vị trí duy nhất |
| ma_kho | String(20) | FOREIGN KEY → kho(ma_kho), ON DELETE RESTRICT | — | Mã kho chứa vị trí này |
| khu_vuc | String(50) | NOT NULL | — | Khu vực (Zone) trong kho |
| hang | String(10) | NOT NULL | — | Hàng (Rack) trong khu vực |
| tang | Integer | NOT NULL | 1 | Tầng (Shelf) trong hàng |
| dien_tich | Float | NOT NULL | — | Diện tích vị trí (m2) |
| gia_thue | Float | NOT NULL | — | Giá thuê mỗi tháng |
| suc_chua | Float | — | — | Sức chứa của vị trí (m3) |
| trang_thai | Enum | NOT NULL | TRONG | Trạng thái: TRONG, DA_THUE, BAO_TRI |

Khi một hợp đồng được tạo, trạng thái vị trí sẽ tự động chuyển từ `TRONG` sang `DA_THUE`. Khi hợp đồng kết thúc hoặc bị chấm dứt, trạng thái vị trí sẽ được chuyển lại thành `TRONG`. Ràng buộc `ON DELETE RESTRICT` trên khóa ngoại ma_kho đảm bảo không thể xóa một kho khi vẫn còn vị trí bên trong.

---

## 7. Bảng hop_dong (Hợp đồng thuê)

Bảng `hop_dong` là bảng trung tâm của hệ thống, lưu trữ thông tin về các hợp đồng thuê kho. Mỗi hợp đồng liên kết một khách hàng với một vị trí lưu trữ trong một khoảng thời gian nhất định. Bảng này có quan hệ nhiều-một với `khach_hang`, nhiều-một với `vi_tri`, một-nhiều với `hang_hoa` và một-nhiều với `thanh_toan`.

Các cột của bảng hop_dong:

| Tên cột | Kiểu dữ liệu | Ràng buộc | Giá trị mặc định | Mô tả |
|---|---|---|---|---|
| ma_hop_dong | String(20) | PRIMARY KEY | — | Mã hợp đồng duy nhất, định dạng HDYYYYMMxxx |
| ma_khach_hang | String(20) | FOREIGN KEY → khach_hang(ma_khach_hang) | — | Mã khách hàng thuê |
| ma_vi_tri | String(30) | FOREIGN KEY → vi_tri(ma_vi_tri) | — | Mã vị trí được thuê |
| ngay_bat_dau | Date | NOT NULL | — | Ngày bắt đầu hiệu lực hợp đồng |
| ngay_ket_thuc | Date | NOT NULL | — | Ngày kết thúc hợp đồng |
| gia_thue | Float | NOT NULL | — | Giá thuê mỗi tháng |
| tien_coc | Float | NOT NULL | 0 | Tiền cọc (nếu có) |
| phuong_thuc_thanh_toan | String(20) | NOT NULL | hang_thang | Phương thức thanh toán: hang_thang, hang_quy, hang_nam, mot_lan |
| dieu_khoan | Text | — | — | Điều khoản hợp đồng |
| trang_thai | Enum | NOT NULL | HIEU_LUC | Trạng thái: HIEU_LUC, HET_HAN, CHAM_DUT, GIA_HAN |
| ly_do_cham_dut | Text | — | — | Lý do chấm dứt hợp đồng (nếu có) |
| ngay_cham_dut | Date | — | — | Ngày chấm dứt thực tế (nếu chấm dứt trước hạn) |

Hợp đồng không thể bị xóa nếu đã có phát sinh thanh toán. Khi xóa hợp đồng, hệ thống sẽ tự động xóa các bản ghi hàng hóa và thanh toán liên quan, đồng thời giải phóng vị trí (chuyển trạng thái vị trí về `TRONG`). Mã hợp đồng được tạo tự động theo định dạng `HD` + `YYYY` + `MM` + 3 chữ số tăng dần, ví dụ: `HD202604001`.

---

## 8. Bảng hang_hoa (Hàng hóa)

Bảng `hang_hoa` lưu trữ thông tin về hàng hóa được khách hàng lưu trữ trong kho. Mỗi mặt hàng thuộc về một hợp đồng cụ thể. Bảng này có quan hệ nhiều-một với bảng `hop_dong`.

Các cột của bảng hang_hoa:

| Tên cột | Kiểu dữ liệu | Ràng buộc | Giá trị mặc định | Mô tả |
|---|---|---|---|---|
| ma_hang_hoa | String(30) | PRIMARY KEY | — | Mã hàng hóa duy nhất, định dạng {MA_HD}-HHxxx |
| ma_hop_dong | String(20) | FOREIGN KEY → hop_dong(ma_hop_dong), ON DELETE CASCADE | — | Mã hợp đồng chứa hàng hóa này |
| ten_hang | String(200) | NOT NULL | — | Tên hàng hóa |
| loai_hang | String(100) | NOT NULL | — | Loại hàng hóa |
| so_luong | Integer | NOT NULL | 0 | Số lượng |
| don_vi | String(20) | NOT NULL | — | Đơn vị tính (kg, cái, thùng, ...) |
| trong_luong | Float | — | — | Trọng lượng (kg) |
| kich_thuoc | String(50) | — | — | Kích thước (dài x rộng x cao) |
| gia_tri | Float | — | — | Giá trị hàng hóa |
| ngay_nhap | DateTime | NOT NULL | datetime.now() | Thời điểm nhập kho |
| ngay_xuat | DateTime | — | — | Thời điểm xuất kho |
| trang_thai | String(20) | NOT NULL | trong_kho | Trạng thái: trong_kho, da_xuat |
| vi_tri_luu_tru | String(30) | — | — | Vị trí lưu trữ cụ thể trong kho |
| ghi_chu | Text | — | — | Ghi chú đặc biệt về hàng hóa |
| hinh_anh | Text | — | — | Danh sách đường dẫn hình ảnh (lưu dưới dạng JSON array) |

Khi hợp đồng bị xóa, tất cả hàng hóa liên quan cũng bị xóa theo nhờ ràng buộc `ON DELETE CASCADE`. Hàng hóa có thể được nhập và xuất nhiều lần, với trạng thái tự động cập nhật khi số lượng tồn kho bằng 0. Mã hàng hóa được tạo tự động theo định dạng `{MaHopDong}-HH` + 3 chữ số, ví dụ: `HD202604001-HH001`.

---

## 9. Bảng loai_hang (Loại hàng)

Bảng `loai_hang` lưu trữ danh mục các loại hàng hóa, giúp người dùng phân loại và quản lý hàng hóa một cách có hệ thống. Đây là bảng độc lập, không có khóa ngoại tham chiếu đến bảng khác.

Các cột của bảng loai_hang:

| Tên cột | Kiểu dữ liệu | Ràng buộc | Giá trị mặc định | Mô tả |
|---|---|---|---|---|
| ma_loai | String(30) | PRIMARY KEY | — | Mã loại hàng duy nhất, định dạng LHxxx |
| ten_loai | String(100) | NOT NULL | — | Tên loại hàng |
| mo_ta | Text | — | — | Mô tả chi tiết về loại hàng |
| ghi_chu | Text | — | — | Ghi chú thêm |

Mã loại hàng được tạo tự động theo định dạng `LH` + 3 chữ số tăng dần, ví dụ: `LH001`, `LH002`. Bảng này cung cấp danh sách các loại hàng để người dùng lựa chọn khi nhập hàng hóa mới.

---

## 10. Bảng thanh_toan (Thanh toán)

Bảng `thanh_toan` lưu trữ thông tin về các khoản thanh toán liên quan đến hợp đồng thuê kho. Mỗi khoản thanh toán thuộc về một hợp đồng cụ thể. Bảng này có quan hệ nhiều-một với bảng `hop_dong`.

Các cột của bảng thanh_toan:

| Tên cột | Kiểu dữ liệu | Ràng buộc | Giá trị mặc định | Mô tả |
|---|---|---|---|---|
| ma_thanh_toan | String(30) | PRIMARY KEY | — | Mã thanh toán duy nhất, định dạng {MA_HD}-TTxxx |
| ma_hop_dong | String(20) | FOREIGN KEY → hop_dong(ma_hop_dong) | — | Mã hợp đồng được thanh toán |
| loai_phi | Enum | NOT NULL | — | Loại phí: TIEN_COC, THUE_THANG, PHU_PHI, PHI_PHAT |
| so_tien | Float | NOT NULL | — | Số tiền thanh toán |
| ky_thanh_toan | String(20) | — | — | Kỳ thanh toán (ví dụ: 2026-04, 2026-Q2) |
| ngay_den_han | Date | NOT NULL | — | Ngày đến hạn thanh toán |
| ngay_thanh_toan | Date | — | — | Ngày thực tế thanh toán |
| phuong_thuc | String(20) | NOT NULL | — | Phương thức thanh toán: tien_mat, chuyen_khoan |
| so_giao_dich | String(50) | — | — | Số giao dịch (nếu chuyển khoản) |
| trang_thai | Enum | NOT NULL | CHUA_THANH_TOAN | Trạng thái: DA_THANH_TOAN, CHUA_THANH_TOAN, QUA_HAN |
| phi_phat | Float | NOT NULL | 0 | Phí phạt trễ hạn |
| ghi_chu | Text | — | — | Ghi chú thêm về khoản thanh toán |
| nguoi_thu | String(100) | — | — | Người thu tiền |

Khi một hợp đồng mới được tạo, hệ thống tự động tạo lịch thanh toán định kỳ dựa trên phương thức thanh toán của hợp đồng (hàng tháng, hàng quý, hàng năm hoặc một lần). Các khoản thanh toán quá hạn được tự động phát hiện và đánh dấu dựa trên ngày hiện tại so với ngày đến hạn. Mã thanh toán được tạo tự động theo định dạng `{MaHopDong}-TT` + 3 chữ số, ví dụ: `HD202604001-TT001`.

---

## 11. Bảng nhan_vien (Nhân viên)

Bảng `nhan_vien` lưu trữ thông tin về nhân viên (người dùng) của hệ thống. Mỗi nhân viên có một tài khoản đăng nhập và mật khẩu được mã hóa. Bảng này có quan hệ một-nhiều với bảng `system_log` (một nhân viên có thể tạo nhiều bản ghi nhật ký) và một-nhiều với bảng `bao_cao` (một nhân viên có thể tạo nhiều báo cáo).

Các cột của bảng nhan_vien:

| Tên cột | Kiểu dữ liệu | Ràng buộc | Giá trị mặc định | Mô tả |
|---|---|---|---|---|
| ma_nhan_vien | String(20) | PRIMARY KEY | — | Mã nhân viên duy nhất, định dạng NVYYYYMMxxx |
| ho_ten | String(200) | NOT NULL | — | Họ tên nhân viên |
| email | String(100) | NOT NULL, UNIQUE | — | Địa chỉ email, không được trùng |
| so_dien_thoai | String(20) | — | — | Số điện thoại |
| vai_tro | Enum | NOT NULL | — | Vai trò: QUAN_TRI, KINH_DOANH, KHO, KE_TOAN |
| tai_khoan | String(50) | NOT NULL, UNIQUE | — | Tên đăng nhập, không được trùng |
| mat_khau | String(255) | NOT NULL | — | Mật khẩu đã được mã hóa bằng bcrypt (12 rounds) |
| trang_thai | Enum | NOT NULL | HOAT_DONG | Trạng thái: HOAT_DONG, NGUNG_HOAT_DONG |
| lan_dang_nhap_cuoi | String(50) | — | — | Thời điểm đăng nhập gần nhất |

Mật khẩu được bảo vệ bằng thuật toán bcrypt với cost factor là 12, đảm bảo an toàn ngay cả khi cơ sở dữ liệu bị lộ. Hệ thống hỗ trợ bốn vai trò với các quyền hạn khác nhau: Quản trị (toàn quyền), Kinh doanh (quản lý khách hàng, hợp đồng, báo cáo), Kho (quản lý kho, vị trí, hàng hóa), Kế toán (quản lý thanh toán, xem báo cáo). Nhân viên bị vô hiệu hóa (NGUNG_HOAT_DONG) sẽ không thể đăng nhập vào hệ thống.

---

## 12. Bảng system_log (Nhật ký hệ thống)

Bảng `system_log` lưu trữ nhật ký chi tiết các thao tác quan trọng trong hệ thống phục vụ mục đích kiểm toán và truy vết. Mỗi bản ghi log ghi lại hành động, thời gian, nhân viên thực hiện, bản ghi bị tác động và giá trị dữ liệu trước/sau khi thay đổi.

Các cột của bảng system_log:

| Tên cột | Kiểu dữ liệu | Ràng buộc | Giá trị mặc định | Mô tả |
|---|---|---|---|---|
| ma_log | Integer | PRIMARY KEY, AUTO INCREMENT | — | Mã log tự động tăng |
| ma_nhan_vien | String(20) | FOREIGN KEY → nhan_vien(ma_nhan_vien), ON DELETE SET NULL | — | Mã nhân viên thực hiện hành động |
| thoi_gian | DateTime | NOT NULL | — | Thời điểm xảy ra hành động |
| hanh_dong | Enum | NOT NULL | — | Hành động: THEM, SUA, XOA, DANG_NHAP, DANG_XUAT |
| ban_ghi | String(100) | NOT NULL | — | Tên bảng và mã bản ghi bị tác động |
| gia_tri_cu | Text | — | — | Giá trị cũ trước khi thay đổi (lưu dưới dạng JSON) |
| gia_tri_moi | Text | — | — | Giá trị mới sau khi thay đổi (lưu dưới dạng JSON) |
| ip_address | String(45) | — | — | Địa chỉ IP của thiết bị thực hiện hành động |
| ghi_chu | Text | — | — | Ghi chú thêm về hành động |

Bảng này ghi lại tất cả các thao tác thêm, sửa, xóa dữ liệu cũng như các sự kiện đăng nhập và đăng xuất. Các trường gia_tri_cu và gia_tri_moi lưu trữ dữ liệu dưới định dạng JSON, cho phép khôi phục hoặc so sánh dữ liệu khi cần thiết. Ràng buộc `ON DELETE SET NULL` đảm bảo log vẫn được giữ lại ngay cả khi nhân viên bị xóa khỏi hệ thống.

---

## 13. Bảng bao_cao (Báo cáo)

Bảng `bao_cao` lưu trữ thông tin về các báo cáo đã được tạo trong hệ thống, bao gồm báo cáo doanh thu, báo cáo tỷ lệ lấp đầy kho, báo cáo khách hàng và các loại báo cáo khác.

Các cột của bảng bao_cao:

| Tên cột | Kiểu dữ liệu | Ràng buộc | Giá trị mặc định | Mô tả |
|---|---|---|---|---|
| ma_bao_cao | String(30) | PRIMARY KEY | — | Mã báo cáo duy nhất |
| nguoi_tao | String(20) | FOREIGN KEY → nhan_vien(ma_nhan_vien), ON DELETE SET NULL | — | Mã nhân viên tạo báo cáo |
| loai_bao_cao | String(50) | NOT NULL | — | Loại báo cáo (doanh_thu, ton_kho, khach_hang, ...) |
| ngay_bat_dau | Date | NOT NULL | — | Ngày bắt đầu của khoảng thời gian báo cáo |
| ngay_ket_thuc | Date | NOT NULL | — | Ngày kết thúc của khoảng thời gian báo cáo |
| du_lieu | Text | — | — | Dữ liệu báo cáo (lưu dưới dạng JSON) |
| file_path | String(500) | — | — | Đường dẫn đến file báo cáo đã xuất (PDF/Excel) |
| trang_thai | String(20) | NOT NULL | hoan_thanh | Trạng thái: hoan_thanh, dang_xu_ly, that_bai |
| ghi_chu | Text | — | — | Ghi chú về báo cáo |

Bảng này cho phép lưu trữ lịch sử các báo cáo đã tạo, giúp người dùng có thể xem lại hoặc tải xuống các báo cáo trước đây mà không cần phải tạo lại từ đầu. Trường du_lieu lưu dữ liệu báo cáo dưới dạng JSON để có thể tái sử dụng mà không cần truy vấn lại cơ sở dữ liệu.

---

## 14. Các chỉ mục (Indexes)

Để tối ưu hiệu năng truy vấn, hệ thống định nghĩa hơn 20 chỉ mục trên các cột thường xuyên được sử dụng trong tìm kiếm và lọc dữ liệu. Các chỉ mục được tạo tự động khi khởi tạo cơ sở dữ liệu thông qua hàm `create_indexes()` trong `src/data/database.py`. Dưới đây là danh sách các chỉ mục theo từng bảng:

Bảng khach_hang:

| Tên chỉ mục | Cột | Mục đích |
|---|---|---|
| idx_khach_hang_email | email | Tìm kiếm khách hàng theo email |
| idx_khach_hang_so_dien_thoai | so_dien_thoai | Tìm kiếm khách hàng theo số điện thoại |
| idx_khach_hang_ho_ten | ho_ten | Tìm kiếm khách hàng theo tên |
| idx_khach_hang_trang_thai | trang_thai | Lọc khách hàng theo trạng thái |

Bảng kho:

| Tên chỉ mục | Cột | Mục đích |
|---|---|---|
| idx_kho_ten_kho | ten_kho | Tìm kiếm kho theo tên |
| idx_kho_trang_thai | trang_thai | Lọc kho theo trạng thái |

Bảng vi_tri:

| Tên chỉ mục | Cột | Mục đích |
|---|---|---|
| idx_vi_tri_ma_kho | ma_kho | Truy vấn vị trí theo kho |
| idx_vi_tri_trang_thai | trang_thai | Lọc vị trí theo trạng thái |

Bảng hop_dong:

| Tên chỉ mục | Cột | Mục đích |
|---|---|---|
| idx_hop_dong_ma_khach_hang | ma_khach_hang | Truy vấn hợp đồng theo khách hàng |
| idx_hop_dong_ma_vi_tri | ma_vi_tri | Truy vấn hợp đồng theo vị trí |
| idx_hop_dong_trang_thai | trang_thai | Lọc hợp đồng theo trạng thái |
| idx_hop_dong_ngay_bat_dau | ngay_bat_dau | Lọc hợp đồng theo ngày bắt đầu |
| idx_hop_dong_ngay_ket_thuc | ngay_ket_thuc | Lọc hợp đồng theo ngày kết thúc |

Bảng hang_hoa:

| Tên chỉ mục | Cột | Mục đích |
|---|---|---|
| idx_hang_hoa_ma_hop_dong | ma_hop_dong | Truy vấn hàng hóa theo hợp đồng |
| idx_hang_hoa_trang_thai | trang_thai | Lọc hàng hóa theo trạng thái |

Bảng thanh_toan:

| Tên chỉ mục | Cột | Mục đích |
|---|---|---|
| idx_thanh_toan_ma_hop_dong | ma_hop_dong | Truy vấn thanh toán theo hợp đồng |
| idx_thanh_toan_trang_thai | trang_thai | Lọc thanh toán theo trạng thái |

Bảng nhan_vien:

| Tên chỉ mục | Cột | Mục đích |
|---|---|---|
| idx_nhan_vien_tai_khoan | tai_khoan | Tra cứu nhân viên theo tài khoản |
| idx_nhan_vien_email | email | Tìm kiếm nhân viên theo email |

Bảng system_log:

| Tên chỉ mục | Cột | Mục đích |
|---|---|---|
| idx_system_log_ma_nhan_vien | ma_nhan_vien | Truy vấn log theo nhân viên |
| idx_system_log_thoi_gian | thoi_gian | Lọc log theo thời gian |
| idx_system_log_hanh_dong | hanh_dong | Lọc log theo hành động |

Bảng bao_cao:

| Tên chỉ mục | Cột | Mục đích |
|---|---|---|
| idx_bao_cao_nguoi_tao | nguoi_tao | Truy vấn báo cáo theo người tạo |
| idx_bao_cao_loai | loai_bao_cao | Lọc báo cáo theo loại |

---

## 15. Các view (Khung nhìn)

Hệ thống định nghĩa ba khung nhìn (view) để phục vụ các báo cáo thường xuyên, giúp giảm thiểu việc viết lại các truy vấn phức tạp. Các view này được tạo tự động khi khởi tạo cơ sở dữ liệu thông qua hàm `create_views()` trong `src/data/database.py`.

View thứ nhất là `v_hop_dong_sap_het_han`, có nhiệm vụ xác định các hợp đồng sắp hết hạn trong vòng 30 ngày tới. View này truy vấn từ bảng `hop_dong` kết hợp với bảng `khach_hang` và `vi_tri`, lọc các hợp đồng có trạng thái `HIEU_LUC` và ngày kết thúc nằm trong khoảng từ ngày hiện tại đến ngày hiện tại cộng thêm 30 ngày. Kết quả trả về bao gồm mã hợp đồng, tên khách hàng, mã vị trí, ngày kết thúc và số ngày còn lại.

View thứ hai là `v_cong_no_chua_thanh_toan`, có nhiệm vụ theo dõi các khoản công nợ chưa được thanh toán. View này truy vấn từ bảng `thanh_toan` kết hợp với bảng `hop_dong` và `khach_hang`, lọc các khoản thanh toán có trạng thái `CHUA_THANH_TOAN` hoặc `QUA_HAN`. Kết quả trả về bao gồm mã hợp đồng, tên khách hàng, số tiền còn nợ, ngày đến hạn và trạng thái quá hạn.

View thứ ba là `v_ty_le_lap_day_kho`, có nhiệm vụ tính toán tỷ lệ lấp đầy của từng kho. View này truy vấn từ bảng `kho` kết hợp với bảng `vi_tri`, tính số lượng vị trí đã thuê so với tổng số vị trí trong mỗi kho. Kết quả trả về bao gồm mã kho, tên kho, tổng số vị trí, số vị trí đã thuê và tỷ lệ lấp đầy phần trăm.

---

## 16. Mối quan hệ giữa các bảng

Các bảng trong cơ sở dữ liệu được liên kết với nhau thông qua các khóa ngoại (foreign keys) và các quan hệ (relationships) được định nghĩa trong SQLAlchemy ORM. Dưới đây là mô tả chi tiết các mối quan hệ giữa các bảng:

| Bảng 1 | Bảng 2 | Loại quan hệ | Khóa ngoại | Mô tả |
|---|---|---|---|---|
| khach_hang | hop_dong | Một-nhiều | hop_dong.ma_khach_hang → khach_hang.ma_khach_hang | Một khách hàng có thể có nhiều hợp đồng. Cascade: all, delete-orphan |
| kho | vi_tri | Một-nhiều | vi_tri.ma_kho → kho.ma_kho | Một kho có thể có nhiều vị trí lưu trữ. Cascade: all, delete-orphan |
| vi_tri | hop_dong | Một-một | hop_dong.ma_vi_tri → vi_tri.ma_vi_tri | Một vị trí chỉ được thuê bởi một hợp đồng tại một thời điểm |
| hop_dong | hang_hoa | Một-nhiều | hang_hoa.ma_hop_dong → hop_dong.ma_hop_dong | Một hợp đồng có thể chứa nhiều mặt hàng. Cascade: all, delete-orphan |
| hop_dong | thanh_toan | Một-nhiều | thanh_toan.ma_hop_dong → hop_dong.ma_hop_dong | Một hợp đồng có thể có nhiều khoản thanh toán |
| nhan_vien | system_log | Một-nhiều | system_log.ma_nhan_vien → nhan_vien.ma_nhan_vien | Một nhân viên có thể tạo nhiều bản ghi nhật ký. ON DELETE SET NULL |
| nhan_vien | bao_cao | Một-nhiều | bao_cao.nguoi_tao → nhan_vien.ma_nhan_vien | Một nhân viên có thể tạo nhiều báo cáo. ON DELETE SET NULL |

Tổng quan các mối quan hệ có thể được hình dung như sau: Khách hàng và Kho là hai thực thể độc lập, được kết nối thông qua bảng Hợp đồng (hop_dong). Mỗi hợp đồng gắn một khách hàng với một vị trí trong kho. Từ hợp đồng, các nghiệp vụ phát sinh bao gồm Hàng hóa (hang_hoa) được lưu trữ và Thanh toán (thanh_toan) được thực hiện định kỳ. Nhân viên (nhan_vien) là người vận hành hệ thống, thực hiện các thao tác được ghi lại trong Nhật ký hệ thống (system_log) và tạo các Báo cáo (bao_cao). Loại hàng (loai_hang) là bảng danh mục độc lập, hỗ trợ phân loại hàng hóa.

---

## Tổng kết

Cơ sở dữ liệu của hệ thống Quản Lý Dịch Vụ Cho Thuê Kho Lưu Trữ Hàng Hóa bao gồm 9 bảng chính, 3 khung nhìn và hơn 20 chỉ mục, được thiết kế theo chuẩn 3NF với các ràng buộc toàn vẹn dữ liệu chặt chẽ. Tất cả các bảng đều kế thừa từ BaseModel, tự động quản lý ngày tạo và ngày cập nhật. Các trạng thái được chuẩn hóa thông qua 11 kiểu liệt kê tập trung trong file enums.py. Hệ thống khóa ngoại và các quan hệ ORM đảm bảo tính nhất quán của dữ liệu, với các ràng buộc cascade phù hợp cho từng mối quan hệ. Các chỉ mục được tối ưu cho các truy vấn thường xuyên, và các khung nhìn cung cấp giao diện truy vấn nhanh cho các báo cáo quan trọng.
