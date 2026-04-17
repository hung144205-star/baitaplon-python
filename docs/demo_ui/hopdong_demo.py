"""
Demo PyQt6 - Quản lý Hợp đồng thuê
Design System: Notion-inspired
Tech Stack: Python 3.10+ + PyQt6
"""

import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QPushButton, QLabel, QLineEdit,
    QDialog, QFormLayout, QComboBox, QTextEdit, QDateEdit, QSpinBox,
    QDoubleSpinBox, QTabWidget, QHeaderView, QMessageBox, QFrame,
    QStackedWidget, QListWidget, QListWidgetItem
)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont


# ==================== DESIGN CONSTANTS ====================
class Design:
    NOTION_BLACK = "#000000f2"
    PURE_WHITE = "#ffffff"
    NOTION_BLUE = "#0075de"
    ACTIVE_BLUE = "#005bab"
    WARM_WHITE = "#f6f5f4"
    WARM_GRAY_500 = "#615d59"
    WARM_GRAY_300 = "#a39e98"
    GREEN = "#1aae39"
    ORANGE = "#dd5b00"
    RED = "#dc2626"
    BADGE_BLUE_BG = "#f2f9ff"
    BADGE_BLUE_TEXT = "#097fe8"
    FONT_FAMILY = "Inter, -apple-system, system-ui, Segoe UI, Helvetica, Arial, sans-serif"
    RADIUS_SMALL = 4
    RADIUS_LARGE = 12


class StyledButton(QPushButton):
    def __init__(self, text, button_type="primary", icon_text="", parent=None):
        super().__init__(f"{icon_text} {text}" if icon_text else text, parent)
        self.button_type = button_type
        self.apply_style()
        
    def apply_style(self):
        styles = {
            "primary": f"""
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
                QPushButton:hover {{ background-color: {Design.ACTIVE_BLUE}; }}
            """,
            "secondary": f"""
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
                QPushButton:hover {{ background-color: rgba(0,0,0,0.08); }}
            """,
            "success": f"""
                QPushButton {{
                    background-color: {Design.GREEN};
                    color: {Design.PURE_WHITE};
                    border: none;
                    border-radius: {Design.RADIUS_SMALL}px;
                    padding: 10px 20px;
                    font-family: {Design.FONT_FAMILY};
                    font-size: 14px;
                    font-weight: 600;
                }}
            """,
            "warning": f"""
                QPushButton {{
                    background-color: {Design.ORANGE};
                    color: {Design.PURE_WHITE};
                    border: none;
                    border-radius: {Design.RADIUS_SMALL}px;
                    padding: 10px 20px;
                    font-family: {Design.FONT_FAMILY};
                    font-size: 14px;
                    font-weight: 600;
                }}
            """
        }
        self.setStyleSheet(styles.get(self.button_type, styles["primary"]))
        self.setCursor(Qt.CursorShape.PointingHandCursor)


class StyledCard(QFrame):
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
    def __init__(self, text, badge_type="active", parent=None):
        super().__init__(text, parent)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        colors = {
            "active": ("#e6f7e9", Design.GREEN),
            "expired": ("#f5f5f5", Design.WARM_GRAY_500),
            "warning": ("#fef3e6", Design.ORANGE),
            "pending": (Design.BADGE_BLUE_BG, Design.BADGE_BLUE_TEXT),
        }
        bg_color, text_color = colors.get(badge_type, colors["active"])
            
        self.setStyleSheet(f"""
            QLabel {{
                background-color: {bg_color};
                color: {text_color};
                border-radius: 9999px;
                padding: 4px 12px;
                font-family: {Design.FONT_FAMILY};
                font-size: 12px;
                font-weight: 600;
            }}
        """)


