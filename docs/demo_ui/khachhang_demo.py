"""
Demo PyQt6 - Quản lý Khách hàng
Design System: Notion-inspired (warm neutrals, Notion Blue, Inter font)
Tech Stack: Python 3.10+ + PyQt6
"""

import sys
from datetime import datetime
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QPushButton, QLabel, QLineEdit,
    QDialog, QFormLayout, QComboBox, QTextEdit, QGroupBox,
    QGridLayout, QHeaderView, QMessageBox, QFrame, QSizePolicy,
    QSpacerItem, QScrollArea, QTabWidget
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QColor, QPalette, QIcon


# ==================== DESIGN CONSTANTS ====================
class Design:
    """Design System Constants"""
    # Colors
    NOTION_BLACK = "#000000f2"  # rgba(0,0,0,0.95)
    PURE_WHITE = "#ffffff"
    NOTION_BLUE = "#0075de"
    ACTIVE_BLUE = "#005bab"
    WARM_WHITE = "#f6f5f4"
    WARM_DARK = "#31302e"
    WARM_GRAY_500 = "#615d59"
    WARM_GRAY_300 = "#a39e98"
    GREEN = "#1aae39"
    ORANGE = "#dd5b00"
    BADGE_BLUE_BG = "#f2f9ff"
    BADGE_BLUE_TEXT = "#097fe8"
    
    # Typography
    FONT_FAMILY = "Inter, -apple-system, system-ui, Segoe UI, Helvetica, Arial, sans-serif"
    
    # Spacing
    PADDING_SMALL = 8
    PADDING_MEDIUM = 16
    PADDING_LARGE = 24
    
    # Border radius
    RADIUS_SMALL = 4
    RADIUS_MEDIUM = 8
    RADIUS_LARGE = 12
    RADIUS_PILL = 9999


class StyledButton(QPushButton):
    """Custom styled button following Notion design"""
    def __init__(self, text, button_type="primary", icon_text="", parent=None):
        super().__init__(f"{icon_text} {text}" if icon_text else text, parent)
        self.button_type = button_type
        self.apply_style()
        
    def apply_style(self):
        if self.button_type == "primary":
            self.setStyleSheet(f"""
                QPushButton {{
                    background-color: {Design.NOTION_BLUE};
                    color: {Design.PURE_WHITE};
                    border: none;
                    border-radius: {Design.RADIUS_SMALL}px;
                    padding: 10px 20px;
                    font-family: {Design.FONT_FAMILY};
                    font-size: 14px;
                    font-weight: 600;
                }}
                QPushButton:hover {{
                    background-color: {Design.ACTIVE_BLUE};
                }}
                QPushButton:pressed {{
                    transform: scale(0.98);
                }}
            """)
        elif self.button_type == "secondary":
            self.setStyleSheet(f"""
                QPushButton {{
                    background-color: rgba(0,0,0,0.05);
                    color: {Design.NOTION_BLACK};
                    border: 1px solid rgba(0,0,0,0.1);
                    border-radius: {Design.RADIUS_SMALL}px;
                    padding: 10px 20px;
                    font-family: {Design.FONT_FAMILY};
                    font-size: 14px;
                    font-weight: 600;
                }}
                QPushButton:hover {{
                    background-color: rgba(0,0,0,0.08);
                }}
            """)
        elif self.button_type == "danger":
            self.setStyleSheet(f"""
                QPushButton {{
                    background-color: #fef2f2;
                    color: #dc2626;
                    border: 1px solid #fecaca;
                    border-radius: {Design.RADIUS_SMALL}px;
                    padding: 10px 20px;
                    font-family: {Design.FONT_FAMILY};
                    font-size: 14px;
                    font-weight: 600;
                }}
                QPushButton:hover {{
                    background-color: #fee2e2;
                }}
            """)
        self.setCursor(Qt.CursorShape.PointingHandCursor)


class StyledCard(QFrame):
    """Styled card container"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {Design.PURE_WHITE};
                border: 1px solid rgba(0,0,0,0.1);
                border-radius: {Design.RADIUS_LARGE}px;
            }}
        """)
        self.setFrameShape(QFrame.Shape.StyledPanel)


