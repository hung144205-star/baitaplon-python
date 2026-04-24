#!/usr/bin/env python3
"""
Phiếu Nhập Form - Dialog nhập kho hàng hóa
"""
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QTextEdit, QDoubleSpinBox, QComboBox, QDialogButtonBox,
    QFormLayout, QFrame, QGroupBox, QSpinBox, QDateEdit, QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSignal, QDate
from datetime import datetime
from typing import Optional, Dict, Any

from src.services import HopDongService, HangHoaService
from src.models import HopDong
from src.gui.dialogs import MessageDialog
from src.utils.formatters import format_currency


class PhieuNhapForm(QDialog):
    """
    Dialog form để nhập kho hàng hóa (Phiếu nhập kho)
    """
    
    nhap_kho_complete = pyqtSignal(object)  # Emit HangHoa object
    
    def __init__(self, parent=None, hang_hoa: Optional = None):
        super().__init__(parent)
        self.hop_dong_service = HopDongService()
        self.hang_hoa_service = HangHoaService()
        self.hang_hoa = hang_hoa  # If provided, this is additional import
        self.setup_ui()
        self.setup_connections()
        self.load_hop_dongs()
        
        if self.hang_hoa:
            self.setWindowTitle("📥 Nhập thêm hàng")
            self.load_hang_hoa_info()
        else:
            self.setWindowTitle("📥 Phiếu Nhập Kho")
    
    def setup_ui(self):
        """Setup UI"""
        self.setMinimumWidth(600)
        self.setModal(True)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title = QLabel("📥 PHIẾU NHẬP KHO" if not self.hang_hoa else "📥 NHẬP THÊM HÀNG")
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
        
        # Contract selection (only for new imports)
        if not self.hang_hoa:
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
            form_layout.addRow("Hợp đồng:", self.hop_dong_selector)
        else:
            self.lbl_hop_dong_info = QLabel("")
            self.lbl_hop_dong_info.setStyleSheet("font-weight: 600; color: #1976d2;")
            form_layout.addRow("Hợp đồng:", self.lbl_hop_dong_info)
        
        # Goods info group
        goods_group = QGroupBox("📦 Thông tin hàng hóa")
        goods_group.setStyleSheet("""
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
        goods_layout = QFormLayout(goods_group)
        goods_layout.setSpacing(12)
        
        # Goods name
        if self.hang_hoa:
            self.lbl_ten_hang = QLabel(self.hang_hoa.ten_hang)
            self.lbl_ten_hang.setStyleSheet("font-weight: 600;")
            goods_layout.addRow("Tên hàng:", self.lbl_ten_hang)
        else:
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
            goods_layout.addRow("Tên hàng:", self.ten_hang_input)
        
        # Goods type
        if self.hang_hoa:
            self.lbl_loai_hang = QLabel(self.hang_hoa.loai_hang)
            goods_layout.addRow("Loại hàng:", self.lbl_loai_hang)
        else:
            self.loai_hang_input = QComboBox()
            self.loai_hang_input.setEditable(True)
            self.loai_hang_input.addItem("Điện tử", "Điện tử")
            self.loai_hang_input.addItem("May mặc", "May mặc")
            self.loai_hang_input.addItem("Thực phẩm", "Thực phẩm")
            self.loai_hang_input.addItem("Gia dụng", "Gia dụng")
            self.loai_hang_input.addItem("Khác", "Khác")
            self.loai_hang_input.setFixedWidth(200)
            self.loai_hang_input.setStyleSheet("""
                QComboBox {
                    padding: 8px;
                    border-radius: 4px;
                    border: 1px solid #bdbdbd;
                }
            """)
            goods_layout.addRow("Loại hàng:", self.loai_hang_input)
        
        form_layout.addRow(goods_group)
        
        # Quantity group
        qty_group = QGroupBox("📊 Số lượng")
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
        
        # Unit
        if self.hang_hoa:
            self.lbl_don_vi = QLabel(self.hang_hoa.don_vi)
            qty_layout.addRow("Đơn vị:", self.lbl_don_vi)
        else:
            self.don_vi_input = QComboBox()
            self.don_vi_input.setEditable(True)
            self.don_vi_input.addItem("cái", "cái")
            self.don_vi_input.addItem("thùng", "thùng")
            self.don_vi_input.addItem("hộp", "hộp")
            self.don_vi_input.addItem("kg", "kg")
            self.don_vi_input.addItem("lít", "lít")
            self.don_vi_input.addItem("mét", "mét")
            self.don_vi_input.setFixedWidth(200)
            self.don_vi_input.setStyleSheet("""
                QComboBox {
                    padding: 8px;
                    border-radius: 4px;
                    border: 1px solid #bdbdbd;
                }
            """)
            qty_layout.addRow("Đơn vị:", self.don_vi_input)
        
        form_layout.addRow(qty_group)
        
        # Value group
        value_group = QGroupBox("💰 Giá trị")
        value_group.setStyleSheet("""
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
        value_layout = QFormLayout(value_group)
        value_layout.setSpacing(12)
        
        # Value
        self.gia_tri_input = QDoubleSpinBox()
        self.gia_tri_input.setRange(0, 1000000000)
        self.gia_tri_input.setDecimals(0)
        self.gia_tri_input.setSuffix(" ₫")
        self.gia_tri_input.setValue(0)
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
        value_layout.addRow("Giá trị:", self.gia_tri_input)
        
        form_layout.addRow(value_group)
        
        # Date & Notes group
        info_group = QGroupBox("📝 Thông tin thêm")
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
        info_layout.addRow("Ngày nhập:", self.ngay_nhap_input)
        
        # Notes
        self.ghi_chu_input = QTextEdit()
        self.ghi_chu_input.setPlaceholderText("Ghi chú về lô hàng nhập...")
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
        
        # Buttons
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save |
            QDialogButtonBox.StandardButton.Cancel
        )
        button_box.button(QDialogButtonBox.StandardButton.Save).setText("💾 Nhập kho")
        button_box.button(QDialogButtonBox.StandardButton.Cancel).setText("❌ Hủy")
        button_box.setStyleSheet("""
            QPushButton {
                padding: 10px 20px;
                border-radius: 6px;
                font-weight: 600;
                font-size: 14px;
            }
            QPushButton[type="accept"] {
                background-color: #1aae39;
                color: white;
            }
            QPushButton[type="accept"]:hover {
                background-color: #157a2a;
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
        if not self.hang_hoa:
            self.hop_dong_selector.currentIndexChanged.connect(self._validate_form)
        self.so_luong_input.valueChanged.connect(self._validate_form)
        self.gia_tri_input.valueChanged.connect(self._validate_form)
    
    def load_hop_dongs(self):
        """Load contracts into selector"""
        if self.hang_hoa:
            return
        
        try:
            hop_dongs = self.hop_dong_service.get_all(limit=100)
            for hd in hop_dongs:
                display = f"{hd.ma_hop_dong} - {hd.ma_khach_hang}"
                self.hop_dong_selector.addItem(display, hd.ma_hop_dong)
        except Exception as e:
            MessageDialog.error(self, "Lỗi", f"Không thể tải hợp đồng:\n{str(e)}")
    
    def load_hang_hoa_info(self):
        """Load existing goods info"""
        if not self.hang_hoa:
            return
        
        # Show current stock
        current_stock = f"{self.hang_hoa.so_luong} {self.hang_hoa.don_vi}"
        stock_label = QLabel(f"⚠️ Tồn kho hiện tại: {current_stock}")
        stock_label.setStyleSheet("color: #ff9800; font-weight: 600; padding: 8px;")
        
        # Add to form (would need to refactor form_layout to insert)
        # For now, just display in title
    
    def _validate_form(self) -> bool:
        """Validate form fields"""
        errors = []
        
        if not self.hang_hoa:
            if not self.hop_dong_selector.currentData():
                errors.append("Phải chọn hợp đồng")
            if not self.ten_hang_input.text().strip():
                errors.append("Phải nhập tên hàng")
        
        if self.so_luong_input.value() <= 0:
            errors.append("Số lượng phải lớn hơn 0")
        
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
                    background-color: #1aae39;
                    color: white;
                }
                QPushButton:hover {
                    background-color: #157a2a;
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
                'so_luong': self.so_luong_input.value(),
                'gia_tri': self.gia_tri_input.value(),
                'ngay_nhap': self.ngay_nhap_input.date().toPyDate(),
                'ghi_chu': self.ghi_chu_input.toPlainText().strip()
            }
            
            if self.hang_hoa:
                # Import additional goods
                data['ma_hop_dong'] = self.hang_hoa.ma_hop_dong
                data['ten_hang'] = self.hang_hoa.ten_hang
                data['loai_hang'] = self.hang_hoa.loai_hang
                data['don_vi'] = self.hang_hoa.don_vi
                
                hang_hoa = self.hang_hoa_service.import_goods(data)
                MessageDialog.success(self, "Thành công", f"Đã nhập thêm {data['so_luong']} {self.hang_hoa.don_vi} {self.hang_hoa.ten_hang}")
            else:
                # New import
                data['ma_hop_dong'] = self.hop_dong_selector.currentData()
                data['ten_hang'] = self.ten_hang_input.text().strip()
                data['loai_hang'] = self.loai_hang_input.currentData()
                data['don_vi'] = self.don_vi_input.currentData()
                
                hang_hoa = self.hang_hoa_service.import_goods(data)
                MessageDialog.success(self, "Thành công", f"Đã nhập kho: {hang_hoa.ma_hang_hoa}")
            
            self.nhap_kho_complete.emit(hang_hoa)
            self.accept()
            
        except ValueError as e:
            MessageDialog.error(self, "Lỗi", str(e))
        except Exception as e:
            MessageDialog.error(self, "Lỗi", f"Không thể nhập kho:\n{str(e)}")


__all__ = ['PhieuNhapForm']
