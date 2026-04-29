#!/usr/bin/env python3
"""
Seed Data Script - Thêm dữ liệu mẫu vào database
Chạy: python scripts/seed_data.py
"""
import sys
import os
from datetime import datetime, date, timedelta
from decimal import Decimal

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.database.connection import get_connection
from src.models import (
    Base, KhachHang, Kho, ViTri, HopDong, HangHoa, 
    ThanhToan, NhanVien, SystemLog, BaoCao,
    LoaiKhachEnum, TrangThaiKHEnum, TrangThaiKhoEnum, 
    TrangThaiViTriEnum, TrangThaiHDEnum, LoaiPhiEnum, 
    TrangThaiTTEnum, VaiTroNVEuum, TrangThaiNhanVienEnum, HanhDongLogEnum
)
from src.services.auth.auth_service import AuthService

def seed_nhan_vien(session, auth_service):
    """Seed 10 nhân viên"""
    nhan_viens = [
        NhanVien(
            ma_nhan_vien='NV001', ho_ten='Nguyễn Văn Admin',
            email='admin@warehouse.local', so_dien_thoai='0901000001',
            vai_tro=VaiTroNVEuum.QUAN_TRI, tai_khoan='admin',
            mat_khau=auth_service.hash_password('admin123'),
            trang_thai=TrangThaiNhanVienEnum.HOAT_DONG
        ),
        NhanVien(
            ma_nhan_vien='NV002', ho_ten='Trần Thị Mai',
            email='mai.tran@warehouse.local', so_dien_thoai='0901000002',
            vai_tro=VaiTroNVEuum.KE_TOAN, tai_khoan='mayke',
            mat_khau=auth_service.hash_password('password123'),
            trang_thai=TrangThaiNhanVienEnum.HOAT_DONG
        ),
        NhanVien(
            ma_nhan_vien='NV003', ho_ten='Lê Hoàng Nam',
            email='nam.hoang@warehouse.local', so_dien_thoai='0901000003',
            vai_tro=VaiTroNVEuum.KINH_DOANH, tai_khoan='namkd',
            mat_khau=auth_service.hash_password('password123'),
            trang_thai=TrangThaiNhanVienEnum.HOAT_DONG
        ),
        NhanVien(
            ma_nhan_vien='NV004', ho_ten='Phạm Thị Lan',
            email='lan.pham@warehouse.local', so_dien_thoai='0901000004',
            vai_tro=VaiTroNVEuum.KHO, tai_khoan='lankho',
            mat_khau=auth_service.hash_password('password123'),
            trang_thai=TrangThaiNhanVienEnum.HOAT_DONG
        ),
        NhanVien(
            ma_nhan_vien='NV005', ho_ten='Đặng Minh Tuấn',
            email='tuan.dang@warehouse.local', so_dien_thoai='0901000005',
            vai_tro=VaiTroNVEuum.KINH_DOANH, tai_khoan='tuankd',
            mat_khau=auth_service.hash_password('password123'),
            trang_thai=TrangThaiNhanVienEnum.HOAT_DONG
        ),
        NhanVien(
            ma_nhan_vien='NV006', ho_ten='Bùi Thị Hương',
            email='huong.bui@warehouse.local', so_dien_thoai='0901000006',
            vai_tro=VaiTroNVEuum.KE_TOAN, tai_khoan='huongkt',
            mat_khau=auth_service.hash_password('password123'),
            trang_thai=TrangThaiNhanVienEnum.HOAT_DONG
        ),
        NhanVien(
            ma_nhan_vien='NV007', ho_ten='Hoàng Văn Đức',
            email='duc.hoang@warehouse.local', so_dien_thoai='0901000007',
            vai_tro=VaiTroNVEuum.KHO, tai_khoan='duckho',
            mat_khau=auth_service.hash_password('password123'),
            trang_thai=TrangThaiNhanVienEnum.HOAT_DONG
        ),
        NhanVien(
            ma_nhan_vien='NV008', ho_ten='Vũ Thị Thanh',
            email='thanh.vu@warehouse.local', so_dien_thoai='0901000008',
            vai_tro=VaiTroNVEuum.KINH_DOANH, tai_khoan='thanhkd',
            mat_khau=auth_service.hash_password('password123'),
            trang_thai=TrangThaiNhanVienEnum.NGUNG_HOAT_DONG
        ),
        NhanVien(
            ma_nhan_vien='NV009', ho_ten='Đỗ Minh Quân',
            email='quan.do@warehouse.local', so_dien_thoai='0901000009',
            vai_tro=VaiTroNVEuum.QUAN_TRI, tai_khoan='quanqt',
            mat_khau=auth_service.hash_password('password123'),
            trang_thai=TrangThaiNhanVienEnum.HOAT_DONG
        ),
        NhanVien(
            ma_nhan_vien='NV010', ho_ten='Ngô Thị Thu',
            email='thu.ngo@warehouse.local', so_dien_thoai='0901000010',
            vai_tro=VaiTroNVEuum.KHO, tai_khoan='thukho',
            mat_khau=auth_service.hash_password('password123'),
            trang_thai=TrangThaiNhanVienEnum.HOAT_DONG
        ),
    ]
    
    for nv in nhan_viens:
        existing = session.query(NhanVien).filter(
            (NhanVien.ma_nhan_vien == nv.ma_nhan_vien) |
            (NhanVien.email == nv.email) |
            (NhanVien.tai_khoan == nv.tai_khoan)
        ).first()
        if not existing:
            session.add(nv)
    
    session.commit()
    print(f"  ✅ Added {len(nhan_viens)} NhanVien")
    return nhan_viens


