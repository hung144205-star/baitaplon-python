#!/usr/bin/env python3
"""Script to generate YEU_CAU_CHUC_NANG.md documentation file."""

content = r"""# Mô Tả Các Chức Năng Của Chương Trình

**Đề tài:** Quản Lý Dịch Vụ Cho Thuê Kho Lưu Trữ Hàng Hóa
**Nhóm thực hiện:** Nhóm 12 - Lập trình Python
**Ngày cập nhật:** 10/05/2026

---

## Mục lục

1. [Kiến trúc tổng quan hệ thống](#1-kiến-trúc-tổng-quan-hệ-thống)
2. [Chức năng Đăng nhập và Bảo mật](#2-chức-năng-đăng-nhập-và-bảo-mật)
3. [Chức năng Dashboard tổng quan](#3-chức-năng-dashboard-tổng-quan)
4. [Chức năng Quản lý Khách hàng](#4-chức-năng-quản-lý-khách-hàng)
5. [Chức năng Quản lý Kho](#5-chức-năng-quản-lý-kho)
6. [Chức năng Quản lý Vị trí lưu trữ](#6-chức-năng-quản-lý-vị-trí-lưu-trữ)
7. [Chức năng Quản lý Hợp đồng](#7-chức-năng-quản-lý-hợp-đồng)
8. [Chức năng Quản lý Hàng hóa](#8-chức-năng-quản-lý-hàng-hóa)
9. [Chức năng Quản lý Thanh toán](#9-chức-năng-quản-lý-thanh-toán)
10. [Chức năng Báo cáo và Thống kê](#10-chức-năng-báo-cáo-và-thống-kê)
11. [Chức năng Quản lý Người dùng](#11-chức-năng-quản-lý-người-dùng)
12. [Chức năng Cài đặt Hệ thống](#12-chức-năng-cài-đặt-hệ-thống)
13. [Chức năng Trợ giúp và Hướng dẫn](#13-chức-năng-trợ-giúp-và-hướng-dẫn)
14. [Chức năng Xuất dữ liệu](#14-chức-năng-xuất-dữ-liệu)
15. [Chức năng Cảnh báo Thông minh](#15-chức-năng-cảnh-báo-thông-minh)
16. [Sơ đồ Quy trình Nghiệp vụ Tổng thể](#16-sơ-đồ-quy-trình-nghiệp-vụ-tổng-thể)

---

## 1. Kiến trúc tổng quan hệ thống

Chương trình được thiết kế theo kiến trúc ba lớp (three-tier architecture) bao gồm tầng giao diện (Presentation Layer), tầng nghiệp vụ (Business Logic Layer) và tầng dữ liệu (Data Layer). Tầng giao diện được xây dựng bằng PyQt6 với các view, form, dialog và wizard cho phép người dùng tương tác trực quan. Tầng nghiệp vụ chứa các service thực hiện xử lý logic, kiểm tra ràng buộc và điều phối dữ liệu. Tầng dữ liệu sử dụng SQLAlchemy ORM kết nối với cơ sở dữ liệu SQLite, đồng thời áp dụng Repository Pattern để tách biệt logic truy vấn.

Sơ đồ kiến trúc hệ thống được mô tả như sau:

```
                    +-----------------------------------------------------------+
                    |         Tầng Giao diện (GUI Layer)                        |
                    |   PyQt6: Views, Forms, Dialogs, Wizards,                 |
                    |   Widgets, Navigation, Stylesheets (QSS)                  |
                    +--------------------------+--------------------------------+
                                               |
                    +--------------------------v--------------------------------+
                    |        Tầng Nghiệp vụ (Service Layer)                     |
                    |  AuthService, KhachHangService, KhoService,               |
                    |  HopDongService, HangHoaService,                          |
                    |  ThanhToanService, ReportService,                         |
                    |  PDFGenerationService, UserService,                       |
                    |  InventoryService, AlertService                           |
                    +--------------------------+--------------------------------+
                                               |
          +------------------------------------+------------------------------------+
          |                                    |                                    |
+---------v----------+   +--------------------v------+   +------------------------v--+
|  Tầng Dữ liệu      |   |  Tầng Xuất báo cáo       |   |  Tầng Tiện ích           |
|  SQLAlchemy ORM   |   |  ReportLab (PDF)          |   |  Validators              |
|  SQLite Database  |   |  Pandas + OpenPyXL        |   |  Formatters              |
|  Repository       |   |  (Excel)                  |   |  Helpers                 |
|  Pattern, Migrate |   |                           |   |  Export Service          |
+--------------------+   +---------------------------+   +--------------------------+
```

Chương trình bao gồm chín module chức năng chính được truy cập thông qua thanh điều hướng: Dashboard tổng quan, Quản lý Khách hàng, Quản lý Kho, Quản lý Vị trí, Quản lý Hợp đồng, Quản lý Hàng hóa, Quản lý Thanh toán, Báo cáo Thống kê và Cài đặt Hệ thống. Mỗi module được triển khai dưới dạng một view riêng biệt trong thư mục src/gui/views/, kết nối với một hoặc nhiều service trong thư mục src/services/ để xử lý nghiệp vụ.

---

## 2. Chức năng Đăng nhập và Bảo mật

Chức năng đăng nhập được triển khai tại file src/gui/views/auth/login_view.py kết hợp với src/services/auth/auth_service.py. Khi người dùng khởi động chương trình, màn hình đăng nhập xuất hiện với hai trường nhập liệu là Tên đăng nhập và Mật khẩu, cùng với hộp kiểm Ghi nhớ đăng nhập. Người dùng nhập thông tin xác thực và nhấn nút Đăng nhập hoặc phím Enter để gửi yêu cầu.

Luồng xử lý đăng nhập được mô tả như sau:

```
Người dùng nhập tên đăng nhập và mật khẩu
                    |
                    v
    Kiểm tra dữ liệu đầu vào không được để trống
                    |
                    v
    AuthService.login(username, password) được gọi
                    |
                    +--- Kiểm tra tài khoản tồn tại và đang hoạt động
                    |       | (nếu sai)
                    |       v
                    |  Hiển thị thông báo lỗi qua MessageDialog
                    |
                    +--- Kiểm tra số lần đăng nhập sai (tối đa 5 lần)
                    |       | (nếu quá 5 lần)
                    |       v
                    |  Khóa tài khoản 30 phút, hiển thị cảnh báo
                    |
                    +--- Xác minh mật khẩu bằng bcrypt
                    |       | (nếu sai)
                    |       v
                    |  Tăng biến đếm số lần đăng nhập sai
                    |
                    +--- Đăng nhập thành công
                            |
                            v
                    Tạo session token, ghi nhận thời gian đăng nhập
                            |
                            v
                    Phát tín hiệu login_successful, chuyển đến MainWindow
```

Hệ thống hỗ trợ cơ chế Ghi nhớ đăng nhập (Remember Me): nếu người dùng chọn hộp kiểm này, tên đăng nhập sẽ được lưu vào tệp JSON tại thư mục ẩn ~/.baitaplon/remember_me.json và tự động điền vào ô nhập liệu ở lần khởi động sau.

Tài khoản mặc định của hệ thống là admin với mật khẩu admin123. Chức năng đổi mật khẩu được thực hiện thông qua ChangePasswordDialog tại src/gui/dialogs/change_password_dialog.py, yêu cầu người dùng nhập mật khẩu cũ, mật khẩu mới và xác nhận mật khẩu mới.

---

## 3. Chức năng Dashboard tổng quan

Dashboard là màn hình đầu tiên hiển thị sau khi đăng nhập, được triển khai tại file src/gui/views/dashboard_view.py kết hợp với src/gui/widgets/charts.py để vẽ biểu đồ. Dashboard cung cấp cái nhìn tổng quan về toàn bộ hệ thống quản lý kho thông qua các chỉ số và biểu đồ trực quan.

Các thành phần hiển thị trên Dashboard bao gồm:

| Thành phan | Mo ta | Du lieu hien thi |
|---|---|---|
| Bon chi so tong quan | Bon o thong tin nhanh o dau trang | Tong so kho, So kho dang hoat dong, Tong so vi tri luu tru, So vi tri trong |
| Thanh ty le lap day | Thanh tien trinh hien thi ty le lap day trung binh | Phan tram lap day (mau xanh neu duoi 50%, mau cam neu 50-75%, mau do neu tren 75%) |
| Bieu do tron (Pie Chart) | Thong ke phan bo trang thai cac kho | Ty le kho Hoat dong, Bao tri, Ngung hoat dong |
| Bieu do cot (Bar Chart) | So sanh ty le lap day giua cac kho | Tung kho voi phan tram lap day tuong ung |
| Bang thong ke chi tiet kho | Danh sach cac kho kem thong tin | Ten kho, Dia chi, Dien tich, Suc chua, Ty le lap day |
| Khu vuc canh bao | Canh bao cac kho qua tai | Ten kho co ty le lap day tren 90%, kem nut Xem chi tiet |

Dashboard co co che tu dong lam moi du lieu sau moi 30 giay thong qua QTimer, dam bao nguoi dung luon thay thong tin moi nhat ma khong can thao tac thu cong.

---

## 4. Chuc nang Quan ly Khach hang

Module Quan ly Khach hang duoc trien khai tai src/gui/views/khach_hang_view.py va src/gui/views/khach_hang_detail_view.py, ket noi voi src/services/khach_hang_service.py. Module nay cho phep quan ly toan bo thong tin khach hang cua he thong.

Chuc nang chinh cua module Quan ly Khach hang:

| Chuc nang | Mo ta | Phuong thuc xu ly |
|---|---|---|
| Xem danh sach khach hang | Hien thi bang du lieu voi cac cot: Ma KH, Ho ten, Loai, SDT, Email, Trang thai | load_data() tu KhachHangService.get_all() |
| Them khach hang moi | Mo form nhap lieu voi cac truong: Ho ten, Loai khach (Ca nhan/Doanh nghiep), SDT, Email, Dia chi, Ma so thue | KhachHangForm + KhachHangService.create() |
| Sua thong tin khach hang | Mo form voi du lieu da co, cho phep cap nhat | KhachHangForm + KhachHangService.update() |
| Xoa khach hang | Xoa mem (soft-delete) voi xac nhan tu nguoi dung | KhachHangService.delete() |
| Xem chi tiet khach hang | Giao dien tab gom 4 tab: Thong tin, Hop dong, Thanh toan, Lich su | KhachHangDetailView |
| Tim kiem khach hang | Tim kiem theo ten, so dien thoai hoac email | SearchBox + KhachHangService.search() |
| Loc danh sach | Loc theo Loai khach (Ca nhan/Doanh nghiep) va Trang thai (Hoat dong/Tam khoa) | _apply_filters() |
| Xuat Excel | Xuat danh sach khach hang ra file Excel | _on_export_clicked() |

Moi khach hang co the la Ca nhan hoac Doanh nghiep, duoc phan biet qua truong loai_khach trong co so du lieu. Khi xem chi tiet mot khach hang, nguoi dung co the chuyen qua lai giua cac tab de xem thong tin co ban, danh sach hop dong da ky, lich su thanh toan va lich su giao dich.

---

## 5. Chuc nang Quan ly Kho

Module Quan ly Kho duoc trien khai tai src/gui/views/kho_view.py ket noi voi src/services/kho_service.py. Module nay quan ly thong tin cac kho hang trong he thong, bao gom dien tich, suc chua va ty le lap day.

Bang du lieu kho hien thi cac thong tin: Ma kho, Ten kho, Dia chi, Dien tich (m2), Suc chua (m3), Dien tich da su dung, Ty le lap day (%), So vi tri va Trang thai.

Cac chuc nang cua module Quan ly Kho:

| Chuc nang | Mo ta |
|---|---|
| Them kho moi | Mo KhoForm de nhap thong tin kho (ten, dia chi, dien tich, suc chua) |
| Sua thong tin kho | Cap nhat thong tin kho da chon thong qua KhoForm |
| Xoa kho | Xoa kho voi xac nhan tu nguoi dung, kiem tra rang buoc du lieu |
| Xem danh sach kho | Hien thi toan bo kho trong bang du lieu |
| Thong ke kho | Thanh thong ke hien thi Tong so kho, So kho Hoat dong, Ty le lap day trung binh |
| Tinh ty le lap day tu dong | He thong tu dong tinh phan tram dien tich da su dung so voi tong dien tich |
| Tim kiem kho | Tim kiem theo ten, ma hoac dia chi |
| Loc theo trang thai | Loc danh sach theo cac trang thai: Tat ca, Hoat dong, Bao tri, Ngung |
| Xuat Excel | Xuat danh sach kho ra file Excel |

Quy trinh them mot kho moi dien ra nhu sau:

```
Nguoi dung nhan nut "+ Them kho"
              |
              v
KhoForm duoc hien thi voi cac truong nhap lieu
(Ten kho, Dia chi, Dien tich, Suc chua, Ghi chu)
              |
              v
Kiem tra tinh hop le cua du lieu (Validators)
Ten kho khong duoc de trong
Dien tich va suc chua phai la so duong
              | (du lieu hop le)
              v
KhoService.create(data) duoc goi
              |
              v
Du lieu duoc luu vao co so du lieu qua SQLAlchemy ORM
              |
              v
Bang du lieu duoc lam moi, thong bao thanh cong
```

---

## 6. Chuc nang Quan ly Vi tri luu tru

Module Quan ly Vi tri duoc trien khai tai src/gui/views/vi_tri_view.py ket noi voi src/services/vi_tri_service.py. Module nay quan ly cac vi tri luu tru ben trong moi kho, to chuc theo cau truc ba cap: Khu vuc (Zone), Hang (Rack) va Tang (Shelf).

Bang du lieu vi tri hien thi cac thong tin: Ma vi tri, Khu vuc, Hang, Tang, Dien tich, Gia thue (theo thang), Trang thai (Trong/Da thue/Bao tri).

Cac chuc nang cua module Quan ly Vi tri:

| Chuc nang | Mo ta |
|---|---|
| Them vi tri moi | Mo ViTriForm de nhap thong tin vi tri trong mot kho cu the |
| Sua thong tin vi tri | Cap nhat thong tin vi tri da chon |
| Xoa vi tri | Xoa vi tri voi xac nhan tu nguoi dung |
| Xem danh sach vi tri | Hien thi danh sach vi tri cua kho duoc chon |
| Thong ke vi tri | Hien thi Tong vi tri, So vi tri trong, So vi tri da thue, Ty le trong |
| Loc theo trang thai | Loc vi tri theo Trong, Da thue hoac Bao tri |
| Tim kiem vi tri | Tim kiem theo ma vi tri hoac khu vuc |
| Xuat Excel | Xuat danh sach vi tri ra file Excel |

Khi nguoi dung chon mot kho tu danh sach, cac vi tri thuoc kho do se duoc tu dong tai va hien thi. Moi vi tri co mot gia thue rieng, duoc su dung de tinh toan chi phi trong hop dong.

---

## 7. Chuc nang Quan ly Hop dong

Module Quan ly Hop dong la mot trong nhung module phuc tap nhat, duoc trien khai tai src/gui/views/hop_dong_view.py, src/gui/views/hop_dong_detail_view.py, src/gui/forms/hop_dong_form.py, src/gui/wizards/renewal_wizard.py va src/gui/wizards/termination_wizard.py, ket noi voi src/services/hop_dong_service.py.

Hop dong thue kho co cac trang thai: Hieu luc (Dang hoat dong), Het han, Cham dut va Gia han. He thong tu dong theo doi thoi han hop dong va dua ra canh bao khi hop dong sap het han.

Cac chuc nang chinh cua module Quan ly Hop dong:

| Chuc nang | Mo ta |
|---|---|
| Tao hop dong moi | Mo HopDongForm cho phep chon khach hang, vi tri kho, nhap ngay bat dau, ngay ket thuc, gia thue, tien coc va phuong thuc thanh toan |
| Sua hop dong | Cap nhat thong tin hop dong |
| Xoa hop dong | Xoa hop dong voi xac nhan |
| Xem chi tiet hop dong | Giao dien 4 tab: Thong tin, Hang hoa, Thanh toan, Lich su |
| Gia han hop dong | Wizard 3 buoc: Xem thong tin hien tai + Nhap so thang gia han va gia moi + Xac nhan |
| Cham dut hop dong | Wizard 3 buoc: Chon ly do + Tinh tien phat + Xac nhan |
| Cap nhat trang thai | Thay doi trang thai hop dong (co xu ly rieng cho cham dut voi ly do) |
| Tim kiem hop dong | Tim kiem theo ma hop dong, ten khach hang hoac vi tri |
| Loc hop dong | Loc theo trang thai, khoang thoi gian |
| Xuat Excel | Xuat danh sach hop dong ra Excel |
| Xuat PDF | Xuat tung hop dong ra file PDF |

Quy trinh tao hop dong moi duoc thuc hien nhu sau:

```
Nguoi dung nhan "+ Tao Hop dong"
              |
              v
HopDongForm duoc hien thi
Buoc 1: Chon Khach hang (QComboBox tim kiem)
Buoc 2: Chon Vi tri kho (QListWidget hien thi vi tri trong)
Buoc 3: Nhap Ngay bat dau, Ngay ket thuc (QDateEdit)
Buoc 4: Nhap Gia thue thang, Tien coc (QDoubleSpinBox)
Buoc 5: Chon Phuong thuc thanh toan (QComboBox)
              |
              v
Kiem tra tinh hop le (Validators)
Ngay ket thuc phai sau ngay bat dau
Gia thue va tien coc phai la so duong
Vi tri phai con trong
              | (du lieu hop le)
              v
HopDongService.create(data) duoc goi
Tao ma hop dong tu dong
Cap nhat trang thai vi tri thanh "Da thue"
Tao lich thanh toan dinh ky tu dong
              |
              v
Luu vao co so du lieu, lam moi bang du lieu
```

Quy trinh gia han hop dong duoc thuc hien qua RenewalWizard voi ba trang:

```
Trang 1 (RenewalIntroPage): Hien thi thong tin hop dong hien tai
Ma hop dong, Ten khach hang, Vi tri
Ngay bat dau, Ngay ket thuc, Gia thue hien tai, Trang thai
              |
              v
Trang 2 (RenewalTermsPage): Nhap dieu khoan gia han moi
So thang gia han (mac dinh 12, tu dong tinh ngay ket thuc moi)
Gia thue moi (tu dong tinh tong tien thue)
              |
              v
Trang 3 (RenewalConfirmPage): Xac nhan thong tin
Tom tat cac thay doi: Ngay ket thuc cu sang moi, Gia thue cu sang moi
Nhan "Hoan tat" de luu
              |
              v
HopDongService.renew() duoc goi
Cap nhat ngay ket thuc va gia thue moi
Ghi nhan lich su gia han
```

Quy trinh cham dut hop dong duoc thuc hien qua TerminationWizard voi ba trang:

```
Trang 1 (TerminationReasonPage): Chon ly do cham dut
Khach hang yeu cau / Vi pham hop dong / Khong thanh toan / Ly do khac
Nhap ghi chu bo sung
              |
              v
Trang 2 (TerminationPenaltyPage): Tinh tien phat
Chon muc phat (theo thang tien thue hoac % tien coc)
He thong tu dong tinh so tien phat va tien hoan lai
              |
              v
Trang 3 (TerminationConfirmPage): Xac nhan
Tom tat ly do, tien phat, tien hoan lai
Canh bao hanh dong khong the hoan tac
Nhan "Cham dut" de hoan tat
              |
              v
HopDongService.terminate() duoc goi
Cap nhat trang thai hop dong thanh "Cham dut"
Cap nhat trang thai vi tri thanh "Trong"
Ghi nhan lich su cham dut
```

---

## 8. Chuc nang Quan ly Hang hoa

Module Quan ly Hang hoa duoc trien khai tai src/gui/views/hang_hoa_view.py ket noi voi src/services/hang_hoa_service.py. Module nay quan ly viec nhap, xuat va theo doi ton kho cua hang hoa trong cac hop dong thue.

Bang du lieu hang hoa hien thi cac thong tin: Ma hang, Ten hang, Loai hang, So luong, Don vi tinh, Gia tri, Trang thai (Trong kho/Da xuat), Hop dong lien quan.

Cac chuc nang cua module Quan ly Hang hoa:

| Chuc nang | Mo ta |
|---|---|
| Them hang hoa moi | Mo HangHoaForm de nhap thong tin hang hoa (ten, loai, so luong, don vi tinh, gia tri, hop dong) |
| Nhap hang vao kho | Nhap hang hoa vao vi tri luu tru cu the |
| Xuat hang khoi kho | Xuat hang hoa voi ghi chu ly do xuat |
| Sua thong tin hang hoa | Cap nhat thong tin hang hoa |
| Xoa hang hoa | Xoa mat hang voi xac nhan |
| Quan ly loai hang | Them, sua, xoa danh muc loai hang thong qua LoaiHangForm |
| Cap nhat trang thai | Thay doi trang thai hang hoa (Trong kho/Da xuat) |
| Canh bao ton kho thap | Tu dong canh bao khi so luong hang duoi 10 |
| Thong ke hang hoa | Hien thi Tong so mat hang, Tong so luong trong kho, So luong sap het, Tong gia tri |
| Tim kiem hang hoa | Tim kiem theo ten hoac loai hang |
| Loc hang hoa | Loc theo Hop dong, Loai hang, Trang thai |
| Xuat Excel | Xuat danh sach hang hoa ra file Excel |

---

## 9. Chuc nang Quan ly Thanh toan

Module Quan ly Thanh toan duoc trien khai tai src/gui/views/thanh_toan_view.py ket noi voi src/services/thanh_toan_service.py. Module nay quan ly cac khoan thanh toan, cong no va lich su thanh toan cua khach hang theo hop dong.

Bang du lieu thanh toan hien thi cac thong tin: Ma thanh toan, Hop dong, Ky thanh toan, So tien, Ngay den han, Ngay thanh toan, Trang thai (Da thanh toan/Chua thanh toan/Qua han).

Cac chuc nang cua module Quan ly Thanh toan:

| Chuc nang | Mo ta |
|---|---|
| Tao thanh toan moi | Mo ThanhToanForm de tao phieu thanh toan cho hop dong |
| Sua thanh toan | Cap nhat thong tin thanh toan |
| Xoa thanh toan | Xoa phieu thanh toan voi xac nhan |
| Tu dong tao lich thanh toan | Khi tao hop dong moi, he thong tu dong tao cac ky thanh toan dinh ky |
| Mark qua han | Tu dong danh dau cac khoan thanh toan qua han dua tren ngay hien tai |
| Thong ke cong no | Hien thi Tong so hoa don, Tong tien da thanh toan, Tong tien con no (bao gom no qua han) |
| Tim kiem thanh toan | Tim kiem theo ma hop dong hoac ten khach hang |
| Loc thanh toan | Loc theo trang thai: Da thanh toan, Chua thanh toan, Qua han |
| Xuat Excel | Xuat danh sach thanh toan ra file Excel |

---

## 10. Chuc nang Bao cao va Thong ke

Module Bao cao duoc trien khai tai src/gui/views/bao_cao_view.py ket noi voi src/services/report_service.py va src/gui/widgets/charts.py. Module nay cung cap cac bao cao tong hop ve tinh hinh kinh doanh.

Cac thanh phan cua module Bao cao:

| Thanh phan | Mo ta |
|---|---|
| Bon chi so tom tat | Doanh thu thang hien tai, So hop dong dang hoat dong, So hop dong sap het han, Tong so khach hang |
| Bieu do tang truong doanh thu | Bieu do cot hien thi doanh thu theo tung thang trong nam |
| Danh sach hop dong gan day | 10 hop dong moi nhat, hien thi Ma KH, Ten KH, Ma HD, Ngay tao, Gia tri |
| Nut Tai lai du lieu | Lam moi toan bo so lieu bao cao |
| Xuat Excel | Xuat bao cao tom tat ra file Excel |

Ngoai ra, he thong con ho tro xuat bao cao PDF tong hop thong qua PDFGenerationService voi ba loai bao cao:

| Loai bao cao PDF | Noi dung |
|---|---|
| Hop dong thue kho | Thong tin hop dong, khach hang, vi tri, dieu khoan, chu ky |
| Hoa don thanh toan | Thong tin hoa don, danh sach dich vu, thue, tong thanh toan, thong tin ngan hang |
| Bao cao tong hop | So lieu khach hang, kho, hop dong, doanh thu, canh bao rui ro, khuyen nghi |

---

## 11. Chuc nang Quan ly Nguoi dung

Module Quan ly Nguoi dung duoc trien khai tai src/gui/views/users/user_view.py ket noi voi src/services/users/user_service.py. Module nay danh cho nguoi dung co quyen Quan tri de quan ly tai khoan nhan vien trong he thong.

Bang du lieu nguoi dung hien thi cac thong tin: Ma nhan vien, Ho ten, Email, So dien thoai, Vai tro (Quan tri/Kinh doanh/Kho/Ke toan), Trang thai (Hoat dong/Ngung hoat dong).

Cac chuc nang cua module Quan ly Nguoi dung:

| Chuc nang | Mo ta | Yeu cau quyen |
|---|---|---|
| Xem danh sach nguoi dung | Hien thi tat ca nhan vien trong he thong | Xem danh sach |
| Them nguoi dung moi | Mo UserForm de tao tai khoan nhan vien moi | create_user |
| Sua thong tin nguoi dung | Cap nhat thong tin va phan quyen nhan vien | edit_user |
| Xoa (vo hieu hoa) nguoi dung | Ngung hoat dong tai khoan nhan vien | delete_user |

He thong phan quyen duoc trien khai thong qua AuthorizationService voi ma tran quyen cho bon vai tro:

| Vai tro | Quyen han |
|---|---|
| Quan tri (admin) | Toan quyen tren tat ca cac chuc nang |
| Kinh doanh (manager) | Quan ly khach hang, hop dong, bao cao |
| Kho (staff) | Quan ly kho, vi tri, hang hoa, nhap xuat |
| Ke toan (guest) | Quan ly thanh toan, xem bao cao |

---

## 12. Chuc nang Cai dat He thong

Module Cai dat duoc trien khai tai src/gui/views/settings_view.py. Module nay cho phep nguoi dung tuy chinh cac thiet lap cua he thong thong qua giao dien dang the (card-based layout), duoc chia thanh bon nhom chuc nang:

| Nhom cai dat | Cac thiet lap |
|---|---|
| Hien thi | So muc tren moi trang bang, Bat/tat xac nhan khi xoa, Bat/tat goi y khi di chuot, Bat/tat tu dong lam moi |
| Thong bao | Bat/tat canh bao hang sap het, Bat/tat canh bao hop dong het han, So ngay canh bao truoc |
| Du lieu | Bat/tat tu dong sao luu, Duong dan thu muc sao luu |
| Tai khoan | Thong tin nguoi dung hien tai, Nut Doi mat khau |

Cac thao tac he thong bao gom Luu cai dat, Khoi phuc mac dinh va Doi mat khau. Luu cai dat ghi lai cac thiet lap hien tai cua nguoi dung. Khoi phuc mac dinh dat lai tat ca thiet lap ve gia tri mac dinh ban dau, co xac nhan truoc khi thuc hien. Doi mat khau mo ChangePasswordDialog cho phep nguoi dung thay doi mat khau dang nhap.

---

## 13. Chuc nang Tro giup va Huong dan

Module Tro giup duoc trien khai tai src/gui/views/help_view.py. Module nay cung cap tai lieu huong dan su dung phan mem ngay trong ung dung, duoc to chuc thanh ba tab.

Tab thu nhat mang ten "Huong dan su dung" cung cap huong dan chi tiet cho sau chuc nang chinh cua he thong: Dang nhap, Quan ly Khach hang, Quan ly Kho, Quan ly Hop dong, Nhap/Xuat Hang hoa va Thanh toan. Moi huong dan bao gom cac buoc thuc hien cu the va giai thich cac trang thai, thuat ngu lien quan.

Tab thu hai mang ten "Phim tat" hien thi danh sach cac phim tat de thao tac nhanh trong ung dung. Cac phim tat duoc phan loai thanh ba nhom: Dieu huong (Ctrl + chu cai de mo cac module), Thao tac tep/form (Ctrl + S de luu, Ctrl + F de tim kiem, Ctrl + N de tao moi), Thao tac bang (Enter de xem chi tiet, Delete de xoa, Escape de dong/huy).

Tab thu ba mang ten "Ve chung toi" cung cap thong tin gioi thieu ve phan mem bao gom muc dich phat trien, cac cong nghe su dung (Python, PyQt6, SQLAlchemy, SQLite, ReportLab) va danh sach thanh vien nhom phat trien.

---

## 14. Chuc nang Xuat du lieu

He thong ho tro hai dinh dang xuat du lieu chinh la PDF va Excel, duoc trien khai tai src/services/pdf/pdf_generation_service.py va src/utils/export_service.py.

Xuat du lieu ra PDF duoc thuc hien thong qua thu vien ReportLab voi kha nang ho tro font tieng Viet (uu tien DejaVu Sans, sau do den Arial va Tahoma). PDFGenerationService cung cap ba chuc nang chinh: xuat hop dong thue kho thanh file PDF chua thong tin hop dong, khach hang, vi tri va cac dieu khoan; xuat hoa don thanh toan thanh file PDF voi danh sach dich vu, thue va thong tin ngan hang; xuat bao cao tong hop thanh file PDF voi so lieu thong ke, canh bao rui ro va khuyen nghi. Tat ca cac file PDF duoc luu vao thu muc data/exports/pdf/.

Xuat du lieu ra Excel duoc thuc hien thong qua thu vien Pandas va OpenPyXL. ExcelExporter cung cap ba chuc nang chinh: xuat danh sach kho ra Excel voi thong tin chi tiet tung kho; xuat danh sach vi tri ra Excel voi thong tin ma vi tri, khu vuc, hang, tang, dien tich, gia thue va trang thai; xuat du lieu Dashboard ra Excel voi ba sheet rieng biet (Kho, Vi tri va Tong hop so lieu). File Excel co dinh dang chuyen nghiep voi font chu, can chinh, duong vien va mau sac cho tieu de. Cac file duoc luu vao thu muc data/exports/ voi ten tu dong gan timestamp.

Bang tong hop cac chuc nang xuat du lieu:

| Chuc nang xuat | Dinh dang | Du lieu xuat | Thu muc luu |
|---|---|---|---|
| Xuat hop dong | PDF | Thong tin hop dong, khach hang, vi tri, dieu khoan | data/exports/pdf/ |
| Xuat hoa don | PDF | Thong tin hoa don, dich vu, thue, ngan hang | data/exports/pdf/ |
| Xuat bao cao tong hop | PDF | So lieu thong ke, canh bao, khuyen nghi | data/exports/pdf/ |
| Xuat danh sach kho | Excel (.xlsx) | Thong tin cac kho | data/exports/ |
| Xuat danh sach vi tri | Excel (.xlsx) | Thong tin cac vi tri luu tru | data/exports/ |
| Xuat Dashboard | Excel (.xlsx) | 3 sheet: Kho, Vi tri, Tong hop | data/exports/ |
| Xuat danh sach khach hang | Excel (.xlsx) | Thong tin khach hang | data/exports/ |
| Xuat danh sach hop dong | Excel (.xlsx) | Thong tin hop dong | data/exports/ |
| Xuat danh sach thanh toan | Excel (.xlsx) | Thong tin thanh toan | data/exports/ |
| Xuat danh sach hang hoa | Excel (.xlsx) | Thong tin hang hoa | data/exports/ |

---

## 15. Chuc nang Canh bao Thong minh

He thong duoc trang bi cac co che canh bao thong minh giup nguoi quan ly chu dong trong viec theo doi va xu ly cac tinh huong phat sinh. Cac canh bao nay duoc trien khai tai src/utils/hop_dong_alert.py va src/services/inventory_service.py.

Co ba loai canh bao ve hop dong duoc phan loai theo muc do uu tien:

| Muc uu tien | Dieu kien | Loai canh bao |
|---|---|---|
| Cao (critical) | Hop dong da qua han | Overdue alert |
| Cao (high) | Hop dong con duoi 7 ngay | Expiring soon alert |
| Trung binh (medium) | Hop dong con tu 7 den 30 ngay | Expiring soon alert |
| Thap (low) | Hop dong con tren 30 ngay | Canh bao nhe |

HopDongAlertService cung cap cac phuong thuc de truy van danh sach hop dong sap het han trong khoang thoi gian nhat dinh, danh sach hop dong het han dung ngay hien tai, danh sach hop dong da qua han. Dich vu nay cung tong hop toan bo canh bao, sap xep theo muc do uu tien va thong ke so luong canh bao theo tung loai. Ngoai ra, he thong con ho tro xuat bao cao chi tiet ve tinh trang canh bao ra tep van ban va co san cac phuong thuc gui thong bao qua email va SMS (dang o trang thai cho trien khai).

Ben canh canh bao hop dong, he thong con co co che canh bao ton kho: khi so luong hang hoa trong kho duoi nguong 10 don vi, hang hoa do se duoc danh dau la "sap het" va hien thi tren thanh thong ke cua module Quan ly Hang hoa. Tuong tu, Dashboard hien thi canh bao cho cac kho co ty le lap day tren 90% (qua tai), kem theo ten kho, ty le hien tai va nut Xem chi tiet.

---

## 16. So do Quy trinh Nghiep vu Tong the

So do duoi day mo ta quy trinh nghiep vu tong the cua he thong tu khi bat dau den khi ket thuc hop dong:

```
                                BAT DAU
                                   |
                                   v
                    +-------------------------------+
                    |       DANG NHAP HE THONG       |
                    |  Nhap ten dang nhap va mat khau  |
                    |  AuthService.xac thuc           |
                    |  Tao session token              |
                    +-------------------+---------------+
                                   |
                                   v
                    +-------------------------------+
                    |       QUAN LY KHACH HANG       |
                    |  Them khach hang moi            |
                    |  Nhap thong tin (ten, SDT,     |
                    |  Email, dia chi, loai KH)       |
                    |  Luu vao co so du lieu          |
                    +-------------------+---------------+
                                   |
                                   v
                    +-------------------------------+
                    |       QUAN LY KHO va VI TRI    |
                    |  Them kho va vi tri luu tru     |
                    |  Tao kho voi dien tich,         |
                    |  suc chua                       |
                    |  Tao vi tri (Khu vuc, Hang,     |
                    |  Tang) trong kho                |
                    +-------------------+---------------+
                                   |
                                   v
                    +-------------------------------+
                    |       TAO HOP DONG THUE KHO    |
                    |  Chon: Khach hang + Vi tri     |
                    |  Nhap: Ngay BD-KT, Gia thue,   |
                    |  Tien coc, Phuong thuc TT     |
                    |  HopDongService.create()       |
                    |  Tu dong tao lich thanh toan   |
                    |  Cap nhat vi tri: Da thue      |
                    +-------------------+---------------+
                                   |
                  +----------------+----------------+
                  |                |                |
                  v                v                v
    +-------------------+ +--------------+ +--------------+
    | NHAP/XUAT HANG   | | THANH TOAN  | | GIA HAN /   |
    | HangHoaService   | | TT Service  | | CHAM DUT    |
    | Nhap hang vao    | | Tao phieu   | | HD Wizard   |
    | vi tri            | | thanh toan  | | Gia han:    |
    | Xuat hang khoi   | | Theo doi    | | Renewal     |
    | kho               | | cong no     | | Cham dut:  |
    | Canh bao ton     | | Phat hien   | | Terminate   |
    | kho thap          | | qua han     | | + phat      |
    +-------------------+ +--------------+ +--------------+
                  |                |                |
                  +----------------+----------------+
                                   |
                                   v
                    +-------------------------------+
                    |       BAO CAO va THONG KE     |
                    |  Dashboard tong quan           |
                    |  Bieu do doanh thu             |
                    |  Xuat PDF (hop dong, hoa don,  |
                    |  bao cao tong hop)             |
                    |  Xuat Excel (danh sach, so     |
                    |  lieu thong ke)                |
                    +-------------------+---------------+
                                   |
                                   v
                    +-------------------------------+
                    |     CANH BAO va THEO DOI      |
                    |  Hop dong sap het han           |
                    |  Kho qua tai (tren 90%)         |
                    |  Hang hoa sap het (duoi 10)    |
                    |  Cong no qua han               |
                    |  Phan loai muc uu tien          |
                    |  Hien thi tren Dashboard       |
                    +-------------------+---------------+
                                   |
                                   v
                    +-------------------------------+
                    |     KET THUC HOP DONG         |
                    |  Het han hoac bi cham dut      |
                    |  Cap nhat vi tri: Trong       |
                    |  Luu lich su hop dong          |
                    +-------------------+---------------+
                                   |
                                   v
                                KET THUC
"""

