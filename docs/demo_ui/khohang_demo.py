"""
Demo PyQt6 - Quản lý Kho hàng
Design System: Notion-inspired
Tech Stack: Python 3.10+ + PyQt6
"""

import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QPushButton, QLabel, QLineEdit,
    QDialog, QFormLayout, QComboBox, QTextEdit, QProgressBar,
    QGridLayout, QHeaderView, QMessageBox, QFrame, QTabWidget,
    QSplitter, QGroupBox, QSpinBox, QDoubleSpinBox
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QColor, QPalette, QIcon, QPainter, QPen


# ==================== DESIGN CONSTANTS ====================
class Design:
    """Design System Constants"""
    NOTION_BLACK = "#000000f2"
    PURE_WHITE = "#ffffff"
    NOTION_BLUE = "#0075de"
    ACTIVE_BLUE = "#005bab"
    WARM_WHITE = "#f6f5f4"
    WARM_DARK = "#31302e"
    WARM_GRAY_500 = "#615d59"
    WARM_GRAY_300 = "#a39e98"
    GREEN = "#1aae39"
    ORANGE = "#dd5b00"
    RED = "#dc2626"
    BADGE_BLUE_BG = "#f2f9ff"
    BADGE_BLUE_TEXT = "#097fe8"
    FONT_FAMILY = "Inter, -apple-system, system-ui, Segoe UI, Helvetica, Arial, sans-serif"
    PADDING_SMALL = 8
    PADDING_MEDIUM = 16
    PADDING_LARGE = 24
    RADIUS_SMALL = 4
    RADIUS_MEDIUM = 8
    RADIUS_LARGE = 12
    RADIUS_PILL = 9999


class StyledButton(QPushButton):
    """Custom styled button"""
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


class Badge(QLabel):
    """Pill badge"""
    def __init__(self, text, badge_type="active", parent=None):
        super().__init__(text, parent)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        colors = {
            "active": ("#e6f7e9", Design.GREEN),
            "inactive": ("#f5f5f5", Design.WARM_GRAY_500),
            "maintenance": ("#fef3e6", Design.ORANGE),
            "full": ("#fef2f2", Design.RED),
            "available": (Design.BADGE_BLUE_BG, Design.BADGE_BLUE_TEXT),
        }
        bg_color, text_color = colors.get(badge_type, colors["active"])
            
        self.setStyleSheet(f"""
            QLabel {{
                background-color: {bg_color};
                color: {text_color};
                border-radius: {Design.RADIUS_PILL}px;
                padding: 4px 12px;
                font-family: {Design.FONT_FAMILY};
                font-size: 12px;
                font-weight: 600;
            }}
        """)


class StatCard(StyledCard):
    """Statistics card"""
    def __init__(self, label, value, change=None, positive=True, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(8)
        
        self.label = QLabel(label)
        self.label.setStyleSheet(f"""
            font-family: {Design.FONT_FAMILY};
            font-size: 14px;
            font-weight: 500;
            color: {Design.WARM_GRAY_500};
        """)
        layout.addWidget(self.label)
        
        self.value = QLabel(value)
        self.value.setStyleSheet(f"""
            font-family: {Design.FONT_FAMILY};
            font-size: 32px;
            font-weight: 700;
            color: {Design.NOTION_BLACK};
        """)
        layout.addWidget(self.value)
        
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


class CapacityIndicator(QWidget):
    """Custom widget showing warehouse capacity"""
    def __init__(self, used, total, parent=None):
        super().__init__(parent)
        self.used = used
        self.total = total
        self.percentage = (used / total) * 100 if total > 0 else 0
        self.setMinimumHeight(60)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Background bar
        bg_rect = self.rect().adjusted(0, 30, 0, -10)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor(Design.WARM_WHITE))
        painter.drawRoundedRect(bg_rect, 4, 4)
        
        # Progress bar
        if self.percentage > 0:
            width = int(bg_rect.width() * (self.percentage / 100))
            progress_rect = bg_rect.adjusted(0, 0, width - bg_rect.width(), 0)
            
            # Color based on percentage
            if self.percentage >= 90:
                color = Design.RED
            elif self.percentage >= 70:
                color = Design.ORANGE
            else:
                color = Design.GREEN
                
            painter.setBrush(QColor(color))
            painter.drawRoundedRect(progress_rect, 4, 4)
        
        # Percentage text
        painter.setPen(QColor(Design.NOTION_BLACK))
        font = QFont("Inter", 14, QFont.Weight.Bold)
        painter.setFont(font)
        text = f"{self.percentage:.1f}%"
        painter.drawText(self.rect().adjusted(0, 0, 0, -35), 
                        Qt.AlignmentFlag.AlignCenter, text)
        
        # Detail text
        painter.setPen(QColor(Design.WARM_GRAY_500))
        font = QFont("Inter", 11)
        painter.setFont(font)
        detail = f"{self.used:,} / {self.total:,} m²"
        painter.drawText(self.rect().adjusted(0, 45, 0, 0), 
                        Qt.AlignmentFlag.AlignCenter, detail)


