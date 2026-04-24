#!/usr/bin/env python3
"""
Hợp đồng Termination Wizard - Dialog chấm dứt hợp đồng với penalty calculation
"""
from PyQt6.QtWidgets import (
    QWizard, QWizardPage, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QFormLayout, QFrame, QTextEdit, QDateEdit,
    QRadioButton, QButtonGroup, QDoubleSpinBox, QMessageBox
)
from PyQt6.QtCore import Qt, QDate, pyqtSignal
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from typing import Optional

from src.services import HopDongService
from src.models import HopDong, TrangThaiHDEnum
from src.gui.dialogs import MessageDialog
from src.utils.formatters import format_currency


class TerminationReasonPage(QWizardPage):
    """Reason selection page"""
    
    def __init__(self, hop_dong: HopDong, parent=None):
        super().__init__(parent)
        self.hop_dong = hop_dong
        self.setTitle("❓ Lý do chấm dứt")
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Info
        info = QLabel(f"""
        <h3>Hợp đồng: {self.hop_dong.ma_hop_dong}</h3>
        <p><b>Khách hàng:</b> {self.hop_dong.ma_khach_hang}</p>
        <p><b>Vị trí:</b> {self.hop_dong.ma_vi_tri}</p>
        <p><b>Ngày kết thúc theo HĐ:</b> {self.hop_dong.ngay_ket_thuc.strftime('%d/%m/%Y')}</p>
        """)
        info.setWordWrap(True)
        info.setStyleSheet("padding: 15px;")
        layout.addWidget(info)
        
        # Reason selection
        reason_group = QFrame()
        reason_group.setStyleSheet("""
            QFrame {
                background-color: #f6f5f4;
                border-radius: 8px;
                padding: 16px;
            }
        """)
        reason_layout = QVBoxLayout(reason_group)
        
        self.reason_buttons = QButtonGroup(self)
        
        reasons = [
            ("Khách hàng yêu cầu", "customer_request"),
            ("Vi phạm hợp đồng", "contract_violation"),
            ("Không thanh toán", "non_payment"),
            ("Lý do khác", "other")
        ]
        
        for text, value in reasons:
            rb = QRadioButton(text)
            rb.setProperty("reason_value", value)
            self.reason_buttons.addButton(rb)
            reason_layout.addWidget(rb)
        
        layout.addWidget(reason_group)
        
        # Additional notes
        self.notes_input = QTextEdit()
        self.notes_input.setPlaceholderText("Ghi chú thêm về lý do chấm dứt...")
        self.notes_input.setMaximumHeight(80)
        self.notes_input.setStyleSheet("""
            QTextEdit {
                padding: 8px;
                border-radius: 4px;
                border: 1px solid #bdbdbd;
            }
        """)
        layout.addWidget(QLabel("Ghi chú:"))
        layout.addWidget(self.notes_input)
    
    def validatePage(self) -> bool:
        """Validate selected reason"""
        if not self.reason_buttons.checkedButton():
            MessageDialog.warning(self, "Cảnh báo", "Vui lòng chọn lý do chấm dứt")
            return False
        return True
    
    def get_selected_reason(self) -> str:
        """Get selected reason"""
        btn = self.reason_buttons.checkedButton()
        if btn:
            return btn.text()
        return ""
    
    def get_notes(self) -> str:
        """Get additional notes"""
        return self.notes_input.toPlainText().strip()


