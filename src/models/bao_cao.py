"""
Báo cáo model
"""
from sqlalchemy import Column, String, Date, Text, ForeignKey
from .base import BaseModel

class BaoCao(BaseModel):
    """
    Báo cáo
    """
    __tablename__ = 'bao_cao'
    
    # Primary Key
    ma_bao_cao = Column(String(30), primary_key=True)
    
    # Foreign Keys
    nguoi_tao = Column(String(20), ForeignKey('nhan_vien.ma_nhan_vien', ondelete='SET NULL'))
    
    # Fields
    loai_bao_cao = Column(String(50), nullable=False)
    ngay_bat_dau = Column(Date, nullable=False)
    ngay_ket_thuc = Column(Date, nullable=False)
    du_lieu = Column(Text)  # JSON
    file_path = Column(String(500))
    trang_thai = Column(String(20), nullable=False, default='hoan_thanh')
    ghi_chu = Column(Text)
    
    def __repr__(self):
        return f"<BaoCao(ma_bao_cao='{self.ma_bao_cao}', loai_bao_cao='{self.loai_bao_cao}')>"