class Badge(QLabel):
    """Pill badge for status indicators"""
    def __init__(self, text, badge_type="active", parent=None):
        super().__init__(text, parent)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        if badge_type == "active":
            bg_color = "#e6f7e9"
            text_color = Design.GREEN
        elif badge_type == "inactive":
            bg_color = "#f5f5f5"
            text_color = Design.WARM_GRAY_500
        elif badge_type == "doanh_nghiep":
            bg_color = "#fef3e6"
            text_color = Design.ORANGE
        elif badge_type == "ca_nhan":
            bg_color = Design.BADGE_BLUE_BG
            text_color = Design.BADGE_BLUE_TEXT
        else:
            bg_color = Design.BADGE_BLUE_BG
            text_color = Design.BADGE_BLUE_TEXT
            
        self.setStyleSheet(f"""
            QLabel {{
                background-color: {bg_color};
                color: {text_color};
                border-radius: {Design.RADIUS_PILL}px;
                padding: 4px 12px;
                font-family: {Design.FONT_FAMILY};
                font-size: 12px;
                font-weight: 600;
                letter-spacing: 0.5px;
            }}
        """)


class StatCard(StyledCard):
    """Statistics card widget"""
    def __init__(self, label, value, change=None, positive=True, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(8)
        
        # Label
        self.label = QLabel(label)
        self.label.setStyleSheet(f"""
            font-family: {Design.FONT_FAMILY};
            font-size: 14px;
            font-weight: 500;
            color: {Design.WARM_GRAY_500};
        """)
        layout.addWidget(self.label)
        
        # Value
        self.value = QLabel(value)
        self.value.setStyleSheet(f"""
            font-family: {Design.FONT_FAMILY};
            font-size: 32px;
            font-weight: 700;
            color: {Design.NOTION_BLACK};
            letter-spacing: -0.6px;
        """)
        layout.addWidget(self.value)
        
        # Change indicator
        if change:
            self.change = QLabel(change)
            color = Design.GREEN if positive else Design.ORANGE
            self.change.setStyleSheet(f"""
                font-family: {Design.FONT_FAMILY};
                font-size: 14px;
                font-weight: 500;
                color: {color};
            """)
            layout.addWidget(self.change)


# ==================== DIALOG CLASSES ====================
class ThemKhachHangDialog(QDialog):
    """Dialog for adding new customer"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Thêm mới khách hàng")
        self.setMinimumSize(600, 700)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(24)
        layout.setContentsMargins(32, 32, 32, 32)
        
        # Header
        header = QLabel("Thêm mới khách hàng")
        header.setStyleSheet(f"""
            font-family: {Design.FONT_FAMILY};
            font-size: 28px;
            font-weight: 700;
            color: {Design.NOTION_BLACK};
            letter-spacing: -0.5px;
        """)
        layout.addWidget(header)
        
        subtitle = QLabel("Nhập thông tin để đăng ký khách hàng mới vào hệ thống")
        subtitle.setStyleSheet(f"""
            font-family: {Design.FONT_FAMILY};
            font-size: 16px;
            font-weight: 500;
            color: {Design.WARM_GRAY_500};
        """)
        layout.addWidget(subtitle)
        
        # Form card
        card = StyledCard()
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(24, 24, 24, 24)
        card_layout.setSpacing(20)
        
        # Form
        form = QFormLayout()
        form.setSpacing(16)
        form.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)
        
        # Loại khách hàng
        self.loai_combo = QComboBox()
        self.loai_combo.addItems(["Doanh nghiệp", "Cá nhân"])
        self.loai_combo.setStyleSheet(self.input_style())
        form.addRow(self.label_style("Loại khách hàng *"), self.loai_combo)
        
        # Mã khách hàng (auto)
        self.ma_kh = QLineEdit("KH-DN-00129")
        self.ma_kh.setReadOnly(True)
        self.ma_kh.setStyleSheet(self.input_style() + f"""
            QLineEdit {{
                background-color: {Design.WARM_WHITE};
                color: {Design.WARM_GRAY_500};
            }}
        """)
        form.addRow(self.label_style("Mã khách hàng"), self.ma_kh)
        
        # Tên
        self.ten = QLineEdit()
        self.ten.setStyleSheet(self.input_style())
        self.ten.setPlaceholderText("Nhập tên khách hàng hoặc tên công ty")
        form.addRow(self.label_style("Tên/Tên công ty *"), self.ten)
        
        # Mã số thuế
        self.mst = QLineEdit()
        self.mst.setStyleSheet(self.input_style())
        self.mst.setPlaceholderText("VD: 0123456789")
        form.addRow(self.label_style("Mã số thuế"), self.mst)
        
        # SĐT
        self.sdt = QLineEdit()
        self.sdt.setStyleSheet(self.input_style())
        self.sdt.setPlaceholderText("VD: 0912345678")
        form.addRow(self.label_style("Số điện thoại *"), self.sdt)
        
        # Email
        self.email = QLineEdit()
        self.email.setStyleSheet(self.input_style())
        self.email.setPlaceholderText("VD: example@email.com")
        form.addRow(self.label_style("Email *"), self.email)
        
        # Địa chỉ
        self.dia_chi = QTextEdit()
        self.dia_chi.setStyleSheet(self.input_style())
        self.dia_chi.setPlaceholderText("Nhập địa chỉ đầy đủ của khách hàng")
        self.dia_chi.setMaximumHeight(80)
        form.addRow(self.label_style("Địa chỉ *"), self.dia_chi)
        
        # Trạng thái
        self.trang_thai = QComboBox()
        self.trang_thai.addItems(["Đang hoạt động", "Tạm ngưng"])
        self.trang_thai.setStyleSheet(self.input_style())
        form.addRow(self.label_style("Trạng thái"), self.trang_thai)
        
        card_layout.addLayout(form)
        layout.addWidget(card)
        
        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        btn_huy = StyledButton("Hủy bỏ", "secondary")
        btn_huy.clicked.connect(self.reject)
        btn_layout.addWidget(btn_huy)
        
        btn_luu = StyledButton("Lưu khách hàng", "primary")
        btn_luu.clicked.connect(self.accept)
        btn_layout.addWidget(btn_luu)
        
        layout.addLayout(btn_layout)
        
    def label_style(self, text):
        label = QLabel(text)
        label.setStyleSheet(f"""
            font-family: {Design.FONT_FAMILY};
            font-size: 14px;
            font-weight: 600;
            color: {Design.NOTION_BLACK};
        """)
        return label
        
    def input_style(self):
        return f"""
            QLineEdit, QTextEdit, QComboBox {{
                font-family: {Design.FONT_FAMILY};
                font-size: 15px;
                padding: 10px 14px;
                border: 1px solid rgba(0,0,0,0.1);
                border-radius: {Design.RADIUS_SMALL}px;
                background-color: {Design.PURE_WHITE};
                color: {Design.NOTION_BLACK};
            }}
            QLineEdit:focus, QTextEdit:focus, QComboBox:focus {{
                border: 2px solid {Design.NOTION_BLUE};
            }}
        """


class ChiTietKhachHangDialog(QDialog):
    """Dialog for viewing customer details"""
    def __init__(self, customer_data, parent=None):
        super().__init__(parent)
        self.customer_data = customer_data
        self.setWindowTitle("Chi tiết khách hàng")
        self.setMinimumSize(700, 600)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(24)
        layout.setContentsMargins(32, 32, 32, 32)
        
        # Header with avatar
        header_layout = QHBoxLayout()
        
        avatar = QLabel("🏢")
        avatar.setStyleSheet(f"""
            font-size: 48px;
            background-color: {Design.BADGE_BLUE_BG};
            border-radius: {Design.RADIUS_LARGE}px;
            padding: 16px;
            min-width: 80px;
            min-height: 80px;
        """)
        avatar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(avatar)
        
        info_layout = QVBoxLayout()
        info_layout.setSpacing(8)
        
        name = QLabel(self.customer_data.get('ten', 'Công ty TNHH Thương mại Hoàng Phát'))
        name.setStyleSheet(f"""
            font-family: {Design.FONT_FAMILY};
            font-size: 28px;
            font-weight: 700;
            color: {Design.NOTION_BLACK};
            letter-spacing: -0.5px;
        """)
        info_layout.addWidget(name)
        
        meta_layout = QHBoxLayout()
        meta_layout.setSpacing(12)
        
        code = QLabel(f"Mã: {self.customer_data.get('ma', 'KH-DN-00001')}")
        code.setStyleSheet(f"color: {Design.WARM_GRAY_500}; font-size: 14px;")
        meta_layout.addWidget(code)
        
        meta_layout.addWidget(Badge("Đang hoạt động", "active"))
        meta_layout.addWidget(Badge("Doanh nghiệp", "doanh_nghiep"))
        meta_layout.addStretch()
        
        info_layout.addLayout(meta_layout)
        header_layout.addLayout(info_layout, 1)
        
        # Action buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(8)
        
        btn_sua = StyledButton("Chỉnh sửa", "secondary", "✏️")
        btn_layout.addWidget(btn_sua)
        
        btn_xoa = StyledButton("Xóa", "danger", "🗑️")
        btn_layout.addWidget(btn_xoa)
        
        header_layout.addLayout(btn_layout)
        layout.addLayout(header_layout)
        
        # Content grid
        content_layout = QHBoxLayout()
        content_layout.setSpacing(24)
        
        # Left column - Contact info
        left_card = StyledCard()
        left_layout = QVBoxLayout(left_card)
        left_layout.setContentsMargins(20, 20, 20, 20)
        left_layout.setSpacing(16)
        
        title1 = QLabel("📋 Thông tin liên hệ")
        title1.setStyleSheet(f"""
            font-family: {Design.FONT_FAMILY};
            font-size: 18px;
            font-weight: 700;
            color: {Design.NOTION_BLACK};
        """)
        left_layout.addWidget(title1)
        
        # Info rows
        info_data = [
            ("Số điện thoại", "0912345678"),
            ("Email", "hoangphat@gmail.com"),
            ("Địa chỉ", "123 Nguyễn Văn A, Quận 1, TP.HCM"),
            ("Mã số thuế", "0123456789"),
        ]
        
        for label, value in info_data:
            row = self.create_info_row(label, value)
            left_layout.addLayout(row)
        
        content_layout.addWidget(left_card)
        
        # Right column - Other info
        right_card = StyledCard()
        right_layout = QVBoxLayout(right_card)
        right_layout.setContentsMargins(20, 20, 20, 20)
        right_layout.setSpacing(16)
        
        title2 = QLabel("👤 Thông tin khác")
        title2.setStyleSheet(f"""
            font-family: {Design.FONT_FAMILY};
            font-size: 18px;
            font-weight: 700;
            color: {Design.NOTION_BLACK};
        """)
        right_layout.addWidget(title2)
        
        other_data = [
            ("Người đại diện", "Ông Nguyễn Văn Hoàng"),
            ("Chức vụ", "Giám đốc"),
            ("Ngày đăng ký", "15/03/2023"),
            ("Ngày cập nhật", "17/04/2026"),
        ]
        
        for label, value in other_data:
            row = self.create_info_row(label, value)
            right_layout.addLayout(row)
        
        content_layout.addWidget(right_card)
        layout.addLayout(content_layout)
        
        # Stats section
        stats_card = StyledCard()
        stats_layout = QVBoxLayout(stats_card)
        stats_layout.setContentsMargins(20, 20, 20, 20)
        
        stats_title = QLabel("📊 Tổng quan")
        stats_title.setStyleSheet(f"""
            font-family: {Design.FONT_FAMILY};
            font-size: 18px;
            font-weight: 700;
            color: {Design.NOTION_BLACK};
            margin-bottom: 16px;
        """)
        stats_layout.addWidget(stats_title)
        
        stats_grid = QHBoxLayout()
        stats_grid.setSpacing(16)
        
        for value, label in [("5", "Hợp đồng"), ("12", "Vị trí thuê"), ("₫45M", "Doanh thu")]:
            stat = self.create_stat_item(value, label)
            stats_grid.addWidget(stat)
        
        stats_layout.addLayout(stats_grid)
        layout.addWidget(stats_card)
        
        # Close button
        close_btn = StyledButton("Đóng", "secondary")
        close_btn.clicked.connect(self.accept)
        
        btn_container = QHBoxLayout()
        btn_container.addStretch()
        btn_container.addWidget(close_btn)
        layout.addLayout(btn_container)
        
    def create_info_row(self, label_text, value_text):
        row = QHBoxLayout()
        row.setSpacing(0)
        
        label = QLabel(label_text)
        label.setStyleSheet(f"""
            font-family: {Design.FONT_FAMILY};
            font-size: 14px;
            font-weight: 500;
            color: {Design.WARM_GRAY_500};
            min-width: 120px;
        """)
        
        value = QLabel(value_text)
        value.setStyleSheet(f"""
            font-family: {Design.FONT_FAMILY};
            font-size: 15px;
            font-weight: 600;
            color: {Design.NOTION_BLACK};
        """)
        
        row.addWidget(label)
        row.addWidget(value, 1)
        
        return row
        
    def create_stat_item(self, value, label):
        widget = QFrame()
        widget.setStyleSheet(f"""
            QFrame {{
                background-color: {Design.WARM_WHITE};
                border-radius: {Design.RADIUS_MEDIUM}px;
                padding: 16px;
            }}
        """)
        
        layout = QVBoxLayout(widget)
        layout.setSpacing(4)
        layout.setContentsMargins(0, 0, 0, 0)
        
        val_label = QLabel(value)
        val_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        val_label.setStyleSheet(f"""
            font-family: {Design.FONT_FAMILY};
            font-size: 28px;
            font-weight: 700;
            color: {Design.NOTION_BLACK};
            letter-spacing: -0.6px;
        """)
        
        lbl_label = QLabel(label)
        lbl_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_label.setStyleSheet(f"""
            font-family: {Design.FONT_FAMILY};
            font-size: 13px;
            font-weight: 500;
            color: {Design.WARM_GRAY_500};
        """)
        
        layout.addWidget(val_label)
        layout.addWidget(lbl_label)
        
        return widget


# ==================== MAIN WINDOW ====================
class MainWindow(QMainWindow):
    """Main application window"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🏭 KhoSmart Pro - Quản lý khách hàng")
        self.setMinimumSize(1200, 800)
        self.setup_ui()
        
    def setup_ui(self):
        # Central widget
        central = QWidget()
        self.setCentralWidget(central)
        
        # Main layout
        main_layout = QVBoxLayout(central)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Navigation bar
        nav = self.create_nav_bar()
        main_layout.addWidget(nav)
        
        # Content area
        content = QWidget()
        content.setStyleSheet(f"background-color: {Design.WARM_WHITE};")
        content_layout = QVBoxLayout(content)
        content_layout.setSpacing(24)
        content_layout.setContentsMargins(32, 32, 32, 32)
        
        # Header
        header = QLabel("Quản lý khách hàng")
        header.setStyleSheet(f"""
            font-family: {Design.FONT_FAMILY};
            font-size: 40px;
            font-weight: 700;
            color: {Design.NOTION_BLACK};
            letter-spacing: -1.5px;
        """)
        content_layout.addWidget(header)
        
        subtitle = QLabel("Danh sách và thông tin tất cả khách hàng đăng ký sử dụng dịch vụ")
        subtitle.setStyleSheet(f"""
            font-family: {Design.FONT_FAMILY};
            font-size: 18px;
            font-weight: 500;
            color: {Design.WARM_GRAY_500};
            margin-bottom: 8px;
        """)
        content_layout.addWidget(subtitle)
        
        # Stats grid
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(16)
        
        stats = [
            ("Tổng khách hàng", "1,284", "↑ 12% so với tháng trước", True),
            ("Khách hàng cá nhân", "856", "↑ 8% so với tháng trước", True),
            ("Doanh nghiệp", "428", "↑ 15% so với tháng trước", True),
            ("Hợp đồng đang hoạt động", "892", "↓ 2% so với tháng trước", False),
        ]
        
        for label, value, change, positive in stats:
            card = StatCard(label, value, change, positive)
            stats_layout.addWidget(card)
        
        content_layout.addLayout(stats_layout)
        
        # Action bar
        action_layout = QHBoxLayout()
        action_layout.setSpacing(12)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Tìm kiếm theo mã, tên, số điện thoại, email...")
        self.search_input.setStyleSheet(f"""
            QLineEdit {{
                font-family: {Design.FONT_FAMILY};
                font-size: 15px;
                padding: 12px 16px;
                border: 1px solid rgba(0,0,0,0.1);
                border-radius: {Design.RADIUS_SMALL}px;
                background-color: {Design.PURE_WHITE};
                color: {Design.NOTION_BLACK};
                min-width: 400px;
            }}
            QLineEdit:focus {{
                border: 2px solid {Design.NOTION_BLUE};
            }}
        """)
        action_layout.addWidget(self.search_input)
        action_layout.addStretch()
        
        btn_loc = StyledButton("⚙️ Lọc", "secondary")
        action_layout.addWidget(btn_loc)
        
        btn_xuat = StyledButton("📥 Xuất Excel", "secondary")
        action_layout.addWidget(btn_xuat)
        
        btn_them = StyledButton("+ Thêm mới", "primary")
        btn_them.clicked.connect(self.open_add_dialog)
        action_layout.addWidget(btn_them)
        
        content_layout.addLayout(action_layout)
        
        # Data table card
        table_card = StyledCard()
        table_layout = QVBoxLayout(table_card)
        table_layout.setContentsMargins(0, 0, 0, 0)
        table_layout.setSpacing(0)
        
        # Table header
        table_header = QWidget()
        table_header.setStyleSheet(f"""
            background-color: {Design.PURE_WHITE};
            border-bottom: 1px solid rgba(0,0,0,0.1);
        """)
        th_layout = QHBoxLayout(table_header)
        th_layout.setContentsMargins(20, 16, 20, 16)
        
        th_title = QLabel("Danh sách khách hàng")
        th_title.setStyleSheet(f"""
            font-family: {Design.FONT_FAMILY};
            font-size: 18px;
            font-weight: 700;
            color: {Design.NOTION_BLACK};
        """)
        th_layout.addWidget(th_title)
        th_layout.addStretch()
        
        btn_lich_su = StyledButton("📋 Xem lịch sử", "secondary")
        th_layout.addWidget(btn_lich_su)
        
        table_layout.addWidget(table_header)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "Khách hàng", "Loại", "Liên hệ", "Số HĐ", "Trạng thái", "Ngày ĐK", "Thao tác"
        ])
        
        # Table style
        self.table.setStyleSheet(f"""
            QTableWidget {{
                font-family: {Design.FONT_FAMILY};
                font-size: 14px;
                border: none;
                background-color: {Design.PURE_WHITE};
            }}
            QTableWidget::item {{
                padding: 12px 8px;
                border-bottom: 1px solid rgba(0,0,0,0.05);
            }}
            QTableWidget::item:hover {{
                background-color: rgba(0,0,0,0.02);
            }}
            QHeaderView::section {{
                font-family: {Design.FONT_FAMILY};
                font-size: 13px;
                font-weight: 600;
                color: {Design.WARM_GRAY_500};
                padding: 14px 8px;
                border: none;
                border-bottom: 1px solid rgba(0,0,0,0.1);
                background-color: {Design.WARM_WHITE};
            }}
        """)
        
        self.table.setAlternatingRowColors(False)
        self.table.setShowGrid(False)
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        
        # Set column widths
        self.table.setColumnWidth(0, 250)
        self.table.setColumnWidth(1, 100)
        self.table.setColumnWidth(2, 180)
        self.table.setColumnWidth(3, 70)
        self.table.setColumnWidth(4, 110)
        self.table.setColumnWidth(5, 90)
        self.table.setColumnWidth(6, 120)
        
        self.load_sample_data()
        
        table_layout.addWidget(self.table)
        
        # Pagination
        pagination = QWidget()
        pagination.setStyleSheet(f"""
            background-color: {Design.PURE_WHITE};
            border-top: 1px solid rgba(0,0,0,0.1);
        """)
        pg_layout = QHBoxLayout(pagination)
        pg_layout.setContentsMargins(20, 12, 20, 12)
        
        pg_info = QLabel("Hiển thị 1-5 / 1,284 khách hàng")
        pg_info.setStyleSheet(f"color: {Design.WARM_GRAY_500}; font-size: 14px;")
        pg_layout.addWidget(pg_info)
        pg_layout.addStretch()
        
        # Page buttons
        for i, page in enumerate(["←", "1", "2", "3", "...", "257", "→"]):
            btn = QPushButton(page)
            if page == "1":
                btn.setStyleSheet(f"""
                    QPushButton {{
                        background-color: {Design.NOTION_BLUE};
                        color: {Design.PURE_WHITE};
                        border: none;
                        border-radius: {Design.RADIUS_SMALL}px;
                        padding: 6px 12px;
                        font-family: {Design.FONT_FAMILY};
                        font-size: 14px;
                        font-weight: 600;
                        min-width: 32px;
                    }}
                """)
            else:
                btn.setStyleSheet(f"""
                    QPushButton {{
                        background-color: {Design.PURE_WHITE};
                        color: {Design.WARM_GRAY_500};
                        border: 1px solid rgba(0,0,0,0.1);
                        border-radius: {Design.RADIUS_SMALL}px;
                        padding: 6px 12px;
                        font-family: {Design.FONT_FAMILY};
                        font-size: 14px;
                        font-weight: 500;
                        min-width: 32px;
                    }}
                    QPushButton:hover {{
                        background-color: rgba(0,0,0,0.05);
                        color: {Design.NOTION_BLACK};
                    }}
                """)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            pg_layout.addWidget(btn)
        
        table_layout.addWidget(pagination)
        content_layout.addWidget(table_card)
        
        main_layout.addWidget(content)
        
    def create_nav_bar(self):
        """Create navigation bar"""
        nav = QWidget()
        nav.setStyleSheet(f"""
            QWidget {{
                background-color: {Design.PURE_WHITE};
                border-bottom: 1px solid rgba(0,0,0,0.1);
            }}
        """)
        nav.setFixedHeight(60)
        
        layout = QHBoxLayout(nav)
        layout.setContentsMargins(24, 0, 24, 0)
        layout.setSpacing(0)
        
        # Brand
        brand = QLabel("🏭 KhoSmart Pro")
        brand.setStyleSheet(f"""
            font-family: {Design.FONT_FAMILY};
            font-size: 20px;
            font-weight: 700;
            color: {Design.NOTION_BLACK};
            letter-spacing: -0.125px;
        """)
        layout.addWidget(brand)
        
        layout.addSpacing(48)
        
        # Nav links
        nav_items = [
            ("Khách hàng", True),
            ("Kho hàng", False),
            ("Hợp đồng", False),
            ("Hàng hóa", False),
            ("Báo cáo", False),
        ]
        
        for text, active in nav_items:
            link = QLabel(text)
            if active:
                link.setStyleSheet(f"""
                    font-family: {Design.FONT_FAMILY};
                    font-size: 15px;
                    font-weight: 600;
                    color: {Design.NOTION_BLUE};
                    padding: 0 16px;
                """)
            else:
                link.setStyleSheet(f"""
                    font-family: {Design.FONT_FAMILY};
                    font-size: 15px;
                    font-weight: 600;
                    color: {Design.WARM_GRAY_500};
                    padding: 0 16px;
                """)
            layout.addWidget(link)
        
        layout.addStretch()
        
        # CTA button
        btn = StyledButton("+ Thêm mới", "primary")
        btn.clicked.connect(self.open_add_dialog)
        layout.addWidget(btn)
        
        return nav
        
    def load_sample_data(self):
        """Load sample customer data"""
        sample_data = [
            {
                "ten": "Công ty TNHH Thương mại Hoàng Phát",
                "ma": "KH-DN-00001",
                "loai": "Doanh nghiệp",
                "sdt": "0912345678",
                "email": "hoangphat@gmail.com",
                "hop_dong": 5,
                "trang_thai": "active",
                "ngay_dk": "15/03/2023"
            },
            {
                "ten": "Nguyễn Văn An",
                "ma": "KH-CN-00002",
                "loai": "Cá nhân",
                "sdt": "0987654321",
                "email": "nguyenvanan@gmail.com",
                "hop_dong": 2,
                "trang_thai": "active",
                "ngay_dk": "20/05/2023"
            },
            {
                "ten": "Công ty CP Logistics Việt Nam",
                "ma": "KH-DN-00003",
                "loai": "Doanh nghiệp",
                "sdt": "0909123456",
                "email": "logisticsvn@corp.vn",
                "hop_dong": 8,
                "trang_thai": "active",
                "ngay_dk": "10/01/2023"
            },
            {
                "ten": "Trần Thị Bình",
                "ma": "KH-CN-00004",
                "loai": "Cá nhân",
                "sdt": "0934567890",
                "email": "tranbinh@email.com",
                "hop_dong": 1,
                "trang_thai": "active",
                "ngay_dk": "05/08/2023"
            },
            {
                "ten": "Công ty TNHH Xuất nhập khẩu Minh Tâm",
                "ma": "KH-DN-00005",
                "loai": "Doanh nghiệp",
                "sdt": "0978123456",
                "email": "minhtam@trade.com",
                "hop_dong": 3,
                "trang_thai": "inactive",
                "ngay_dk": "12/02/2023"
            },
        ]
        
        self.table.setRowCount(len(sample_data))
        
        for i, data in enumerate(sample_data):
            # Customer name & code
            name_widget = QWidget()
            name_layout = QVBoxLayout(name_widget)
            name_layout.setSpacing(4)
            name_layout.setContentsMargins(0, 0, 0, 0)
            
            name_label = QLabel(data["ten"])
            name_label.setStyleSheet(f"font-weight: 600; color: {Design.NOTION_BLACK};")
            name_layout.addWidget(name_label)
            
            code_label = QLabel(data["ma"])
            code_label.setStyleSheet(f"font-size: 13px; color: {Design.WARM_GRAY_300};")
            name_layout.addWidget(code_label)
            
            self.table.setCellWidget(i, 0, name_widget)
            
            # Type badge
            badge_type = "doanh_nghiep" if data["loai"] == "Doanh nghiệp" else "ca_nhan"
            self.table.setCellWidget(i, 1, Badge(data["loai"], badge_type))
            
            # Contact
            contact_widget = QWidget()
            contact_layout = QVBoxLayout(contact_widget)
            contact_layout.setSpacing(2)
            contact_layout.setContentsMargins(0, 0, 0, 0)
            
            sdt_label = QLabel(data["sdt"])
            sdt_label.setStyleSheet(f"color: {Design.NOTION_BLACK};")
            contact_layout.addWidget(sdt_label)
            
            email_label = QLabel(data["email"])
            email_label.setStyleSheet(f"font-size: 13px; color: {Design.WARM_GRAY_500};")
            contact_layout.addWidget(email_label)
            
            self.table.setCellWidget(i, 2, contact_widget)
            
            # Contract count
            self.table.setItem(i, 3, QTableWidgetItem(str(data["hop_dong"])))
            
            # Status badge
            status_badge = Badge("Đang hoạt động" if data["trang_thai"] == "active" else "Đã xóa",
                               "active" if data["trang_thai"] == "active" else "inactive")
            self.table.setCellWidget(i, 4, status_badge)
            
            # Registration date
            self.table.setItem(i, 5, QTableWidgetItem(data["ngay_dk"]))
            
            # Action buttons
            action_widget = QWidget()
            action_layout = QHBoxLayout(action_widget)
            action_layout.setSpacing(8)
            action_layout.setContentsMargins(0, 0, 0, 0)
            
            for icon, title in [("👁️", "Xem"), ("✏️", "Sửa"), ("📋", "Lịch sử")]:
                btn = QPushButton(icon)
                btn.setStyleSheet(f"""
                    QPushButton {{
                        background-color: transparent;
                        border: 1px solid rgba(0,0,0,0.1);
                        border-radius: {Design.RADIUS_SMALL}px;
                        padding: 6px;
                        font-size: 14px;
                    }}
                    QPushButton:hover {{
                        background-color: rgba(0,0,0,0.05);
                    }}
                """)
                btn.setFixedSize(32, 32)
                btn.setCursor(Qt.CursorShape.PointingHandCursor)
                btn.setToolTip(title)
                
                if title == "Xem":
                    btn.clicked.connect(lambda checked, d=data: self.open_detail_dialog(d))
                
                action_layout.addWidget(btn)
            
            self.table.setCellWidget(i, 6, action_widget)
            
    def open_add_dialog(self):
        """Open add customer dialog"""
        dialog = ThemKhachHangDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            QMessageBox.information(self, "Thành công", "Đã thêm khách hàng mới!")
            
    def open_detail_dialog(self, customer_data):
        """Open customer detail dialog"""
        dialog = ChiTietKhachHangDialog(customer_data, self)
        dialog.exec()


# ==================== MAIN ENTRY ====================
def main():
    app = QApplication(sys.argv)
    
    # Set application font
    font = QFont("Inter", 10)
    font.setStyleHint(QFont.StyleHint.SansSerif)
    app.setFont(font)
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
