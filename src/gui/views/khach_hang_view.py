#!/usr/bin/env python3
"""
Khách hàng View - Giao diện Quản lý Khách hàng (Modern UI)
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QComboBox, QMessageBox, QHeaderView, QGridLayout,
    QTableWidget, QTableWidgetItem, QScrollArea, QSizePolicy
)
from PyQt6.QtCore import Qt, pyqtSignal, QSize
from PyQt6.QtGui import QFont, QColor, QPalette
from typing import Optional, Dict, Any, List

from src.services import KhachHangService
from src.models import KhachHang, LoaiKhachEnum, TrangThaiKHEnum
from src.gui.widgets import SearchBox
from src.gui.dialogs import MessageDialog, ConfirmDialog
from src.utils.formatters import format_phone, format_date
from src.gui.forms import KhachHangForm


class StatsCard(QFrame):
    """Card hiển thị thống kê"""
    
    def __init__(self, icon: str, title: str, value: str, subtitle: str = "", 
                 color: str = "#1976d2", parent=None):
        super().__init__(parent)
        self.setStyleSheet(f"""
            QFrame {{
                background-color: #ffffff;
                border-radius: 12px;
                border: 1px solid #e0e0e0;
                padding: 20px;
            }}
        """)
        self.setMinimumHeight(140)
        self.setMaximumHeight(140)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(8)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Icon và title
        header = QHBoxLayout()
        icon_label = QLabel(icon)
        icon_label.setStyleSheet(f"font-size: 24px; color: {color};")
        header.addWidget(icon_label)
        header.addStretch()
        layout.addLayout(header)
        
        # Title
        title_label = QLabel(title)
        title_label.setStyleSheet("font-size: 12px; color: #757575; font-weight: 600;")
        layout.addWidget(title_label)
        
        # Value
        self.value_label = QLabel(value)
        self.value_label.setStyleSheet(f"font-size: 32px; font-weight: 700; color: {color};")
        layout.addWidget(self.value_label)
        
        # Subtitle
        if subtitle:
            sub_label = QLabel(subtitle)
            sub_label.setStyleSheet("font-size: 11px; color: #9e9e9e;")
            layout.addWidget(sub_label)
        
        layout.addStretch()
    
    def set_value(self, value: str):
        self.value_label.setText(value)


class KhachHangView(QWidget):
    """
    Giao diện Quản lý Khách hàng - Modern UI
    """
    
    # Signals
    khach_hang_selected = pyqtSignal(object)
    khach_hang_added = pyqtSignal(object)
    khach_hang_updated = pyqtSignal(object)
    khach_hang_deleted = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.service = KhachHangService()
        self.current_khach_hang: Optional[KhachHang] = None
        self.all_data: List[KhachHang] = []
        self.setup_ui()
        self.setup_connections()
        self.load_data()
    
    def setup_ui(self):
        """Setup Modern UI"""
        self.setStyleSheet("""
            QWidget {
                background-color: #faf9f8;
                font-family: 'Inter', sans-serif;
            }
            QFrame {
                background-color: transparent;
            }
            QPushButton {
                border-radius: 6px;
                padding: 10px 20px;
                font-weight: 600;
                font-size: 13px;
            }
            QPushButton#primaryButton {
                background-color: #005db2;
                color: white;
                border: none;
            }
            QPushButton#primaryButton:hover {
                background-color: #00468a;
            }
            QPushButton#secondaryButton {
                background-color: #ffffff;
                color: #31302e;
                border: 1px solid #e0e0e0;
            }
            QPushButton#secondaryButton:hover {
                background-color: #f5f5f5;
            }
            QComboBox {
                padding: 8px 12px;
                border: 1px solid #e0e0e0;
                border-radius: 6px;
                background-color: #ffffff;
                font-size: 13px;
            }
            QComboBox:hover {
                border-color: #005db2;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            QTableWidget {
                background-color: #ffffff;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                gridline-color: #f0f0f0;
            }
            QTableWidget::item {
                padding: 12px 16px;
                border-bottom: 1px solid #f0f0f0;
            }
            QTableWidget::item:selected {
                background-color: #e3f2fd;
                color: #005db2;
            }
            QHeaderView::section {
                background-color: #f8f9fa;
                color: #757575;
                font-weight: 600;
                font-size: 11px;
                text-transform: uppercase;
                letter-spacing: 0.5px;
                padding: 12px 16px;
                border: none;
                border-bottom: 2px solid #e0e0e0;
            }
            QLabel#titleLabel {
                font-size: 32px;
                font-weight: 700;
                color: #1a1c1c;
                letter-spacing: -0.5px;
            }
            QLabel#subtitleLabel {
                font-size: 14px;
                color: #757575;
            }
        """)
        
        # Main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 30, 40, 30)
        layout.setSpacing(24)
        
        # Header Section
        header = self._create_header()
        layout.addLayout(header)
        
        # Stats Cards
        stats = self._create_stats_section()
        layout.addLayout(stats)
        
        # Table Section
        table_section = self._create_table_section()
        layout.addWidget(table_section, 1)
    
    def _create_header(self) -> QHBoxLayout:
        """Create header with title and buttons"""
        layout = QHBoxLayout()
        
        # Left: Title
        left_layout = QVBoxLayout()
        
        subtitle = QLabel("Quản lý Khách hàng")
        subtitle.setObjectName("subtitleLabel")
        subtitle.setStyleSheet("font-size: 12px; color: #005db2; font-weight: 600; text-transform: uppercase; letter-spacing: 1px;")
        left_layout.addWidget(subtitle)
        
        title = QLabel("Danh sách Khách hàng")
        title.setObjectName("titleLabel")
        title.setStyleSheet("font-size: 32px; font-weight: 700; color: #1a1c1c; letter-spacing: -0.5px;")
        left_layout.addWidget(title)
        
        desc = QLabel("Quản lý thông tin khách hàng, theo dõi trạng thái và xử lý hợp đồng.")
        desc.setStyleSheet("font-size: 14px; color: #757575; margin-top: 4px;")
        left_layout.addWidget(desc)
        
        layout.addLayout(left_layout, 1)
        
        # Right: Buttons
        right_layout = QHBoxLayout()
        right_layout.setSpacing(12)
        
        self.export_btn = QPushButton("📥 Xuất Excel")
        self.export_btn.setObjectName("secondaryButton")
        right_layout.addWidget(self.export_btn)
        
        self.add_btn = QPushButton("➕ Thêm khách hàng")
        self.add_btn.setObjectName("primaryButton")
        right_layout.addWidget(self.add_btn)
        
        layout.addLayout(right_layout)
        return layout
    
    def _create_stats_section(self) -> QHBoxLayout:
        """Create statistics cards"""
        layout = QHBoxLayout()
        layout.setSpacing(16)
        
        # Tổng số KH
        self.stat_tong = StatsCard(
            "👥", "Tổng số khách hàng", "0", "", "#005db2"
        )
        layout.addWidget(self.stat_tong)
        
        # Hoạt động
        self.stat_hoat_dong = StatsCard(
            "✅", "Đang hoạt động", "0", "", "#1aae39"
        )
        layout.addWidget(self.stat_hoat_dong)
        
        # Cá nhân
        self.stat_ca_nhan = StatsCard(
            "🏠", "Khách cá nhân", "0", "", "#ff9800"
        )
        layout.addWidget(self.stat_ca_nhan)
        
        # Doanh nghiệp
        self.stat_doanh_nghiep = StatsCard(
            "🏢", "Doanh nghiệp", "0", "", "#9c27b0"
        )
        layout.addWidget(self.stat_doanh_nghiep)
        
        return layout
    
    def _create_table_section(self) -> QFrame:
        """Create table section with filters"""
        section = QFrame()
        section.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border-radius: 12px;
                border: 1px solid #e0e0e0;
            }
        """)
        
        layout = QVBoxLayout(section)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)
        
        # Filter Bar
        filter_bar = QHBoxLayout()
        filter_bar.setSpacing(12)
        
        # Search
        self.search_input = SearchBox(placeholder="🔍 Tìm theo tên, SĐT, email...")
        filter_bar.addWidget(self.search_input, 1)
        
        # Filters
        filter_bar.addWidget(QLabel("Loại:"))
        self.filter_loai = QComboBox()
        self.filter_loai.addItem("Tất cả", "")
        self.filter_loai.addItem("🏠 Cá nhân", "ca_nhan")
        self.filter_loai.addItem("🏢 Doanh nghiệp", "doanh_nghiep")
        self.filter_loai.setFixedWidth(150)
        filter_bar.addWidget(self.filter_loai)
        
        filter_bar.addWidget(QLabel("Trạng thái:"))
        self.filter_trang_thai = QComboBox()
        self.filter_trang_thai.addItem("Tất cả", "")
        self.filter_trang_thai.addItem("✅ Hoạt động", "hoat_dong")
        self.filter_trang_thai.addItem("⏸️ Tạm khóa", "tam_khoa")
        self.filter_trang_thai.setFixedWidth(150)
        filter_bar.addWidget(self.filter_trang_thai)
        
        layout.addLayout(filter_bar)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "Mã KH", "Họ tên", "Loại", "SĐT", "Email", "Trạng thái"
        ])
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setColumnWidth(0, 100)
        self.table.setColumnWidth(1, 200)
        self.table.setColumnWidth(2, 120)
        self.table.setColumnWidth(3, 120)
        self.table.setColumnWidth(4, 200)
        self.table.setColumnWidth(5, 120)
        
        layout.addWidget(self.table, 1)
        
        # Info bar
        info_layout = QHBoxLayout()
        self.info_label = QLabel("Đang hiển thị 0 trên 0 kết quả")
        self.info_label.setStyleSheet("font-size: 13px; color: #757575; font-style: italic;")
        info_layout.addWidget(self.info_label)
        
        # Pagination
        pagination = QHBoxLayout()
        self.prev_btn = QPushButton("◀")
        self.prev_btn.setFixedSize(32, 32)
        self.prev_btn.setObjectName("secondaryButton")
        self.page_label = QLabel("Trang 1 / 1")
        self.page_label.setStyleSheet("font-size: 13px; font-weight: 600;")
        self.page_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.page_label.setFixedWidth(80)
        self.next_btn = QPushButton("▶")
        self.next_btn.setFixedSize(32, 32)
        self.next_btn.setObjectName("secondaryButton")
        
        pagination.addStretch()
        pagination.addWidget(self.prev_btn)
        pagination.addWidget(self.page_label)
        pagination.addWidget(self.next_btn)
        pagination.addStretch()
        
        info_layout.addLayout(pagination)
        
        layout.addLayout(info_layout)
        
        return section
    
    def setup_connections(self):
        """Setup signal connections"""
        self.add_btn.clicked.connect(self._on_add_clicked)
        self.export_btn.clicked.connect(self._on_export_clicked)
        
        self.search_input.search_changed.connect(self._on_search_changed)
        self.filter_loai.currentIndexChanged.connect(self._apply_filters)
        self.filter_trang_thai.currentIndexChanged.connect(self._apply_filters)
        
        self.table.itemSelectionChanged.connect(self._on_selection_changed)
        self.table.doubleClicked.connect(self._on_table_double_clicked)
    
    def load_data(self):
        """Load data from database"""
        try:
            self.all_data = self.service.get_all(limit=1000)
            self._update_stats()
            self._apply_filters()
        except Exception as e:
            MessageDialog.error(self, "Lỗi", f"Không thể tải dữ liệu:\n{str(e)}")
    
    def _update_stats(self):
        """Update statistics cards"""
        # Filter out deleted
        active_data = [kh for kh in self.all_data if kh.trang_thai != TrangThaiKHEnum.DA_XOA]
        
        # Tổng
        self.stat_tong.set_value(str(len(active_data)))
        
        # Hoạt động
        hoat_dong = sum(1 for kh in active_data if kh.trang_thai == TrangThaiKHEnum.HOAT_DONG)
        self.stat_hoat_dong.set_value(str(hoat_dong))
        
        # Cá nhân
        ca_nhan = sum(1 for kh in active_data if kh.loai_khach == LoaiKhachEnum.CA_NHAN)
        self.stat_ca_nhan.set_value(str(ca_nhan))
        
        # Doanh nghiệp
        doanh_nghiep = sum(1 for kh in active_data if kh.loai_khach == LoaiKhachEnum.DOANH_NGHIEP)
        self.stat_doanh_nghiep.set_value(str(doanh_nghiep))
    
    def _apply_filters(self):
        """Apply filters and update table"""
        try:
            loai = self.filter_loai.currentData()
            trang_thai = self.filter_trang_thai.currentData()
            search_text = self.search_input.current_text().lower().strip()
            
            # Filter data
            filtered = []
            for kh in self.all_data:
                # Skip deleted unless specified
                if kh.trang_thai == TrangThaiKHEnum.DA_XOA:
                    continue
                
                # Filter by type
                if loai and str(kh.loai_khach) != loai:
                    continue
                
                # Filter by status
                if trang_thai:
                    if hasattr(kh.trang_thai, 'value'):
                        if kh.trang_thai.value != trang_thai:
                            continue
                    elif str(kh.trang_thai) != trang_thai:
                        continue
                
                # Search
                if search_text:
                    if search_text not in kh.ho_ten.lower() and \
                       search_text not in kh.so_dien_thoai.lower() and \
                       search_text not in (kh.email or "").lower() and \
                       search_text not in kh.ma_khach_hang.lower():
                        continue
                
                filtered.append(kh)
            
            self._update_table(filtered)
            self.info_label.setText(f"Đang hiển thị {len(filtered)} trên {len(filtered)} kết quả")
            
        except Exception as e:
            MessageDialog.error(self, "Lỗi", f"Không thể lọc dữ liệu:\n{str(e)}")
    
    def _update_table(self, data: List[KhachHang]):
        """Update table with data"""
        self.table.setRowCount(len(data))
        
        for row_idx, kh in enumerate(data):
            # Mã KH
            self.table.setItem(row_idx, 0, QTableWidgetItem(kh.ma_khach_hang))
            
            # Họ tên
            self.table.setItem(row_idx, 1, QTableWidgetItem(kh.ho_ten))
            
            # Loại
            loai_text = "🏢 Doanh nghiệp" if kh.loai_khach == LoaiKhachEnum.DOANH_NGHIEP else "🏠 Cá nhân"
            self.table.setItem(row_idx, 2, QTableWidgetItem(loai_text))
            
            # SĐT
            self.table.setItem(row_idx, 3, QTableWidgetItem(format_phone(kh.so_dien_thoai)))
            
            # Email
            self.table.setItem(row_idx, 4, QTableWidgetItem(kh.email or "-"))
            
            # Trạng thái
            status_text = self._get_trang_thai_label(kh.trang_thai)
            self.table.setItem(row_idx, 5, QTableWidgetItem(status_text))
            
            # Store data
            self.table.item(row_idx, 0).setData(Qt.ItemDataRole.UserRole, kh)
    
    def _get_trang_thai_label(self, trang_thai) -> str:
        """Get status label with emoji"""
        if hasattr(trang_thai, 'value'):
            status_value = trang_thai.value
        else:
            status_value = str(trang_thai)
            
        labels = {
            "hoat_dong": "✅ Hoạt động",
            "tam_khoa": "⏸️ Tạm khóa",
            "da_xoa": "❌ Đã xóa",
        }
        return labels.get(status_value, str(trang_thai))
    
    def _on_selection_changed(self):
        """Handle row selection"""
        selected = self.table.selectedItems()
        if selected:
            row = selected[0].row()
            item = self.table.item(row, 0)
            if item:
                self.current_khach_hang = item.data(Qt.ItemDataRole.UserRole)
                self.khach_hang_selected.emit(self.current_khach_hang)
    
    def _on_table_double_clicked(self):
        """Handle double click"""
        if self.current_khach_hang:
            self._on_edit_clicked()
    
    def _on_add_clicked(self):
        """Handle add button"""
        dialog = KhachHangForm(self)
        dialog.accepted_with_data.connect(self._on_saved)
        dialog.exec()
    
    def _on_edit_clicked(self):
        """Handle edit"""
        if not self.current_khach_hang:
            MessageDialog.warning(self, "Cảnh báo", "Vui lòng chọn khách hàng để sửa")
            return
        
        dialog = KhachHangForm(self, khach_hang=self.current_khach_hang)
        dialog.accepted_with_data.connect(self._on_saved)
        dialog.exec()
    
    def _on_saved(self, khach_hang: KhachHang):
        """Handle saved"""
        self.load_data()
        if hasattr(self, 'current_khach_hang') and self.current_khach_hang:
            self.khach_hang_updated.emit(khach_hang)
        else:
            self.khach_hang_added.emit(khach_hang)
    
    def _on_export_clicked(self):
        """Handle export"""
        MessageDialog.info(self, "Thông báo", "Chức năng xuất Excel đang được phát triển")
    
    def _on_search_changed(self, text: str):
        """Handle search"""
        self._apply_filters()
    
    def refresh_data(self):
        """Refresh data"""
        self.load_data()


__all__ = ['KhachHangView']
