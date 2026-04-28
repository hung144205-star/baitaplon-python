#!/usr/bin/env python3
"""
Login View - Giao diện đăng nhập hệ thống
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QFrame, QMessageBox, QCheckBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPixmap, QFont

from src.services.auth.auth_service import login, AuthStatus
from src.gui.dialogs import MessageDialog


class LoginView(QWidget):
    """
    Giao diện đăng nhập hệ thống
    """
    
    # Signals
    login_successful = pyqtSignal(dict)  # Emit user info when login successful
    login_cancelled = pyqtSignal()      # Emit when user cancels login
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.setup_connections()
    
    def setup_ui(self):
        """Setup UI"""
        self.setWindowTitle("🔐 Đăng nhập hệ thống")
        self.setFixedSize(400, 500)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(24)
        
        # Logo/Title
        title_container = QHBoxLayout()
        title_container.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        title_label = QLabel("QUẢN LÝ KHO LƯU TRỮ")
        title_label.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: #1976d2;
                margin-bottom: 8px;
            }
        """)
        title_container.addWidget(title_label)
        layout.addLayout(title_container)
        
        subtitle_label = QLabel("Đăng nhập để tiếp tục")
        subtitle_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #666;
                margin-bottom: 32px;
            }
        """)
        layout.addWidget(subtitle_label, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Login form container
        form_container = QFrame()
        form_container.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 12px;
                padding: 24px;
                border: 1px solid #e0e0e0;
            }
        """)
        form_layout = QVBoxLayout(form_container)
        form_layout.setSpacing(20)
        
        # Username field
        username_label = QLabel("Tên đăng nhập:")
        username_label.setStyleSheet("font-weight: bold; color: #333;")
        form_layout.addWidget(username_label)
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Nhập mã nhân viên hoặc email")
        self.username_input.setStyleSheet("""
            QLineEdit {
                padding: 12px;
                border: 1px solid #ddd;
                border-radius: 6px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: #1976d2;
                outline: none;
            }
        """)
        form_layout.addWidget(self.username_input)
        
        # Password field
        password_label = QLabel("Mật khẩu:")
        password_label.setStyleSheet("font-weight: bold; color: #333;")
        form_layout.addWidget(password_label)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Nhập mật khẩu")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setStyleSheet("""
            QLineEdit {
                padding: 12px;
                border: 1px solid #ddd;
                border-radius: 6px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: #1976d2;
                outline: none;
            }
        """)
        form_layout.addWidget(self.password_input)
        
        # Remember me and Forgot password
        options_layout = QHBoxLayout()
        options_layout.setSpacing(16)
        
        self.remember_checkbox = QCheckBox("Ghi nhớ đăng nhập")
        self.remember_checkbox.setStyleSheet("""
            QCheckBox {
                color: #666;
                font-size: 12px;
            }
        """)
        options_layout.addWidget(self.remember_checkbox)
        
        options_layout.addStretch()
        
        self.forgot_password_link = QPushButton("Quên mật khẩu?")
        self.forgot_password_link.setStyleSheet("""
            QPushButton {
                color: #1976d2;
                text-decoration: underline;
                border: none;
                background: transparent;
                font-size: 12px;
            }
            QPushButton:hover {
                color: #0d47a1;
            }
        """)
        self.forgot_password_link.setCursor(Qt.CursorShape.PointingHandCursor)
        options_layout.addWidget(self.forgot_password_link)
        
        form_layout.addLayout(options_layout)
        
        layout.addWidget(form_container)
        
        # Login button
        self.login_button = QPushButton("🔐 Đăng nhập")
        self.login_button.setStyleSheet("""
            QPushButton {
                background-color: #1976d2;
                color: white;
                border: none;
                padding: 12px;
                border-radius: 6px;
                font-size: 16px;
                font-weight: bold;
                margin-top: 16px;
            }
            QPushButton:hover {
                background-color: #1565c0;
            }
            QPushButton:pressed {
                background-color: #0d47a1;
            }
        """)
        layout.addWidget(self.login_button)
        
        # Cancel button
        self.cancel_button = QPushButton("❌ Hủy")
        self.cancel_button.setStyleSheet("""
            QPushButton {
                background-color: #f5f5f5;
                color: #666;
                border: 1px solid #ddd;
                padding: 12px;
                border-radius: 6px;
                font-size: 16px;
                margin-top: 8px;
            }
            QPushButton:hover {
                background-color: #eeeeee;
            }
        """)
        layout.addWidget(self.cancel_button)
        
        layout.addStretch()
    
    def setup_connections(self):
        """Setup signal connections"""
        self.login_button.clicked.connect(self._on_login_clicked)
        self.cancel_button.clicked.connect(self._on_cancel_clicked)
        self.forgot_password_link.clicked.connect(self._on_forgot_password_clicked)
        self.password_input.returnPressed.connect(self._on_login_clicked)
        self.username_input.returnPressed.connect(self._on_login_clicked)
    
    def _on_login_clicked(self):
        """Handle login button click"""
        username = self.username_input.text().strip()
        password = self.password_input.text()
        
        if not username or not password:
            MessageDialog(
                self,
                "Lỗi",
                "Vui lòng nhập đầy đủ tên đăng nhập và mật khẩu.",
                "error"
            ).exec()
            return
        
        # Perform login
        result = login(username, password)
        
        if result['status'] == AuthStatus.SUCCESS:
            self.login_successful.emit(result['user'])
        else:
            MessageDialog(
                self,
                "Đăng nhập thất bại",
                result['message'],
                "error"
            ).exec()
    
    def _on_cancel_clicked(self):
        """Handle cancel button click"""
        self.login_cancelled.emit()
    
    def _on_forgot_password_clicked(self):
        """Handle forgot password link click"""
        MessageDialog(
            self,
            "Quên mật khẩu",
            "Vui lòng liên hệ quản trị viên để đặt lại mật khẩu.",
            "info"
        ).exec()
    
    def clear_inputs(self):
        """Clear input fields"""
        self.username_input.clear()
        self.password_input.clear()
        self.remember_checkbox.setChecked(False)


# Convenience function
def show_login_dialog(parent=None) -> dict:
    """Show login dialog and return user info if successful"""
    from PyQt6.QtWidgets import QDialog
    
    class LoginDialog(QDialog):
        def __init__(self, parent=None):
            super().__init__(parent)
            self.setWindowTitle("🔐 Đăng nhập hệ thống")
            self.setModal(True)
            self.user_info = None
            
            layout = QVBoxLayout(self)
            self.login_view = LoginView()
            layout.addWidget(self.login_view)
            
            self.login_view.login_successful.connect(self._on_login_successful)
            self.login_view.login_cancelled.connect(self.reject)
        
        def _on_login_successful(self, user_info):
            self.user_info = user_info
            self.accept()
    
    dialog = LoginDialog(parent)
    if dialog.exec() == QDialog.DialogCode.Accepted:
        return dialog.user_info
    return None


__all__ = ['LoginView', 'show_login_dialog']