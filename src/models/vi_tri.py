"""
Vị trí lưu trữ model
"""
import enum
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Enum
from sqlalchemy.orm import relationship
from .base import BaseModel

class TrangThaiViTriEnum(enum.Enum):
    """Trạng thái vị trí"""
    TRONG = 'trong'
    DA_THUE = 'da_thue'
    BAO_TRI = 'bao_tri'

class ViTri(BaseModel):
    """
    Vị trí lưu trữ trong kho
    """
    __tablename__ = 'vi_tri'
    
    # Primary Key
    ma_vi_tri = Column(String(30), primary_key=True)
    
    # Foreign Keys
    ma_kho = Column(String(20), ForeignKey('kho.ma_kho', ondelete='RESTRICT'), nullable=False)
    
    # Fields
    khu_vuc = Column(String(50), nullable=False)
    hang = Column(String(10), nullable=False)
    tang = Column(Integer, nullable=False, default=1)
    dien_tich = Column(Float, nullable=False)
    gia_thue = Column(Float, nullable=False)
    suc_chua = Column(Float)
    trang_thai = Column(Enum(TrangThaiViTriEnum), nullable=False, default=TrangThaiViTriEnum.TRONG)
    
    # Relationships
    kho = relationship("Kho", back_populates="vi_tris")
    
    def __repr__(self):
        return f"<ViTri(ma_vi_tri='{self.ma_vi_tri}', khu_vuc='{self.khu_vuc}')>"
