#!/usr/bin/env python3
"""
Settings View - Giao diện Cài đặt
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QGroupBox, QComboBox, QCheckBox, QSpinBox, QLineEdit,
    QFormLayout, QScrollArea
)
from PyQt6.QtCore import Qt

from src.gui.dialogs import MessageDialog


class SettingsView(QWidget):
    """
    Giao diện Cài đặt - Quản lý tùy chọn ứng dụng
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.load_settings()
    
    def setup_ui(self):
        """Setup UI"""
        self.setStyleSheet("""
            QWidget {
                background-color: #faf9f8;
                font-family: 'Inter', sans-serif;
            }
            QLabel#titleLabel {
                font-size: 24px;
                font-weight: 700;
                color: #31302e;
            }
            QLabel#sectionLabel {
                font-size: 16px;
                font-weight: 600;
                color: #005db2;
            }
            QLabel#descLabel {
                font-size: 13px;
                color: #615d59;
            }
            QPushButton {
                border-radius: 6px;
                padding: 10px 20px;
                font-weight: 600;
                font-size: 13px;
            }
            QPushButton#primaryButton {
                background-color: #005db2;
                color: white;
                border: none;
            }
            QPushButton#primaryButton:hover {
                background-color: #00468a;
            }
            QPushButton#secondaryButton {
                background-color: #ffffff;
                color: #005db2;
                border: 1px solid #005db2;
            }
            QPushButton#secondaryButton:hover {
                background-color: #e3f2fd;
            }
            QGroupBox {
                background-color: #ffffff;
                border: 1px solid rgba(0, 0, 0, 0.1);
                border-radius: 8px;
                padding: 20px;
                margin-top: 16px;
                font-weight: 600;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 16px;
                padding: 0 8px;
            }
            QComboBox {
                padding: 8px 12px;
                border: 1px solid #e0e0e0;
                border-radius: 6px;
                background-color: #ffffff;
                font-size: 13px;
                min-width: 200px;
            }
            QCheckBox {
                spacing: 8px;
                font-size: 13px;
                color: #31302e;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border-radius: 4px;
                border: 1px solid #e0e0e0;
                background-color: #ffffff;
            }
            QCheckBox::indicator:checked {
                background-color: #005db2;
                border-color: #005db2;
            }
            QSpinBox {
                padding: 8px 12px;
                border: 1px solid #e0e0e0;
                border-radius: 6px;
                background-color: #ffffff;
                font-size: 13px;
            }
            QLineEdit {
                padding: 8px 12px;
                border: 1px solid #e0e0e0;
                border-radius: 6px;
                background-color: #ffffff;
                font-size: 13px;
            }
            QLineEdit:focus {
                border: 2px solid #005db2;
            }
        """)
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 30, 40, 30)
        main_layout.setSpacing(20)
        
        # Title
        title_layout = QHBoxLayout()
        title = QLabel("⚙️ CÀI ĐẶT")
        title.setObjectName("titleLabel")
        title_layout.addWidget(title)
        title_layout.addStretch()
        main_layout.addLayout(title_layout)
        
        # Scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border: none;")
        
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setSpacing(20)
        
        # 1. General Settings
        general_group = QGroupBox("🌐 Cài đặt Chung")
        general_layout = QFormLayout(general_group)
        general_layout.setSpacing(16)
        
        # Language
        self.language_combo = QComboBox()
        self.language_combo.addItems(["Tiếng Việt", "English"])
        general_layout.addRow("Ngôn ngữ:", self.language_combo)
        
        # Theme
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Sáng (Mặc định)", "Tối", "Tự động"])
        general_layout.addRow("Giao diện:", self.theme_combo)
        
        # Startup module
        self.startup_combo = QComboBox()
        self.startup_combo.addItems(["Dashboard", "Khách hàng", "Kho hàng", "Hợp đồng", "Hàng hóa", "Thanh toán", "Báo cáo"])
        general_layout.addRow("Mở đầu khi khởi động:", self.startup_combo)
        
        layout.addWidget(general_group)
        
        # 2. Display Settings
        display_group = QGroupBox("📺 Cài đặt Hiển thị")
        display_layout = QFormLayout(display_group)
        display_layout.setSpacing(16)
        
        # Items per page
        self.items_per_page = QSpinBox()
        self.items_per_page.setRange(10, 100)
        self.items_per_page.setSuffix(" mục")
        self.items_per_page.setSingleStep(10)
        display_layout.addRow("Số mục trên trang:", self.items_per_page)
        
        # Show confirm dialog
        self.show_confirm_check = QCheckBox("Hiện hộp thoại xác nhận khi xóa")
        display_layout.addRow(self.show_confirm_check)
        
        # Show tooltips
        self.show_tooltips_check = QCheckBox("Hiện gợi ý khi di chuột")
        self.show_tooltips_check.setChecked(True)
        display_layout.addRow(self.show_tooltips_check)
        
        # Auto refresh
        self.auto_refresh_check = QCheckBox("Tự động làm mới dữ liệu")
        display_layout.addRow(self.auto_refresh_check)
        
        layout.addWidget(display_group)
        
        # 3. Notification Settings
        notification_group = QGroupBox("🔔 Cài đặt Thông báo")
        notification_layout = QFormLayout(notification_group)
        notification_layout.setSpacing(16)
        
        # Low stock alert
        self.low_stock_alert_check = QCheckBox("Cảnh báo khi hàng sắp hết")
        self.low_stock_alert_check.setChecked(True)
        notification_layout.addRow(self.low_stock_alert_check)
        
        # Contract expiry alert
        self.contract_expiry_check = QCheckBox("Cảnh báo khi hợp đồng sắp hết hạn")
        self.contract_expiry_check.setChecked(True)
        notification_layout.addRow(self.contract_expiry_check)
        
        # Alert days before
        self.alert_days = QSpinBox()
        self.alert_days.setRange(1, 90)
        self.alert_days.setSuffix(" ngày")
        notification_layout.addRow("Số ngày cảnh báo trước:", self.alert_days)
        
        layout.addWidget(notification_group)
        
        # 4. Data Settings
        data_group = QGroupBox("💾 Cài đặt Dữ liệu")
        data_layout = QFormLayout(data_group)
        data_layout.setSpacing(16)
        
        # Auto backup
        self.auto_backup_check = QCheckBox("Tự động sao lưu dữ liệu")
        self.auto_backup_check.setChecked(True)
        data_layout.addRow(self.auto_backup_check)
        
        # Backup path
        self.backup_path = QLineEdit()
        self.backup_path.setPlaceholderText("Đường dẫn lưu sao lưu...")
        data_layout.addRow("Thư mục sao lưu:", self.backup_path)
        
        layout.addWidget(data_group)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        reset_btn = QPushButton("Khôi phục mặc định")
        reset_btn.setObjectName("secondaryButton")
        reset_btn.clicked.connect(self._on_reset)
        button_layout.addWidget(reset_btn)
        
        save_btn = QPushButton("💾 Lưu cài đặt")
        save_btn.setObjectName("primaryButton")
        save_btn.clicked.connect(self._on_save)
        button_layout.addWidget(save_btn)
        
        layout.addLayout(button_layout)
        
        # User account section
        account_group = QGroupBox("🔐 Tài khoản của bạn")
        account_layout = QVBoxLayout(account_group)
        account_layout.setSpacing(12)
        
        change_pwd_btn = QPushButton("🔑 Đổi mật khẩu")
        change_pwd_btn.setObjectName("secondaryButton")
        change_pwd_btn.setStyleSheet("""
            QPushButton#secondaryButton {
                background-color: #ffffff;
                color: #005db2;
                border: 1px solid #005db2;
            }
            QPushButton#secondaryButton:hover {
                background-color: #e3f2fd;
            }
        """)
        change_pwd_btn.clicked.connect(self._on_change_password)
        account_layout.addWidget(change_pwd_btn)
        
        layout.addWidget(account_group)
        layout.addStretch()
        
        scroll.setWidget(container)
        
        main_layout.addWidget(scroll, 1)
    
    def load_settings(self):
        """Load settings from config"""
        # Placeholder - in real implementation, load from config file
        self.items_per_page.setValue(25)
        self.alert_days.setValue(30)
        self.backup_path.setText("./data/backups")
    
    def _on_save(self):
        """Save settings"""
        try:
            # In real implementation, save to config file
            MessageDialog.success(self, "Thành công", "Đã lưu cài đặt thành công!")
        except Exception as e:
            MessageDialog.error(self, "Lỗi", f"Không thể lưu cài đặt:\n{str(e)}")
    
    def _on_reset(self):
        """Reset settings to default"""
        reply = MessageDialog.confirm(
            self,
            "Xác nhận",
            "Bạn có chắc muốn khôi phục cài đặt mặc định?"
        )
        
        if reply:
            self.language_combo.setCurrentIndex(0)
            self.theme_combo.setCurrentIndex(0)
            self.startup_combo.setCurrentIndex(0)
            self.items_per_page.setValue(25)
            self.show_confirm_check.setChecked(True)
            self.show_tooltips_check.setChecked(True)
            self.auto_refresh_check.setChecked(False)
            self.low_stock_alert_check.setChecked(True)
            self.contract_expiry_check.setChecked(True)
            self.alert_days.setValue(30)
            self.auto_backup_check.setChecked(True)
            self.backup_path.setText("./data/backups")
    
    def _on_change_password(self):
        """Handle change password button click"""
        from src.gui.dialogs import ChangePasswordDialog
        from src.services.auth.auth_middleware import get_auth_middleware
        
        # Get current logged-in user
        middleware = get_auth_middleware()
        current_user = middleware.current_user
        
        if not current_user or not current_user.get('ma_nhan_vien'):
            MessageDialog.warning(
                self,
                "Cảnh báo",
                "Không thể xác định người dùng hiện tại. Vui lòng đăng nhập lại."
            )
            return
        
        ma_nhan_vien = current_user.get('ma_nhan_vien')
        ChangePasswordDialog.show_dialog(self, ma_nhan_vien)


__all__ = ['SettingsView']
