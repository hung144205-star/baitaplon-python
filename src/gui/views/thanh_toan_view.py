#!/usr/bin/env python3
"""
Thanh toán View - Giao diện Quản lý Thanh toán
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QComboBox, QMessageBox, QHeaderView, QStackedWidget
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from typing import Optional, Dict, Any

from src.gui.widgets import DataTableWithToolbar, SearchBox
from src.gui.dialogs import MessageDialog, ConfirmDialog
from src.utils.formatters import format_currency, format_date


class ThanhToanView(QWidget):
    """
    Giao diện Quản lý Thanh toán
    """
    
    # Signals
    thanh_toan_selected = pyqtSignal(object)
    thanh_toan_updated = pyqtSignal(object)
    thanh_toan_deleted = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_thanh_toan = None
        self.setup_ui()
        self.setup_connections()
        self.load_data()
    
    def setup_ui(self):
        """Setup UI"""
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
        layout.setSpacing(16)
        
        # Title
        title = QLabel("💰 QUẢN LÝ THANH TOÁN")
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
            headers=["Mã TT", "Hợp đồng", "Kỳ thanh toán", "Số tiền", "Ngày đến hạn", "Ngày thanh toán", "Trạng thái"]
        )
        
        self.table_with_toolbar.export_clicked.connect(self._on_export_clicked)
        
        layout.addWidget(self.table_with_toolbar, 1)
        
        # Summary cards
        summary_bar = self._create_summary_bar()
        layout.addWidget(summary_bar)
        
        # Info label
        self.info_label = QLabel("Chọn một thanh toán để xem chi tiết")
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
        self.search_box = SearchBox(placeholder="🔍 Tìm theo mã hợp đồng, khách hàng...")
        layout.addWidget(self.search_box, 1)
        
        # Filter by status
        layout.addWidget(QLabel("Trạng thái:"))
        self.filter_trang_thai = QComboBox()
        self.filter_trang_thai.addItem("Tất cả", "")
        self.filter_trang_thai.addItem("Đã thanh toán", "da_thanh_toan")
        self.filter_trang_thai.addItem("Chưa thanh toán", "chua_thanh_toan")
        self.filter_trang_thai.addItem("Quá hạn", "qua_han")
        self.filter_trang_thai.setFixedWidth(150)
        layout.addWidget(self.filter_trang_thai)
        
        return filter_bar
    
    def _create_summary_bar(self) -> QFrame:
        """Create summary statistics bar"""
        summary_bar = QFrame()
        summary_bar.setFrameShape(QFrame.Shape.StyledPanel)
        summary_bar.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border: 1px solid rgba(0, 0, 0, 0.1);
                border-radius: 8px;
                padding: 16px;
            }
        """)
        
        layout = QHBoxLayout(summary_bar)
        layout.setSpacing(24)
        
        # Tổng số hóa đơn
        self.total_count_label = QLabel("Tổng: 0 hóa đơn")
        self.total_count_label.setStyleSheet("font-weight: 600; color: #31302e;")
        layout.addWidget(self.total_count_label)
        
        layout.addStretch()
        
        # Tổng tiền đã thanh toán
        self.da_thanh_toan_label = QLabel("💵 Đã thanh toán: 0đ")
        self.da_thanh_toan_label.setStyleSheet("color: #2e7d32; font-weight: 600;")
        layout.addWidget(self.da_thanh_toan_label)
        
        # Tổng tiền chưa thanh toán
        self.chua_thanh_toan_label = QLabel("⏳ Còn nợ: 0đ")
        self.chua_thanh_toan_label.setStyleSheet("color: #d32f2f; font-weight: 600;")
        layout.addWidget(self.chua_thanh_toan_label)
        
        return summary_bar
    
    def setup_connections(self):
        """Setup signal connections"""
        self.table_with_toolbar.row_selected.connect(self._on_row_selected)
        self.table_with_toolbar.row_double_clicked.connect(self._on_row_double_clicked)
        
        self.table_with_toolbar.add_clicked.connect(self._on_add_clicked)
        self.table_with_toolbar.edit_clicked.connect(self._on_edit_clicked)
        self.table_with_toolbar.delete_clicked.connect(self._on_delete_clicked)
        self.table_with_toolbar.refresh_clicked.connect(self._on_refresh_clicked)
        
        self.search_box.search_changed.connect(self._on_search_changed)
        self.filter_trang_thai.currentIndexChanged.connect(self._apply_filters)
    
    def load_data(self):
        """Load data from database"""
        try:
            from src.services.thanh_toan_service import ThanhToanService
            from src.database import get_session
            from src.models import ThanhToan, HopDong, KhachHang, TrangThaiTTEnum
            
            service = ThanhToanService()
            session = get_session()
            
            # Get all payments with contract info
            payments = session.query(ThanhToan).all()
            
            # Convert to table data
            data = []
            tong_da_thanh_toan = 0
            tong_chua_thanh_toan = 0
            tong_qua_han = 0
            
            for p in payments:
                # Get contract info
                hop_dong = session.query(HopDong).filter(HopDong.ma_hop_dong == p.ma_hop_dong).first()
                if hop_dong:
                    khach_hang = session.query(KhachHang).filter(KhachHang.ma_khach_hang == hop_dong.ma_khach_hang).first()
                    khach_hang_name = khach_hang.ho_ten if khach_hang else "N/A"
                else:
                    khach_hang_name = "N/A"
                
                # Get status
                trang_thai = p.trang_thai.value if hasattr(p.trang_thai, 'value') else str(p.trang_thai)
                
                # Calculate totals
                if trang_thai == 'da_thanh_toan':
                    tong_da_thanh_toan += p.so_tien
                elif trang_thai == 'chua_thanh_toan':
                    tong_chua_thanh_toan += p.so_tien
                elif trang_thai == 'qua_han':
                    tong_qua_han += p.so_tien
                
                # Format dates
                ngay_den_han = format_date(p.ngay_den_han) if p.ngay_den_han else "-"
                ngay_thanh_toan = format_date(p.ngay_thanh_toan) if p.ngay_thanh_toan else "-"
                
                data.append({
                    "Mã TT": p.ma_thanh_toan,
                    "Hợp đồng": f"{p.ma_hop_dong} - {khach_hang_name}",
                    "Kỳ thanh toán": p.ky_thanh_toan or "-",
                    "Số tiền": format_currency(p.so_tien),
                    "Ngày đến hạn": ngay_den_han,
                    "Ngày thanh toán": ngay_thanh_toan,
                    "Trạng thái": self._get_trang_thai_label(trang_thai),
                    "__data": p
                })
            
            session.close()
            
            self.table_with_toolbar.set_data(data)
            
            # Update summary
            self.total_count_label.setText(f"Tổng: {len(data)} hóa đơn")
            self.da_thanh_toan_label.setText(f"💵 Đã thanh toán: {format_currency(tong_da_thanh_toan)}")
            self.chua_thanh_toan_label.setText(f"⏳ Còn nợ: {format_currency(tong_chua_thanh_toan + tong_qua_han)}")
            
            self.info_label.setText(f"Tổng: {len(data)} thanh toán")
            
        except Exception as e:
            MessageDialog.error(self, "Lỗi", f"Không thể tải dữ liệu:\n{str(e)}")
    
    def _get_trang_thai_label(self, trang_thai: str) -> str:
        """Get status label with emoji"""
        labels = {
            "da_thanh_toan": "✅ Đã thanh toán",
            "chua_thanh_toan": "⏳ Chưa thanh toán",
            "qua_han": "❌ Quá hạn",
        }
        return labels.get(trang_thai, trang_thai)
    
    def _on_row_selected(self, row_index: int, row_data: dict):
        """Handle row selection"""
        if "__data" in row_data:
            self.current_thanh_toan = row_data["__data"]
            self.thanh_toan_selected.emit(self.current_thanh_toan)
            self.info_label.setText(
                f"Đang xem: {self.current_thanh_toan.ma_thanh_toan} - {self.current_thanh_toan.ky_thanh_toan}"
            )
    
    def _on_row_double_clicked(self, row_index: int, row_data: dict):
        """Handle row double click"""
        if "__data" in row_data:
            self._on_edit_clicked()
    
    def _on_add_clicked(self):
        """Handle add button click"""
        try:
            from src.gui.forms import ThanhToanForm
            
            dialog = ThanhToanForm(self)
            dialog.accepted_with_data.connect(self._on_form_accepted)
            dialog.exec()
        except ImportError as e:
            MessageDialog.error(self, "Lỗi", f"Không thể mở form: {str(e)}")
        except Exception as e:
            MessageDialog.error(self, "Lỗi", f"Lỗi: {str(e)}")
    
    def _on_form_accepted(self, form_data: dict):
        """Handle form accepted with data"""
        try:
            from src.services.thanh_toan_service import ThanhToanService
            
            service = ThanhToanService()
            thanh_toan = service.create(form_data)
            self.load_data()
            self.thanh_toan_updated.emit(thanh_toan)
            MessageDialog.success(self, "Thành công", f"Đã thêm thanh toán {thanh_toan.ma_thanh_toan}")
        except Exception as e:
            MessageDialog.error(self, "Lỗi", f"Không thể lưu thanh toán: {str(e)}")
    
    def _on_edit_clicked(self):
        """Handle edit button click"""
        if not self.current_thanh_toan:
            MessageDialog.warning(self, "Cảnh báo", "Vui lòng chọn một thanh toán để sửa")
            return
        
        try:
            from src.gui.forms import ThanhToanForm
            
            ma_tt = self.current_thanh_toan.ma_thanh_toan
            dialog = ThanhToanForm(self, thanh_toan=self.current_thanh_toan)
            dialog.accepted_with_data.connect(lambda data: self._on_edit_accepted(data, ma_tt))
            dialog.exec()
        except ImportError as e:
            MessageDialog.error(self, "Lỗi", f"Không thể mở form: {str(e)}")
        except Exception as e:
            MessageDialog.error(self, "Lỗi", f"Lỗi: {str(e)}")
    
    def _on_edit_accepted(self, form_data: dict, ma_thanh_toan: str):
        """Handle edit form accepted with data"""
        try:
            from src.services.thanh_toan_service import ThanhToanService
            
            service = ThanhToanService()
            updated = service.update(ma_thanh_toan, form_data)
            self.load_data()
            if updated:
                self.thanh_toan_updated.emit(updated)
                MessageDialog.success(self, "Thành công", f"Đã cập nhật thanh toán {updated.ma_thanh_toan}")
        except Exception as e:
            MessageDialog.error(self, "Lỗi", f"Không thể cập nhật thanh toán: {str(e)}")
    
    def _on_delete_clicked(self):
        """Handle delete button click"""
        if not self.current_thanh_toan:
            MessageDialog.warning(self, "Cảnh báo", "Vui lòng chọn một thanh toán để xóa")
            return
        
        confirm = ConfirmDialog(
            self,
            "Xác nhận xóa",
            f"Bạn có chắc muốn xóa thanh toán {self.current_thanh_toan.ma_thanh_toan}?",
            "warning"
        )
        
        if confirm.exec():
            try:
                from src.services.thanh_toan_service import ThanhToanService
                
                service = ThanhToanService()
                service.delete(self.current_thanh_toan.ma_thanh_toan)
                self.thanh_toan_deleted.emit(self.current_thanh_toan.ma_thanh_toan)
                self.load_data()
                self.current_thanh_toan = None
                MessageDialog.success(self, "Thành công", "Đã xóa thanh toán")
            except Exception as e:
                MessageDialog.error(self, "Lỗi", f"Không thể xóa thanh toán: {str(e)}")
    
    def _on_refresh_clicked(self):
        """Handle refresh button click"""
        self.load_data()
    
    def _on_export_clicked(self):
        """Handle export button click"""
        try:
            from src.services.thanh_toan_service import ThanhToanService
            from src.utils.helpers import export_to_excel
            from datetime import datetime
            import os
            
            service = ThanhToanService()
            session = service.db
            from src.models import ThanhToan
            
            payments = session.query(ThanhToan).all()
            
            # Prepare data for export
            export_data = []
            for p in payments:
                export_data.append({
                    "Mã TT": p.ma_thanh_toan,
                    "Hợp đồng": p.ma_hop_dong,
                    "Kỳ thanh toán": p.ky_thanh_toan,
                    "Số tiền": p.so_tien,
                    "Ngày đến hạn": p.ngay_den_han,
                    "Ngày thanh toán": p.ngay_thanh_toan,
                    "Trạng thái": p.trang_thai.value if hasattr(p.trang_thai, 'value') else str(p.trang_thai),
                    "Ghi chú": p.ghi_chu or ""
                })
            
            # Create export directory
            export_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 'data', 'exports')
            os.makedirs(export_dir, exist_ok=True)
            
            # Export file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_path = os.path.join(export_dir, f'thanh_toan_{timestamp}.xlsx')
            
            export_to_excel(export_data, file_path)
            MessageDialog.success(self, "Thành công", f"Đã xuất file: {file_path}")
            
        except Exception as e:
            MessageDialog.error(self, "Lỗi", f"Không thể xuất file: {str(e)}")
    
    def _on_search_changed(self, text: str):
        """Handle search"""
        if not text.strip():
            self.load_data()
        else:
            try:
                from src.services.thanh_toan_service import ThanhToanService
                from src.database import get_session
                from src.models import ThanhToan, HopDong, KhachHang
                
                service = ThanhToanService()
                session = get_session()
                
                # Search by contract ID or customer name
                search_pattern = f"%{text}%"
                
                # Find matching contracts
                hop_dongs = session.query(HopDong).filter(
                    HopDong.ma_hop_dong.ilike(search_pattern)
                ).all()
                
                ma_hop_dongs = [hd.ma_hop_dong for hd in hop_dongs]
                
                # Find matching customers
                khach_hangs = session.query(KhachHang).filter(
                    KhachHang.ho_ten.ilike(search_pattern)
                ).all()
                
                ma_khach_hangs = [kh.ma_khach_hang for kh in khach_hangs]
                
                # Get contracts by customer
                hop_dongs_by_customer = session.query(HopDong).filter(
                    HopDong.ma_khach_hang.in_(ma_khach_hangs)
                ).all()
                
                for hd in hop_dongs_by_customer:
                    if hd.ma_hop_dong not in ma_hop_dongs:
                        ma_hop_dongs.append(hd.ma_hop_dong)
                
                # Get payments
                payments = session.query(ThanhToan).filter(
                    ThanhToan.ma_hop_dong.in_(ma_hop_dongs) if ma_hop_dongs else False
                ).all()
                
                # Convert to table data
                data = []
                for p in payments:
                    hop_dong = session.query(HopDong).filter(HopDong.ma_hop_dong == p.ma_hop_dong).first()
                    khach_hang = session.query(KhachHang).filter(KhachHang.ma_khach_hang == hop_dong.ma_khach_hang).first() if hop_dong else None
                    khach_hang_name = khach_hang.ho_ten if khach_hang else "N/A"
                    
                    trang_thai = p.trang_thai.value if hasattr(p.trang_thai, 'value') else str(p.trang_thai)
                    
                    data.append({
                        "Mã TT": p.ma_thanh_toan,
                        "Hợp đồng": f"{p.ma_hop_dong} - {khach_hang_name}",
                        "Kỳ thanh toán": p.ky_thanh_toan or "-",
                        "Số tiền": format_currency(p.so_tien),
                        "Ngày đến hạn": format_date(p.ngay_den_han) if p.ngay_den_han else "-",
                        "Ngày thanh toán": format_date(p.ngay_thanh_toan) if p.ngay_thanh_toan else "-",
                        "Trạng thái": self._get_trang_thai_label(trang_thai),
                        "__data": p
                    })
                
                session.close()
                
                self.table_with_toolbar.set_data(data)
                self.info_label.setText(f"Tìm thấy: {len(data)} thanh toán")
                
            except Exception as e:
                MessageDialog.error(self, "Lỗi", f"Không thể tìm kiếm:\n{str(e)}")
    
    def _apply_filters(self):
        """Apply filters"""
        try:
            trang_thai = self.filter_trang_thai.currentData()
            
            from src.services.thanh_toan_service import ThanhToanService
            from src.database import get_session
            from src.models import ThanhToan, HopDong, KhachHang
            
            service = ThanhToanService()
            session = get_session()
            
            query = session.query(ThanhToan)
            
            if trang_thai:
                query = query.filter(ThanhToan.trang_thai == trang_thai)
            
            payments = query.all()
            
            # Convert to table data
            data = []
            for p in payments:
                hop_dong = session.query(HopDong).filter(HopDong.ma_hop_dong == p.ma_hop_dong).first()
                khach_hang = session.query(KhachHang).filter(KhachHang.ma_khach_hang == hop_dong.ma_khach_hang).first() if hop_dong else None
                khach_hang_name = khach_hang.ho_ten if khach_hang else "N/A"
                
                trang_thai_val = p.trang_thai.value if hasattr(p.trang_thai, 'value') else str(p.trang_thai)
                
                data.append({
                    "Mã TT": p.ma_thanh_toan,
                    "Hợp đồng": f"{p.ma_hop_dong} - {khach_hang_name}",
                    "Kỳ thanh toán": p.ky_thanh_toan or "-",
                    "Số tiền": format_currency(p.so_tien),
                    "Ngày đến hạn": format_date(p.ngay_den_han) if p.ngay_den_han else "-",
                    "Ngày thanh toán": format_date(p.ngay_thanh_toan) if p.ngay_thanh_toan else "-",
                    "Trạng thái": self._get_trang_thai_label(trang_thai_val),
                    "__data": p
                })
            
            session.close()
            
            self.table_with_toolbar.set_data(data)
            self.info_label.setText(f"Tổng: {len(data)} thanh toán")
            
        except Exception as e:
            MessageDialog.error(self, "Lỗi", f"Không thể lọc dữ liệu:\n{str(e)}")
    
    def refresh_data(self):
        """Refresh data from outside"""
        self.load_data()


__all__ = ['ThanhToanView']
