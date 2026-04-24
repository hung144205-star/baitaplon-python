#!/usr/bin/env python3
"""
Fix enum case issues in database
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.database import get_session, DatabaseConnection
from sqlalchemy import text

def fix_enum_cases():
    """Fix enum case issues in database"""
    session = get_session()
    
    try:
        # Fix KhachHang loai_khach enum values
        print("Fixing KhachHang loai_khach values...")
        
        # Update lowercase to uppercase with underscore
        updates = [
            ("UPDATE khach_hang SET loai_khach = 'CA_NHAN' WHERE loai_khach = 'ca_nhan'"),
            ("UPDATE khach_hang SET loai_khach = 'DOANH_NGHIEP' WHERE loai_khach = 'doanh_nghiep'"),
            ("UPDATE khach_hang SET loai_khach = 'HO_KINH_DANH' WHERE loai_khach = 'ho_kinh_danh'"),
        ]
        
        for sql in updates:
            result = session.execute(text(sql))
            if result.rowcount > 0:
                print(f"  Updated {result.rowcount} rows")
        
        # Fix KhachHang trang_thai enum values
        print("\nFixing KhachHang trang_thai values...")
        trang_thai_updates = [
            ("UPDATE khach_hang SET trang_thai = 'HOAT_DONG' WHERE trang_thai = 'hoat_dong'"),
            ("UPDATE khach_hang SET trang_thai = 'NGUNG_HOAT_DONG' WHERE trang_thai = 'ngung_hoat_dong'"),
            ("UPDATE khach_hang SET trang_thai = 'DA_XOA' WHERE trang_thai = 'da_xoa'"),
        ]
        
        for sql in trang_thai_updates:
            result = session.execute(text(sql))
            if result.rowcount > 0:
                print(f"  Updated {result.rowcount} rows")
        
        # Fix Kho trang_thai enum values
        print("\nFixing Kho trang_thai values...")
        kho_updates = [
            ("UPDATE kho SET trang_thai = 'HOAT_DONG' WHERE trang_thai = 'hoat_dong'"),
            ("UPDATE kho SET trang_thai = 'BAO_TRI' WHERE trang_thai = 'bao_tri'"),
            ("UPDATE kho SET trang_thai = 'NGUNG' WHERE trang_thai = 'ngung'"),
        ]
        
        for sql in kho_updates:
            result = session.execute(text(sql))
            if result.rowcount > 0:
                print(f"  Updated {result.rowcount} rows")
        
        # Fix ViTri trang_thai enum values
        print("\nFixing ViTri trang_thai values...")
        vi_tri_updates = [
            ("UPDATE vi_tri SET trang_thai = 'TRONG' WHERE trang_thai = 'trong'"),
            ("UPDATE vi_tri SET trang_thai = 'DA_THUE' WHERE trang_thai = 'da_thue'"),
            ("UPDATE vi_tri SET trang_thai = 'BAO_TRI' WHERE trang_thai = 'bao_tri'"),
        ]
        
        for sql in vi_tri_updates:
            result = session.execute(text(sql))
            if result.rowcount > 0:
                print(f"  Updated {result.rowcount} rows")
        
        # Fix HopDong trang_thai enum values
        print("\nFixing HopDong trang_thai values...")
        hop_dong_updates = [
            ("UPDATE hop_dong SET trang_thai = 'HIEU_LUC' WHERE trang_thai = 'hieu_luc'"),
            ("UPDATE hop_dong SET trang_thai = 'HET_HAN' WHERE trang_thai = 'het_han'"),
            ("UPDATE hop_dong SET trang_thai = 'CHAM_DUT' WHERE trang_thai = 'cham_dut'"),
            ("UPDATE hop_dong SET trang_thai = 'GIA_HAN' WHERE trang_thai = 'gia_han'"),
        ]
        
        for sql in hop_dong_updates:
            result = session.execute(text(sql))
            if result.rowcount > 0:
                print(f"  Updated {result.rowcount} rows")
        
        # Fix HangHoa trang_thai enum values
        print("\nFixing HangHoa trang_thai values...")
        hang_hoa_updates = [
            ("UPDATE hang_hoa SET trang_thai = 'TRONG_KHO' WHERE trang_thai = 'trong_kho'"),
            ("UPDATE hang_hoa SET trang_thai = 'DA_XUAT' WHERE trang_thai = 'da_xuat'"),
        ]
        
        for sql in hang_hoa_updates:
            result = session.execute(text(sql))
            if result.rowcount > 0:
                print(f"  Updated {result.rowcount} rows")
        
        # Commit changes
        session.commit()
        print("\n✅ All enum values fixed successfully!")
        
    except Exception as e:
        session.rollback()
        print(f"\n❌ Error: {e}")
        raise
    finally:
        session.close()


if __name__ == '__main__':
    print("🔧 Fixing enum case issues in database...\n")
    fix_enum_cases()
    print("\n✨ Done!")
