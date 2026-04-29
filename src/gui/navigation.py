#!/usr/bin/env python3
"""
Navigation System - Quản lý điều hướng giữa các màn hình
"""
from PyQt6.QtWidgets import QStackedWidget, QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QFrame
from PyQt6.QtCore import pyqtSignal, QObject, Qt
from typing import Dict, Any, Optional, List
from datetime import datetime


class NavigationHistory:
    """
    Quản lý lịch sử navigation
    Hỗ trợ back/forward navigation
    """

    def __init__(self, max_size: int = 100):
        self.forward_stack: List[str] = []
        self.back_stack: List[str] = []
        self.max_size = max_size

    def push(self, view_key: str):
        """Push view to history"""
        self.back_stack.append(view_key)
        if len(self.back_stack) > self.max_size:
            self.back_stack.pop(0)
        self.forward_stack.clear()  # Clear forward history on new navigation

    def go_back(self) -> Optional[str]:
        """Go back to previous view"""
        if len(self.back_stack) > 1:
            current = self.back_stack.pop()
            self.forward_stack.append(current)
            return self.back_stack[-1]
        return None

    def go_forward(self) -> Optional[str]:
        """Go forward to next view"""
        if self.forward_stack:
            next_view = self.forward_stack.pop()
            self.back_stack.append(next_view)
            return next_view
        return None

    def can_go_back(self) -> bool:
        """Check if can go back"""
        return len(self.back_stack) > 1

    def can_go_forward(self) -> bool:
        """Check if can go forward"""
        return len(self.forward_stack) > 0

    def clear(self):
        """Clear history"""
        self.back_stack.clear()
        self.forward_stack.clear()


class NavigationManager(QObject):
    """
    Quản lý navigation toàn ứng dụng
    """

    # Signals
    view_changed = pyqtSignal(str, dict)  # view_key, data
    history_updated = pyqtSignal(bool, bool)  # can_back, can_forward

    def __init__(self, stacked_widget: QStackedWidget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.history = NavigationHistory()
        self.views: Dict[str, int] = {}  # view_key -> index
        self.current_view: Optional[str] = None

    def register_view(self, view_key: str, index: int):
        """Register a view"""
        self.views[view_key] = index

    def navigate_to(self, view_key: str, data: Dict[str, Any] = None, add_to_history: bool = True):
        """
        Navigate to a view

        Args:
            view_key: Key of the view to navigate to
            data: Optional data to pass to the view
            add_to_history: Whether to add to navigation history
        """
        if view_key not in self.views:
            print(f"⚠️  View not found: {view_key}")
            return

        index = self.views[view_key]
        self.stacked_widget.setCurrentIndex(index)

        if add_to_history:
            self.history.push(view_key)

        self.current_view = view_key
        self.view_changed.emit(view_key, data or {})
        self._update_history_signals()

    def go_back(self):
        """Go back to previous view"""
        previous_view = self.history.go_back()
        if previous_view:
            self.navigate_to(previous_view, add_to_history=False)

    def go_forward(self):
        """Go forward to next view"""
        next_view = self.history.go_forward()
        if next_view:
            self.navigate_to(next_view, add_to_history=False)

    def can_go_back(self) -> bool:
        """Check if can go back"""
        return self.history.can_go_back()

    def can_go_forward(self) -> bool:
        """Check if can go forward"""
        return self.history.can_go_forward()

    def _update_history_signals(self):
        """Update history signals"""
        can_back = self.history.can_go_back()
        can_forward = self.history.can_go_forward()
        self.history_updated.emit(can_back, can_forward)

    def get_current_view(self) -> Optional[str]:
        """Get current view key"""
        return self.current_view

    def clear_history(self):
        """Clear navigation history"""
        self.history.clear()
        self._update_history_signals()


class BreadcrumbWidget(QFrame):
    """
    Hiển thị breadcrumb navigation
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.path: List[Dict[str, str]] = []

    def setup_ui(self):
        """Setup UI"""
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border-bottom: 1px solid rgba(0, 0, 0, 0.1);
                padding: 8px 16px;
            }
            QPushButton {
                background-color: transparent;
                color: #1976d2;
                border: none;
                padding: 4px 8px;
                text-align: left;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #e3f2fd;
                border-radius: 4px;
            }
            QLabel {
                color: #615d59;
                padding: 4px 8px;
            }
            QLabel#current {
                color: #31302e;
                font-weight: 600;
            }
        """)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)

        self.layout_container = layout
        self.button_group: List[QPushButton] = []

    def set_path(self, path: List[Dict[str, str]]):
        """
        Set breadcrumb path

        Args:
            path: List of {label, key} dicts
        """
        self.path = path
        self._rebuild()

    def _rebuild(self):
        """Rebuild breadcrumb UI"""
        # Clear existing buttons
        for i in reversed(range(self.layout_container.count())):
            widget = self.layout_container.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        self.button_group.clear()

        # Add breadcrumbs
        for i, item in enumerate(self.path):
            # Add separator
            if i > 0:
                separator = QLabel("›")
                separator.setStyleSheet("color: #9e9e9e; font-size: 16px;")
                self.layout_container.addWidget(separator)

            # Add button/label
            label = item.get('label', 'Home')
            is_last = i == len(self.path) - 1

            if is_last:
                current_label = QLabel(label)
                current_label.setObjectName("current")
                self.layout_container.addWidget(current_label)
            else:
                btn = QPushButton(label)
                btn.clicked.connect(lambda checked, idx=i: self._on_click(idx))
                self.layout_container.addWidget(btn)
                self.button_group.append(btn)

        # Add spacer
        self.layout_container.addStretch()

    def _on_click(self, index: int):
        """Handle breadcrumb click"""
        if index < len(self.path):
            # Emit signal with the clicked path
            from PyQt6.QtCore import QCoreApplication
            event = {
                'type': 'breadcrumb_click',
                'index': index,
                'path': self.path[:index+1]
            }
            # Find parent window and emit event
            parent = self.parent()
            if parent and hasattr(parent, 'on_breadcrumb_click'):
                parent.on_breadcrumb_click(event)


