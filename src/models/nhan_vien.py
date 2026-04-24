"""
Nhân viên model
"""
import enum
from sqlalchemy import Column, String, Enum, Text
from .base import BaseModel

class VaiTroNVEuum(enum.Enum):
    """Vai trò nhân viên"""
    QUAN_TRI = 'quan_tri'
    KINH_DOANH = 'kinh_doanh'
    KHO = 'kho'
    KE_TOAN = 'ke_toan'

class NhanVien(BaseModel):
    """
    Nhân viên hệ thống
    """
    __tablename__ = 'nhan_vien'
    
    # Primary Key
    ma_nhan_vien = Column(String(20), primary_key=True)
    
    # Fields
    ho_ten = Column(String(200), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    so_dien_thoai = Column(String(20))
    vai_tro = Column(Enum(VaiTroNVEuum), nullable=False)
    tai_khoan = Column(String(50), unique=True, nullable=False)
    mat_khau = Column(String(255), nullable=False)  # bcrypt hash
    trang_thai = Column(String(20), nullable=False, default='hoat_dong')
    lan_dang_nhap_cuoi = Column(String(50))
    
    def __repr__(self):
        return f"<NhanVien(ma_nhan_vien='{self.ma_nhan_vien}', tai_khoan='{self.tai_khoan}')>"
