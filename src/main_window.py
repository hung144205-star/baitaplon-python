#!/usr/bin/env python3
"""
Main Window - QMainWindow với menu bar, toolbar, status bar
"""
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QMenuBar, QMenu, QToolBar, QStatusBar, QLabel,
    QStackedWidget, QSizePolicy, QTextEdit, QMessageBox
)
from PyQt6.QtCore import Qt, QSize, QTimer
from PyQt6.QtGui import QAction, QIcon, QActionGroup, QKeySequence, QFont

import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

class MainWindow(QMainWindow):
    """
    Main application window
    """
    
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Quản Lý Kho Lưu Trữ - Nhóm 12")
        self.setMinimumSize(1200, 800)
        self.resize(1400, 900)
        
        # Center window
        self._center_window()
        
        # Setup UI
        self._setup_menu_bar()
        self._setup_toolbar()
        self._setup_central_widget()
        self._setup_status_bar()
        
        # Load current user info (placeholder)
        self.current_user = None
        
        print("✅ MainWindow initialized")
    
    def _center_window(self):
        """Center window on screen"""
        from PyQt6.QtWidgets import QStyle
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    
    def _setup_menu_bar(self):
        """Setup menu bar"""
        menubar = self.menuBar()
        
        # File Menu
        file_menu = menubar.addMenu("Tệp")
        
        # Dashboard action
        dashboard_action = QAction("Dashboard", self)
        dashboard_action.setShortcut(QKeySequence("Ctrl+D"))
        dashboard_action.setStatusTip("Về dashboard")
        dashboard_action.triggered.connect(self._show_dashboard)
        file_menu.addAction(dashboard_action)
        
        file_menu.addSeparator()
        
        # Exit action
        exit_action = QAction("Thoát", self)
        exit_action.setShortcut(QKeySequence("Ctrl+Q"))
        exit_action.setStatusTip("Thoát ứng dụng")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Module Menus
        modules = {
            "Khách hàng": ("ql_khach_hang", "Quản lý khách hàng", "Ctrl+K"),
            "Kho hàng": ("ql_kho", "Quản lý kho hàng", "Ctrl+O"),
            "Hợp đồng": ("ql_hop_dong", "Quản lý hợp đồng", "Ctrl+H"),
            "Hàng hóa": ("ql_hang_hoa", "Quản lý hàng hóa", "Ctrl+G"),
            "Thanh toán": ("ql_thanh_toan", "Quản lý thanh toán", "Ctrl+T"),
            "Báo cáo": ("ql_bao_cao", "Xem báo cáo", "Ctrl+B"),
        }
        
        self.module_actions = {}
        
        for name, (key, tooltip, shortcut) in modules.items():
            menu = menubar.addMenu(name)
            
            # Main module action
            action = QAction(name, self)
            action.setShortcut(QKeySequence(shortcut))
            action.setStatusTip(tooltip)
            action.triggered.connect(lambda checked, k=key: self._switch_module(k))
            menu.addAction(action)
            
            self.module_actions[key] = action
            
            # Add separator and sub-actions if needed
            if name == "Khách hàng":
                menu.addSeparator()
                add_action = QAction("Thêm khách hàng mới", self)
                add_action.setStatusTip("Thêm khách hàng mới")
                menu.addAction(add_action)
        
        # Settings Menu
        settings_menu = menubar.addMenu("Cài đặt")
        
        # User settings
        user_action = QAction("Thông tin người dùng", self)
        user_action.setStatusTip("Xem và sửa thông tin người dùng")
        settings_menu.addAction(user_action)
        
        settings_menu.addSeparator()
        
        # Preferences
        prefs_action = QAction("Tùy chọn", self)
        prefs_action.setStatusTip("Tùy chọn ứng dụng")
        settings_menu.addAction(prefs_action)
        
        # Help Menu
        help_menu = menubar.addMenu("Trợ giúp")
        
        # About
        about_action = QAction("Giới thiệu", self)
        about_action.setStatusTip("Giới thiệu về ứng dụng")
        about_action.triggered.connect(self._show_about)
        help_menu.addAction(about_action)
        
        help_menu.addSeparator()
        
        # Check for updates
        update_action = QAction("Kiểm tra cập nhật", self)
        update_action.setStatusTip("Kiểm tra phiên bản mới")
        help_menu.addAction(update_action)
        
        print("✅ Menu bar setup complete")
    
    def _setup_toolbar(self):
        """Setup toolbar"""
        toolbar = QToolBar("Main Toolbar")
        toolbar.setMovable(False)
        toolbar.setIconSize(QSize(24, 24))
        toolbar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        
        self.addToolBar(toolbar)
        
        # Dashboard button
        dashboard_btn = QAction("📊 Dashboard", self)
        dashboard_btn.setStatusTip("Về dashboard")
        dashboard_btn.triggered.connect(self._show_dashboard)
        toolbar.addAction(dashboard_btn)
        
        toolbar.addSeparator()
        
        # Module buttons
        module_icons = {
            "ql_khach_hang": "👥",
            "ql_kho": "🏭",
            "ql_hop_dong": "📄",
            "ql_hang_hoa": "📦",
            "ql_thanh_toan": "💰",
            "ql_bao_cao": "📈",
        }
        
        module_names = {
            "ql_khach_hang": "Khách hàng",
            "ql_kho": "Kho",
            "ql_hop_dong": "Hợp đồng",
            "ql_hang_hoa": "Hàng hóa",
            "ql_thanh_toan": "Thanh toán",
            "ql_bao_cao": "Báo cáo",
        }
        
        for key, icon in module_icons.items():
            btn = QAction(f"{icon} {module_names[key]}", self)
            btn.setStatusTip(f"Mở {module_names[key]}")
            btn.triggered.connect(lambda checked, k=key: self._switch_module(k))
            toolbar.addAction(btn)
        
        print("✅ Toolbar setup complete")
    
    def _setup_central_widget(self):
        """Setup central widget with navigation panel"""
        # Import NavigationPanel
        from src.gui.navigation import NavigationPanel
        
        # Create navigation panel
        self.nav_panel = NavigationPanel()
        self.setCentralWidget(self.nav_panel)
        
        # Get navigation manager
        self.nav_manager = self.nav_panel.get_navigation_manager()
        
        # Setup placeholder widgets for each module
        self._setup_module_placeholders_in_nav_panel()
        
        print("✅ Navigation panel setup complete")
    
    def _setup_module_placeholders_in_nav_panel(self):
        """Setup actual view widgets in navigation panel's stacked widget"""
        from src.gui.views import (
            DashboardView,
            KhachHangView,
            KhoView,
            HopDongView,
            HangHoaView
        )
        
        stacked_widget = self.nav_panel.stacked_widget
        
        # Mapping from module key to actual view class
        module_views = {
            "dashboard": DashboardView,
            "ql_khach_hang": KhachHangView,
            "ql_kho": KhoView,
            "ql_hop_dong": HopDongView,
            "ql_hang_hoa": HangHoaView,
        }
        
        modules = [
            ("dashboard", "Dashboard"),
            ("ql_khach_hang", "Quản lý Khách hàng"),
            ("ql_kho", "Quản lý Kho hàng"),
            ("ql_hop_dong", "Quản lý Hợp đồng"),
            ("ql_hang_hoa", "Quản lý Hàng hóa"),
            ("ql_thanh_toan", "Quản lý Thanh toán"),
            ("ql_bao_cao", "Báo cáo"),
        ]
        
        for key, title in modules:
            if key in module_views:
                # Use actual view
                view_class = module_views[key]
                view_widget = view_class()
                stacked_widget.addWidget(view_widget)
                setattr(self, f"widget_{key}", view_widget)
            else:
                # Placeholder for modules without views yet
                placeholder = QTextEdit()
                placeholder.setReadOnly(True)
                placeholder.setHtml(f"""
                    <div style="text-align: center; padding: 100px; font-size: 24px; color: #757575;">
                        <h1>{title}</h1>
                        <p>Module đang được phát triển...</p>
                        <p style="font-size: 16px; margin-top: 20px;">
                            Sẽ sớm ra mắt
                        </p>
                    </div>
                """)
                stacked_widget.addWidget(placeholder)
                setattr(self, f"widget_{key}", placeholder)
        
        # Connect navigation manager to update status bar
        self.nav_manager.view_changed.connect(self._on_navigation_changed)
    
    def _setup_status_bar(self):
        """Setup status bar"""
        statusbar = QStatusBar()
        self.setStatusBar(statusbar)
        
        # Left side - Status message
        self.status_label = QLabel("Sẵn sàng")
        statusbar.addWidget(self.status_label, 1)
        
        # Right side - User info and time
        self.user_label = QLabel("👤 Chưa đăng nhập")
        self.user_label.setStyleSheet("padding: 5px;")
        statusbar.addPermanentWidget(self.user_label)
        
        # Time display
        self.time_label = QLabel("")
        self.time_label.setStyleSheet("padding: 5px;")
        statusbar.addPermanentWidget(self.time_label)
        
        # Update time every minute
        from PyQt6.QtCore import QTimer
        self.timer = QTimer()
        self.timer.timeout.connect(self._update_time)
        self.timer.start(60000)  # Update every minute
        self._update_time()  # Initial update
        
        print("✅ Status bar setup complete")
    
    def _on_navigation_changed(self, view_key: str, data: dict):
        """Handle navigation change"""
        module_names = {
            "dashboard": "Dashboard",
            "ql_khach_hang": "Khách hàng",
            "ql_kho": "Kho hàng",
            "ql_hop_dong": "Hợp đồng",
            "ql_hang_hoa": "Hàng hóa",
            "ql_thanh_toan": "Thanh toán",
            "ql_bao_cao": "Báo cáo",
        }
        
        self.status_label.setText(f"Đang xem: {module_names.get(view_key, '')}")
    
    def _update_time(self):
        """Update time display"""
        from datetime import datetime
        now = datetime.now()
        self.time_label.setText(now.strftime("%H:%M - %d/%m/%Y"))
    
    def _switch_module(self, module_key: str):
        """Switch to a module using navigation manager"""
        if hasattr(self, 'nav_manager') and self.nav_manager:
            self.nav_manager.navigate_to(module_key)
        else:
            # Fallback - just update status bar
            module_names = {
                "dashboard": "Dashboard",
                "ql_khach_hang": "Khách hàng",
                "ql_kho": "Kho hàng",
                "ql_hop_dong": "Hợp đồng",
                "ql_hang_hoa": "Hàng hóa",
                "ql_thanh_toan": "Thanh toán",
                "ql_bao_cao": "Báo cáo",
            }
            self.status_label.setText(f"Đang xem: {module_names.get(module_key, '')}")
    
    def _show_dashboard(self):
        """Show dashboard"""
        self._switch_module("dashboard")
    
    def _show_about(self):
        """Show about dialog"""
        QMessageBox.about(
            self,
            "Về ứng dụng",
            """
            <h2>Quản Lý Kho Lưu Trữ</h2>
            <p><b>Phiên bản:</b> 1.0.0</p>
            <p><b>Nhóm:</b> Nhóm 12 - Lập trình Python</p>
            <p><b>Thành viên:</b></p>
            <ul>
                <li>Đoàn Mạnh Hùng (Trưởng nhóm)</li>
                <li>Lương Hán Hải</li>
                <li>Nguyễn Đồng Thanh</li>
            </ul>
            <p><b>Công nghệ:</b></p>
            <ul>
                <li>Python 3.10+</li>
                <li>PyQt6 6.4+</li>
                <li>SQLAlchemy 2.0+</li>
                <li>SQLite 3.x</li>
            </ul>
            """
        )
    
    def show_module(self, module_name: str):
        """Public method to switch module"""
        self._switch_module(module_name)
    
    def set_user_info(self, user_info: dict):
        """Set current user info"""
        self.current_user = user_info
        if user_info:
            self.user_label.setText(f"👤 {user_info.get('ho_ten', 'User')}")
            self.status_label.setText(f"Chào mừng, {user_info.get('ho_ten', 'User')}!")
