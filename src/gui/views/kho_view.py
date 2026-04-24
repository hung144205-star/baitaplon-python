#!/usr/bin/env python3
"""
Kho View - Giao diện Quản lý Kho hàng
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QComboBox, QMessageBox, QProgressBar
)
from PyQt6.QtCore import Qt, pyqtSignal
from datetime import datetime
from typing import Optional, Dict, Any

from src.services import KhoService
from src.models import Kho, TrangThaiKhoEnum
from src.gui.widgets import DataTableWithToolbar, SearchBox
from src.gui.dialogs import MessageDialog, ConfirmDialog
from src.utils.formatters import format_number
from src.gui.forms import KhoForm


class KhoView(QWidget):
    """
    Giao diện Quản lý Kho hàng
    """
    
    # Signals
    kho_selected = pyqtSignal(object)  # Kho object
    kho_added = pyqtSignal(object)  # Kho object
    kho_updated = pyqtSignal(object)  # Kho object
    kho_deleted = pyqtSignal(str)  # ma_kho
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.service = KhoService()
        self.current_kho: Optional[Kho] = None
        self.setup_ui()
        self.setup_connections()
        self.load_data()
    
    def setup_ui(self):
        """Setup UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)
        
        # Title
        title = QLabel("🏭 QUẢN LÝ KHO HÀNG")
        title.setObjectName("titleLabel")
        title.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: 700;
                color: #31302e;
                padding: 10px 0;
            }
        """)
        layout.addWidget(title)
        
        # Statistics bar
        stats_bar = self._create_stats_bar()
        layout.addWidget(stats_bar)
        
        # Filter bar
        filter_bar = self._create_filter_bar()
        layout.addWidget(filter_bar)
        
        # Data table with toolbar
        self.table_with_toolbar = DataTableWithToolbar(
            headers=["Mã Kho", "Tên Kho", "Địa Chỉ", "Diện Tích", "Sức Chứa", "Đã Sử Dụng", "% Lấp Đầy", "Trạng Thái"]
        )
        layout.addWidget(self.table_with_toolbar, 1)
        
        # Info label
        self.info_label = QLabel("Chọn một kho để xem chi tiết")
        self.info_label.setStyleSheet("""
            QLabel {
                color: #615d59;
                font-size: 14px;
                padding: 8px;
                background-color: #f6f5f4;
                border-radius: 6px;
            }
        """)
        layout.addWidget(self.info_label)
    
    def _create_stats_bar(self) -> QFrame:
        """Create statistics bar"""
        stats_bar = QFrame()
        stats_bar.setFrameShape(QFrame.Shape.StyledPanel)
        stats_bar.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border: 1px solid rgba(0, 0, 0, 0.1);
                border-radius: 8px;
                padding: 12px;
            }
        """)
        
        layout = QHBoxLayout(stats_bar)
        layout.setSpacing(20)
        
        # Total warehouses
        self.stat_tong = QLabel("0")
        self.stat_tong.setStyleSheet("font-size: 24px; font-weight: 700; color: #1976d2;")
        layout.addWidget(QLabel("Tổng kho:"))
        layout.addWidget(self.stat_tong)
        
        layout.addSpacing(20)
        
        # Active warehouses
        self.stat_hoat_dong = QLabel("0")
        self.stat_hoat_dong.setStyleSheet("font-size: 24px; font-weight: 700; color: #1aae39;")
        layout.addWidget(QLabel("Hoạt động:"))
        layout.addWidget(self.stat_hoat_dong)
        
        layout.addSpacing(20)
        
        # Fill rate average
        self.stat_fill_rate = QLabel("0%")
        self.stat_fill_rate.setStyleSheet("font-size: 24px; font-weight: 700; color: #ff9800;")
        layout.addWidget(QLabel("Lấp đầy TB:"))
        layout.addWidget(self.stat_fill_rate)
        
        layout.addStretch()
        
        return stats_bar
    
    def _create_filter_bar(self) -> QFrame:
        """Create filter bar"""
        filter_bar = QFrame()
        filter_bar.setFrameShape(QFrame.Shape.StyledPanel)
        filter_bar.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border: 1px solid rgba(0, 0, 0, 0.1);
                border-radius: 8px;
                padding: 12px;
            }
        """)
        
        layout = QHBoxLayout(filter_bar)
        layout.setSpacing(12)
        
        # Search box
        self.search_box = SearchBox(placeholder="🔍 Tìm theo tên, mã, địa chỉ...")
        layout.addWidget(self.search_box, 1)
        
        # Filter by status
        layout.addWidget(QLabel("Trạng thái:"))
        self.filter_trang_thai = QComboBox()
        self.filter_trang_thai.addItem("Tất cả", "")
        self.filter_trang_thai.addItem("Hoạt động", "hoat_dong")
        self.filter_trang_thai.addItem("Bảo trì", "bao_tri")
        self.filter_trang_thai.addItem("Ngừng", "ngung")
        self.filter_trang_thai.setFixedWidth(150)
        layout.addWidget(self.filter_trang_thai)
        
        return filter_bar
    
    def setup_connections(self):
        """Setup signal connections"""
        # Table events
        self.table_with_toolbar.row_selected.connect(self._on_row_selected)
        self.table_with_toolbar.row_double_clicked.connect(self._on_row_double_clicked)
        
        # Toolbar buttons
        self.table_with_toolbar.add_clicked.connect(self._on_add_clicked)
        self.table_with_toolbar.edit_clicked.connect(self._on_edit_clicked)
        self.table_with_toolbar.delete_clicked.connect(self._on_delete_clicked)
        self.table_with_toolbar.refresh_clicked.connect(self._on_refresh_clicked)
        self.table_with_toolbar.export_clicked.connect(self._on_export_clicked)
        
        # Search & filter
        self.search_box.search_changed.connect(self._on_search_changed)
        self.filter_trang_thai.currentIndexChanged.connect(self._apply_filters)
    
    def load_data(self):
        """Load data from database"""
        try:
            khos = self.service.get_all(limit=1000)
            
            # Convert to table data
            data = []
            total_fill_rate = 0
            
            for kho in khos:
                if kho.trang_thai != TrangThaiKhoEnum.NGUNG:
                    # Calculate fill rate
                    fill_rate = self.service.calculate_fill_rate(kho.ma_kho)
                    total_fill_rate += fill_rate
                    
                    data.append({
                        "Mã Kho": kho.ma_kho,
                        "Tên Kho": kho.ten_kho,
                        "Địa Chỉ": kho.dia_chi,
                        "Diện Tích": f"{kho.dien_tich:,.0f} m²",
                        "Sức Chứa": f"{kho.suc_chua:,.0f} m³",
                        "Đã Sử Dụng": f"{kho.da_su_dung:,.0f} m³",
                        "% Lấp Đầy": f"{fill_rate:.1f}%",
                        "Trạng Thái": self._get_trang_thai_label(kho.trang_thai),
                        "_data": kho
                    })
            
            self.table_with_toolbar.set_data(data)
            
            # Update statistics
            self._update_statistics(khos, total_fill_rate)
            
            # Update info
            self.info_label.setText(f"Tổng: {len(data)} kho")
            
        except Exception as e:
            MessageDialog.error(self, "Lỗi", f"Không thể tải dữ liệu:\n{str(e)}")
    
    def _update_statistics(self, khos: list, total_fill_rate: float):
        """Update statistics bar"""
        tong = len(khos)
        hoat_dong = sum(1 for k in khos if k.trang_thai == TrangThaiKhoEnum.HOAT_DONG)
        avg_fill_rate = total_fill_rate / tong if tong > 0 else 0
        
        self.stat_tong.setText(str(tong))
        self.stat_hoat_dong.setText(str(hoat_dong))
        self.stat_fill_rate.setText(f"{avg_fill_rate:.1f}%")
    
    def _get_trang_thai_label(self, trang_thai) -> str:
        """Get status label with emoji"""
        labels = {
            "hoat_dong": "✅ Hoạt động",
            "bao_tri": "🔧 Bảo trì",
            "ngung": "❌ Ngừng",
        }
        return labels.get(str(trang_thai), str(trang_thai))
    
    def _on_row_selected(self, row_index: int, row_data: dict):
        """Handle row selection"""
        if "_data" in row_data:
            self.current_kho = row_data["_data"]
            self.kho_selected.emit(self.current_kho)
            self.info_label.setText(
                f"Đang xem: {self.current_kho.ten_kho} ({self.current_kho.ma_kho})"
            )
    
    def _on_row_double_clicked(self, row_index: int, row_data: dict):
        """Handle row double click"""
        if "_data" in row_data:
            self._on_edit_clicked()
    
    def _on_add_clicked(self):
        """Handle add button click"""
        dialog = KhoForm(self)
        dialog.kho_saved.connect(self._on_kho_saved)
        dialog.exec()
    
    def _on_kho_saved(self, kho: Kho):
        """Handle kho saved from form"""
        self.load_data()  # Refresh table
        self.kho_added.emit(kho)
    
    def _on_edit_clicked(self):
        """Handle edit button click"""
        if not self.current_kho:
            MessageDialog.warning(self, "Cảnh báo", "Vui lòng chọn một kho để sửa")
            return
        
        dialog = KhoForm(self, kho=self.current_kho)
        dialog.kho_saved.connect(self._on_kho_saved)
        dialog.exec()
    
    def _on_delete_clicked(self):
        """Handle delete button click"""
        if not self.current_kho:
            MessageDialog.warning(self, "Cảnh báo", "Vui lòng chọn một kho để xóa")
            return
        
        # Confirm delete
        confirmed = ConfirmDialog.ask_delete(
            self, 
            f"{self.current_kho.ten_kho} ({self.current_kho.ma_kho})"
        )
        
        if confirmed:
            try:
                success = self.service.delete(self.current_kho.ma_kho)
                if success:
                    MessageDialog.success(self, "Thành công", "Đã xóa kho thành công")
                    self.kho_deleted.emit(self.current_kho.ma_kho)
                    self.load_data()
                    self.current_kho = None
                else:
                    MessageDialog.error(self, "Lỗi", "Không thể xóa kho")
            except ValueError as e:
                MessageDialog.error(self, "Không thể xóa", str(e))
            except Exception as e:
                MessageDialog.error(self, "Lỗi", f"Không thể xóa kho:\n{str(e)}")
    
    def _on_refresh_clicked(self):
        """Handle refresh button click"""
        self.load_data()
    
    def _on_export_clicked(self):
        """Handle export button click"""
        try:
            from src.utils.export_service import export_kho_to_excel
            from PyQt6.QtWidgets import QFileDialog
            
            # Get all data
            khos_data = []
            for row in self.table_with_toolbar._data:
                if "_data" in row:
                    kho = row["_data"]
                    fill_rate = self.service.calculate_fill_rate(kho.ma_kho)
                    khos_data.append({
                        'ma_kho': kho.ma_kho,
                        'ten_kho': kho.ten_kho,
                        'dia_chi': kho.dia_chi,
                        'dien_tich': kho.dien_tich,
                        'suc_chua': kho.suc_chua,
                        'trang_thai_label': self._get_trang_thai_label(kho.trang_thai),
                        'ghi_chu': kho.ghi_chu or '',
                        'fill_rate': fill_rate
                    })
            
            if not khos_data:
                MessageDialog.warning(self, "Cảnh báo", "Không có dữ liệu để xuất")
                return
            
            # Ask for save location
            default_name = f"kho_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Xuất Excel",
                default_name,
                "Excel Files (*.xlsx)"
            )
            
            if file_path:
                output = export_kho_to_excel(khos_data, file_path)
                MessageDialog.success(self, "Thành công", f"Đã xuất file Excel:\n{output}")
                
        except ImportError as e:
            MessageDialog.error(self, "Thiếu thư viện", "Cần cài đặt pandas và openpyxl:\npip install pandas openpyxl")
        except Exception as e:
            MessageDialog.error(self, "Lỗi", f"Không thể xuất Excel:\n{str(e)}")
    
    def _on_search_changed(self, text: str):
        """Handle search"""
        if not text.strip():
            self.load_data()
        else:
            try:
                results = self.service.search(text, limit=100)
                
                # Convert to table data
                data = []
                for kho in results:
                    fill_rate = self.service.calculate_fill_rate(kho.ma_kho)
                    data.append({
                        "Mã Kho": kho.ma_kho,
                        "Tên Kho": kho.ten_kho,
                        "Địa Chỉ": kho.dia_chi,
                        "Diện Tích": f"{kho.dien_tich:,.0f} m²",
                        "Sức Chứa": f"{kho.suc_chua:,.0f} m³",
                        "Đã Sử Dụng": f"{kho.da_su_dung:,.0f} m³",
                        "% Lấp Đầy": f"{fill_rate:.1f}%",
                        "Trạng Thái": self._get_trang_thai_label(kho.trang_thai),
                        "_data": kho
                    })
                
                self.table_with_toolbar.set_data(data)
                self.info_label.setText(f"Tìm thấy: {len(data)} kho")
                
            except Exception as e:
                MessageDialog.error(self, "Lỗi", f"Không thể tìm kiếm:\n{str(e)}")
    
    def _apply_filters(self):
        """Apply filters"""
        try:
            trang_thai = self.filter_trang_thai.currentData()
            
            khos = self.service.get_all(limit=1000)
            
            # Filter by status
            if trang_thai:
                khos = [k for k in khos if str(k.trang_thai) == trang_thai]
            
            # Convert to table data
            data = []
            for kho in khos:
                if kho.trang_thai != TrangThaiKhoEnum.NGUNG:
                    fill_rate = self.service.calculate_fill_rate(kho.ma_kho)
                    data.append({
                        "Mã Kho": kho.ma_kho,
                        "Tên Kho": kho.ten_kho,
                        "Địa Chỉ": kho.dia_chi,
                        "Diện Tích": f"{kho.dien_tich:,.0f} m²",
                        "Sức Chứa": f"{kho.suc_chua:,.0f} m³",
                        "Đã Sử Dụng": f"{kho.da_su_dung:,.0f} m³",
                        "% Lấp Đầy": f"{fill_rate:.1f}%",
                        "Trạng Thái": self._get_trang_thai_label(kho.trang_thai),
                        "_data": kho
                    })
            
            self.table_with_toolbar.set_data(data)
            self.info_label.setText(f"Tổng: {len(data)} kho")
            
        except Exception as e:
            MessageDialog.error(self, "Lỗi", f"Không thể lọc dữ liệu:\n{str(e)}")
    
    def refresh_data(self):
        """Refresh data from outside"""
        self.load_data()


class ViTriSubView(QWidget):
    """
    Sub-view for Vị trí within a warehouse
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_kho = None
        self.setup_ui()
    
    def setup_ui(self):
        """Setup UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Title
        title = QLabel("📦 Vị trí lưu trữ")
        title.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: 700;
                color: #31302e;
                padding: 10px 0;
            }
        """)
        layout.addWidget(title)
        
        # Placeholder
        placeholder = QLabel("Chọn một kho để xem vị trí")
        placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        placeholder.setStyleSheet("""
            QLabel {
                color: #757575;
                font-size: 16px;
                padding: 100px;
            }
        """)
        layout.addWidget(placeholder, 1)
    
    def set_kho(self, kho):
        """Set current warehouse"""
        self.current_kho = kho
        # TODO: Load positions


__all__ = ['KhoView', 'ViTriSubView']