def seed_kho(session):
    """Seed 10 kho"""
    khos = [
        Kho(
            ma_kho='KHO001', ten_kho='Kho A - Quận 7',
            dia_chi='123 Đường Nguyễn Văn Linh, Quận 7, TP.HCM',
            dien_tich=1000.0, suc_chua=5000.0, da_su_dung=2500.0,
            trang_thai=TrangThaiKhoEnum.HOAT_DONG
        ),
        Kho(
            ma_kho='KHO002', ten_kho='Kho B - Quận 9',
            dia_chi='456 Đường Đại Lộ 2, Quận 9, TP.HCM',
            dien_tich=1500.0, suc_chua=6000.0, da_su_dung=4200.0,
            trang_thai=TrangThaiKhoEnum.HOAT_DONG
        ),
        Kho(
            ma_kho='KHO003', ten_kho='Kho C - Thủ Đức',
            dia_chi='789 Đường Man Thiện, Thủ Đức, TP.HCM',
            dien_tich=800.0, suc_chua=3000.0, da_su_dung=2400.0,
            trang_thai=TrangThaiKhoEnum.HOAT_DONG
        ),
        Kho(
            ma_kho='KHO004', ten_kho='Kho D - Bình Thạnh',
            dia_chi='321 Đường Nguyễn Hữu Cảnh, Bình Thạnh, TP.HCM',
            dien_tich=600.0, suc_chua=2000.0, da_su_dung=1800.0,
            trang_thai=TrangThaiKhoEnum.HOAT_DONG
        ),
        Kho(
            ma_kho='KHO005', ten_kho='Kho E - Tân Bình',
            dia_chi='555 Đường Cộng Hòa, Tân Bình, TP.HCM',
            dien_tich=1200.0, suc_chua=4500.0, da_su_dung=3000.0,
            trang_thai=TrangThaiKhoEnum.HOAT_DONG
        ),
        Kho(
            ma_kho='KHO006', ten_kho='Kho F - Gò Vấp',
            dia_chi='888 Đường Phan Văn Trị, Gò Vấp, TP.HCM',
            dien_tich=900.0, suc_chua=3500.0, da_su_dung=500.0,
            trang_thai=TrangThaiKhoEnum.HOAT_DONG
        ),
        Kho(
            ma_kho='KHO007', ten_kho='Kho G - Bình Tân',
            dia_chi='999 Đường Kinh Dương Vương, Bình Tân, TP.HCM',
            dien_tich=2000.0, suc_chua=8000.0, da_su_dung=0.0,
            trang_thai=TrangThaiKhoEnum.BAO_TRI
        ),
        Kho(
            ma_kho='KHO008', ten_kho='Kho H - Tân Phú',
            dia_chi='111 Đường Độc Lập, Tân Phú, TP.HCM',
            dien_tich=750.0, suc_chua=2800.0, da_su_dung=0.0,
            trang_thai=TrangThaiKhoEnum.NGUNG
        ),
        Kho(
            ma_kho='KHO009', ten_kho='Kho I - Phú Nhuận',
            dia_chi='222 Đường Hoàng Văn Thụ, Phú Nhuận, TP.HCM',
            dien_tich=500.0, suc_chua=1800.0, da_su_dung=900.0,
            trang_thai=TrangThaiKhoEnum.HOAT_DONG
        ),
        Kho(
            ma_kho='KHO010', ten_kho='Kho K - Hóc Môn',
            dia_chi='333 Đường Quang Trung, Hóc Môn, TP.HCM',
            dien_tich=1800.0, suc_chua=7000.0, da_su_dung=5600.0,
            trang_thai=TrangThaiKhoEnum.HOAT_DONG
        ),
    ]
    
    for kho in khos:
        existing = session.query(Kho).filter(Kho.ma_kho == kho.ma_kho).first()
        if not existing:
            session.add(kho)
    
    session.commit()
    print(f"  ✅ Added {len(khos)} Kho")
    return khos


