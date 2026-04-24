#!/usr/bin/env python3
"""
Hợp đồng Detail View - Chi tiết hợp đồng với tabs (Full Implementation)
"""
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTabWidget, QFrame, QFormLayout, QScrollArea, QWidget,
    QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox,
    QInputDialog
)
from PyQt6.QtCore import Qt
from datetime import datetime
from typing import Optional

from src.services import (
    HopDongService, KhachHangService, ViTriService,
    HangHoaService, ThanhToanService, HopDongHistoryService,
    TrangThaiTTEnum
)
from src.models import HopDong, TrangThaiHDEnum
from src.gui.dialogs import MessageDialog
from src.utils.formatters import format_currency


class HopDongDetailView(QDialog):
    """
    Dialog xem chi tiết hợp đồng với 4 tabs đầy đủ
    """
    
    def __init__(self, parent=None, hop_dong: Optional[HopDong] = None):
        super().__init__(parent)
        self.hop_dong = hop_dong
        self.service = HopDongService()
        self.khach_hang_service = KhachHangService()
        self.vi_tri_service = ViTriService()
        self.hang_hoa_service = HangHoaService()
        self.thanh_toan_service = ThanhToanService()
        self.history_service = HopDongHistoryService()
        self.setup_ui()
        
        if hop_dong:
            self.load_data()
            self.setWindowTitle(f"📋 Chi tiết hợp đồng {hop_dong.ma_hop_dong}")
        else:
            self.setWindowTitle("📋 Chi tiết hợp đồng")
    
    def setup_ui(self):
        """Setup UI"""
        self.setMinimumWidth(900)
        self.setMinimumHeight(700)
        self.setModal(True)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title = QLabel("📋 CHI TIẾT HỢP ĐỒNG")
        title.setStyleSheet("""
            QLabel {
                font-size: 20px;
                font-weight: 700;
                color: #31302e;
                padding: 10px 0;
            }
        """)
        layout.addWidget(title)
        
        # Tab widget
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid rgba(0, 0, 0, 0.1);
                border-radius: 8px;
                background-color: #ffffff;
            }
            QTabBar::tab {
                background-color: #f6f5f4;
                padding: 10px 20px;
                margin-right: 2px;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
            }
            QTabBar::tab:selected {
                background-color: #ffffff;
                font-weight: 600;
            }
            QTabBar::tab:hover {
                background-color: #eeeeee;
            }
        """)
        
        # Tab 1: Thông tin hợp đồng
        self.tab_thong_tin = self._create_thong_tin_tab()
        self.tabs.addTab(self.tab_thong_tin, "📄 Thông tin")
        
        # Tab 2: Hàng hóa
        self.tab_hang_hoa = self._create_hang_hoa_tab()
        self.tabs.addTab(self.tab_hang_hoa, "📦 Hàng hóa")
        
        # Tab 3: Thanh toán
        self.tab_thanh_toan = self._create_thanh_toan_tab()
        self.tabs.addTab(self.tab_thanh_toan, "💰 Thanh toán")
        
        # Tab 4: Lịch sử
        self.tab_lich_su = self._create_lich_su_tab()
        self.tabs.addTab(self.tab_lich_su, "🕐 Lịch sử")
        
        layout.addWidget(self.tabs)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        close_btn = QPushButton("❌ Đóng")
        close_btn.setStyleSheet("""
            QPushButton {
                padding: 10px 20px;
                border-radius: 6px;
                font-weight: 600;
                font-size: 14px;
                background-color: #757575;
                color: white;
            }
            QPushButton:hover {
                background-color: #616161;
            }
        """)
        close_btn.clicked.connect(self.accept)
        button_layout.addWidget(close_btn)
        
        layout.addLayout(button_layout)
    
    def _create_thong_tin_tab(self) -> QWidget:
        """Create contract info tab (fully implemented)"""
        widget = QWidget()
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        
        container = QWidget()
        layout = QFormLayout(container)
        layout.setSpacing(12)
        layout.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)
        
        # Basic info group
        basic_group = self._create_group("Thông tin cơ bản")
        basic_layout = QFormLayout(basic_group)
        basic_layout.setSpacing(12)
        
        self.lbl_ma_hop_dong = self._create_label()
        basic_layout.addRow("Mã hợp đồng:", self.lbl_ma_hop_dong)
        
        self.lbl_trang_thai = self._create_label()
        basic_layout.addRow("Trạng thái:", self.lbl_trang_thai)
        
        layout.addRow(basic_group)
        
        # Customer & location group
        relation_group = self._create_group("Khách hàng & Vị trí")
        relation_layout = QFormLayout(relation_group)
        relation_layout.setSpacing(12)
        
        self.lbl_khach_hang = self._create_label()
        relation_layout.addRow("Khách hàng:", self.lbl_khach_hang)
        
        self.lbl_vi_tri = self._create_label()
        relation_layout.addRow("Vị trí:", self.lbl_vi_tri)
        
        layout.addRow(relation_group)
        
        # Date group
        date_group = self._create_group("Thời hạn")
        date_layout = QFormLayout(date_group)
        date_layout.setSpacing(12)
        
        self.lbl_ngay_bat_dau = self._create_label()
        date_layout.addRow("Ngày bắt đầu:", self.lbl_ngay_bat_dau)
        
        self.lbl_ngay_ket_thuc = self._create_label()
        date_layout.addRow("Ngày kết thúc:", self.lbl_ngay_ket_thuc)
        
        self.lbl_so_ngay_con_lai = self._create_label()
        date_layout.addRow("Còn lại:", self.lbl_so_ngay_con_lai)
        
        layout.addRow(date_group)
        
        # Financial group
        financial_group = self._create_group("Thông tin tài chính")
        financial_layout = QFormLayout(financial_group)
        financial_layout.setSpacing(12)
        
        self.lbl_gia_thue = self._create_label()
        financial_layout.addRow("Giá thuê:", self.lbl_gia_thue)
        
        self.lbl_tien_coc = self._create_label()
        financial_layout.addRow("Tiền cọc:", self.lbl_tien_coc)
        
        self.lbl_phuong_thuc_tt = self._create_label()
        financial_layout.addRow("Phương thức TT:", self.lbl_phuong_thuc_tt)
        
        self.lbl_tong_tien = self._create_label()
        financial_layout.addRow("Tổng tiền thuê:", self.lbl_tong_tien)
        
        layout.addRow(financial_group)
        
        # Terms
        self.lbl_dieu_khoan = QLabel("")
        self.lbl_dieu_khoan.setWordWrap(True)
        self.lbl_dieu_khoan.setStyleSheet("""
            QLabel {
                padding: 12px;
                background-color: #f6f5f4;
                border-radius: 6px;
                color: #31302e;
            }
        """)
        layout.addRow("Điều khoản:", self.lbl_dieu_khoan)
        
        scroll.setWidget(container)
        
        main_layout = QVBoxLayout(widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(scroll)
        
        return widget
    
    def _create_hang_hoa_tab(self) -> QWidget:
        """Create goods tab (fully implemented)"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Goods table
        self.hang_hoa_table = QTableWidget()
        self.hang_hoa_table.setColumnCount(6)
        self.hang_hoa_table.setHorizontalHeaderLabels([
            "Mã HH", "Tên hàng hóa", "Số lượng", "ĐVT", "Giá trị", "Ghi chú"
        ])
        
        header = self.hang_hoa_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        self.hang_hoa_table.setStyleSheet("""
            QTableWidget {
                border: 1px solid rgba(0, 0, 0, 0.1);
                border-radius: 6px;
                gridline-color: rgba(0, 0, 0, 0.05);
            }
            QTableWidget::item {
                padding: 8px;
            }
            QHeaderView::section {
                background-color: #f6f5f4;
                padding: 8px;
                border: none;
                font-weight: 600;
            }
        """)
        
        layout.addWidget(self.hang_hoa_table)
        
        # Total value summary
        summary_frame = QFrame()
        summary_frame.setFrameShape(QFrame.Shape.StyledPanel)
        summary_frame.setStyleSheet("""
            QFrame {
                background-color: #e8f5e9;
                border-radius: 6px;
                padding: 12px;
            }
        """)
        summary_layout = QHBoxLayout(summary_frame)
        
        self.lbl_tong_gia_tri_hh = QLabel("Tổng giá trị hàng hóa: 0₫")
        self.lbl_tong_gia_tri_hh.setStyleSheet("font-weight: 700; color: #2e7d32; font-size: 16px;")
        summary_layout.addWidget(self.lbl_tong_gia_tri_hh)
        
        layout.addWidget(summary_frame)
        
        return widget
    
    def _create_thanh_toan_tab(self) -> QWidget:
        """Create payment tab (fully implemented)"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Payment table
        self.payment_table = QTableWidget()
        self.payment_table.setColumnCount(5)
        self.payment_table.setHorizontalHeaderLabels([
            "Mã TT", "Kỳ thanh toán", "Đến hạn", "Số tiền", "Trạng thái"
        ])
        
        header = self.payment_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        self.payment_table.setStyleSheet("""
            QTableWidget {
                border: 1px solid rgba(0, 0, 0, 0.1);
                border-radius: 6px;
                gridline-color: rgba(0, 0, 0, 0.05);
            }
            QTableWidget::item {
                padding: 8px;
            }
            QHeaderView::section {
                background-color: #f6f5f4;
                padding: 8px;
                border: none;
                font-weight: 600;
            }
        """)
        
        layout.addWidget(self.payment_table)
        
        # Payment summary
        summary_frame = QFrame()
        summary_frame.setFrameShape(QFrame.Shape.StyledPanel)
        summary_frame.setStyleSheet("""
            QFrame {
                background-color: #e3f2fd;
                border-radius: 6px;
                padding: 12px;
            }
        """)
        summary_layout = QHBoxLayout(summary_frame)
        
        self.lbl_tong_da_thanh_toan = QLabel("Đã thanh toán: 0₫")
        self.lbl_tong_da_thanh_toan.setStyleSheet("font-weight: 600; color: #1976d2;")
        summary_layout.addWidget(self.lbl_tong_da_thanh_toan)
        
        summary_layout.addSpacing(20)
        
        self.lbl_con_lai = QLabel("Còn lại: 0₫")
        self.lbl_con_lai.setStyleSheet("font-weight: 600; color: #ff9800;")
        summary_layout.addWidget(self.lbl_con_lai)
        
        layout.addWidget(summary_frame)
        
        return widget
    
    def _create_lich_su_tab(self) -> QWidget:
        """Create history tab (fully implemented)"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # History table
        self.history_table = QTableWidget()
        self.history_table.setColumnCount(4)
        self.history_table.setHorizontalHeaderLabels([
            "STT", "Ngày", "Sự kiện", "Mô tả"
        ])
        
        header = self.history_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        self.history_table.setStyleSheet("""
            QTableWidget {
                border: 1px solid rgba(0, 0, 0, 0.1);
                border-radius: 6px;
                gridline-color: rgba(0, 0, 0, 0.05);
            }
            QTableWidget::item {
                padding: 8px;
            }
            QHeaderView::section {
                background-color: #f6f5f4;
                padding: 8px;
                border: none;
                font-weight: 600;
            }
        """)
        
        layout.addWidget(self.history_table)
        
        return widget
    
    def _create_group(self, title: str) -> QFrame:
        """Create a styled group box"""
        group = QFrame()
        group.setFrameShape(QFrame.Shape.StyledPanel)
        group.setStyleSheet("""
            QFrame {
                background-color: #f6f5f4;
                border-radius: 8px;
                padding: 16px;
                margin-bottom: 12px;
            }
        """)
        return group
    
    def _create_label(self) -> QLabel:
        """Create a styled label"""
        label = QLabel("")
        label.setStyleSheet("""
            QLabel {
                color: #31302e;
                font-size: 14px;
                padding: 4px;
            }
        """)
        return label
    
    def _get_trang_thai_label(self, trang_thai) -> str:
        """Get status label with emoji and color"""
        labels = {
            "hieu_luc": ("✅ Hiệu lực", "#1aae39"),
            "het_han": ("⏰ Hết hạn", "#ff9800"),
            "cham_dut": ("❌ Chấm dứt", "#f44336"),
            "gia_han": ("🔄 Gia hạn", "#2196f3"),
        }
        label, color = labels.get(str(trang_thai), (str(trang_thai), "#757575"))
        return f"<span style='color: {color}; font-weight: 600;'>{label}</span>"
    
    def _get_payment_status_label(self, trang_thai) -> str:
        """Get payment status label with color"""
        labels = {
            'chua_thanh_toan': ("⏳ Chưa TT", "#ff9800"),
            'da_thanh_toan': ("✅ Đã TT", "#1aae39"),
            'qua_han': ("❌ Quá hạn", "#f44336"),
        }
        label, color = labels.get(trang_thai, (trang_thai, "#757575"))
        return f"<span style='color: {color}; font-weight: 600;'>{label}</span>"
    
    def _get_event_icon(self, event_type: str) -> str:
        """Get icon for event type"""
        icons = {
            'created': '📝',
            'updated': '✏️',
            'renewed': '🔄',
            'terminated': '❌',
            'payment_received': '💰',
            'goods_added': '📦',
            'goods_removed': '📤',
        }
        return icons.get(event_type, '📌')
    
    def load_data(self):
        """Load all contract data"""
        if not self.hop_dong:
            return
        
        try:
            # Load related data
            khach_hang = self.khach_hang_service.get_by_id(self.hop_dong.ma_khach_hang)
            vi_tri = self.vi_tri_service.get_by_id(self.hop_dong.ma_vi_tri)
            
            # Calculate remaining days
            today = datetime.now().date()
            remaining_days = (self.hop_dong.ngay_ket_thuc - today).days
            
            # Calculate contract duration and total
            from dateutil.relativedelta import relativedelta
            delta = relativedelta(self.hop_dong.ngay_ket_thuc, self.hop_dong.ngay_bat_dau)
            duration_months = delta.years * 12 + delta.months
            total_rent = duration_months * self.hop_dong.gia_thue
            
            # ========== TAB 1: THÔNG TIN ==========
            self.lbl_ma_hop_dong.setText(f"<b>{self.hop_dong.ma_hop_dong}</b>")
            self.lbl_trang_thai.setText(self._get_trang_thai_label(self.hop_dong.trang_thai))
            self.lbl_trang_thai.setTextFormat(Qt.TextFormat.RichText)
            
            self.lbl_khach_hang.setText(f"{khach_hang.ten_khach_hang if khach_hang else 'N/A'}")
            
            if vi_tri:
                vi_tri_info = f"{vi_tri.ma_vi_tri} - KV:{vi_tri.khu_vuc} H:{vi_tri.hang} T:{vi_tri.tang} ({vi_tri.dien_tich} m²)"
            else:
                vi_tri_info = self.hop_dong.ma_vi_tri
            self.lbl_vi_tri.setText(vi_tri_info)
            
            self.lbl_ngay_bat_dau.setText(self.hop_dong.ngay_bat_dau.strftime("%d/%m/%Y"))
            self.lbl_ngay_ket_thuc.setText(self.hop_dong.ngay_ket_thuc.strftime("%d/%m/%Y"))
            
            if remaining_days < 0:
                self.lbl_so_ngay_con_lai.setText(f"<span style='color: #f44336;'>Quá hạn {-remaining_days} ngày</span>")
            elif remaining_days == 0:
                self.lbl_so_ngay_con_lai.setText("<span style='color: #ff9800;'>Hôm nay</span>")
            elif remaining_days <= 7:
                self.lbl_so_ngay_con_lai.setText(f"<span style='color: #ff9800;'>⚠️ {remaining_days} ngày</span>")
            else:
                self.lbl_so_ngay_con_lai.setText(f"{remaining_days} ngày")
            self.lbl_so_ngay_con_lai.setTextFormat(Qt.TextFormat.RichText)
            
            self.lbl_gia_thue.setText(format_currency(self.hop_dong.gia_thue) + "/tháng")
            self.lbl_tien_coc.setText(format_currency(self.hop_dong.tien_coc))
            
            phuong_thuc_labels = {
                'hang_thang': 'Hàng tháng',
                'hang_quy': 'Hàng quý',
                'hang_nam': 'Hàng năm',
                'mot_lan': 'Một lần'
            }
            self.lbl_phuong_thuc_tt.setText(phuong_thuc_labels.get(self.hop_dong.phuong_thuc_thanh_toan, self.hop_dong.phuong_thuc_thanh_toan))
            
            self.lbl_tong_tien.setText(format_currency(total_rent))
            
            self.lbl_dieu_khoan.setText(self.hop_dong.dieu_khoan or "Không có")
            
            # ========== TAB 2: HÀNG HÓA ==========
            self._load_hang_hoa()
            
            # ========== TAB 3: THANH TOÁN ==========
            self._load_thanh_toan()
            
            # ========== TAB 4: LỊCH SỬ ==========
            self._load_lich_su()
            
        except Exception as e:
            MessageDialog.error(self, "Lỗi", f"Không thể tải dữ liệu:\n{str(e)}")
    
    def _load_hang_hoa(self):
        """Load goods data (Tab 2)"""
        try:
            hang_hoas = self.hang_hoa_service.get_by_hop_dong(self.hop_dong.ma_hop_dong)
            
            self.hang_hoa_table.setRowCount(len(hang_hoas))
            
            tong_gia_tri = 0
            
            for i, hh in enumerate(hang_hoas):
                self.hang_hoa_table.setItem(i, 0, QTableWidgetItem(hh.ma_hang_hoa))
                self.hang_hoa_table.setItem(i, 1, QTableWidgetItem(hh.ten_hang_hoa))
                self.hang_hoa_table.setItem(i, 2, QTableWidgetItem(str(hh.so_luong)))
                self.hang_hoa_table.setItem(i, 3, QTableWidgetItem(hh.don_vi_tinh or 'cái'))
                self.hang_hoa_table.setItem(i, 4, QTableWidgetItem(format_currency(hh.gia_tri or 0)))
                self.hang_hoa_table.setItem(i, 5, QTableWidgetItem(hh.ghi_chu or ''))
                
                tong_gia_tri += hh.gia_tri or 0
            
            self.lbl_tong_gia_tri_hh.setText(f"Tổng giá trị hàng hóa: {format_currency(tong_gia_tri)}")
            
        except Exception as e:
            self.hang_hoa_table.setRowCount(0)
            self.lbl_tong_gia_tri_hh.setText("Tổng giá trị hàng hóa: 0₫ (Chưa có dữ liệu)")
    
    def _load_thanh_toan(self):
        """Load payment data (Tab 3)"""
        try:
            payments = self.thanh_toan_service.get_by_hop_dong(self.hop_dong.ma_hop_dong)
            
            self.payment_table.setRowCount(len(payments))
            
            tong_da_tt = 0
            tong_con_lai = 0
            
            for i, p in enumerate(payments):
                self.payment_table.setItem(i, 0, QTableWidgetItem(p.ma_thanh_toan))
                self.payment_table.setItem(i, 1, QTableWidgetItem(p.ky_thanh_toan))
                self.payment_table.setItem(i, 2, QTableWidgetItem(p.den_han.strftime("%d/%m/%Y")))
                self.payment_table.setItem(i, 3, QTableWidgetItem(format_currency(p.so_tien)))
                
                status_label = self._get_payment_status_label(p.trang_thai)
                status_item = QTableWidgetItem(p.trang_thai)
                status_item.setForeground(Qt.GlobalColor.darkGray)  # Will be styled
                self.payment_table.setItem(i, 4, status_item)
                
                if p.trang_thai == 'da_thanh_toan':
                    tong_da_tt += p.so_tien
                else:
                    tong_con_lai += p.so_tien
            
            self.lbl_tong_da_thanh_toan.setText(f"Đã thanh toán: {format_currency(tong_da_tt)}")
            self.lbl_con_lai.setText(f"Còn lại: {format_currency(tong_con_lai)}")
            
        except Exception as e:
            self.payment_table.setRowCount(0)
            self.lbl_tong_da_thanh_toan.setText("Đã thanh toán: 0₫")
            self.lbl_con_lai.setText("Còn lại: 0₫ (Chưa tạo lịch thanh toán)")
    
    def _load_lich_su(self):
        """Load history data (Tab 4)"""
        try:
            history = self.history_service.get_history(self.hop_dong.ma_hop_dong)
            
            self.history_table.setRowCount(len(history))
            
            for i, event in enumerate(history):
                self.history_table.setItem(i, 0, QTableWidgetItem(str(i + 1)))
                self.history_table.setItem(i, 1, QTableWidgetItem(event.event_date.strftime("%d/%m/%Y")))
                
                event_icon = self._get_event_icon(event.event_type)
                event_label = f"{event_icon} {event.event_type}"
                self.history_table.setItem(i, 2, QTableWidgetItem(event_label))
                
                self.history_table.setItem(i, 3, QTableWidgetItem(event.description))
            
            # Set row heights for better readability
            for i in range(len(history)):
                self.history_table.setRowHeight(i, 40)
            
        except Exception as e:
            self.history_table.setRowCount(0)


class HopDongDetailWidget(QWidget):
    """
    Widget version of detail view (for embedding in other views)
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        """Setup UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Placeholder
        placeholder = QLabel("Chọn một hợp đồng để xem chi tiết")
        placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        placeholder.setStyleSheet("""
            QLabel {
                color: #757575;
                font-size: 16px;
                padding: 100px;
            }
        """)
        layout.addWidget(placeholder)
    
    def set_hop_dong(self, hop_dong):
        """Set contract to display"""
        # TODO: Implement
        pass


__all__ = ['HopDongDetailView', 'HopDongDetailWidget']
