#!/usr/bin/env python3
"""
Button Widgets - Các loại buttons styled
"""
from PyQt6.QtWidgets import QPushButton, QToolButton, QWidget, QHBoxLayout, QVBoxLayout
from PyQt6.QtCore import Qt, pyqtSignal, QSize
from PyQt6.QtGui import QIcon


class PrimaryButton(QPushButton):
    """
    Primary button - Notion blue style
    """
    
    def __init__(self, text: str = "", parent=None, icon: str = None):
        super().__init__(text, parent)
        self.setup_ui()
        if icon:
            self.setIcon(icon)
    
    def setup_ui(self):
        """Setup UI"""
        self.setStyleSheet("""
            QPushButton {
                background-color: #0075de;
                color: #ffffff;
                border: none;
                padding: 10px 20px;
                border-radius: 6px;
                font-weight: 600;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #005bab;
            }
            QPushButton:pressed {
                background-color: #004494;
            }
            QPushButton:disabled {
                background-color: #a39e98;
                color: #e8e8e8;
            }
        """)
        
        # Set minimum size
        self.setMinimumSize(100, 40)
    
    def set_icon(self, icon_char: str):
        """Set icon character (emoji)"""
        if icon_char:
            self.setText(f"{icon_char} {self.text()}")


class SecondaryButton(QPushButton):
    """
    Secondary button - Subtle style
    """
    
    def __init__(self, text: str = "", parent=None, icon: str = None):
        super().__init__(text, parent)
        self.setup_ui()
        if icon:
            self.setIcon(icon)
    
    def setup_ui(self):
        """Setup UI"""
        self.setStyleSheet("""
            QPushButton {
                background-color: rgba(0, 0, 0, 0.05);
                color: #31302e;
                border: 1px solid rgba(0, 0, 0, 0.1);
                padding: 10px 20px;
                border-radius: 6px;
                font-weight: 500;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: rgba(0, 0, 0, 0.08);
                border-color: rgba(0, 0, 0, 0.2);
            }
            QPushButton:pressed {
                background-color: rgba(0, 0, 0, 0.12);
            }
            QPushButton:disabled {
                background-color: rgba(0, 0, 0, 0.05);
                color: #a39e98;
            }
        """)
        
        self.setMinimumSize(100, 40)
    
    def set_icon(self, icon_char: str):
        """Set icon character (emoji)"""
        if icon_char:
            self.setText(f"{icon_char} {self.text()}")


class DangerButton(QPushButton):
    """
    Danger button - Red style for destructive actions
    """
    
    def __init__(self, text: str = "", parent=None, icon: str = None):
        super().__init__(text, parent)
        self.setup_ui()
        if icon:
            self.setIcon(icon)
    
    def setup_ui(self):
        """Setup UI"""
        self.setStyleSheet("""
            QPushButton {
                background-color: #d32f2f;
                color: #ffffff;
                border: none;
                padding: 10px 20px;
                border-radius: 6px;
                font-weight: 600;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #b71c1c;
            }
            QPushButton:pressed {
                background-color: #8e0000;
            }
            QPushButton:disabled {
                background-color: #a39e98;
                color: #e8e8e8;
            }
        """)
        
        self.setMinimumSize(100, 40)
    
    def set_icon(self, icon_char: str):
        """Set icon character (emoji)"""
        if icon_char:
            self.setText(f"{icon_char} {self.text()}")


