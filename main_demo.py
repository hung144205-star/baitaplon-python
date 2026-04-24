#!/usr/bin/env python3
"""
Main Application - Demo giao diện các Phase
"""
import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QFrame, QScrollArea, QTabWidget, QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class MainWindow(QMainWindow):
    """
    Main window với menu chọn các module
    """
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🏢 HỆ THỐNG QUẢN LÝ KHO - DEMO")
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
        subtitle = QLabel("Demo giao diện các Phase đã hoàn thành")
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
        self.add_phase_tabs()
        
        main_layout.addWidget(self.tabs)
        
        # Status bar
        self.statusBar().showMessage("Sẵn sàng | Select a module to start")
    
    def add_phase_tabs(self):
        """Add tabs for each phase"""
        
        # Phase 3: Customer Management
        from src.gui.views import KhachHangView
        khach_hang_view = KhachHangView()
        self.tabs.addTab(khach_hang_view, "👥 Khách Hàng (P3)")
        
        # Phase 4: Warehouse Management
        # Create a tab with sub-options for Phase 4
        phase4_widget = self.create_phase4_widget()
        self.tabs.addTab(phase4_widget, "🏭 Kho Hàng (P4)")
        
        # Phase 5: Contract Management
        from src.gui.views import HopDongView
        hop_dong_view = HopDongView()
        self.tabs.addTab(hop_dong_view, "📋 Hợp Đồng (P5)")
        
        # Phase 6: Goods Management
        from src.gui.views import HangHoaView
        hang_hoa_view = HangHoaView()
        self.tabs.addTab(hang_hoa_view, "📦 Hàng Hóa (P6)")
        
        # Phase 7: Reports
        from src.gui.views import DashboardView
        dashboard_view = DashboardView()
        self.tabs.addTab(dashboard_view, "📊 Báo Cáo (P7)")
    
    def create_phase4_widget(self):
        """Create widget with Phase 4 sub-modules"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title = QLabel("🏭 QUẢN LÝ KHO HÀNG")
        title.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: 700;
                color: #1976d2;
                padding: 20px;
            }
        """)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Module buttons
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(20)
        
        # Kho View button
        kho_btn = self.create_module_button(
            "🏭 Danh Sách Kho",
            "Xem và quản lý danh sách kho",
            self.open_kho_view
        )
        buttons_layout.addWidget(kho_btn)
        
        # Vi Tri View button
        vi_tri_btn = self.create_module_button(
            "📍 Vị Trí Lưu Trữ",
            "Quản lý vị trí trong kho",
            self.open_vi_tri_view
        )
        buttons_layout.addWidget(vi_tri_btn)
        
        layout.addLayout(buttons_layout)
        
        # Dashboard button
        dashboard_btn = self.create_module_button(
            "📊 Dashboard Kho",
            "Thống kê và biểu đồ kho hàng",
            self.open_kho_dashboard
        )
        layout.addWidget(dashboard_btn)
        
        layout.addStretch()
        
        return widget
    
    def create_module_button(self, title: str, description: str, callback) -> QFrame:
        """Create a styled module button"""
        button_frame = QFrame()
        button_frame.setFrameShape(QFrame.Shape.StyledPanel)
        button_frame.setStyleSheet("""
            QFrame {
                background-color: #f6f5f4;
                border: 2px solid #1976d2;
                border-radius: 12px;
                padding: 20px;
            }
            QFrame:hover {
                background-color: #e3f2fd;
            }
        """)
        
        layout = QVBoxLayout(button_frame)
        layout.setSpacing(10)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Title
        title_label = QLabel(title)
        title_label.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: 700;
                color: #1976d2;
            }
        """)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)
        
        # Description
        desc_label = QLabel(description)
        desc_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #757575;
            }
        """)
        desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)
        
        # Button
        btn = QPushButton("Mở")
        btn.setStyleSheet("""
            QPushButton {
                background-color: #1976d2;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 6px;
                font-weight: 600;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #1565c0;
            }
        """)
        btn.clicked.connect(callback)
        layout.addWidget(btn)
        
        return button_frame
    
    def open_kho_view(self):
        """Open Kho View"""
        from src.gui.views import KhoView
        view = KhoView()
        self.tabs.addTab(view, "🏭 Kho")
        self.tabs.setCurrentIndex(self.tabs.count() - 1)
        self.statusBar().showMessage("Module: Quản lý Kho")
    
    def open_vi_tri_view(self):
        """Open Vi Tri View"""
        from src.gui.views import ViTriView
        view = ViTriView()
        self.tabs.addTab(view, "📍 Vị Trí")
        self.tabs.setCurrentIndex(self.tabs.count() - 1)
        self.statusBar().showMessage("Module: Quản lý Vị Trí")
    
    def open_kho_dashboard(self):
        """Open Kho Dashboard"""
        from src.gui.views import DashboardView
        view = DashboardView()
        self.tabs.addTab(view, "📊 Dashboard Kho")
        self.tabs.setCurrentIndex(self.tabs.count() - 1)
        self.statusBar().showMessage("Module: Dashboard Kho")
    
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


if __name__ == '__main__':
    main()
