#!/usr/bin/env python3
"""
Hàng hóa Form - Dialog thêm/sửa hàng hóa
"""
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QTextEdit, QDoubleSpinBox, QComboBox, QDialogButtonBox,
    QFormLayout, QFrame, QGroupBox, QSpinBox, QDateEdit,
    QMessageBox, QPushButton, QFileDialog
)
from PyQt6.QtCore import Qt, pyqtSignal, QDate
from datetime import datetime
from typing import Optional, Dict, Any, List

from src.services import HopDongService, HangHoaService, ViTriService
from src.models import HopDong, ViTri, HangHoa
from src.gui.dialogs import MessageDialog
from src.utils.formatters import format_currency


class HangHoaForm(QDialog):
    """
    Dialog form để thêm/sửa hàng hóa
    """
    
    hang_hoa_saved = pyqtSignal(object)  # Emit HangHoa object
    
    def __init__(self, parent=None, hang_hoa: Optional[HangHoa] = None):
        super().__init__(parent)
        self.hop_dong_service = HopDongService()
        self.hang_hoa_service = HangHoaService()
        self.vi_tri_service = ViTriService()
        self.hang_hoa = hang_hoa
        self.is_edit_mode = hang_hoa is not None
        self.setup_ui()
        self.setup_connections()
        self.load_hop_dongs()
        self.load_vi_tris()
        
        if self.is_edit_mode:
            self.load_hang_hoa_data()
            self.setWindowTitle("✏️ Chỉnh sửa hàng hóa")
        else:
            self.setWindowTitle("➕ Thêm hàng hóa mới")
    
    def setup_ui(self):
        """Setup UI"""
        self.setMinimumWidth(650)
        self.setModal(True)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title = QLabel("📦 THÔNG TIN HÀNG HÓA" if self.is_edit_mode else "📦 THÊM HÀNG HÓA MỚI")
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
        
        # Basic info group
        basic_group = QGroupBox("📄 Thông tin cơ bản")
        basic_group.setStyleSheet("""
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
        basic_layout = QFormLayout(basic_group)
        basic_layout.setSpacing(12)
        
        # Contract selection
        self.hop_dong_selector = QComboBox()
        self.hop_dong_selector.addItem("-- Chọn hợp đồng --", None)
        self.hop_dong_selector.setFixedWidth(300)
        self.hop_dong_selector.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border-radius: 4px;
                border: 1px solid #bdbdbd;
            }
            QComboBox:focus {
                border: 2px solid #1976d2;
            }
        """)
        basic_layout.addRow("Hợp đồng:", self.hop_dong_selector)
        
        # Goods name
        self.ten_hang_input = QLineEdit()
        self.ten_hang_input.setPlaceholderText("Tên hàng hóa")
        self.ten_hang_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border-radius: 4px;
                border: 1px solid #bdbdbd;
            }
            QLineEdit:focus {
                border: 2px solid #1976d2;
            }
        """)
        basic_layout.addRow("Tên hàng:", self.ten_hang_input)
        
        # Goods type
        self.loai_hang_input = QComboBox()
        self.loai_hang_input.setEditable(True)
        self.loai_hang_input.addItem("Điện tử", "Điện tử")
        self.loai_hang_input.addItem("May mặc", "May mặc")
        self.loai_hang_input.addItem("Thực phẩm", "Thực phẩm")
        self.loai_hang_input.addItem("Gia dụng", "Gia dụng")
        self.loai_hang_input.addItem("Nguyên liệu", "Nguyên liệu")
        self.loai_hang_input.addItem("Khác", "Khác")
        self.loai_hang_input.setFixedWidth(200)
        self.loai_hang_input.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border-radius: 4px;
                border: 1px solid #bdbdbd;
            }
            QComboBox:focus {
                border: 2px solid #1976d2;
            }
        """)
        basic_layout.addRow("Loại hàng:", self.loai_hang_input)
        
        form_layout.addRow(basic_group)
        
        # Quantity group
        qty_group = QGroupBox("📊 Số lượng & Đơn vị")
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
        
        # Quantity
        self.so_luong_input = QSpinBox()
        self.so_luong_input.setRange(0, 1000000)
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
        
        # Unit
        self.don_vi_input = QComboBox()
        self.don_vi_input.setEditable(True)
        self.don_vi_input.addItem("cái", "cái")
        self.don_vi_input.addItem("thùng", "thùng")
        self.don_vi_input.addItem("hộp", "hộp")
        self.don_vi_input.addItem("kg", "kg")
        self.don_vi_input.addItem("lít", "lít")
        self.don_vi_input.addItem("mét", "mét")
        self.don_vi_input.addItem("cuộn", "cuộn")
        self.don_vi_input.addItem("bao", "bao")
        self.don_vi_input.setFixedWidth(200)
        self.don_vi_input.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border-radius: 4px;
                border: 1px solid #bdbdbd;
            }
            QComboBox:focus {
                border: 2px solid #1976d2;
            }
        """)
        qty_layout.addRow("Đơn vị:", self.don_vi_input)
        
        form_layout.addRow(qty_group)
        
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
        """)
        spec_layout = QFormLayout(spec_group)
        spec_layout.setSpacing(12)
        
        # Weight
        self.trong_luong_input = QDoubleSpinBox()
        self.trong_luong_input.setRange(0, 10000)
        self.trong_luong_input.setDecimals(2)
        self.trong_luong_input.setSuffix(" kg")
        self.trong_luong_input.setValue(0.0)
        self.trong_luong_input.setStyleSheet("""
            QDoubleSpinBox {
                padding: 8px;
                border-radius: 4px;
                border: 1px solid #bdbdbd;
            }
            QDoubleSpinBox:focus {
                border: 2px solid #1976d2;
            }
        """)
        spec_layout.addRow("Trọng lượng:", self.trong_luong_input)
        
        # Dimensions
        self.kich_thuoc_input = QLineEdit()
        self.kich_thuoc_input.setPlaceholderText("Dài x Rộng x Cao (cm)")
        self.kich_thuoc_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border-radius: 4px;
                border: 1px solid #bdbdbd;
            }
            QLineEdit:focus {
                border: 2px solid #1976d2;
            }
        """)
        spec_layout.addRow("Kích thước:", self.kich_thuoc_input)
        
        # Value
        self.gia_tri_input = QDoubleSpinBox()
        self.gia_tri_input.setRange(0, 1000000000)
        self.gia_tri_input.setDecimals(0)
        self.gia_tri_input.setSuffix(" ₫")
        self.gia_tri_input.setValue(0.0)
        self.gia_tri_input.setStyleSheet("""
            QDoubleSpinBox {
                padding: 8px;
                border-radius: 4px;
                border: 1px solid #bdbdbd;
            }
            QDoubleSpinBox:focus {
                border: 2px solid #1976d2;
            }
        """)
        spec_layout.addRow("Giá trị:", self.gia_tri_input)
        
        form_layout.addRow(spec_group)
        
        # Storage group
        storage_group = QGroupBox("📍 Vị trí lưu trữ")
        storage_group.setStyleSheet("""
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
        storage_layout = QFormLayout(storage_group)
        storage_layout.setSpacing(12)
        
        # Storage position
        self.vi_tri_input = QComboBox()
        self.vi_tri_input.addItem("-- Chọn vị trí --", None)
        self.vi_tri_input.setFixedWidth(300)
        self.vi_tri_input.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border-radius: 4px;
                border: 1px solid #bdbdbd;
            }
            QComboBox:focus {
                border: 2px solid #1976d2;
            }
        """)
        storage_layout.addRow("Vị trí:", self.vi_tri_input)
        
        # Import date
        self.ngay_nhap_input = QDateEdit()
        self.ngay_nhap_input.setCalendarPopup(True)
        self.ngay_nhap_input.setDate(QDate.currentDate())
        self.ngay_nhap_input.setFixedWidth(150)
        self.ngay_nhap_input.setStyleSheet("""
            QDateEdit {
                padding: 8px;
                border-radius: 4px;
                border: 1px solid #bdbdbd;
            }
        """)
        storage_layout.addRow("Ngày nhập:", self.ngay_nhap_input)
        
        form_layout.addRow(storage_group)
        
        # Image upload
        image_group = QGroupBox("📷 Hình ảnh")
        image_group.setStyleSheet("""
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
        image_layout = QVBoxLayout(image_group)
        image_layout.setSpacing(8)
        
        self.hinh_anh_paths: List[str] = []
        self.hinh_anh_label = QLabel("Chưa có hình ảnh")
        self.hinh_anh_label.setStyleSheet("color: #757575; padding: 8px;")
        image_layout.addWidget(self.hinh_anh_label)
        
        image_btn_layout = QHBoxLayout()
        
        upload_btn = QPushButton("📷 Thêm hình")
        upload_btn.setStyleSheet("""
            QPushButton {
                background-color: #1976d2;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #1565c0;
            }
        """)
        upload_btn.clicked.connect(self._upload_image)
        image_btn_layout.addWidget(upload_btn)
        
        image_btn_layout.addStretch()
        
        image_layout.addLayout(image_btn_layout)
        
        form_layout.addRow(image_group)
        
        # Notes
        self.ghi_chu_input = QTextEdit()
        self.ghi_chu_input.setPlaceholderText("Ghi chú thêm về hàng hóa...")
        self.ghi_chu_input.setMaximumHeight(80)
        self.ghi_chu_input.setStyleSheet("""
            QTextEdit {
                padding: 8px;
                border-radius: 4px;
                border: 1px solid #bdbdbd;
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
        self.hop_dong_selector.currentIndexChanged.connect(self._validate_form)
        self.ten_hang_input.textChanged.connect(self._validate_form)
        self.so_luong_input.valueChanged.connect(self._validate_form)
        self.gia_tri_input.valueChanged.connect(self._validate_form)
    
    def load_hop_dongs(self):
        """Load contracts into selector"""
        try:
            hop_dongs = self.hop_dong_service.get_all(limit=100)
            for hd in hop_dongs:
                display = f"{hd.ma_hop_dong} - {hd.ma_khach_hang}"
                self.hop_dong_selector.addItem(display, hd.ma_hop_dong)
        except Exception as e:
            MessageDialog.error(self, "Lỗi", f"Không thể tải hợp đồng:\n{str(e)}")
    
    def load_vi_tris(self):
        """Load storage positions"""
        try:
            vi_tris = self.vi_tri_service.get_all(limit=100)
            for vt in vi_tris:
                if str(vt.trang_thai) == 'trong':
                    display = f"{vt.ma_vi_tri} - KV:{vt.khu_vuc} H:{vt.hang} T:{vt.tang}"
                    self.vi_tri_input.addItem(display, vt.ma_vi_tri)
        except Exception as e:
            print(f"Error loading positions: {e}")
    
    def load_hang_hoa_data(self):
        """Load existing goods data"""
        if not self.hang_hoa:
            return
        
        # Set contract
        for i in range(self.hop_dong_selector.count()):
            if self.hop_dong_selector.itemData(i) == self.hang_hoa.ma_hop_dong:
                self.hop_dong_selector.setCurrentIndex(i)
                break
        
        self.ten_hang_input.setText(self.hang_hoa.ten_hang)
        self.loai_hang_input.setCurrentText(self.hang_hoa.loai_hang)
        self.so_luong_input.setValue(self.hang_hoa.so_luong)
        self.don_vi_input.setCurrentText(self.hang_hoa.don_vi)
        self.trong_luong_input.setValue(self.hang_hoa.trong_luong or 0.0)
        self.kich_thuoc_input.setText(self.hang_hoa.kich_thuoc or '')
        self.gia_tri_input.setValue(self.hang_hoa.gia_tri or 0.0)
        
        # Set storage position
        if self.hang_hoa.vi_tri_luu_tru:
            for i in range(self.vi_tri_input.count()):
                if self.vi_tri_input.itemData(i) == self.hang_hoa.vi_tri_luu_tru:
                    self.vi_tri_input.setCurrentIndex(i)
                    break
        
        # Set import date
        if self.hang_hoa.ngay_nhap:
            self.ngay_nhap_input.setDate(QDate(
                self.hang_hoa.ngay_nhap.year,
                self.hang_hoa.ngay_nhap.month,
                self.hang_hoa.ngay_nhap.day
            ))
        
        # Set images
        import json
        try:
            self.hinh_anh_paths = json.loads(self.hang_hoa.hinh_anh or '[]')
            if self.hinh_anh_paths:
                self.hinh_anh_label.setText(f"Đã có {len(self.hinh_anh_paths)} hình ảnh")
        except:
            self.hinh_anh_paths = []
        
        # Set notes
        self.ghi_chu_input.setPlainText(self.hang_hoa.ghi_chu or '')
        
        self._validate_form()
    
    def _upload_image(self):
        """Upload image file"""
        file_paths, _ = QFileDialog.getOpenFileNames(
            self,
            "Chọn hình ảnh",
            "",
            "Image Files (*.png *.jpg *.jpeg *.gif *.webp)"
        )
        
        if file_paths:
            self.hinh_anh_paths.extend(file_paths)
            self.hinh_anh_label.setText(f"Đã có {len(self.hinh_anh_paths)} hình ảnh")
    
    def _validate_form(self) -> bool:
        """Validate form fields"""
        errors = []
        
        if not self.hop_dong_selector.currentData():
            errors.append("Phải chọn hợp đồng")
        
        if not self.ten_hang_input.text().strip():
            errors.append("Phải nhập tên hàng")
        
        if self.so_luong_input.value() < 0:
            errors.append("Số lượng không được âm")
        
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
            import json
            data = {
                'ma_hop_dong': self.hop_dong_selector.currentData(),
                'ten_hang': self.ten_hang_input.text().strip(),
                'loai_hang': self.loai_hang_input.currentData(),
                'so_luong': self.so_luong_input.value(),
                'don_vi': self.don_vi_input.currentData(),
                'trong_luong': self.trong_luong_input.value() if self.trong_luong_input.value() > 0 else None,
                'kich_thuoc': self.kich_thuoc_input.text().strip() or None,
                'gia_tri': self.gia_tri_input.value(),
                'vi_tri_luu_tru': self.vi_tri_input.currentData(),
                'ngay_nhap': self.ngay_nhap_input.date().toPyDate(),
                'ghi_chu': self.ghi_chu_input.toPlainText().strip(),
                'hinh_anh': json.dumps(self.hinh_anh_paths)
            }
            
            if self.is_edit_mode:
                # Update existing
                hang_hoa = self.hang_hoa_service.update(self.hang_hoa.ma_hang_hoa, data)
                MessageDialog.success(self, "Thành công", f"Đã cập nhật hàng hóa {hang_hoa.ma_hang_hoa}")
            else:
                # Create new
                hang_hoa = self.hang_hoa_service.create(data)
                MessageDialog.success(self, "Thành công", f"Đã tạo hàng hóa {hang_hoa.ma_hang_hoa}")
            
            self.hang_hoa_saved.emit(hang_hoa)
            self.accept()
            
        except ValueError as e:
            MessageDialog.error(self, "Lỗi", str(e))
        except Exception as e:
            MessageDialog.error(self, "Lỗi", f"Không thể lưu hàng hóa:\n{str(e)}")


__all__ = ['HangHoaForm']
