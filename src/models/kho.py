"""
Kho hàng model
"""
import enum
from sqlalchemy import Column, String, Float, Enum
from .base import BaseModel

class TrangThaiKhoEnum(enum.Enum):
    """Trạng thái kho"""
    HOAT_DONG = 'hoat_dong'
    BAO_TRI = 'bao_tri'
    NGUNG = 'ngung'

class Kho(BaseModel):
    """
    Kho hàng
    """
    __tablename__ = 'kho'
    
    # Primary Key
    ma_kho = Column(String(20), primary_key=True)
    
    # Fields
    ten_kho = Column(String(200), nullable=False)
    dia_chi = Column(String(500), nullable=False)
    dien_tich = Column(Float, nullable=False)
    suc_chua = Column(Float, nullable=False)
    da_su_dung = Column(Float, nullable=False, default=0)
    trang_thai = Column(
        Enum(TrangThaiKhoEnum, values_callable=lambda x: [e.value for e in x], native_enum=False),
        nullable=False,
        default=TrangThaiKhoEnum.HOAT_DONG,
    )
    
    @property
    def ty_le_lap_day(self):
        """Tính tỷ lệ lấp đầy (%)"""
        if self.suc_chua == 0:
            return 0
        return (self.da_su_dung / self.suc_chua) * 100
    
    @property
    def dung_tich_con_lai(self):
        """Tính dung tích còn lại"""
        return self.suc_chua - self.da_su_dung
    
    def __repr__(self):
        return f"<Kho(ma_kho='{self.ma_kho}', ten_kho='{self.ten_kho}')>"
