#!/usr/bin/env python3
"""
Help View - Giao diện Trợ giúp và Hướng dẫn sử dụng
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QTabWidget, QScrollArea, QTableWidget, QTableWidgetItem,
    QTextEdit, QGroupBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from src.gui.dialogs import MessageDialog


class HelpView(QWidget):
    """
    Giao diện Trợ giúp - Hướng dẫn sử dụng, phím tắt và thông tin
    """
    
    APP_VERSION = "1.0.0"
    APP_NAME = "Quản Lý Kho Lưu Trữ"
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        """Setup UI"""
        self.setStyleSheet("""
            QWidget {
                background-color: #faf9f8;
                font-family: 'Inter', sans-serif;
            }
            QLabel#titleLabel {
                font-size: 24px;
                font-weight: 700;
                color: #31302e;
            }
            QLabel#headerLabel {
                font-size: 16px;
                font-weight: 600;
                color: #005db2;
            }
            QLabel#sectionLabel {
                font-size: 14px;
                font-weight: 600;
                color: #31302e;
            }
            QLabel#bodyLabel {
                font-size: 13px;
                color: #615d59;
                line-height: 1.6;
            }
            QPushButton {
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: 600;
                font-size: 13px;
            }
            QPushButton#primaryButton {
                background-color: #005db2;
                color: white;
                border: none;
            }
            QPushButton#primaryButton:hover {
                background-color: #00468a;
            }
            QTabWidget::pane {
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                background-color: #ffffff;
                padding: 16px;
            }
            QTabBar::tab {
                padding: 10px 20px;
                font-size: 13px;
                font-weight: 600;
                color: #615d59;
                background-color: #f5f5f5;
                border: 1px solid #e0e0e0;
                border-bottom: none;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
            }
            QTabBar::tab:selected {
                color: #005db2;
                background-color: #ffffff;
                border-bottom: 2px solid #005db2;
            }
            QTabBar::tab:hover:!selected {
                background-color: #e3f2fd;
            }
            QGroupBox {
                background-color: #ffffff;
                border: 1px solid rgba(0, 0, 0, 0.1);
                border-radius: 8px;
                padding: 16px;
                margin-top: 8px;
                font-weight: 600;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 16px;
                padding: 0 8px;
            }
            QTableWidget {
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                background-color: #ffffff;
                font-size: 13px;
                gridline-color: #f0f0f0;
            }
            QTableWidget::item {
                padding: 8px 12px;
            }
            QTableWidget::item:selected {
                background-color: #e3f2fd;
                color: #31302e;
            }
            QHeaderView::section {
                background-color: #f5f5f5;
                padding: 10px 12px;
                font-weight: 600;
                color: #31302e;
                border: none;
                border-bottom: 2px solid #e0e0e0;
            }
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QTextEdit {
                background-color: transparent;
                border: none;
                font-size: 13px;
                line-height: 1.6;
                color: #31302e;
            }
        """)
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 30, 40, 30)
        main_layout.setSpacing(20)
        
        # Title
        title_layout = QHBoxLayout()
        title = QLabel("❓ TRỢ GIÚP & HƯỚNG DẪN")
        title.setObjectName("titleLabel")
        title_layout.addWidget(title)
        title_layout.addStretch()
        main_layout.addLayout(title_layout)
        
        # Tab widget
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabPosition(QTabWidget.TabPosition.North)
        
        # Tab 1: Hướng dẫn sử dụng
        self._setup_user_guide_tab()
        
        # Tab 2: Phím tắt
        self._setup_shortcuts_tab()
        
        # Tab 3: Về chúng tôi
        self._setup_about_tab()
        
        main_layout.addWidget(self.tab_widget, 1)
    
    def _setup_user_guide_tab(self):
        """Setup User Guide tab"""
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border: none;")
        
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setSpacing(24)
        
        # 1. Hướng dẫn đăng nhập
        login_group = self._create_guide_section(
            "🔐 1. Hướng dẫn Đăng nhập",
            """
            <p><b>Bước 1:</b> Khởi động ứng dụng</p>
            <p style="margin-left: 15px;">Chạy file <code>main.py</code> để mở màn hình đăng nhập.</p>
            
            <p><b>Bước 2:</b> Nhập thông tin</p>
            <p style="margin-left: 15px;">Điền <b>Tên đăng nhập</b> và <b>Mật khẩu</b> được cấp bởi quản trị viên.</p>
            
            <p><b>Bước 3:</b> Đăng nhập</p>
            <p style="margin-left: 15px;">Nhấn nút <b>Đăng nhập</b> hoặc nhấn <code>Enter</code>.</p>
            
            <p><b>Lưu ý:</b></p>
            <ul style="margin-left: 15px;">
                <li>Tài khoản mặc định: <code>admin</code> / <code>admin123</code></li>
                <li>Nếu quên mật khẩu, liên hệ quản trị viên để reset</li>
            </ul>
            """
        )
        layout.addWidget(login_group)
        
        # 2. Hướng dẫn quản lý khách hàng
        customer_group = self._create_guide_section(
            "👥 2. Hướng dẫn Quản lý Khách hàng",
            """
            <p><b>Truy cập:</b> Nhấn <code>Ctrl+K</code> hoặc chọn <b>Khách hàng</b> trên thanh toolbar.</p>
            
            <p><b>Các chức năng chính:</b></p>
            <ul style="margin-left: 15px;">
                <li><b>Xem danh sách:</b> Bảng hiển thị thông tin khách hàng với tìm kiếm và lọc</li>
                <li><b>Thêm mới:</b> Nhấn nút <b>+ Thêm Khách hàng</b>, điền form và lưu</li>
                <li><b>Sửa thông tin:</b> Nhấn đúp vào dòng khách hàng cần sửa</li>
                <li><b>Xóa:</b> Chọn khách hàng → nhấn nút <b>Xóa</b> và xác nhận</li>
            </ul>
            
            <p><b>Thông tin cần điền khi thêm mới:</b></p>
            <ul style="margin-left: 15px;">
                <li>Họ tên (*)</li>
                <li>Số điện thoại</li>
                <li>Email</li>
                <li>Địa chỉ</li>
                <li>Ghi chú</li>
            </ul>
            """
        )
        layout.addWidget(customer_group)
        
        # 3. Hướng dẫn quản lý kho
        warehouse_group = self._create_guide_section(
            "🏭 3. Hướng dẫn Quản lý Kho",
            """
            <p><b>Truy cập:</b> Nhấn <code>Ctrl+O</code> hoặc chọn <b>Kho hàng</b> trên thanh toolbar.</p>
            
            <p><b>Các chức năng chính:</b></p>
            <ul style="margin-left: 15px;">
                <li><b>Xem kho:</b> Danh sách các kho với thông tin diện tích, sức chứa, tỷ lệ lấp đầy</li>
                <li><b>Thêm kho mới:</b> Nhấn <b>+ Thêm Kho</b>, nhập thông tin kho</li>
                <li><b>Quản lý vị trí:</b> Mỗi kho có nhiều vị trí lưu trữ (tầng, ngăn)</li>
                <li><b>Theo dõi tồn kho:</b> Xem tổng quan và chi tiết hàng trong kho</li>
            </ul>
            
            <p><b>Trạng thái kho:</b></p>
            <ul style="margin-left: 15px;">
                <li><span style="color: #2e7d32;">● Đang hoạt động</span> - Kho đang sử dụng</li>
                <li><span style="color: #757575;">● Ngừng hoạt động</span> - Kho tạm thời không dùng</li>
            </ul>
            """
        )
        layout.addWidget(warehouse_group)
        
        # 4. Hướng dẫn quản lý hợp đồng
        contract_group = self._create_guide_section(
            "📄 4. Hướng dẫn Quản lý Hợp đồng",
            """
            <p><b>Truy cập:</b> Nhấn <code>Ctrl+H</code> hoặc chọn <b>Hợp đồng</b> trên thanh toolbar.</p>
            
            <p><b>Các chức năng chính:</b></p>
            <ul style="margin-left: 15px;">
                <li><b>Danh sách hợp đồng:</b> Xem tất cả hợp đồng với trạng thái</li>
                <li><b>Tạo hợp đồng mới:</b> Chọn khách hàng → điền thông tin → lưu</li>
                <li><b>Xem chi tiết:</b> Nhấn vào hợp đồng để xem đầy đủ thông tin</li>
                <li><b>Gia hạn:</b> Hợp đồng sắp hết sẽ hiển thị cảnh báo</li>
            </ul>
            
            <p><b>Trạng thái hợp đồng:</b></p>
            <ul style="margin-left: 15px;">
                <li><span style="color: #2e7d32;">● Đang hoạt động</span></li>
                <li><span style="color: #ff9800;">● Sắp hết hạn</span> (còn 30 ngày)</li>
                <li><span style="color: #d32f2f;">● Đã hết hạn</span></li>
                <li><span style="color: #757575;">● Đã hủy</span></li>
            </ul>
            """
        )
        layout.addWidget(contract_group)
        
        # 5. Hướng dẫn nhập/xuất hàng hóa
        goods_group = self._create_guide_section(
            "📦 5. Hướng dẫn Nhập/Xuất Hàng hóa",
            """
            <p><b>Truy cập:</b> Nhấn <code>Ctrl+G</code> hoặc chọn <b>Hàng hóa</b> trên thanh toolbar.</p>
            
            <p><b>Nhập hàng:</b></p>
            <ul style="margin-left: 15px;">
                <li>Vào mục <b>Hàng hóa</b> → nhấn <b>+ Thêm Hàng</b></li>
                <li>Chọn <b>kho</b> và <b>vị trí</b> lưu trữ</li>
                <li>Nhập thông tin: tên hàng, số lượng, đơn vị tính</li>
                <li>Nhấn <b>Lưu</b> để cập nhật tồn kho</li>
            </ul>
            
            <p><b>Xuất hàng:</b></p>
            <ul style="margin-left: 15px;">
                <li>Chọn hàng cần xuất → nhấn <b>Xuất hàng</b></li>
                <li>Nhập số lượng xuất</li>
                <li>Hệ thống tự động cập nhật tồn kho</li>
            </ul>
            
            <p><b>Cảnh báo:</b></p>
            <ul style="margin-left: 15px;">
                <li>Hàng sắp hết → hiển thị màu đỏ trong danh sách</li>
                <li>Tồn kho bằng 0 → không thể xuất</li>
            </ul>
            """
        )
        layout.addWidget(goods_group)
        
        # 6. Hướng dẫn thanh toán
        payment_group = self._create_guide_section(
            "💰 6. Hướng dẫn Thanh toán",
            """
            <p><b>Truy cập:</b> Nhấn <code>Ctrl+T</code> hoặc chọn <b>Thanh toán</b> trên thanh toolbar.</p>
            
            <p><b>Các chức năng chính:</b></p>
            <ul style="margin-left: 15px;">
                <li><b>Danh sách thanh toán:</b> Xem tất cả các phiếu thanh toán</li>
                <li><b>Tạo thanh toán:</b> Tạo phiếu thanh toán mới cho hợp đồng</li>
                <li><b>Cập nhật trạng thái:</b> Đã thanh toán / Chưa thanh toán</li>
                <li><b>In phiếu:</b> Xuất phiếu thanh toán ra file</li>
            </ul>
            
            <p><b>Quy trình thanh toán:</b></p>
            <ol style="margin-left: 15px;">
                <li>Chọn hợp đồng cần thanh toán</li>
                <li>Nhập số tiền và ngày thanh toán</li>
                <li>Chọn phương thức thanh toán</li>
                <li>Nhấn <b>Lưu</b> để hoàn tất</li>
            </ol>
            """
        )
        layout.addWidget(payment_group)
        
        layout.addStretch()
        scroll.setWidget(container)
        
        # Wrap scroll in widget
        scroll_wrapper = QWidget()
        scroll_wrapper_layout = QVBoxLayout(scroll_wrapper)
        scroll_wrapper_layout.setContentsMargins(0, 0, 0, 0)
        scroll_wrapper_layout.addWidget(scroll)
        
        self.tab_widget.addTab(scroll_wrapper, "📖 Hướng dẫn sử dụng")
    
    def _create_guide_section(self, title: str, content: str) -> QGroupBox:
        """Create a guide section group box"""
        group = QGroupBox(title)
        layout = QVBoxLayout(group)
        
        text_edit = QTextEdit()
        text_edit.setHtml(content)
        text_edit.setReadOnly(True)
        text_edit.setLineWrapMode(QTextEdit.LineWrapMode.WidgetWidth)
        
        layout.addWidget(text_edit)
        
        return group
    
    def _setup_shortcuts_tab(self):
        """Setup Keyboard Shortcuts tab"""
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border: none;")
        
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setSpacing(20)
        
        # Header
        header_label = QLabel("Danh sách phím tắt trong ứng dụng")
        header_label.setStyleSheet("font-size: 14px; color: #615d59; margin-bottom: 10px;")
        layout.addWidget(header_label)
        
        # Table
        self.shortcuts_table = QTableWidget()
        self.shortcuts_table.setColumnCount(2)
        self.shortcuts_table.setHorizontalHeaderLabels(["Phím tắt", "Chức năng"])
        self.shortcuts_table.horizontalHeader().setStretchLastSection(True)
        self.shortcuts_table.setAlternatingRowColors(True)
        self.shortcuts_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.shortcuts_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        
        # Add shortcuts data
        shortcuts = [
            # Navigation
            ("Ctrl + D", "Mở Dashboard"),
            ("Ctrl + K", "Mở Quản lý Khách hàng"),
            ("Ctrl + O", "Mở Quản lý Kho hàng"),
            ("Ctrl + H", "Mở Quản lý Hợp đồng"),
            ("Ctrl + G", "Mở Quản lý Hàng hóa"),
            ("Ctrl + T", "Mở Quản lý Thanh toán"),
            ("Ctrl + B", "Mở Báo cáo"),
            
            # File operations
            ("Ctrl + Q", "Thoát ứng dụng"),
            ("Ctrl + S", "Lưu (trong form nhập liệu)"),
            ("Ctrl + N", "Tạo mới (thêm mới)"),
            ("Ctrl + F", "Tìm kiếm"),
            
            # Table operations
            ("Enter", "Xem chi tiết / Sửa"),
            ("Delete", "Xóa (sau khi chọn)"),
            ("Escape", "Đóng cửa sổ / Hủy"),
            
            # Quick filters
            ("Alt + 1", "Lọc theo trạng thái Hoạt động"),
            ("Alt + 2", "Lọc theo trạng thái Không hoạt động"),
            ("Alt + A", "Hiện tất cả (Bỏ lọc)"),
        ]
        
        self.shortcuts_table.setRowCount(len(shortcuts))
        for row, (shortcut, description) in enumerate(shortcuts):
            shortcut_item = QTableWidgetItem(shortcut)
            shortcut_item.setFont(QFont("Consolas", 12))
            self.shortcuts_table.setItem(row, 0, shortcut_item)
            
            desc_item = QTableWidgetItem(description)
            self.shortcuts_table.setItem(row, 1, desc_item)
        
        self.shortcuts_table.resizeColumnsToContents()
        layout.addWidget(self.shortcuts_table)
        
        # Tips section
        tips_group = QGroupBox("💡 Mẹo sử dụng")
        tips_layout = QVBoxLayout(tips_group)
        
        tips_text = QTextEdit()
        tips_text.setHtml("""
            <p>• <b>Đặt hàng nhanh:</b> Sử dụng phím tắt để di chuyển nhanh giữa các module</p>
            <p>• <b>Tìm kiếm thông minh:</b> Nhấn <code>Ctrl+F</code> rồi gõ từ khóa để tìm nhanh</p>
            <p>• <b>Thêm nhanh:</b> Nhấn <code>Ctrl+N</code> khi đang ở danh sách để thêm mới</p>
            <p>• <b>Sửa nhanh:</b> Nhấn đúp chuột vào dòng để mở form sửa</p>
            <p>• <b>Xóa an toàn:</b> Hệ thống sẽ yêu cầu xác nhận trước khi xóa</p>
        """)
        tips_text.setReadOnly(True)
        tips_layout.addWidget(tips_text)
        
        layout.addWidget(tips_group)
        layout.addStretch()
        
        scroll.setWidget(container)
        
        scroll_wrapper = QWidget()
        scroll_wrapper_layout = QVBoxLayout(scroll_wrapper)
        scroll_wrapper_layout.setContentsMargins(0, 0, 0, 0)
        scroll_wrapper_layout.addWidget(scroll)
        
        self.tab_widget.addTab(scroll_wrapper, "⌨️ Phím tắt")
    
    def _setup_about_tab(self):
        """Setup About tab"""
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border: none;")
        
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setSpacing(20)
        layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        
        # App logo/title
        app_title = QLabel("🏢")
        app_title.setStyleSheet("font-size: 64px;")
        app_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(app_title)
        
        app_name = QLabel(self.APP_NAME)
        app_name.setStyleSheet("font-size: 28px; font-weight: 700; color: #31302e;")
        app_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(app_name)
        
        version_label = QLabel(f"Phiên bản {self.APP_VERSION}")
        version_label.setStyleSheet("font-size: 14px; color: #757575;")
        version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(version_label)
        
        layout.addSpacing(10)
        
        # About description
        about_group = QGroupBox("Giới thiệu ứng dụng")
        about_layout = QVBoxLayout(about_group)
        
        about_text = QTextEdit()
        about_text.setHtml("""
            <p><b>Quản Lý Kho Lưu Trữ</b> là phần mềm quản lý kho hàng hiện đại, được phát triển bởi 
            <b>Nhóm 12</b> trong khuôn khổ môn Lập trình Python.</p>
            
            <p>Phần mềm hỗ trợ:</p>
            <ul>
                <li>✅ Quản lý khách hàng và hợp đồng thuê kho</li>
                <li>✅ Quản lý kho hàng và vị trí lưu trữ</li>
                <li>✅ Quản lý hàng hóa nhập/xuất</li>
                <li>✅ Theo dõi thanh toán và công nợ</li>
                <li>✅ Xuất báo cáo và thống kê</li>
            </ul>
        """)
        about_text.setReadOnly(True)
        about_layout.addWidget(about_text)
        
        layout.addWidget(about_group)
        
        # Technology stack
        tech_group = QGroupBox("Công nghệ sử dụng")
        tech_layout = QVBoxLayout(tech_group)
        
        tech_text = QTextEdit()
        tech_text.setHtml("""
            <ul>
                <li><b>Python 3.10+</b> - Ngôn ngữ lập trình chính</li>
                <li><b>PyQt6 6.4+</b> - Framework giao diện người dùng</li>
                <li><b>SQLAlchemy 2.0+</b> - ORM cho tương tác database</li>
                <li><b>SQLite 3.x</b> - Hệ quản trị cơ sở dữ liệu</li>
                <li><b>ReportLab</b> - Thư viện xuất PDF</li>
            </ul>
        """)
        tech_text.setReadOnly(True)
        tech_layout.addWidget(tech_text)
        
        layout.addWidget(tech_group)
        
        # Team info
        team_group = QGroupBox("Thông tin nhóm phát triển")
        team_layout = QVBoxLayout(team_group)
        
        team_text = QTextEdit()
        team_text.setHtml("""
            <p style="text-align: center;"><b>Nhóm 12 - Lập trình Python</b></p>
            
            <p style="text-align: center; margin-top: 15px;"><b>Thành viên:</b></p>
            <ul style="text-align: center; list-style-position: inside;">
                <li>👤 Đoàn Mạnh Hùng (Trưởng nhóm)</li>
                <li>👤 Lương Hán Hải</li>
                <li>👤 Nguyễn Đồng Thanh</li>
            </ul>
            
            <p style="text-align: center; margin-top: 15px;"><b>Liên hệ:</b></p>
            <p style="text-align: center;">📧 nhom12@example.edu.vn</p>
        """)
        team_text.setReadOnly(True)
        team_layout.addWidget(team_text)
        
        layout.addWidget(team_group)
        
        # Copyright
        copyright_label = QLabel("© 2024 Nhóm 12 - Lập trình Python. Mọi quyền được bảo lưu.")
        copyright_label.setStyleSheet("font-size: 11px; color: #757575; padding: 10px;")
        copyright_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(copyright_label)
        
        layout.addStretch()
        
        scroll.setWidget(container)
        
        scroll_wrapper = QWidget()
        scroll_wrapper_layout = QVBoxLayout(scroll_wrapper)
        scroll_wrapper_layout.setContentsMargins(0, 0, 0, 0)
        scroll_wrapper_layout.addWidget(scroll)
        
        self.tab_widget.addTab(scroll_wrapper, "ℹ️ Về chúng tôi")


__all__ = ['HelpView']
