#!/usr/bin/env python3
"""
Vi Tri Form - Dialog thêm/sửa vị trí lưu trữ
"""
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QDoubleSpinBox, QComboBox, QDialogButtonBox,
    QFormLayout, QFrame, QGroupBox, QSpinBox, QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from typing import Optional

from src.services import ViTriService, KhoService
from src.models import ViTri, Kho, TrangThaiViTriEnum, TrangThaiKhoEnum
from src.gui.dialogs import MessageDialog


class ViTriForm(QDialog):
    """
    Dialog form để thêm/sửa vị trí lưu trữ
    """
    
    vi_tri_saved = pyqtSignal(object)  # Emit ViTri object when saved
    
    def __init__(self, parent=None, vi_tri: Optional[ViTri] = None, kho: Optional[Kho] = None):
        super().__init__(parent)
        self.vi_tri_service = ViTriService()
        self.kho_service = KhoService()
        self.vi_tri = vi_tri  # If None, this is add mode
        self.selected_kho = kho  # Required for add mode
        self.is_edit_mode = vi_tri is not None
        self.setup_ui()
        self.setup_connections()
        
        if self.is_edit_mode:
            self.load_data()
            self.setWindowTitle("✏️ Chỉnh sửa vị trí")
        else:
            self.setWindowTitle("➕ Thêm vị trí mới")
            if kho:
                self._on_kho_selected(kho)
    
    def setup_ui(self):
        """Setup UI"""
        self.setMinimumWidth(550)
        self.setModal(True)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title = QLabel("📍 THÔNG TIN VỊ TRÍ" if self.is_edit_mode else "📍 THÊM VỊ TRÍ MỚI")
        title.setStyleSheet("""
            QLabel {
                font-size: 20px;
                font-weight: 700;
                color: #31302e;
                padding: 10px 0;
            }
        """)
        layout.addWidget(title)
        
        # Kho selection (only for add mode)
        if not self.is_edit_mode:
            kho_group = self._create_kho_selector()
            layout.addWidget(kho_group)
        
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
        
        # Mã vị trí (read-only, auto-generated)
        self.ma_vi_tri_input = QLineEdit()
        self.ma_vi_tri_input.setPlaceholderText("Tự động tạo")
        self.ma_vi_tri_input.setReadOnly(True)
        self.ma_vi_tri_input.setStyleSheet("""
            QLineEdit {
                background-color: #e0e0e0;
                padding: 8px;
                border-radius: 4px;
                border: 1px solid #bdbdbd;
            }
        """)
        form_layout.addRow("Mã vị trí:", self.ma_vi_tri_input)
        
        # Location info group
        location_group = QGroupBox("📍 Vị trí trong kho")
        location_group.setStyleSheet("""
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
        location_layout = QFormLayout(location_group)
        location_layout.setSpacing(12)
        
        # Khu vực
        self.khu_vuc_input = QComboBox()
        self.khu_vuc_input.setEditable(True)
        self.khu_vuc_input.addItem("A", "A")
        self.khu_vuc_input.addItem("B", "B")
        self.khu_vuc_input.addItem("C", "C")
        self.khu_vuc_input.addItem("D", "D")
        self.khu_vuc_input.setFixedWidth(150)
        self.khu_vuc_input.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border-radius: 4px;
                border: 1px solid #bdbdbd;
            }
            QComboBox:focus {
                border: 2px solid #1976d2;
            }
        """)
        location_layout.addRow("Khu vực:", self.khu_vuc_input)
        
        # Hàng
        self.hang_input = QLineEdit()
        self.hang_input.setPlaceholderText("01")
        self.hang_input.setMaxLength(2)
        self.hang_input.setFixedWidth(150)
        self.hang_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border-radius: 4px;
                border: 1px solid #bdbdbd;
            }
            QLineEdit:focus {
                border: 2px solid #1976d2;
            }
        """)
        location_layout.addRow("Hàng:", self.hang_input)
        
        # Tầng
        self.tang_input = QSpinBox()
        self.tang_input.setRange(1, 10)
        self.tang_input.setValue(1)
        self.tang_input.setFixedWidth(150)
        self.tang_input.setStyleSheet("""
            QSpinBox {
                padding: 8px;
                border-radius: 4px;
                border: 1px solid #bdbdbd;
            }
            QSpinBox:focus {
                border: 2px solid #1976d2;
            }
        """)
        location_layout.addRow("Tầng:", self.tang_input)
        
        form_layout.addRow(location_group)
        
        # Specifications group
        spec_group = QGroupBox("⚙️ Thông số kỹ thuật")
        spec_group.setStyleSheet("""
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
        spec_layout = QFormLayout(spec_group)
        spec_layout.setSpacing(12)
        
        # Diện tích
        self.dien_tich_input = QDoubleSpinBox()
        self.dien_tich_input.setRange(1, 10000)
        self.dien_tich_input.setDecimals(2)
        self.dien_tich_input.setSuffix(" m²")
        self.dien_tich_input.setValue(50.0)
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
        spec_layout.addRow("Diện tích:", self.dien_tich_input)
        
        # Sức chứa
        self.suc_chua_input = QDoubleSpinBox()
        self.suc_chua_input.setRange(1, 1000)
        self.suc_chua_input.setDecimals(2)
        self.suc_chua_input.setSuffix(" m³")
        self.suc_chua_input.setValue(30.0)
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
        spec_layout.addRow("Sức chứa:", self.suc_chua_input)
        
        # Giá thuê
        self.gia_thue_input = QDoubleSpinBox()
        self.gia_thue_input.setRange(0, 1000000000)
        self.gia_thue_input.setDecimals(0)
        self.gia_thue_input.setSuffix(" ₫/tháng")
        self.gia_thue_input.setValue(150000.0)
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
        spec_layout.addRow("Giá thuê:", self.gia_thue_input)
        
        form_layout.addRow(spec_group)
        
        # Trạng thái
        self.trang_thai_input = QComboBox()
        self.trang_thai_input.addItem("✅ Trống", TrangThaiViTriEnum.TRONG)
        self.trang_thai_input.addItem("📋 Đã thuê", TrangThaiViTriEnum.DA_THUE)
        self.trang_thai_input.addItem("🔧 Bảo trì", TrangThaiViTriEnum.BAO_TRI)
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
    
    def _create_kho_selector(self) -> QGroupBox:
        """Create warehouse selector"""
        group = QGroupBox("🏭 Chọn kho")
        group.setStyleSheet("""
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
        
        layout = QHBoxLayout(group)
        
        layout.addWidget(QLabel("Kho:"))
        self.kho_selector = QComboBox()
        self.kho_selector.addItem("-- Chọn kho --", None)
        self.kho_selector.currentIndexChanged.connect(self._on_kho_selector_changed)
        layout.addWidget(self.kho_selector)
        
        layout.addStretch()
        
        # Load warehouses
        try:
            khos = self.kho_service.get_all(limit=100)
            for kho in khos:
                if kho.trang_thai == TrangThaiKhoEnum.HOAT_DONG:
                    self.kho_selector.addItem(f"{kho.ten_kho} ({kho.ma_kho})", kho)
        except Exception as e:
            print(f"Error loading warehouses: {e}")
        
        return group
    
    def setup_connections(self):
        """Setup signal connections"""
        # Live validation
        self.khu_vuc_input.currentTextChanged.connect(self._update_ma_vi_tri_preview)
        self.khu_vuc_input.editTextChanged.connect(self._update_ma_vi_tri_preview)
        self.hang_input.textChanged.connect(self._update_ma_vi_tri_preview)
        self.tang_input.valueChanged.connect(self._update_ma_vi_tri_preview)
        self.dien_tich_input.valueChanged.connect(self._validate_form)
        self.gia_thue_input.valueChanged.connect(self._validate_form)
    
    def _on_kho_selector_changed(self, index: int):
        """Handle warehouse selection"""
        kho = self.kho_selector.itemData(index)
        if kho:
            self._on_kho_selected(kho)
    
    def _on_kho_selected(self, kho: Kho):
        """Handle warehouse selection (programmatic)"""
        self.selected_kho = kho
        self._update_ma_vi_tri_preview()
    
    def _update_ma_vi_tri_preview(self):
        """Update mã vị trí preview"""
        if not self.selected_kho:
            return
        
        # Auto-generate preview
        khu_vuc = self.khu_vuc_input.currentText().upper() or "A"
        hang = self.hang_input.text().zfill(2) or "01"
        tang = str(self.tang_input.value()).zfill(2)
        so_thu_tu = "001"
        
        ma_vi_tri = f"{self.selected_kho.ma_kho}-{khu_vuc}-{hang}-{tang}-{so_thu_tu}"
        self.ma_vi_tri_input.setText(ma_vi_tri)
    
    def load_data(self):
        """Load existing vi_tri data into form"""
        if not self.vi_tri:
            return
        
        self.ma_vi_tri_input.setText(self.vi_tri.ma_vi_tri)
        self.khu_vuc_input.setCurrentText(self.vi_tri.khu_vuc)
        self.hang_input.setText(self.vi_tri.hang)
        self.tang_input.setValue(self.vi_tri.tang)
        self.dien_tich_input.setValue(self.vi_tri.dien_tich)
        # Handle None value for suc_chua
        if self.vi_tri.suc_chua is not None:
            self.suc_chua_input.setValue(self.vi_tri.suc_chua)
        else:
            self.suc_chua_input.setValue(0.0)
        self.gia_thue_input.setValue(self.vi_tri.gia_thue)
        
        # Set status
        for i in range(self.trang_thai_input.count()):
            if self.trang_thai_input.itemData(i) == self.vi_tri.trang_thai:
                self.trang_thai_input.setCurrentIndex(i)
                break
    
    def _validate_form(self) -> bool:
        """Validate form fields"""
        errors = []
        
        # Validate khu_vuc
        if not self.khu_vuc_input.currentText().strip():
            errors.append("Khu vực không được để trống")
        
        # Validate hang
        if not self.hang_input.text().strip():
            errors.append("Hàng không được để trống")
        
        # Validate dien_tich
        if self.dien_tich_input.value() <= 0:
            errors.append("Diện tích phải lớn hơn 0")
        
        # Validate gia_thue
        if self.gia_thue_input.value() < 0:
            errors.append("Giá thuê không được âm")
        
        # Validate selected_kho
        if not self.selected_kho and not self.is_edit_mode:
            errors.append("Phải chọn kho")
        
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
                'ma_kho': self.selected_kho.ma_kho if self.selected_kho else self.vi_tri.ma_kho,
                'khu_vuc': self.khu_vuc_input.currentText().strip().upper(),
                'hang': self.hang_input.text().strip().zfill(2),
                'tang': self.tang_input.value(),
                'dien_tich': self.dien_tich_input.value(),
                'suc_chua': self.suc_chua_input.value(),
                'gia_thue': self.gia_thue_input.value(),
                'trang_thai': self.trang_thai_input.currentData()
            }
            
            if self.is_edit_mode:
                # Update existing
                vi_tri = self.vi_tri_service.update(self.vi_tri.ma_vi_tri, data)
                MessageDialog.success(self, "Thành công", f"Đã cập nhật vị trí {vi_tri.ma_vi_tri}")
            else:
                # Create new
                vi_tri = self.vi_tri_service.create(data)
                MessageDialog.success(self, "Thành công", f"Đã tạo vị trí {vi_tri.ma_vi_tri}")
            
            self.vi_tri_saved.emit(vi_tri)
            self.accept()
            
        except ValueError as e:
            MessageDialog.error(self, "Lỗi", str(e))
        except Exception as e:
            MessageDialog.error(self, "Lỗi", f"Không thể lưu vị trí:\n{str(e)}")


__all__ = ['ViTriForm']
