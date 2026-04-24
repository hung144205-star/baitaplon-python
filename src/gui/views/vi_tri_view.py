#!/usr/bin/env python3
"""
Vi Tri View - Giao diện Quản lý Vị trí lưu trữ
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QComboBox, QMessageBox, QProgressBar, QGroupBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from datetime import datetime
from typing import Optional, Dict, Any, List

from src.services import ViTriService, KhoService
from src.models import ViTri, Kho, TrangThaiViTriEnum
from src.gui.widgets import DataTableWithToolbar, SearchBox
from src.gui.dialogs import MessageDialog, ConfirmDialog
from src.utils.formatters import format_currency, format_number
from src.gui.forms import ViTriForm


class ViTriView(QWidget):
    """
    Giao diện Quản lý Vị trí lưu trữ
    """
    
    # Signals
    vi_tri_selected = pyqtSignal(object)  # ViTri object
    vi_tri_added = pyqtSignal(object)  # ViTri object
    vi_tri_updated = pyqtSignal(object)  # ViTri object
    vi_tri_deleted = pyqtSignal(str)  # ma_vi_tri
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.vi_tri_service = ViTriService()
        self.kho_service = KhoService()
        self.current_vi_tri: Optional[ViTri] = None
        self.current_kho: Optional[Kho] = None
        self.setup_ui()
        self.setup_connections()
        self.load_khos()
    
    def setup_ui(self):
        """Setup UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)
        
        # Title
        title = QLabel("📦 QUẢN LÝ VỊ TRÍ LƯU TRỮ")
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
        
        # Kho selection
        kho_selector = self._create_kho_selector()
        layout.addWidget(kho_selector)
        
        # Filter bar
        filter_bar = self._create_filter_bar()
        layout.addWidget(filter_bar)
        
        # Data table with toolbar
        self.table_with_toolbar = DataTableWithToolbar(
            headers=["Mã Vị Trí", "Khu Vực", "Hàng", "Tầng", "Diện Tích", "Giá Thuê", "Trạng Thái"]
        )
        layout.addWidget(self.table_with_toolbar, 1)
        
        # Info label
        self.info_label = QLabel("Chọn một kho để xem vị trí")
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
        
        # Total positions
        layout.addWidget(QLabel("Tổng vị trí:"))
        self.stat_tong = QLabel("0")
        self.stat_tong.setStyleSheet("font-size: 24px; font-weight: 700; color: #1976d2;")
        layout.addWidget(self.stat_tong)
        
        layout.addSpacing(20)
        
        # Empty positions
        layout.addWidget(QLabel("Trống:"))
        self.stat_trong = QLabel("0")
        self.stat_trong.setStyleSheet("font-size: 24px; font-weight: 700; color: #1aae39;")
        layout.addWidget(self.stat_trong)
        
        layout.addSpacing(20)
        
        # Rented positions
        layout.addWidget(QLabel("Đã thuê:"))
        self.stat_da_thue = QLabel("0")
        self.stat_da_thue.setStyleSheet("font-size: 24px; font-weight: 700; color: #ff9800;")
        layout.addWidget(self.stat_da_thue)
        
        layout.addSpacing(20)
        
        # Empty rate
        layout.addWidget(QLabel("Tỷ lệ trống:"))
        self.stat_ty_le = QLabel("0%")
        self.stat_ty_le.setStyleSheet("font-size: 24px; font-weight: 700; color: #4caf50;")
        layout.addWidget(self.stat_ty_le)
        
        layout.addStretch()
        
        return stats_bar
    
    def _create_kho_selector(self) -> QFrame:
        """Create warehouse selector"""
        kho_selector = QFrame()
        kho_selector.setFrameShape(QFrame.Shape.StyledPanel)
        kho_selector.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border: 1px solid rgba(0, 0, 0, 0.1);
                border-radius: 8px;
                padding: 12px;
            }
        """)
        
        layout = QHBoxLayout(kho_selector)
        layout.setSpacing(12)
        
        layout.addWidget(QLabel("🏭 Chọn kho:"))
        self.kho_selector = QComboBox()
        self.kho_selector.addItem("-- Chọn kho --", None)
        self.kho_selector.setFixedWidth(300)
        self.kho_selector.currentIndexChanged.connect(self._on_kho_changed)
        layout.addWidget(self.kho_selector)
        
        layout.addStretch()
        
        return kho_selector
    
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
        self.search_box = SearchBox(placeholder="🔍 Tìm theo mã, khu vực...")
        layout.addWidget(self.search_box, 1)
        
        # Filter by status
        layout.addWidget(QLabel("Trạng thái:"))
        self.filter_trang_thai = QComboBox()
        self.filter_trang_thai.addItem("Tất cả", "")
        self.filter_trang_thai.addItem("Trống", "trong")
        self.filter_trang_thai.addItem("Đã thuê", "da_thue")
        self.filter_trang_thai.addItem("Bảo trì", "bao_tri")
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
    
    def load_khos(self):
        """Load warehouses into selector"""
        try:
            khos = self.kho_service.get_all(limit=100)
            
            # Clear existing (keep first item)
            while self.kho_selector.count() > 1:
                self.kho_selector.removeItem(1)
            
            # Add warehouses
            for kho in khos:
                if kho.trang_thai == TrangThaiViTriEnum.HOAT_DONG:
                    self.kho_selector.addItem(f"{kho.ten_kho} ({kho.ma_kho})", kho)
            
        except Exception as e:
            MessageDialog.error(self, "Lỗi", f"Không thể tải danh sách kho:\n{str(e)}")
    
    def load_data(self):
        """Load data from database"""
        kho = self.kho_selector.currentData()
        
        if not kho:
            self.table_with_toolbar.set_data([])
            self._update_statistics([])
            self.info_label.setText("Chọn một kho để xem vị trí")
            return
        
        self.current_kho = kho
        
        try:
            vi_tris = self.vi_tri_service.get_vi_tri_by_kho(kho.ma_kho)
            
            # Convert to table data
            data = []
            for vt in vi_tris:
                data.append({
                    "Mã Vị Trí": vt.ma_vi_tri,
                    "Khu Vực": vt.khu_vuc,
                    "Hàng": vt.hang,
                    "Tầng": vt.tang,
                    "Diện Tích": f"{vt.dien_tich:,.0f} m²",
                    "Giá Thuê": format_currency(vt.gia_thue),
                    "Trạng Thái": self._get_trang_thai_label(vt.trang_thai),
                    "_data": vt
                })
            
            self.table_with_toolbar.set_data(data)
            
            # Update statistics
            self._update_statistics(vi_tris)
            
            # Update info
            self.info_label.setText(f"Tổng: {len(data)} vị trí")
            
        except Exception as e:
            MessageDialog.error(self, "Lỗi", f"Không thể tải dữ liệu:\n{str(e)}")
    
    def _update_statistics(self, vi_tris: List[ViTri]):
        """Update statistics bar"""
        tong = len(vi_tris)
        trong = sum(1 for v in vi_tris if v.trang_thai == TrangThaiViTriEnum.TRONG)
        da_thue = sum(1 for v in vi_tris if v.trang_thai == TrangThaiViTriEnum.DA_THUE)
        ty_le_trong = (trong / tong * 100) if tong > 0 else 0
        
        self.stat_tong.setText(str(tong))
        self.stat_trong.setText(str(trong))
        self.stat_da_thue.setText(str(da_thue))
        self.stat_ty_le.setText(f"{ty_le_trong:.1f}%")
    
    def _get_trang_thai_label(self, trang_thai) -> str:
        """Get status label with emoji and color"""
        labels = {
            "trong": "✅ Trống",
            "da_thue": "📋 Đã thuê",
            "bao_tri": "🔧 Bảo trì",
        }
        return labels.get(str(trang_thai), str(trang_thai))
    
    def _on_kho_changed(self, index: int):
        """Handle warehouse selection change"""
        self.load_data()
    
    def _on_row_selected(self, row_index: int, row_data: dict):
        """Handle row selection"""
        if "_data" in row_data:
            self.current_vi_tri = row_data["_data"]
            self.vi_tri_selected.emit(self.current_vi_tri)
            self.info_label.setText(
                f"Đang xem: {self.current_vi_tri.ma_vi_tri} - {self._get_trang_thai_label(self.current_vi_tri.trang_thai)}"
            )
    
    def _on_row_double_clicked(self, row_index: int, row_data: dict):
        """Handle row double click"""
        if "_data" in row_data:
            self._on_edit_clicked()
    
    def _on_add_clicked(self):
        """Handle add button click"""
        kho = self.kho_selector.currentData()
        
        if not kho:
            MessageDialog.warning(self, "Cảnh báo", "Vui lòng chọn một kho trước")
            return
        
        dialog = ViTriForm(self, kho=kho)
        dialog.vi_tri_saved.connect(self._on_vi_tri_saved)
        dialog.exec()
    
    def _on_vi_tri_saved(self, vi_tri: ViTri):
        """Handle vi_tri saved from form"""
        self.load_data()  # Refresh table
        self.vi_tri_added.emit(vi_tri)
    
    def _on_edit_clicked(self):
        """Handle edit button click"""
        if not self.current_vi_tri:
            MessageDialog.warning(self, "Cảnh báo", "Vui lòng chọn một vị trí để sửa")
            return
        
        dialog = ViTriForm(self, vi_tri=self.current_vi_tri)
        dialog.vi_tri_saved.connect(self._on_vi_tri_saved)
        dialog.exec()
    
    def _on_delete_clicked(self):
        """Handle delete button click"""
        if not self.current_vi_tri:
            MessageDialog.warning(self, "Cảnh báo", "Vui lòng chọn một vị trí để xóa")
            return
        
        # Confirm delete
        confirmed = ConfirmDialog.ask_delete(
            self, 
            f"Vị trí {self.current_vi_tri.ma_vi_tri}"
        )
        
        if confirmed:
            try:
                success = self.vi_tri_service.delete_vi_tri(self.current_vi_tri.ma_vi_tri)
                if success:
                    MessageDialog.success(self, "Thành công", "Đã xóa vị trí thành công")
                    self.vi_tri_deleted.emit(self.current_vi_tri.ma_vi_tri)
                    self.load_data()
                    self.current_vi_tri = None
                else:
                    MessageDialog.error(self, "Lỗi", "Không thể xóa vị trí")
            except ValueError as e:
                MessageDialog.error(self, "Không thể xóa", str(e))
            except Exception as e:
                MessageDialog.error(self, "Lỗi", f"Không thể xóa vị trí:\n{str(e)}")
    
    def _on_refresh_clicked(self):
        """Handle refresh button click"""
        self.load_data()
    
    def _on_export_clicked(self):
        """Handle export button click"""
        try:
            from src.utils.export_service import export_vi_tri_to_excel
            from PyQt6.QtWidgets import QFileDialog
            
            # Get all data
            vi_tris_data = []
            for row in self.table_with_toolbar._data:
                if "_data" in row:
                    vt = row["_data"]
                    vi_tris_data.append({
                        'ma_vi_tri': vt.ma_vi_tri,
                        'ma_kho': vt.ma_kho,
                        'khu_vuc': vt.khu_vuc,
                        'hang': vt.hang,
                        'tang': vt.tang,
                        'dien_tich': vt.dien_tich,
                        'chieu_cao': vt.chieu_cao,
                        'gia_thue': vt.gia_thue,
                        'trang_thai_label': self._get_trang_thai_label(vt.trang_thai),
                    })
            
            if not vi_tris_data:
                MessageDialog.warning(self, "Cảnh báo", "Không có dữ liệu để xuất")
                return
            
            # Ask for save location
            default_name = f"vi_tri_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Xuất Excel",
                default_name,
                "Excel Files (*.xlsx)"
            )
            
            if file_path:
                output = export_vi_tri_to_excel(vi_tris_data, file_path)
                MessageDialog.success(self, "Thành công", f"Đã xuất file Excel:\n{output}")
                
        except ImportError as e:
            MessageDialog.error(self, "Thiếu thư viện", "Cần cài đặt pandas và openpyxl:\npip install pandas openpyxl")
        except Exception as e:
            MessageDialog.error(self, "Lỗi", f"Không thể xuất Excel:\n{str(e)}")
    
    def _on_search_changed(self, text: str):
        """Handle search"""
        kho = self.kho_selector.currentData()
        
        if not kho:
            return
        
        if not text.strip():
            self.load_data()
        else:
            try:
                vi_tris = self.vi_tri_service.get_vi_tri_by_kho(kho.ma_kho)
                
                # Filter by search text
                search_text = text.strip().lower()
                filtered = [
                    vt for vt in vi_tris
                    if search_text in vt.ma_vi_tri.lower() or
                       search_text in vt.khu_vuc.lower() or
                       search_text in vt.hang.lower()
                ]
                
                # Convert to table data
                data = []
                for vt in filtered:
                    data.append({
                        "Mã Vị Trí": vt.ma_vi_tri,
                        "Khu Vực": vt.khu_vuc,
                        "Hàng": vt.hang,
                        "Tầng": vt.tang,
                        "Diện Tích": f"{vt.dien_tich:,.0f} m²",
                        "Giá Thuê": format_currency(vt.gia_thue),
                        "Trạng Thái": self._get_trang_thai_label(vt.trang_thai),
                        "_data": vt
                    })
                
                self.table_with_toolbar.set_data(data)
                self.info_label.setText(f"Tìm thấy: {len(data)} vị trí")
                
            except Exception as e:
                MessageDialog.error(self, "Lỗi", f"Không thể tìm kiếm:\n{str(e)}")
    
    def _apply_filters(self):
        """Apply filters"""
        kho = self.kho_selector.currentData()
        
        if not kho:
            return
        
        try:
            trang_thai = self.filter_trang_thai.currentData()
            
            vi_tris = self.vi_tri_service.get_vi_tri_by_kho(kho.ma_kho)
            
            # Filter by status
            if trang_thai:
                vi_tris = [v for v in vi_tris if str(v.trang_thai) == trang_thai]
            
            # Convert to table data
            data = []
            for vt in vi_tris:
                data.append({
                    "Mã Vị Trí": vt.ma_vi_tri,
                    "Khu Vực": vt.khu_vuc,
                    "Hàng": vt.hang,
                    "Tầng": vt.tang,
                    "Diện Tích": f"{vt.dien_tich:,.0f} m²",
                    "Giá Thuê": format_currency(vt.gia_thue),
                    "Trạng Thái": self._get_trang_thai_label(vt.trang_thai),
                    "_data": vt
                })
            
            self.table_with_toolbar.set_data(data)
            self._update_statistics(data)
            self.info_label.setText(f"Tổng: {len(data)} vị trí")
            
        except Exception as e:
            MessageDialog.error(self, "Lỗi", f"Không thể lọc dữ liệu:\n{str(e)}")
    
    def refresh_data(self):
        """Refresh data from outside"""
        self.load_data()
    
    def set_kho(self, kho: Kho):
        """Set current warehouse programmatically"""
        for i in range(self.kho_selector.count()):
            if self.kho_selector.itemData(i) == kho:
                self.kho_selector.setCurrentIndex(i)
                break


class ViTriDetailView(QWidget):
    """
    Detail view for a single position
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_vi_tri = None
        self.setup_ui()
    
    def setup_ui(self):
        """Setup UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title = QLabel("📍 CHI TIẾT VỊ TRÍ")
        title.setStyleSheet("""
            QLabel {
                font-size: 20px;
                font-weight: 700;
                color: #31302e;
                padding: 10px 0;
            }
        """)
        layout.addWidget(title)
        
        # Placeholder
        placeholder = QLabel("Chọn một vị trí để xem chi tiết")
        placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        placeholder.setStyleSheet("""
            QLabel {
                color: #757575;
                font-size: 16px;
                padding: 100px;
            }
        """)
        layout.addWidget(placeholder, 1)
    
    def set_vi_tri(self, vi_tri: ViTri):
        """Set position to display"""
        self.current_vi_tri = vi_tri
        # TODO: Implement detail view


__all__ = ['ViTriView', 'ViTriDetailView']