class SidebarMenu(QFrame):
    """
    Sidebar menu với danh sách các module
    """

    module_selected = pyqtSignal(str)  # module_key

    def __init__(self, parent=None):
        super().__init__(parent)
        self.buttons: Dict[str, QPushButton] = {}
        self.setup_ui()

    def setup_ui(self):
        """Setup UI"""
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border-right: 1px solid rgba(0, 0, 0, 0.1);
            }
            QLabel#titleLabel {
                font-size: 18px;
                font-weight: 700;
                color: #31302e;
                padding: 20px 16px 16px;
            }
            QPushButton {
                background-color: transparent;
                color: #615d59;
                border: none;
                padding: 12px 16px;
                text-align: left;
                font-size: 14px;
                font-weight: 500;
                border-radius: 6px;
                margin: 4px 8px;
            }
            QPushButton:hover {
                background-color: #f6f5f4;
                color: #31302e;
            }
            QPushButton:selected, QPushButton#active {
                background-color: #e3f2fd;
                color: #1976d2;
            }
            QPushButton:pressed {
                background-color: #bbdefb;
            }
            QFrame#separator {
                background-color: rgba(0, 0, 0, 0.1);
                min-height: 1px;
                max-height: 1px;
                margin: 8px 16px;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Title
        title = QLabel("QUẢN LÝ KHO")
        title.setObjectName("titleLabel")
        layout.addWidget(title)

        # Modules
        modules = [
            ("📊", "dashboard", "Dashboard"),
            ("👥", "ql_khach_hang", "Khách hàng"),
            ("🏭", "ql_kho", "Kho hàng"),
            ("📄", "ql_hop_dong", "Hợp đồng"),
            ("📦", "ql_hang_hoa", "Hàng hóa"),
            ("💰", "ql_thanh_toan", "Thanh toán"),
            ("📈", "ql_bao_cao", "Báo cáo"),
        ]

        for icon, key, label in modules:
            btn = QPushButton(f"{icon}  {label}")
            btn.setCheckable(True)
            btn.clicked.connect(lambda checked, k=key: self._on_module_click(k))
            layout.addWidget(btn)
            self.buttons[key] = btn

        # Separator
        separator = QFrame()
        separator.setObjectName("separator")
        separator.setFixedHeight(1)
        layout.addWidget(separator)

        # Settings button
        settings_btn = QPushButton("⚙️  Cài đặt")
        settings_btn.clicked.connect(lambda: self.module_selected.emit("settings"))
        layout.addWidget(settings_btn)

        # Help button
        help_btn = QPushButton("❓  Trợ giúp")
        help_btn.clicked.connect(lambda: self.module_selected.emit("help"))
        layout.addWidget(help_btn)

        # Add spacer
        layout.addStretch()

        # Footer
        from datetime import datetime
        year = datetime.now().year
        footer = QLabel(f"© {year} Nhóm 12")
        footer.setStyleSheet("color: #a39e98; font-size: 12px; padding: 16px;")
        layout.addWidget(footer)

    def _on_module_click(self, module_key: str):
        """Handle module selection"""
        # Update active state
        for key, btn in self.buttons.items():
            if key == module_key:
                btn.setObjectName("active")
            else:
                btn.setObjectName("")
            btn.setStyle(btn.style())

        self.module_selected.emit(module_key)

    def set_active_module(self, module_key: str):
        """Set active module"""
        if module_key in self.buttons:
            self.buttons[module_key].setChecked(True)
            self.buttons[module_key].setObjectName("active")
            self.buttons[module_key].setStyle(self.buttons[module_key].style())


