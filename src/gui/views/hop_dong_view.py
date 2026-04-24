#!/usr/bin/env python3
"""
Hợp đồng View - Giao diện Quản lý Hợp đồng
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QComboBox, QDateEdit, QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSignal, QDate
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

from src.services import HopDongService, KhachHangService, ViTriService
from src.models import HopDong, TrangThaiHDEnum
from src.gui.widgets import DataTableWithToolbar, SearchBox
from src.gui.dialogs import MessageDialog, ConfirmDialog
from src.utils.formatters import format_currency, format_number
from src.gui.forms import HopDongForm


class HopDongView(QWidget):
    """
    Giao diện Quản lý Hợp đồng
    """
    
    # Signals
    hop_dong_selected = pyqtSignal(object)  # HopDong object
    hop_dong_added = pyqtSignal(object)  # HopDong object
    hop_dong_updated = pyqtSignal(object)  # HopDong object
    hop_dong_deleted = pyqtSignal(str)  # ma_hop_dong
    hop_dong_renewed = pyqtSignal(object)  # HopDong object
    hop_dong_terminated = pyqtSignal(str)  # ma_hop_dong
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.service = HopDongService()
        self.khach_hang_service = KhachHangService()
        self.vi_tri_service = ViTriService()
        self.current_hop_dong: Optional[HopDong] = None
        self.setup_ui()
        self.setup_connections()
        self.load_data()
    
    def setup_ui(self):
        """Setup UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)
        
        # Title
        title = QLabel("📋 QUẢN LÝ HỢP ĐỒNG")
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
            headers=["Mã HĐ", "Khách Hàng", "Vị Trí", "Ngày BĐ", "Ngày KT", "Giá Thuê", "Còn Lại", "Trạng Thái"]
        )
        layout.addWidget(self.table_with_toolbar, 1)
        
        # Info label
        self.info_label = QLabel("Tổng: 0 hợp đồng")
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
        
        # Total contracts
        layout.addWidget(QLabel("Tổng:"))
        self.stat_tong = QLabel("0")
        self.stat_tong.setStyleSheet("font-size: 24px; font-weight: 700; color: #1976d2;")
        layout.addWidget(self.stat_tong)
        
        layout.addSpacing(20)
        
        # Active contracts
        layout.addWidget(QLabel("Hiệu lực:"))
        self.stat_hieu_luc = QLabel("0")
        self.stat_hieu_luc.setStyleSheet("font-size: 24px; font-weight: 700; color: #1aae39;")
        layout.addWidget(self.stat_hieu_luc)
        
        layout.addSpacing(20)
        
        # Expiring soon
        layout.addWidget(QLabel("Sắp hết hạn:"))
        self.stat_sap_het_han = QLabel("0")
        self.stat_sap_het_han.setStyleSheet("font-size: 24px; font-weight: 700; color: #ff9800;")
        layout.addWidget(self.stat_sap_het_han)
        
        layout.addSpacing(20)
        
        # Expired
        layout.addWidget(QLabel("Hết hạn:"))
        self.stat_het_han = QLabel("0")
        self.stat_het_han.setStyleSheet("font-size: 24px; font-weight: 700; color: #f44336;")
        layout.addWidget(self.stat_het_han)
        
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
        self.search_box = SearchBox(placeholder="🔍 Tìm theo mã, khách hàng, vị trí...")
        layout.addWidget(self.search_box, 1)
        
        # Filter by status
        layout.addWidget(QLabel("Trạng thái:"))
        self.filter_trang_thai = QComboBox()
        self.filter_trang_thai.addItem("Tất cả", "")
        self.filter_trang_thai.addItem("✅ Hiệu lực", "hieu_luc")
        self.filter_trang_thai.addItem("⏰ Hết hạn", "het_han")
        self.filter_trang_thai.addItem("❌ Chấm dứt", "cham_dut")
        self.filter_trang_thai.addItem("🔄 Gia hạn", "gia_han")
        self.filter_trang_thai.setFixedWidth(180)
        layout.addWidget(self.filter_trang_thai)
        
        # Date range filter
        layout.addWidget(QLabel("Từ ngày:"))
        self.filter_tu_ngay = QDateEdit()
        self.filter_tu_ngay.setCalendarPopup(True)
        self.filter_tu_ngay.setDate(QDate.currentDate().addMonths(-1))
        self.filter_tu_ngay.setFixedWidth(120)
        layout.addWidget(self.filter_tu_ngay)
        
        layout.addWidget(QLabel("Đến ngày:"))
        self.filter_den_ngay = QDateEdit()
        self.filter_den_ngay.setCalendarPopup(True)
        self.filter_den_ngay.setDate(QDate.currentDate().addMonths(1))
        self.filter_den_ngay.setFixedWidth(120)
        layout.addWidget(self.filter_den_ngay)
        
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
        
        # Custom buttons
        self._connect_custom_buttons()
        
        # Search & filter
        self.search_box.search_changed.connect(self._on_search_changed)
        self.filter_trang_thai.currentIndexChanged.connect(self._apply_filters)
        self.filter_tu_ngay.dateChanged.connect(self._apply_filters)
        self.filter_den_ngay.dateChanged.connect(self._apply_filters)
    
    def _connect_custom_buttons(self):
        """Connect custom buttons (renew, terminate)"""
        # Note: Renew and Terminate buttons should be added to the toolbar in DataTableWithToolbar
        # For now, just document that these features need the buttons to be added to the widget
        # This is a limitation - DataTableWithToolbar should support custom action buttons
        pass
    
    def load_data(self):
        """Load data from database"""
        try:
            hop_dongs = self.service.get_all(limit=1000)
            
            # Convert to table data
            data = []
            today = datetime.now().date()
            
            for hd in hop_dongs:
                # Calculate remaining days
                remaining_days = (hd.ngay_ket_thuc - today).days
                
                # Get customer name
                try:
                    khach_hang = self.khach_hang_service.get_by_id(hd.ma_khach_hang)
                    ten_khach_hang = khach_hang.ho_ten if khach_hang else hd.ma_khach_hang
                except:
                    ten_khach_hang = hd.ma_khach_hang
                
                # Get location info
                try:
                    vi_tri = self.vi_tri_service.get_by_id(hd.ma_vi_tri)
                    vi_tri_info = f"{vi_tri.khu_vuc}-{vi_tri.hang}-{vi_tri.tang}" if vi_tri else hd.ma_vi_tri
                except:
                    vi_tri_info = hd.ma_vi_tri
                
                data.append({
                    "Mã HĐ": hd.ma_hop_dong,
                    "Khách Hàng": ten_khach_hang,
                    "Vị Trí": vi_tri_info,
                    "Ngày BĐ": hd.ngay_bat_dau.strftime("%d/%m/%Y"),
                    "Ngày KT": hd.ngay_ket_thuc.strftime("%d/%m/%Y"),
                    "Giá Thuê": format_currency(hd.gia_thue),
                    "Còn Lại": self._format_remaining_days(remaining_days),
                    "Trạng Thái": self._get_trang_thai_label(hd.trang_thai),
                    "__data": hd,
                    "_remaining_days": remaining_days,
                    "_expiring_soon": 0 < remaining_days <= 30
                })
            
            self.table_with_toolbar.set_data(data)
            
            # Update statistics
            self._update_statistics(hop_dongs, today)
            
            # Update info
            self.info_label.setText(f"Tổng: {len(data)} hợp đồng")
            
        except Exception as e:
            MessageDialog.error(self, "Lỗi", f"Không thể tải dữ liệu:\n{str(e)}")
    
    def _format_remaining_days(self, days: int) -> str:
        """Format remaining days with color"""
        if days < 0:
            return f"Quá hạn {-days} ngày"
        elif days == 0:
            return "Hôm nay"
        elif days <= 7:
            return f"⚠️ {days} ngày"
        elif days <= 30:
            return f"{days} ngày"
        else:
            return f"{days} ngày"
    
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
    
    def _update_statistics(self, hop_dongs: list, today):
        """Update statistics bar"""
        tong = len(hop_dongs)
        hieu_luc = sum(1 for h in hop_dongs if str(h.trang_thai) == 'hieu_luc')
        sap_het_han = sum(1 for h in hop_dongs if str(h.trang_thai) == 'hieu_luc' and 0 < (h.ngay_ket_thuc - today).days <= 30)
        het_han = sum(1 for h in hop_dongs if str(h.trang_thai) == 'het_han')
        
        self.stat_tong.setText(str(tong))
        self.stat_hieu_luc.setText(str(hieu_luc))
        self.stat_sap_het_han.setText(str(sap_het_han))
        self.stat_het_han.setText(str(het_han))
    
    def _on_row_selected(self, row_index: int, row_data: dict):
        """Handle row selection"""
        if "_data" in row_data:
            self.current_hop_dong = row_data["_data"]
            self.hop_dong_selected.emit(self.current_hop_dong)
            self.info_label.setText(
                f"Đang xem: {self.current_hop_dong.ma_hop_dong} - {self._get_trang_thai_label(self.current_hop_dong.trang_thai)}"
            )
    
    def _on_row_double_clicked(self, row_index: int, row_data: dict):
        """Handle row double click"""
        if "_data" in row_data:
            self._on_edit_clicked()
    
    def _on_add_clicked(self):
        """Handle add button click"""
        dialog = HopDongForm(self)
        dialog.hop_dong_saved.connect(self._on_hop_dong_saved)
        dialog.exec()
    
    def _on_hop_dong_saved(self, hop_dong: HopDong):
        """Handle hop_dong saved from form"""
        self.load_data()  # Refresh table
        self.hop_dong_added.emit(hop_dong)
    
    def _on_edit_clicked(self):
        """Handle edit button click"""
        if not self.current_hop_dong:
            MessageDialog.warning(self, "Cảnh báo", "Vui lòng chọn một hợp đồng để sửa")
            return
        
        dialog = HopDongForm(self, hop_dong=self.current_hop_dong)
        dialog.hop_dong_saved.connect(self._on_hop_dong_saved)
        dialog.exec()
    
    def _on_delete_clicked(self):
        """Handle delete button click"""
        if not self.current_hop_dong:
            MessageDialog.warning(self, "Cảnh báo", "Vui lòng chọn một hợp đồng để xóa")
            return
        
        # Confirm delete
        confirmed = ConfirmDialog.ask_delete(
            self, 
            f"Hợp đồng {self.current_hop_dong.ma_hop_dong}"
        )
        
        if confirmed:
            try:
                success = self.service.delete(self.current_hop_dong.ma_hop_dong)
                if success:
                    MessageDialog.success(self, "Thành công", "Đã xóa hợp đồng thành công")
                    self.hop_dong_deleted.emit(self.current_hop_dong.ma_hop_dong)
                    self.load_data()
                    self.current_hop_dong = None
                else:
                    MessageDialog.error(self, "Lỗi", "Không thể xóa hợp đồng")
            except ValueError as e:
                MessageDialog.error(self, "Không thể xóa", str(e))
            except Exception as e:
                MessageDialog.error(self, "Lỗi", f"Không thể xóa hợp đồng:\n{str(e)}")
    
    def _on_refresh_clicked(self):
        """Handle refresh button click"""
        self.load_data()
    
    def _on_renew_clicked(self):
        """Handle renew button click"""
        if not self.current_hop_dong:
            MessageDialog.warning(self, "Cảnh báo", "Vui lòng chọn một hợp đồng để gia hạn")
            return
        
        # Check if eligible for renewal
        if str(self.current_hop_dong.trang_thai) not in ['hieu_luc', 'het_han']:
            MessageDialog.warning(self, "Cảnh báo", "Hợp đồng không thể gia hạn")
            return
        
        self.hop_dong_renewed.emit(self.current_hop_dong)
    
    def _on_terminate_clicked(self):
        """Handle terminate button click"""
        if not self.current_hop_dong:
            MessageDialog.warning(self, "Cảnh báo", "Vui lòng chọn một hợp đồng để chấm dứt")
            return
        
        # Confirm terminate
        confirmed = ConfirmDialog.ask(
            self,
            "Xác nhận chấm dứt",
            f"Bạn có chắc chắn muốn chấm dứt hợp đồng {self.current_hop_dong.ma_hop_dong}?",
            "❌ Chấm dứt",
            "⏹️ Hủy"
        )
        
        if confirmed:
            # Ask for reason
            from PyQt6.QtWidgets import QInputDialog
            reason, ok = QInputDialog.getText(
                self,
                "Lý do chấm dứt",
                "Vui lòng nhập lý do chấm dứt:"
            )
            
            if ok and reason:
                try:
                    success = self.service.terminate(self.current_hop_dong.ma_hop_dong, reason)
                    if success:
                        MessageDialog.success(self, "Thành công", "Đã chấm dứt hợp đồng")
                        self.hop_dong_terminated.emit(self.current_hop_dong.ma_hop_dong)
                        self.load_data()
                        self.current_hop_dong = None
                    else:
                        MessageDialog.error(self, "Lỗi", "Không thể chấm dứt hợp đồng")
                except Exception as e:
                    MessageDialog.error(self, "Lỗi", f"Không thể chấm dứt hợp đồng:\n{str(e)}")
    
    def _on_search_changed(self, text: str):
        """Handle search"""
        if not text.strip():
            self.load_data()
        else:
            try:
                hop_dongs = self.service.search(text.strip(), limit=100)
                
                # Convert to table data
                data = []
                today = datetime.now().date()
                
                for hd in hop_dongs:
                    remaining_days = (hd.ngay_ket_thuc - today).days
                    
                    try:
                        khach_hang = self.khach_hang_service.get_by_id(hd.ma_khach_hang)
                        ten_khach_hang = khach_hang.ho_ten if khach_hang else hd.ma_khach_hang
                    except:
                        ten_khach_hang = hd.ma_khach_hang
                    
                    try:
                        vi_tri = self.vi_tri_service.get_by_id(hd.ma_vi_tri)
                        vi_tri_info = f"{vi_tri.khu_vuc}-{vi_tri.hang}-{vi_tri.tang}" if vi_tri else hd.ma_vi_tri
                    except:
                        vi_tri_info = hd.ma_vi_tri
                    
                    data.append({
                        "Mã HĐ": hd.ma_hop_dong,
                        "Khách Hàng": ten_khach_hang,
                        "Vị Trí": vi_tri_info,
                        "Ngày BĐ": hd.ngay_bat_dau.strftime("%d/%m/%Y"),
                        "Ngày KT": hd.ngay_ket_thuc.strftime("%d/%m/%Y"),
                        "Giá Thuê": format_currency(hd.gia_thue),
                        "Còn Lại": self._format_remaining_days(remaining_days),
                        "Trạng Thái": self._get_trang_thai_label(hd.trang_thai),
                        "__data": hd,
                        "_remaining_days": remaining_days,
                        "_expiring_soon": 0 < remaining_days <= 30
                    })
                
                self.table_with_toolbar.set_data(data)
                self.info_label.setText(f"Tìm thấy: {len(data)} hợp đồng")
                
            except Exception as e:
                MessageDialog.error(self, "Lỗi", f"Không thể tìm kiếm:\n{str(e)}")
    
    def _apply_filters(self):
        """Apply filters"""
        try:
            trang_thai = self.filter_trang_thai.currentData()
            tu_ngay = self.filter_tu_ngay.date().toPyDate()
            den_ngay = self.filter_den_ngay.date().toPyDate()
            
            hop_dongs = self.service.get_all(limit=1000)
            
            # Filter by status
            if trang_thai:
                hop_dongs = [h for h in hop_dongs if str(h.trang_thai) == trang_thai]
            
            # Filter by date range
            hop_dongs = [h for h in hop_dongs if tu_ngay <= h.ngay_ket_thuc <= den_ngay]
            
            # Convert to table data
            data = []
            today = datetime.now().date()
            
            for hd in hop_dongs:
                remaining_days = (hd.ngay_ket_thuc - today).days
                
                try:
                    khach_hang = self.khach_hang_service.get_by_id(hd.ma_khach_hang)
                    ten_khach_hang = khach_hang.ho_ten if khach_hang else hd.ma_khach_hang
                except:
                    ten_khach_hang = hd.ma_khach_hang
                
                try:
                    vi_tri = self.vi_tri_service.get_by_id(hd.ma_vi_tri)
                    vi_tri_info = f"{vi_tri.khu_vuc}-{vi_tri.hang}-{vi_tri.tang}" if vi_tri else hd.ma_vi_tri
                except:
                    vi_tri_info = hd.ma_vi_tri
                
                data.append({
                    "Mã HĐ": hd.ma_hop_dong,
                    "Khách Hàng": ten_khach_hang,
                    "Vị Trí": vi_tri_info,
                    "Ngày BĐ": hd.ngay_bat_dau.strftime("%d/%m/%Y"),
                    "Ngày KT": hd.ngay_ket_thuc.strftime("%d/%m/%Y"),
                    "Giá Thuê": format_currency(hd.gia_thue),
                    "Còn Lại": self._format_remaining_days(remaining_days),
                    "Trạng Thái": self._get_trang_thai_label(hd.trang_thai),
                    "__data": hd,
                    "_remaining_days": remaining_days,
                    "_expiring_soon": 0 < remaining_days <= 30
                })
            
            self.table_with_toolbar.set_data(data)
            self._update_statistics(data, today)
            self.info_label.setText(f"Tổng: {len(data)} hợp đồng")
            
        except Exception as e:
            MessageDialog.error(self, "Lỗi", f"Không thể lọc dữ liệu:\n{str(e)}")
    
    def refresh_data(self):
        """Refresh data from outside"""
        self.load_data()


__all__ = ['HopDongView']