def seed_vi_tri(session):
    """Seed 10 vị trí"""
    vi_tris = [
        ViTri(
            ma_vi_tri='K01-A-01-01', ma_kho='KHO001',
            khu_vuc='A', hang='01', tang=1,
            dien_tich=50.0, gia_thue=150000.0, suc_chua=100.0,
            trang_thai=TrangThaiViTriEnum.DA_THUE
        ),
        ViTri(
            ma_vi_tri='K01-A-01-02', ma_kho='KHO001',
            khu_vuc='A', hang='01', tang=1,
            dien_tich=75.0, gia_thue=175000.0, suc_chua=150.0,
            trang_thai=TrangThaiViTriEnum.TRONG
        ),
        ViTri(
            ma_vi_tri='K01-B-02-01', ma_kho='KHO002',
            khu_vuc='B', hang='02', tang=1,
            dien_tich=100.0, gia_thue=200000.0, suc_chua=200.0,
            trang_thai=TrangThaiViTriEnum.DA_THUE
        ),
        ViTri(
            ma_vi_tri='K02-A-01-01', ma_kho='KHO003',
            khu_vuc='A', hang='01', tang=1,
            dien_tich=60.0, gia_thue=160000.0, suc_chua=120.0,
            trang_thai=TrangThaiViTriEnum.BAO_TRI
        ),
        ViTri(
            ma_vi_tri='K03-C-03-02', ma_kho='KHO004',
            khu_vuc='C', hang='03', tang=2,
            dien_tich=80.0, gia_thue=180000.0, suc_chua=160.0,
            trang_thai=TrangThaiViTriEnum.DA_THUE
        ),
        ViTri(
            ma_vi_tri='K04-D-01-01', ma_kho='KHO005',
            khu_vuc='D', hang='01', tang=1,
            dien_tich=45.0, gia_thue=140000.0, suc_chua=90.0,
            trang_thai=TrangThaiViTriEnum.TRONG
        ),
        ViTri(
            ma_vi_tri='K05-E-02-01', ma_kho='KHO006',
            khu_vuc='E', hang='02', tang=1,
            dien_tich=55.0, gia_thue=155000.0, suc_chua=110.0,
            trang_thai=TrangThaiViTriEnum.TRONG
        ),
        ViTri(
            ma_vi_tri='K06-F-01-01', ma_kho='KHO007',
            khu_vuc='F', hang='01', tang=1,
            dien_tich=90.0, gia_thue=190000.0, suc_chua=180.0,
            trang_thai=TrangThaiViTriEnum.DA_THUE
        ),
        ViTri(
            ma_vi_tri='K07-G-03-02', ma_kho='KHO008',
            khu_vuc='G', hang='03', tang=2,
            dien_tich=70.0, gia_thue=170000.0, suc_chua=140.0,
            trang_thai=TrangThaiViTriEnum.TRONG
        ),
        ViTri(
            ma_vi_tri='K08-H-02-01', ma_kho='KHO009',
            khu_vuc='H', hang='02', tang=1,
            dien_tich=65.0, gia_thue=165000.0, suc_chua=130.0,
            trang_thai=TrangThaiViTriEnum.DA_THUE
        ),
    ]
    
    for vt in vi_tris:
        existing = session.query(ViTri).filter(ViTri.ma_vi_tri == vt.ma_vi_tri).first()
        if not existing:
            session.add(vt)
    
    session.commit()
    print(f"  ✅ Added {len(vi_tris)} ViTri")
    return vi_tris


def seed_khach_hang(session):
    """Seed 10 khách hàng"""
    khach_hangs = [
        KhachHang(
            ma_khach_hang='KH001', ho_ten='Nguyễn Văn An',
            loai_khach=LoaiKhachEnum.CA_NHAN, so_dien_thoai='0902000001',
            email='nguyenvanan@email.com', dia_chi='123 Đường ABC, Quận 1, TP.HCM',
            ngay_dang_ky=date(2024, 1, 15), trang_thai=TrangThaiKHEnum.HOAT_DONG
        ),
        KhachHang(
            ma_khach_hang='KH002', ho_ten='Công Ty TNHH ABC',
            loai_khach=LoaiKhachEnum.DOANH_NGHIEP, so_dien_thoai='0902000002',
            email='info@abc.vn', dia_chi='456 Đường XYZ, Quận 2, TP.HCM',
            ma_so_thue='0123456789', ngay_dang_ky=date(2024, 2, 20), trang_thai=TrangThaiKHEnum.HOAT_DONG
        ),
        KhachHang(
            ma_khach_hang='KH003', ho_ten='Trần Thị Bình',
            loai_khach=LoaiKhachEnum.CA_NHAN, so_dien_thoai='0902000003',
            email='binhtran@email.com', dia_chi='789 Đường DEF, Quận 3, TP.HCM',
            ngay_dang_ky=date(2024, 3, 10), trang_thai=TrangThaiKHEnum.HOAT_DONG
        ),
        KhachHang(
            ma_khach_hang='KH004', ho_ten='Doanh Nghiệp Tư Nhân Bình Minh',
            loai_khach=LoaiKhachEnum.DOANH_NGHIEP, so_dien_thoai='0902000004',
            email='contact@binhminh.vn', dia_chi='321 Đường GHI, Quận 4, TP.HCM',
            ma_so_thue='9876543210', ngay_dang_ky=date(2024, 4, 5), trang_thai=TrangThaiKHEnum.HOAT_DONG
        ),
        KhachHang(
            ma_khach_hang='KH005', ho_ten='Lê Văn Cường',
            loai_khach=LoaiKhachEnum.CA_NHAN, so_dien_thoai='0902000005',
            email='cuongle@email.com', dia_chi='654 Đường JKL, Quận 5, TP.HCM',
            ngay_dang_ky=date(2024, 5, 18), trang_thai=TrangThaiKHEnum.TAM_KHOA
        ),
        KhachHang(
            ma_khach_hang='KH006', ho_ten='Công Ty Cổ Phần Thương Mại Delta',
            loai_khach=LoaiKhachEnum.DOANH_NGHIEP, so_dien_thoai='0902000006',
            email='delta@commerce.vn', dia_chi='987 Đường MNO, Quận 6, TP.HCM',
            ma_so_thue='1122334455', ngay_dang_ky=date(2024, 6, 22), trang_thai=TrangThaiKHEnum.HOAT_DONG
        ),
        KhachHang(
            ma_khach_hang='KH007', ho_ten='Phạm Thị Dung',
            loai_khach=LoaiKhachEnum.CA_NHAN, so_dien_thoai='0902000007',
            email='dungpham@email.com', dia_chi='147 Đường PQR, Quận 7, TP.HCM',
            ngay_dang_ky=date(2024, 7, 30), trang_thai=TrangThaiKHEnum.HOAT_DONG
        ),
        KhachHang(
            ma_khach_hang='KH008', ho_ten='Hộ Kinh Doanh Thành Công',
            loai_khach=LoaiKhachEnum.DOANH_NGHIEP, so_dien_thoai='0902000008',
            email='thanhncong@gmail.com', dia_chi='258 Đường STU, Quận 8, TP.HCM',
            ma_so_thue='5544332211', ngay_dang_ky=date(2024, 8, 12), trang_thai=TrangThaiKHEnum.HOAT_DONG
        ),
        KhachHang(
            ma_khach_hang='KH009', ho_ten='Hoàng Văn Em',
            loai_khach=LoaiKhachEnum.CA_NHAN, so_dien_thoai='0902000009',
            email='emhoang@email.com', dia_chi='369 Đường VWX, Quận 9, TP.HCM',
            ngay_dang_ky=date(2024, 9, 25), trang_thai=TrangThaiKHEnum.HOAT_DONG
        ),
        KhachHang(
            ma_khach_hang='KH010', ho_ten='Công Ty TNHH MTV Hùng Vương',
            loai_khach=LoaiKhachEnum.DOANH_NGHIEP, so_dien_thoai='0902000010',
            email='hungvuong@corp.vn', dia_chi='480 Đường YZA, Thủ Đức, TP.HCM',
            ma_so_thue='9988776655', ngay_dang_ky=date(2024, 10, 8), trang_thai=TrangThaiKHEnum.DA_XOA
        ),
    ]
    
    for kh in khach_hangs:
        existing = session.query(KhachHang).filter(
            (KhachHang.ma_khach_hang == kh.ma_khach_hang) |
            (KhachHang.email == kh.email)
        ).first()
        if not existing:
            session.add(kh)
    
    session.commit()
    print(f"  ✅ Added {len(khach_hangs)} KhachHang")
    return khach_hangs


