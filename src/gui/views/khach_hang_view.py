#!/usr/bin/env python3
"""
Khách hàng View - Giao diện Quản lý Khách hàng
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QComboBox, QMessageBox, QHeaderView
)
from PyQt6.QtCore import Qt, pyqtSignal
from typing import Optional, Dict, Any

from src.services import KhachHangService
from src.models import KhachHang, LoaiKhachEnum, TrangThaiKHEnum
from src.gui.widgets import DataTableWithToolbar, SearchBox
from src.gui.dialogs import MessageDialog, ConfirmDialog
from src.utils.formatters import format_phone, format_date


class KhachHangView(QWidget):
    """
    Giao diện Quản lý Khách hàng
    """
    
    # Signals
    khach_hang_selected = pyqtSignal(object)  # KhachHang object
    khach_hang_added = pyqtSignal(object)  # KhachHang object
    khach_hang_updated = pyqtSignal(object)  # KhachHang object
    khach_hang_deleted = pyqtSignal(str)  # ma_khach_hang
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.service = KhachHangService()
        self.current_khach_hang: Optional[KhachHang] = None
        self.setup_ui()
        self.setup_connections()
        self.load_data()
    
    def setup_ui(self):

        """Setup UI"""
        # Modern CSS
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
                padding: 8px 16px;
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
                font-size: 24px;
                font-weight: 700;
                color: #31302e;
                padding: 10px 0;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 30, 40, 30)
        layout.setSpacing(24)
        layout.setSpacing(16)
        
        # Title
        title = QLabel("👥 QUẢN LÝ KHÁCH HÀNG")
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
        
        # Filter bar
        filter_bar = self._create_filter_bar()
        layout.addWidget(filter_bar)
        
        # Data table with toolbar
        self.table_with_toolbar = DataTableWithToolbar(
            headers=["Mã KH", "Họ tên", "Loại", "SĐT", "Email", "Trạng thái"]
        )
        
        # Connect export button (already in DataTableWithToolbar)
        self.table_with_toolbar.export_clicked.connect(self._on_export_clicked)
        
        layout.addWidget(self.table_with_toolbar, 1)
        
        # Info label
        self.info_label = QLabel("Chọn một khách hàng để xem chi tiết")
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
        self.search_box = SearchBox(placeholder="🔍 Tìm theo tên, SĐT, email...")
        layout.addWidget(self.search_box, 1)
        
        # Filter by type
        layout.addWidget(QLabel("Loại:"))
        self.filter_loai = QComboBox()
        self.filter_loai.addItem("Tất cả", "")
        self.filter_loai.addItem("Cá nhân", "ca_nhan")
        self.filter_loai.addItem("Doanh nghiệp", "doanh_nghiep")
        self.filter_loai.setFixedWidth(180)
        layout.addWidget(self.filter_loai)
        
        # Filter by status
        layout.addWidget(QLabel("Trạng thái:"))
        self.filter_trang_thai = QComboBox()
        self.filter_trang_thai.addItem("Tất cả", "")
        self.filter_trang_thai.addItem("Hoạt động", "hoat_dong")
        self.filter_trang_thai.addItem("Tạm khóa", "tam_khoa")
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
        
        # Search & filter
        self.search_box.search_changed.connect(self._on_search_changed)
        self.filter_loai.currentIndexChanged.connect(self._apply_filters)
        self.filter_trang_thai.currentIndexChanged.connect(self._apply_filters)
    
    def load_data(self):
        """Load data from database"""
        try:
            khach_hangs = self.service.get_all(limit=1000)
            
            # Convert to table data
            data = []
            for kh in khach_hangs:
                if kh.trang_thai != TrangThaiKHEnum.DA_XOA:
                    data.append({
                        "Mã KH": kh.ma_khach_hang,
                        "Họ tên": kh.ho_ten,
                        "Loại": "Doanh nghiệp" if kh.loai_khach == LoaiKhachEnum.DOANH_NGHIEP else "Cá nhân",
                        "SĐT": format_phone(kh.so_dien_thoai),
                        "Email": kh.email or "-",
                        "Trạng thái": self._get_trang_thai_label(kh.trang_thai),
                        "__data": kh  # Store object for reference
                    })
            
            self.table_with_toolbar.set_data(data)
            
            # Update info
            self.info_label.setText(f"Tổng: {len(data)} khách hàng")
            
        except Exception as e:
            MessageDialog.error(self, "Lỗi", f"Không thể tải dữ liệu:\n{str(e)}")
    
    def _get_trang_thai_label(self, trang_thai) -> str:
        """Get status label with emoji"""
        # Handle both enum object and string values
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
    
    def _on_row_selected(self, row_index: int, row_data: dict):
        """Handle row selection"""
        if "__data" in row_data:
            self.current_khach_hang = row_data["__data"]
            self.khach_hang_selected.emit(self.current_khach_hang)
            self.info_label.setText(
                f"Đang xem: {self.current_khach_hang.ho_ten} ({self.current_khach_hang.ma_khach_hang})"
            )
    
    def _on_row_double_clicked(self, row_index: int, row_data: dict):
        """Handle row double click"""
        if "__data" in row_data:
            self._on_edit_clicked()
    
    def _on_add_clicked(self):
        """Handle add button click"""
        try:
            from src.gui.forms import KhachHangForm
            from src.services import KhachHangService
            
            dialog = KhachHangForm(self)
            dialog.accepted_with_data.connect(self._on_form_accepted)
            dialog.exec()
        except ImportError as e:
            MessageDialog.error(self, "Lỗi", f"Không thể mở form: {str(e)}")
    
    def _on_form_accepted(self, form_data: dict):
        """Handle form accepted with data"""
        try:
            service = KhachHangService()
            khach_hang = service.create(form_data)
            self.load_data()  # Refresh table
            self.khach_hang_added.emit(khach_hang)
            MessageDialog.success(self, "Thành công", f"Đã thêm khách hàng {khach_hang.ma_khach_hang}")
        except Exception as e:
            MessageDialog.error(self, "Lỗi", f"Không thể lưu khách hàng: {str(e)}")
    
    def _on_edit_clicked(self):
        """Handle edit button click"""
        if not self.current_khach_hang:
            MessageDialog.warning(self, "Cảnh báo", "Vui lòng chọn một khách hàng để sửa")
            return
        
        try:
            from src.gui.forms import KhachHangForm
            from src.services import KhachHangService
            
            # Pass only the ID, not the object (to avoid session issues)
            ma_kh = self.current_khach_hang.ma_khach_hang
            dialog = KhachHangForm(self, khach_hang=self.current_khach_hang)
            dialog.accepted_with_data.connect(lambda data: self._on_edit_accepted(data, ma_kh))
            dialog.exec()
        except ImportError as e:
            MessageDialog.error(self, "Lỗi", f"Không thể mở form: {str(e)}")
    
    def _on_edit_accepted(self, form_data: dict, ma_khach_hang: str):
        """Handle edit form accepted with data"""
        try:
            service = KhachHangService()
            updated = service.update(ma_khach_hang, form_data)
            self.load_data()  # Refresh table
            if updated:
                self.khach_hang_updated.emit(updated)
                MessageDialog.success(self, "Thành công", f"Đã cập nhật khách hàng {updated.ma_khach_hang}")
            else:
                MessageDialog.error(self, "Lỗi", "Không tìm thấy khách hàng")
        except Exception as e:
            MessageDialog.error(self, "Lỗi", f"Không thể cập nhật khách hàng: {str(e)}")
    
    def _on_delete_clicked(self):
        """Handle delete button click"""
        if not self.current_khach_hang:
            MessageDialog.warning(self, "Cảnh báo", "Vui lòng chọn một khách hàng để xóa")
            return
        
        # Confirm delete
        confirmed = ConfirmDialog.ask_delete(
            self, 
            f"{self.current_khach_hang.ho_ten} ({self.current_khach_hang.ma_khach_hang})"
        )
        
        if confirmed:
            try:
                success = self.service.delete(self.current_khach_hang.ma_khach_hang)
                if success:
                    MessageDialog.success(self, "Thành công", "Đã xóa khách hàng thành công")
                    self.khach_hang_deleted.emit(self.current_khach_hang.ma_khach_hang)
                    self.load_data()  # Reload data
                    self.current_khach_hang = None
                else:
                    MessageDialog.error(self, "Lỗi", "Không thể xóa khách hàng")
            except ValueError as e:
                MessageDialog.error(self, "Không thể xóa", str(e))
            except Exception as e:
                MessageDialog.error(self, "Lỗi", f"Không thể xóa khách hàng:\n{str(e)}")
    
    def _on_refresh_clicked(self):
        """Handle refresh button click"""
        self.load_data()
    
    def _on_export_clicked(self):
        """Handle export button click"""
        try:
            from src.services.khach_hang_service import export_khach_hang_to_excel
            
            # Get current data (filtered)
            khach_hangs = []
            for row in range(self.table_with_toolbar.table.rowCount()):
                item = self.table_with_toolbar.table.item(row, 0)
                if item and "__data" in item.data(Qt.ItemDataRole.UserRole):
                    khach_hangs.append(item.data(Qt.ItemDataRole.UserRole)["__data"])
            
            if not khach_hangs:
                MessageDialog.warning(self, "Cảnh báo", "Không có dữ liệu để xuất")
                return
            
            # Export to Excel
            from PyQt6.QtWidgets import QFileDialog
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Xuất Excel",
                "",
                "Excel Files (*.xlsx)"
            )
            
            if file_path:
                export_path = export_khach_hang_to_excel(khach_hangs, file_path)
                MessageDialog.success(
                    self, 
                    "Thành công", 
                    f"Đã xuất {len(khach_hangs)} khách hàng ra file:\n{export_path}"
                )
        
        except ImportError:
            MessageDialog.error(
                self, 
                "Lỗi", 
                "Thiếu thư viện openpyxl.\nVui lòng cài đặt: pip install openpyxl"
            )
        except Exception as e:
            MessageDialog.error(self, "Lỗi", f"Không thể xuất file:\n{str(e)}")
    
    def _on_search_changed(self, text: str):
        """Handle search"""
        if not text.strip():
            self.load_data()
        else:
            try:
                results = self.service.search(text, limit=100)
                
                # Convert to table data
                data = []
                for kh in results:
                    data.append({
                        "Mã KH": kh.ma_khach_hang,
                        "Họ tên": kh.ho_ten,
                        "Loại": "Doanh nghiệp" if kh.loai_khach == LoaiKhachEnum.DOANH_NGHIEP else "Cá nhân",
                        "SĐT": format_phone(kh.so_dien_thoai),
                        "Email": kh.email or "-",
                        "Trạng thái": self._get_trang_thai_label(kh.trang_thai),
                        "__data": kh
                    })
                
                self.table_with_toolbar.set_data(data)
                self.info_label.setText(f"Tìm thấy: {len(data)} khách hàng")
                
            except Exception as e:
                MessageDialog.error(self, "Lỗi", f"Không thể tìm kiếm:\n{str(e)}")
    
    def _apply_filters(self):
        """Apply filters"""
        try:
            loai = self.filter_loai.currentData()
            trang_thai = self.filter_trang_thai.currentData()
            
            khach_hangs = self.service.get_all(limit=1000)
            
            # Filter
            if loai:
                khach_hangs = [kh for kh in khach_hangs if str(kh.loai_khach) == loai]
            if trang_thai:
                khach_hangs = [kh for kh in khach_hangs if str(kh.trang_thai) == trang_thai]
            
            # Convert to table data
            data = []
            for kh in khach_hangs:
                data.append({
                    "Mã KH": kh.ma_khach_hang,
                    "Họ tên": kh.ho_ten,
                    "Loại": "Doanh nghiệp" if kh.loai_khach == LoaiKhachEnum.DOANH_NGHIEP else "Cá nhân",
                    "SĐT": format_phone(kh.so_dien_thoai),
                    "Email": kh.email or "-",
                    "Trạng thái": self._get_trang_thai_label(kh.trang_thai),
                    "__data": kh
                })
            
            self.table_with_toolbar.set_data(data)
            self.info_label.setText(f"Tổng: {len(data)} khách hàng")
            
        except Exception as e:
            MessageDialog.error(self, "Lỗi", f"Không thể lọc dữ liệu:\n{str(e)}")
    
    def refresh_data(self):
        """Refresh data from outside"""
        self.load_data()


class KhachHangDetailView(QWidget):
    """
    Chi tiết Khách hàng
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_khach_hang = None
        self.setup_ui()
    
    def setup_ui(self):
        """Setup UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)
        
        # Title
        title = QLabel("📋 CHI TIẾT KHÁCH HÀNG")
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
        
        # Content placeholder
        placeholder = QLabel("Chọn một khách hàng để xem chi tiết")
        placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        placeholder.setStyleSheet("""
            QLabel {
                color: #757575;
                font-size: 16px;
                padding: 100px;
            }
        """)
        layout.addWidget(placeholder, 1)
    
    def set_khach_hang(self, khach_hang):
        """Set khách hàng to display"""
        self.current_khach_hang = khach_hang
        # TODO: Implement detail view


__all__ = ['KhachHangView', 'KhachHangDetailView']
