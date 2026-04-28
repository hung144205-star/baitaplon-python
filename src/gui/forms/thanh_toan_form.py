#!/usr/bin/env python3
"""
Thanh toán Form - Form nhập liệu Thanh toán
"""
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QComboBox, QTextEdit, QDateEdit, QPushButton, QFrame,
    QFormLayout, QMessageBox, QDoubleSpinBox, QSpinBox
)
from PyQt6.QtCore import Qt, QDate, pyqtSignal
from PyQt6.QtGui import QFont

from src.gui.dialogs import MessageDialog


class ThanhToanForm(QDialog):
    """
    Form nhập liệu Thanh toán (Thêm/Sửa)
    """
    
    accepted_with_data = pyqtSignal(dict)
    
    def __init__(self, parent=None, thanh_toan=None):
        """
        Args:
            parent: Parent widget
            thanh_toan: ThanhToan object to edit (None if adding new)
        """
        super().__init__(parent)
        self.thanh_toan = thanh_toan
        self.is_edit_mode = thanh_toan is not None
        self.setup_ui()
        self.setup_connections()
        
        if self.is_edit_mode:
            self._load_data()
        else:
            self._set_defaults()
    
    def setup_ui(self):
        """Setup UI"""
        self.setWindowTitle("Thêm Thanh toán" if not self.is_edit_mode else "Sửa Thanh toán")
        self.setMinimumWidth(600)
        self.setMinimumHeight(600)
        self.setModal(True)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Title
        title = QLabel("💰 THÔNG TIN THANH TOÁN" if not self.is_edit_mode else "✏️ CẬP NHẬT THANH TOÁN")
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
        
        # Mã thanh toán (auto-generate, read-only)
        self.ma_tt_label = QLabel("Mã thanh toán:")
        self.ma_tt_input = QLineEdit()
        self.ma_tt_input.setReadOnly(True)
        self.ma_tt_input.setStyleSheet("""
            QLineEdit:read-only {
                background-color: #f6f5f4;
                color: #615d59;
            }
        """)
        form_layout.addRow(self.ma_tt_label, self.ma_tt_input)
        
        # Hợp đồng (required)
        self.hop_dong_label = QLabel("Hợp đồng <span style='color: #d32f2f;'>*</span>:")
        self.hop_dong_input = QComboBox()
        self.hop_dong_input.setEditable(True)
        self.hop_dong_input.lineEdit().setPlaceholderText("Chọn hoặc nhập mã hợp đồng")
        self._load_contracts()
        form_layout.addRow(self.hop_dong_label, self.hop_dong_input)
        
        # Kỳ thanh toán
        self.ky_tt_label = QLabel("Kỳ thanh toán:")
        self.ky_tt_input = QLineEdit()
        self.ky_tt_input.setPlaceholderText("Ví dụ: Kỳ 1/2026")
        form_layout.addRow(self.ky_tt_label, self.ky_tt_input)
        
        # Số tiền (required)
        self.so_tien_label = QLabel("Số tiền <span style='color: #d32f2f;'>*</span>:")
        self.so_tien_input = QDoubleSpinBox()
        self.so_tien_input.setRange(0, 999999999)
        self.so_tien_input.setDecimals(0)
        self.so_tien_input.setSuffix(" đ")
        self.so_tien_input.setStyleSheet("padding: 8px;")
        form_layout.addRow(self.so_tien_label, self.so_tien_input)
        
        # Ngày đến hạn (required)
        self.ngay_den_han_label = QLabel("Ngày đến hạn <span style='color: #d32f2f;'>*</span>:")
        self.ngay_den_han_input = QDateEdit()
        self.ngay_den_han_input.setCalendarPopup(True)
        self.ngay_den_han_input.setDate(QDate.currentDate())
        self.ngay_den_han_input.setStyleSheet("padding: 8px;")
        form_layout.addRow(self.ngay_den_han_label, self.ngay_den_han_input)
        
        # Ngày thanh toán
        self.ngay_tt_label = QLabel("Ngày thanh toán:")
        self.ngay_tt_input = QDateEdit()
        self.ngay_tt_input.setCalendarPopup(True)
        self.ngay_tt_input.setStyleSheet("padding: 8px;")
        self.ngay_tt_input.setEnabled(False)  # Disabled until marked as paid
        form_layout.addRow(self.ngay_tt_label, self.ngay_tt_input)
        
        # Trạng thái
        self.trang_thai_label = QLabel("Trạng thái:")
        self.trang_thai_input = QComboBox()
        self.trang_thai_input.addItem("Chưa thanh toán", "chua_thanh_toan")
        self.trang_thai_input.addItem("Đã thanh toán", "da_thanh_toan")
        self.trang_thai_input.addItem("Quá hạn", "qua_han")
        form_layout.addRow(self.trang_thai_label, self.trang_thai_input)
        
        # Phương thức thanh toán
        self.phuong_thuc_label = QLabel("Phương thức thanh toán:")
        self.phuong_thuc_input = QComboBox()
        self.phuong_thuc_input.addItem("Tiền mặt", "tien_mat")
        self.phuong_thuc_input.addItem("Chuyển khoản", "chuyen_khoan")
        self.phuong_thuc_input.addItem("Ví điện tử", "vi_dien_tu")
        self.phuong_thuc_input.addItem("Khác", "khac")
        form_layout.addRow(self.phuong_thuc_label, self.phuong_thuc_input)
        
        # Số giao dịch
        self.so_gd_label = QLabel("Số giao dịch:")
        self.so_gd_input = QLineEdit()
        self.so_gd_input.setPlaceholderText("Số bill, mã giao dịch...")
        form_layout.addRow(self.so_gd_label, self.so_gd_input)
        
        # Người thu
        self.nguoi_thu_label = QLabel("Người thu:")
        self.nguoi_thu_input = QLineEdit()
        self.nguoi_thu_input.setPlaceholderText("Tên người thu tiền")
        form_layout.addRow(self.nguoi_thu_label, self.nguoi_thu_input)
        
        # Ghi chú
        self.ghi_chu_label = QLabel("Ghi chú:")
        self.ghi_chu_input = QTextEdit()
        self.ghi_chu_input.setPlaceholderText("Nhập ghi chú (nếu có)")
        self.ghi_chu_input.setMaximumHeight(80)
        form_layout.addRow(self.ghi_chu_label, self.ghi_chu_input)
        
        layout.addWidget(form_container)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        cancel_btn = QPushButton("Hủy")
        cancel_btn.setFixedWidth(100)
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #f5f5f5;
                color: #666;
                border: 1px solid #ddd;
                border-radius: 6px;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
        """)
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        save_btn = QPushButton("Lưu")
        save_btn.setFixedWidth(100)
        save_btn.setObjectName("primaryButton")
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #005db2;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #00468a;
            }
        """)
        save_btn.clicked.connect(self._on_save)
        button_layout.addWidget(save_btn)
        
        layout.addLayout(button_layout)
    
    def _load_contracts(self):
        """Load contracts into combobox"""
        try:
            from src.database import get_session
            from src.models import HopDong, KhachHang
            
            session = get_session()
            
            # Get active contracts
            hop_dongs = session.query(HopDong).filter(
                HopDong.trang_thai == 'hieu_luc'
            ).all()
            
            for hd in hop_dongs:
                kh = session.query(KhachHang).filter(KhachHang.ma_khach_hang == hd.ma_khach_hang).first()
                kh_name = kh.ho_ten if kh else "N/A"
                self.hop_dong_input.addItem(
                    f"{hd.ma_hop_dong} - {kh_name}",
                    hd.ma_hop_dong
                )
            
            session.close()
        except Exception as e:
            print(f"Error loading contracts: {e}")
    
    def setup_connections(self):
        """Setup signal connections"""
        self.trang_thai_input.currentIndexChanged.connect(self._on_status_changed)
        self.hop_dong_input.currentIndexChanged.connect(self._on_contract_changed)
    
    def _on_status_changed(self, index):
        """Handle status change"""
        status = self.trang_thai_input.currentData()
        if status == "da_thanh_toan":
            self.ngay_tt_input.setEnabled(True)
            if self.ngay_tt_input.date() == QDate(1900, 1, 1):
                self.ngay_tt_input.setDate(QDate.currentDate())
        else:
            self.ngay_tt_input.setEnabled(False)
            self.ngay_tt_input.setDate(QDate(1900, 1, 1))
    
    def _on_contract_changed(self, index):
        """Handle contract selection - auto-fill amount"""
        if not self.is_edit_mode and index >= 0:
            ma_hop_dong = self.hop_dong_input.currentData()
            if ma_hop_dong:
                try:
                    from src.database import get_session
                    from src.models import HopDong
                    
                    session = get_session()
                    hop_dong = session.query(HopDong).filter(
                        HopDong.ma_hop_dong == ma_hop_dong
                    ).first()
                    
                    if hop_dong:
                        self.so_tien_input.setValue(hop_dong.gia_thue)
                    
                    session.close()
                except Exception as e:
                    print(f"Error loading contract: {e}")
    
    def _set_defaults(self):
        """Set default values for new payment"""
        self.ma_tt_input.setText("(Tự động)")
        self.ngay_tt_input.setDate(QDate(1900, 1, 1))
    
    def _load_data(self):
        """Load existing payment data"""
        if not self.thanh_toan:
            return
        
        tt = self.thanh_toan
        
        self.ma_tt_input.setText(tt.ma_thanh_toan)
        
        # Set contract
        for i in range(self.hop_dong_input.count()):
            if self.hop_dong_input.itemData(i) == tt.ma_hop_dong:
                self.hop_dong_input.setCurrentIndex(i)
                break
        
        self.ky_tt_input.setText(tt.ky_thanh_toan or "")
        self.so_tien_input.setValue(tt.so_tien or 0)
        
        if tt.ngay_den_han:
            from datetime import date
            d = tt.ngay_den_han
            if isinstance(d, date):
                self.ngay_den_han_input.setDate(QDate(d.year, d.month, d.day))
            else:
                self.ngay_den_han_input.setDate(QDate.currentDate())
        
        if tt.ngay_thanh_toan:
            from datetime import date
            d = tt.ngay_thanh_toan
            if isinstance(d, date):
                self.ngay_tt_input.setDate(QDate(d.year, d.month, d.day))
                self.ngay_tt_input.setEnabled(True)
        
        # Set status
        status = tt.trang_thai.value if hasattr(tt.trang_thai, 'value') else str(tt.trang_thai)
        for i in range(self.trang_thai_input.count()):
            if self.trang_thai_input.itemData(i) == status:
                self.trang_thai_input.setCurrentIndex(i)
                break
        
        # Set payment method
        phuong_thuc = tt.phuong_thuc or "tien_mat"
        for i in range(self.phuong_thuc_input.count()):
            if self.phuong_thuc_input.itemData(i) == phuong_thuc:
                self.phuong_thuc_input.setCurrentIndex(i)
                break
        
        self.so_gd_input.setText(tt.so_giao_dich or "")
        self.nguoi_thu_input.setText(tt.nguoi_thu or "")
        self.ghi_chu_input.setPlainText(tt.ghi_chu or "")
    
    def _on_save(self):
        """Handle save button click"""
        # Validate required fields
        if self.hop_dong_input.currentData() is None:
            MessageDialog.warning(self, "Cảnh báo", "Vui lòng chọn hợp đồng")
            return
        
        so_tien = self.so_tien_input.value()
        if so_tien <= 0:
            MessageDialog.warning(self, "Cảnh báo", "Số tiền phải lớn hơn 0")
            return
        
        ngay_den_han = self.ngay_den_han_input.date().toPyDate()
        
        # Build data dict
        data = {
            'ma_hop_dong': self.hop_dong_input.currentData(),
            'ky_thanh_toan': self.ky_tt_input.text().strip() or None,
            'so_tien': so_tien,
            'ngay_den_han': ngay_den_han,
            'trang_thai': self.trang_thai_input.currentData(),
            'phuong_thuc': self.phuong_thuc_input.currentData(),
            'so_giao_dich': self.so_gd_input.text().strip() or None,
            'nguoi_thu': self.nguoi_thu_input.text().strip() or None,
            'ghi_chu': self.ghi_chu_input.toPlainText().strip() or None,
        }
        
        # Handle payment date
        ngay_tt_date = self.ngay_tt_input.date()
        if ngay_tt_date.year() != 1900 and self.trang_thai_input.currentData() == "da_thanh_toan":
            data['ngay_thanh_toan'] = ngay_tt_date.toPyDate()
        else:
            data['ngay_thanh_toan'] = None
        
        self.accepted_with_data.emit(data)
        self.accept()
    
    def get_form_data(self) -> dict:
        """Get form data (for external access)"""
        return self._get_data()


__all__ = ['ThanhToanForm']