class NavigationPanel(QWidget):
    """
    Panel chứa sidebar + main content với navigation
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

        # Create navigation manager
        self.nav_manager = NavigationManager(self.stacked_widget)

        # Register views
        self._register_views()

        # Connect signals
        self.sidebar.module_selected.connect(self._on_module_selected)
        self.nav_manager.view_changed.connect(self._on_view_changed)

    def setup_ui(self):
        """Setup UI"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Sidebar
        self.sidebar = SidebarMenu()
        self.sidebar.setFixedWidth(220)
        layout.addWidget(self.sidebar)

        # Main content
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Breadcrumb
        self.breadcrumb = BreadcrumbWidget()
        main_layout.addWidget(self.breadcrumb)

        # Content area
        self.stacked_widget = QStackedWidget()
        main_layout.addWidget(self.stacked_widget)

        layout.addWidget(main_widget)

    def _register_views(self):
        """Register views with navigation manager"""
        views = [
            "dashboard",
            "ql_khach_hang",
            "ql_kho",
            "ql_hop_dong",
            "ql_hang_hoa",
            "ql_thanh_toan",
            "ql_bao_cao",
            "tro_giup",
            "settings",
        ]
        
        for i, view_key in enumerate(views):
            self.nav_manager.register_view(view_key, i)

    def _on_module_selected(self, module_key: str):
        """Handle module selection from sidebar"""
        # Map sidebar keys to view keys
        key_mapping = {
            "help": "tro_giup",
            "settings": "settings",
        }
        
        if module_key in key_mapping:
            # Navigate to special module
            self.nav_manager.navigate_to(key_mapping[module_key])
        else:
            self.nav_manager.navigate_to(module_key)

    def _on_view_changed(self, view_key: str, data: dict):
        """Handle view change"""
        # Update breadcrumb
        view_names = {
            "dashboard": "Dashboard",
            "ql_khach_hang": "Khách hàng",
            "ql_kho": "Kho hàng",
            "ql_hop_dong": "Hợp đồng",
            "ql_hang_hoa": "Hàng hóa",
            "ql_thanh_toan": "Thanh toán",
            "ql_bao_cao": "Báo cáo",
            "tro_giup": "Trợ giúp",
            "settings": "Cài đặt",
        }

        path = [
            {"label": "Home", "key": "dashboard"},
            {"label": view_names.get(view_key, view_key), "key": view_key}
        ]
        self.breadcrumb.set_path(path)

        # Update sidebar
        self.sidebar.set_active_module(view_key)

    def navigate_to(self, view_key: str, data: dict = None):
        """Navigate to a view"""
        self.nav_manager.navigate_to(view_key, data)

    def go_back(self):
        """Go back"""
        self.nav_manager.go_back()

    def go_forward(self):
        """Go forward"""
        self.nav_manager.go_forward()

    def get_navigation_manager(self) -> NavigationManager:
        """Get navigation manager"""
        return self.nav_manager


__all__ = [
    'NavigationManager',
    'NavigationHistory',
    'BreadcrumbWidget',
    'SidebarMenu',
    'NavigationPanel',
]
