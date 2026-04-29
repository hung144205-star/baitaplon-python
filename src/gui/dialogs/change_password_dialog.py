#!/usr/bin/env python3
"""
Change Password Dialog - Hộp thoại đổi mật khẩu
"""
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QWidget
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from src.gui.dialogs import MessageDialog
from src.services.auth.auth_service import AuthService


class ChangePasswordDialog(QDialog):
    """
    Dialog đổi mật khẩu người dùng
    """
    
    def __init__(self, parent=None, ma_nhan_vien: str = None):
        super().__init__(parent)
        self.ma_nhan_vien = ma_nhan_vien
        self.auth_service = AuthService()
        self.setup_ui()
    
    def setup_ui(self):
        """Setup UI"""
        self.setWindowTitle("🔐 Đổi mật khẩu")
        self.setMinimumWidth(420)
        self.setModal(True)
        
        self.setStyleSheet("""
            QDialog {
                background-color: #ffffff;
                border: 1px solid rgba(0, 0, 0, 0.1);
                border-radius: 12px;
            }
            QLabel {
                font-size: 14px;
                color: #31302e;
                font-weight: 500;
            }
            QLabel#titleLabel {
                font-size: 20px;
                font-weight: 700;
                color: #1976d2;
            }
            QLabel#descLabel {
                font-size: 13px;
                color: #615d59;
                font-weight: normal;
            }
            QLineEdit {
                padding: 10px 12px;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                font-size: 14px;
                background-color: #ffffff;
            }
            QLineEdit:focus {
                border-color: #1976d2;
            }
            QPushButton {
                border-radius: 8px;
                padding: 10px 20px;
                font-weight: 600;
                font-size: 14px;
            }
            QPushButton#primaryButton {
                background-color: #1976d2;
                color: white;
                border: none;
            }
            QPushButton#primaryButton:hover {
                background-color: #1565c0;
            }
            QPushButton#secondaryButton {
                background-color: transparent;
                color: #666;
                border: 1px solid #ddd;
            }
            QPushButton#secondaryButton:hover {
                background-color: #f5f5f5;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Title
        title = QLabel("🔐 Đổi mật khẩu")
        title.setObjectName("titleLabel")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Description
        desc = QLabel("Vui lòng nhập mật khẩu cũ và mật khẩu mới")
        desc.setObjectName("descLabel")
        desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(desc)
        
        # Form fields
        form_widget = QWidget()
        form_layout = QVBoxLayout(form_widget)
        form_layout.setSpacing(16)
        form_layout.setContentsMargins(0, 0, 0, 0)
        
        # Old password
        old_password_label = QLabel("Mật khẩu cũ")
        form_layout.addWidget(old_password_label)
        
        self.old_password_input = QLineEdit()
        self.old_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.old_password_input.setPlaceholderText("Nhập mật khẩu hiện tại")
        form_layout.addWidget(self.old_password_input)
        
        # New password
        new_password_label = QLabel("Mật khẩu mới")
        form_layout.addWidget(new_password_label)
        
        self.new_password_input = QLineEdit()
        self.new_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.new_password_input.setPlaceholderText("Nhập mật khẩu mới")
        form_layout.addWidget(self.new_password_input)
        
        # Confirm new password
        confirm_password_label = QLabel("Xác nhận mật khẩu mới")
        form_layout.addWidget(confirm_password_label)
        
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.confirm_password_input.setPlaceholderText("Nhập lại mật khẩu mới")
        form_layout.addWidget(self.confirm_password_input)
        
        # Password requirements hint
        hint = QLabel("Mật khẩu mới phải có ít nhất 8 ký tự, bao gồm chữ hoa, chữ thường và số")
        hint.setStyleSheet("""
            QLabel {
                font-size: 12px;
                color: #9e9e9e;
                font-weight: normal;
            }
        """)
        form_layout.addWidget(hint)
        
        layout.addWidget(form_widget)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(12)
        
        cancel_btn = QPushButton("Hủy")
        cancel_btn.setObjectName("secondaryButton")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        change_btn = QPushButton("Đổi mật khẩu")
        change_btn.setObjectName("primaryButton")
        change_btn.clicked.connect(self._on_change_password)
        button_layout.addWidget(change_btn)
        
        layout.addLayout(button_layout)
    
    def _on_change_password(self):
        """Handle change password"""
        old_password = self.old_password_input.text()
        new_password = self.new_password_input.text()
        confirm_password = self.confirm_password_input.text()
        
        # Validation
        if not old_password:
            MessageDialog.warning(self, "Cảnh báo", "Vui lòng nhập mật khẩu cũ")
            self.old_password_input.setFocus()
            return
        
        if not new_password:
            MessageDialog.warning(self, "Cảnh báo", "Vui lòng nhập mật khẩu mới")
            self.new_password_input.setFocus()
            return
        
        if len(new_password) < 8:
            MessageDialog.warning(self, "Cảnh báo", "Mật khẩu mới phải có ít nhất 8 ký tự")
            self.new_password_input.setFocus()
            return
        
        if new_password != confirm_password:
            MessageDialog.warning(self, "Cảnh báo", "Mật khẩu mới không khớp với xác nhận")
            self.confirm_password_input.setFocus()
            return
        
        if old_password == new_password:
            MessageDialog.warning(self, "Cảnh báo", "Mật khẩu mới phải khác mật khẩu cũ")
            self.new_password_input.setFocus()
            return
        
        # Call auth service
        result = self.auth_service.change_password(
            self.ma_nhan_vien,
            old_password,
            new_password
        )
        
        if result['success']:
            MessageDialog.success(self, "Thành công", "Đổi mật khẩu thành công!")
            self.accept()
        else:
            MessageDialog.error(self, "Lỗi", result['message'])
    
    @staticmethod
    def show_dialog(parent=None, ma_nhan_vien: str = None) -> bool:
        """
        Show change password dialog
        
        Args:
            parent: Parent widget
            ma_nhan_vien: Mã nhân viên
            
        Returns:
            True if password was changed
        """
        dialog = ChangePasswordDialog(parent, ma_nhan_vien)
        return dialog.exec() == QDialog.DialogCode.Accepted


__all__ = ['ChangePasswordDialog']
