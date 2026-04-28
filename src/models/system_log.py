"""
System log model
"""
import enum
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Enum
from .base import BaseModel

class HanhDongLogEnum(enum.Enum):
    """Hành động log"""
    THEM = 'THEM'
    SUA = 'SUA'
    XOA = 'XOA'
    DANG_NHAP = 'DANG_NHAP'
    DANG_XUAT = 'DANG_XUAT'

class SystemLog(BaseModel):
    """
    Audit log hệ thống
    """
    __tablename__ = 'system_log'
    
    # Primary Key
    ma_log = Column(Integer, primary_key=True, autoincrement=True)
    
    # Foreign Keys
    ma_nhan_vien = Column(String(20), ForeignKey('nhan_vien.ma_nhan_vien', ondelete='SET NULL'))
    
    # Fields
    thoi_gian = Column(DateTime, nullable=False)
    hanh_dong = Column(
        Enum(HanhDongLogEnum, values_callable=lambda x: [e.value for e in x], native_enum=False),
        nullable=False,
    )
    ban_ghi = Column(String(100), nullable=False)
    gia_tri_cu = Column(Text)  # JSON
    gia_tri_moi = Column(Text)  # JSON
    ip_address = Column(String(45))
    ghi_chu = Column(Text)
    
    def __repr__(self):
        return f"<SystemLog(ma_log={self.ma_log}, hanh_dong='{self.hanh_dong}')>"