class StatCard(StyledCard):
    def __init__(self, label, value, change=None, positive=True, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(8)
        
        self.label = QLabel(label)
        self.label.setStyleSheet(f"color: {Design.WARM_GRAY_500}; font-size: 14px;")
        layout.addWidget(self.label)
        
        self.value = QLabel(value)
        self.value.setStyleSheet(f"font-size: 32px; font-weight: 700; color: {Design.NOTION_BLACK};")
        layout.addWidget(self.value)
        
        if change:
            self.change = QLabel(change)
            color = Design.GREEN if positive else Design.ORANGE
            self.change.setStyleSheet(f"color: {color}; font-size: 14px; font-weight: 500;")
            layout.addWidget(self.change)


class NavigationBar(QWidget):
    """Shared navigation bar for all modules"""
    def __init__(self, current_module="hopdong", parent=None):
        super().__init__(parent)
        self.current_module = current_module
        self.setup_ui()
        
    def setup_ui(self):
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {Design.PURE_WHITE};
                border-bottom: 1px solid rgba(0,0,0,0.1);
            }}
        """)
        self.setFixedHeight(60)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(24, 0, 24, 0)
        
        # Brand
        brand = QLabel("🏭 KhoSmart Pro")
        brand.setStyleSheet(f"""
            font-family: {Design.FONT_FAMILY};
            font-size: 20px;
            font-weight: 700;
            color: {Design.NOTION_BLACK};
        """)
        layout.addWidget(brand)
        layout.addSpacing(48)
        
        # Nav links with navigation
        nav_items = [
            ("Khách hàng", "khachhang"),
            ("Kho hàng", "khohang"),
            ("Hợp đồng", "hopdong"),
            ("Hàng hóa", "hanghoa"),
            ("Báo cáo", "baocao"),
        ]
        
        for text, module in nav_items:
            link = QPushButton(text)
            is_active = module == self.current_module
            color = Design.NOTION_BLUE if is_active else Design.WARM_GRAY_500
            link.setStyleSheet(f"""
                QPushButton {{
                    font-family: {Design.FONT_FAMILY};
                    font-size: 15px;
                    font-weight: 600;
                    color: {color};
                    padding: 0 16px;
                    border: none;
                    background: transparent;
                }}
                QPushButton:hover {{ color: {Design.NOTION_BLACK}; }}
            """)
            link.setCursor(Qt.CursorShape.PointingHandCursor)
            link.clicked.connect(lambda checked, m=module: self.navigate_to(m))
            layout.addWidget(link)
        
        layout.addStretch()
        
        # Quick add button
        btn = StyledButton("+ Thêm mới", "primary")
        layout.addWidget(btn)
        
    def navigate_to(self, module):
        """Navigate to different modules"""
        if module == self.current_module:
            return
            
        # Import and open other modules
        if module == "khachhang":
            try:
                from khachhang_demo import MainWindow as KhachHangWindow
                self.new_window = KhachHangWindow()
                self.new_window.show()
                self.window().close()
            except ImportError:
                QMessageBox.information(self, "Thông báo", "Module Quản lý khách hàng")
                
        elif module == "khohang":
            try:
                from khohang_demo import MainWindow as KhoHangWindow
                self.new_window = KhoHangWindow()
                self.new_window.show()
                self.window().close()
            except ImportError:
                QMessageBox.information(self, "Thông báo", "Module Quản lý kho hàng")
                
        elif module == "hopdong":
            # Already here
            pass
        else:
            QMessageBox.information(self, "Thông báo", f"Module {module} đang phát triển")


class TaoHopDongDialog(QDialog):
    """Dialog for creating new contract"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Tạo hợp đồng thuê mới")
        self.setMinimumSize(700, 750)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(32, 32, 32, 32)
        
        # Header
        header = QLabel("📄 Tạo hợp đồng thuê mới")
        header.setStyleSheet(f"font-size: 28px; font-weight: 700; color: {Design.NOTION_BLACK};")
        layout.addWidget(header)
        
        # Wizard steps
        steps = QLabel("Bước 1/3: Chọn khách hàng → Bước 2/3: Chọn vị trí → Bước 3/3: Xác nhận")
        steps.setStyleSheet(f"color: {Design.WARM_GRAY_500}; font-size: 14px;")
        layout.addWidget(steps)
        
        # Main card
        card = StyledCard()
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(24, 24, 24, 24)
        
        # Stacked widget for wizard
        self.wizard = QStackedWidget()
        
        # Step 1: Select customer
        step1 = self.create_step1()
        self.wizard.addWidget(step1)
        
        # Step 2: Select warehouse position
        step2 = self.create_step2()
        self.wizard.addWidget(step2)
        
        # Step 3: Contract details
        step3 = self.create_step3()
        self.wizard.addWidget(step3)
        
        card_layout.addWidget(self.wizard)
        layout.addWidget(card)
        
        # Navigation buttons
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        self.btn_prev = StyledButton("← Quay lại", "secondary")
        self.btn_prev.clicked.connect(self.prev_step)
        self.btn_prev.setVisible(False)
        btn_layout.addWidget(self.btn_prev)
        
        self.btn_next = StyledButton("Tiếp theo →", "primary")
        self.btn_next.clicked.connect(self.next_step)
        btn_layout.addWidget(self.btn_next)
        
        self.btn_save = StyledButton("✓ Lưu hợp đồng", "success")
        self.btn_save.clicked.connect(self.accept)
        self.btn_save.setVisible(False)
        btn_layout.addWidget(self.btn_save)
        
        layout.addLayout(btn_layout)
        
    def create_step1(self):
        """Step 1: Select customer"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(16)
        
        title = QLabel("👤 Bước 1: Chọn khách hàng")
        title.setStyleSheet(f"font-size: 20px; font-weight: 700; color: {Design.NOTION_BLACK};")
        layout.addWidget(title)
        
        # Search
        search = QLineEdit()
        search.setPlaceholderText("🔍 Tìm kiếm khách hàng theo mã, tên, SĐT...")
        search.setStyleSheet(self.input_style())
        layout.addWidget(search)
        
        # Customer list
        customer_list = QListWidget()
        customer_list.setStyleSheet(f"""
            QListWidget {{
                border: 1px solid rgba(0,0,0,0.1);
                border-radius: {Design.RADIUS_SMALL}px;
                padding: 8px;
            }}
            QListWidget::item {{
                padding: 12px;
                border-bottom: 1px solid rgba(0,0,0,0.05);
            }}
            QListWidget::item:hover {{
                background-color: {Design.BADGE_BLUE_BG};
            }}
            QListWidget::item:selected {{
                background-color: {Design.NOTION_BLUE};
                color: white;
            }}
        """)
        
        customers = [
            "KH-DN-00001 - Công ty TNHH Thương mại Hoàng Phát",
            "KH-CN-00002 - Nguyễn Văn An",
            "KH-DN-00003 - Công ty CP Logistics Việt Nam",
            "KH-CN-00004 - Trần Thị Bình",
            "KH-DN-00005 - Công ty TNHH Xuất nhập khẩu Minh Tâm",
        ]
        
        for customer in customers:
            item = QListWidgetItem(customer)
            customer_list.addItem(item)
        
        layout.addWidget(customer_list)
        
        # Quick add customer
        quick_add = StyledButton("+ Thêm khách hàng mới", "secondary")
        quick_add.clicked.connect(self.open_add_customer)
        layout.addWidget(quick_add)
        
        return widget
        
    def create_step2(self):
        """Step 2: Select warehouse position"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(16)
        
        title = QLabel("🏭 Bước 2: Chọn kho và vị trí lưu trữ")
        title.setStyleSheet(f"font-size: 20px; font-weight: 700; color: {Design.NOTION_BLACK};")
        layout.addWidget(title)
        
        # Warehouse selection
        form = QFormLayout()
        form.setSpacing(12)
        
        kho_combo = QComboBox()
        kho_combo.addItems([
            "KHO-HM-01 - Kho Hóc Môn (Còn trống: 5 vị trí)",
            "KHO-CC-01 - Kho Củ Chi (Còn trống: 8 vị trí)",
            "KHO-BC-01 - Kho Bình Chánh (Đang bảo trì)",
            "KHO-TD-01 - Kho Thủ Đức (Còn trống: 15 vị trí)",
        ])
        kho_combo.setStyleSheet(self.input_style())
        form.addRow(self.label_style("Chọn kho:"), kho_combo)
        
        vitri_combo = QComboBox()
        vitri_combo.addItems([
            "A-01 - 50 m² - Giá: ₫5,000,000/tháng",
            "A-02 - 50 m² - Giá: ₫5,000,000/tháng",
            "A-03 - 75 m² - Giá: ₫7,500,000/tháng",
            "B-01 - 100 m² - Giá: ₫10,000,000/tháng",
            "B-02 - 100 m² - Giá: ₫10,000,000/tháng",
        ])
        vitri_combo.setStyleSheet(self.input_style())
        form.addRow(self.label_style("Chọn vị trí:"), vitri_combo)
        
        layout.addLayout(form)
        
        # Position details
        details_card = StyledCard()
        details_layout = QFormLayout(details_card)
        details_layout.setSpacing(8)
        
        details_layout.addRow(self.label_style("Diện tích:"), QLabel("50 m²"))
        details_layout.addRow(self.label_style("Giá thuê tháng:"), QLabel("₫5,000,000"))
        details_layout.addRow(self.label_style("Tình trạng:"), Badge("Trống", "active"))
        
        layout.addWidget(details_card)
        
        # Quick view warehouse
        quick_view = StyledButton("👁️ Xem chi tiết kho", "secondary")
        quick_view.clicked.connect(self.open_warehouse_detail)
        layout.addWidget(quick_view)
        
        layout.addStretch()
        return widget
        
    def create_step3(self):
        """Step 3: Contract details"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(16)
        
        title = QLabel("✓ Bước 3: Thông tin hợp đồng")
        title.setStyleSheet(f"font-size: 20px; font-weight: 700; color: {Design.NOTION_BLACK};")
        layout.addWidget(title)
        
        # Auto-generated contract code
        form = QFormLayout()
        form.setSpacing(12)
        
        ma_hd = QLineEdit("HD-2026-0042")
        ma_hd.setReadOnly(True)
        ma_hd.setStyleSheet(self.input_style(True))
        form.addRow(self.label_style("Mã hợp đồng:"), ma_hd)
        
        # Dates
        ngay_bat_dau = QDateEdit()
        ngay_bat_dau.setCalendarPopup(True)
        ngay_bat_dau.setDate(QDate.currentDate())
        ngay_bat_dau.setStyleSheet(self.input_style())
        form.addRow(self.label_style("Ngày bắt đầu:"), ngay_bat_dau)
        
        ngay_ket_thuc = QDateEdit()
        ngay_ket_thuc.setCalendarPopup(True)
        ngay_ket_thuc.setDate(QDate.currentDate().addMonths(12))
        ngay_ket_thuc.setStyleSheet(self.input_style())
        form.addRow(self.label_style("Ngày kết thúc:"), ngay_ket_thuc)
        
        # Deposit
        coc = QDoubleSpinBox()
        coc.setRange(0, 1000000000)
        coc.setValue(15000000)
        coc.setSuffix(" VNĐ")
        coc.setStyleSheet(self.input_style())
        form.addRow(self.label_style("Tiền đặt cọc:"), coc)
        
        # Monthly fee (auto)
        phi_thang = QLineEdit("₫5,000,000")
        phi_thang.setReadOnly(True)
        phi_thang.setStyleSheet(self.input_style(True))
        form.addRow(self.label_style("Phí thuê tháng:"), phi_thang)
        
        # Total
        tong = QLineEdit("₫75,000,000 (12 tháng + cọc)")
        tong.setReadOnly(True)
        tong.setStyleSheet(self.input_style(True))
        form.addRow(self.label_style("Tổng giá trị:"), tong)
        
        # Notes
        ghichu = QTextEdit()
        ghichu.setPlaceholderText("Điều khoản bổ sung...")
        ghichu.setMaximumHeight(80)
        ghichu.setStyleSheet(self.input_style())
        form.addRow(self.label_style("Ghi chú:"), ghichu)
        
        layout.addLayout(form)
        
        # Summary card
        summary = StyledCard()
        summary.setStyleSheet(f"""
            QFrame {{
                background-color: {Design.BADGE_BLUE_BG};
                border: 1px solid rgba(0,0,0,0.1);
                border-radius: {Design.RADIUS_LARGE}px;
            }}
        """)
        summary_layout = QVBoxLayout(summary)
        
        summary_title = QLabel("📋 Tóm tắt hợp đồng")
        summary_title.setStyleSheet(f"font-size: 16px; font-weight: 700; color: {Design.BADGE_BLUE_TEXT};")
        summary_layout.addWidget(summary_title)
        
        summary_text = QLabel("""
            • Khách hàng: Công ty TNHH Thương mại Hoàng Phát (KH-DN-00001)
            • Kho: KHO-HM-01 - Kho Hóc Môn
            • Vị trí: A-01 (50 m²)
            • Thời hạn: 12 tháng (17/04/2026 - 17/04/2027)
            • Tổng giá trị: ₫75,000,000
        """)
        summary_text.setStyleSheet(f"color: {Design.NOTION_BLACK}; line-height: 1.6;")
        summary_layout.addWidget(summary_text)
        
        layout.addWidget(summary)
        layout.addStretch()
        
        return widget
        
    def next_step(self):
        current = self.wizard.currentIndex()
        if current < 2:
            self.wizard.setCurrentIndex(current + 1)
            self.btn_prev.setVisible(True)
            
        if self.wizard.currentIndex() == 2:
            self.btn_next.setVisible(False)
            self.btn_save.setVisible(True)
            
    def prev_step(self):
        current = self.wizard.currentIndex()
        if current > 0:
            self.wizard.setCurrentIndex(current - 1)
            
        if self.wizard.currentIndex() == 0:
            self.btn_prev.setVisible(False)
            
        self.btn_next.setVisible(True)
        self.btn_save.setVisible(False)
        
    def open_add_customer(self):
        QMessageBox.information(self, "Thêm khách hàng", "Mở dialog thêm khách hàng mới")
        
    def open_warehouse_detail(self):
        QMessageBox.information(self, "Chi tiết kho", "Mở dialog xem chi tiết kho hàng")
        
    def label_style(self, text):
        label = QLabel(text)
        label.setStyleSheet(f"font-weight: 600; color: {Design.NOTION_BLACK};")
        return label
        
    def input_style(self, readonly=False):
        if readonly:
            return f"""
                QLineEdit, QTextEdit, QComboBox, QDateEdit, QDoubleSpinBox {{
                    padding: 10px 14px;
                    border: 1px solid rgba(0,0,0,0.1);
                    border-radius: {Design.RADIUS_SMALL}px;
                    background-color: {Design.WARM_WHITE};
                    color: {Design.WARM_GRAY_500};
                }}
            """
        return f"""
            QLineEdit, QTextEdit, QComboBox, QDateEdit, QDoubleSpinBox {{
                padding: 10px 14px;
                border: 1px solid rgba(0,0,0,0.1);
                border-radius: {Design.RADIUS_SMALL}px;
                background-color: {Design.PURE_WHITE};
            }}
            QLineEdit:focus, QTextEdit:focus, QComboBox:focus {{
                border: 2px solid {Design.NOTION_BLUE};
            }}
        """


class GiaHanDialog(QDialog):
    """Dialog for extending contract"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Gia hạn hợp đồng")
        self.setMinimumSize(500, 400)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(32, 32, 32, 32)
        
        header = QLabel("🔄 Gia hạn hợp đồng")
        header.setStyleSheet(f"font-size: 24px; font-weight: 700; color: {Design.NOTION_BLACK};")
        layout.addWidget(header)
        
        card = StyledCard()
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(24, 24, 24, 24)
        
        # Current info
        info = QLabel("""
            <b>Hợp đồng:</b> HD-2024-001<br>
            <b>Khách hàng:</b> Công ty TNHH Thương mại Hoàng Phát<br>
            <b>Vị trí:</b> KHO-HM-01 / A-01<br>
            <b>Hết hạn:</b> 15/03/2025
        """)
        info.setStyleSheet(f"color: {Design.NOTION_BLACK}; line-height: 1.6;")
        card_layout.addWidget(info)
        
        # Form
        form = QFormLayout()
        form.setSpacing(12)
        
        thoi_han = QComboBox()
        thoi_han.addItems(["3 tháng", "6 tháng", "12 tháng", "24 tháng"])
        thoi_han.setCurrentIndex(2)
        form.addRow(self.label_style("Thời hạn gia hạn:"), thoi_han)
        
        ngay_ket_thuc_moi = QLineEdit("15/03/2026")
        ngay_ket_thuc_moi.setReadOnly(True)
        ngay_ket_thuc_moi.setStyleSheet(f"""
            QLineEdit {{
                padding: 10px 14px;
                border: 1px solid rgba(0,0,0,0.1);
                border-radius: {Design.RADIUS_SMALL}px;
                background-color: {Design.WARM_WHITE};
            }}
        """)
        form.addRow(self.label_style("Ngày kết thúc mới:"), ngay_ket_thuc_moi)
        
        gia_moi = QDoubleSpinBox()
        gia_moi.setRange(0, 1000000000)
        gia_moi.setValue(5500000)
        gia_moi.setSuffix(" VNĐ/tháng")
        form.addRow(self.label_style("Giá thuê mới:"), gia_moi)
        
        card_layout.addLayout(form)
        
        # Warning
        warning = QLabel("⚠️ Giá thuê mới cao hơn 10% so với hợp đồng cũ")
        warning.setStyleSheet(f"color: {Design.ORANGE}; font-size: 13px;")
        card_layout.addWidget(warning)
        
        layout.addWidget(card)
        
        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        btn_huy = StyledButton("Hủy", "secondary")
        btn_huy.clicked.connect(self.reject)
        btn_layout.addWidget(btn_huy)
        
        btn_luu = StyledButton("✓ Tạo phụ lục gia hạn", "success")
        btn_luu.clicked.connect(self.accept)
        btn_layout.addWidget(btn_luu)
        
        layout.addLayout(btn_layout)
        
    def label_style(self, text):
        label = QLabel(text)
        label.setStyleSheet(f"font-weight: 600; color: {Design.NOTION_BLACK};")
        return label


