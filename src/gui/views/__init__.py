"""
Views package - Main screens
"""
from .khach_hang_view import KhachHangView
from .khach_hang_detail_view import KhachHangDetailView as KhachHangDetailFullView, KhachHangDetailWidget
from .kho_view import KhoView, ViTriSubView
from .vi_tri_view import ViTriView, ViTriDetailView
from .dashboard_view import DashboardView
from .hop_dong_view import HopDongView
from .hop_dong_detail_view import HopDongDetailView, HopDongDetailWidget
from .hang_hoa_view import HangHoaView
from .thanh_toan_view import ThanhToanView
from .bao_cao_view import BaoCaoView
from .help_view import HelpView
from .settings_view import SettingsView

__all__ = [
    # Customer
    'KhachHangView',
    'KhachHangDetailFullView',
    'KhachHangDetailWidget',
    # Warehouse
    'KhoView',
    'ViTriSubView',
    'ViTriView',
    'ViTriDetailView',
    # Dashboard
    'DashboardView',
    # Contract
    'HopDongView',
    'HopDongDetailView',
    'HopDongDetailWidget',
    # Goods
    'HangHoaView',
    # Payment
    'ThanhToanView',
    # Report
    'BaoCaoView',
    # Help & Settings
    'HelpView',
    'SettingsView',
]