def seed_hop_dong(session):
    """Seed 10 hợp đồng"""
    hop_dongs = [
        HopDong(
            ma_hop_dong='HD001', ma_khach_hang='KH001', ma_vi_tri='K01-A-01-01',
            ngay_bat_dau=date(2024, 1, 20), ngay_ket_thuc=date(2025, 1, 20),
            gia_thue=150000.0, tien_coc=3000000.0, phuong_thuc_thanh_toan='hang_thang',
            trang_thai=TrangThaiHDEnum.HIEU_LUC
        ),
        HopDong(
            ma_hop_dong='HD002', ma_khach_hang='KH002', ma_vi_tri='K01-B-02-01',
            ngay_bat_dau=date(2024, 2, 25), ngay_ket_thuc=date(2025, 2, 25),
            gia_thue=200000.0, tien_coc=4000000.0, phuong_thuc_thanh_toan='hang_thang',
            trang_thai=TrangThaiHDEnum.HIEU_LUC
        ),
        HopDong(
            ma_hop_dong='HD003', ma_khach_hang='KH003', ma_vi_tri='K03-C-03-02',
            ngay_bat_dau=date(2024, 3, 15), ngay_ket_thuc=date(2024, 9, 15),
            gia_thue=180000.0, tien_coc=3600000.0, phuong_thuc_thanh_toan='hang_quy',
            trang_thai=TrangThaiHDEnum.HET_HAN
        ),
        HopDong(
            ma_hop_dong='HD004', ma_khach_hang='KH004', ma_vi_tri='K06-F-01-01',
            ngay_bat_dau=date(2024, 5, 10), ngay_ket_thuc=date(2025, 5, 10),
            gia_thue=190000.0, tien_coc=3800000.0, phuong_thuc_thanh_toan='hang_thang',
            trang_thai=TrangThaiHDEnum.HIEU_LUC
        ),
        HopDong(
            ma_hop_dong='HD005', ma_khach_hang='KH006', ma_vi_tri='K08-H-02-01',
            ngay_bat_dau=date(2024, 6, 25), ngay_ket_thuc=date(2025, 6, 25),
            gia_thue=165000.0, tien_coc=3300000.0, phuong_thuc_thanh_toan='hang_thang',
            trang_thai=TrangThaiHDEnum.HIEU_LUC
        ),
        HopDong(
            ma_hop_dong='HD006', ma_khach_hang='KH007', ma_vi_tri='K01-A-01-02',
            ngay_bat_dau=date(2024, 8, 5), ngay_ket_thuc=date(2025, 8, 5),
            gia_thue=175000.0, tien_coc=3500000.0, phuong_thuc_thanh_toan='hang_quy',
            trang_thai=TrangThaiHDEnum.HIEU_LUC
        ),
        HopDong(
            ma_hop_dong='HD007', ma_khach_hang='KH008', ma_vi_tri='K04-D-01-01',
            ngay_bat_dau=date(2024, 9, 1), ngay_ket_thuc=date(2025, 3, 1),
            gia_thue=140000.0, tien_coc=2800000.0, phuong_thuc_thanh_toan='hang_thang',
            trang_thai=TrangThaiHDEnum.CHAM_DUT, ly_do_cham_dut='Khách hàng chấm dứt hợp đồng sớm',
            ngay_cham_dut=date(2024, 12, 15)
        ),
        HopDong(
            ma_hop_dong='HD008', ma_khach_hang='KH009', ma_vi_tri='K05-E-02-01',
            ngay_bat_dau=date(2024, 10, 1), ngay_ket_thuc=date(2025, 10, 1),
            gia_thue=155000.0, tien_coc=3100000.0, phuong_thuc_thanh_toan='hang_thang',
            trang_thai=TrangThaiHDEnum.HIEU_LUC
        ),
        HopDong(
            ma_hop_dong='HD009', ma_khach_hang='KH005', ma_vi_tri='K02-A-01-01',
            ngay_bat_dau=date(2024, 11, 10), ngay_ket_thuc=date(2025, 5, 10),
            gia_thue=160000.0, tien_coc=3200000.0, phuong_thuc_thanh_toan='hang_quy',
            trang_thai=TrangThaiHDEnum.GIA_HAN
        ),
        HopDong(
            ma_hop_dong='HD010', ma_khach_hang='KH001', ma_vi_tri='K07-G-03-02',
            ngay_bat_dau=date(2024, 12, 1), ngay_ket_thuc=date(2025, 12, 1),
            gia_thue=170000.0, tien_coc=3400000.0, phuong_thuc_thanh_toan='hang_thang',
            trang_thai=TrangThaiHDEnum.HIEU_LUC
        ),
    ]
    
    for hd in hop_dongs:
        existing = session.query(HopDong).filter(HopDong.ma_hop_dong == hd.ma_hop_dong).first()
        if not existing:
            session.add(hd)
    
    session.commit()
    print(f"  ✅ Added {len(hop_dongs)} HopDong")
    return hop_dongs


