#!/usr/bin/env python3
"""
User Form - Dialog thêm/sửa người dùng
"""
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QComboBox, QDialogButtonBox, QFormLayout, QFrame,
    QMessageBox, QTextEdit
)
from PyQt6.QtCore import Qt, pyqtSignal
from typing import Optional, Dict, Any

from src.models import NhanVien, TrangThaiNhanVienEnum
from src.services.users.user_service import UserService
from src.gui.dialogs import MessageDialog


class UserForm(QDialog):
    """
    Dialog form để thêm/sửa người dùng
    """
    
    user_saved = pyqtSignal(object)  # Emit NhanVien object when saved
    
    def __init__(self, parent=None, user: Optional[NhanVien] = None):
        super().__init__(parent)
        self.user_service = UserService()
        self.user = user
        self.is_edit_mode = user is not None
        self.setup_ui()
        self.setup_connections()
        
        if self.is_edit_mode:
            self.load_user_data()
            self.setWindowTitle("✏️ Chỉnh sửa người dùng")
        else:
            self.setWindowTitle("➕ Thêm người dùng mới")
    
    def setup_ui(self):
        """Setup UI"""
        self.setMinimumWidth(500)
        self.setModal(True)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title = QLabel("👤 THÔNG TIN NGƯỜI DÙNG" if self.is_edit_mode else "👤 THÊM NGƯỜI DÙNG MỚI")
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
        
        # Mã nhân viên (read-only if edit mode)
        self.ma_nhan_vien_input = QLineEdit()
        self.ma_nhan_vien_input.setPlaceholderText("Tự động tạo (NV202604001)")
        if self.is_edit_mode:
            self.ma_nhan_vien_input.setReadOnly(True)
            self.ma_nhan_vien_input.setText(self.user.ma_nhan_vien)
        self.ma_nhan_vien_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border-radius: 4px;
                border: 1px solid #bdbdbd;
            }
            QLineEdit:focus {
                border: 2px solid #1976d2;
            }
        """)
        form_layout.addRow("Mã nhân viên:", self.ma_nhan_vien_input)
        
        # Họ tên
        self.ho_ten_input = QLineEdit()
        self.ho_ten_input.setPlaceholderText("Nhập họ và tên đầy đủ")
        self.ho_ten_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border-radius: 4px;
                border: 1px solid #bdbdbd;
            }
            QLineEdit:focus {
                border: 2px solid #1976d2;
            }
        """)
        form_layout.addRow("Họ tên:", self.ho_ten_input)
        
        # Email
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("example@company.com")
        self.email_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border-radius: 4px;
                border: 1px solid #bdbdbd;
            }
            QLineEdit:focus {
                border: 2px solid #1976d2;
            }
        """)
        form_layout.addRow("Email:", self.email_input)
        
        # Số điện thoại
        self.sdt_input = QLineEdit()
        self.sdt_input.setPlaceholderText("090x xxx xxx")
        self.sdt_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border-radius: 4px;
                border: 1px solid #bdbdbd;
            }
            QLineEdit:focus {
                border: 2px solid #1976d2;
            }
        """)
        form_layout.addRow("Số điện thoại:", self.sdt_input)
        
        # Vai trò
        self.vai_tro_input = QComboBox()
        self.vai_tro_input.addItems([
            ("Admin", "admin"),
            ("Quản lý", "manager"),
            ("Nhân viên", "staff"),
            ("Khách", "guest")
        ])
        self.vai_tro_input.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border-radius: 4px;
                border: 1px solid #bdbdbd;
            }
            QComboBox:focus {
                border: 2px solid #1976d2;
            }
        """)
        form_layout.addRow("Vai trò:", self.vai_tro_input)
        
        # Trạng thái
        self.trang_thai_input = QComboBox()
        self.trang_thai_input.addItems([
            ("Hoạt động", TrangThaiNhanVienEnum.HOAT_DONG.value),
            ("Ngừng hoạt động", TrangThaiNhanVienEnum.NGUNG_HOAT_DONG.value)
        ])
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
        self.ghi_chu_input.setPlaceholderText("Ghi chú thêm về người dùng (nếu có)")
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
        button_box.accepted.connect(self._on_save_clicked)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
    
    def setup_connections(self):
        """Setup signal connections"""
        pass
    
    def load_user_data(self):
        """Load existing user data into form"""
        if not self.user:
            return
        
        self.ho_ten_input.setText(self.user.ho_ten or "")
        self.email_input.setText(self.user.email or "")
        self.sdt_input.setText(self.user.so_dien_thoai or "")
        
        # Set vai tro
        role_mapping = {
            'admin': 0,
            'manager': 1, 
            'staff': 2,
            'guest': 3
        }
        role_index = role_mapping.get(self.user.vai_tro, 2)  # Default to staff
        self.vai_tro_input.setCurrentIndex(role_index)
        
        # Set trang thai
        status_mapping = {
            TrangThaiNhanVienEnum.HOAT_DONG.value: 0,
            TrangThaiNhanVienEnum.NGUNG_HOAT_DONG.value: 1
        }
        status_index = status_mapping.get(self.user.trang_thai, 0)
        self.trang_thai_input.setCurrentIndex(status_index)
        
        self.ghi_chu_input.setPlainText(self.user.ghi_chu or "")
    
    def _validate_form(self) -> bool:
        """Validate form fields"""
        errors = []
        
        # Validate ho ten
        if not self.ho_ten_input.text().strip():
            errors.append("Họ tên không được để trống")
        
        # Validate email
        email = self.email_input.text().strip()
        if not email:
            errors.append("Email không được để trống")
        else:
            # Simple email validation
            if '@' not in email or '.' not in email:
                errors.append("Định dạng email không hợp lệ")
        
        # Validate vai tro
        if self.vai_tro_input.currentIndex() == -1:
            errors.append("Vui lòng chọn vai trò")
        
        if errors:
            MessageDialog(
                self,
                "Lỗi nhập liệu",
                "\n".join(errors),
                "error"
            ).exec()
            return False
        
        return True
    
    def _on_save_clicked(self):
        """Handle save button click"""
        if not self._validate_form():
            return
        
        try:
            # Prepare data
            data = {
                'ho_ten': self.ho_ten_input.text().strip(),
                'email': self.email_input.text().strip(),
                'so_dien_thoai': self.sdt_input.text().strip(),
                'vai_tro': self.vai_tro_input.currentData(),
                'trang_thai': self.trang_thai_input.currentData(),
                'ghi_chu': self.ghi_chu_input.toPlainText().strip()
            }
            
            if self.is_edit_mode:
                # Update existing user
                user = self.user_service.update_user(self.user.ma_nhan_vien, data)
                MessageDialog(
                    self,
                    "Thành công",
                    f"Đã cập nhật người dùng {user.ho_ten}",
                    "success"
                ).exec()
            else:
                # Create new user
                # Set default password as ma_nhan_vien
                data['mat_khau'] = self.ma_nhan_vien_input.text().strip() or "default123"
                user = self.user_service.create_user(data)
                MessageDialog(
                    self,
                    "Thành công", 
                    f"Đã tạo người dùng {user.ho_ten}\nMật khẩu mặc định: {data['mat_khau']}",
                    "success"
                ).exec()
            
            self.user_saved.emit(user)
            self.accept()
            
        except ValueError as e:
            MessageDialog(
                self,
                "Lỗi",
                str(e),
                "error"
            ).exec()
        except Exception as e:
            MessageDialog(
                self,
                "Lỗi",
                f"Không thể lưu người dùng:\n{str(e)}",
                "error"
            ).exec()


__all__ = ['UserForm']