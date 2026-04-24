#!/usr/bin/env python3
"""
Dialog Widgets - Các loại dialog windows
"""
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QTextEdit, QComboBox, QDateEdit, QSpinBox,
    QDoubleSpinBox, QFrame, QProgressBar, QWidget
)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from PyQt6.QtGui import QFont


class MessageDialog(QDialog):
    """
    Message dialog với các loại: Info, Warning, Error, Success
    """
    
    def __init__(self, parent=None, title: str = "", message: str = "", 
                 dialog_type: str = "info"):
        super().__init__(parent)
        self.dialog_type = dialog_type
        self.title_text = title
        self.message_text = message
        self.setup_ui()
    
    def setup_ui(self):
        """Setup UI"""
        self.setWindowTitle(self.title_text)
        self.setMinimumWidth(400)
        self.setModal(True)
        
        # Set dialog style based on type
        self.setStyleSheet(self._get_dialog_style())
        
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(40, 40, 40, 40)
        
        # Icon and message container
        container = QHBoxLayout()
        container.setSpacing(20)
        
        # Icon
        icon_label = QLabel(self._get_icon())
        icon_label.setStyleSheet("font-size: 48px;")
        container.addWidget(icon_label)
        
        # Message
        message_label = QLabel(self.message_text)
        message_label.setWordWrap(True)
        message_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #31302e;
                line-height: 1.5;
            }
        """)
        container.addWidget(message_label, 1)
        
        layout.addLayout(container)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        ok_btn = QPushButton("OK")
        ok_btn.setObjectName("primaryButton")
        ok_btn.setFixedWidth(100)
        ok_btn.clicked.connect(self.accept)
        button_layout.addWidget(ok_btn)
        
        layout.addLayout(button_layout)
    
    def _get_dialog_style(self) -> str:
        """Get style based on dialog type"""
        return """
            QDialog {
                background-color: #ffffff;
                border: 1px solid rgba(0, 0, 0, 0.1);
                border-radius: 12px;
            }
            QPushButton#primaryButton {
                background-color: #0075de;
                color: #ffffff;
                border: none;
                padding: 10px 20px;
                border-radius: 6px;
                font-weight: 600;
            }
            QPushButton#primaryButton:hover {
                background-color: #005bab;
            }
        """
    
    def _get_icon(self) -> str:
        """Get icon based on dialog type"""
        icons = {
            "info": "ℹ️",
            "warning": "⚠️",
            "error": "❌",
            "success": "✅",
        }
        return icons.get(self.dialog_type, "ℹ️")
    
    @staticmethod
    def info(parent, title: str, message: str):
        """Show info dialog"""
        dialog = MessageDialog(parent, title, message, "info")
        return dialog.exec()
    
    @staticmethod
    def warning(parent, title: str, message: str):
        """Show warning dialog"""
        dialog = MessageDialog(parent, title, message, "warning")
        return dialog.exec()
    
    @staticmethod
    def error(parent, title: str, message: str):
        """Show error dialog"""
        dialog = MessageDialog(parent, title, message, "error")
        return dialog.exec()
    
    @staticmethod
    def success(parent, title: str, message: str):
        """Show success dialog"""
        dialog = MessageDialog(parent, title, message, "success")
        return dialog.exec()


class ConfirmDialog(QDialog):
    """
    Confirmation dialog cho các hành động
    """
    
    confirmed = pyqtSignal(bool)  # is_confirmed
    
    def __init__(self, parent=None, title: str = "Xác nhận",
                 message: str = "Bạn có chắc chắn không?",
                 confirm_text: str = "Xác nhận",
                 cancel_text: str = "Hủy",
                 dialog_type: str = "warning"):
        super().__init__(parent)
        self.title_text = title
        self.message_text = message
        self.confirm_text = confirm_text
        self.cancel_text = cancel_text
        self.dialog_type = dialog_type
        self.setup_ui()
    
    def setup_ui(self):
        """Setup UI"""
        self.setWindowTitle(self.title_text)
        self.setMinimumWidth(450)
        self.setModal(True)
        self.setStyleSheet("""
            QDialog {
                background-color: #ffffff;
                border: 1px solid rgba(0, 0, 0, 0.1);
                border-radius: 12px;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(40, 40, 40, 40)
        
        # Icon and message
        container = QHBoxLayout()
        container.setSpacing(20)
        
        icon = QLabel("⚠️" if self.dialog_type == "warning" else "❓")
        icon.setStyleSheet("font-size: 48px;")
        container.addWidget(icon)
        
        message = QLabel(self.message_text)
        message.setWordWrap(True)
        message.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #31302e;
                line-height: 1.5;
            }
        """)
        container.addWidget(message, 1)
        
        layout.addLayout(container)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        # Cancel button
        cancel_btn = QPushButton(self.cancel_text)
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #f6f5f4;
                color: #31302e;
                border: 1px solid rgba(0, 0, 0, 0.1);
                padding: 10px 20px;
                border-radius: 6px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #eeeeee;
            }
        """)
        cancel_btn.setFixedWidth(120)
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        # Confirm button
        confirm_btn = QPushButton(self.confirm_text)
        confirm_btn.setObjectName("confirmButton")
        if self.dialog_type == "danger":
            confirm_btn.setStyleSheet("""
                QPushButton#confirmButton {
                    background-color: #d32f2f;
                    color: #ffffff;
                    border: none;
                    padding: 10px 20px;
                    border-radius: 6px;
                    font-weight: 600;
                }
                QPushButton#confirmButton:hover {
                    background-color: #b71c1c;
                }
            """)
        else:
            confirm_btn.setStyleSheet("""
                QPushButton#confirmButton {
                    background-color: #0075de;
                    color: #ffffff;
                    border: none;
                    padding: 10px 20px;
                    border-radius: 6px;
                    font-weight: 600;
                }
                QPushButton#confirmButton:hover {
                    background-color: #005bab;
                }
            """)
        confirm_btn.setFixedWidth(120)
        confirm_btn.clicked.connect(self._on_confirm)
        button_layout.addWidget(confirm_btn)
        
        layout.addLayout(button_layout)
    
    def _on_confirm(self):
        """Handle confirm click"""
        self.confirmed.emit(True)
        self.accept()
    
    @staticmethod
    def ask(parent, message: str, title: str = "Xác nhận") -> bool:
        """Show confirmation dialog"""
        dialog = ConfirmDialog(parent, title, message)
        return dialog.exec() == QDialog.DialogCode.Accepted
    
    @staticmethod
    def ask_delete(parent, item_name: str) -> bool:
        """Show delete confirmation"""
        message = f"Bạn có chắc chắn muốn xóa <b>{item_name}</b>?\n\nHành động này không thể hoàn tác."
        dialog = ConfirmDialog(
            parent, "Xác nhận xóa", message,
            confirm_text="Xóa", cancel_text="Hủy",
            dialog_type="danger"
        )
        return dialog.exec() == QDialog.DialogCode.Accepted


