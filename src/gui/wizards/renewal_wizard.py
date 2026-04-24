#!/usr/bin/env python3
"""
Hợp đồng Renewal Wizard - Dialog gia hạn hợp đồng
"""
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFormLayout, QFrame, QDateEdit, QDoubleSpinBox, QMessageBox,
    QWizard, QWizardPage, QRadioButton, QButtonGroup
)
from PyQt6.QtCore import Qt, QDate, pyqtSignal
from datetime import datetime
from dateutil.relativedelta import relativedelta
from typing import Optional

from src.services import HopDongService
from src.models import HopDong, TrangThaiHDEnum
from src.gui.dialogs import MessageDialog
from src.utils.formatters import format_currency


class RenewalIntroPage(QWizardPage):
    """Introduction page for renewal wizard"""
    
    def __init__(self, hop_dong: HopDong, parent=None):
        super().__init__(parent)
        self.hop_dong = hop_dong
        self.setTitle("📋 Thông tin hợp đồng hiện tại")
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        info_text = QLabel(f"""
        <h3>Hợp đồng: {self.hop_dong.ma_hop_dong}</h3>
        <p><b>Khách hàng:</b> {self.hop_dong.ma_khach_hang}</p>
        <p><b>Vị trí:</b> {self.hop_dong.ma_vi_tri}</p>
        <p><b>Ngày bắt đầu:</b> {self.hop_dong.ngay_bat_dau.strftime('%d/%m/%Y')}</p>
        <p><b>Ngày kết thúc:</b> {self.hop_dong.ngay_ket_thuc.strftime('%d/%m/%Y')}</p>
        <p><b>Giá thuê hiện tại:</b> {format_currency(self.hop_dong.gia_thue)}/tháng</p>
        <p><b>Trạng thái:</b> {self.hop_dong.trang_thai.value}</p>
        """)
        info_text.setWordWrap(True)
        info_text.setStyleSheet("padding: 20px; font-size: 14px;")
        layout.addWidget(info_text)
        
        notice = QLabel("⚠️ Hợp đồng sẽ được gia hạn với điều khoản mới")
        notice.setStyleSheet("color: #ff9800; font-weight: 600; padding: 10px;")
        layout.addWidget(notice)


class RenewalTermsPage(QWizardPage):
    """Terms adjustment page"""
    
    def __init__(self, hop_dong: HopDong, parent=None):
        super().__init__(parent)
        self.hop_dong = hop_dong
        self.setTitle("📝 Điều khoản gia hạn")
        self.setup_ui()
    
    def setup_ui(self):
        layout = QFormLayout(self)
        layout.setSpacing(12)
        
        # Option: Extend duration
        self.extend_months = QDoubleSpinBox()
        self.extend_months.setRange(1, 120)
        self.extend_months.setValue(12)
        self.extend_months.setSuffix(" tháng")
        self.extend_months.setStyleSheet("padding: 8px;")
        layout.addRow("Thời gian gia hạn:", self.extend_months)
        
        # Option: Adjust rent price
        self.new_rent = QDoubleSpinBox()
        self.new_rent.setRange(0, 1000000000)
        self.new_rent.setValue(self.hop_dong.gia_thue)
        self.new_rent.setSuffix(" ₫/tháng")
        self.new_rent.setStyleSheet("padding: 8px;")
        layout.addRow("Giá thuê mới:", self.new_rent)
        
        # Calculate new end date preview
        self.preview_label = QLabel("")
        self.preview_label.setStyleSheet("""
            QLabel {
                color: #1976d2;
                font-weight: 600;
                padding: 12px;
                background-color: #e3f2fd;
                border-radius: 6px;
            }
        """)
        self.update_preview()
        layout.addRow("Dự kiến:", self.preview_label)
        
        # Connect signals
        self.extend_months.valueChanged.connect(self.update_preview)
    
    def update_preview(self):
        """Update preview label"""
        months = int(self.extend_months.value())
        new_end = self.hop_dong.ngay_ket_thuc + relativedelta(months=months)
        self.preview_label.setText(
            f"Ngày kết thúc mới: {new_end.strftime('%d/%m/%Y')} | "
            f"Tổng tiền thuê: {format_currency(months * self.new_rent.value())}"
        )
    
    def validatePage(self) -> bool:
        """Validate page"""
        if self.new_rent.value() <= 0:
            MessageDialog.error(self, "Lỗi", "Giá thuê phải lớn hơn 0")
            return False
        return True


