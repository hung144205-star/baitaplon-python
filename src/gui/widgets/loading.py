#!/usr/bin/env python3
"""
Loading Widget - Loading spinner và loading overlay
"""
from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QProgressBar, QFrame, QGraphicsOpacityEffect
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QMovie


class LoadingSpinner(QWidget):
    """
    Loading spinner widget
    """
    
    def __init__(self, parent=None, size: int = 40, color: str = "#1976d2"):
        super().__init__(parent)
        self.size = size
        self.color = color
        self.setup_ui()
    
    def setup_ui(self):
        """Setup UI"""
        self.setFixedSize(self.size, self.size)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Loading label with spinning animation
        self.spinner = QLabel("⏳")
        self.spinner.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.spinner.setStyleSheet(f"font-size: {self.size}px; color: {self.color};")
        
        # Create rotation animation
        from PyQt6.QtCore import QPropertyAnimation, QEasingCurve
        self.rotation = 0
        
        self.timer = QTimer()
        self.timer.timeout.connect(self._rotate)
        self.timer.start(50)  # Update every 50ms
        
        layout.addWidget(self.spinner)
    
    def _rotate(self):
        """Rotate spinner"""
        self.rotation = (self.rotation + 10) % 360
        # Note: QLabel doesn't support rotation directly
        # For production, use QMovie with GIF or custom paintEvent
    
    def start(self):
        """Start animation"""
        self.timer.start(50)
        self.setVisible(True)
    
    def stop(self):
        """Stop animation"""
        self.timer.stop()
        self.setVisible(False)
    
    def set_color(self, color: str):
        """Set spinner color"""
        self.color = color
        self.spinner.setStyleSheet(f"font-size: {self.size}px; color: {self.color};")