def seed_hang_hoa(session):
    """Seed 10 hàng hóa"""
    hang_hoas = [
        HangHoa(
            ma_hang_hoa='HH001', ma_hop_dong='HD001', ten_hang='Máy tính xách tay Dell XPS 15',
            loai_hang='Điện tử', so_luong=10, don_vi='chiếc', trong_luong=2.5,
            kich_thuoc='35x24x2 cm', gia_tri=25000000.0,
            ngay_nhap=datetime(2024, 2, 1), trang_thai='trong_kho', vi_tri_luu_tru='K01-A-01-01-01'
        ),
        HangHoa(
            ma_hang_hoa='HH002', ma_hop_dong='HD001', ten_hang='Ghế công thái họa',
            loai_hang='Nội thất', so_luong=20, don_vi='chiếc', trong_luong=15.0,
            kich_thuoc='60x60x120 cm', gia_tri=8500000.0,
            ngay_nhap=datetime(2024, 2, 5), trang_thai='trong_kho', vi_tri_luu_tru='K01-A-01-01-02'
        ),
        HangHoa(
            ma_hang_hoa='HH003', ma_hop_dong='HD002', ten_hang='Máy in laser HP',
            loai_hang='Văn phòng phẩm', so_luong=5, don_vi='chiếc', trong_luong=8.5,
            kich_thuoc='40x35x30 cm', gia_tri=12000000.0,
            ngay_nhap=datetime(2024, 3, 1), trang_thai='trong_kho', vi_tri_luu_tru='K01-B-02-01-01'
        ),
        HangHoa(
            ma_hang_hoa='HH004', ma_hop_dong='HD004', ten_hang='Tivi Samsung 55 inch',
            loai_hang='Điện tử', so_luong=15, don_vi='chiếc', trong_luong=18.0,
            kich_thuoc='125x72x8 cm', gia_tri=18500000.0,
            ngay_nhap=datetime(2024, 6, 1), trang_thai='trong_kho', vi_tri_luu_tru='K06-F-01-01-01'
        ),
        HangHoa(
            ma_hang_hoa='HH005', ma_hop_dong='HD005', ten_hang='Bàn làm việc',
            loai_hang='Nội thất', so_luong=30, don_vi='chiếc', trong_luong=25.0,
            kich_thuoc='140x70x75 cm', gia_tri=5500000.0,
            ngay_nhap=datetime(2024, 7, 10), trang_thai='trong_kho', vi_tri_luu_tru='K08-H-02-01-01'
        ),
        HangHoa(
            ma_hang_hoa='HH006', ma_hop_dong='HD006', ten_hang='Điện thoại iPhone 15 Pro',
            loai_hang='Điện tử', so_luong=50, don_vi='chiếc', trong_luong=0.3,
            kich_thuoc='15x8x1 cm', gia_tri=28000000.0,
            ngay_nhap=datetime(2024, 8, 15), trang_thai='trong_kho', vi_tri_luu_tru='K01-A-01-02-01'
        ),
        HangHoa(
            ma_hang_hoa='HH007', ma_hop_dong='HD008', ten_hang='Máy chiếu Sony',
            loai_hang='Điện tử', so_luong=8, don_vi='chiếc', trong_luong=4.5,
            kich_thuoc='30x25x10 cm', gia_tri=22000000.0,
            ngay_nhap=datetime(2024, 10, 5), trang_thai='trong_kho', vi_tri_luu_tru='K05-E-02-01-01'
        ),
        HangHoa(
            ma_hang_hoa='HH008', ma_hop_dong='HD009', ten_hang='Kệ sách 4 tầng',
            loai_hang='Nội thất', so_luong=25, don_vi='chiếc', trong_luong=20.0,
            kich_thuoc='80x30x150 cm', gia_tri=3200000.0,
            ngay_nhap=datetime(2024, 11, 15), trang_thai='trong_kho', vi_tri_luu_tru='K02-A-01-01-01'
        ),
        HangHoa(
            ma_hang_hoa='HH009', ma_hop_dong='HD010', ten_hang='Loa Bluetooth JBL',
            loai_hang='Điện tử', so_luong=40, don_vi='chiếc', trong_luong=1.5,
            kich_thuoc='22x10x10 cm', gia_tri=4500000.0,
            ngay_nhap=datetime(2024, 12, 5), trang_thai='trong_kho', vi_tri_luu_tru='K07-G-03-02-01'
        ),
        HangHoa(
            ma_hang_hoa='HH010', ma_hop_dong='HD001', ten_hang='Camera giám sát',
            loai_hang='Thiết bị an ninh', so_luong=12, don_vi='chiếc', trong_luong=0.8,
            kich_thuoc='10x10x15 cm', gia_tri=3500000.0,
            ngay_nhap=datetime(2024, 12, 10), trang_thai='trong_kho', vi_tri_luu_tru='K01-A-01-01-03'
        ),
    ]
    
    for hh in hang_hoas:
        existing = session.query(HangHoa).filter(HangHoa.ma_hang_hoa == hh.ma_hang_hoa).first()
        if not existing:
            session.add(hh)
    
    session.commit()
    print(f"  ✅ Added {len(hang_hoas)} HangHoa")
    return hang_hoas


