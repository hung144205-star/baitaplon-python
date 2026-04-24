#!/usr/bin/env python3
"""
Kho Form - Dialog thêm/sửa kho
"""
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QTextEdit, QDoubleSpinBox, QSpinBox, QDialogButtonBox,
    QComboBox, QMessageBox, QFormLayout, QFrame, QWidget
)
from PyQt6.QtCore import Qt, pyqtSignal
from typing import Optional

from src.services import KhoService
from src.models import Kho, TrangThaiKhoEnum
from src.gui.dialogs import MessageDialog
from src.utils.formatters import format_number


class KhoForm(QDialog):
    """
    Dialog form để thêm/sửa kho
    """
    
    kho_saved = pyqtSignal(object)  # Emit Kho object when saved
    
    def __init__(self, parent=None, kho: Optional[Kho] = None):
        super().__init__(parent)
        self.kho_service = KhoService()
        self.kho = kho  # If None, this is add mode; else edit mode
        self.is_edit_mode = kho is not None
        self.setup_ui()
        self.setup_connections()
        
        if self.is_edit_mode:
            self.load_data()
            self.setWindowTitle("✏️ Chỉnh sửa kho")
        else:
            self.setWindowTitle("➕ Thêm kho mới")
    
    def setup_ui(self):
        """Setup UI"""
        self.setMinimumWidth(500)
        self.setModal(True)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title = QLabel("🏭 THÔNG TIN KHO" if self.is_edit_mode else "🏭 THÊM KHO MỚI")
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
        
        # Mã kho (read-only if edit mode)
        self.ma_kho_input = QLineEdit()
        self.ma_kho_input.setPlaceholderText("Tự động tạo (KHO001)")
        self.ma_kho_input.setReadOnly(True)
        self.ma_kho_input.setStyleSheet("""
            QLineEdit {
                background-color: #e0e0e0;
                padding: 8px;
                border-radius: 4px;
                border: 1px solid #bdbdbd;
            }
        """)
        form_layout.addRow("Mã kho:", self.ma_kho_input)
        
        # Tên kho
        self.ten_kho_input = QLineEdit()
        self.ten_kho_input.setPlaceholderText("Ví dụ: Kho A - Quận 7")
        self.ten_kho_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border-radius: 4px;
                border: 1px solid #bdbdbd;
            }
            QLineEdit:focus {
                border: 2px solid #1976d2;
            }
        """)
        form_layout.addRow("Tên kho:", self.ten_kho_input)
        
        # Địa chỉ
        self.dia_chi_input = QLineEdit()
        self.dia_chi_input.setPlaceholderText("Địa chỉ đầy đủ")
        self.dia_chi_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border-radius: 4px;
                border: 1px solid #bdbdbd;
            }
            QLineEdit:focus {
                border: 2px solid #1976d2;
            }
        """)
        form_layout.addRow("Địa chỉ:", self.dia_chi_input)
        
        # Diện tích (m²)
        self.dien_tich_input = QDoubleSpinBox()
        self.dien_tich_input.setRange(1, 1000000)
        self.dien_tich_input.setDecimals(2)
        self.dien_tich_input.setSuffix(" m²")
        self.dien_tich_input.setValue(100.0)
        self.dien_tich_input.setStyleSheet("""
            QDoubleSpinBox {
                padding: 8px;
                border-radius: 4px;
                border: 1px solid #bdbdbd;
            }
            QDoubleSpinBox:focus {
                border: 2px solid #1976d2;
            }
        """)
        form_layout.addRow("Diện tích:", self.dien_tich_input)
        
        # Sức chứa (m³)
        self.suc_chua_input = QDoubleSpinBox()
        self.suc_chua_input.setRange(1, 10000000)
        self.suc_chua_input.setDecimals(2)
        self.suc_chua_input.setSuffix(" m³")
        self.suc_chua_input.setValue(500.0)
        self.suc_chua_input.setStyleSheet("""
            QDoubleSpinBox {
                padding: 8px;
                border-radius: 4px;
                border: 1px solid #bdbdbd;
            }
            QDoubleSpinBox:focus {
                border: 2px solid #1976d2;
            }
        """)
        form_layout.addRow("Sức chứa:", self.suc_chua_input)
        
        # Trạng thái
        self.trang_thai_input = QComboBox()
        self.trang_thai_input.addItem("✅ Hoạt động", TrangThaiKhoEnum.HOAT_DONG)
        self.trang_thai_input.addItem("🔧 Bảo trì", TrangThaiKhoEnum.BAO_TRI)
        self.trang_thai_input.addItem("⏸️ Ngừng hoạt động", TrangThaiKhoEnum.NGUNG)
        self.trang_thai_input.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border-radius: 4px;
                border: 1px solid #bdbdbd;
            }
            QComboBox:focus {
                border: 2px solid #1976d2;
            }
        """)
        form_layout.addRow("Trạng thái:", self.trang_thai_input)
        
        # Ghi chú
        self.ghi_chu_input = QTextEdit()
        self.ghi_chu_input.setPlaceholderText("Ghi chú thêm (nếu có)")
        self.ghi_chu_input.setMaximumHeight(80)
        self.ghi_chu_input.setStyleSheet("""
            QTextEdit {
                padding: 8px;
                border-radius: 4px;
                border: 1px solid #bdbdbd;
            }
            QTextEdit:focus {
                border: 2px solid #1976d2;
            }
        """)
        form_layout.addRow("Ghi chú:", self.ghi_chu_input)
        
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
        # Live validation
        self.ten_kho_input.textChanged.connect(self._validate_form)
        self.dien_tich_input.valueChanged.connect(self._validate_form)
        self.suc_chua_input.valueChanged.connect(self._validate_form)
    
    def load_data(self):
        """Load existing kho data into form"""
        if not self.kho:
            return
        
        self.ma_kho_input.setText(self.kho.ma_kho)
        self.ten_kho_input.setText(self.kho.ten_kho)
        self.dia_chi_input.setText(self.kho.dia_chi)
        self.dien_tich_input.setValue(self.kho.dien_tich)
        self.suc_chua_input.setValue(self.kho.suc_chua)
        
        # Set status
        for i in range(self.trang_thai_input.count()):
            if self.trang_thai_input.itemData(i) == self.kho.trang_thai:
                self.trang_thai_input.setCurrentIndex(i)
                break
        
        if self.kho.ghi_chu:
            self.ghi_chu_input.setPlainText(self.kho.ghi_chu)
    
    def _validate_form(self) -> bool:
        """Validate form fields"""
        errors = []
        
        # Validate ten_kho
        if not self.ten_kho_input.text().strip():
            errors.append("Tên kho không được để trống")
        
        # Validate dia_chi
        if not self.dia_chi_input.text().strip():
            errors.append("Địa chỉ không được để trống")
        
        # Validate dien_tich
        if self.dien_tich_input.value() <= 0:
            errors.append("Diện tích phải lớn hơn 0")
        
        # Validate suc_chua
        if self.suc_chua_input.value() <= 0:
            errors.append("Sức chứa phải lớn hơn 0")
        
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
    
    def _on_save(self):
        """Handle save button click"""
        if not self._validate_form():
            return
        
        try:
            # Prepare data
            data = {
                'ten_kho': self.ten_kho_input.text().strip(),
                'dia_chi': self.dia_chi_input.text().strip(),
                'dien_tich': self.dien_tich_input.value(),
                'suc_chua': self.suc_chua_input.value(),
                'trang_thai': self.trang_thai_input.currentData(),
                'ghi_chu': self.ghi_chu_input.toPlainText().strip()
            }
            
            if self.is_edit_mode:
                # Update existing
                kho = self.kho_service.update(self.kho.ma_kho, data)
                MessageDialog.success(self, "Thành công", f"Đã cập nhật kho {kho.ma_kho}")
            else:
                # Create new
                kho = self.kho_service.create(data)
                MessageDialog.success(self, "Thành công", f"Đã tạo kho {kho.ma_kho}")
            
            self.kho_saved.emit(kho)
            self.accept()
            
        except ValueError as e:
            MessageDialog.error(self, "Lỗi", str(e))
        except Exception as e:
            MessageDialog.error(self, "Lỗi", f"Không thể lưu kho:\n{str(e)}")
    
    def get_data(self) -> dict:
        """Get form data as dict"""
        return {
            'ten_kho': self.ten_kho_input.text().strip(),
            'dia_chi': self.dia_chi_input.text().strip(),
            'dien_tich': self.dien_tich_input.value(),
            'suc_chua': self.suc_chua_input.value(),
            'trang_thai': self.trang_thai_input.currentData(),
            'ghi_chu': self.ghi_chu_input.toPlainText().strip()
        }


__all__ = ['KhoForm']