class InputDialog(QDialog):
    """
    Input dialog cho text, number, date
    """
    
    accepted_with_value = pyqtSignal(object)  # value
    
    def __init__(self, parent=None, title: str = "Nhập liệu",
                 label: str = "", input_type: str = "text",
                 default_value = None, placeholder: str = ""):
        super().__init__(parent)
        self.title_text = title
        self.label_text = label
        self.input_type = input_type
        self.default_value = default_value
        self.placeholder_text = placeholder
        self.result_value = None
        self.setup_ui()
    
    def setup_ui(self):
        """Setup UI"""
        self.setWindowTitle(self.title_text)
        self.setMinimumWidth(400)
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
        """)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Label
        if self.label_text:
            label = QLabel(self.label_text)
            layout.addWidget(label)
        
        # Input widget
        self.input_widget = self._create_input()
        layout.addWidget(self.input_widget)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        cancel_btn = QPushButton("Hủy")
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #f6f5f4;
                color: #31302e;
                border: 1px solid rgba(0, 0, 0, 0.1);
                padding: 10px 20px;
                border-radius: 6px;
                font-weight: 500;
            }
        """)
        cancel_btn.setFixedWidth(100)
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        ok_btn = QPushButton("OK")
        ok_btn.setStyleSheet("""
            QPushButton {
                background-color: #0075de;
                color: #ffffff;
                border: none;
                padding: 10px 20px;
                border-radius: 6px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #005bab;
            }
        """)
        ok_btn.setFixedWidth(100)
        ok_btn.clicked.connect(self._on_accept)
        button_layout.addWidget(ok_btn)
        
        layout.addLayout(button_layout)
    
    def _create_input(self):
        """Create input widget based on type"""
        if self.input_type == "text":
            widget = QLineEdit()
            widget.setPlaceholderText(self.placeholder_text)
            if self.default_value:
                widget.setText(str(self.default_value))
        elif self.input_type == "number":
            widget = QSpinBox()
            widget.setMinimum(0)
            widget.setMaximum(999999)
            if self.default_value:
                widget.setValue(int(self.default_value))
        elif self.input_type == "double":
            widget = QDoubleSpinBox()
            widget.setMinimum(0.0)
            widget.setMaximum(999999.99)
            widget.setDecimals(2)
            if self.default_value:
                widget.setValue(float(self.default_value))
        elif self.input_type == "date":
            from PyQt6.QtCore import QDate
            widget = QDateEdit()
            widget.setCalendarPopup(True)
            if self.default_value:
                widget.setDate(self.default_value)
            else:
                widget.setDate(QDate.currentDate())
        elif self.input_type == "multilinetext":
            widget = QTextEdit()
            widget.setPlaceholderText(self.placeholder_text)
            widget.setMaximumHeight(150)
            if self.default_value:
                widget.setText(str(self.default_value))
        else:
            widget = QLineEdit()
        
        widget.setStyleSheet("""
            QLineEdit, QTextEdit, QSpinBox, QDoubleSpinBox, QDateEdit {
                padding: 10px 12px;
                border: 1px solid rgba(0, 0, 0, 0.2);
                border-radius: 6px;
                font-size: 14px;
            }
            QLineEdit:focus, QTextEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus, QDateEdit:focus {
                border-color: #1976d2;
            }
        """)
        
        return widget
    
    def _on_accept(self):
        """Handle accept"""
        if isinstance(self.input_widget, QLineEdit):
            self.result_value = self.input_widget.text()
        elif isinstance(self.input_widget, QTextEdit):
            self.result_value = self.input_widget.toPlainText()
        elif isinstance(self.input_widget, (QSpinBox, QDoubleSpinBox)):
            self.result_value = self.input_widget.value()
        elif isinstance(self.input_widget, QDateEdit):
            self.result_value = self.input_widget.date()
        
        self.accepted_with_value.emit(self.result_value)
        self.accept()
    
    @staticmethod
    def get_text(parent, label: str, title: str = "Nhập", 
                 default: str = "", placeholder: str = "") -> str:
        """Get text input"""
        dialog = InputDialog(parent, title, label, "text", default, placeholder)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            return dialog.result_value
        return None
    
    @staticmethod
    def get_number(parent, label: str, title: str = "Nhập số",
                   default: int = 0) -> int:
        """Get number input"""
        dialog = InputDialog(parent, title, label, "number", default)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            return dialog.result_value
        return None


