#!/usr/bin/env python3
"""
Báo cáo View - Giao diện Quản lý Báo cáo
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QComboBox, QTextEdit, QDateEdit, QScrollArea,
    QGridLayout, QProgressBar, QGroupBox, QStackedWidget
)
from PyQt6.QtCore import Qt, pyqtSignal, QDate
from PyQt6.QtGui import QFont
from typing import Optional, Dict, Any

from src.gui.widgets import DataTableWithToolbar
from src.gui.dialogs import MessageDialog
from src.utils.formatters import format_currency, format_date


class BaoCaoView(QWidget):
    """
    Giao diện Quản lý Báo cáo - Xem và xuất các loại báo cáo
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_report = None
        self.setup_ui()
        self.load_dashboard_summary()
    
    def setup_ui(self):
        """Setup UI"""
        self.setStyleSheet("""
            QWidget {
                background-color: #faf9f8;
                font-family: 'Inter', sans-serif;
            }
            QFrame {
                background-color: transparent;
            }
            QPushButton {
                border-radius: 6px;
                padding: 10px 20px;
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
            QPushButton#successButton {
                background-color: #2e7d32;
                color: white;
                border: none;
            }
            QPushButton#successButton:hover {
                background-color: #1b5e20;
            }
            QComboBox {
                padding: 8px 12px;
                border: 1px solid #e0e0e0;
                border-radius: 6px;
                background-color: #ffffff;
                font-size: 13px;
            }
            QTextEdit {
                background-color: #ffffff;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                padding: 16px;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 12px;
                line-height: 1.5;
            }
            QLabel#titleLabel {
                font-size: 24px;
                font-weight: 700;
                color: #31302e;
            }
            QLabel#subtitleLabel {
                font-size: 14px;
                color: #615d59;
            }
            QLabel#statValue {
                font-size: 28px;
                font-weight: 700;
                color: #005db2;
            }
            QLabel#statLabel {
                font-size: 12px;
                color: #757575;
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
            QProgressBar {
                border: none;
                border-radius: 4px;
                background-color: #e0e0e0;
                height: 8px;
            }
            QProgressBar::chunk {
                border-radius: 4px;
                background-color: #005db2;
            }
        """)
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 30, 40, 30)
        main_layout.setSpacing(20)
        
        # Title section
        title_layout = QHBoxLayout()
        title = QLabel("📊 BÁO CÁO & THỐNG KÊ")
        title.setObjectName("titleLabel")
        title_layout.addWidget(title)
        title_layout.addStretch()
        
        refresh_btn = QPushButton("🔄 Tải lại")
        refresh_btn.setFixedWidth(100)
        refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #ffffff;
                color: #005db2;
                border: 1px solid #005db2;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #e3f2fd;
            }
        """)
        refresh_btn.clicked.connect(self.load_dashboard_summary)
        title_layout.addWidget(refresh_btn)
        
        main_layout.addLayout(title_layout)
        
        # Report type selector
        selector_bar = self._create_selector_bar()
        main_layout.addWidget(selector_bar)
        
        # Content area with stacked widget
        self.content_stack = QStackedWidget()
        
        # Page 1: Dashboard summary
        self.dashboard_page = self._create_dashboard_page()
        self.content_stack.addWidget(self.dashboard_page)
        
        # Page 2: Report preview
        self.report_page = self._create_report_page()
        self.content_stack.addWidget(self.report_page)
        
        main_layout.addWidget(self.content_stack, 1)
    
    def _create_selector_bar(self) -> QFrame:
        """Create report type selector bar"""
        selector_bar = QFrame()
        selector_bar.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border: 1px solid rgba(0, 0, 0, 0.1);
                border-radius: 8px;
                padding: 16px;
            }
        """)
        
        layout = QHBoxLayout(selector_bar)
        layout.setSpacing(16)
        
        # Report type selector
        layout.addWidget(QLabel("Loại báo cáo:"))
        self.report_type_combo = QComboBox()
        self.report_type_combo.addItem("📈 Tổng quan Dashboard", "dashboard")
        self.report_type_combo.addItem("📋 Báo cáo Tổng hợp", "summary")
        self.report_type_combo.addItem("💰 Báo cáo Doanh thu", "revenue")
        self.report_type_combo.addItem("📦 Báo cáo Kho", "warehouse")
        self.report_type_combo.addItem("📄 Báo cáo Hợp đồng", "contract")
        self.report_type_combo.addItem("⚠️ Cảnh báo", "alerts")
        self.report_type_combo.setFixedWidth(250)
        self.report_type_combo.currentIndexChanged.connect(self._on_report_type_changed)
        layout.addWidget(self.report_type_combo)
        
        layout.addStretch()
        
        # Action buttons
        export_txt_btn = QPushButton("📝 Xuất TXT")
        export_txt_btn.setObjectName("primaryButton")
        export_txt_btn.clicked.connect(self._on_export_txt)
        layout.addWidget(export_txt_btn)
        
        export_excel_btn = QPushButton("📊 Xuất Excel")
        export_excel_btn.setObjectName("primaryButton")
        export_excel_btn.clicked.connect(self._on_export_excel)
        layout.addWidget(export_excel_btn)
        
        print_btn = QPushButton("🖨️ In báo cáo")
        print_btn.setObjectName("primaryButton")
        print_btn.clicked.connect(self._on_print)
        layout.addWidget(print_btn)
        
        return selector_bar
    
    def _create_dashboard_page(self) -> QWidget:
        """Create dashboard summary page"""
        page = QScrollArea()
        page.setWidgetResizable(True)
        page.setStyleSheet("border: none;")
        
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setSpacing(20)
        
        # Stats cards row 1
        stats_row1 = QHBoxLayout()
        stats_row1.addWidget(self._create_stat_card("khach_hang", "👥", "Khách hàng", "total"))
        stats_row1.addWidget(self._create_stat_card("kho", "🏭", "Kho hàng", "total"))
        stats_row1.addWidget(self._create_stat_card("hop_dong", "📄", "Hợp đồng", "total"))
        stats_row1.addWidget(self._create_stat_card("hang_hoa", "📦", "Mặt hàng", "total"))
        layout.addLayout(stats_row1)
        
        # Stats cards row 2
        stats_row2 = QHBoxLayout()
        stats_row2.addWidget(self._create_revenue_card())
        stats_row2.addWidget(self._create_fill_rate_card())
        stats_row2.addWidget(self._create_alert_card())
        layout.addLayout(stats_row2)
        
        # Highlights and recommendations
        highlights_group = QGroupBox("📌 Điểm nổi bật")
        highlights_layout = QVBoxLayout()
        self.highlights_text = QTextEdit()
        self.highlights_text.setReadOnly(True)
        self.highlights_text.setMaximumHeight(150)
        highlights_layout.addWidget(self.highlights_text)
        highlights_group.setLayout(highlights_layout)
        layout.addWidget(highlights_group)
        
        recommendations_group = QGroupBox("💡 Khuyến nghị")
        recommendations_layout = QVBoxLayout()
        self.recommendations_text = QTextEdit()
        self.recommendations_text.setReadOnly(True)
        self.recommendations_text.setMaximumHeight(150)
        recommendations_layout.addWidget(self.recommendations_text)
        recommendations_group.setLayout(recommendations_layout)
        layout.addWidget(recommendations_group)
        
        layout.addStretch()
        
        page.setWidget(container)
        return page
    
    def _create_stat_card(self, category: str, icon: str, title: str, key: str) -> QFrame:
        """Create a statistics card"""
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border: 1px solid rgba(0, 0, 0, 0.1);
                border-radius: 8px;
                padding: 20px;
            }
        """)
        
        layout = QVBoxLayout(card)
        layout.setSpacing(8)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        icon_label = QLabel(icon)
        icon_label.setStyleSheet("font-size: 32px;")
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(icon_label)
        
        self.stats_labels[f"{category}_{key}"] = QLabel("0")
        self.stats_labels[f"{category}_{key}"].setObjectName("statValue")
        self.stats_labels[f"{category}_{key}"].setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.stats_labels[f"{category}_{key}"])
        
        title_label = QLabel(title)
        title_label.setObjectName("statLabel")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)
        
        return card
    
    def _create_revenue_card(self) -> QFrame:
        """Create revenue statistics card"""
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border: 1px solid rgba(0, 0, 0, 0.1);
                border-radius: 8px;
                padding: 20px;
            }
        """)
        
        layout = QVBoxLayout(card)
        layout.setSpacing(8)
        
        title = QLabel("💰 Doanh thu tháng")
        title.setStyleSheet("font-weight: 600; color: #2e7d32;")
        layout.addWidget(title)
        
        self.revenue_monthly_label = QLabel("0 đ")
        self.revenue_monthly_label.setStyleSheet("font-size: 24px; font-weight: 700; color: #2e7d32;")
        layout.addWidget(self.revenue_monthly_label)
        
        yearly_title = QLabel("Doanh thu năm (dự kiến):")
        yearly_title.setStyleSheet("font-size: 11px; color: #757575;")
        layout.addWidget(yearly_title)
        
        self.revenue_yearly_label = QLabel("0 đ")
        self.revenue_yearly_label.setStyleSheet("font-size: 16px; font-weight: 600; color: #2e7d32;")
        layout.addWidget(self.revenue_yearly_label)
        
        return card
    
    def _create_fill_rate_card(self) -> QFrame:
        """Create warehouse fill rate card"""
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border: 1px solid rgba(0, 0, 0, 0.1);
                border-radius: 8px;
                padding: 20px;
            }
        """)
        
        layout = QVBoxLayout(card)
        layout.setSpacing(8)
        
        title = QLabel("🏭 Tỷ lệ lấp đầy TB")
        title.setStyleSheet("font-weight: 600; color: #005db2;")
        layout.addWidget(title)
        
        self.fill_rate_label = QLabel("0%")
        self.fill_rate_label.setStyleSheet("font-size: 24px; font-weight: 700; color: #005db2;")
        layout.addWidget(self.fill_rate_label)
        
        self.fill_rate_progress = QProgressBar()
        self.fill_rate_progress.setRange(0, 100)
        self.fill_rate_progress.setValue(0)
        layout.addWidget(self.fill_rate_progress)
        
        return card
    
    def _create_alert_card(self) -> QFrame:
        """Create alerts card"""
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border: 1px solid rgba(0, 0, 0, 0.1);
                border-radius: 8px;
                padding: 20px;
            }
        """)
        
        layout = QVBoxLayout(card)
        layout.setSpacing(8)
        
        title = QLabel("⚠️ Cảnh báo")
        title.setStyleSheet("font-weight: 600; color: #d32f2f;")
        layout.addWidget(title)
        
        self.alert_low_stock_label = QLabel("Hàng sắp hết: 0")
        self.alert_low_stock_label.setStyleSheet("font-size: 13px;")
        layout.addWidget(self.alert_low_stock_label)
        
        self.alert_contract_label = QLabel("Hợp đồng sắp hết: 0")
        self.alert_contract_label.setStyleSheet("font-size: 13px;")
        layout.addWidget(self.alert_contract_label)
        
        self.alert_critical_label = QLabel("Nghiêm trọng: 0")
        self.alert_critical_label.setStyleSheet("font-size: 13px; color: #d32f2f;")
        layout.addWidget(self.alert_critical_label)
        
        return card
    
    def _create_report_page(self) -> QWidget:
        """Create report preview page"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setSpacing(16)
        
        # Report header
        header_frame = QFrame()
        header_frame.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border: 1px solid rgba(0, 0, 0, 0.1);
                border-radius: 8px;
                padding: 16px;
            }
        """)
        header_layout = QHBoxLayout(header_frame)
        
        self.report_title = QLabel("BÁO CÁO TỔNG HỢP")
        self.report_title.setStyleSheet("font-size: 18px; font-weight: 700; color: #31302e;")
        header_layout.addWidget(self.report_title)
        
        header_layout.addStretch()
        
        self.report_date = QLabel(f"Ngày sinh: {QDate.currentDate().toString('dd/MM/yyyy')}")
        self.report_date.setStyleSheet("color: #757575;")
        header_layout.addWidget(self.report_date)
        
        layout.addWidget(header_frame)
        
        # Report content
        self.report_content = QTextEdit()
        self.report_content.setReadOnly(True)
        layout.addWidget(self.report_content, 1)
        
        return page
    
    def _init_stats_labels(self):
        """Initialize stats labels dictionary"""
        self.stats_labels = {}
    
    def load_dashboard_summary(self):
        """Load dashboard summary data"""
        self._init_stats_labels()
        
        try:
            from src.services.report_service import ReportService
            
            service = ReportService()
            summary = service.get_dashboard_summary()
            
            # Update customer stats
            khach = summary.get('khach_hang', {})
            self.stats_labels['khach_hang_total'].setText(str(khach.get('total', 0)))
            
            # Update warehouse stats
            kho = summary.get('kho', {})
            self.stats_labels['kho_total'].setText(str(kho.get('total', 0)))
            fill_rate = kho.get('avg_fill_rate', 0)
            self.fill_rate_label.setText(f"{fill_rate:.1f}%")
            self.fill_rate_progress.setValue(int(fill_rate))
            
            # Update contract stats
            hop_dong = summary.get('hop_dong', {})
            self.stats_labels['hop_dong_total'].setText(str(hop_dong.get('total', 0)))
            expiring = hop_dong.get('expiring_soon', 0)
            self.alert_contract_label.setText(f"Hợp đồng sắp hết: {expiring}")
            
            # Update goods stats
            hang_hoa = summary.get('hang_hoa', {})
            self.stats_labels['hang_hoa_total'].setText(str(hang_hoa.get('total_items', 0)))
            
            # Update revenue stats
            revenue = summary.get('revenue', {})
            monthly = revenue.get('monthly_revenue', 0)
            yearly = revenue.get('yearly_revenue', 0)
            self.revenue_monthly_label.setText(format_currency(monthly))
            self.revenue_yearly_label.setText(format_currency(yearly))
            
            # Update alert stats
            alerts = summary.get('alerts', {})
            low_stock = alerts.get('low_stock_count', 0)
            critical = alerts.get('critical_alerts', 0)
            self.alert_low_stock_label.setText(f"Hàng sắp hết: {low_stock}")
            self.alert_critical_label.setText(f"Nghiêm trọng: {critical}")
            
            # Update highlights and recommendations
            report = service.generate_summary_report()
            highlights = report.get('highlights', [])
            recommendations = report.get('recommendations', [])
            
            self.highlights_text.clear()
            for h in highlights:
                self.highlights_text.append(f"• {h}")
            
            self.recommendations_text.clear()
            for r in recommendations:
                self.recommendations_text.append(f"• {r}")
            
            # Switch to dashboard view
            self.content_stack.setCurrentIndex(0)
            
        except Exception as e:
            MessageDialog.error(self, "Lỗi", f"Không thể tải dữ liệu:\n{str(e)}")
    
    def _on_report_type_changed(self, index: int):
        """Handle report type selection change"""
        report_type = self.report_type_combo.currentData()
        
        if report_type == "dashboard":
            self.load_dashboard_summary()
        else:
            self._generate_report(report_type)
    
    def _generate_report(self, report_type: str):
        """Generate specific report"""
        try:
            from src.services.report_service import ReportService
            from datetime import datetime
            
            service = ReportService()
            
            # Generate report content based on type
            if report_type == "summary":
                report = service.generate_summary_report()
                content = self._format_summary_report(report)
            elif report_type == "revenue":
                content = self._generate_revenue_report()
            elif report_type == "warehouse":
                content = self._generate_warehouse_report()
            elif report_type == "contract":
                content = self._generate_contract_report()
            elif report_type == "alerts":
                content = self._generate_alerts_report()
            else:
                content = "Loại báo cáo không hợp lệ."
            
            # Update report page
            self.report_title.setText(f"BÁO CÁO {report_type.upper()}")
            self.report_date.setText(f"Ngày sinh: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
            self.report_content.setPlainText(content)
            
            # Switch to report view
            self.content_stack.setCurrentIndex(1)
            
        except Exception as e:
            MessageDialog.error(self, "Lỗi", f"Không thể tạo báo cáo:\n{str(e)}")
    
    def _format_summary_report(self, report: dict) -> str:
        """Format summary report for display"""
        lines = []
        lines.append("=" * 80)
        lines.append("                    BÁO CÁO TỔNG HỢP")
        lines.append("=" * 80)
        lines.append("")
        
        summary = report.get('summary', {})
        
        # Customer section
        kh = summary.get('customers', {})
        lines.append("I. KHÁCH HÀNG")
        lines.append("-" * 40)
        lines.append(f"  Tổng số: {kh.get('total', 0)}")
        lines.append(f"  Đang hoạt động: {kh.get('active', 0)}")
        lines.append(f"  Không hoạt động: {kh.get('inactive', 0)}")
        lines.append("")
        
        # Warehouse section
        kho = summary.get('warehouses', {})
        lines.append("II. KHO HÀNG")
        lines.append("-" * 40)
        lines.append(f"  Tổng số kho: {kho.get('total', 0)}")
        lines.append(f"  Tổng diện tích: {kho.get('total_dien_tich', 0):,.0f} m²")
        lines.append(f"  Tổng sức chứa: {kho.get('total_suc_chua', 0):,.0f} m³")
        lines.append(f"  Tỷ lệ lấp đầy TB: {kho.get('avg_fill_rate', 0):.1f}%")
        lines.append("")
        
        # Contract section
        hd = summary.get('contracts', {})
        lines.append("III. HỢP ĐỒNG")
        lines.append("-" * 40)
        lines.append(f"  Tổng số: {hd.get('total', 0)}")
        lines.append(f"  Sắp hết hạn (30 ngày): {hd.get('expiring_soon', 0)}")
        lines.append(f"  Tổng doanh thu: {hd.get('total_revenue', 0):,.0f}₫")
        lines.append("")
        
        # Goods section
        hh = summary.get('goods', {})
        lines.append("IV. HÀNG HÓA")
        lines.append("-" * 40)
        lines.append(f"  Tổng mặt hàng: {hh.get('total_items', 0)}")
        lines.append(f"  Đang trong kho: {hh.get('in_stock', 0)}")
        lines.append("")
        
        # Revenue section
        rev = summary.get('revenue', {})
        lines.append("V. DOANH THU")
        lines.append("-" * 40)
        lines.append(f"  Doanh thu tháng: {rev.get('monthly_revenue', 0):,.0f}₫")
        lines.append(f"  Doanh thu năm (dự kiến): {rev.get('yearly_revenue', 0):,.0f}₫")
        lines.append("")
        
        # Alerts section
        al = summary.get('alerts', {})
        lines.append("VI. CẢNH BÁO")
        lines.append("-" * 40)
        lines.append(f"  Hàng sắp hết: {al.get('low_stock_count', 0)}")
        lines.append(f"  Nghiêm trọng: {al.get('critical_alerts', 0)}")
        lines.append(f"  Hợp đồng sắp hết hạn: {al.get('expiring_contracts', 0)}")
        lines.append("")
        
        lines.append("=" * 80)
        lines.append("                    KẾT THÚC BÁO CÁO")
        lines.append("=" * 80)
        
        return "\n".join(lines)
    
    def _generate_revenue_report(self) -> str:
        """Generate revenue report"""
        try:
            from src.services.report_service import ReportService
            from datetime import datetime
            
            service = ReportService()
            summary = service.get_dashboard_summary()
            revenue = summary.get('revenue', {})
            
            lines = []
            lines.append("=" * 80)
            lines.append("                    BÁO CÁO DOANH THU")
            lines.append(f"                    Ngày: {datetime.now().strftime('%d/%m/%Y')}")
            lines.append("=" * 80)
            lines.append("")
            
            lines.append("1. DOANH THU THEO THÁNG")
            lines.append("-" * 40)
            lines.append(f"  Doanh thu tháng hiện tại: {format_currency(revenue.get('monthly_revenue', 0))}")
            lines.append(f"  Tăng trưởng (tháng): {revenue.get('monthly_growth', 0):.1f}%")
            lines.append("")
            
            lines.append("2. DOANH THU THEO NĂM")
            lines.append("-" * 40)
            lines.append(f"  Doanh thu năm (dự kiến): {format_currency(revenue.get('yearly_revenue', 0))}")
            lines.append("")
            
            lines.append("3. BIỂU ĐỒ DOANH THU")
            lines.append("-" * 40)
            monthly = revenue.get('monthly_revenue', 0)
            bars = int(monthly / 1000000) if monthly > 0 else 0
            lines.append(f"  Tháng: {'█' * min(bars, 50)} {format_currency(monthly)}")
            lines.append("")
            
            lines.append("=" * 80)
            
            return "\n".join(lines)
        except Exception as e:
            return f"Lỗi tạo báo cáo: {str(e)}"
    
    def _generate_warehouse_report(self) -> str:
        """Generate warehouse report"""
        try:
            from src.services.report_service import ReportService
            from datetime import datetime
            
            service = ReportService()
            summary = service.get_dashboard_summary()
            kho = summary.get('kho', {})
            
            lines = []
            lines.append("=" * 80)
            lines.append("                    BÁO CÁO KHO HÀNG")
            lines.append(f"                    Ngày: {datetime.now().strftime('%d/%m/%Y')}")
            lines.append("=" * 80)
            lines.append("")
            
            lines.append("1. TỔNG QUAN KHO")
            lines.append("-" * 40)
            lines.append(f"  Tổng số kho: {kho.get('total', 0)}")
            lines.append(f"  Kho hoạt động: {kho.get('active', 0)}")
            lines.append("")
            
            lines.append("2. DIỆN TÍCH & SỨC CHỨA")
            lines.append("-" * 40)
            lines.append(f"  Tổng diện tích: {kho.get('total_dien_tich', 0):,.0f} m²")
            lines.append(f"  Tổng sức chứa: {kho.get('total_suc_chua', 0):,.0f} m³")
            lines.append("")
            
            lines.append("3. TỶ LỆ LẤP ĐẦY")
            lines.append("-" * 40)
            fill_rate = kho.get('avg_fill_rate', 0)
            bars = int(fill_rate / 2)
            lines.append(f"  Trung bình: {fill_rate:.1f}%")
            lines.append(f"  [{'█' * bars}{'░' * (50 - bars)}]")
            lines.append("")
            
            if fill_rate > 90:
                lines.append("  ⚠️ CẢNH BÁO: Kho gần đầy, cần mở rộng!")
            elif fill_rate < 30:
                lines.append("  💡 GỢI Ý: Kho còn nhiều chỗ trống, cần marketing")
            
            lines.append("")
            lines.append("=" * 80)
            
            return "\n".join(lines)
        except Exception as e:
            return f"Lỗi tạo báo cáo: {str(e)}"
    
    def _generate_contract_report(self) -> str:
        """Generate contract report"""
        try:
            from src.services.report_service import ReportService
            from datetime import datetime
            
            service = ReportService()
            summary = service.get_dashboard_summary()
            hop_dong = summary.get('hop_dong', {})
            
            lines = []
            lines.append("=" * 80)
            lines.append("                    BÁO CÁO HỢP ĐỒNG")
            lines.append(f"                    Ngày: {datetime.now().strftime('%d/%m/%Y')}")
            lines.append("=" * 80)
            lines.append("")
            
            lines.append("1. TỔNG SỐ HỢP ĐỒNG")
            lines.append("-" * 40)
            lines.append(f"  Tổng: {hop_dong.get('total', 0)}")
            lines.append("")
            
            lines.append("2. THEO TRẠNG THÁI")
            lines.append("-" * 40)
            by_status = hop_dong.get('by_status', {})
            for status, count in by_status.items():
                lines.append(f"  {status}: {count}")
            lines.append("")
            
            lines.append("3. CẢNH BÁO")
            lines.append("-" * 40)
            expiring = hop_dong.get('expiring_soon', 0)
            lines.append(f"  Hợp đồng sắp hết hạn (30 ngày): {expiring}")
            if expiring > 0:
                lines.append("  ⚠️ Cần liên hệ khách hàng để gia hạn")
            lines.append("")
            
            lines.append("=" * 80)
            
            return "\n".join(lines)
        except Exception as e:
            return f"Lỗi tạo báo cáo: {str(e)}"
    
    def _generate_alerts_report(self) -> str:
        """Generate alerts report"""
        try:
            from src.services.report_service import ReportService
            from datetime import datetime
            
            service = ReportService()
            summary = service.get_dashboard_summary()
            alerts = summary.get('alerts', {})
            
            lines = []
            lines.append("=" * 80)
            lines.append("                    BÁO CÁO CẢNH BÁO")
            lines.append(f"                    Ngày: {datetime.now().strftime('%d/%m/%Y')}")
            lines.append("=" * 80)
            lines.append("")
            
            lines.append("1. HÀNG HÓA")
            lines.append("-" * 40)
            lines.append(f"  Hàng sắp hết: {alerts.get('low_stock_count', 0)}")
            lines.append(f"  Nghiêm trọng: {alerts.get('critical_alerts', 0)}")
            lines.append("")
            
            lines.append("2. HỢP ĐỒNG")
            lines.append("-" * 40)
            lines.append(f"  Sắp hết hạn: {alerts.get('expiring_contracts', 0)}")
            lines.append("")
            
            lines.append("3. HÀNH ĐỘNG CẦN THỰC HIỆN")
            lines.append("-" * 40)
            if alerts.get('low_stock_count', 0) > 0:
                lines.append("  📦 Cần nhập thêm hàng vào kho")
            if alerts.get('expiring_contracts', 0) > 0:
                lines.append("  📋 Liên hệ khách hàng gia hạn hợp đồng")
            if alerts.get('critical_alerts', 0) > 0:
                lines.append("  🚨 Xử lý các cảnh báo nghiêm trọng ngay")
            if alerts.get('low_stock_count', 0) == 0 and alerts.get('expiring_contracts', 0) == 0:
                lines.append("  ✅ Không có cảnh báo nào")
            
            lines.append("")
            lines.append("=" * 80)
            
            return "\n".join(lines)
        except Exception as e:
            return f"Lỗi tạo báo cáo: {str(e)}"
    
    def _on_export_txt(self):
        """Export report to TXT file"""
        try:
            from src.services.report_service import ReportService
            from datetime import datetime
            import os
            
            service = ReportService()
            
            # Get current report type
            report_type = self.report_type_combo.currentData()
            
            if report_type == "dashboard" or report_type == "summary":
                output_path = service.export_summary_to_text()
                MessageDialog.success(self, "Thành công", f"Đã xuất báo cáo:\n{output_path}")
            else:
                # Generate and save specific report
                if report_type == "revenue":
                    content = self._generate_revenue_report()
                elif report_type == "warehouse":
                    content = self._generate_warehouse_report()
                elif report_type == "contract":
                    content = self._generate_contract_report()
                elif report_type == "alerts":
                    content = self._generate_alerts_report()
                else:
                    content = self.report_content.toPlainText()
                
                # Save to file
                export_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 'data', 'exports')
                os.makedirs(export_dir, exist_ok=True)
                
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                file_path = os.path.join(export_dir, f"bao_cao_{report_type}_{timestamp}.txt")
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                MessageDialog.success(self, "Thành công", f"Đã xuất báo cáo:\n{file_path}")
                
        except Exception as e:
            MessageDialog.error(self, "Lỗi", f"Không thể xuất báo cáo:\n{str(e)}")
    
    def _on_export_excel(self):
        """Export report to Excel"""
        try:
            from datetime import datetime
            import os
            
            # Get current report content
            content = self.report_content.toPlainText()
            if not content:
                MessageDialog.warning(self, "Cảnh báo", "Vui lòng chọn và xem báo cáo trước khi xuất")
                return
            
            # Save as text (Excel export would require openpyxl for formatted export)
            export_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 'data', 'exports')
            os.makedirs(export_dir, exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_type = self.report_type_combo.currentData()
            file_path = os.path.join(export_dir, f"bao_cao_{report_type}_{timestamp}.xlsx")
            
            # Use export_to_excel from helpers if available
            try:
                from src.utils.helpers import export_to_excel
                
                # Create simple data structure
                data = [{'Báo cáo': line} for line in content.split('\n')]
                export_to_excel(data, file_path)
                
                MessageDialog.success(self, "Thành công", f"Đã xuất báo cáo:\n{file_path}")
            except ImportError:
                MessageDialog.warning(self, "Cảnh báo", "Chức năng xuất Excel chưa được cài đặt.\nVui lòng xuất dạng TXT.")
                
        except Exception as e:
            MessageDialog.error(self, "Lỗi", f"Không thể xuất báo cáo:\n{str(e)}")
    
    def _on_print(self):
        """Print report"""
        MessageDialog.info(self, "Thông tin", "Chức năng in báo cáo đang được phát triển.")
    
    def refresh_data(self):
        """Refresh data"""
        self.load_dashboard_summary()


__all__ = ['BaoCaoView']
