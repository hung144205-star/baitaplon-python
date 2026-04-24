#!/usr/bin/env python3
"""
Phiếu Xuất Form - Dialog xuất kho hàng hóa
"""
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QTextEdit, QSpinBox, QDialogButtonBox,
    QFormLayout, QFrame, QGroupBox, QDateEdit, QMessageBox,
    QProgressBar
)
from PyQt6.QtCore import Qt, pyqtSignal, QDate
from datetime import datetime
from typing import Optional

from src.services import HangHoaService
from src.models import HangHoa
from src.gui.dialogs import MessageDialog
from src.utils.formatters import format_currency


class PhieuXuatForm(QDialog):
    """
    Dialog form để xuất kho hàng hóa (Phiếu xuất kho)
    """
    
    xuat_kho_complete = pyqtSignal(object)  # Emit HangHoa object
    
    def __init__(self, parent=None, hang_hoa: Optional[HangHoa] = None):
        super().__init__(parent)
        self.hang_hoa_service = HangHoaService()
        self.hang_hoa = hang_hoa
        self.setup_ui()
        self.setup_connections()
        
        if self.hang_hoa:
            self.load_hang_hoa_info()
            self.setWindowTitle("📤 Phiếu Xuất Kho")
        else:
            self.setWindowTitle("⚠️ Chọn hàng hóa")
            MessageDialog.warning(self, "Cảnh báo", "Vui lòng chọn một mặt hàng để xuất")
            self.reject()
    
    def setup_ui(self):
        """Setup UI"""
        self.setMinimumWidth(600)
        self.setModal(True)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title = QLabel("📤 PHIẾU XUẤT KHO")
        title.setStyleSheet("""
            QLabel {
                font-size: 20px;
                font-weight: 700;
                color: #31302e;
                padding: 10px 0;
            }
        """)
        layout.addWidget(title)
        
        # Goods info box
        goods_info = QFrame()
        goods_info.setFrameShape(QFrame.Shape.StyledPanel)
        goods_info.setStyleSheet("""
            QFrame {
                background-color: #e3f2fd;
                border-radius: 8px;
                padding: 16px;
                border-left: 4px solid #1976d2;
            }
        """)
        goods_layout = QVBoxLayout(goods_info)
        goods_layout.setSpacing(8)
        
        self.lbl_ma_hang = QLabel("")
        self.lbl_ma_hang.setStyleSheet("font-weight: 700; font-size: 16px; color: #1976d2;")
        goods_layout.addWidget(self.lbl_ma_hang)
        
        self.lbl_ten_hang = QLabel("")
        self.lbl_ten_hang.setStyleSheet("font-size: 14px;")
        goods_layout.addWidget(self.lbl_ten_hang)
        
        self.lbl_current_stock = QLabel("")
        self.lbl_current_stock.setStyleSheet("font-weight: 600; color: #ff9800;")
        goods_layout.addWidget(self.lbl_current_stock)
        
        layout.addWidget(goods_info)
        
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
        
        # Quantity to export
        qty_group = QGroupBox("📊 Số lượng xuất")
        qty_group.setStyleSheet("""
            QGroupBox {
                font-weight: 600;
                font-size: 14px;
                color: #31302e;
                border: 1px solid #bdbdbd;
                border-radius: 6px;
                margin-top: 12px;
                padding-top: 12px;
            }
        """)
        qty_layout = QFormLayout(qty_group)
        qty_layout.setSpacing(12)
        
        self.so_luong_input = QSpinBox()
        self.so_luong_input.setRange(1, 1000000)
        self.so_luong_input.setValue(1)
        self.so_luong_input.setStyleSheet("""
            QSpinBox {
                padding: 8px;
                border-radius: 4px;
                border: 1px solid #bdbdbd;
            }
            QSpinBox:focus {
                border: 2px solid #1976d2;
            }
        """)
        qty_layout.addRow("Số lượng:", self.so_luong_input)
        
        self.lbl_remaining = QLabel("")
        self.lbl_remaining.setStyleSheet("font-size: 13px; color: #615d59;")
        qty_layout.addRow("Còn lại:", self.lbl_remaining)
        
        # Stock level indicator
        self.stock_indicator = QProgressBar()
        self.stock_indicator.setMinimum(0)
        self.stock_indicator.setMaximum(100)
        self.stock_indicator.setValue(100)
        self.stock_indicator.setFormat("%p%")
        self.stock_indicator.setStyleSheet("""
            QProgressBar {
                background-color: #e0e0e0;
                border: none;
                border-radius: 6px;
                height: 20px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #1aae39;
                border-radius: 6px;
            }
        """)
        qty_layout.addRow("Mức tồn:", self.stock_indicator)
        
        form_layout.addRow(qty_group)
        
        # Date & Notes group
        info_group = QGroupBox("📝 Thông tin xuất")
        info_group.setStyleSheet("""
            QGroupBox {
                font-weight: 600;
                font-size: 14px;
                color: #31302e;
                border: 1px solid #bdbdbd;
                border-radius: 6px;
                margin-top: 12px;
                padding-top: 12px;
            }
        """)
        info_layout = QFormLayout(info_group)
        info_layout.setSpacing(12)
        
        # Export date
        self.ngay_xuat_input = QDateEdit()
        self.ngay_xuat_input.setCalendarPopup(True)
        self.ngay_xuat_input.setDate(QDate.currentDate())
        self.ngay_xuat_input.setFixedWidth(150)
        self.ngay_xuat_input.setStyleSheet("""
            QDateEdit {
                padding: 8px;
                border-radius: 4px;
                border: 1px solid #bdbdbd;
            }
        """)
        info_layout.addRow("Ngày xuất:", self.ngay_xuat_input)
        
        # Notes
        self.ghi_chu_input = QTextEdit()
        self.ghi_chu_input.setPlaceholderText("Lý do xuất, người nhận, ghi chú...")
        self.ghi_chu_input.setMaximumHeight(80)
        self.ghi_chu_input.setStyleSheet("""
            QTextEdit {
                padding: 8px;
                border-radius: 4px;
                border: 1px solid #bdbdbd;
            }
        """)
        info_layout.addRow("Ghi chú:", self.ghi_chu_input)
        
        form_layout.addRow(info_group)
        
        layout.addWidget(form_container)
        
        # Warning label
        self.warning_label = QLabel("")
        self.warning_label.setWordWrap(True)
        self.warning_label.setStyleSheet("""
            QLabel {
                color: #d32f2f;
                font-weight: 600;
                padding: 12px;
                background-color: #ffebee;
                border-radius: 6px;
            }
        """)
        self.warning_label.hide()
        layout.addWidget(self.warning_label)
        
        # Buttons
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save |
            QDialogButtonBox.StandardButton.Cancel
        )
        button_box.button(QDialogButtonBox.StandardButton.Save).setText("📤 Xuất kho")
        button_box.button(QDialogButtonBox.StandardButton.Cancel).setText("❌ Hủy")
        button_box.setStyleSheet("""
            QPushButton {
                padding: 10px 20px;
                border-radius: 6px;
                font-weight: 600;
                font-size: 14px;
            }
            QPushButton[type="accept"] {
                background-color: #ff9800;
                color: white;
            }
            QPushButton[type="accept"]:hover {
                background-color: #f57c00;
            }
            QPushButton[type="reject"] {
                background-color: #757575;
                color: white;
            }
        """)
        layout.addWidget(button_box)
        
        self.save_button = button_box.button(QDialogButtonBox.StandardButton.Save)
        self.cancel_button = button_box.button(QDialogButtonBox.StandardButton.Cancel)
        
        self.save_button.clicked.connect(self._on_save)
        self.cancel_button.clicked.connect(self.reject)
    
    def setup_connections(self):
        """Setup signal connections"""
        self.so_luong_input.valueChanged.connect(self._update_remaining)
    
    def load_hang_hoa_info(self):
        """Load goods information"""
        if not self.hang_hoa:
            return
        
        self.lbl_ma_hang.setText(f"Mã: {self.hang_hoa.ma_hang_hoa}")
        self.lbl_ten_hang.setText(f"📦 {self.hang_hoa.ten_hang} ({self.hang_hoa.loai_hang})")
        self.lbl_current_stock.setText(f"✅ Tồn kho: {self.hang_hoa.so_luong} {self.hang_hoa.don_vi}")
        
        # Set max quantity
        self.so_luong_input.setMaximum(self.hang_hoa.so_luong)
        self.so_luong_input.setValue(min(1, self.hang_hoa.so_luong))
        
        # Update remaining
        self._update_remaining()
    
    def _update_remaining(self):
        """Update remaining quantity display"""
        if not self.hang_hoa:
            return
        
        so_luong_xuat = self.so_luong_input.value()
        con_lai = self.hang_hoa.so_luong - so_luong_xuat
        
        # Update remaining label
        self.lbl_remaining.setText(f"{con_lai} {self.hang_hoa.don_vi}")
        
        # Update stock indicator
        if self.hang_hoa.so_luong > 0:
            percent = (con_lai / self.hang_hoa.so_luong) * 100
        else:
            percent = 0
        
        self.stock_indicator.setValue(int(percent))
        
        # Change color based on remaining
        if con_lai == 0:
            color = "#f44336"  # Red - empty
            self.warning_label.setText("⚠️ CẢNH BÁO: Xuất hết hàng! Không còn tồn kho.")
            self.warning_label.show()
        elif con_lai <= 10:
            color = "#ff9800"  # Orange - low stock
            self.warning_label.setText(f"⚠️ CẢNH BÁO: Số lượng còn lại rất thấp ({con_lai} {self.hang_hoa.don_vi})")
            self.warning_label.show()
        else:
            color = "#1aae39"  # Green - good
            self.warning_label.hide()
        
        self.stock_indicator.setStyleSheet(f"""
            QProgressBar {{
                background-color: #e0e0e0;
                border: none;
                border-radius: 6px;
                height: 20px;
                text-align: center;
            }}
            QProgressBar::chunk {{
                background-color: {color};
                border-radius: 6px;
            }}
        """)
        
        # Validate
        self._validate_form()
    
    def _validate_form(self) -> bool:
        """Validate form fields"""
        so_luong_xuat = self.so_luong_input.value()
        
        if so_luong_xuat <= 0:
            self.save_button.setEnabled(False)
            return False
        
        if so_luong_xuat > self.hang_hoa.so_luong:
            self.save_button.setEnabled(False)
            self.warning_label.setText(f"⚠️ Số lượng xuất ({so_luong_xuat}) vượt quá tồn kho ({self.hang_hoa.so_luong})")
            self.warning_label.show()
            return False
        
        if not self.warning_label.isVisible():
            self.save_button.setEnabled(True)
            return True
        
        # Allow export even with warning, but show warning
        self.save_button.setEnabled(True)
        return True
    
    def _on_save(self):
        """Handle save button click"""
        if not self._validate_form():
            return
        
        # Confirm export
        reply = QMessageBox.question(
            self,
            "Xác nhận xuất kho",
            f"Bạn có chắc chắn muốn xuất {self.so_luong_input.value()} {self.hang_hoa.don_vi} {self.hang_hoa.ten_hang}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply != QMessageBox.StandardButton.Yes:
            return
        
        try:
            # Prepare export data
            export_data = {
                'ghi_chu': self.ghi_chu_input.toPlainText().strip()
            }
            
            # Export goods
            success = self.hang_hoa_service.export_goods(
                self.hang_hoa.ma_hang_hoa,
                self.so_luong_input.value(),
                export_data
            )
            
            if success:
                con_lai = self.hang_hoa.so_luong - self.so_luong_input.value()
                MessageDialog.success(
                    self,
                    "Thành công",
                    f"Đã xuất kho thành công!\n"
                    f"Số lượng: {self.so_luong_input.value()} {self.hang_hoa.don_vi}\n"
                    f"Còn lại: {con_lai} {self.hang_hoa.don_vi}"
                )
                
                self.xuat_kho_complete.emit(self.hang_hoa)
                self.accept()
            else:
                MessageDialog.error(self, "Lỗi", "Không thể xuất kho")
                
        except ValueError as e:
            MessageDialog.error(self, "Lỗi", str(e))
        except Exception as e:
            MessageDialog.error(self, "Lỗi", f"Không thể xuất kho:\n{str(e)}")


__all__ = ['PhieuXuatForm']
