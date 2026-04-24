#!/usr/bin/env python3
"""
Hàng hóa View - Giao diện Quản lý Hàng hóa
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QComboBox, QMessageBox, QDoubleSpinBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from datetime import datetime
from typing import Optional, Dict, Any

from src.services import HangHoaService, HopDongService
from src.models import HangHoa
from src.gui.widgets import DataTableWithToolbar, SearchBox
from src.gui.dialogs import MessageDialog, ConfirmDialog
from src.utils.formatters import format_currency, format_number


class HangHoaView(QWidget):
    """
    Giao diện Quản lý Hàng hóa
    """
    
    # Signals
    hang_hoa_selected = pyqtSignal(object)  # HangHoa object
    hang_hoa_added = pyqtSignal(object)  # HangHoa object
    hang_hoa_updated = pyqtSignal(object)  # HangHoa object
    hang_hoa_deleted = pyqtSignal(str)  # ma_hang_hoa
    import_clicked = pyqtSignal()
    export_clicked = pyqtSignal(object)  # HangHoa object
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.service = HangHoaService()
        self.hop_dong_service = HopDongService()
        self.current_hang_hoa: Optional[HangHoa] = None
        self.setup_ui()
        self.setup_connections()
        self.load_data()
    
    def setup_ui(self):
        """Setup UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)
        
        # Title
        title = QLabel("📦 QUẢN LÝ HÀNG HÓA")
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
            headers=["Mã HH", "Tên Hàng", "Loại", "SL", "ĐVT", "Giá Trị", "Trạng Thái", "Hợp Đồng"]
        )
        layout.addWidget(self.table_with_toolbar, 1)
        
        # Info label
        self.info_label = QLabel("Tổng: 0 mặt hàng")
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
        
        # Total items
        layout.addWidget(QLabel("Tổng:"))
        self.stat_tong = QLabel("0")
        self.stat_tong.setStyleSheet("font-size: 24px; font-weight: 700; color: #1976d2;")
        layout.addWidget(self.stat_tong)
        
        layout.addSpacing(20)
        
        # In stock
        layout.addWidget(QLabel("Trong kho:"))
        self.stat_trong_kho = QLabel("0")
        self.stat_trong_kho.setStyleSheet("font-size: 24px; font-weight: 700; color: #1aae39;")
        layout.addWidget(self.stat_trong_kho)
        
        layout.addSpacing(20)
        
        # Low stock
        layout.addWidget(QLabel("Sắp hết:"))
        self.stat_low_stock = QLabel("0")
        self.stat_low_stock.setStyleSheet("font-size: 24px; font-weight: 700; color: #ff9800;")
        layout.addWidget(self.stat_low_stock)
        
        layout.addSpacing(20)
        
        # Total value
        layout.addWidget(QLabel("Tổng giá trị:"))
        self.stat_tong_gia_tri = QLabel("0₫")
        self.stat_tong_gia_tri.setStyleSheet("font-size: 24px; font-weight: 700; color: #4caf50;")
        layout.addWidget(self.stat_tong_gia_tri)
        
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
        self.search_box = SearchBox(placeholder="🔍 Tìm theo tên, loại hàng...")
        layout.addWidget(self.search_box, 1)
        
        # Filter by contract
        layout.addWidget(QLabel("Hợp đồng:"))
        self.filter_hop_dong = QComboBox()
        self.filter_hop_dong.addItem("Tất cả", None)
        self.filter_hop_dong.setFixedWidth(200)
        self._load_hop_dongs()
        layout.addWidget(self.filter_hop_dong)
        
        # Filter by type
        layout.addWidget(QLabel("Loại hàng:"))
        self.filter_loai_hang = QComboBox()
        self.filter_loai_hang.addItem("Tất cả", "")
        self.filter_loai_hang.addItem("Điện tử", "Điện tử")
        self.filter_loai_hang.addItem("May mặc", "May mặc")
        self.filter_loai_hang.addItem("Thực phẩm", "Thực phẩm")
        self.filter_loai_hang.addItem("Khác", "Khác")
        self.filter_loai_hang.setFixedWidth(150)
        layout.addWidget(self.filter_loai_hang)
        
        # Filter by status
        layout.addWidget(QLabel("Trạng thái:"))
        self.filter_trang_thai = QComboBox()
        self.filter_trang_thai.addItem("Tất cả", "")
        self.filter_trang_thai.addItem("✅ Trong kho", "trong_kho")
        self.filter_trang_thai.addItem("📤 Đã xuất", "da_xuat")
        self.filter_trang_thai.setFixedWidth(150)
        layout.addWidget(self.filter_trang_thai)
        
        return filter_bar
    
    def _load_hop_dongs(self):
        """Load contracts into filter"""
        try:
            hop_dongs = self.hop_dong_service.get_all(limit=100)
            for hd in hop_dongs:
                display = f"{hd.ma_hop_dong} - {hd.ma_khach_hang}"
                self.filter_hop_dong.addItem(display, hd.ma_hop_dong)
        except Exception as e:
            print(f"Error loading contracts: {e}")
    
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
        
        # Custom buttons
        self._connect_custom_buttons()
        
        # Search & filter
        self.search_box.search_changed.connect(self._on_search_changed)
        self.filter_hop_dong.currentIndexChanged.connect(self._apply_filters)
        self.filter_loai_hang.currentIndexChanged.connect(self._apply_filters)
        self.filter_trang_thai.currentIndexChanged.connect(self._apply_filters)
    
    def _connect_custom_buttons(self):
        """Connect custom buttons (Import, Export)"""
        # Note: Import and Export buttons should be added to the toolbar in DataTableWithToolbar
        # For now, connect to the existing export button and add import button separately
        
        # Connect to existing export button signal
        self.table_with_toolbar.export_clicked.connect(self._on_export_clicked)
        
        # Import button needs to be added separately - will add to filter bar
        # This is a workaround - ideally DataTableWithToolbar should support custom buttons
    
    def load_data(self):
        """Load data from database"""
        try:
            hang_hoas = self.service.get_all(limit=1000)
            
            # Convert to table data
            data = []
            
            for hh in hang_hoas:
                data.append({
                    "Mã HH": hh.ma_hang_hoa,
                    "Tên Hàng": hh.ten_hang,
                    "Loại": hh.loai_hang,
                    "SL": hh.so_luong,
                    "ĐVT": hh.don_vi,
                    "Giá Trị": format_currency(hh.gia_tri or 0),
                    "Trạng Thái": self._get_trang_thai_label(hh.trang_thai),
                    "Hợp Đồng": hh.ma_hop_dong,
                    "__data": hh,
                    "_is_low_stock": hh.so_luong <= 10 and hh.trang_thai == 'trong_kho'
                })
            
            self.table_with_toolbar.set_data(data)
            
            # Update statistics
            self._update_statistics(hang_hoas)
            
            # Update info
            self.info_label.setText(f"Tổng: {len(data)} mặt hàng")
            
        except Exception as e:
            MessageDialog.error(self, "Lỗi", f"Không thể tải dữ liệu:\n{str(e)}")
    
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
    
    def _update_statistics(self, hang_hoas: list):
        """Update statistics bar"""
        tong = len(hang_hoas)
        trong_kho = sum(1 for h in hang_hoas if h.trang_thai == 'trong_kho')
        low_stock = sum(1 for h in hang_hoas if h.so_luong <= 10 and h.trang_thai == 'trong_kho')
        tong_gia_tri = sum(h.gia_tri or 0 for h in hang_hoas)
        
        self.stat_tong.setText(str(tong))
        self.stat_trong_kho.setText(str(trong_kho))
        self.stat_low_stock.setText(str(low_stock))
        self.stat_tong_gia_tri.setText(format_currency(tong_gia_tri))
        
        # Highlight low stock warning
        if low_stock > 0:
            self.stat_low_stock.setStyleSheet("""
                QLabel {
                    font-size: 24px;
                    font-weight: 700;
                    color: #f44336;
                    background-color: #ffebee;
                    padding: 4px 8px;
                    border-radius: 4px;
                }
            """)
        else:
            self.stat_low_stock.setStyleSheet("""
                QLabel {
                    font-size: 24px;
                    font-weight: 700;
                    color: #1aae39;
                }
            """)
    
    def _on_row_selected(self, row_index: int, row_data: dict):
        """Handle row selection"""
        if "_data" in row_data:
            self.current_hang_hoa = row_data["_data"]
            self.hang_hoa_selected.emit(self.current_hang_hoa)
            
            # Highlight low stock
            if row_data.get('_is_low_stock'):
                self.info_label.setText(
                    f"⚠️ CẢNH BÁO: {self.current_hang_hoa.ten_hang} sắp hết hàng! "
                    f"(Còn: {self.current_hang_hoa.so_luong} {self.current_hang_hoa.don_vi})"
                )
                self.info_label.setStyleSheet("""
                    QLabel {
                        color: #d32f2f;
                        font-size: 14px;
                        font-weight: 600;
                        padding: 8px;
                        background-color: #ffebee;
                        border-radius: 6px;
                    }
                """)
            else:
                self.info_label.setText(
                    f"Đang xem: {self.current_hang_hoa.ma_hang_hoa} - {self.current_hang_hoa.ten_hang}"
                )
                self.info_label.setStyleSheet("""
                    QLabel {
                        color: #615d59;
                        font-size: 14px;
                        padding: 8px;
                        background-color: #f6f5f4;
                        border-radius: 6px;
                    }
                """)
    
    def _on_row_double_clicked(self, row_index: int, row_data: dict):
        """Handle row double click"""
        if "_data" in row_data:
            self._on_edit_clicked()
    
    def _on_add_clicked(self):
        """Handle add button click"""
        try:
            from src.gui.forms import HangHoaForm
            from src.services import HangHoaService
            
            dialog = HangHoaForm(self)
            dialog.hang_hoa_saved.connect(self._on_hang_hoa_saved)
            dialog.exec()
        except ImportError as e:
            MessageDialog.error(self, "Lỗi", f"Không thể mở form: {str(e)}")
    
    def _on_form_accepted(self, form_data: dict):
        """Handle form accepted with data"""
        try:
            service = HangHoaService()
            hang_hoa = service.create(form_data)
            self.load_data()  # Refresh table
            self.hang_hoa_added.emit(hang_hoa)
            MessageDialog.success(self, "Thành công", f"Đã thêm hàng hóa {hang_hoa.ma_hang_hoa}")
        except Exception as e:
            MessageDialog.error(self, "Lỗi", f"Không thể lưu hàng hóa: {str(e)}")
    
    def _on_edit_clicked(self):
        """Handle edit button click"""
        if not self.current_hang_hoa:
            MessageDialog.warning(self, "Cảnh báo", "Vui lòng chọn một mặt hàng để sửa")
            return
        
        try:
            from src.gui.forms import HangHoaForm
            from src.services import HangHoaService
            
            # Pass only the ID, not the object (to avoid session issues)
            ma_hh = self.current_hang_hoa.ma_hang_hoa
            dialog = HangHoaForm(self, hang_hoa=self.current_hang_hoa)
            dialog.hang_hoa_saved.connect(lambda hang_hoa: self._on_edit_accepted(hang_hoa))
            dialog.exec()
        except ImportError as e:
            MessageDialog.error(self, "Lỗi", f"Không thể mở form: {str(e)}")
    
    def _on_hang_hoa_saved(self, hang_hoa: HangHoa):
        """Handle goods saved from form"""
        self.load_data()  # Refresh table
        self.hang_hoa_added.emit(hang_hoa)
        MessageDialog.success(self, "Thành công", f"Đã thêm hàng hóa {hang_hoa.ma_hang_hoa}")
    
    def _on_edit_accepted(self, hang_hoa: HangHoa):
        """Handle edit form accepted with data"""
        try:
            service = HangHoaService()
            updated = service.update(hang_hoa.ma_hang_hoa, {
                'ten_hang': hang_hoa.ten_hang,
                'loai_hang': hang_hoa.loai_hang,
                'so_luong': hang_hoa.so_luong,
                'don_vi': hang_hoa.don_vi,
                'trong_luong': hang_hoa.trong_luong,
                'kich_thuoc': hang_hoa.kich_thuoc,
                'gia_tri': hang_hoa.gia_tri,
                'vi_tri_luu_tru': hang_hoa.vi_tri_luu_tru,
                'ghi_chu': hang_hoa.ghi_chu,
                'hinh_anh': hang_hoa.hinh_anh,
                'trang_thai': hang_hoa.trang_thai.value if hasattr(hang_hoa.trang_thai, 'value') else hang_hoa.trang_thai
            })
            self.load_data()  # Refresh table
            self.hang_hoa_updated.emit(updated)
            MessageDialog.success(self, "Thành công", f"Đã cập nhật hàng hóa {updated.ma_hang_hoa}")
        except Exception as e:
            MessageDialog.error(self, "Lỗi", f"Không thể cập nhật hàng hóa: {str(e)}")
    
    def _on_delete_clicked(self):
        """Handle delete button click"""
        if not self.current_hang_hoa:
            MessageDialog.warning(self, "Cảnh báo", "Vui lòng chọn một mặt hàng để xóa")
            return
        
        # Confirm delete
        confirmed = ConfirmDialog.ask_delete(
            self, 
            f"{self.current_hang_hoa.ten_hang} ({self.current_hang_hoa.ma_hang_hoa})"
        )
        
        if confirmed:
            try:
                success = self.service.delete(self.current_hang_hoa.ma_hang_hoa)
                if success:
                    MessageDialog.success(self, "Thành công", "Đã xóa mặt hàng thành công")
                    self.hang_hoa_deleted.emit(self.current_hang_hoa.ma_hang_hoa)
                    self.load_data()
                    self.current_hang_hoa = None
                else:
                    MessageDialog.error(self, "Lỗi", "Không thể xóa mặt hàng")
            except Exception as e:
                MessageDialog.error(self, "Lỗi", f"Không thể xóa mặt hàng:\n{str(e)}")
    
    def _on_refresh_clicked(self):
        """Handle refresh button click"""
        self.load_data()
    
    def _on_import_clicked(self):
        """Handle import button click"""
        self.import_clicked.emit()
    
    def _on_export_clicked(self):
        """Handle export button click"""
        if not self.current_hang_hoa:
            MessageDialog.warning(self, "Cảnh báo", "Vui lòng chọn một mặt hàng để xuất")
            return
        
        if self.current_hang_hoa.trang_thai == 'da_xuat':
            MessageDialog.warning(self, "Cảnh báo", "Mặt hàng đã xuất kho rồi")
            return
        
        self.export_clicked.emit(self.current_hang_hoa)
    
    def _on_search_changed(self, text: str):
        """Handle search"""
        if not text.strip():
            self.load_data()
        else:
            try:
                hang_hoas = self.service.search(text.strip(), limit=100)
                
                # Convert to table data
                data = []
                for hh in hang_hoas:
                    data.append({
                        "Mã HH": hh.ma_hang_hoa,
                        "Tên Hàng": hh.ten_hang,
                        "Loại": hh.loai_hang,
                        "SL": hh.so_luong,
                        "ĐVT": hh.don_vi,
                        "Giá Trị": format_currency(hh.gia_tri or 0),
                        "Trạng Thái": self._get_trang_thai_label(hh.trang_thai),
                        "Hợp Đồng": hh.ma_hop_dong,
                        "__data": hh,
                        "_is_low_stock": hh.so_luong <= 10 and hh.trang_thai == 'trong_kho'
                    })
                
                self.table_with_toolbar.set_data(data)
                self.info_label.setText(f"Tìm thấy: {len(data)} mặt hàng")
                
            except Exception as e:
                MessageDialog.error(self, "Lỗi", f"Không thể tìm kiếm:\n{str(e)}")
    
    def _apply_filters(self):
        """Apply filters"""
        try:
            ma_hop_dong = self.filter_hop_dong.currentData()
            loai_hang = self.filter_loai_hang.currentData()
            trang_thai = self.filter_trang_thai.currentData()
            
            hang_hoas = self.service.get_all(limit=1000)
            
            # Filter by contract
            if ma_hop_dong:
                hang_hoas = [h for h in hang_hoas if h.ma_hop_dong == ma_hop_dong]
            
            # Filter by type
            if loai_hang:
                hang_hoas = [h for h in hang_hoas if h.loai_hang == loai_hang]
            
            # Filter by status
            if trang_thai:
                hang_hoas = [h for h in hang_hoas if h.trang_thai == trang_thai]
            
            # Convert to table data
            data = []
            for hh in hang_hoas:
                data.append({
                    "Mã HH": hh.ma_hang_hoa,
                    "Tên Hàng": hh.ten_hang,
                    "Loại": hh.loai_hang,
                    "SL": hh.so_luong,
                    "ĐVT": hh.don_vi,
                    "Giá Trị": format_currency(hh.gia_tri or 0),
                    "Trạng Thái": self._get_trang_thai_label(hh.trang_thai),
                    "Hợp Đồng": hh.ma_hop_dong,
                    "__data": hh,
                    "_is_low_stock": hh.so_luong <= 10 and hh.trang_thai == 'trong_kho'
                })
            
            self.table_with_toolbar.set_data(data)
            self._update_statistics(data)
            self.info_label.setText(f"Tổng: {len(data)} mặt hàng")
            
        except Exception as e:
            MessageDialog.error(self, "Lỗi", f"Không thể lọc dữ liệu:\n{str(e)}")
    
    def refresh_data(self):
        """Refresh data from outside"""
        self.load_data()


__all__ = ['HangHoaView']
