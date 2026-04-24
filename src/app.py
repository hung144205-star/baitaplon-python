#!/usr/bin/env python3
"""
Quản Lý Kho Lưu trữ - Application Entry Point
Nhóm 12 - Lập trình Python

Usage:
    python src/app.py
"""
import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt, QCoreApplication
from PyQt6.QtGui import QFont, QIcon

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.main_window import MainWindow
from src.database import get_session

class Application(QApplication):
    """
    Main Application class
    """
    
    def __init__(self):
        super().__init__(sys.argv)
        
        # Application metadata
        QCoreApplication.setApplicationName("Quản Lý Kho Lưu Trữ")
        QCoreApplication.setApplicationVersion("1.0.0")
        QCoreApplication.setOrganizationName("Nhóm 12")
        QCoreApplication.setOrganizationDomain("warehouse.local")
        
        # Setup application
        self._setup_style()
        self._setup_font()
        
        # Create main window
        self.main_window = MainWindow()
        
    def _setup_style(self):
        """Setup application stylesheet"""
        # Load main stylesheet
        style_file = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'gui',
            'styles',
            'main.qss'
        )
        
        if os.path.exists(style_file):
            with open(style_file, 'r', encoding='utf-8') as f:
                stylesheet = f.read()
            self.setStyleSheet(stylesheet)
            print(f"✅ Loaded stylesheet: {style_file}")
        else:
            # Default minimal style
            self.setStyleSheet("""
                QMainWindow {
                    background-color: #f5f5f5;
                }
                QMenuBar {
                    background-color: #ffffff;
                    border-bottom: 1px solid #e0e0e0;
                }
                QMenuBar::item:selected {
                    background-color: #e3f2fd;
                }
                QToolBar {
                    background-color: #ffffff;
                    border-bottom: 1px solid #e0e0e0;
                    spacing: 5px;
                    padding: 5px;
                }
                QStatusBar {
                    background-color: #ffffff;
                    border-top: 1px solid #e0e0e0;
                }
                QPushButton {
                    background-color: #1976d2;
                    color: white;
                    border: none;
                    padding: 8px 16px;
                    border-radius: 4px;
                    font-weight: 500;
                }
                QPushButton:hover {
                    background-color: #1565c0;
                }
                QPushButton:pressed {
                    background-color: #0d47a1;
                }
                QTableWidget {
                    background-color: #ffffff;
                    alternate-background-color: #f5f5f5;
                    border: 1px solid #e0e0e0;
                    gridline-color: #e0e0e0;
                }
                QTableWidget::item:selected {
                    background-color: #e3f2fd;
                    color: #1976d2;
                }
                QHeaderView::section {
                    background-color: #f5f5f5;
                    border: 1px solid #e0e0e0;
                    padding: 8px;
                    font-weight: 600;
                }
                QLineEdit, QComboBox, QDateEdit, QTextEdit {
                    border: 1px solid #e0e0e0;
                    border-radius: 4px;
                    padding: 6px;
                }
                QLineEdit:focus, QComboBox:focus, QDateEdit:focus, QTextEdit:focus {
                    border-color: #1976d2;
                }
                QLabel {
                    color: #212121;
                }
            """)
            print("✅ Using default stylesheet")
    
    def _setup_font(self):
        """Setup application font"""
        font = QFont("Segoe UI", 10)
        font.setStyleHint(QFont.StyleHint.SansSerif)
        self.setFont(font)
    
    def run(self):
        """Run the application"""
        self.main_window.show()
        return self.exec()


def main():
    """Main entry point"""
    print("=" * 60)
    print("QUẢN LÝ DỊCH VỤ CHO THUÊ KHO LƯU TRỮ HÀNG HÓA")
    print("=" * 60)
    print("\n🚀 Starting application...")
    print("📦 Loading database...")
    
    # Test database connection
    try:
        session = get_session()
        session.execute("SELECT 1")
        print("✅ Database connected")
        session.close()
    except Exception as e:
        print(f"⚠️  Database warning: {e}")
    
    print("\n🎨 Initializing GUI...")
    
    # Create and run application
    app = Application()
    sys.exit(app.run())


if __name__ == "__main__":
    main()