---

## Bang Tong Ket Cac Chuc Nang Chuong Trinh

| STT | Module chuc nang | View chinh | Service chinh | File chinh |
|---|---|---|---|---|
| 1 | Dang nhap va Bao mat | LoginView | AuthService | login_view.py, auth_service.py |
| 2 | Dashboard tong quan | DashboardView | KhoService, ViTriService | dashboard_view.py, charts.py |
| 3 | Quan ly Khach hang | KhachHangView | KhachHangService | khach_hang_view.py, khach_hang_service.py |
| 4 | Quan ly Kho | KhoView | KhoService | kho_view.py, kho_service.py |
| 5 | Quan ly Vi tri | ViTriView | ViTriService | vi_tri_view.py, vi_tri_service.py |
| 6 | Quan ly Hop dong | HopDongView | HopDongService | hop_dong_view.py, hop_dong_service.py |
| 7 | Quan ly Hang hoa | HangHoaView | HangHoaService | hang_hoa_view.py, hang_hoa_service.py |
| 8 | Quan ly Thanh toan | ThanhToanView | ThanhToanService | thanh_toan_view.py, thanh_toan_service.py |
| 9 | Bao cao va Thong ke | BaoCaoView | ReportService | bao_cao_view.py, report_service.py |
| 10 | Quan ly Nguoi dung | UserView | UserService | user_view.py, user_service.py |
| 11 | Cai dat He thong | SettingsView | (none) | settings_view.py |
| 12 | Tro giup va Huong dan | HelpView | (none) | help_view.py |