class TerminationPenaltyPage(QWizardPage):
    """Penalty calculation page"""
    
    def __init__(self, hop_dong: HopDong, parent=None):
        super().__init__(parent)
        self.hop_dong = hop_dong
        self.setTitle("💰 Tính toán phạt vi phạm")
        self.setup_ui()
        self.calculate_penalty()
    
    def setup_ui(self):
        layout = QFormLayout(self)
        layout.setSpacing(12)
        
        # Penalty type selection
        penalty_group = QFrame()
        penalty_group.setStyleSheet("""
            QFrame {
                background-color: #fff3e0;
                border-radius: 8px;
                padding: 16px;
            }
        """)
        penalty_layout = QVBoxLayout(penalty_group)
        
        self.penalty_buttons = QButtonGroup(self)
        
        penalties = [
            ("Không phạt", 0.0),
            ("Phạt 1 tháng tiền thuê", 1.0),
            ("Phạt 2 tháng tiền thuê", 2.0),
            ("Phạt 3 tháng tiền thuê", 3.0),
            ("Phạt theo % tiền cọc", -1.0),  # Special case
        ]
        
        for text, multiplier in penalties:
            rb = QRadioButton(text)
            rb.setProperty("penalty_multiplier", multiplier)
            self.penalty_buttons.addButton(rb)
            penalty_layout.addWidget(rb)
        
        layout.addRow("Mức phạt:", penalty_group)
        
        # Custom penalty percentage (for deposit % option)
        self.custom_percent = QDoubleSpinBox()
        self.custom_percent.setRange(0, 100)
        self.custom_percent.setValue(50)
        self.custom_percent.setSuffix(" %")
        self.custom_percent.setEnabled(False)
        self.custom_percent.setStyleSheet("padding: 8px;")
        layout.addRow("Phần trăm cọc:", self.custom_percent)
        
        # Connect signals
        self.penalty_buttons.buttonClicked.connect(self.on_penalty_changed)
        self.custom_percent.valueChanged.connect(self.update_penalty_display)
        
        # Penalty summary
        self.penalty_summary = QLabel("")
        self.penalty_summary.setStyleSheet("""
            QLabel {
                padding: 15px;
                font-weight: 600;
                font-size: 15px;
                background-color: #ffebee;
                border-radius: 8px;
                color: #c62828;
            }
        """)
        layout.addRow("Tổng phạt:", self.penalty_summary)
        
        # Financial summary
        self.financial_summary = QLabel("")
        self.financial_summary.setWordWrap(True)
        self.financial_summary.setStyleSheet("""
            QLabel {
                padding: 15px;
                background-color: #e3f2fd;
                border-radius: 8px;
            }
        """)
        layout.addRow("Quyết toán:", self.financial_summary)
    
    def on_penalty_changed(self, button):
        """Handle penalty selection change"""
        multiplier = button.property("penalty_multiplier")
        self.custom_percent.setEnabled(multiplier == -1.0)
        self.update_penalty_display()
    
    def calculate_penalty(self):
        """Calculate penalty amounts"""
        # Get selected penalty
        button = self.penalty_buttons.checkedButton()
        if not button:
            return
        
        multiplier = button.property("penalty_multiplier")
        
        if multiplier >= 0:
            # Fixed months of rent
            self.penalty_amount = multiplier * self.hop_dong.gia_thue
        else:
            # Percentage of deposit
            percent = self.custom_percent.value() / 100
            self.penalty_amount = percent * self.hop_dong.tien_coc
        
        self.update_penalty_display()
    
    def update_penalty_display(self):
        """Update penalty display"""
        self.calculate_penalty()
        
        # Penalty display
        if self.penalty_amount > 0:
            self.penalty_summary.setText(f"💰 Số tiền phạt: {format_currency(self.penalty_amount)}")
        else:
            self.penalty_summary.setText("✅ Không phạt")
        
        # Financial summary
        refund = self.hop_dong.tien_coc - self.penalty_amount
        
        if refund >= 0:
            refund_text = f"Hoàn lại: {format_currency(refund)}"
        else:
            refund_text = f"Khách hàng nợ: {format_currency(abs(refund))}"
        
        self.financial_summary.setText(f"""
        <p><b>Tiền cọc:</b> {format_currency(self.hop_dong.tien_coc)}</p>
        <p><b>Tiền phạt:</b> {format_currency(self.penalty_amount)}</p>
        <hr style="border: 1px solid #90caf9;">
        <p style="font-weight: 700; font-size: 16px;">{refund_text}</p>
        """)
    
    def get_penalty_amount(self) -> float:
        """Get calculated penalty"""
        return self.penalty_amount if hasattr(self, 'penalty_amount') else 0.0
    
    def get_penalty_reason(self) -> str:
        """Get penalty description"""
        button = self.penalty_buttons.checkedButton()
        if button:
            return button.text()
        return "Không phạt"
    
    def validatePage(self) -> bool:
        """Validate penalty selection"""
        if not self.penalty_buttons.checkedButton():
            MessageDialog.warning(self, "Cảnh báo", "Vui lòng chọn mức phạt")
            return False
        return True