class ThemKhoDialog(QDialog):
    """Dialog for adding new warehouse"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Thêm mới kho hàng")
        self.setMinimumSize(550, 550)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(32, 32, 32, 32)
        
        # Header
        header = QLabel("🏭 Thêm mới kho hàng")
        header.setStyleSheet(f"""
            font-family: {Design.FONT_FAMILY};
            font-size: 28px;
            font-weight: 700;
            color: {Design.NOTION_BLACK};
        """)
        layout.addWidget(header)
        
        # Form card
        card = StyledCard()
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(24, 24, 24, 24)
        
        form = QFormLayout()
        form.setSpacing(16)
        
        # Mã kho
        self.ma_kho = QLineEdit("KHO-0015")
        self.ma_kho.setReadOnly(True)
        self.ma_kho.setStyleSheet(self.input_style(True))
        form.addRow(self.label_style("Mã kho"), self.ma_kho)
        
        # Tên kho
        self.ten_kho = QLineEdit()
        self.ten_kho.setPlaceholderText("Nhập tên kho")
        self.ten_kho.setStyleSheet(self.input_style())
        form.addRow(self.label_style("Tên kho *"), self.ten_kho)
        
        # Địa chỉ
        self.dia_chi = QTextEdit()
        self.dia_chi.setPlaceholderText("Nhập địa chỉ kho")
        self.dia_chi.setMaximumHeight(60)
        self.dia_chi.setStyleSheet(self.input_style())
        form.addRow(self.label_style("Địa chỉ *"), self.dia_chi)
        
        # Diện tích tổng
        self.dien_tich = QDoubleSpinBox()
        self.dien_tich.setRange(100, 100000)
        self.dien_tich.setValue(1000)
        self.dien_tich.setSuffix(" m²")
        self.dien_tich.setStyleSheet(self.input_style())
        form.addRow(self.label_style("Tổng diện tích *"), self.dien_tich)
        
        # Sức chứa tối đa
        self.suc_chua = QSpinBox()
        self.suc_chua.setRange(10, 10000)
        self.suc_chua.setValue(100)
        self.suc_chua.setSuffix(" vị trí")
        self.suc_chua.setStyleSheet(self.input_style())
        form.addRow(self.label_style("Sức chứa tối đa *"), self.suc_chua)
        
        # Trạng thái
        self.trang_thai = QComboBox()
        self.trang_thai.addItems(["Hoạt động", "Bảo trì", "Ngừng hoạt động"])
        self.trang_thai.setStyleSheet(self.input_style())
        form.addRow(self.label_style("Trạng thái"), self.trang_thai)
        
        # Ghi chú
        self.ghi_chu = QTextEdit()
        self.ghi_chu.setPlaceholderText("Thông tin thêm về kho...")
        self.ghi_chu.setMaximumHeight(80)
        self.ghi_chu.setStyleSheet(self.input_style())
        form.addRow(self.label_style("Ghi chú"), self.ghi_chu)
        
        card_layout.addLayout(form)
        layout.addWidget(card)
        
        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        btn_huy = StyledButton("Hủy bỏ", "secondary")
        btn_huy.clicked.connect(self.reject)
        btn_layout.addWidget(btn_huy)
        
        btn_luu = StyledButton("Lưu kho hàng", "primary")
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
        
    def input_style(self, readonly=False):
        if readonly:
            return f"""
                QLineEdit, QTextEdit, QComboBox, QSpinBox, QDoubleSpinBox {{
                    font-family: {Design.FONT_FAMILY};
                    font-size: 15px;
                    padding: 10px 14px;
                    border: 1px solid rgba(0,0,0,0.1);
                    border-radius: {Design.RADIUS_SMALL}px;
                    background-color: {Design.WARM_WHITE};
                    color: {Design.WARM_GRAY_500};
                }}
            """
        return f"""
            QLineEdit, QTextEdit, QComboBox, QSpinBox, QDoubleSpinBox {{
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


class KhoDetailDialog(QDialog):
    """Dialog showing warehouse details"""
    def __init__(self, kho_data, parent=None):
        super().__init__(parent)
        self.kho_data = kho_data
        self.setWindowTitle("Chi tiết kho hàng")
        self.setMinimumSize(800, 600)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(32, 32, 32, 32)
        
        # Header
        header_layout = QHBoxLayout()
        
        info_layout = QVBoxLayout()
        name = QLabel(f"🏭 {self.kho_data['ten']}")
        name.setStyleSheet(f"""
            font-family: {Design.FONT_FAMILY};
            font-size: 28px;
            font-weight: 700;
            color: {Design.NOTION_BLACK};
        """)
        info_layout.addWidget(name)
        
        meta = QLabel(f"Mã: {self.kho_data['ma']}  •  Địa chỉ: {self.kho_data['dia_chi']}")
        meta.setStyleSheet(f"color: {Design.WARM_GRAY_500}; font-size: 14px;")
        info_layout.addWidget(meta)
        
        header_layout.addLayout(info_layout, 1)
        
        # Actions
        btn_sua = StyledButton("✏️ Chỉnh sửa", "secondary")
        header_layout.addWidget(btn_sua)
        
        layout.addLayout(header_layout)
        
        # Tabs
        tabs = QTabWidget()
        tabs.setStyleSheet(f"""
            QTabWidget::pane {{
                border: 1px solid rgba(0,0,0,0.1);
                border-radius: {Design.RADIUS_LARGE}px;
                background-color: {Design.PURE_WHITE};
            }}
            QTabBar::tab {{
                font-family: {Design.FONT_FAMILY};
                font-size: 14px;
                font-weight: 600;
                padding: 12px 24px;
                color: {Design.WARM_GRAY_500};
                border: none;
                background: transparent;
            }}
            QTabBar::tab:selected {{
                color: {Design.NOTION_BLUE};
                border-bottom: 2px solid {Design.NOTION_BLUE};
            }}
        """)
        
        # Tab 1: Tổng quan
        tab_overview = QWidget()
        overview_layout = QVBoxLayout(tab_overview)
        overview_layout.setSpacing(20)
        overview_layout.setContentsMargins(20, 20, 20, 20)
        
        # Stats grid
        stats_grid = QHBoxLayout()
        stats_grid.setSpacing(16)
        
        stats = [
            ("Tổng diện tích", f"{self.kho_data['dien_tich']:,} m²"),
            ("Đã sử dụng", f"{self.kho_data['da_dung']:,} m²"),
            ("Còn trống", f"{self.kho_data['con_trong']:,} m²"),
        ]
        
        for label, value in stats:
            card = StyledCard()
            card_layout = QVBoxLayout(card)
            card_layout.setContentsMargins(16, 16, 16, 16)
            
            lbl = QLabel(label)
            lbl.setStyleSheet(f"color: {Design.WARM_GRAY_500}; font-size: 13px;")
            card_layout.addWidget(lbl)
            
            val = QLabel(value)
            val.setStyleSheet(f"font-size: 24px; font-weight: 700; color: {Design.NOTION_BLACK};")
            card_layout.addWidget(val)
            
            stats_grid.addWidget(card)
        
        overview_layout.addLayout(stats_grid)
        
        # Capacity indicator
        capacity_card = StyledCard()
        capacity_layout = QVBoxLayout(capacity_card)
        capacity_layout.setContentsMargins(20, 20, 20, 20)
        
        cap_title = QLabel("📊 Tỷ lệ lấp đầy")
        cap_title.setStyleSheet(f"font-size: 18px; font-weight: 700; margin-bottom: 10px;")
        capacity_layout.addWidget(cap_title)
        
        indicator = CapacityIndicator(
            self.kho_data['da_dung'], 
            self.kho_data['dien_tich']
        )
        capacity_layout.addWidget(indicator)
        
        overview_layout.addWidget(capacity_card)
        overview_layout.addStretch()
        
        tabs.addTab(tab_overview, "📊 Tổng quan")
        
        # Tab 2: Vị trí lưu trữ
        tab_vitri = QWidget()
        vitri_layout = QVBoxLayout(tab_vitri)
        vitri_layout.setContentsMargins(20, 20, 20, 20)
        
        # Vitri table
        vitri_table = QTableWidget()
        vitri_table.setColumnCount(5)
        vitri_table.setHorizontalHeaderLabels([
            "Mã vị trí", "Diện tích", "Giá thuê", "Trạng thái", "Khách hàng"
        ])
        vitri_table.setStyleSheet(f"""
            QTableWidget {{
                border: none;
                background-color: {Design.PURE_WHITE};
            }}
            QHeaderView::section {{
                background-color: {Design.WARM_WHITE};
                color: {Design.WARM_GRAY_500};
                font-weight: 600;
                padding: 12px;
                border: none;
                border-bottom: 1px solid rgba(0,0,0,0.1);
            }}
        """)
        
        sample_vitri = [
            ("A-01", "50 m²", "₫5,000,000", "Đang thuê", "Công ty TNHH Hoàng Phát"),
            ("A-02", "50 m²", "₫5,000,000", "Trống", "-"),
            ("A-03", "75 m²", "₫7,500,000", "Đang thuê", "Công ty CP Logistics"),
            ("B-01", "100 m²", "₫10,000,000", "Bảo trì", "-"),
            ("B-02", "100 m²", "₫10,000,000", "Trống", "-"),
        ]
        
        vitri_table.setRowCount(len(sample_vitri))
        for i, row in enumerate(sample_vitri):
            for j, val in enumerate(row):
                if j == 3:  # Status column
                    badge = Badge(val, "active" if val == "Đang thuê" else 
                                 "available" if val == "Trống" else "maintenance")
                    vitri_table.setCellWidget(i, j, badge)
                else:
                    vitri_table.setItem(i, j, QTableWidgetItem(val))
        
        vitri_table.resizeColumnsToContents()
        vitri_layout.addWidget(vitri_table)
        tabs.addTab(tab_vitri, "📍 Vị trí lưu trữ")
        
        # Tab 3: Lịch sử
        tab_history = QWidget()
        history_layout = QVBoxLayout(tab_history)
        history_layout.setContentsMargins(20, 20, 20, 20)
        
        history_label = QLabel("📜 Lịch sử hoạt động kho")
        history_label.setStyleSheet(f"font-size: 18px; font-weight: 700;")
        history_layout.addWidget(history_label)
        
        history_list = QTableWidget()
        history_list.setColumnCount(4)
        history_list.setHorizontalHeaderLabels([
            "Thời gian", "Hoạt động", "Người thực hiện", "Chi tiết"
        ])
        
        history_data = [
            ("17/04/2026 14:30", "Cập nhật thông tin", "Admin", "Thay đổi số điện thoại liên hệ"),
            ("15/03/2026 09:00", "Kiểm tra định kỳ", "Nhân viên A", "Hoạt động bình thường"),
            ("10/02/2026 08:00", "Bảo trì", "Kỹ thuật", "Sửa chữa hệ thống điện"),
        ]
        
        history_list.setRowCount(len(history_data))
        for i, row in enumerate(history_data):
            for j, val in enumerate(row):
                history_list.setItem(i, j, QTableWidgetItem(val))
        
        history_layout.addWidget(history_list)
        tabs.addTab(tab_history, "📜 Lịch sử")
        
        layout.addWidget(tabs)
        
        # Close button
        close_btn = StyledButton("Đóng", "secondary")
        close_btn.clicked.connect(self.accept)
        btn_container = QHBoxLayout()
        btn_container.addStretch()
        btn_container.addWidget(close_btn)
        layout.addLayout(btn_container)


class MainWindow(QMainWindow):
    """Main application window for Quan ly kho hang"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🏭 KhoSmart Pro - Quản lý kho hàng")
        self.setMinimumSize(1200, 800)
        self.setup_ui()
        
    def setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        
        main_layout = QVBoxLayout(central)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Navigation
        nav = self.create_nav_bar()
        main_layout.addWidget(nav)
        
        # Content
        content = QWidget()
        content.setStyleSheet(f"background-color: {Design.WARM_WHITE};")
        content_layout = QVBoxLayout(content)
        content_layout.setSpacing(24)
        content_layout.setContentsMargins(32, 32, 32, 32)
        
        # Header
        header = QLabel("Quản lý kho hàng")
        header.setStyleSheet(f"""
            font-family: {Design.FONT_FAMILY};
            font-size: 40px;
            font-weight: 700;
            color: {Design.NOTION_BLACK};
        """)
        content_layout.addWidget(header)
        
        subtitle = QLabel("Quản lý danh sách kho và vị trí lưu trữ")
        subtitle.setStyleSheet(f"color: {Design.WARM_GRAY_500}; font-size: 18px;")
        content_layout.addWidget(subtitle)
        
        # Stats
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(16)
        
        stats = [
            ("Tổng số kho", "5", None, True),
            ("Kho đang hoạt động", "4", None, True),
            ("Đang bảo trì", "1", None, True),
            ("Tổng diện tích", "15,000 m²", "↑ 5% so với tháng trước", True),
        ]
        
        for label, value, change, positive in stats:
            card = StatCard(label, value, change, positive)
            stats_layout.addWidget(card)
        
        content_layout.addLayout(stats_layout)
        
        # Action bar
        action_layout = QHBoxLayout()
        action_layout.setSpacing(12)
        
        self.search = QLineEdit()
        self.search.setPlaceholderText("🔍 Tìm kiếm theo mã, tên kho...")
        self.search.setStyleSheet(f"""
            QLineEdit {{
                font-family: {Design.FONT_FAMILY};
                font-size: 15px;
                padding: 12px 16px;
                border: 1px solid rgba(0,0,0,0.1);
                border-radius: {Design.RADIUS_SMALL}px;
                background-color: {Design.PURE_WHITE};
                min-width: 350px;
            }}
        """)
        action_layout.addWidget(self.search)
        action_layout.addStretch()
        
        btn_loc = StyledButton("⚙️ Lọc", "secondary")
        action_layout.addWidget(btn_loc)
        
        btn_them = StyledButton("+ Thêm kho mới", "primary")
        btn_them.clicked.connect(self.open_add_dialog)
        action_layout.addWidget(btn_them)
        
        content_layout.addLayout(action_layout)
        
        # Table card
        table_card = StyledCard()
        table_layout = QVBoxLayout(table_card)
        table_layout.setContentsMargins(0, 0, 0, 0)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "Kho hàng", "Diện tích", "Sức chứa", "Đã sử dụng", "Trạng thái", "Vị trí trống", "Thao tác"
        ])
        
        self.table.setStyleSheet(f"""
            QTableWidget {{
                border: none;
                background-color: {Design.PURE_WHITE};
            }}
            QHeaderView::section {{
                background-color: {Design.WARM_WHITE};
                color: {Design.WARM_GRAY_500};
                font-weight: 600;
                padding: 14px 8px;
                border: none;
                border-bottom: 1px solid rgba(0,0,0,0.1);
            }}
            QTableWidget::item {{
                padding: 12px 8px;
                border-bottom: 1px solid rgba(0,0,0,0.05);
            }}
        """)
        
        self.table.setShowGrid(False)
        self.table.verticalHeader().setVisible(False)
        
        # Column widths
        self.table.setColumnWidth(0, 220)
        self.table.setColumnWidth(1, 120)
        self.table.setColumnWidth(2, 100)
        self.table.setColumnWidth(3, 150)
        self.table.setColumnWidth(4, 120)
        self.table.setColumnWidth(5, 100)
        self.table.setColumnWidth(6, 120)
        
        self.load_sample_data()
        table_layout.addWidget(self.table)
        content_layout.addWidget(table_card)
        
        main_layout.addWidget(content)
        
    def create_nav_bar(self):
        nav = QWidget()
        nav.setStyleSheet(f"""
            background-color: {Design.PURE_WHITE};
            border-bottom: 1px solid rgba(0,0,0,0.1);
        """)
        nav.setFixedHeight(60)
        
        layout = QHBoxLayout(nav)
        layout.setContentsMargins(24, 0, 24, 0)
        
        brand = QLabel("🏭 KhoSmart Pro")
        brand.setStyleSheet(f"""
            font-family: {Design.FONT_FAMILY};
            font-size: 20px;
            font-weight: 700;
            color: {Design.NOTION_BLACK};
        """)
        layout.addWidget(brand)
        layout.addSpacing(48)
        
        nav_items = [
            ("Khách hàng", False),
            ("Kho hàng", True),
            ("Hợp đồng", False),
            ("Hàng hóa", False),
            ("Báo cáo", False),
        ]
        
        for text, active in nav_items:
            link = QLabel(text)
            color = Design.NOTION_BLUE if active else Design.WARM_GRAY_500
            link.setStyleSheet(f"""
                font-family: {Design.FONT_FAMILY};
                font-size: 15px;
                font-weight: 600;
                color: {color};
                padding: 0 16px;
            """)
            layout.addWidget(link)
        
        layout.addStretch()
        
        btn = StyledButton("+ Thêm mới", "primary")
        btn.clicked.connect(self.open_add_dialog)
        layout.addWidget(btn)
        
        return nav
        
    def load_sample_data(self):
        sample_data = [
            {
                "ten": "Kho Hóc Môn - Khu vực 1",
                "ma": "KHO-HM-01",
                "dia_chi": "123 Quốc lộ 22, Hóc Môn, TP.HCM",
                "dien_tich": 5000,
                "suc_chua": 50,
                "da_dung": 4200,
                "trang_thai": "active",
                "vitri_trong": 5,
            },
            {
                "ten": "Kho Củ Chi - Khu vực 2",
                "ma": "KHO-CC-01",
                "dia_chi": "456 Tỉnh lộ 8, Củ Chi, TP.HCM",
                "dien_tich": 3500,
                "suc_chua": 35,
                "da_dung": 2800,
                "trang_thai": "active",
                "vitri_trong": 8,
            },
            {
                "ten": "Kho Bình Chánh - Trung tâm",
                "ma": "KHO-BC-01",
                "dia_chi": "789 Nguyễn Văn Linh, Bình Chánh, TP.HCM",
                "dien_tich": 4200,
                "suc_chua": 42,
                "da_dung": 3800,
                "trang_thai": "maintenance",
                "vitri_trong": 0,
            },
            {
                "ten": "Kho Thủ Đức - Khu công nghệ",
                "ma": "KHO-TD-01",
                "dia_chi": "321 Xa lộ Hà Nội, Thủ Đức, TP.HCM",
                "dien_tich": 2800,
                "suc_chua": 28,
                "da_dung": 1200,
                "trang_thai": "active",
                "vitri_trong": 15,
            },
            {
                "ten": "Kho Quận 9 - Khu công nghiệp",
                "ma": "KHO-Q9-01",
                "dia_chi": "654 Đường số 10, Quận 9, TP.HCM",
                "dien_tich": 1500,
                "suc_chua": 15,
                "da_dung": 1350,
                "trang_thai": "active",
                "vitri_trong": 2,
            },
        ]
        
        self.table.setRowCount(len(sample_data))
        
        for i, data in enumerate(sample_data):
            # Name & code
            name_widget = QWidget()
            name_layout = QVBoxLayout(name_widget)
            name_layout.setSpacing(4)
            name_layout.setContentsMargins(0, 0, 0, 0)
            
            name = QLabel(data["ten"])
            name.setStyleSheet(f"font-weight: 600; color: {Design.NOTION_BLACK};")
            name_layout.addWidget(name)
            
            code = QLabel(data["ma"])
            code.setStyleSheet(f"font-size: 13px; color: {Design.WARM_GRAY_300};")
            name_layout.addWidget(code)
            
            self.table.setCellWidget(i, 0, name_widget)
            
            # Area
            self.table.setItem(i, 1, QTableWidgetItem(f"{data['dien_tich']:,} m²"))
            
            # Capacity
            self.table.setItem(i, 2, QTableWidgetItem(f"{data['suc_chua']} vị trí"))
            
            # Capacity indicator
            indicator = CapacityIndicator(data['da_dung'], data['dien_tich'])
            indicator.setMaximumWidth(150)
            self.table.setCellWidget(i, 3, indicator)
            
            # Status
            status_map = {
                "active": ("Hoạt động", "active"),
                "maintenance": ("Bảo trì", "maintenance"),
                "inactive": ("Ngừng", "inactive"),
            }
            status_text, status_type = status_map.get(data["trang_thai"], ("Không xác định", "inactive"))
            self.table.setCellWidget(i, 4, Badge(status_text, status_type))
            
            # Available positions
            self.table.setItem(i, 5, QTableWidgetItem(str(data['vitri_trong'])))
            
            # Actions
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
                """)
                btn.setFixedSize(32, 32)
                btn.setToolTip(title)
                
                if title == "Xem":
                    btn.clicked.connect(lambda checked, d=data: self.open_detail_dialog(d))
                
                action_layout.addWidget(btn)
            
            self.table.setCellWidget(i, 6, action_widget)
            
    def open_add_dialog(self):
        dialog = ThemKhoDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            QMessageBox.information(self, "Thành công", "Đã thêm kho hàng mới!")
            
    def open_detail_dialog(self, kho_data):
        dialog = KhoDetailDialog(kho_data, self)
        dialog.exec()


def main():
    app = QApplication(sys.argv)
    font = QFont("Inter", 10)
    font.setStyleHint(QFont.StyleHint.SansSerif)
    app.setFont(font)
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