| STT | Chuc nang ho tro | File trien khai | Mo ta |
|---|---|---|---|
| 1 | Xuat PDF | pdf_generation_service.py | Xuat hop dong, hoa don, bao cao tong hop |
| 2 | Xuat Excel | export_service.py | Xuat danh sach va so lieu thong ke |
| 3 | Canh bao hop dong | hop_dong_alert.py | Theo doi va phan loai canh bao hop dong |
| 4 | Kiem tra ton kho | inventory_service.py | Kiem tra va canh bao ton kho |
| 5 | Wizard gia han | renewal_wizard.py | Huong dan gia han hop dong 3 buoc |
| 6 | Wizard cham dut | termination_wizard.py | Huong dan cham dut hop dong 3 buoc |
| 7 | Chi tiet khach hang | khach_hang_detail_view.py | 4 tab: Thong tin, Hop dong, Thanh toan, Lich su |
| 8 | Chi tiet hop dong | hop_dong_detail_view.py | 4 tab: Thong tin, Hang hoa, Thanh toan, Lich su |
| 9 | Chuc nang tim kiem | search_box.py | Tim kiem du lieu trong tat ca cac module |
| 10 | Bang du lieu | data_table.py | Bang du lieu tuy chinh voi toolbar |

---

## Tai lieu tham khao

1. PyQt6 Documentation: https://www.riverbankcomputing.com/static/Docs/PyQt6/
2. SQLAlchemy 2.0 Documentation: https://docs.sqlalchemy.org/en/20/
3. ReportLab User Guide: https://www.reportlab.com/docs/reportlab-userguide.pdf
4. pandas Documentation: https://pandas.pydata.org/docs/
5. Matplotlib Documentation: https://matplotlib.org/stable/contents.html
6. bcrypt Documentation: https://pypi.org/project/bcrypt/
7. pytest Documentation: https://docs.pytest.org/
"""

with open("docs/YEU_CAU_CHUC_NANG.md", "w", encoding="utf-8") as f:
    f.write(content)
print("File written successfully")