class IconButton(QToolButton):
    """
    Icon button - Small button with icon only
    """
    
    clicked_with_pos = pyqtSignal(int, int)  # x, y
    
    def __init__(self, icon_char: str = "", tooltip: str = "", parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.setText(icon_char)
        self.setToolTip(tooltip)
    
    def setup_ui(self):
        """Setup UI"""
        self.setStyleSheet("""
            QToolButton {
                background-color: transparent;
                border: 1px solid transparent;
                border-radius: 6px;
                padding: 6px 10px;
                font-size: 16px;
                color: #615d59;
            }
            QToolButton:hover {
                background-color: #f6f5f4;
                border-color: rgba(0, 0, 0, 0.1);
                color: #31302e;
            }
            QToolButton:pressed {
                background-color: #eeeeee;
            }
        """)
        
        self.setFixedSize(36, 36)
    
    def mousePressEvent(self, event):
        """Handle mouse press"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked_with_pos.emit(event.globalPosition().x(), event.globalPosition().y())
        super().mousePressEvent(event)


class ButtonGroup(QWidget):
    """
    Group of buttons with consistent spacing
    """
    
    def __init__(self, parent=None, orientation: str = "horizontal"):
        super().__init__(parent)
        self.orientation = orientation
        self.buttons = []
        self.setup_ui()
    
    def setup_ui(self):
        """Setup UI"""
        if self.orientation == "horizontal":
            self.layout = QHBoxLayout(self)
        else:
            self.layout = QVBoxLayout(self)
        
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(8)
    
    def add_button(self, button: QPushButton):
        """Add button to group"""
        self.layout.addWidget(button)
        self.buttons.append(button)
    
    def add_primary(self, text: str, icon: str = None) -> PrimaryButton:
        """Add primary button"""
        btn = PrimaryButton(text, icon=icon)
        self.add_button(btn)
        return btn
    
    def add_secondary(self, text: str, icon: str = None) -> SecondaryButton:
        """Add secondary button"""
        btn = SecondaryButton(text, icon=icon)
        self.add_button(btn)
        return btn
    
    def add_danger(self, text: str, icon: str = None) -> DangerButton:
        """Add danger button"""
        btn = DangerButton(text, icon=icon)
        self.add_button(btn)
        return btn
    
    def add_stretch(self):
        """Add stretch spacer"""
        self.layout.addStretch()
    
    def clear(self):
        """Clear all buttons"""
        for btn in self.buttons:
            self.layout.removeWidget(btn)
            btn.deleteLater()
        self.buttons.clear()


class ToggleButton(QPushButton):
    """
    Toggle button - On/Off state
    """
    
    toggled = pyqtSignal(bool)  # is_on
    
    def __init__(self, text_on: str = "Bật", text_off: str = "Tắt", parent=None):
        super().__init__(text_off, parent)
        self.text_on = text_on
        self.text_off = text_off
        self.is_on = False
        self.setup_ui()
        self.clicked.connect(self._toggle)
    
    def setup_ui(self):
        """Setup UI"""
        self._update_style()
        self.setMinimumSize(80, 40)
    
    def _update_style(self):
        """Update style based on state"""
        if self.is_on:
            self.setStyleSheet("""
                QPushButton {
                    background-color: #1aae39;
                    color: #ffffff;
                    border: none;
                    padding: 10px 20px;
                    border-radius: 20px;
                    font-weight: 600;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background-color: #159a32;
                }
                QPushButton:pressed {
                    background-color: #0f7a27;
                }
            """)
            self.setText(self.text_on)
        else:
            self.setStyleSheet("""
                QPushButton {
                    background-color: #f6f5f4;
                    color: #615d59;
                    border: 1px solid rgba(0, 0, 0, 0.1);
                    padding: 10px 20px;
                    border-radius: 20px;
                    font-weight: 500;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background-color: #eeeeee;
                }
                QPushButton:pressed {
                    background-color: #e0e0e0;
                }
            """)
            self.setText(self.text_off)
    
    def _toggle(self):
        """Toggle state"""
        self.is_on = not self.is_on
        self._update_style()
        self.toggled.emit(self.is_on)
    
    def set_on(self, on: bool):
        """Set state"""
        self.is_on = on
        self._update_style()


class LoadingButton(QPushButton):
    """
    Button with loading state
    """
    
    def __init__(self, text: str = "", parent=None):
        super().__init__(text, parent)
        self.loading = False
        self.original_text = text
        self.setup_ui()
    
    def setup_ui(self):
        """Setup UI"""
        self.setStyleSheet("""
            QPushButton {
                background-color: #0075de;
                color: #ffffff;
                border: none;
                padding: 10px 20px;
                border-radius: 6px;
                font-weight: 600;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #005bab;
            }
            QPushButton:pressed {
                background-color: #004494;
            }
            QPushButton:disabled {
                background-color: #a39e98;
                color: #e8e8e8;
            }
        """)
    
    def set_loading(self, loading: bool):
        """Set loading state"""
        self.loading = loading
        self.setEnabled(not loading)
        
        if loading:
            self.setText("⏳ Đang xử lý...")
        else:
            self.setText(self.original_text)


__all__ = [
    'PrimaryButton',
    'SecondaryButton',
    'DangerButton',
    'IconButton',
    'ButtonGroup',
    'ToggleButton',
    'LoadingButton',
]
