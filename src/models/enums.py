"""
Centralized Enum Definitions

All enums in the project are centralized here to avoid duplication
and ensure consistency across services and models.
"""
import enum


# ==================== Contract Status ====================

class TrangThaiHDEnum(enum.Enum):
    """Trạng thái hợp đồng"""
    HIEU_LUC = 'hieu_luc'
    HET_HAN = 'het_han'
    CHAM_DUT = 'cham_dut'
    GIA_HAN = 'gia_han'


# ==================== Payment Status ====================

class TrangThaiTTEnum(enum.Enum):
    """Trạng thái thanh toán"""
    DA_THANH_TOAN = 'da_thanh_toan'
    CHUA_THANH_TOAN = 'chua_thanh_toan'
    QUA_HAN = 'qua_han'


# ==================== Position Status ====================

class TrangThaiViTriEnum(enum.Enum):
    """Trạng thái vị trí"""
    TRONG = 'trong'
    DA_THUE = 'da_thue'
    BAO_TRI = 'bao_tri'


# ==================== Warehouse Status ====================

class TrangThaiKhoEnum(enum.Enum):
    """Trạng thái kho"""
    HOAT_DONG = 'hoat_dong'
    BAO_TRI = 'bao_tri'
    NGUNG = 'ngung'


# ==================== Customer ====================

class LoaiKhachEnum(enum.Enum):
    """Loại khách hàng"""
    CA_NHAN = 'ca_nhan'
    DOANH_NGHIEP = 'doanh_nghiep'


class TrangThaiKHEnum(enum.Enum):
    """Trạng thái khách hàng"""
    HOAT_DONG = 'hoat_dong'
    TAM_KHOA = 'tam_khoa'
    DA_XOA = 'da_xoa'


# ==================== Payment Types ====================

class LoaiPhiEnum(enum.Enum):
    """Loại phí thanh toán"""
    TIEN_COC = 'tien_coc'
    THUE_THANG = 'thue_thang'
    PHU_PHI = 'phu_phi'
    PHI_PHAT = 'phi_phat'


# ==================== Goods Status ====================

class TrangThaiHHEnum(enum.Enum):
    """Trạng thái hàng hóa"""
    TRONG_KHO = 'trong_kho'
    DA_XUAT = 'da_xuat'


# ==================== Employee ====================

class VaiTroNhanVienEnum(enum.Enum):
    """Vai trò nhân viên"""
    QUAN_TRI = 'quan_tri'
    KINH_DOANH = 'kinh_doanh'
    KHO = 'kho'
    KE_TOAN = 'ke_toan'


class TrangThaiNhanVienEnum(enum.Enum):
    """Trạng thái nhân viên"""
    HOAT_DONG = 'hoat_dong'
    NGUNG_HOAT_DONG = 'ngung_hoat_dong'


# ==================== System Log ====================

class HanhDongLogEnum(enum.Enum):
    """Hành động log"""
    THEM = 'them'
    SUA = 'sua'
    XOA = 'xoa'
    DANG_NHAP = 'dang_nhap'
    DANG_XUAT = 'dang_xuat'