class LoadingOverlay(QWidget):
    """
    Loading overlay - Covers parent widget with loading indicator
    """
    
    def __init__(self, parent=None, message: str = "Đang tải..."):
        super().__init__(parent)
        self.message = message
        self.setup_ui()
    
    def setup_ui(self):
        """Setup UI"""
        # Semi-transparent background
        self.setStyleSheet("""
            QWidget {
                background-color: rgba(255, 255, 255, 0.8);
            }
        """)
        
        # Main layout
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(20)
        
        # Spinner
        self.spinner = LoadingSpinner(size=60)
        layout.addWidget(self.spinner, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Message
        self.message_label = QLabel(self.message)
        self.message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.message_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                color: #31302e;
                font-weight: 500;
                padding: 10px;
            }
        """)
        layout.addWidget(self.message_label, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Start hidden
        self.hide()
    
    def set_message(self, message: str):
        """Set loading message"""
        self.message = message
        self.message_label.setText(message)
    
    def show_loading(self, message: str = None):
        """Show loading overlay"""
        if message:
            self.set_message(message)
        self.show()
        self.spinner.start()
        self.raise_()  # Bring to front
    
    def hide_loading(self):
        """Hide loading overlay"""
        self.hide()
        self.spinner.stop()


class LoadingProgressBar(QProgressBar):
    """
    Progress bar với loading animation
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        """Setup UI"""
        self.setStyleSheet("""
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
        
        self.setMinimum(0)
        self.setMaximum(0)  # Indeterminate mode
        self.setTextVisible(False)
    
    def start(self):
        """Start indeterminate animation"""
        self.setMaximum(0)
    
    def stop(self):
        """Stop animation"""
        self.setMaximum(100)
        self.setValue(100)
    
    def set_progress(self, value: int):
        """Set progress value (0-100)"""
        self.setMaximum(100)
        self.setValue(value)


class LoadingDialog(QFrame):
    """
    Loading dialog - Modal loading indicator
    """
    
    def __init__(self, parent=None, title: str = "Đang xử lý", message: str = ""):
        super().__init__(parent)
        self.title = title
        self.message = message
        self.setup_ui()
    
    def setup_ui(self):
        """Setup UI"""
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border: 1px solid rgba(0, 0, 0, 0.1);
                border-radius: 12px;
                padding: 40px;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(20)
        
        # Spinner
        self.spinner = LoadingSpinner(size=80)
        layout.addWidget(self.spinner, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Title
        self.title_label = QLabel(self.title)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet("""
            QLabel {
                font-size: 20px;
                color: #31302e;
                font-weight: 700;
            }
        """)
        layout.addWidget(self.title_label, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Message
        if self.message:
            self.message_label = QLabel(self.message)
            self.message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.message_label.setStyleSheet("""
                QLabel {
                    font-size: 14px;
                    color: #615d59;
                    padding: 10px;
                }
            """)
            layout.addWidget(self.message_label, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.hide()
    
    def show_loading(self, title: str = None, message: str = None):
        """Show loading dialog"""
        if title:
            self.title = title
            self.title_label.setText(title)
        if message:
            self.message = message
            self.message_label.setText(message)
        
        self.show()
        self.spinner.start()
    
    def hide_loading(self):
        """Hide loading dialog"""
        self.hide()
        self.spinner.stop()


class ProgressStep(QFrame):
    """
    Single step in a progress stepper
    """
    
    def __init__(self, parent=None, step_number: int = 1, title: str = "", completed: bool = False):
        super().__init__(parent)
        self.step_number = step_number
        self.title = title
        self.completed = completed
        self.setup_ui()
    
    def setup_ui(self):
        """Setup UI"""
        self.setFrameShape(QFrame.Shape.NoFrame)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)
        
        # Circle
        self.circle = QLabel(str(self.step_number))
        self.circle.setFixedSize(40, 40)
        self.circle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.circle.setStyleSheet(self._get_circle_style())
        layout.addWidget(self.circle)
        
        # Title
        if self.title:
            self.title_label = QLabel(self.title)
            self.title_label.setStyleSheet(self._get_title_style())
            layout.addWidget(self.title_label, 1)
    
    def _get_circle_style(self) -> str:
        """Get circle style based on state"""
        if self.completed:
            return """
                QLabel {
                    background-color: #1aae39;
                    color: #ffffff;
                    border-radius: 20px;
                    font-weight: 600;
                    font-size: 16px;
                }
            """
        else:
            return """
                QLabel {
                    background-color: #f6f5f4;
                    color: #615d59;
                    border: 2px solid rgba(0, 0, 0, 0.1);
                    border-radius: 20px;
                    font-weight: 600;
                    font-size: 16px;
                }
            """
    
    def _get_title_style(self) -> str:
        """Get title style based on state"""
        if self.completed:
            return """
                QLabel {
                    color: #1aae39;
                    font-weight: 600;
                    font-size: 14px;
                }
            """
        else:
            return """
                QLabel {
                    color: #615d59;
                    font-size: 14px;
                }
            """
    
    def set_completed(self, completed: bool):
        """Set completion state"""
        self.completed = completed
        self.circle.setStyleSheet(self._get_circle_style())
        if self.title:
            self.title_label.setStyleSheet(self._get_title_style())


class ProgressStepper(QWidget):
    """
    Multi-step progress stepper
    """
    
    def __init__(self, parent=None, steps: list = None):
        super().__init__(parent)
        self.steps = steps or ["Bước 1", "Bước 2", "Bước 3"]
        self.current_step = 0
        self.setup_ui()
    
    def setup_ui(self):
        """Setup UI"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 20, 0, 20)
        layout.setSpacing(0)
        
        self.step_widgets = []
        
        for i, step_title in enumerate(self.steps):
            # Step
            step = ProgressStep(step_number=i+1, title=step_title, completed=(i < self.current_step))
            layout.addWidget(step)
            self.step_widgets.append(step)
            
            # Connector line (except last step)
            if i < len(self.steps) - 1:
                line = QFrame()
                line.setFrameShape(QFrame.Shape.HLine)
                line.setFixedHeight(2)
                line.setStyleSheet("""
                    QFrame {
                        background-color: #e0e0e0;
                    }
                """)
                layout.addWidget(line, 1)
    
    def set_current_step(self, step: int):
        """Set current step (0-indexed)"""
        self.current_step = step
        
        for i, step_widget in enumerate(self.step_widgets):
            step_widget.set_completed(i < step)
    
    def next_step(self):
        """Go to next step"""
        if self.current_step < len(self.steps) - 1:
            self.set_current_step(self.current_step + 1)
    
    def prev_step(self):
        """Go to previous step"""
        if self.current_step > 0:
            self.set_current_step(self.current_step - 1)
    
    def reset(self):
        """Reset to first step"""
        self.set_current_step(0)


__all__ = [
    'LoadingSpinner',
    'LoadingOverlay',
    'LoadingProgressBar',
    'LoadingDialog',
    'ProgressStep',
    'ProgressStepper',
]
