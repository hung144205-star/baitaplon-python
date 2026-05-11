"""
Khách hàng model
"""
from sqlalchemy import Column, String, Date, Enum
from sqlalchemy.orm import relationship
from datetime import date
from .base import BaseModel
from .enums import LoaiKhachEnum, TrangThaiKHEnum

class KhachHang(BaseModel):
    """
    Khách hàng thuê kho
    """
    __tablename__ = 'khach_hang'
    
    # Primary Key
    ma_khach_hang = Column(String(20), primary_key=True)
    
    # Fields
    ho_ten = Column(String(200), nullable=False)
    loai_khach = Column(
        Enum(LoaiKhachEnum, values_callable=lambda x: [e.value for e in x], native_enum=False),
        nullable=False,
        default=LoaiKhachEnum.CA_NHAN,
    )
    so_dien_thoai = Column(String(20), nullable=False)
    email = Column(String(100), unique=True)
    dia_chi = Column(String(500), nullable=False)
    ma_so_thue = Column(String(20))
    ngay_dang_ky = Column(Date, nullable=False, default=date.today)
    trang_thai = Column(
        Enum(TrangThaiKHEnum, values_callable=lambda x: [e.value for e in x], native_enum=False),
        nullable=False,
        default=TrangThaiKHEnum.HOAT_DONG,
    )
    
    # Relationships
    hop_dongs = relationship("HopDong", back_populates="khach_hang", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<KhachHang(ma_khach_hang='{self.ma_khach_hang}', ho_ten='{self.ho_ten}')>"