def seed_thanh_toan(session):
    """Seed 10 thanh toán"""
    thanh_toans = [
        ThanhToan(
            ma_thanh_toan='TT001', ma_hop_dong='HD001', loai_phi=LoaiPhiEnum.TIEN_COC,
            so_tien=3000000.0, ngay_den_han=date(2024, 1, 20),
            ngay_thanh_toan=date(2024, 1, 18), phuong_thuc='chuyen_khoan',
            so_giao_dich='CK001', trang_thai=TrangThaiTTEnum.DA_THANH_TOAN
        ),
        ThanhToan(
            ma_thanh_toan='TT002', ma_hop_dong='HD001', loai_phi=LoaiPhiEnum.THUE_THANG,
            so_tien=1500000.0, ky_thanh_toan='2024-02', ngay_den_han=date(2024, 2, 20),
            ngay_thanh_toan=date(2024, 2, 18), phuong_thuc='chuyen_khoan',
            so_giao_dich='CK002', trang_thai=TrangThaiTTEnum.DA_THANH_TOAN
        ),
        ThanhToan(
            ma_thanh_toan='TT003', ma_hop_dong='HD002', loai_phi=LoaiPhiEnum.TIEN_COC,
            so_tien=4000000.0, ngay_den_han=date(2024, 2, 25),
            ngay_thanh_toan=date(2024, 2, 23), phuong_thuc='chuyen_khoan',
            so_giao_dich='CK003', trang_thai=TrangThaiTTEnum.DA_THANH_TOAN
        ),
        ThanhToan(
            ma_thanh_toan='TT004', ma_hop_dong='HD003', loai_phi=LoaiPhiEnum.THUE_THANG,
            so_tien=1800000.0, ky_thanh_toan='2024-04', ngay_den_han=date(2024, 4, 20),
            phuong_thuc='chuyen_khoan', trang_thai=TrangThaiTTEnum.QUA_HAN,
            phi_phat=50000.0
        ),
        ThanhToan(
            ma_thanh_toan='TT005', ma_hop_dong='HD004', loai_phi=LoaiPhiEnum.TIEN_COC,
            so_tien=3800000.0, ngay_den_han=date(2024, 5, 10),
            ngay_thanh_toan=date(2024, 5, 8), phuong_thuc='tien_mat',
            so_giao_dich='TM001', trang_thai=TrangThaiTTEnum.DA_THANH_TOAN
        ),
        ThanhToan(
            ma_thanh_toan='TT006', ma_hop_dong='HD005', loai_phi=LoaiPhiEnum.THUE_THANG,
            so_tien=1650000.0, ky_thanh_toan='2024-07', ngay_den_han=date(2024, 7, 25),
            ngay_thanh_toan=date(2024, 7, 26), phuong_thuc='chuyen_khoan',
            so_giao_dich='CK004', trang_thai=TrangThaiTTEnum.DA_THANH_TOAN
        ),
        ThanhToan(
            ma_thanh_toan='TT007', ma_hop_dong='HD006', loai_phi=LoaiPhiEnum.PHU_PHI,
            so_tien=500000.0, ngay_den_han=date(2024, 9, 5),
            ngay_thanh_toan=date(2024, 9, 4), phuong_thuc='chuyen_khoan',
            so_giao_dich='CK005', trang_thai=TrangThaiTTEnum.DA_THANH_TOAN,
            ghi_chu='Phí vận chuyển nội bộ'
        ),
        ThanhToan(
            ma_thanh_toan='TT008', ma_hop_dong='HD008', loai_phi=LoaiPhiEnum.TIEN_COC,
            so_tien=3100000.0, ngay_den_han=date(2024, 10, 1),
            ngay_thanh_toan=date(2024, 9, 30), phuong_thuc='chuyen_khoan',
            so_giao_dich='CK006', trang_thai=TrangThaiTTEnum.DA_THANH_TOAN
        ),
        ThanhToan(
            ma_thanh_toan='TT009', ma_hop_dong='HD009', loai_phi=LoaiPhiEnum.THUE_THANG,
            so_tien=1600000.0, ky_thanh_toan='2024-11', ngay_den_han=date(2024, 11, 10),
            phuong_thuc='chuyen_khoan', trang_thai=TrangThaiTTEnum.CHUA_THANH_TOAN
        ),
        ThanhToan(
            ma_thanh_toan='TT010', ma_hop_dong='HD010', loai_phi=LoaiPhiEnum.PHI_PHAT,
            so_tien=200000.0, ngay_den_han=date(2024, 12, 20),
            ngay_thanh_toan=date(2024, 12, 18), phuong_thuc='chuyen_khoan',
            so_giao_dich='CK007', trang_thai=TrangThaiTTEnum.DA_THANH_TOAN,
            ghi_chu='Phạt giao hàng trễ'
        ),
    ]
    
    for tt in thanh_toans:
        existing = session.query(ThanhToan).filter(ThanhToan.ma_thanh_toan == tt.ma_thanh_toan).first()
        if not existing:
            session.add(tt)
    
    session.commit()
    print(f"  ✅ Added {len(thanh_toans)} ThanhToan")
    return thanh_toans


