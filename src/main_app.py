#!/usr/bin/env python3
"""
Main Application - Ứng dụng chính với hệ thống xác thực
"""
import sys
import os
from datetime import datetime, timedelta

from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QFont

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.gui.views.auth.login_view import LoginView, show_login_dialog
from src.main_window import MainWindow
from src.services.auth.auth_middleware import set_current_user, get_auth_middleware
from src.services.auth.auth_service import AuthService


class MainApplication(QMainWindow):
    """
    Main application with authentication flow
    """
    
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Quản Lý Kho Lưu Trữ - Nhóm 12")
        self.setMinimumSize(1200, 800)
        self.resize(1400, 900)
        
        # Center window
        self._center_window()
        
        # Initialize services
        self.auth_service = AuthService()
        self.auth_middleware = get_auth_middleware()
        
        # Session management
        self.session_start_time = None
        self.session_timeout = timedelta(hours=8)  # 8 hours timeout
        self.inactivity_timer = QTimer()
        self.inactivity_timer.timeout.connect(self._check_session_timeout)
        self.inactivity_timer.start(60000)  # Check every minute
        
        # Last activity time
        self.last_activity_time = datetime.now()
        
        # Setup login screen
        self.show_login_screen()
    
    def _center_window(self):
        """Center window on screen"""
        from PyQt6.QtWidgets import QStyle
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    
    def show_login_screen(self):
        """Show login screen"""
        # Clear current central widget if any
        if self.centralWidget():
            self.centralWidget().deleteLater()
        
        # Create login view
        login_widget = LoginView()
        login_widget.login_successful.connect(self._on_login_successful)
        login_widget.login_cancelled.connect(self._on_login_cancelled)

        # Center login view within the main window
        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        container_layout.addWidget(login_widget)

        # Set as central widget
        self.setCentralWidget(container)
        
        # Update window title
        self.setWindowTitle("🔐 Đăng nhập - Quản Lý Kho Lưu Trữ")
    
    def _on_login_successful(self, user_info: dict):
        """Handle successful login"""
        print(f"✅ Đăng nhập thành công: {user_info['ho_ten']}")
        
        # Set current user in middleware
        set_current_user(user_info)
        
        # Store session info
        self.session_start_time = datetime.now()
        self.last_activity_time = datetime.now()
        
        # Show main window
        self.show_main_window(user_info)
    
    def _on_login_cancelled(self):
        """Handle login cancelled"""
        print("❌ Đăng nhập bị hủy")
        # Close application if login is cancelled
        self.close()
    
    def show_main_window(self, user_info: dict):
        """Show main application window"""
        # Clear current central widget
        if self.centralWidget():
            self.centralWidget().deleteLater()
        
        # Create main window
        main_window = MainWindow()
        main_window.set_user_info(user_info)
        
        # Set as central widget
        self.setCentralWidget(main_window)
        
        # Update window title
        self.setWindowTitle(f"Quản Lý Kho Lưu Trữ - Chào mừng, {user_info['ho_ten']}")
        
        # Connect activity tracking
        self._setup_activity_tracking(main_window)
    
    def _setup_activity_tracking(self, main_window):
        """Setup activity tracking for auto-logout"""
        # Override key press event to track activity
        original_key_press = main_window.keyPressEvent
        
        def track_key_press(event):
            self.last_activity_time = datetime.now()
            if original_key_press:
                original_key_press(event)
        
        main_window.keyPressEvent = track_key_press
        
        # Override mouse press event to track activity
        original_mouse_press = main_window.mousePressEvent
        
        def track_mouse_press(event):
            self.last_activity_time = datetime.now()
            if original_mouse_press:
                original_mouse_press(event)
        
        main_window.mousePressEvent = track_mouse_press
    
    def _check_session_timeout(self):
        """Check if session has timed out"""
        if not self.session_start_time:
            return
        
        current_time = datetime.now()
        
        # Check total session timeout (8 hours)
        if current_time - self.session_start_time > self.session_timeout:
            print("⏰ Session timeout - Auto logout")
            self._auto_logout()
            return
        
        # Check inactivity timeout (30 minutes of inactivity)
        inactivity_timeout = timedelta(minutes=30)
        if current_time - self.last_activity_time > inactivity_timeout:
            print("⏰ Inactivity timeout - Auto logout")
            self._auto_logout()
    
    def _auto_logout(self):
        """Auto logout due to timeout"""
        from src.gui.dialogs import MessageDialog
        
        # Show timeout message
        dialog = MessageDialog(
            self,
            "Phiên làm việc đã hết hạn",
            "Phiên làm việc của bạn đã hết hạn do không hoạt động.\nVui lòng đăng nhập lại.",
            "warning"
        )
        dialog.exec()
        
        # Return to login screen
        self.show_login_screen()
    
    def closeEvent(self, event):
        """Handle application close"""
        print("👋 Đóng ứng dụng")
        # Clean up session
        if hasattr(self, 'inactivity_timer'):
            self.inactivity_timer.stop()
        event.accept()


def main():
    """Main entry point"""
    app = QApplication(sys.argv)
    
    # Set application font
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    
    # Create and show main application
    main_app = MainApplication()
    main_app.show()
    
    # Start event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()