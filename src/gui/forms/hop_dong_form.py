#!/usr/bin/env python3
"""
Hợp đồng Form - Dialog thêm/sửa hợp đồng
"""
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QTextEdit, QDoubleSpinBox, QComboBox, QDialogButtonBox,
    QFormLayout, QFrame, QGroupBox, QDateEdit, QMessageBox,
    QCompleter, QListWidget, QListWidgetItem, QAbstractItemView,
    QPushButton, QWidget, QScrollArea, QCheckBox, QGridLayout
)
from PyQt6.QtCore import Qt, pyqtSignal, QDate
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List

from src.services import HopDongService, KhachHangService, ViTriService, KhoService
from src.models import HopDong, KhachHang, ViTri, TrangThaiHDEnum, TrangThaiViTriEnum, Kho
from src.gui.dialogs import MessageDialog


class HopDongForm(QDialog):
    """
    Dialog form để thêm/sửa hợp đồng
    """

    hop_dong_saved = pyqtSignal(object)  # Emit HopDong object when saved

    def __init__(self, parent=None, hop_dong: Optional[HopDong] = None):
        super().__init__(parent)
        self.service = HopDongService()
        self.khach_hang_service = KhachHangService()
        self.vi_tri_service = ViTriService()
        self.kho_service = KhoService()
        self.hop_dong = hop_dong
        self.is_edit_mode = hop_dong is not None
        self.available_vi_tris: List[ViTri] = []
        self.khach_hangs: List[KhachHang] = []
        self.selected_vi_tris: List[str] = []
        self.setup_ui()
        self.setup_connections()
        self.load_data()

        if self.is_edit_mode:
            self.load_hop_dong_data()
            self.setWindowTitle("✏️ Chỉnh sửa hợp đồng")
        else:
            self.setWindowTitle("➕ Thêm hợp đồng mới")
    
    def setup_ui(self):
        """Setup UI"""
        self.setMinimumWidth(600)
        self.setModal(True)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title = QLabel("📋 THÔNG TIN HỢP ĐỒNG" if self.is_edit_mode else "📋 THÊM HỢP ĐỒNG MỚI")
        title.setStyleSheet("""
            QLabel {
                font-size: 20px;
                font-weight: 700;
                color: #31302e;
                padding: 10px 0;
            }
        """)
        layout.addWidget(title)
        
        # Form container
        form_container = QFrame()
        form_container.setFrameShape(QFrame.Shape.StyledPanel)
        form_container.setStyleSheet("""
            QFrame {
                background-color: #f6f5f4;
                border-radius: 8px;
                padding: 16px;
            }
        """)
        
        form_layout = QFormLayout(form_container)
        form_layout.setSpacing(12)
        form_layout.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)
        
        # Mã hợp đồng (read-only if edit mode)
        self.ma_hop_dong_input = QLineEdit()
        self.ma_hop_dong_input.setPlaceholderText("Tự động tạo (HD202604001)")
        if self.is_edit_mode:
            self.ma_hop_dong_input.setReadOnly(True)
        self.ma_hop_dong_input.setStyleSheet("""
            QLineEdit {
                background-color: #e0e0e0;
                padding: 8px;
                border-radius: 4px;
                border: 1px solid #bdbdbd;
            }
        """)
        form_layout.addRow("Mã hợp đồng:", self.ma_hop_dong_input)
        
        # Khách hàng (ComboBox with search)
        self.khach_hang_selector = QComboBox()
        self.khach_hang_selector.setEditable(True)
        self.khach_hang_selector.addItem("-- Chọn khách hàng --", None)
        self.khach_hang_selector.setFixedWidth(300)
        self.khach_hang_selector.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border-radius: 4px;
                border: 1px solid #bdbdbd;
            }
            QComboBox:focus {
                border: 2px solid #1976d2;
            }
        """)
        form_layout.addRow("Khách hàng:", self.khach_hang_selector)

        # Vị trí section - Multi-select
        vi_tri_group = QGroupBox("📍 Vị trí lưu trữ (có thể chọn nhiều)")
        vi_tri_group.setStyleSheet("""
            QGroupBox {
                font-weight: 600;
                font-size: 14px;
                color: #31302e;
                border: 1px solid #bdbdbd;
                border-radius: 6px;
                margin-top: 12px;
                padding-top: 12px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
        """)

        vi_tri_layout = QVBoxLayout(vi_tri_group)
        vi_tri_layout.setSpacing(8)

        # Kho selector
        kho_row = QHBoxLayout()
        kho_row.addWidget(QLabel("Kho:"))
        self.kho_selector = QComboBox()
        self.kho_selector.addItem("-- Tất cả kho --", None)
        self.kho_selector.setFixedWidth(300)
        self.kho_selector.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border-radius: 4px;
                border: 1px solid #bdbdbd;
            }
        """)
        kho_row.addWidget(self.kho_selector)
        kho_row.addStretch()
        vi_tri_layout.addLayout(kho_row)

        # Selected positions display
        self.selected_count_label = QLabel("Chưa chọn vị trí nào")
        self.selected_count_label.setStyleSheet("""
            QLabel {
                color: #1976d2;
                font-weight: 600;
                padding: 4px 8px;
                background-color: #e3f2fd;
                border-radius: 4px;
            }
        """)
        vi_tri_layout.addWidget(self.selected_count_label)

        # Select all / Deselect all buttons
        btn_row = QHBoxLayout()
        self.select_all_btn = QPushButton("✓ Chọn tất cả")
        self.select_all_btn.setFixedWidth(120)
        self.select_all_btn.setStyleSheet("""
            QPushButton {
                padding: 6px 12px;
                border-radius: 4px;
                background-color: #e3f2fd;
                color: #1976d2;
                border: 1px solid #1976d2;
            }
            QPushButton:hover {
                background-color: #bbdefb;
            }
        """)
        self.deselect_all_btn = QPushButton("✗ Bỏ chọn tất cả")
        self.deselect_all_btn.setFixedWidth(120)
        self.deselect_all_btn.setStyleSheet("""
            QPushButton {
                padding: 6px 12px;
                border-radius: 4px;
                background-color: #f6f5f4;
                color: #757575;
                border: 1px solid #bdbdbd;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
        """)
        btn_row.addWidget(self.select_all_btn)
        btn_row.addWidget(self.deselect_all_btn)
        btn_row.addStretch()
        vi_tri_layout.addLayout(btn_row)

        # Scroll area for position list
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)

        self.vi_tri_list_widget = QListWidget()
        self.vi_tri_list_widget.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        self.vi_tri_list_widget.setStyleSheet("""
            QListWidget {
                border: 1px solid #bdbdbd;
                border-radius: 4px;
                background-color: #ffffff;
                padding: 4px;
            }
            QListWidget::item {
                padding: 8px;
                border-radius: 4px;
                margin: 2px;
            }
            QListWidget::item:selected {
                background-color: #e3f2fd;
                color: #1976d2;
            }
            QListWidget::item:hover {
                background-color: #f6f5f4;
            }
        """)
        scroll.setWidget(self.vi_tri_list_widget)
        scroll.setMinimumHeight(200)
        scroll.setMaximumHeight(300)
        vi_tri_layout.addWidget(scroll)

        form_layout.addRow(vi_tri_group)

        # Horizontal container for date and financial groups
        h_container = QWidget()
        h_layout = QHBoxLayout(h_container)
        h_layout.setSpacing(12)
        h_layout.setContentsMargins(0, 0, 0, 0)

        # Date range group
        date_group = QGroupBox("Thoi han HD")
        date_group.setStyleSheet("""
            QGroupBox {
                font-weight: 600;
                font-size: 13px;
                color: #31302e;
                border: 1px solid #bdbdbd;
                border-radius: 6px;
                padding: 8px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 8px;
                padding: 0 4px;
            }
        """)
        date_layout = QFormLayout(date_group)
        date_layout.setSpacing(8)

        # Ngay bat dau & ket thuc on same row
        h_date_layout = QHBoxLayout()
        h_date_layout.setSpacing(8)

        self.ngay_bat_dau_input = QDateEdit()
        self.ngay_bat_dau_input.setCalendarPopup(True)
        self.ngay_bat_dau_input.setDate(QDate.currentDate())
        self.ngay_bat_dau_input.setFixedWidth(120)
        self.ngay_bat_dau_input.setStyleSheet("""
            QDateEdit {
                padding: 6px;
                border-radius: 4px;
                border: 1px solid #bdbdbd;
            }
        """)

        self.ngay_ket_thuc_input = QDateEdit()
        self.ngay_ket_thuc_input.setCalendarPopup(True)
        self.ngay_ket_thuc_input.setDate(QDate.currentDate().addMonths(12))
        self.ngay_ket_thuc_input.setMinimumDate(QDate.currentDate().addDays(1))
        self.ngay_ket_thuc_input.setFixedWidth(120)
        self.ngay_ket_thuc_input.setStyleSheet("""
            QDateEdit {
                padding: 6px;
                border-radius: 4px;
                border: 1px solid #bdbdbd;
            }
        """)

        lbl1 = QLabel("Tu:")
        lbl1.setFixedWidth(25)
        h_date_layout.addWidget(lbl1)
        h_date_layout.addWidget(self.ngay_bat_dau_input)
        h_date_layout.addWidget(QLabel("Den:"))
        h_date_layout.addWidget(self.ngay_ket_thuc_input)
        h_date_layout.addStretch()
        date_layout.addRow(h_date_layout)

        # Financial group
        financial_group = QGroupBox("Tai chinh")
        financial_group.setStyleSheet("""
            QGroupBox {
                font-weight: 600;
                font-size: 13px;
                color: #31302e;
                border: 1px solid #bdbdbd;
                border-radius: 6px;
                padding: 8px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 8px;
                padding: 0 4px;
            }
        """)
        financial_layout = QFormLayout(financial_group)
        financial_layout.setSpacing(8)

        # Gia thue & Tien coc on same row
        h_fin_layout = QHBoxLayout()
        h_fin_layout.setSpacing(8)

        self.gia_thue_input = QDoubleSpinBox()
        self.gia_thue_input.setRange(0, 1000000000)
        self.gia_thue_input.setDecimals(0)
        self.gia_thue_input.setSuffix(" ₫")
        self.gia_thue_input.setValue(1500000.0)
        self.gia_thue_input.setFixedWidth(120)
        self.gia_thue_input.setButtonSymbols(QDoubleSpinBox.ButtonSymbols.NoButtons)
        self.gia_thue_input.setStyleSheet("""
            QDoubleSpinBox {
                padding: 6px;
                border-radius: 4px;
                border: 1px solid #bdbdbd;
            }
        """)

        self.tien_coc_input = QDoubleSpinBox()
        self.tien_coc_input.setRange(0, 1000000000)
        self.tien_coc_input.setDecimals(0)
        self.tien_coc_input.setSuffix(" ₫")
        self.tien_coc_input.setValue(3000000.0)
        self.tien_coc_input.setFixedWidth(120)
        self.tien_coc_input.setButtonSymbols(QDoubleSpinBox.ButtonSymbols.NoButtons)
        self.tien_coc_input.setStyleSheet("""
            QDoubleSpinBox {
                padding: 6px;
                border-radius: 4px;
                border: 1px solid #bdbdbd;
            }
        """)

        self.phuong_thuc_thanh_toan_input = QComboBox()
        self.phuong_thuc_thanh_toan_input.addItem("Hang thang", "hang_thang")
        self.phuong_thuc_thanh_toan_input.addItem("Hang quy", "hang_quy")
        self.phuong_thuc_thanh_toan_input.addItem("Hang nam", "hang_nam")
        self.phuong_thuc_thanh_toan_input.addItem("Mot lan", "mot_lan")
        self.phuong_thuc_thanh_toan_input.setFixedWidth(100)
        self.phuong_thuc_thanh_toan_input.setStyleSheet("""
            QComboBox {
                padding: 6px;
                border-radius: 4px;
                border: 1px solid #bdbdbd;
            }
        """)

        h_fin_layout.addWidget(QLabel("Gia:"))
        h_fin_layout.addWidget(self.gia_thue_input)
        h_fin_layout.addWidget(QLabel("Coc:"))
        h_fin_layout.addWidget(self.tien_coc_input)
        h_fin_layout.addWidget(QLabel("TT:"))
        h_fin_layout.addWidget(self.phuong_thuc_thanh_toan_input)
        h_fin_layout.addStretch()
        financial_layout.addRow(h_fin_layout)

        # Add both groups to horizontal layout
        h_layout.addWidget(date_group, 1)
        h_layout.addWidget(financial_group, 1)

        form_layout.addRow(h_container)
        
        # Summary info
        self.summary_label = QLabel("")
        self.summary_label.setStyleSheet("""
            QLabel {
                color: #1976d2;
                font-size: 14px;
                font-weight: 600;
                padding: 8px;
                background-color: #e3f2fd;
                border-radius: 4px;
            }
        """)
        form_layout.addRow(self.summary_label)
        
        # Điều khoản
        self.dieu_khoan_input = QTextEdit()
        self.dieu_khoan_input.setPlaceholderText("Các điều khoản và ghi chú khác...")
        self.dieu_khoan_input.setMaximumHeight(100)
        self.dieu_khoan_input.setStyleSheet("""
            QTextEdit {
                padding: 8px;
                border-radius: 4px;
                border: 1px solid #bdbdbd;
            }
            QTextEdit:focus {
                border: 2px solid #1976d2;
            }
        """)
        form_layout.addRow("Điều khoản:", self.dieu_khoan_input)
        
        layout.addWidget(form_container)
        
        # Buttons
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save | 
            QDialogButtonBox.StandardButton.Cancel
        )
        button_box.button(QDialogButtonBox.StandardButton.Save).setText("💾 Lưu")
        button_box.button(QDialogButtonBox.StandardButton.Cancel).setText("❌ Hủy")
        button_box.setStyleSheet("""
            QPushButton {
                padding: 10px 20px;
                border-radius: 6px;
                font-weight: 600;
                font-size: 14px;
            }
            QPushButton[type="accept"] {
                background-color: #1976d2;
                color: white;
            }
            QPushButton[type="accept"]:hover {
                background-color: #1565c0;
            }
            QPushButton[type="reject"] {
                background-color: #757575;
                color: white;
            }
            QPushButton[type="reject"]:hover {
                background-color: #616161;
            }
        """)
        layout.addWidget(button_box)
        
        self.save_button = button_box.button(QDialogButtonBox.StandardButton.Save)
        self.cancel_button = button_box.button(QDialogButtonBox.StandardButton.Cancel)
        
        self.save_button.clicked.connect(self._on_save)
        self.cancel_button.clicked.connect(self.reject)
    
    def setup_connections(self):
        """Setup signal connections"""
        # Auto-calculate duration and total
        self.ngay_bat_dau_input.dateChanged.connect(self._update_summary)
        self.ngay_ket_thuc_input.dateChanged.connect(self._update_summary)
        self.gia_thue_input.valueChanged.connect(self._update_summary)

        # Live validation
        self.khach_hang_selector.currentIndexChanged.connect(self._validate_form)
        self.ngay_bat_dau_input.dateChanged.connect(self._validate_dates)
        self.ngay_ket_thuc_input.dateChanged.connect(self._validate_dates)

        # Position list connections
        self.kho_selector.currentIndexChanged.connect(self._load_vi_tri_list)
        self.vi_tri_list_widget.itemSelectionChanged.connect(self._on_vi_tri_selection_changed)
        self.select_all_btn.clicked.connect(self._select_all_vi_tri)
        self.deselect_all_btn.clicked.connect(self._deselect_all_vi_tri)

    def load_data(self):
        """Load customers and available positions"""
        try:
            # Load customers
            self.khach_hangs = self.khach_hang_service.get_all(limit=1000)
            self.khach_hang_selector.clear()
            self.khach_hang_selector.addItem("-- Chọn khách hàng --", None)

            for kh in self.khach_hangs:
                display_text = f"{kh.ho_ten} ({kh.ma_khach_hang})"
                self.khach_hang_selector.addItem(display_text, kh.ma_khach_hang)

            # Load warehouses for filter
            khos = self.kho_service.get_all(limit=100)
            self.kho_selector.clear()
            self.kho_selector.addItem("-- Tất cả kho --", None)
            for kho in khos:
                if kho.trang_thai.value == 'hoat_dong':
                    self.kho_selector.addItem(f"{kho.ten_kho} ({kho.ma_kho})", kho.ma_kho)

            # Load available positions into list
            self._load_vi_tri_list()

        except Exception as e:
            MessageDialog.error(self, "Lỗi", f"Không thể tải dữ liệu:\n{str(e)}")

    def _load_vi_tri_list(self):
        """Load position list based on warehouse filter"""
        ma_kho = self.kho_selector.currentData()

        # Get available positions
        all_vi_tris = self.vi_tri_service.get_all(limit=1000)
        available_vi_tris = [
            vt for vt in all_vi_tris if vt.trang_thai == TrangThaiViTriEnum.TRONG
        ]

        # Filter by warehouse if selected
        if ma_kho:
            available_vi_tris = [vt for vt in available_vi_tris if vt.ma_kho == ma_kho]

        self.available_vi_tris = available_vi_tris

        # Clear and repopulate list
        self.vi_tri_list_widget.clear()

        for vt in self.available_vi_tris:
            display_text = f"{vt.ma_vi_tri} | KV:{vt.khu_vuc} H:{vt.hang} T:{vt.tang} | {vt.dien_tich} m² | {vt.gia_thue:,.0f} ₫"
            item = QListWidgetItem(display_text)
            item.setData(Qt.ItemDataRole.UserRole, vt.ma_vi_tri)
            self.vi_tri_list_widget.addItem(item)

        self._update_selected_count()

    def _on_vi_tri_selection_changed(self):
        """Handle position selection change"""
        selected_items = self.vi_tri_list_widget.selectedItems()
        self.selected_vi_tris = [item.data(Qt.ItemDataRole.UserRole) for item in selected_items]
        self._update_selected_count()
        self._validate_form()
        self._update_summary()

    def _update_selected_count(self):
        """Update selected positions count label"""
        count = len(self.selected_vi_tris)
        if count == 0:
            self.selected_count_label.setText("Chưa chọn vị trí nào")
            self.selected_count_label.setStyleSheet("""
                QLabel {
                    color: #757575;
                    font-weight: 500;
                    padding: 4px 8px;
                    background-color: #f6f5f4;
                    border-radius: 4px;
                }
            """)
        else:
            total_area = sum(vt.dien_tich for vt in self.available_vi_tris if vt.ma_vi_tri in self.selected_vi_tris)
            self.selected_count_label.setText(f"Đã chọn {count} vị trí (Tổng: {total_area:,.0f} m²)")
            self.selected_count_label.setStyleSheet("""
                QLabel {
                    color: #1976d2;
                    font-weight: 600;
                    padding: 4px 8px;
                    background-color: #e3f2fd;
                    border-radius: 4px;
                }
            """)

    def _select_all_vi_tri(self):
        """Select all available positions"""
        for i in range(self.vi_tri_list_widget.count()):
            self.vi_tri_list_widget.item(i).setSelected(True)

    def _deselect_all_vi_tri(self):
        """Deselect all positions"""
        self.vi_tri_list_widget.clearSelection()

    def load_hop_dong_data(self):
        """Load existing hop_dong data into form"""
        if not self.hop_dong:
            return

        self.ma_hop_dong_input.setText(self.hop_dong.ma_hop_dong)

        # Set customer
        for i in range(self.khach_hang_selector.count()):
            if self.khach_hang_selector.itemData(i) == self.hop_dong.ma_khach_hang:
                self.khach_hang_selector.setCurrentIndex(i)
                break

        # For edit mode, load the contract's position
        self.selected_vi_tris = [self.hop_dong.ma_vi_tri]
        for i in range(self.vi_tri_list_widget.count()):
            if self.vi_tri_list_widget.item(i).data(Qt.ItemDataRole.UserRole) == self.hop_dong.ma_vi_tri:
                self.vi_tri_list_widget.item(i).setSelected(True)
                break

        self._update_selected_count()
        
        # Set dates
        self.ngay_bat_dau_input.setDate(QDate(self.hop_dong.ngay_bat_dau.year, 
                                               self.hop_dong.ngay_bat_dau.month,
                                               self.hop_dong.ngay_bat_dau.day))
        self.ngay_ket_thuc_input.setDate(QDate(self.hop_dong.ngay_ket_thuc.year,
                                                self.hop_dong.ngay_ket_thuc.month,
                                                self.hop_dong.ngay_ket_thuc.day))
        
        # Set financial info
        self.gia_thue_input.setValue(self.hop_dong.gia_thue)
        self.tien_coc_input.setValue(self.hop_dong.tien_coc)
        
        # Set payment method
        for i in range(self.phuong_thuc_thanh_toan_input.count()):
            if self.phuong_thuc_thanh_toan_input.itemData(i) == self.hop_dong.phuong_thuc_thanh_toan:
                self.phuong_thuc_thanh_toan_input.setCurrentIndex(i)
                break
        
        # Set terms
        if self.hop_dong.dieu_khoan:
            self.dieu_khoan_input.setPlainText(self.hop_dong.dieu_khoan)
        
        self._update_summary()
    
    def _validate_dates(self):
        """Validate date range"""
        start_date = self.ngay_bat_dau_input.date().toPyDate()
        end_date = self.ngay_ket_thuc_input.date().toPyDate()
        
        if end_date <= start_date:
            self.ngay_ket_thuc_input.setStyleSheet("""
                QDateEdit {
                    padding: 8px;
                    border-radius: 4px;
                    border: 2px solid #f44336;
                }
            """)
            return False
        else:
            self.ngay_ket_thuc_input.setStyleSheet("""
                QDateEdit {
                    padding: 8px;
                    border-radius: 4px;
                    border: 1px solid #bdbdbd;
                }
                QDateEdit:focus {
                    border: 2px solid #1976d2;
                }
            """)
            return True
    
    def _validate_form(self) -> bool:
        """Validate form fields"""
        errors = []

        # Validate customer
        if not self.khach_hang_selector.currentData():
            errors.append("Phải chọn khách hàng")

        # Validate positions (multi-select)
        if len(self.selected_vi_tris) == 0:
            errors.append("Phải chọn ít nhất một vị trí")

        # Validate dates
        if not self._validate_dates():
            errors.append("Ngày kết thúc phải sau ngày bắt đầu")

        # Validate price
        if self.gia_thue_input.value() <= 0:
            errors.append("Giá thuê phải lớn hơn 0")

        # Update save button state
        if errors:
            self.save_button.setEnabled(False)
            self.save_button.setStyleSheet("""
                QPushButton {
                    padding: 10px 20px;
                    border-radius: 6px;
                    font-weight: 600;
                    font-size: 14px;
                    background-color: #bdbdbd;
                    color: #757575;
                }
            """)
        else:
            self.save_button.setEnabled(True)
            self.save_button.setStyleSheet("""
                QPushButton {
                    padding: 10px 20px;
                    border-radius: 6px;
                    font-weight: 600;
                    font-size: 14px;
                    background-color: #1976d2;
                    color: white;
                }
                QPushButton:hover {
                    background-color: #1565c0;
                }
            """)

        return len(errors) == 0

    def _update_summary(self):
        """Update contract summary"""
        start_date = self.ngay_bat_dau_input.date().toPyDate()
        end_date = self.ngay_ket_thuc_input.date().toPyDate()

        # Calculate duration in months
        duration_months = (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month)
        if end_date.day < start_date.day:
            duration_months -= 1

        duration_months = max(1, duration_months)

        # Calculate total for each position
        selected_count = len(self.selected_vi_tris)
        if selected_count > 0:
            total_rent = duration_months * self.gia_thue_input.value() * selected_count
            total_with_deposit = total_rent + (self.tien_coc_input.value() * selected_count)

            self.summary_label.setText(
                f"⏱️ Thời hạn: {duration_months} tháng | "
                f"📍 {selected_count} vị trí | "
                f"💰 Tổng tiền thuê: {total_rent:,.0f}₫ | "
                f"📦 Tổng cộng (với cọc): {total_with_deposit:,.0f}₫"
            )
        else:
            total_rent = duration_months * self.gia_thue_input.value()
            total_with_deposit = total_rent + self.tien_coc_input.value()
            self.summary_label.setText(
                f"⏱️ Thời hạn: {duration_months} tháng | "
                f"💰 Tổng tiền thuê: {total_rent:,.0f}₫ | "
                f"📦 Tổng cộng (với cọc): {total_with_deposit:,.0f}₫"
            )

    def _on_save(self):
        """Handle save button click"""
        if not self._validate_form():
            return

        try:
            created_contracts = []

            if self.is_edit_mode:
                # Update existing single contract
                data = {
                    'ma_khach_hang': self.khach_hang_selector.currentData(),
                    'ma_vi_tri': self.selected_vi_tris[0] if self.selected_vi_tris else None,
                    'ngay_bat_dau': self.ngay_bat_dau_input.date().toPyDate(),
                    'ngay_ket_thuc': self.ngay_ket_thuc_input.date().toPyDate(),
                    'gia_thue': self.gia_thue_input.value(),
                    'tien_coc': self.tien_coc_input.value(),
                    'phuong_thuc_thanh_toan': self.phuong_thuc_thanh_toan_input.currentData(),
                    'dieu_khoan': self.dieu_khoan_input.toPlainText().strip()
                }
                hop_dong = self.service.update(self.hop_dong.ma_hop_dong, data)
                created_contracts.append(hop_dong)
                MessageDialog.success(self, "Thành công", f"Đã cập nhật hợp đồng {hop_dong.ma_hop_dong}")
            else:
                # Create new contracts for each selected position
                for ma_vi_tri in self.selected_vi_tris:
                    data = {
                        'ma_khach_hang': self.khach_hang_selector.currentData(),
                        'ma_vi_tri': ma_vi_tri,
                        'ngay_bat_dau': self.ngay_bat_dau_input.date().toPyDate(),
                        'ngay_ket_thuc': self.ngay_ket_thuc_input.date().toPyDate(),
                        'gia_thue': self.gia_thue_input.value(),
                        'tien_coc': self.tien_coc_input.value(),
                        'phuong_thuc_thanh_toan': self.phuong_thuc_thanh_toan_input.currentData(),
                        'dieu_khoan': self.dieu_khoan_input.toPlainText().strip()
                    }
                    hop_dong = self.service.create(data)
                    created_contracts.append(hop_dong)

                if len(created_contracts) == 1:
                    MessageDialog.success(self, "Thành công", f"Đã tạo hợp đồng {created_contracts[0].ma_hop_dong}")
                else:
                    MessageDialog.success(self, "Thành công", f"Đã tạo {len(created_contracts)} hợp đồng")

            # Emit the contracts
            for hop_dong in created_contracts:
                self.hop_dong_saved.emit(hop_dong)

            self.accept()

        except ValueError as e:
            MessageDialog.error(self, "Lỗi", str(e))
        except Exception as e:
            MessageDialog.error(self, "Lỗi", f"Không thể lưu hợp đồng:\n{str(e)}")

    def get_data(self) -> dict:
        """Get form data as dict"""
        return {
            'ma_khach_hang': self.khach_hang_selector.currentData(),
            'ma_vi_tri': self.selected_vi_tris[0] if self.selected_vi_tris else None,
            'danh_sach_vi_tri': self.selected_vi_tris,
            'ngay_bat_dau': self.ngay_bat_dau_input.date().toPyDate(),
            'ngay_ket_thuc': self.ngay_ket_thuc_input.date().toPyDate(),
            'gia_thue': self.gia_thue_input.value(),
            'tien_coc': self.tien_coc_input.value(),
            'phuong_thuc_thanh_toan': self.phuong_thuc_thanh_toan_input.currentData(),
            'dieu_khoan': self.dieu_khoan_input.toPlainText().strip()
        }


__all__ = ['HopDongForm']