class TerminationConfirmPage(QWizardPage):
    """Confirmation page"""
    
    def __init__(self, hop_dong: HopDong, parent=None):
        super().__init__(parent)
        self.hop_dong = hop_dong
        self.setTitle("✅ Xác nhận chấm dứt")
        self.setCommitPage(True)
        self.setButtonText(QWizardPage.WizardPage.CommitButton, "❌ Chấm dứt")
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
        ⚠️ <b>Cảnh báo:</b>
        <ul>
        <li>Hợp đồng sẽ bị chấm dứt ngay lập tức</li>
        <li>Vị trí sẽ được giải phóng</li>
        <li>Không thể hoàn tác hành động này</li>
        </ul>
        """)
        warning.setWordWrap(True)
        warning.setStyleSheet("padding: 15px; color: #f44336;")
        layout.addWidget(warning)
    
    def initializePage(self):
        """Initialize with summary"""
        wizard = self.wizard()
        reason = wizard.get_reason()
        notes = wizard.get_notes()
        penalty = wizard.get_penalty()
        
        self.summary_label.setText(f"""
        <h3>Xác nhận chấm dứt hợp đồng</h3>
        <p><b>Hợp đồng:</b> {self.hop_dong.ma_hop_dong}</p>
        <p><b>Lý do:</b> {reason}</p>
        {f'<p><b>Ghi chú:</b> {notes}</p>' if notes else ''}
        <p><b>Tiền phạt:</b> {format_currency(penalty)}</p>
        <p><b>Ngày chấm dứt:</b> {date.today().strftime('%d/%m/%Y')}</p>
        """)


class TerminationWizard(QWizard):
    """
    Wizard for contract termination with penalty calculation
    """
    
    hop_dong_terminated = pyqtSignal(str)  # Emit ma_hop_dong
    
    def __init__(self, hop_dong: HopDong, parent=None):
        super().__init__(parent)
        self.hop_dong = hop_dong
        self.service = HopDongService()
        self.penalty_amount = 0.0
        self.reason = ""
        self.notes = ""
        self.setWindowTitle("❌ Wizard Chấm dứt Hợp đồng")
        self.setMinimumWidth(600)
        self.setMinimumHeight(500)
        self.setup_wizard()
    
    def setup_wizard(self):
        """Setup wizard pages"""
        self.addPage(TerminationReasonPage(self.hop_dong, self))
        self.addPage(TerminationPenaltyPage(self.hop_dong, self))
        self.addPage(TerminationConfirmPage(self.hop_dong, self))
        
        # Set wizard style
        self.setWizardStyle(QWizard.WizardStyle.ModernStyle)
        self.setStyleSheet("""
            QWizard {
                background-color: #ffffff;
            }
            QWizardPage {
                background-color: #ffffff;
            }
        """)
    
    def accept(self):
        """Handle wizard completion"""
        try:
            # Get data from pages
            reason_page = self.page(0)
            self.reason = reason_page.get_selected_reason()
            self.notes = reason_page.get_notes()
            
            penalty_page = self.page(1)
            self.penalty_amount = penalty_page.get_penalty_amount()
            
            # Build termination reason with penalty info
            full_reason = f"{self.reason}. {self.notes}".strip()
            if self.penalty_amount > 0:
                full_reason += f" | Phạt: {format_currency(self.penalty_amount)}"
            
            # Terminate contract
            self.service.terminate(self.hop_dong.ma_hop_dong, full_reason)
            
            MessageDialog.success(self, "Thành công", f"Đã chấm dứt hợp đồng {self.hop_dong.ma_hop_dong}")
            
            self.hop_dong_terminated.emit(self.hop_dong.ma_hop_dong)
            
            super().accept()
            
        except ValueError as e:
            MessageDialog.error(self, "Lỗi", str(e))
        except Exception as e:
            MessageDialog.error(self, "Lỗi", f"Không thể chấm dứt hợp đồng:\n{str(e)}")
    
    def get_reason(self) -> str:
        """Get termination reason"""
        return self.reason
    
    def get_notes(self) -> str:
        """Get additional notes"""
        return self.notes
    
    def get_penalty(self) -> float:
        """Get penalty amount"""
        return self.penalty_amount


__all__ = ['TerminationWizard']
