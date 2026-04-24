#!/usr/bin/env python3
"""
Search Box Widget - Input tìm kiếm với real-time search, clear button
"""
from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QLineEdit, QPushButton, QLabel,
    QCompleter, QFrame, QVBoxLayout, QListWidget, QListWidgetItem
)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from PyQt6.QtGui import QIcon, QAction


class SearchBox(QFrame):
    """
    Enhanced search box với features:
    - Real-time search (debounced)
    - Clear button
    - Search history
    - Auto-complete suggestions
    - Custom styling
    """
    
    # Signals
    search_changed = pyqtSignal(str)  # search_text
    search_submitted = pyqtSignal(str)  # search_text (on Enter)
    cleared = pyqtSignal()
    
    def __init__(self, parent=None, placeholder: str = "🔍 Tìm kiếm..."):
        super().__init__(parent)
        self.placeholder_text = placeholder
        self.setup_ui()
        self.setup_connections()
        
        # Search history
        self.history: list = []
        self.max_history = 20
        
        # Debounce timer
        self.debounce_timer = QTimer()
        self.debounce_timer.setSingleShot(True)
        self.debounce_timer.timeout.connect(self._emit_search)
        self.debounce_delay = 300  # ms
        
        # Completer
        self._setup_completer()
    
    def setup_ui(self):
        """Setup UI"""
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border: 2px solid rgba(0, 0, 0, 0.1);
                border-radius: 8px;
                padding: 2px;
            }
            QFrame:focus-within {
                border-color: #1976d2;
            }
            QLineEdit {
                background-color: transparent;
                border: none;
                padding: 8px 12px;
                font-size: 14px;
                color: #31302e;
            }
            QLineEdit::placeholder {
                color: #a39e98;
            }
            QPushButton {
                background-color: transparent;
                border: none;
                padding: 4px 8px;
                border-radius: 4px;
                color: #615d59;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #f6f5f4;
            }
            QPushButton:pressed {
                background-color: #eeeeee;
            }
        """)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 4, 8, 4)
        layout.setSpacing(4)
        
        # Search icon
        search_icon = QLabel("🔍")
        search_icon.setStyleSheet("font-size: 16px; padding: 4px;")
        layout.addWidget(search_icon)
        
        # Search input
        self.input = QLineEdit()
        self.input.setPlaceholderText(self.placeholder_text)
        layout.addWidget(self.input, 1)
        
        # Clear button (hidden by default)
        self.clear_btn = QPushButton("✕")
        self.clear_btn.setVisible(False)
        self.clear_btn.setFixedSize(24, 24)
        layout.addWidget(self.clear_btn)
        
        # History button
        self.history_btn = QPushButton("🕐")
        self.history_btn.setFixedSize(24, 24)
        layout.addWidget(self.history_btn)
    
    def setup_connections(self):
        """Setup signal connections"""
        self.input.textChanged.connect(self._on_text_changed)
        self.input.returnPressed.connect(self._on_return_pressed)
        self.clear_btn.clicked.connect(self.clear)
        self.history_btn.clicked.connect(self._toggle_history)
    
    def _setup_completer(self):
        """Setup auto-completer"""
        self.completer = QCompleter()
        self.completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.completer.setFilterMode(Qt.MatchFlag.MatchContains)
        self.completer.activated.connect(self._on_completer_activated)
        self.input.setCompleter(self.completer)
    
    def _on_text_changed(self, text: str):
        """Handle text change"""
        # Show/hide clear button
        self.clear_btn.setVisible(bool(text.strip()))
        
        # Debounce search
        self.debounce_timer.stop()
        self.debounce_timer.start(self.debounce_delay)
    
    def _emit_search(self):
        """Emit search signal after debounce"""
        text = self.input.text().strip()
        self.search_changed.emit(text)
    
    def _on_return_pressed(self):
        """Handle Enter key"""
        text = self.input.text().strip()
        if text:
            self.search_submitted.emit(text)
            self._add_to_history(text)
    
    def _on_completer_activated(self, text: str):
        """Handle completer selection"""
        self.input.setText(text)
        self.search_submitted.emit(text)
    
    def _toggle_history(self):
        """Toggle history popup"""
        # TODO: Implement history popup
        pass
    
    def _add_to_history(self, text: str):
        """Add text to search history"""
        if text and text not in self.history:
            self.history.insert(0, text)
            if len(self.history) > self.max_history:
                self.history.pop()
            self._update_completer()
    
    def _update_completer(self):
        """Update completer with history"""
        self.completer.setModelFromStringList(self.history)
    
    def clear(self):
        """Clear search"""
        self.input.clear()
        self.clear_btn.setVisible(False)
        self.cleared.emit()
        self.search_changed.emit("")
    
    def get_text(self) -> str:
        """Get search text"""
        return self.input.text().strip()
    
    def set_text(self, text: str):
        """Set search text"""
        self.input.setText(text)
        self.clear_btn.setVisible(bool(text.strip()))
    
    def set_placeholder(self, text: str):
        """Set placeholder text"""
        self.input.setPlaceholderText(text)
    
    def enable_history(self, enabled: bool):
        """Enable/disable history button"""
        self.history_btn.setVisible(enabled)
    
    def set_debounce_delay(self, delay_ms: int):
        """Set debounce delay in milliseconds"""
        self.debounce_delay = delay_ms
    
    def focus(self):
        """Focus search input"""
        self.input.setFocus()


class AdvancedSearchBox(QWidget):
    """
    Advanced search box với filters
    """
    
    search_changed = pyqtSignal(dict)  # {text, filters}
    
    def __init__(self, parent=None, filters: list = None):
        super().__init__(parent)
        self.filters = filters or []
        self.setup_ui()
        self.setup_connections()
    
    def setup_ui(self):
        """Setup UI"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)
        
        # Search box
        self.search_box = SearchBox()
        layout.addWidget(self.search_box, 1)
        
        # Filter dropdowns
        self.filter_widgets = {}
        for filter_def in self.filters:
            name = filter_def.get('name', 'filter')
            label = filter_def.get('label', name)
            options = filter_def.get('options', [])
            
            from PyQt6.QtWidgets import QComboBox
            
            combo = QComboBox()
            combo.addItem(f"Tất cả {label}", "")
            for opt in options:
                combo.addItem(opt, opt)
            
            combo.setStyleSheet("""
                QComboBox {
                    padding: 8px 12px;
                    border: 1px solid rgba(0, 0, 0, 0.2);
                    border-radius: 4px;
                    min-width: 150px;
                }
                QComboBox:focus {
                    border-color: #1976d2;
                }
            """)
            
            layout.addWidget(combo)
            self.filter_widgets[name] = combo
    
    def setup_connections(self):
        """Setup signal connections"""
        self.search_box.search_changed.connect(self._emit_search)
        self.search_box.search_submitted.connect(self._emit_search)
        
        for combo in self.filter_widgets.values():
            combo.currentIndexChanged.connect(self._emit_search)
    
    def _emit_search(self, *args):
        """Emit search signal with all filters"""
        data = {
            'text': self.search_box.get_text(),
            'filters': {}
        }
        
        for name, combo in self.filter_widgets.items():
            data['filters'][name] = combo.currentData()
        
        self.search_changed.emit(data)
    
    def get_search_data(self) -> dict:
        """Get current search data"""
        return {
            'text': self.search_box.get_text(),
            'filters': {
                name: combo.currentData()
                for name, combo in self.filter_widgets.items()
            }
        }
    
    def clear(self):
        """Clear all filters"""
        self.search_box.clear()
        for combo in self.filter_widgets.values():
            combo.setCurrentIndex(0)


__all__ = ['SearchBox', 'AdvancedSearchBox']