class ProgressDialog(QDialog):
    """
    Progress dialog với progress bar
    """
    
    cancelled = pyqtSignal()
    
    def __init__(self, parent=None, title: str = "Đang xử lý",
                 message: str = "", show_cancel: bool = True,
                 total: int = 0):
        super().__init__(parent)
        self.title_text = title
        self.message_text = message
        self.show_cancel = show_cancel
        self.total = total
        self.setup_ui()
    
    def setup_ui(self):
        """Setup UI"""
        self.setWindowTitle(self.title_text)
        self.setMinimumWidth(400)
        self.setModal(True)
        self.setWindowFlags(
            self.windowFlags() & ~Qt.WindowType.WindowCloseButtonHint
        )
        self.setStyleSheet("""
            QDialog {
                background-color: #ffffff;
                border: 1px solid rgba(0, 0, 0, 0.1);
                border-radius: 12px;
            }
            QLabel {
                color: #31302e;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(40, 40, 40, 40)
        
        # Loading spinner
        spinner = QLabel("⏳")
        spinner.setStyleSheet("font-size: 48px;")
        spinner.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(spinner)
        
        # Message
        self.message_label = QLabel(self.message_text)
        self.message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.message_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #615d59;
            }
        """)
        layout.addWidget(self.message_label)
        
        # Progress bar
        if self.total > 0:
            self.progress_bar = QProgressBar()
            self.progress_bar.setMaximum(self.total)
            self.progress_bar.setStyleSheet("""
                QProgressBar {
                    background-color: #f6f5f4;
                    border: none;
                    border-radius: 4px;
                    height: 8px;
                    text-align: center;
                }
                QProgressBar::chunk {
                    background-color: #0075de;
                    border-radius: 4px;
                }
            """)
            layout.addWidget(self.progress_bar)
        else:
            # Indeterminate progress
            self.progress_bar = QProgressBar()
            self.progress_bar.setMaximum(0)
            self.progress_bar.setMinimum(0)
            self.progress_bar.setTextVisible(False)
            self.progress_bar.setStyleSheet("""
                QProgressBar {
                    background-color: #f6f5f4;
                    border: none;
                    border-radius: 4px;
                    height: 8px;
                }
                QProgressBar::chunk {
                    background-color: #0075de;
                    border-radius: 4px;
                }
            """)
            layout.addWidget(self.progress_bar)
        
        # Cancel button
        if self.show_cancel:
            cancel_btn = QPushButton("Hủy")
            cancel_btn.setStyleSheet("""
                QPushButton {
                    background-color: #f6f5f4;
                    color: #31302e;
                    border: 1px solid rgba(0, 0, 0, 0.1);
                    padding: 10px 20px;
                    border-radius: 6px;
                    font-weight: 500;
                }
            """)
            cancel_btn.setFixedWidth(120)
            cancel_btn.clicked.connect(self._on_cancel)
            
            button_layout = QHBoxLayout()
            button_layout.addStretch()
            button_layout.addWidget(cancel_btn)
            button_layout.addStretch()
            layout.addLayout(button_layout)
    
    def _on_cancel(self):
        """Handle cancel"""
        self.cancelled.emit()
        self.reject()
    
    def set_progress(self, value: int):
        """Set progress value"""
        self.progress_bar.setValue(value)
    
    def set_message(self, message: str):
        """Set message"""
        self.message_text = message
        self.message_label.setText(message)


