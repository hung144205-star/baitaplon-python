#!/usr/bin/env python3
"""
Khách hàng Form - Form nhập liệu Khách hàng
"""
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QComboBox, QTextEdit, QDateEdit, QPushButton, QFrame,
    QGroupBox, QFormLayout, QMessageBox, QButtonGroup, QRadioButton
)
from PyQt6.QtCore import Qt, QDate, pyqtSignal
from PyQt6.QtGui import QFont

from src.models import KhachHang, LoaiKhachEnum, TrangThaiKHEnum
from src.utils.validators import (
    validate_email, validate_phone, validate_required, validate_length
)
from src.gui.dialogs import MessageDialog


class KhachHangForm(QDialog):
    """
    Form nhập liệu Khách hàng (Thêm/Sửa)
    """
    
    accepted_with_data = pyqtSignal(dict)  # form_data
    
    def __init__(self, parent=None, khach_hang: KhachHang = None):
        """
        Args:
            parent: Parent widget
            khach_hang: Khách hàng cần sửa (None nếu thêm mới)
        """
        super().__init__(parent)
        self.khach_hang = khach_hang
        self.is_edit_mode = khach_hang is not None
        self.setup_ui()
        self.setup_connections()
        
        if self.is_edit_mode:
            self._load_data()
    
    def setup_ui(self):
        """Setup UI"""
        self.setWindowTitle("Thêm Khách hàng" if not self.is_edit_mode else "Sửa Khách hàng")
        self.setMinimumWidth(600)
        self.setMinimumHeight(700)
        self.setModal(True)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Title
        title = QLabel("👥 THÔNG TIN KHÁCH HÀNG" if not self.is_edit_mode else "✏️ CẬP NHẬT THÔNG TIN")
        title.setObjectName("titleLabel")
        title.setStyleSheet("""
            QLabel {
                font-size: 20px;
                font-weight: 700;
                color: #31302e;
                padding: 10px 0;
            }
        """)
        layout.addWidget(title)
        
        # Main form
        form_container = QFrame()
        form_container.setFrameShape(QFrame.Shape.StyledPanel)
        form_container.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border: 1px solid rgba(0, 0, 0, 0.1);
                border-radius: 8px;
                padding: 20px;
            }
        """)
        
        form_layout = QFormLayout(form_container)
        form_layout.setSpacing(12)
        form_layout.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)
        
        # Mã khách hàng (auto-generate, read-only)
        self.ma_kh_label = QLabel("Mã khách hàng:")
        self.ma_kh_input = QLineEdit()
        self.ma_kh_input.setReadOnly(True)
        self.ma_kh_input.setStyleSheet("""
            QLineEdit:read-only {
                background-color: #f6f5f4;
                color: #615d59;
            }
        """)
        form_layout.addRow(self.ma_kh_label, self.ma_kh_input)
        
        # Họ tên (required)
        self.ho_ten_label = QLabel("Họ tên <span style='color: #d32f2f;'>*</span>:")
        self.ho_ten_input = QLineEdit()
        self.ho_ten_input.setPlaceholderText("Nhập họ tên đầy đủ")
        form_layout.addRow(self.ho_ten_label, self.ho_ten_input)
        
        # Loại khách (Cá nhân/Doanh nghiệp)
        self.loai_khach_label = QLabel("Loại khách hàng:")
        self.loai_khach_input = QComboBox()
        self.loai_khach_input.addItem("Cá nhân", "ca_nhan")
        self.loai_khach_input.addItem("Doanh nghiệp", "doanh_nghiep")
        form_layout.addRow(self.loai_khach_label, self.loai_khach_input)
        
        # Số điện thoại (required)
        self.sdt_label = QLabel("Số điện thoại <span style='color: #d32f2f;'>*</span>:")
        self.sdt_input = QLineEdit()
        self.sdt_input.setPlaceholderText("Ví dụ: 0901234567")
        form_layout.addRow(self.sdt_label, self.sdt_input)
        
        # Email
        self.email_label = QLabel("Email:")
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("email@example.com")
        form_layout.addRow(self.email_label, self.email_input)
        
        # Địa chỉ (required, multiline)
        self.dia_chi_label = QLabel("Địa chỉ <span style='color: #d32f2f;'>*</span>:")
        self.dia_chi_input = QTextEdit()
        self.dia_chi_input.setPlaceholderText("Nhập địa chỉ đầy đủ")
        self.dia_chi_input.setMaximumHeight(80)
        form_layout.addRow(self.dia_chi_label, self.dia_chi_input)
        
        # Mã số thuế (optional, chỉ hiển thị nếu là doanh nghiệp)
        self.mst_label = QLabel("Mã số thuế:")
        self.mst_input = QLineEdit()
        self.mst_input.setPlaceholderText("Mã số thuế (nếu có)")
        self.mst_label.setVisible(False)
        self.mst_input.setVisible(False)
        form_layout.addRow(self.mst_label, self.mst_input)
        
        # Ngày đăng ký
        self.ngay_dk_label = QLabel("Ngày đăng ký:")
        self.ngay_dk_input = QDateEdit()
        self.ngay_dk_input.setCalendarPopup(True)
        self.ngay_dk_input.setDate(QDate.currentDate())
        self.ngay_dk_input.setStyleSheet("padding: 8px;")
        form_layout.addRow(self.ngay_dk_label, self.ngay_dk_input)
        
        # Trạng thái
        self.trang_thai_label = QLabel("Trạng thái:")
        self.trang_thai_input = QComboBox()
        self.trang_thai_input.addItem("Hoạt động", "hoat_dong")
        self.trang_thai_input.addItem("Tạm khóa", "tam_khoa")
        if self.is_edit_mode:
            self.trang_thai_input.addItem("Đã xóa", "da_xoa")
        form_layout.addRow(self.trang_thai_label, self.trang_thai_input)
        
        layout.addWidget(form_container)
        
        # Required field note
        note = QLabel("<span style='color: #d32f2f;'>*</span> Trường bắt buộc")
        note.setStyleSheet("color: #615d59; font-size: 13px;")
        layout.addWidget(note)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        self.cancel_btn = QPushButton("Hủy")
        self.cancel_btn.setObjectName("secondaryButton")
        self.cancel_btn.setFixedWidth(120)
        self.cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_btn)
        
        self.save_btn = QPushButton("💾 Lưu")
        self.save_btn.setObjectName("primaryButton")
        self.save_btn.setFixedWidth(120)
        self.save_btn.clicked.connect(self._on_save)
        button_layout.addWidget(self.save_btn)
        
        layout.addLayout(button_layout)
    
    def setup_connections(self):
        """Setup signal connections"""
        # Show/hide MST field based on customer type
        self.loai_khach_input.currentIndexChanged.connect(self._on_loai_khach_changed)
    
    def _on_loai_khach_changed(self, index: int):
        """Handle customer type change"""
        loai_khach = self.loai_khach_input.currentData()
        is_doanh_nghiep = loai_khach == "doanh_nghiep"
        
        self.mst_label.setVisible(is_doanh_nghiep)
        self.mst_input.setVisible(is_doanh_nghiep)
    
    def _load_data(self):
        """Load existing customer data"""
        if not self.khach_hang:
            return
        
        self.ma_kh_input.setText(self.khach_hang.ma_khach_hang)
        self.ho_ten_input.setText(self.khach_hang.ho_ten)
        self.loai_khach_input.setCurrentIndex(self.loai_khach_input.findData(self.khach_hang.loai_khach.value))
        self.sdt_input.setText(self.khach_hang.so_dien_thoai)
        self.email_input.setText(self.khach_hang.email or "")
        self.dia_chi_input.setText(self.khach_hang.dia_chi)
        self.mst_input.setText(self.khach_hang.ma_so_thue or "")
        
        if self.khach_hang.ngay_dang_ky:
            self.ngay_dk_input.setDate(self.khach_hang.ngay_dang_ky)
        
        self.trang_thai_input.setCurrentIndex(self.trang_thai_input.findData(self.khach_hang.trang_thai.value))
    
    def _on_save(self):
        """Handle save button"""
        # Validate form
        is_valid, errors = self._validate_form()
        
        if not is_valid:
            error_message = "Vui lòng kiểm tra các trường:\n\n" + "\n".join(f"• {e}" for e in errors)
            MessageDialog.error(self, "Lỗi nhập liệu", error_message)
            return
        
        # Get form data
        data = self._get_form_data()
        
        # Emit signal
        self.accepted_with_data.emit(data)
        self.accept()
    
    def _validate_form(self) -> tuple:
        """
        Validate form data
        
        Returns:
            Tuple (is_valid, errors_list)
        """
        errors = []
        
        # Validate họ tên (required)
        ho_ten = self.ho_ten_input.text().strip()
        result = validate_required(ho_ten, "Họ tên")
        if not result:
            errors.append(result.message)
        else:
            result = validate_length(ho_ten, min_len=2, max_len=200, field_name="Họ tên")
            if not result:
                errors.append(result.message)
        
        # Validate số điện thoại (required)
        sdt = self.sdt_input.text().strip()
        result = validate_required(sdt, "Số điện thoại")
        if not result:
            errors.append(result.message)
        else:
            result = validate_phone(sdt)
            if not result:
                errors.append(result.message)
        
        # Validate địa chỉ (required)
        dia_chi = self.dia_chi_input.toPlainText().strip()
        result = validate_required(dia_chi, "Địa chỉ")
        if not result:
            errors.append(result.message)
        
        # Validate email (optional but must be valid if provided)
        email = self.email_input.text().strip()
        if email:
            result = validate_email(email)
            if not result:
                errors.append(result.message)
        
        # Validate mã số thuế (optional)
        mst = self.mst_input.text().strip()
        if mst:
            result = validate_length(mst, min_len=10, max_len=20, field_name="Mã số thuế")
            if not result:
                errors.append(result.message)
        
        return len(errors) == 0, errors
    
    def _get_form_data(self) -> dict:
        """Get form data as dictionary"""
        loai_khach_value = self.loai_khach_input.currentData()
        loai_khach = LoaiKhachEnum.DOANH_NGHIEP if loai_khach_value == "doanh_nghiep" else LoaiKhachEnum.CA_NHAN
        
        trang_thai_value = self.trang_thai_input.currentData()
        trang_thai = TrangThaiKHEnum(trang_thai_value)
        
        return {
            'ho_ten': self.ho_ten_input.text().strip(),
            'loai_khach': loai_khach,
            'so_dien_thoai': self.sdt_input.text().strip(),
            'email': self.email_input.text().strip() or None,
            'dia_chi': self.dia_chi_input.toPlainText().strip(),
            'ma_so_thue': self.mst_input.text().strip() or None,
            'ngay_dang_ky': self.ngay_dk_input.date().toPyDate(),
            'trang_thai': trang_thai,
        }
    
    def get_data(self) -> dict:
        """Get form data (convenience method)"""
        return self._get_form_data()


def show_khach_hang_form(parent=None, khach_hang: KhachHang = None) -> tuple:
    """
    Show customer form dialog
    
    Args:
        parent: Parent widget
        khach_hang: Customer to edit (None for add mode)
    
    Returns:
        Tuple (accepted: bool, data: dict or None)
    """
    dialog = KhachHangForm(parent, khach_hang)
    accepted = dialog.exec()
    
    if accepted:
        return True, dialog.get_data()
    return False, None


__all__ = ['KhachHangForm', 'show_khach_hang_form']
