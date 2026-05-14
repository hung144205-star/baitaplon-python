"""
Loại hàng hóa model
"""
from sqlalchemy import Column, String, Text
from .base import BaseModel


class LoaiHang(BaseModel):
    """
    Loại hàng hóa
    """
    __tablename__ = 'loai_hang'

    # Primary Key
    ma_loai = Column(String(30), primary_key=True)

    # Fields
    ten_loai = Column(String(100), nullable=False)
    mo_ta = Column(Text)
    ghi_chu = Column(Text)

    def __repr__(self):
        return f"<LoaiHang(ma_loai='{self.ma_loai}', ten_loai='{self.ten_loai}')>"


__all__ = ['LoaiHang']