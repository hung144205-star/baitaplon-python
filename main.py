#!/usr/bin/env python3
"""
Quản Lý Dịch Vụ Cho Thuê Kho Lưu Trữ Hàng Hóa
Nhóm 12 - Lập trình Python

Usage:
    python main.py
"""
import sys
import os

# Add src to path
src_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src')
sys.path.insert(0, src_path)

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QFrame, QTabWidget, QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from src.gui.views import (
    KhachHangView, KhoView, ViTriView, HopDongView,
    HangHoaView, DashboardView
)


class MainWindow(QMainWindow):
    """
    Main window với menu chọn các module
    """
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🏢 HỆ THỐNG QUẢN LÝ KHO")
        self.setMinimumSize(1200, 800)
        self.setup_ui()
    
    def setup_ui(self):
        """Setup UI"""
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # Title
        title = QLabel("🏢 HỆ THỐNG QUẢN LÝ KHO")
        title.setStyleSheet("""
            QLabel {
                font-size: 32px;
                font-weight: 700;
                color: #1976d2;
                padding: 20px;
            }
        """)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)
        
        # Subtitle
        subtitle = QLabel("Quản lý khách hàng, kho hàng, hợp đồng và hàng hóa")
        subtitle.setStyleSheet("""
            QLabel {
                font-size: 16px;
                color: #757575;
                padding: 10px;
            }
        """)
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(subtitle)
        
        # Tab widget
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 2px solid #1976d2;
                border-radius: 8px;
                background-color: #ffffff;
            }
            QTabBar::tab {
                background-color: #f6f5f4;
                padding: 12px 24px;
                margin-right: 2px;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
                font-weight: 600;
                font-size: 14px;
            }
            QTabBar::tab:selected {
                background-color: #1976d2;
                color: white;
            }
            QTabBar::tab:hover {
                background-color: #eeeeee;
            }
        """)
        
        # Add module tabs
        self.add_module_tabs()
        
        main_layout.addWidget(self.tabs)
        
        # Status bar
        self.statusBar().showMessage("Sẵn sàng | Chọn module để bắt đầu")
    
    def add_module_tabs(self):
        """Add tabs for each module"""
        
        # Module 1: Customer Management
        khach_hang_view = KhachHangView()
        self.tabs.addTab(khach_hang_view, "👥 Khách Hàng")
        
        # Module 2: Warehouse Management
        kho_view = KhoView()
        self.tabs.addTab(kho_view, "🏭 Kho Hàng")
        
        # Module 3: Storage Location
        vi_tri_view = ViTriView()
        self.tabs.addTab(vi_tri_view, "📍 Vị Trí")
        
        # Module 4: Contract Management
        hop_dong_view = HopDongView()
        self.tabs.addTab(hop_dong_view, "📋 Hợp Đồng")
        
        # Module 5: Goods Management
        hang_hoa_view = HangHoaView()
        self.tabs.addTab(hang_hoa_view, "📦 Hàng Hóa")
        
        # Module 6: Dashboard
        dashboard_view = DashboardView()
        self.tabs.addTab(dashboard_view, "📊 Dashboard")
        
        # Set first tab active
        if self.tabs.count() > 0:
            self.tabs.setCurrentIndex(0)
    
    def closeEvent(self, event):
        """Handle close event"""
        reply = QMessageBox.question(
            self,
            'Xác nhận thoát',
            'Bạn có chắc chắn muốn thoát?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            event.accept()
        else:
            event.ignore()


def main():
    """Main entry point"""
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')
    
    # Set font
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
