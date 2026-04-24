#!/usr/bin/env python3
"""
Hợp đồng Form - Dialog thêm/sửa hợp đồng
"""
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QTextEdit, QDoubleSpinBox, QComboBox, QDialogButtonBox,
    QFormLayout, QFrame, QGroupBox, QDateEdit, QMessageBox,
    QCompleter
)
from PyQt6.QtCore import Qt, pyqtSignal, QDate
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List

from src.services import HopDongService, KhachHangService, ViTriService
from src.models import HopDong, KhachHang, ViTri, TrangThaiHDEnum, TrangThaiViTriEnum
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
        self.hop_dong = hop_dong
        self.is_edit_mode = hop_dong is not None
        self.available_vi_tris: List[ViTri] = []
        self.khach_hangs: List[KhachHang] = []
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
        
        # Vị trí (ComboBox with filter)
        self.vi_tri_selector = QComboBox()
        self.vi_tri_selector.setEditable(True)
        self.vi_tri_selector.addItem("-- Chọn vị trí (trống) --", None)
        self.vi_tri_selector.setFixedWidth(300)
        self.vi_tri_selector.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border-radius: 4px;
                border: 1px solid #bdbdbd;
            }
            QComboBox:focus {
                border: 2px solid #1976d2;
            }
        """)
        form_layout.addRow("Vị trí:", self.vi_tri_selector)
        
        # Date range group
        date_group = QGroupBox("📅 Thời hạn hợp đồng")
        date_group.setStyleSheet("""
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
        date_layout = QFormLayout(date_group)
        date_layout.setSpacing(12)
        
        # Ngày bắt đầu
        self.ngay_bat_dau_input = QDateEdit()
        self.ngay_bat_dau_input.setCalendarPopup(True)
        self.ngay_bat_dau_input.setDate(QDate.currentDate())
        self.ngay_bat_dau_input.setFixedWidth(150)
        self.ngay_bat_dau_input.setStyleSheet("""
            QDateEdit {
                padding: 8px;
                border-radius: 4px;
                border: 1px solid #bdbdbd;
            }
            QDateEdit:focus {
                border: 2px solid #1976d2;
            }
        """)
        date_layout.addRow("Ngày bắt đầu:", self.ngay_bat_dau_input)
        
        # Ngày kết thúc
        self.ngay_ket_thuc_input = QDateEdit()
        self.ngay_ket_thuc_input.setCalendarPopup(True)
        self.ngay_ket_thuc_input.setDate(QDate.currentDate().addMonths(12))
        self.ngay_ket_thuc_input.setMinimumDate(QDate.currentDate().addDays(1))
        self.ngay_ket_thuc_input.setFixedWidth(150)
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
        date_layout.addRow("Ngày kết thúc:", self.ngay_ket_thuc_input)
        
        form_layout.addRow(date_group)
        
        # Financial group
        financial_group = QGroupBox("💰 Thông tin tài chính")
        financial_group.setStyleSheet("""
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
        financial_layout = QFormLayout(financial_group)
        financial_layout.setSpacing(12)
        
        # Giá thuê
        self.gia_thue_input = QDoubleSpinBox()
        self.gia_thue_input.setRange(0, 1000000000)
        self.gia_thue_input.setDecimals(0)
        self.gia_thue_input.setSuffix(" ₫/tháng")
        self.gia_thue_input.setValue(1500000.0)
        self.gia_thue_input.setFixedWidth(200)
        self.gia_thue_input.setStyleSheet("""
            QDoubleSpinBox {
                padding: 8px;
                border-radius: 4px;
                border: 1px solid #bdbdbd;
            }
            QDoubleSpinBox:focus {
                border: 2px solid #1976d2;
            }
        """)
        financial_layout.addRow("Giá thuê:", self.gia_thue_input)
        
        # Tiền cọc
        self.tien_coc_input = QDoubleSpinBox()
        self.tien_coc_input.setRange(0, 1000000000)
        self.tien_coc_input.setDecimals(0)
        self.tien_coc_input.setSuffix(" ₫")
        self.tien_coc_input.setValue(3000000.0)
        self.tien_coc_input.setFixedWidth(200)
        self.tien_coc_input.setStyleSheet("""
            QDoubleSpinBox {
                padding: 8px;
                border-radius: 4px;
                border: 1px solid #bdbdbd;
            }
            QDoubleSpinBox:focus {
                border: 2px solid #1976d2;
            }
        """)
        financial_layout.addRow("Tiền cọc:", self.tien_coc_input)
        
        # Phương thức thanh toán
        self.phuong_thuc_thanh_toan_input = QComboBox()
        self.phuong_thuc_thanh_toan_input.addItem("Hàng tháng", "hang_thang")
        self.phuong_thuc_thanh_toan_input.addItem("Hàng quý", "hang_quy")
        self.phuong_thuc_thanh_toan_input.addItem("Hàng năm", "hang_nam")
        self.phuong_thuc_thanh_toan_input.addItem("Một lần", "mot_lan")
        self.phuong_thuc_thanh_toan_input.setFixedWidth(200)
        self.phuong_thuc_thanh_toan_input.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border-radius: 4px;
                border: 1px solid #bdbdbd;
            }
            QComboBox:focus {
                border: 2px solid #1976d2;
            }
        """)
        financial_layout.addRow("Phương thức TT:", self.phuong_thuc_thanh_toan_input)
        
        form_layout.addRow(financial_group)
        
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
        self.vi_tri_selector.currentIndexChanged.connect(self._validate_form)
        self.ngay_bat_dau_input.dateChanged.connect(self._validate_dates)
        self.ngay_ket_thuc_input.dateChanged.connect(self._validate_dates)
    
    def load_data(self):
        """Load customers and available positions"""
        try:
            # Load customers
            self.khach_hangs = self.khach_hang_service.get_all(limit=1000)
            self.khach_hang_selector.clear()
            self.khach_hang_selector.addItem("-- Chọn khách hàng --", None)
            
            for kh in self.khach_hangs:
                display_text = f"{kh.ten_khach_hang} ({kh.ma_khach_hang})"
                self.khach_hang_selector.addItem(display_text, kh.ma_khach_hang)
            
            # Load available positions
            self.available_vi_tris = self.vi_tri_service.get_all(limit=1000)
            # Filter only available positions
            self.available_vi_tris = [
                vt for vt in self.available_vi_tris 
                if str(vt.trang_thai) == 'trong'
            ]
            
            self.vi_tri_selector.clear()
            self.vi_tri_selector.addItem("-- Chọn vị trí (trống) --", None)
            
            for vt in self.available_vi_tris:
                display_text = f"{vt.ma_vi_tri} - KV:{vt.khu_vuc} H:{vt.hang} T:{vt.tang} ({vt.dien_tich} m²)"
                self.vi_tri_selector.addItem(display_text, vt.ma_vi_tri)
            
        except Exception as e:
            MessageDialog.error(self, "Lỗi", f"Không thể tải dữ liệu:\n{str(e)}")
    
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
        
        # Set position
        for i in range(self.vi_tri_selector.count()):
            if self.vi_tri_selector.itemData(i) == self.hop_dong.ma_vi_tri:
                self.vi_tri_selector.setCurrentIndex(i)
                break
        
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
        
        # Validate position
        if not self.vi_tri_selector.currentData():
            errors.append("Phải chọn vị trí")
        
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
        
        # Calculate total amount
        total_rent = duration_months * self.gia_thue_input.value()
        total_with_deposit = total_rent + self.tien_coc_input.value()
        
        # Update summary label
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
            # Prepare data
            data = {
                'ma_khach_hang': self.khach_hang_selector.currentData(),
                'ma_vi_tri': self.vi_tri_selector.currentData(),
                'ngay_bat_dau': self.ngay_bat_dau_input.date().toPyDate(),
                'ngay_ket_thuc': self.ngay_ket_thuc_input.date().toPyDate(),
                'gia_thue': self.gia_thue_input.value(),
                'tien_coc': self.tien_coc_input.value(),
                'phuong_thuc_thanh_toan': self.phuong_thuc_thanh_toan_input.currentData(),
                'dieu_khoan': self.dieu_khoan_input.toPlainText().strip()
            }
            
            if self.is_edit_mode:
                # Update existing
                hop_dong = self.service.update(self.hop_dong.ma_hop_dong, data)
                MessageDialog.success(self, "Thành công", f"Đã cập nhật hợp đồng {hop_dong.ma_hop_dong}")
            else:
                # Create new
                hop_dong = self.service.create(data)
                MessageDialog.success(self, "Thành công", f"Đã tạo hợp đồng {hop_dong.ma_hop_dong}")
            
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
            'ma_vi_tri': self.vi_tri_selector.currentData(),
            'ngay_bat_dau': self.ngay_bat_dau_input.date().toPyDate(),
            'ngay_ket_thuc': self.ngay_ket_thuc_input.date().toPyDate(),
            'gia_thue': self.gia_thue_input.value(),
            'tien_coc': self.tien_coc_input.value(),
            'phuong_thuc_thanh_toan': self.phuong_thuc_thanh_toan_input.currentData(),
            'dieu_khoan': self.dieu_khoan_input.toPlainText().strip()
        }


__all__ = ['HopDongForm']
