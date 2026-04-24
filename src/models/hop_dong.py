"""
Hợp đồng thuê model
"""
import enum
from sqlalchemy import Column, String, Date, Float, Enum, ForeignKey, Text
from sqlalchemy.orm import relationship
from .base import BaseModel

class TrangThaiHDEnum(enum.Enum):
    """Trạng thái hợp đồng"""
    HIEU_LUC = 'hieu_luc'
    HET_HAN = 'het_han'
    CHAM_DUT = 'cham_dut'
    GIA_HAN = 'gia_han'

class HopDong(BaseModel):
    """
    Hợp đồng thuê kho
    """
    __tablename__ = 'hop_dong'
    
    # Primary Key
    ma_hop_dong = Column(String(20), primary_key=True)
    
    # Foreign Keys
    ma_khach_hang = Column(String(20), ForeignKey('khach_hang.ma_khach_hang'), nullable=False)
    ma_vi_tri = Column(String(30), ForeignKey('vi_tri.ma_vi_tri'), nullable=False)
    
    # Fields
    ngay_bat_dau = Column(Date, nullable=False)
    ngay_ket_thuc = Column(Date, nullable=False)
    gia_thue = Column(Float, nullable=False)
    tien_coc = Column(Float, nullable=False, default=0)
    phuong_thuc_thanh_toan = Column(String(20), default='hang_thang')
    dieu_khoan = Column(Text)
    trang_thai = Column(Enum(TrangThaiHDEnum), nullable=False, default=TrangThaiHDEnum.HIEU_LUC)
    ly_do_cham_dut = Column(Text)
    ngay_cham_dut = Column(Date)
    
    # Relationships
    khach_hang = relationship("KhachHang", back_populates="hop_dongs")
    vi_tri = relationship("ViTri", back_populates="hop_dongs")
    hang_hoas = relationship("HangHoa", back_populates="hop_dong", cascade="all, delete-orphan")
    thanh_toans = relationship("ThanhToan", back_populates="hop_dong")
    
    def __repr__(self):
        return f"<HopDong(ma_hop_dong='{self.ma_hop_dong}', trang_thai='{self.trang_thai}')>"