def seed_system_log(session):
    """Seed 10 system logs"""
    logs = [
        SystemLog(
            ma_nhan_vien='NV001', thoi_gian=datetime(2024, 1, 15, 8, 30),
            hanh_dong=HanhDongLogEnum.THEM, ban_ghi='khach_hang:KH001',
            gia_tri_moi='{"ho_ten": "Nguyễn Văn An"}', ip_address='192.168.1.10'
        ),
        SystemLog(
            ma_nhan_vien='NV002', thoi_gian=datetime(2024, 1, 20, 9, 0),
            hanh_dong=HanhDongLogEnum.THEM, ban_ghi='hop_dong:HD001',
            gia_tri_moi='{"ma_hop_dong": "HD001", "gia_thue": 1500000}',
            ip_address='192.168.1.11'
        ),
        SystemLog(
            ma_nhan_vien='NV001', thoi_gian=datetime(2024, 2, 1, 10, 15),
            hanh_dong=HanhDongLogEnum.DANG_NHAP, ban_ghi='nhan_vien:NV001',
            ip_address='192.168.1.10'
        ),
        SystemLog(
            ma_nhan_vien='NV003', thoi_gian=datetime(2024, 3, 5, 14, 30),
            hanh_dong=HanhDongLogEnum.SUA, ban_ghi='khach_hang:KH002',
            gia_tri_cu='{"so_dien_thoai": "0902000002"}',
            gia_tri_moi='{"so_dien_thoai": "0902000003"}',
            ip_address='192.168.1.12'
        ),
        SystemLog(
            ma_nhan_vien='NV004', thoi_gian=datetime(2024, 4, 10, 11, 0),
            hanh_dong=HanhDongLogEnum.THEM, ban_ghi='hang_hoa:HH001',
            gia_tri_moi='{"ma_hang_hoa": "HH001", "ten_hang": "Máy tính xách tay"}',
            ip_address='192.168.1.13'
        ),
        SystemLog(
            ma_nhan_vien='NV005', thoi_gian=datetime(2024, 5, 15, 16, 45),
            hanh_dong=HanhDongLogEnum.XOA, ban_ghi='hop_dong:HD007',
            gia_tri_cu='{"ma_hop_dong": "HD007", "trang_thai": "hieu_luc"}',
            gia_tri_moi='{"trang_thai": "cham_dut"}',
            ip_address='192.168.1.14'
        ),
        SystemLog(
            ma_nhan_vien='NV002', thoi_gian=datetime(2024, 6, 20, 8, 30),
            hanh_dong=HanhDongLogEnum.THEM, ban_ghi='thanh_toan:TT001',
            gia_tri_moi='{"ma_thanh_toan": "TT001", "so_tien": 3000000}',
            ip_address='192.168.1.11'
        ),
        SystemLog(
            ma_nhan_vien='NV001', thoi_gian=datetime(2024, 7, 25, 17, 0),
            hanh_dong=HanhDongLogEnum.DANG_XUAT, ban_ghi='nhan_vien:NV001',
            ip_address='192.168.1.10'
        ),
        SystemLog(
            ma_nhan_vien='NV006', thoi_gian=datetime(2024, 8, 30, 13, 30),
            hanh_dong=HanhDongLogEnum.SUA, ban_ghi='kho:KHO001',
            gia_tri_cu='{"da_su_dung": 2000}',
            gia_tri_moi='{"da_su_dung": 2500}',
            ip_address='192.168.1.15'
        ),
        SystemLog(
            ma_nhan_vien='NV007', thoi_gian=datetime(2024, 9, 15, 10, 0),
            hanh_dong=HanhDongLogEnum.THEM, ban_ghi='vi_tri:K01-A-01-02',
            gia_tri_moi='{"ma_vi_tri": "K01-A-01-02", "trang_thai": "trong"}',
            ip_address='192.168.1.16'
        ),
    ]
    
    for log in logs:
        try:
            session.add(log)
        except:
            pass
    
    session.commit()
    print(f"  ✅ Added {len(logs)} SystemLog")
    return logs