class FormDialog(QDialog):
    """
    Generic form dialog với multiple fields
    """
    
    accepted_with_data = pyqtSignal(dict)  # form_data
    
    def __init__(self, parent=None, title: str = "Nhập thông tin",
                 fields: list = None):
        """
        Args:
            fields: List of field dicts:
                {
                    "name": "field_name",
                    "label": "Field Label",
                    "type": "text|number|date|combobox|textarea",
                    "required": True,
                    "placeholder": "Placeholder text",
                    "default": "default value",
                    "options": ["option1", "option2"]  # for combobox
                }
        """
        super().__init__(parent)
        self.title_text = title
        self.fields = fields or []
        self.input_widgets = {}
        self.setup_ui()
    
    def setup_ui(self):
        """Setup UI"""
        self.setWindowTitle(self.title_text)
        self.setMinimumWidth(500)
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
        """)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Form fields
        for field in self.fields:
            field_widget = self._create_field(field)
            layout.addWidget(field_widget)
        
        layout.addStretch()
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        cancel_btn = QPushButton("Hủy")
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #f6f5f4;
                color: #31302e;
                border: 1px solid rgba(0, 0, 0, 0.1);
                padding: 10px 20px;
                border-radius: 6px;
                font-weight: 500;
            }
        """)
        cancel_btn.setFixedWidth(100)
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        ok_btn = QPushButton("Lưu")
        ok_btn.setStyleSheet("""
            QPushButton {
                background-color: #0075de;
                color: #ffffff;
                border: none;
                padding: 10px 20px;
                border-radius: 6px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #005bab;
            }
        """)
        ok_btn.setFixedWidth(100)
        ok_btn.clicked.connect(self._on_accept)
        button_layout.addWidget(ok_btn)
        
        layout.addLayout(button_layout)
    
    def _create_field(self, field: dict) -> QWidget:
        """Create field widget"""
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)
        
        # Label
        label = QLabel(field.get("label", field.get("name", "")))
        if field.get("required", False):
            label.setText(label.text() + " <span style='color: #d32f2f;'>*</span>")
        layout.addWidget(label)
        
        # Input
        input_type = field.get("type", "text")
        input_widget = self._create_input(input_type, field)
        layout.addWidget(input_widget)
        
        self.input_widgets[field.get("name")] = {
            "widget": input_widget,
            "type": input_type,
            "required": field.get("required", False)
        }
        
        return container
    
    def _create_input(self, input_type: str, field: dict):
        """Create input widget"""
        if input_type == "text":
            widget = QLineEdit()
            widget.setPlaceholderText(field.get("placeholder", ""))
            if field.get("default"):
                widget.setText(str(field["default"]))
        elif input_type == "number":
            widget = QSpinBox()
            widget.setMinimum(field.get("min", 0))
            widget.setMaximum(field.get("max", 999999))
            if field.get("default"):
                widget.setValue(int(field["default"]))
        elif input_type == "date":
            from PyQt6.QtCore import QDate
            widget = QDateEdit()
            widget.setCalendarPopup(True)
            if field.get("default"):
                widget.setDate(field["default"])
            else:
                widget.setDate(QDate.currentDate())
        elif input_type == "combobox":
            widget = QComboBox()
            for option in field.get("options", []):
                widget.addItem(option)
            if field.get("default") and field.get("default") in field.get("options", []):
                widget.setCurrentText(field["default"])
        elif input_type == "textarea":
            widget = QTextEdit()
            widget.setPlaceholderText(field.get("placeholder", ""))
            widget.setMaximumHeight(100)
            if field.get("default"):
                widget.setText(str(field["default"]))
        else:
            widget = QLineEdit()
        
        widget.setStyleSheet("""
            QLineEdit, QTextEdit, QSpinBox, QDoubleSpinBox, QDateEdit, QComboBox {
                padding: 10px 12px;
                border: 1px solid rgba(0, 0, 0, 0.2);
                border-radius: 6px;
                font-size: 14px;
            }
            QLineEdit:focus, QTextEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus, QDateEdit:focus, QComboBox:focus {
                border-color: #1976d2;
            }
        """)
        
        return widget
    
    def _on_accept(self):
        """Handle accept with validation"""
        data = {}
        
        for name, info in self.input_widgets.items():
            widget = info["widget"]
            widget_type = info["type"]
            required = info["required"]
            
            # Get value
            if widget_type == "text":
                value = widget.text().strip()
            elif widget_type == "textarea":
                value = widget.toPlainText().strip()
            elif widget_type == "number":
                value = widget.value()
            elif widget_type == "date":
                value = widget.date()
            elif widget_type == "combobox":
                value = widget.currentText()
            else:
                value = widget.text().strip() if hasattr(widget, "text") else None
            
            # Validate required
            if required and not value:
                MessageDialog.error(self, "Lỗi", f"Vui lòng nhập {name}")
                return
            
            data[name] = value
        
        self.accepted_with_data.emit(data)
        self.accept()


__all__ = [
    'MessageDialog',
    'ConfirmDialog',
    'InputDialog',
    'ProgressDialog',
    'FormDialog',
]
