"""
Services package - Business logic layer
"""
from .khach_hang_service import (
    KhachHangService,
    create_khach_hang,
    get_khach_hang,
    get_all_khach_hang,
    search_khach_hang,
)
from .kho_service import KhoService, create_kho, get_kho, get_all_kho
from .vi_tri_service import ViTriService, create_vi_tri, get_vi_tri, get_vi_tri_by_kho
from .hop_dong_service import (
    HopDongService,
    TrangThaiHDEnum,
    create_hop_dong,
    get_hop_dong_by_id,
    get_all_hop_dongs,
    get_hop_dongs_by_customer,
    get_expiring_contracts,
)
from .hang_hoa_service import (
    HangHoaService,
    create_hang_hoa,
    get_hang_hoa_by_id,
    get_hang_hoa_by_contract,
    get_inventory,
    import_goods,
    export_goods,
)
from .thanh_toan_service import ThanhToanService, TrangThaiTTEnum
from .hop_dong_history_service import HopDongHistoryService, EventType, HopDongHistory
from .inventory_service import InventoryService
from .report_service import ReportService, ReportType
from .base_service import BaseService
from .transaction_context import TransactionContext, tx, transactional
from .loai_hang_service import (
    LoaiHangService,
    create_loai_hang,
    get_loai_hang,
    get_all_loai_hangs,
    update_loai_hang,
    delete_loai_hang,
)

__all__ = [
    # Base classes
    'BaseService',
    'TransactionContext',
    'tx',
    'transactional',

    # Services
    'KhachHangService',
    'KhoService',
    'ViTriService',
    'HopDongService',
    'HangHoaService',
    'LoaiHangService',
    'ThanhToanService',
    'HopDongHistoryService',
    'InventoryService',
    'ReportService',

    # Enums
    'TrangThaiHDEnum',
    'TrangThaiTTEnum',
    'EventType',
    'ReportType',

    # Convenience functions
    'create_khach_hang',
    'get_khach_hang',
    'get_all_khach_hang',
    'search_khach_hang',
    'create_kho',
    'get_kho',
    'get_all_kho',
    'create_vi_tri',
    'get_vi_tri',
    'get_vi_tri_by_kho',
    'create_hop_dong',
    'get_hop_dong_by_id',
    'get_all_hop_dongs',
    'get_hop_dongs_by_customer',
    'get_expiring_contracts',
    'create_hang_hoa',
    'get_hang_hoa_by_id',
    'get_hang_hoa_by_contract',
    'get_inventory',
    'import_goods',
    'export_goods',
    'create_loai_hang',
    'get_loai_hang',
    'get_all_loai_hangs',
    'update_loai_hang',
    'delete_loai_hang',
]
