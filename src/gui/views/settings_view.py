#!/usr/bin/env python3
"""
Settings View - Redesigned Settings Interface
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QCheckBox, QSpinBox, QLineEdit,
    QScrollArea, QGridLayout, QGroupBox
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QIcon

from src.gui.dialogs import MessageDialog, ConfirmDialog


class SettingsView(QWidget):
    """
    Redesigned Settings View - Modern card-based interface
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.load_settings()
    
    def setup_ui(self):
        """Setup modern UI"""
        # Main stylesheet
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f4f8;
                font-family: 'Segoe UI', 'Inter', sans-serif;
            }
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollArea > QWidget > QWidget {
                background-color: transparent;
            }
        """)
        
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Header
        header = self._create_header()
        main_layout.addWidget(header)
        
        # Scrollable content
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: #f0f4f8;
            }
        """)
        
        container = QWidget()
        container.setStyleSheet("background-color: #f0f4f8;")
        content_layout = QVBoxLayout(container)
        content_layout.setContentsMargins(32, 24, 32, 32)
        content_layout.setSpacing(24)
        
        # Settings cards in 2-column grid
        grid_layout = QGridLayout()
        grid_layout.setSpacing(20)
        grid_layout.setColumnStretch(0, 1)
        grid_layout.setColumnStretch(1, 1)
        
        # Card 1: Display Settings (left)
        display_card = self._create_display_card()
        grid_layout.addWidget(display_card, 0, 0)
        
        # Card 2: Notification Settings (right)
        notification_card = self._create_notification_card()
        grid_layout.addWidget(notification_card, 0, 1)
        
        # Card 3: Data Settings (left)
        data_card = self._create_data_card()
        grid_layout.addWidget(data_card, 1, 0)
        
        # Card 4: Account Settings (right)
        account_card = self._create_account_card()
        grid_layout.addWidget(account_card, 1, 1)
        
        content_layout.addLayout(grid_layout)
        
        # Action buttons
        buttons_frame = self._create_buttons()
        content_layout.addWidget(buttons_frame)
        
        content_layout.addStretch()
        
        scroll.setWidget(container)
        main_layout.addWidget(scroll, 1)
    
    def _create_header(self) -> QFrame:
        """Create header with title"""
        header = QFrame()
        header.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    from: #1976d2, to: #2196f3);
                padding: 24px 32px;
            }
        """)
        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(32, 24, 32, 24)
        
        title = QLabel("⚙️ Cài Đặt Hệ Thống")
        title.setStyleSheet("""
            QLabel {
                font-size: 28px;
                font-weight: 700;
                color: #ffffff;
            }
        """)
        header_layout.addWidget(title)
        
        subtitle = QLabel("Quản lý tùy chọn và cấu hình ứng dụng")
        subtitle.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: rgba(255, 255, 255, 0.85);
                margin-top: 4px;
            }
        """)
        header_layout.addWidget(subtitle)
        
        return header
    
    def _create_card(self, title: str, icon: str, color: str = "#1976d2") -> QFrame:
        """Create a settings card"""
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: #ffffff;
                border-radius: 16px;
                border: 1px solid rgba(0, 0, 0, 0.05);
            }}
        """)
        
        layout = QVBoxLayout(card)
        layout.setContentsMargins(24, 20, 24, 24)
        layout.setSpacing(16)
        
        # Card header
        header_layout = QHBoxLayout()
        header_layout.setSpacing(12)
        
        icon_label = QLabel(icon)
        icon_label.setStyleSheet(f"""
            QLabel {{
                font-size: 24px;
                background-color: {color}15;
                border-radius: 10px;
                padding: 8px;
                min-width: 40px;
                min-height: 40px;
                alignment: center;
            }}
        """)
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_label.setFixedSize(56, 56)
        
        title_label = QLabel(title)
        title_label.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: 700;
                color: #1a1a2e;
            }
        """)
        
        header_layout.addWidget(icon_label)
        header_layout.addWidget(title_label, 1)
        header_layout.addStretch()
        
        layout.addLayout(header_layout)
        
        # Separator
        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet("""
            QFrame {
                background-color: #e8e8e8;
                max-height: 1px;
            }
        """)
        layout.addWidget(sep)
        
        return card
    
    def _create_display_card(self) -> QFrame:
        """Display settings card"""
        card = self._create_card("📺 Hiển thị", "📺", "#7c4dff")
        layout = card.layout()
        
        # Items per page
        row1 = self._create_setting_row(
            "Số mục trên trang",
            "Số lượng items hiển thị trong bảng",
            self._create_spinbox(10, 100, 25, " mục")
        )
        layout.addLayout(row1[0])
        
        # Show confirm dialog
        row2 = self._create_setting_row_with_checkbox(
            "Xác nhận khi xóa",
            "Hiện hộp thoại xác nhận trước khi xóa dữ liệu",
            True
        )
        self.show_confirm_check = row2[1]
        layout.addLayout(row2[0])
        
        # Show tooltips
        row3 = self._create_setting_row_with_checkbox(
            "Gợi ý khi di chuột",
            "Hiện tooltip khi hover vào các phần tử",
            True
        )
        self.show_tooltips_check = row3[1]
        layout.addLayout(row3[0])
        
        # Auto refresh
        row4 = self._create_setting_row_with_checkbox(
            "Tự động làm mới",
            "Tự động cập nhật dữ liệu định kỳ",
            False
        )
        self.auto_refresh_check = row4[1]
        layout.addLayout(row4[0])
        
        return card
    
    def _create_notification_card(self) -> QFrame:
        """Notification settings card"""
        card = self._create_card("🔔 Thông báo", "🔔", "#ff9800")
        layout = card.layout()
        
        # Low stock alert
        row1 = self._create_setting_row_with_checkbox(
            "Cảnh báo hàng sắp hết",
            "Nhắc nhở khi số lượng hàng trong kho thấp",
            True
        )
        self.low_stock_alert_check = row1[1]
        layout.addLayout(row1[0])
        
        # Contract expiry alert
        row2 = self._create_setting_row_with_checkbox(
            "Cảnh báo hợp đồng hết hạn",
            "Thông báo khi hợp đồng sắp hết hiệu lực",
            True
        )
        self.contract_expiry_check = row2[1]
        layout.addLayout(row2[0])
        
        # Alert days
        row3 = self._create_setting_row(
            "Số ngày cảnh báo trước",
            "Thời gian trước khi hết hạn để nhắc nhở",
            self._create_spinbox(1, 90, 30, " ngày")
        )
        self.alert_days = row3[1]
        layout.addLayout(row3[0])
        
        return card
    
    def _create_data_card(self) -> QFrame:
        """Data settings card"""
        card = self._create_card("💾 Dữ liệu", "💾", "#4caf50")
        layout = card.layout()
        
        # Auto backup
        row1 = self._create_setting_row_with_checkbox(
            "Tự động sao lưu",
            "Sao lưu dữ liệu định kỳ",
            True
        )
        self.auto_backup_check = row1[1]
        layout.addLayout(row1[0])
        
        # Backup path
        path_row = self._create_setting_row(
            "Thư mục sao lưu",
            "Đường dẫn lưu trữ file backup",
            None
        )
        self.backup_path = QLineEdit()
        self.backup_path.setPlaceholderText("./data/backups")
        self.backup_path.setText("./data/backups")
        self.backup_path.setStyleSheet("""
            QLineEdit {
                padding: 12px 16px;
                border: 2px solid #e0e0e0;
                border-radius: 10px;
                background-color: #fafafa;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: #4caf50;
                background-color: #fff;
            }
        """)
        self.backup_path.setMinimumHeight(44)
        
        # Update the widget in row
        layout.removeItem(path_row[0])
        path_row_layout = path_row[0]
        # Remove spacer items to just keep label and input
        while path_row_layout.count() > 2:
            path_row_layout.takeAt(2)
        path_row_layout.addWidget(self.backup_path)
        layout.addLayout(path_row_layout)
        
        return card
    
    def _create_account_card(self) -> QFrame:
        """Account settings card"""
        card = self._create_card("🔐 Tài Khoản", "🔐", "#f44336")
        layout = card.layout()
        
        # User info section
        user_info = QFrame()
        user_info.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border-radius: 12px;
                padding: 16px;
            }
        """)
        user_layout = QHBoxLayout(user_info)
        user_layout.setSpacing(16)
        
        avatar = QLabel("👤")
        avatar.setStyleSheet("""
            QLabel {
                font-size: 36px;
                background-color: #e3f2fd;
                border-radius: 25px;
                padding: 12px;
                min-width: 50px;
                alignment: center;
            }
        """)
        avatar.setFixedSize(74, 74)
        
        info_layout = QVBoxLayout()
        info_layout.setSpacing(4)
        
        name_label = QLabel("Người dùng hiện tại")
        name_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: 600;
                color: #1a1a2e;
            }
        """)
        
        role_label = QLabel("Quản trị viên")
        role_label.setStyleSheet("""
            QLabel {
                font-size: 13px;
                color: #666;
            }
        """)
        
        info_layout.addWidget(name_label)
        info_layout.addWidget(role_label)
        info_layout.addStretch()
        
        user_layout.addWidget(avatar)
        user_layout.addLayout(info_layout, 1)
        
        layout.addWidget(user_info)
        
        # Change password button
        change_pwd_btn = QPushButton("🔑  Đổi mật khẩu")
        change_pwd_btn.setStyleSheet("""
            QPushButton {
                background-color: #fff;
                color: #f44336;
                border: 2px solid #f44336;
                border-radius: 10px;
                padding: 14px 24px;
                font-size: 14px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #f44336;
                color: #fff;
            }
        """)
        change_pwd_btn.clicked.connect(self._on_change_password)
        layout.addWidget(change_pwd_btn)
        
        return card
    
    def _create_setting_row(self, label: str, description: str, widget) -> tuple:
        """Create a setting row with label, description and widget"""
        row_layout = QVBoxLayout()
        row_layout.setSpacing(6)
        
        label_layout = QHBoxLayout()
        label_layout.setSpacing(8)
        
        title = QLabel(label)
        title.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-weight: 600;
                color: #333;
            }
        """)
        
        label_layout.addWidget(title)
        label_layout.addStretch()
        
        desc = QLabel(description)
        desc.setStyleSheet("""
            QLabel {
                font-size: 12px;
                color: #888;
            }
        """)
        
        row_layout.addLayout(label_layout)
        row_layout.addWidget(desc)
        
        if widget:
            if isinstance(widget, QSpinBox):
                spin_container = QFrame()
                spin_layout = QHBoxLayout(spin_container)
                spin_layout.setContentsMargins(0, 8, 0, 0)
                spin_layout.addWidget(widget)
                spin_layout.addStretch()
                row_layout.addWidget(spin_container)
                return (row_layout, widget)
            else:
                widget_container = QFrame()
                widget_layout = QHBoxLayout(widget_container)
                widget_layout.setContentsMargins(0, 8, 0, 0)
                widget_layout.addWidget(widget)
                widget_layout.addStretch()
                row_layout.addWidget(widget_container)
        
        return (row_layout, None)
    
    def _create_setting_row_with_checkbox(self, label: str, description: str, default_checked: bool) -> tuple:
        """Create a setting row with checkbox"""
        row_layout = QVBoxLayout()
        row_layout.setSpacing(6)
        
        checkbox_layout = QHBoxLayout()
        checkbox_layout.setSpacing(12)
        
        checkbox = QCheckBox(label)
        checkbox.setChecked(default_checked)
        checkbox.setStyleSheet("""
            QCheckBox {
                spacing: 10px;
                font-size: 14px;
                font-weight: 600;
                color: #333;
            }
            QCheckBox::indicator {
                width: 22px;
                height: 22px;
                border-radius: 6px;
                border: 2px solid #d0d0d0;
                background-color: #fff;
            }
            QCheckBox::indicator:checked {
                background-color: #1976d2;
                border-color: #1976d2;
            }
        """)
        
        checkbox_layout.addWidget(checkbox)
        checkbox_layout.addStretch()
        
        row_layout.addLayout(checkbox_layout)
        
        desc = QLabel(description)
        desc.setStyleSheet("""
            QLabel {
                font-size: 12px;
                color: #888;
                padding-left: 34px;
            }
        """)
        row_layout.addWidget(desc)
        
        return (row_layout, checkbox)
    
    def _create_spinbox(self, min_val: int, max_val: int, default: int, suffix: str) -> QSpinBox:
        """Create a styled spinbox"""
        spin = QSpinBox()
        spin.setRange(min_val, max_val)
        spin.setValue(default)
        spin.setSuffix(suffix)
        spin.setButtonSymbols(QSpinBox.ButtonSymbols.NoButtons)
        spin.setStyleSheet("""
            QSpinBox {
                padding: 12px 16px;
                border: 2px solid #e0e0e0;
                border-radius: 10px;
                background-color: #fafafa;
                font-size: 14px;
                min-width: 120px;
            }
            QSpinBox:focus {
                border-color: #1976d2;
                background-color: #fff;
            }
        """)
        spin.setMinimumHeight(44)
        return spin
    
    def _create_buttons(self) -> QFrame:
        """Create action buttons frame"""
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border-radius: 16px;
                border: 1px solid rgba(0, 0, 0, 0.05);
                padding: 20px 24px;
            }
        """)
        
        layout = QHBoxLayout(frame)
        layout.setSpacing(16)
        
        # Reset button
        reset_btn = QPushButton("↺  Khôi phục mặc định")
        reset_btn.setStyleSheet("""
            QPushButton {
                background-color: #fff;
                color: #666;
                border: 2px solid #ddd;
                border-radius: 10px;
                padding: 14px 28px;
                font-size: 14px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #f5f5f5;
                border-color: #bbb;
            }
        """)
        reset_btn.clicked.connect(self._on_reset)
        
        # Save button
        save_btn = QPushButton("💾  Lưu cài đặt")
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #1976d2;
                color: #fff;
                border: none;
                border-radius: 10px;
                padding: 14px 32px;
                font-size: 14px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #1565c0;
            }
        """)
        save_btn.clicked.connect(self._on_save)
        
        layout.addStretch()
        layout.addWidget(reset_btn)
        layout.addWidget(save_btn)
        
        return frame
    
    def load_settings(self):
        """Load settings from config"""
        # Placeholder - in real implementation, load from config file
        pass
    
    def _on_save(self):
        """Save settings"""
        try:
            # In real implementation, save to config file
            MessageDialog.success(self, "Thành công", "Đã lưu cài đặt thành công!")
        except Exception as e:
            MessageDialog.error(self, "Lỗi", f"Không thể lưu cài đặt:\n{str(e)}")
    
    def _on_reset(self):
        """Reset settings to default"""
        reply = ConfirmDialog.ask(
            self,
            "Bạn có chắc muốn khôi phục cài đặt mặc định?",
            "Xác nhận"
        )
        
        if reply:
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
