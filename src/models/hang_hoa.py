"""
Hàng hóa model
"""
from sqlalchemy import Column, String, Integer, Float, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import BaseModel

class HangHoa(BaseModel):
    """
    Hàng hóa trong kho
    """
    __tablename__ = 'hang_hoa'
    
    # Primary Key
    ma_hang_hoa = Column(String(30), primary_key=True)
    
    # Foreign Keys
    ma_hop_dong = Column(String(20), ForeignKey('hop_dong.ma_hop_dong', ondelete='CASCADE'), nullable=False)
    
    # Fields
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
    hinh_anh = Column(Text)  # JSON array of image paths
    
    # Relationships
    hop_dong = relationship("HopDong", back_populates="hang_hoas")
    
    def __repr__(self):
        return f"<HangHoa(ma_hang_hoa='{self.ma_hang_hoa}', ten_hang='{self.ten_hang}')>"
