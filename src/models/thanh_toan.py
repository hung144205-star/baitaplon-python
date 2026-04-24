"""
Thanh toán model
"""
import enum
from sqlalchemy import Column, String, Float, Date, Enum, ForeignKey, Text
from sqlalchemy.orm import relationship
from .base import BaseModel

class LoaiPhiEnum(enum.Enum):
    """Loại phí thanh toán"""
    TIEN_COC = 'tien_coc'
    THUE_THANG = 'thue_thang'
    PHU_PHI = 'phu_phi'
    PHI_PHAT = 'phi_phat'

class TrangThaiTTEnum(enum.Enum):
    """Trạng thái thanh toán"""
    DA_THANH_TOAN = 'da_thanh_toan'
    CHUA_THANH_TOAN = 'chua_thanh_toan'
    QUA_HAN = 'qua_han'

class ThanhToan(BaseModel):
    """
    Thanh toán
    """
    __tablename__ = 'thanh_toan'
    
    # Primary Key
    ma_thanh_toan = Column(String(30), primary_key=True)
    
    # Foreign Keys
    ma_hop_dong = Column(String(20), ForeignKey('hop_dong.ma_hop_dong'), nullable=False)
    
    # Fields
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
    
    # Relationships
    hop_dong = relationship("HopDong", back_populates="thanh_toans")
    
    def __repr__(self):
        return f"<ThanhToan(ma_thanh_toan='{self.ma_thanh_toan}', so_tien={self.so_tien})>"
