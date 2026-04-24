"""
Models package - Export tất cả models
"""
from .base import Base, BaseModel
from .khach_hang import KhachHang, LoaiKhachEnum, TrangThaiKHEnum
from .kho import Kho, TrangThaiKhoEnum
from .vi_tri import ViTri, TrangThaiViTriEnum
from .hop_dong import HopDong, TrangThaiHDEnum
from .hang_hoa import HangHoa
from .thanh_toan import ThanhToan, LoaiPhiEnum, TrangThaiTTEnum
from .nhan_vien import NhanVien, VaiTroNVEuum
from .system_log import SystemLog, HanhDongLogEnum
from .bao_cao import BaoCao

# Import relationships
from sqlalchemy.orm import relationship

# Setup relationships (import after all models are defined)
def setup_relationships():
    """
    Setup relationships giữa các models
    """
    # KhachHang -> HopDong
    from .khach_hang import KhachHang
    from .hop_dong import HopDong
    KhachHang.hop_dongs = relationship("HopDong", back_populates="khach_hang", cascade="all, delete-orphan")
    
    # Kho -> ViTri
    from .kho import Kho
    from .vi_tri import ViTri
    Kho.vi_tris = relationship("ViTri", back_populates="kho", cascade="all, delete-orphan")
    
    # ViTri -> HopDong
    ViTri.hop_dongs = relationship("HopDong", back_populates="vi_tri")
    
    # HopDong -> HangHoa, ThanhToan
    HopDong.hang_hoas = relationship("HangHoa", back_populates="hop_dong", cascade="all, delete-orphan")
    HopDong.thanh_toans = relationship("ThanhToan", back_populates="hop_dong")
    
    # HangHoa -> HopDong (already defined in model)
    # ThanhToan -> HopDong (already defined in model)

# Call setup_relationships() để config relationships
setup_relationships()

__all__ = [
    # Base
    'Base',
    'BaseModel',
    
    # Models
    'KhachHang',
    'Kho',
    'ViTri',
    'HopDong',
    'HangHoa',
    'ThanhToan',
    'NhanVien',
    'SystemLog',
    'BaoCao',
    
    # Enums
    'LoaiKhachEnum',
    'TrangThaiKHEnum',
    'TrangThaiKhoEnum',
    'TrangThaiViTriEnum',
    'TrangThaiHDEnum',
    'LoaiPhiEnum',
    'TrangThaiTTEnum',
    'VaiTroNVEuum',
    'HanhDongLogEnum',
]