def seed_bao_cao(session):
    """Seed 10 báo cáo"""
    bao_caos = [
        BaoCao(
            ma_bao_cao='BC001', nguoi_tao='NV001', loai_bao_cao='Báo cáo tồn kho',
            ngay_bat_dau=date(2024, 1, 1), ngay_ket_thuc=date(2024, 1, 31),
            du_lieu='{"tong_hang_hoa": 100, "tong_gia_tri": 500000000}',
            file_path='/reports/ton_kho_012024.pdf', trang_thai='hoan_thanh'
        ),
        BaoCao(
            ma_bao_cao='BC002', nguoi_tao='NV002', loai_bao_cao='Báo cáo doanh thu',
            ngay_bat_dau=date(2024, 1, 1), ngay_ket_thuc=date(2024, 3, 31),
            du_lieu='{"tong_doanh_thu": 150000000, "so_ hop_dong": 5}',
            file_path='/reports/doanh_thu_q1_2024.pdf', trang_thai='hoan_thanh'
        ),
        BaoCao(
            ma_bao_cao='BC003', nguoi_tao='NV003', loai_bao_cao='Báo cáo công nợ',
            ngay_bat_dau=date(2024, 4, 1), ngay_ket_thuc=date(2024, 4, 30),
            du_lieu='{"tong_cong_no": 25000000, "so_khach_no": 3}',
            file_path='/reports/cong_no_042024.pdf', trang_thai='hoan_thanh'
        ),
        BaoCao(
            ma_bao_cao='BC004', nguoi_tao='NV001', loai_bao_cao='Báo cáo hợp đồng',
            ngay_bat_dau=date(2024, 5, 1), ngay_ket_thuc=date(2024, 5, 31),
            du_lieu='{"tong_hop_dong": 8, "hop_dong_moi": 2, "hop_dong_het_han": 1}',
            file_path='/reports/hop_dong_052024.pdf', trang_thai='hoan_thanh'
        ),
        BaoCao(
            ma_bao_cao='BC005', nguoi_tao='NV004', loai_bao_cao='Báo cáo tồn kho',
            ngay_bat_dau=date(2024, 6, 1), ngay_ket_thuc=date(2024, 6, 30),
            du_lieu='{"tong_hang_hoa": 120, "tong_gia_tri": 620000000}',
            file_path='/reports/ton_kho_062024.pdf', trang_thai='hoan_thanh'
        ),
        BaoCao(
            ma_bao_cao='BC006', nguoi_tao='NV002', loai_bao_cao='Báo cáo doanh thu',
            ngay_bat_dau=date(2024, 4, 1), ngay_ket_thuc=date(2024, 6, 30),
            du_lieu='{"tong_doanh_thu": 450000000, "so_hop_dong": 12}',
            file_path='/reports/doanh_thu_q2_2024.pdf', trang_thai='hoan_thanh'
        ),
        BaoCao(
            ma_bao_cao='BC007', nguoi_tao='NV005', loai_bao_cao='Báo cáo khách hàng',
            ngay_bat_dau=date(2024, 7, 1), ngay_ket_thuc=date(2024, 7, 31),
            du_lieu='{"tong_khach_hang": 10, "khach_moi": 2, "khach_xoa": 1}',
            file_path='/reports/khach_hang_072024.pdf', trang_thai='dang_xu_ly'
        ),
        BaoCao(
            ma_bao_cao='BC008', nguoi_tao='NV001', loai_bao_cao='Báo cáo tồn kho',
            ngay_bat_dau=date(2024, 8, 1), ngay_ket_thuc=date(2024, 8, 31),
            du_lieu='{"tong_hang_hoa": 115, "tong_gia_tri": 590000000}',
            file_path='/reports/ton_kho_082024.pdf', trang_thai='hoan_thanh'
        ),
        BaoCao(
            ma_bao_cao='BC009', nguoi_tao='NV006', loai_bao_cao='Báo cáo công nợ',
            ngay_bat_dau=date(2024, 9, 1), ngay_ket_thuc=date(2024, 9, 30),
            du_lieu='{"tong_cong_no": 18000000, "so_khach_no": 2}',
            file_path='/reports/cong_no_092024.pdf', trang_thai='hoan_thanh'
        ),
        BaoCao(
            ma_bao_cao='BC010', nguoi_tao='NV002', loai_bao_cao='Báo cáo doanh thu',
            ngay_bat_dau=date(2024, 7, 1), ngay_ket_thuc=date(2024, 9, 30),
            du_lieu='{"tong_doanh_thu": 680000000, "so_hop_dong": 15}',
            file_path='/reports/doanh_thu_q3_2024.pdf', trang_thai='dang_xu_ly'
        ),
    ]
    
    for bc in bao_caos:
        existing = session.query(BaoCao).filter(BaoCao.ma_bao_cao == bc.ma_bao_cao).first()
        if not existing:
            session.add(bc)
    
    session.commit()
    print(f"  ✅ Added {len(bao_caos)} BaoCao")
    return bao_caos


def main():
    print("=" * 60)
    print("SEED DATA - Thêm dữ liệu mẫu")
    print("=" * 60)
    
    # Get database connection
    conn = get_connection()
    session = conn.get_session()
    auth_service = AuthService()
    
    try:
        print("\n📊 Đang thêm dữ liệu mẫu...")
        
        seed_nhan_vien(session, auth_service)
        seed_kho(session)
        seed_vi_tri(session)
        seed_khach_hang(session)
        seed_hop_dong(session)
        seed_hang_hoa(session)
        seed_thanh_toan(session)
        seed_system_log(session)
        seed_bao_cao(session)
        
        print("\n" + "=" * 60)
        print("✅ HOÀN THÀNH SEED DATA!")
        print("=" * 60)
        
    except Exception as e:
        session.rollback()
        print(f"\n❌ Lỗi: {e}")
        raise
    finally:
        session.close()


if __name__ == "__main__":
    main()