class RenewalConfirmPage(QWizardPage):
    """Confirmation page"""
    
    def __init__(self, hop_dong: HopDong, parent=None):
        super().__init__(parent)
        self.hop_dong = hop_dong
        self.setTitle("✅ Xác nhận gia hạn")
        self.setCommitPage(True)
        self.setButtonText(QWizardPage.WizardButton.CommitButton, "💾 Gia hạn")
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        self.summary_label = QLabel("")
        self.summary_label.setWordWrap(True)
        self.summary_label.setStyleSheet("""
            QLabel {
                padding: 20px;
                font-size: 14px;
                background-color: #f6f5f4;
                border-radius: 8px;
            }
        """)
        layout.addWidget(self.summary_label)
        
        warning = QLabel("""
        ⚠️ <b>Lưu ý:</b>
        <ul>
        <li>Hợp đồng sẽ được cập nhật với điều khoản mới</li>
        <li>Trạng thái sẽ chuyển sang 'Gia hạn'</li>
        <li>Lịch sử gia hạn sẽ được ghi nhận</li>
        </ul>
        """)
        warning.setWordWrap(True)
        warning.setStyleSheet("padding: 15px; color: #ff9800;")
        layout.addWidget(warning)
    
    def initializePage(self):
        """Initialize page with summary"""
        wizard = self.wizard()
        months = int(wizard.field("extend_months"))
        new_rent = wizard.field("new_rent")
        
        new_end = self.hop_dong.ngay_ket_thuc + relativedelta(months=months)
        total_rent = months * new_rent
        
        self.summary_label.setText(f"""
        <h3>Tóm tắt gia hạn</h3>
        <p><b>Hợp đồng:</b> {self.hop_dong.ma_hop_dong}</p>
        <p><b>Thời gian gia hạn:</b> {months} tháng</p>
        <p><b>Giá thuê mới:</b> {format_currency(new_rent)}/tháng</p>
        <p><b>Tổng tiền thuê:</b> {format_currency(total_rent)}</p>
        <p><b>Ngày kết thúc mới:</b> {new_end.strftime('%d/%m/%Y')}</p>
        """)


class RenewalWizard(QWizard):
    """
    Wizard for contract renewal
    """
    
    hop_dong_renewed = pyqtSignal(object)  # Emit updated HopDong
    
    def __init__(self, hop_dong: HopDong, parent=None):
        super().__init__(parent)
        self.hop_dong = hop_dong
        self.service = HopDongService()
        self.setWindowTitle("🔄 Wizard Gia hạn Hợp đồng")
        self.setMinimumWidth(600)
        self.setMinimumHeight(500)
        self.setup_wizard()
    
    def setup_wizard(self):
        """Setup wizard pages"""
        # Register fields
        self.setField("extend_months", 12)
        self.setField("new_rent", self.hop_dong.gia_thue)
        
        # Add pages
        self.addPage(RenewalIntroPage(self.hop_dong, self))
        self.addPage(RenewalTermsPage(self.hop_dong, self))
        self.addPage(RenewalConfirmPage(self.hop_dong, self))
        
        # Set wizard style
        self.setWizardStyle(QWizard.WizardStyle.ModernStyle)
        self.setStyleSheet("""
            QWizard {
                background-color: #ffffff;
            }
            QWizardPage {
                background-color: #ffffff;
            }
            QLabel#titleLabel {
                font-size: 18px;
                font-weight: 700;
            }
        """)
    
    def accept(self):
        """Handle wizard completion"""
        try:
            # Get data from wizard
            months = int(self.field("extend_months"))
            new_rent = self.field("new_rent")
            
            # Calculate new end date
            new_end_date = self.hop_dong.ngay_ket_thuc + relativedelta(months=months)
            
            # Prepare update data
            update_data = {
                'ngay_ket_thuc_moi': new_end_date,
                'gia_thue_moi': new_rent
            }
            
            # Renew contract
            updated_hop_dong = self.service.renew(self.hop_dong.ma_hop_dong, update_data)
            
            MessageDialog.success(self, "Thành công", f"Đã gia hạn hợp đồng {updated_hop_dong.ma_hop_dong}")
            
            self.hop_dong_renewed.emit(updated_hop_dong)
            
            super().accept()
            
        except ValueError as e:
            MessageDialog.error(self, "Lỗi", str(e))
        except Exception as e:
            MessageDialog.error(self, "Lỗi", f"Không thể gia hạn hợp đồng:\n{str(e)}")


__all__ = ['RenewalWizard']
