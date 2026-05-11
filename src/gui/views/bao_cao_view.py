#!/usr/bin/env python3
"""
Báo cáo View - Giao diện Quản lý Báo cáo với biểu đồ
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QComboBox, QScrollArea, QTableWidget, QTableWidgetItem,
    QHeaderView, QAbstractItemView, QSizePolicy
)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont
from typing import Optional, Dict, Any

from src.gui.widgets.charts import BarChartCanvas
from src.gui.dialogs import MessageDialog
from src.utils.formatters import format_currency, format_date


class BaoCaoView(QWidget):
    """
    Giao diện Quản lý Báo cáo - Hiển thị biểu đồ và thống kê
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_report = None
        self.stats_labels = {}
        self.charts = {}
        self._is_refreshing = False
        self.setup_ui()
        self.load_dashboard_summary()

    def setup_ui(self):
        """Setup UI"""
        self.setStyleSheet("""
            QWidget {
                background-color: #f5f5f5;
                font-family: 'Segoe UI', sans-serif;
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
                background-color: #1976d2;
                color: white;
                border: none;
            }
            QPushButton#primaryButton:hover {
                background-color: #1565c0;
            }
            QTableWidget {
                background-color: #ffffff;
                border: none;
                border-radius: 8px;
                gridline-color: #e0e0e0;
            }
            QTableWidget::item {
                padding: 10px;
            }
            QTableWidget::item:selected {
                background-color: #e3f2fd;
            }
            QHeaderView::section {
                background-color: #f8f9fa;
                padding: 12px 8px;
                font-weight: 600;
                color: #31302e;
                border: none;
                border-bottom: 2px solid #1976d2;
            }
        """)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 20, 30, 20)
        main_layout.setSpacing(20)

        # Title section
        title_layout = QHBoxLayout()
        title = QLabel("📊 BÁO CÁO & THỐNG KÊ")
        title.setStyleSheet("font-size: 24px; font-weight: 700; color: #31302e;")
        title_layout.addWidget(title)
        title_layout.addStretch()

        refresh_btn = QPushButton("🔄 Tải lại dữ liệu")
        refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #ffffff;
                color: #1976d2;
                border: 1px solid #1976d2;
                border-radius: 6px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #e3f2fd;
            }
        """)
        refresh_btn.clicked.connect(self.load_dashboard_summary)
        title_layout.addWidget(refresh_btn)

        main_layout.addLayout(title_layout)

        # Scroll area for content
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border: none; background-color: #f5f5f5;")

        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setSpacing(12)
        self.content_layout.setContentsMargins(0, 0, 0, 0)

        # Dashboard page
        self._create_dashboard_content()

        scroll.setWidget(self.content_widget)
        main_layout.addWidget(scroll, 1)

    def _create_dashboard_content(self):
        """Create main dashboard content with chart and table"""
        # Guard against concurrent refresh operations
        if self._is_refreshing:
            return
        self._is_refreshing = True

        try:
            # Clear existing content
            self._clear_layout(self.content_layout)

            # Clear charts dictionary
            self.charts.clear()

            # Summary info section (text-based, no cards)
            summary_section = self._create_summary_section()
            self.content_layout.addWidget(summary_section)

            # Growth chart
            growth_chart = self._create_growth_chart()
            self.content_layout.addWidget(growth_chart)

            # Recent contracts table (will take remaining space)
            recent_table = self._create_recent_contracts_table()
            self.content_layout.addWidget(recent_table, 1)  # Stretch factor 1

        finally:
            self._is_refreshing = False

    def _create_summary_section(self) -> QFrame:
        """Create summary section with text-based info"""
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border: 1px solid rgba(0, 0, 0, 0.08);
                border-radius: 10px;
                padding: 16px;
            }
        """)
        layout = QHBoxLayout(frame)
        layout.setSpacing(30)
        layout.setContentsMargins(20, 12, 20, 12)

        # Summary items
        self.summary_labels = {}

        # Doanh thu tháng
        rev_layout = QVBoxLayout()
        rev_layout.setSpacing(4)
        rev_title = QLabel("Doanh thu tháng")
        rev_title.setStyleSheet("font-size: 12px; color: #757575; font-weight: 500;")
        rev_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        rev_layout.addWidget(rev_title)
        self.summary_labels['revenue'] = QLabel("0 đ")
        self.summary_labels['revenue'].setStyleSheet("font-size: 18px; font-weight: 700; color: #43a047;")
        self.summary_labels['revenue'].setAlignment(Qt.AlignmentFlag.AlignCenter)
        rev_layout.addWidget(self.summary_labels['revenue'])
        layout.addLayout(rev_layout)

        # Separator
        sep1 = QFrame()
        sep1.setFixedWidth(1)
        sep1.setStyleSheet("background-color: #e0e0e0;")
        sep1.setFixedHeight(40)
        layout.addWidget(sep1)

        # Hợp đồng đang hoạt động
        active_layout = QVBoxLayout()
        active_layout.setSpacing(4)
        active_title = QLabel("Hợp đồng đang hoạt động")
        active_title.setStyleSheet("font-size: 12px; color: #757575; font-weight: 500;")
        active_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        active_layout.addWidget(active_title)
        self.summary_labels['active_contracts'] = QLabel("0")
        self.summary_labels['active_contracts'].setStyleSheet("font-size: 18px; font-weight: 700; color: #1976d2;")
        self.summary_labels['active_contracts'].setAlignment(Qt.AlignmentFlag.AlignCenter)
        active_layout.addWidget(self.summary_labels['active_contracts'])
        layout.addLayout(active_layout)

        # Separator
        sep2 = QFrame()
        sep2.setFixedWidth(1)
        sep2.setStyleSheet("background-color: #e0e0e0;")
        sep2.setFixedHeight(40)
        layout.addWidget(sep2)

        # Hợp đồng sắp hết hạn
        expiring_layout = QVBoxLayout()
        expiring_layout.setSpacing(4)
        expiring_title = QLabel("Hợp đồng sắp hết hạn")
        expiring_title.setStyleSheet("font-size: 12px; color: #757575; font-weight: 500;")
        expiring_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        expiring_layout.addWidget(expiring_title)
        self.summary_labels['expiring'] = QLabel("0")
        self.summary_labels['expiring'].setStyleSheet("font-size: 18px; font-weight: 700; color: #ff9800;")
        self.summary_labels['expiring'].setAlignment(Qt.AlignmentFlag.AlignCenter)
        expiring_layout.addWidget(self.summary_labels['expiring'])
        layout.addLayout(expiring_layout)

        # Separator
        sep3 = QFrame()
        sep3.setFixedWidth(1)
        sep3.setStyleSheet("background-color: #e0e0e0;")
        sep3.setFixedHeight(40)
        layout.addWidget(sep3)

        # Tổng khách hàng
        customer_layout = QVBoxLayout()
        customer_layout.setSpacing(4)
        customer_title = QLabel("Tổng khách hàng")
        customer_title.setStyleSheet("font-size: 12px; color: #757575; font-weight: 500;")
        customer_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        customer_layout.addWidget(customer_title)
        self.summary_labels['total_customers'] = QLabel("0")
        self.summary_labels['total_customers'].setStyleSheet("font-size: 18px; font-weight: 700; color: #9c27b0;")
        self.summary_labels['total_customers'].setAlignment(Qt.AlignmentFlag.AlignCenter)
        customer_layout.addWidget(self.summary_labels['total_customers'])
        layout.addLayout(customer_layout)

        layout.addStretch(1)

        return frame

    def _create_stat_card(self, category: str, icon: str, title: str, color: str, is_currency: bool = False) -> QFrame:
        """Create a statistics card"""
        card = QFrame()
        card.setMinimumSize(150, 90)  # Explicit minimum size
        card.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        card.setStyleSheet(f"""
            QFrame {{
                background-color: #f8f9fa;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                padding: 8px;
            }}
        """)
        card.setAutoFillBackground(True)

        layout = QVBoxLayout(card)
        layout.setSpacing(4)
        layout.setContentsMargins(8, 6, 8, 6)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        icon_label = QLabel(icon)
        icon_label.setStyleSheet("font-size: 20px; background-color: transparent;")
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_label.setFixedHeight(24)
        layout.addWidget(icon_label)

        self.stats_labels[f"{category}_value"] = QLabel("0")
        value_color = color if not is_currency else "#43a047"
        self.stats_labels[f"{category}_value"].setStyleSheet(f"""
            QLabel {{
                font-size: 20px;
                font-weight: 700;
                color: {value_color};
                background-color: transparent;
            }}
        """)
        self.stats_labels[f"{category}_value"].setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.stats_labels[f"{category}_value"].setFixedHeight(26)
        layout.addWidget(self.stats_labels[f"{category}_value"])

        title_label = QLabel(title)
        title_label.setStyleSheet("font-size: 11px; color: #616161; font-weight: 500; background-color: transparent;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setWordWrap(True)
        title_label.setFixedHeight(20)
        layout.addWidget(title_label)

        return card

    def _create_growth_chart(self) -> QFrame:
        """Create growth bar chart"""
        frame = QFrame()
        frame.setFixedHeight(220)  # Fixed height for compactness
        frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        frame.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border: 1px solid rgba(0, 0, 0, 0.08);
                border-radius: 10px;
                padding: 12px;
            }
        """)

        layout = QVBoxLayout(frame)
        layout.setContentsMargins(8, 8, 8, 8)

        title = QLabel("📈 Mức độ tăng trưởng")
        title.setStyleSheet("font-size: 14px; font-weight: 600; color: #31302e; padding-bottom: 6px;")
        layout.addWidget(title)

        self.charts['growth'] = BarChartCanvas(
            data={}, title="", x_label="Tháng", y_label="Doanh thu (VNĐ)",
            colors='#1976d2', width=10, height=2.8
        )
        layout.addWidget(self.charts['growth'])

        return frame

    def _create_recent_contracts_table(self) -> QFrame:
        """Create recent contracts table"""
        frame = QFrame()
        frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        frame.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border: 1px solid rgba(0, 0, 0, 0.08);
                border-radius: 10px;
                padding: 12px;
            }
        """)

        layout = QVBoxLayout(frame)
        layout.setContentsMargins(8, 8, 8, 8)

        title = QLabel("📋 Danh sách khách hàng tạo hợp đồng gần đây")
        title.setStyleSheet("font-size: 14px; font-weight: 600; color: #31302e; padding-bottom: 6px;")
        layout.addWidget(title)

        # Table widget - set to expand vertically
        self.recent_table = QTableWidget()
        self.recent_table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.recent_table.setColumnCount(5)
        self.recent_table.setHorizontalHeaderLabels([
            "Mã KH", "Tên khách hàng", "Mã hợp đồng", "Ngày tạo", "Giá trị"
        ])
        self.recent_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.recent_table.verticalHeader().setVisible(False)
        self.recent_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.recent_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.recent_table.setMinimumHeight(150)
        self.recent_table.setStyleSheet("""
            QTableWidget {
                border: none;
                border-radius: 8px;
            }
            QTableWidget::item {
                padding: 8px 6px;
            }
        """)

        layout.addWidget(self.recent_table, 1)  # Stretch factor 1

        return frame

    def load_dashboard_summary(self):
        """Load dashboard summary data and update UI"""
        try:
            from src.services.report_service import ReportService
            from src.services.hop_dong_service import HopDongService
            from src.models import KhachHang

            service = ReportService()
            summary = service.get_dashboard_summary()

            # Update summary labels
            revenue = summary.get('revenue', {})
            monthly_revenue = revenue.get('monthly_revenue', 0)
            self.summary_labels['revenue'].setText(format_currency(monthly_revenue))

            hop_dong = summary.get('hop_dong', {})
            active_count = hop_dong.get('by_status', {}).get('hieu_luc', 0)
            self.summary_labels['active_contracts'].setText(str(active_count))

            expiring_count = hop_dong.get('expiring_soon', 0)
            self.summary_labels['expiring'].setText(str(expiring_count))

            khach_hang = summary.get('khach_hang', {})
            total_customers = khach_hang.get('total', 0)
            self.summary_labels['total_customers'].setText(str(total_customers))

            # Update growth chart
            self._update_growth_chart(revenue)

            # Update recent contracts table
            self._update_recent_contracts_table()

        except Exception as e:
            MessageDialog.error(self, "Lỗi", f"Không thể tải dữ liệu:\n{str(e)}")

    def _update_growth_chart(self, revenue: dict):
        """Update growth bar chart"""
        # Create mock monthly data for demonstration
        # In production, this would come from actual historical data
        monthly_data = {
            'T1': 0, 'T2': 0, 'T3': 0, 'T4': 0, 'T5': 0, 'T6': 0,
            'T7': 0, 'T8': 0, 'T9': 0, 'T10': 0, 'T11': 0, 'T12': 0
        }
        monthly_rev = revenue.get('monthly_revenue', 0)
        if monthly_rev > 0:
            for key in monthly_data:
                monthly_data[key] = monthly_rev // 12

        if 'growth' in self.charts:
            self.charts['growth'].update_data(monthly_data)

    def _update_recent_contracts_table(self):
        """Update recent contracts table"""
        try:
            from src.services.hop_dong_service import HopDongService

            service = HopDongService()
            hop_dongs = service.get_all(limit=20)

            # Sort by creation date (most recent first)
            # Filter only active contracts
            active_contracts = [
                hd for hd in hop_dongs
                if (hd.trang_thai.value if hasattr(hd.trang_thai, 'value') else str(hd.trang_thai)) == 'hieu_luc'
            ]

            # Sort by ngay_ky (or ngay_tao) if available, most recent first
            def get_date(hd):
                if hasattr(hd, 'ngay_bat_dau') and hd.ngay_bat_dau:
                    return hd.ngay_bat_dau
                return getattr(hd, 'created_at', None) or QDate(2000, 1, 1)

            active_contracts.sort(key=get_date, reverse=True)

            # Take top 10 most recent
            recent = active_contracts[:10]

            # Update table
            self.recent_table.setRowCount(len(recent))

            for row, hd in enumerate(recent):
                # Get customer info
                ma_khach_hang = hd.ma_khach_hang or ""
                ten_khach_hang = ""
                if hasattr(hd, 'khach_hang') and hd.khach_hang:
                    ten_khach_hang = hd.khach_hang.ho_ten or ""

                # Get contract info
                ma_hop_dong = hd.ma_hop_dong or ""

                # Get date
                ngay_tao = ""
                if hasattr(hd, 'ngay_bat_dau') and hd.ngay_bat_dau:
                    if isinstance(hd.ngay_bat_dau, QDate):
                        ngay_tao = hd.ngay_bat_dau.toString('dd/MM/yyyy')
                    else:
                        ngay_tao = format_date(hd.ngay_bat_dau)

                # Get value
                gia_tri = hd.gia_thue or 0

                self.recent_table.setItem(row, 0, QTableWidgetItem(ma_khach_hang))
                self.recent_table.setItem(row, 1, QTableWidgetItem(ten_khach_hang))
                self.recent_table.setItem(row, 2, QTableWidgetItem(ma_hop_dong))
                self.recent_table.setItem(row, 3, QTableWidgetItem(ngay_tao))
                self.recent_table.setItem(row, 4, QTableWidgetItem(format_currency(gia_tri)))

        except Exception as e:
            print(f"Error updating recent contracts table: {e}")

    def refresh_data(self):
        """Refresh data"""
        self._create_dashboard_content()
        self.load_dashboard_summary()

    def _clear_layout(self, layout):
        """Recursively clear a layout"""
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
            elif child.layout():
                self._clear_layout(child.layout())

    def _on_export_excel(self):
        """Export report to Excel"""
        try:
            from src.utils.export_service import export_to_excel
            from src.services.report_service import ReportService
            from PyQt6.QtWidgets import QFileDialog
            from datetime import datetime

            service = ReportService()
            summary = service.get_dashboard_summary()

            # Prepare export data
            export_data = []

            # Stats
            revenue = summary.get('revenue', {})
            hop_dong = summary.get('hop_dong', {})

            export_data.append({"Danh mục": "Doanh thu tháng", "Giá trị": revenue.get('monthly_revenue', 0)})
            export_data.append({"Danh mục": "Hợp đồng đang hoạt động", "Giá trị": hop_dong.get('by_status', {}).get('hieu_luc', 0)})
            export_data.append({"Danh mục": "Hợp đồng sắp hết hạn", "Giá trị": hop_dong.get('expiring_soon', 0)})

            # Ask for save location
            default_name = f"bao_cao_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Xuất Excel",
                default_name,
                "Excel Files (*.xlsx)"
            )

            if file_path:
                export_to_excel(export_data, file_path)
                MessageDialog.success(self, "Thành công", f"Đã xuất file Excel:\n{file_path}")

        except ImportError as e:
            MessageDialog.error(self, "Thiếu thư viện", "Cần cài đặt pandas và openpyxl:\npip install pandas openpyxl")
        except Exception as e:
            MessageDialog.error(self, "Lỗi", f"Không thể xuất Excel:\n{str(e)}")


__all__ = ['BaoCaoView']