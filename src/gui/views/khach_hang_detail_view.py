#!/usr/bin/env python3
"""
Khách hàng Detail View - Chi tiết Khách hàng với Tabs
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QTabWidget, QTableWidget, QTableWidgetItem, QHeaderView,
    QGroupBox, QFormLayout, QScrollArea, QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

from src.models import KhachHang, HopDong, ThanhToan, LoaiKhachEnum, TrangThaiKHEnum
from src.services import KhachHangService
from src.gui.widgets import DataTable
from src.gui.dialogs import MessageDialog
from src.utils.formatters import format_currency, format_date, format_phone


class KhachHangDetailView(QWidget):
    """
    Chi tiết Khách hàng với nhiều tabs
    - Tab 1: Thông tin cơ bản
    - Tab 2: Hợp đồng
    - Tab 3: Thanh toán
    - Tab 4: Lịch sử
    """
    
    edit_requested = pyqtSignal(object)  # KhachHang
    close_requested = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.service = KhachHangService()
        self.current_khach_hang: KhachHang = None
        self.setup_ui()
    
    def setup_ui(self):
        """Setup UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Header
        header = self._create_header()
        layout.addWidget(header)
        
        # Tab widget
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid rgba(0, 0, 0, 0.1);
                border-top: none;
                border-radius: 0 0 8px 8px;
            }
            QTabBar::tab {
                background-color: #f6f5f4;
                border: 1px solid rgba(0, 0, 0, 0.1);
                border-bottom: none;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                padding: 10px 20px;
                margin-right: 4px;
                color: #615d59;
                font-weight: 500;
            }
            QTabBar::tab:selected {
                background-color: #ffffff;
                color: #0075de;
            }
            QTabBar::tab:hover:!selected {
                background-color: #eeeeee;
            }
        """)
        
        # Add tabs
        self.tabs.addTab(self._create_thong_tin_tab(), "📋 Thông tin")
        self.tabs.addTab(self._create_hop_dong_tab(), "📄 Hợp đồng")
        self.tabs.addTab(self._create_thanh_toan_tab(), "💰 Thanh toán")
        self.tabs.addTab(self._create_lich_su_tab(), "🕐 Lịch sử")
        
        layout.addWidget(self.tabs, 1)
    
    def _create_header(self) -> QFrame:
        """Create header with customer info and actions"""
        header = QFrame()
        header.setFrameShape(QFrame.Shape.StyledPanel)
        header.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border: 1px solid rgba(0, 0, 0, 0.1);
                border-bottom: none;
                border-radius: 8px 8px 0 0;
                padding: 20px;
            }
        """)
        
        layout = QHBoxLayout(header)
        
        # Avatar placeholder
        avatar = QLabel("👤")
        avatar.setFixedSize(60, 60)
        avatar.setStyleSheet("""
            QLabel {
                background-color: #e3f2fd;
                border-radius: 30px;
                font-size: 32px;
                qproperty-alignment: AlignCenter;
            }
        """)
        layout.addWidget(avatar)
        
        # Customer info
        info_layout = QVBoxLayout()
        info_layout.setSpacing(4)
        
        self.ten_label = QLabel("Chưa chọn khách hàng")
        self.ten_label.setStyleSheet("""
            QLabel {
                font-size: 20px;
                font-weight: 700;
                color: #31302e;
            }
        """)
        info_layout.addWidget(self.ten_label)
        
        self.ma_label = QLabel("Mã: -")
        self.ma_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #615d59;
            }
        """)
        info_layout.addWidget(self.ma_label)
        
        self.sdt_label = QLabel("SĐT: -")
        self.sdt_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #615d59;
            }
        """)
        info_layout.addWidget(self.sdt_label)
        
        self.email_label = QLabel("Email: -")
        self.email_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #615d59;
            }
        """)
        info_layout.addWidget(self.email_label)
        
        layout.addLayout(info_layout, 1)
        
        # Action buttons
        button_layout = QVBoxLayout()
        button_layout.setSpacing(8)
        
        self.edit_btn = QPushButton("✏️ Sửa")
        self.edit_btn.setObjectName("primaryButton")
        self.edit_btn.setFixedWidth(120)
        self.edit_btn.clicked.connect(self._on_edit)
        self.edit_btn.setEnabled(False)
        button_layout.addWidget(self.edit_btn)
        
        self.close_btn = QPushButton("❌ Đóng")
        self.close_btn.setObjectName("secondaryButton")
        self.close_btn.setFixedWidth(120)
        self.close_btn.clicked.connect(self.close_requested.emit)
        button_layout.addWidget(self.close_btn)
        
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
        return header
    
    def _create_thong_tin_tab(self) -> QWidget:
        """Create Thông tin tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(16)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Basic info group
        basic_group = QGroupBox("📌 Thông tin cơ bản")
        basic_group.setStyleSheet("""
            QGroupBox {
                font-weight: 600;
                font-size: 14px;
                color: #31302e;
                border: 1px solid rgba(0, 0, 0, 0.1);
                border-radius: 8px;
                margin-top: 12px;
                padding-top: 12px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                left: 16px;
                padding: 0 8px;
            }
        """)
        
        basic_layout = QFormLayout(basic_group)
        basic_layout.setSpacing(12)
        
        self.info_ma = QLabel("-")
        self.info_loai = QLabel("-")
        self.info_sdt = QLabel("-")
        self.info_email = QLabel("-")
        self.info_dia_chi = QLabel("-")
        self.info_mst = QLabel("-")
        self.info_ngay_dk = QLabel("-")
        self.info_trang_thai = QLabel("-")
        
        for label, widget in [
            ("Mã khách hàng:", self.info_ma),
            ("Loại khách:", self.info_loai),
            ("Số điện thoại:", self.info_sdt),
            ("Email:", self.info_email),
            ("Địa chỉ:", self.info_dia_chi),
            ("Mã số thuế:", self.info_mst),
            ("Ngày đăng ký:", self.info_ngay_dk),
            ("Trạng thái:", self.info_trang_thai),
        ]:
            widget.setStyleSheet("color: #31302e; padding: 4px;")
            basic_layout.addRow(f"<b>{label}</b>", widget)
        
        layout.addWidget(basic_group)
        
        # Statistics group
        stats_group = QGroupBox("📊 Thống kê")
        stats_group.setStyleSheet(basic_group.styleSheet())
        stats_layout = QFormLayout(stats_group)
        stats_layout.setSpacing(12)
        
        self.stats_tong_hd = QLabel("0")
        self.stats_hd_hieu_luc = QLabel("0")
        self.stats_tong_da_tt = QLabel("0 ₫")
        self.stats_tong_cong_no = QLabel("0 ₫")
        
        for label, widget in [
            ("Tổng hợp đồng:", self.stats_tong_hd),
            ("Hợp đồng hiệu lực:", self.stats_hd_hieu_luc),
            ("Tổng đã thanh toán:", self.stats_tong_da_tt),
            ("Tổng công nợ:", self.stats_tong_cong_no),
        ]:
            widget.setStyleSheet("color: #1976d2; font-weight: 600; padding: 4px;")
            stats_layout.addRow(f"<b>{label}</b>", widget)
        
        layout.addWidget(stats_group)
        layout.addStretch()
        
        return widget
    
    def _create_hop_dong_tab(self) -> QWidget:
        """Create Hợp đồng tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Contracts table
        self.hop_dong_table = DataTable()
        self.hop_dong_table.setColumnCount(6)
        self.hop_dong_table.setHorizontalHeaderLabels([
            "Mã HĐ", "Vị trí", "Ngày BĐ", "Ngày KT", "Giá thuê", "Trạng thái"
        ])
        
        header = self.hop_dong_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        layout.addWidget(self.hop_dong_table)
        
        return widget
    
    def _create_thanh_toan_tab(self) -> QWidget:
        """Create Thanh toán tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Payments table
        self.thanh_toan_table = DataTable()
        self.thanh_toan_table.setColumnCount(7)
        self.thanh_toan_table.setHorizontalHeaderLabels([
            "Mã TT", "Loại phí", "Số tiền", "Kỳ", "Đến hạn", "Đã TT", "Trạng thái"
        ])
        
        header = self.thanh_toan_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        layout.addWidget(self.thanh_toan_table)
        
        return widget
    
    def _create_lich_su_tab(self) -> QWidget:
        """Create Lịch sử tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Timeline placeholder
        timeline_label = QLabel("🕐 Lịch sử giao dịch sẽ được hiển thị ở đây")
        timeline_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        timeline_label.setStyleSheet("""
            QLabel {
                color: #757575;
                font-size: 14px;
                padding: 100px;
            }
        """)
        layout.addWidget(timeline_label)
        
        return widget
    
    def set_khach_hang(self, khach_hang: KhachHang):
        """
        Set customer to display
        
        Args:
            khach_hang: KhachHang object
        """
        self.current_khach_hang = khach_hang
        
        if not khach_hang:
            self._clear_data()
            return
        
        # Update header
        self.ten_label.setText(khach_hang.ho_ten)
        self.ma_label.setText(f"Mã: {khach_hang.ma_khach_hang}")
        self.sdt_label.setText(f"SĐT: {format_phone(khach_hang.so_dien_thoai)}")
        self.email_label.setText(f"Email: {khach_hang.email or '-'}")
        
        # Enable edit button
        self.edit_btn.setEnabled(True)
        
        # Update info tab
        self.info_ma.setText(khach_hang.ma_khach_hang)
        self.info_loai.setText("Doanh nghiệp" if khach_hang.loai_khach == LoaiKhachEnum.DOANH_NGHIEP else "Cá nhân")
        self.info_sdt.setText(format_phone(khach_hang.so_dien_thoai))
        self.info_email.setText(khach_hang.email or "-")
        self.info_dia_chi.setText(khach_hang.dia_chi)
        self.info_mst.setText(khach_hang.ma_so_thue or "-")
        self.info_ngay_dk.setText(format_date(khach_hang.ngay_dang_ky) if khach_hang.ngay_dang_ky else "-")
        
        trang_thai_labels = {
            "hoat_dong": "✅ Hoạt động",
            "tam_khoa": "⏸️ Tạm khóa",
            "da_xoa": "❌ Đã xóa",
        }
        self.info_trang_thai.setText(trang_thai_labels.get(str(khach_hang.trang_thai), str(khach_hang.trang_thai)))
        
        # Load related data
        self._load_hop_dongs()
        self._load_thanh_toans()
        self._load_statistics()
        
        # Switch to info tab
        self.tabs.setCurrentIndex(0)
    
    def _clear_data(self):
        """Clear all data"""
        # Header
        self.ten_label.setText("Chưa chọn khách hàng")
        self.ma_label.setText("Mã: -")
        self.sdt_label.setText("SĐT: -")
        self.email_label.setText("Email: -")
        self.edit_btn.setEnabled(False)
        
        # Info tab
        for widget in [
            self.info_ma, self.info_loai, self.info_sdt,
            self.info_email, self.info_dia_chi, self.info_mst,
            self.info_ngay_dk, self.info_trang_thai
        ]:
            widget.setText("-")
        
        # Stats
        self.stats_tong_hd.setText("0")
        self.stats_hd_hieu_luc.setText("0")
        self.stats_tong_da_tt.setText("0 ₫")
        self.stats_tong_cong_no.setText("0 ₫")
        
        # Tables
        self.hop_dong_table.clear()
        self.hop_dong_table.setRowCount(0)
        self.thanh_toan_table.clear()
        self.thanh_toan_table.setRowCount(0)
    
    def _load_hop_dongs(self):
        """Load contracts"""
        try:
            history = self.service.get_history(self.current_khach_hang.ma_khach_hang)
            hop_dongs = history.get('hop_dongs', [])
            
            self.hop_dong_table.setRowCount(len(hop_dongs))
            
            for row, hd in enumerate(hop_dongs):
                self.hop_dong_table.setItem(row, 0, QTableWidgetItem(hd.ma_hop_dong))
                self.hop_dong_table.setItem(row, 1, QTableWidgetItem(hd.ma_vi_tri))
                self.hop_dong_table.setItem(row, 2, QTableWidgetItem(format_date(hd.ngay_bat_dau)))
                self.hop_dong_table.setItem(row, 3, QTableWidgetItem(format_date(hd.ngay_ket_thuc)))
                self.hop_dong_table.setItem(row, 4, QTableWidgetItem(format_currency(hd.gia_thue)))
                
                trang_thai = QTableWidgetItem(self._get_trang_thai_label(hd.trang_thai))
                self.hop_dong_table.setItem(row, 5, trang_thai)
            
        except Exception as e:
            print(f"Error loading hop dongs: {e}")
    
    def _load_thanh_toans(self):
        """Load payments"""
        try:
            history = self.service.get_history(self.current_khach_hang.ma_khach_hang)
            hop_dongs = history.get('hop_dongs', [])
            
            all_thanh_toans = []
            for hd in hop_dongs:
                # In real implementation, fetch payments for each contract
                pass
            
            self.thanh_toan_table.setRowCount(len(all_thanh_toans))
            
        except Exception as e:
            print(f"Error loading thanh toans: {e}")
    
    def _load_statistics(self):
        """Load statistics"""
        try:
            history = self.service.get_history(self.current_khach_hang.ma_khach_hang)
            
            self.stats_tong_hd.setText(str(history.get('tong_hop_dong', 0)))
            self.stats_hd_hieu_luc.setText(str(history.get('hop_dong_dang_hieu_luc', 0)))
            self.stats_tong_da_tt.setText(format_currency(history.get('tong_da_thanh_toan', 0)))
            self.stats_tong_cong_no.setText(format_currency(history.get('tong_cong_no', 0)))
            
        except Exception as e:
            print(f"Error loading statistics: {e}")
    
    def _get_trang_thai_label(self, trang_thai) -> str:
        """Get status label with emoji - handles both enum objects and string values"""
        # Handle both enum object and string values
        if hasattr(trang_thai, 'value'):
            status_value = trang_thai.value
        else:
            status_value = str(trang_thai)
            
        # Common status labels
        common_labels = {
            "hoat_dong": "✅ Hoạt động",
            "tam_khoa": "⏸️ Tạm khóa", 
            "da_xoa": "❌ Đã xóa",
            "trong": "🟢 Trống",
            "da_thue": "🔴 Đã thuê",
            "bao_tri": "🔧 Bảo trì",
            "hieu_luc": "✅ Hiệu lực",
            "het_han": "⏰ Hết hạn",
            "cham_dut": "❌ Chấm dứt",
            "gia_han": "🔄 Gia hạn",
            "trong_kho": "📦 Trong kho",
            "da_xuat": "📤 Đã xuất",
            "hu_hong": "⚠️ Hư hỏng",
            "cho_thanh_toan": "⏳ Chờ thanh toán",
            "da_thanh_toan": "💰 Đã thanh toán"
        }
        
        return common_labels.get(status_value, str(trang_thai))
    
    def _on_edit(self):
        """Handle edit button click"""
        if self.current_khach_hang:
            self.edit_requested.emit(self.current_khach_hang)


class KhachHangDetailWidget(QFrame):
    """
    Khung xem chi tiết khách hàng (embedded in main view)
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        """Setup UI"""
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border: 1px solid rgba(0, 0, 0, 0.1);
                border-radius: 8px;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Placeholder
        placeholder = QLabel("📋 Chọn một khách hàng để xem chi tiết")
        placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        placeholder.setStyleSheet("""
            QLabel {
                color: #757575;
                font-size: 16px;
                padding: 100px;
            }
        """)
        layout.addWidget(placeholder)
    
    def set_khach_hang(self, khach_hang: KhachHang):
        """Set customer (placeholder for future implementation)"""
        pass


__all__ = ['KhachHangDetailView', 'KhachHangDetailWidget']