class MainWindow(QMainWindow):
    """Main window for Hop Dong management"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🏭 KhoSmart Pro - Quản lý hợp đồng thuê")
        self.setMinimumSize(1200, 800)
        self.setup_ui()
        
    def setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        
        main_layout = QVBoxLayout(central)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Navigation bar with module linking
        nav = NavigationBar("hopdong")
        main_layout.addWidget(nav)
        
        # Content
        content = QWidget()
        content.setStyleSheet(f"background-color: {Design.WARM_WHITE};")
        content_layout = QVBoxLayout(content)
        content_layout.setSpacing(24)
        content_layout.setContentsMargins(32, 32, 32, 32)
        
        # Header
        header = QLabel("Quản lý hợp đồng thuê")
        header.setStyleSheet(f"font-size: 40px; font-weight: 700; color: {Design.NOTION_BLACK};")
        content_layout.addWidget(header)
        
        subtitle = QLabel("Quản lý toàn bộ vòng đời hợp đồng từ tạo mới đến kết thúc")
        subtitle.setStyleSheet(f"color: {Design.WARM_GRAY_500}; font-size: 18px;")
        content_layout.addWidget(subtitle)
        
        # Stats
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(16)
        
        stats = [
            ("Tổng hợp đồng", "156", None, True),
            ("Đang hoạt động", "142", "91%", True),
            ("Sắp hết hạn (30 ngày)", "8", "Cần gia hạn", False),
            ("Đã kết thúc", "6", None, True),
        ]
        
        for label, value, change, positive in stats:
            card = StatCard(label, value, change, positive)
            stats_layout.addWidget(card)
        
        content_layout.addLayout(stats_layout)
        
        # Action bar
        action_layout = QHBoxLayout()
        action_layout.setSpacing(12)
        
        self.search = QLineEdit()
        self.search.setPlaceholderText("🔍 Tìm kiếm theo mã HĐ, khách hàng...")
        self.search.setStyleSheet(f"""
            QLineEdit {{
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
        
        btn_giahan = StyledButton("🔄 Gia hạn", "secondary")
        btn_giahan.clicked.connect(self.open_gia_han)
        action_layout.addWidget(btn_giahan)
        
        btn_them = StyledButton("+ Tạo hợp đồng mới", "primary")
        btn_them.clicked.connect(self.open_tao_moi)
        action_layout.addWidget(btn_them)
        
        content_layout.addLayout(action_layout)
        
        # Table card
        table_card = StyledCard()
        table_layout = QVBoxLayout(table_card)
        table_layout.setContentsMargins(0, 0, 0, 0)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            "Mã HĐ", "Khách hàng", "Kho/Vị trí", "Ngày bắt đầu", "Ngày kết thúc", 
            "Giá thuê", "Trạng thái", "Thao tác"
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
        """)
        
        self.table.setShowGrid(False)
        self.table.verticalHeader().setVisible(False)
        
        widths = [100, 220, 150, 100, 100, 120, 110, 120]
        for i, w in enumerate(widths):
            self.table.setColumnWidth(i, w)
        
        self.load_sample_data()
        table_layout.addWidget(self.table)
        content_layout.addWidget(table_card)
        
        main_layout.addWidget(content)
        
    def load_sample_data(self):
        sample_data = [
            {
                "ma": "HD-2024-001",
                "khachhang": "Công ty TNHH Thương mại Hoàng Phát",
                "vitri": "KHO-HM-01 / A-01",
                "ngay_bd": "15/03/2024",
                "ngay_kt": "15/03/2025",
                "gia": "₫5,000,000",
                "trang_thai": "active"
            },
            {
                "ma": "HD-2024-015",
                "khachhang": "Nguyễn Văn An",
                "vitri": "KHO-CC-01 / B-02",
                "ngay_bd": "20/06/2024",
                "ngay_kt": "20/06/2025",
                "gia": "₫8,000,000",
                "trang_thai": "active"
            },
            {
                "ma": "HD-2024-042",
                "khachhang": "Công ty CP Logistics Việt Nam",
                "vitri": "KHO-TD-01 / A-03",
                "ngay_bd": "10/09/2024",
                "ngay_kt": "10/09/2025",
                "gia": "₫12,000,000",
                "trang_thai": "warning"
            },
            {
                "ma": "HD-2023-008",
                "khachhang": "Công ty TNHH Xuất nhập khẩu Minh Tâm",
                "vitri": "KHO-HM-01 / B-01",
                "ngay_bd": "15/03/2023",
                "ngay_kt": "15/03/2024",
                "gia": "₫6,000,000",
                "trang_thai": "expired"
            },
        ]
        
        self.table.setRowCount(len(sample_data))
        
        for i, data in enumerate(sample_data):
            self.table.setItem(i, 0, QTableWidgetItem(data["ma"]))
            
            # Customer name
            kh_widget = QWidget()
            kh_layout = QVBoxLayout(kh_widget)
            kh_layout.setSpacing(2)
            kh_layout.setContentsMargins(0, 0, 0, 0)
            
            kh_name = QLabel(data["khachhang"])
            kh_name.setStyleSheet(f"font-weight: 600; color: {Design.NOTION_BLACK};")
            kh_layout.addWidget(kh_name)
            
            # Make customer clickable
            kh_btn = QPushButton("👤 Xem KH")
            kh_btn.setStyleSheet(f"""
                QPushButton {{
                    color: {Design.NOTION_BLUE};
                    border: none;
                    background: transparent;
                    text-align: left;
                    font-size: 12px;
                }}
                QPushButton:hover {{ text-decoration: underline; }}
            """)
            kh_btn.setCursor(Qt.CursorShape.PointingHandCursor)
            kh_btn.clicked.connect(self.open_customer_detail)
            kh_layout.addWidget(kh_btn)
            
            self.table.setCellWidget(i, 1, kh_widget)
            
            # Warehouse position - clickable
            vitri_widget = QWidget()
            vitri_layout = QVBoxLayout(vitri_widget)
            vitri_layout.setSpacing(2)
            vitri_layout.setContentsMargins(0, 0, 0, 0)
            
            vitri_label = QLabel(data["vitri"])
            vitri_layout.addWidget(vitri_label)
            
            vitri_btn = QPushButton("🏭 Xem kho")
            vitri_btn.setStyleSheet(f"""
                QPushButton {{
                    color: {Design.NOTION_BLUE};
                    border: none;
                    background: transparent;
                    text-align: left;
                    font-size: 12px;
                }}
                QPushButton:hover {{ text-decoration: underline; }}
            """)
            vitri_btn.setCursor(Qt.CursorShape.PointingHandCursor)
            vitri_btn.clicked.connect(self.open_warehouse_detail)
            vitri_layout.addWidget(vitri_btn)
            
            self.table.setCellWidget(i, 2, vitri_widget)
            
            self.table.setItem(i, 3, QTableWidgetItem(data["ngay_bd"]))
            self.table.setItem(i, 4, QTableWidgetItem(data["ngay_kt"]))
            self.table.setItem(i, 5, QTableWidgetItem(data["gia"]))
            
            # Status
            status_map = {
                "active": ("Đang hoạt động", "active"),
                "warning": ("Sắp hết hạn", "warning"),
                "expired": ("Đã kết thúc", "expired"),
            }
            status_text, status_type = status_map.get(data["trang_thai"])
            self.table.setCellWidget(i, 6, Badge(status_text, status_type))
            
            # Actions
            action_widget = QWidget()
            action_layout = QHBoxLayout(action_widget)
            action_layout.setSpacing(8)
            action_layout.setContentsMargins(0, 0, 0, 0)
            
            for icon in ["👁️", "✏️", "🔄"]:
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
                action_layout.addWidget(btn)
            
            self.table.setCellWidget(i, 7, action_widget)
            
    def open_tao_moi(self):
        dialog = TaoHopDongDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            QMessageBox.information(self, "Thành công", "Đã tạo hợp đồng mới!")
            
    def open_gia_han(self):
        dialog = GiaHanDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            QMessageBox.information(self, "Thành công", "Đã tạo phụ lục gia hạn!")
            
    def open_customer_detail(self):
        """Link to customer module"""
        try:
            from khachhang_demo import MainWindow as KhachHangWindow
            self.customer_window = KhachHangWindow()
            self.customer_window.show()
        except ImportError:
            QMessageBox.information(self, "Liên kết", "Mở chi tiết khách hàng...")
            
    def open_warehouse_detail(self):
        """Link to warehouse module"""
        try:
            from khohang_demo import MainWindow as KhoHangWindow
            self.warehouse_window = KhoHangWindow()
            self.warehouse_window.show()
        except ImportError:
            QMessageBox.information(self, "Liên kết", "Mở chi tiết kho hàng...")


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
