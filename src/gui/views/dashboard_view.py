#!/usr/bin/env python3
"""
Dashboard View - Giao diện tổng quan với thống kê kho
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QGridLayout, QProgressBar, QScrollArea, QPushButton
)
from PyQt6.QtCore import Qt, QTimer
from typing import Dict, Any, List

from src.services import KhoService, ViTriService
from src.models import Kho, TrangThaiKhoEnum
from src.gui.dialogs import MessageDialog
from src.gui.widgets.charts import PieChartCanvas, FillRateBarChart
from src.utils.formatters import format_currency, format_number


class DashboardView(QWidget):
    """
    Dashboard với thống kê tổng quan về kho và vị trí
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.kho_service = KhoService()
        self.vi_tri_service = ViTriService()
        self.setup_ui()
        self.load_data()
        
        # Auto-refresh every 30 seconds
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self.load_data)
        self.refresh_timer.start(30000)  # 30 seconds
    
    def setup_ui(self):
        """Setup UI"""
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title = QLabel("📊 DASHBOARD TỔNG QUAN")
        title.setObjectName("titleLabel")
        title.setStyleSheet("""
            QLabel {
                font-size: 28px;
                font-weight: 700;
                color: #31302e;
                padding: 10px 0 20px;
            }
        """)
        layout.addWidget(title)
        
        # Key metrics
        metrics = self._create_key_metrics()
        layout.addWidget(metrics)
        
        # Warehouse stats
        warehouse_stats = self._create_warehouse_stats()
        layout.addWidget(warehouse_stats)
        
        # Fill rate chart
        fill_rate_section = self._create_fill_rate_section()
        layout.addWidget(fill_rate_section)
        
        # Charts section
        charts_section = self._create_charts_section()
        layout.addWidget(charts_section)
        
        # Overcrowded alerts
        alerts_section = self._create_alerts_section()
        layout.addWidget(alerts_section)
        
        # Recent activity (placeholder)
        activity_section = self._create_activity_section()
        layout.addWidget(activity_section)
        
        layout.addStretch()
        
        scroll.setWidget(container)
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(scroll)
    
    def _create_key_metrics(self) -> QFrame:
        """Create key metrics cards"""
        frame = QFrame()
        frame.setFrameShape(QFrame.Shape.StyledPanel)
        frame.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border: 1px solid rgba(0, 0, 0, 0.1);
                border-radius: 12px;
                padding: 20px;
            }
        """)
        
        layout = QGridLayout(frame)
        layout.setSpacing(20)
        
        # Metric cards
        self.metric_tong_kho = self._create_metric_card("🏭", "Tổng Kho", "0", "#1976d2")
        self.metric_kho_hoat_dong = self._create_metric_card("✅", "Hoạt Động", "0", "#1aae39")
        self.metric_tong_vi_tri = self._create_metric_card("📦", "Vị Trí", "0", "#ff9800")
        self.metric_vi_tri_trong = self._create_metric_card("✅", "Vị Trí Trống", "0", "#4caf50")
        
        layout.addWidget(self.metric_tong_kho, 0, 0)
        layout.addWidget(self.metric_kho_hoat_dong, 0, 1)
        layout.addWidget(self.metric_tong_vi_tri, 1, 0)
        layout.addWidget(self.metric_vi_tri_trong, 1, 1)
        
        return frame
    
    def _create_metric_card(self, icon: str, label: str, value: str, color: str) -> QFrame:
        """Create a metric card"""
        card = QFrame()
        card.setFrameShape(QFrame.Shape.StyledPanel)
        card.setStyleSheet(f"""
            QFrame {{
                background-color: #f6f5f4;
                border-radius: 8px;
                padding: 16px;
            }}
        """)
        
        layout = QVBoxLayout(card)
        layout.setSpacing(8)
        
        # Icon
        icon_label = QLabel(icon)
        icon_label.setStyleSheet("font-size: 32px;")
        layout.addWidget(icon_label)
        
        # Label
        label_label = QLabel(label)
        label_label.setStyleSheet("""
            QLabel {
                color: #615d59;
                font-size: 13px;
                font-weight: 500;
            }
        """)
        layout.addWidget(label_label)
        
        # Value
        value_label = QLabel(value)
        value_label.setStyleSheet(f"""
            QLabel {{
                color: {color};
                font-size: 32px;
                font-weight: 700;
            }}
        """)
        layout.addWidget(value_label)
        
        return card
    
    def _create_warehouse_stats(self) -> QFrame:
        """Create warehouse statistics section"""
        frame = QFrame()
        frame.setFrameShape(QFrame.Shape.StyledPanel)
        frame.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border: 1px solid rgba(0, 0, 0, 0.1);
                border-radius: 12px;
                padding: 20px;
            }
        """)
        
        layout = QVBoxLayout(frame)
        layout.setSpacing(16)
        
        # Title
        title = QLabel("📈 Thống Kê Kho")
        title.setStyleSheet("""
            QLabel {
                font-size: 20px;
                font-weight: 700;
                color: #31302e;
            }
        """)
        layout.addWidget(title)
        
        # Warehouse list with fill rates
        self.warehouse_list_layout = QVBoxLayout()
        self.warehouse_list_layout.setSpacing(12)
        layout.addLayout(self.warehouse_list_layout)
        
        return frame
    
    def _create_fill_rate_section(self) -> QFrame:
        """Create fill rate visualization"""
        frame = QFrame()
        frame.setFrameShape(QFrame.Shape.StyledPanel)
        frame.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border: 1px solid rgba(0, 0, 0, 0.1);
                border-radius: 12px;
                padding: 20px;
            }
        """)
        
        layout = QVBoxLayout(frame)
        layout.setSpacing(16)
        
        # Title
        title = QLabel("📊 Tỷ Lệ Lấp Đầy")
        title.setStyleSheet("""
            QLabel {
                font-size: 20px;
                font-weight: 700;
                color: #31302e;
            }
        """)
        layout.addWidget(title)
        
        # Average fill rate
        avg_layout = QHBoxLayout()
        avg_layout.addWidget(QLabel("Trung bình:"))
        self.avg_fill_rate = QLabel("0%")
        self.avg_fill_rate.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: 700;
                color: #ff9800;
            }
        """)
        avg_layout.addWidget(self.avg_fill_rate)
        avg_layout.addStretch()
        layout.addLayout(avg_layout)
        
        # Progress bar
        self.fill_rate_progress = QProgressBar()
        self.fill_rate_progress.setMinimum(0)
        self.fill_rate_progress.setMaximum(100)
        self.fill_rate_progress.setValue(0)
        self.fill_rate_progress.setFormat("%p%")
        self.fill_rate_progress.setStyleSheet("""
            QProgressBar {
                background-color: #f6f5f4;
                border: none;
                border-radius: 6px;
                height: 24px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #ff9800;
                border-radius: 6px;
            }
        """)
        layout.addWidget(self.fill_rate_progress)
        
        # Legend
        legend_layout = QHBoxLayout()
        legend_layout.setSpacing(20)
        
        legend_layout.addWidget(self._create_legend_item("Thấp (<50%)", "#4caf50"))
        legend_layout.addWidget(self._create_legend_item("TB (50-75%)", "#ff9800"))
        legend_layout.addWidget(self._create_legend_item("Cao (>75%)", "#f44336"))
        
        layout.addLayout(legend_layout)
        
        return frame
    
    def _create_charts_section(self) -> QFrame:
        """Create charts section with pie and bar charts"""
        frame = QFrame()
        frame.setFrameShape(QFrame.Shape.StyledPanel)
        frame.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border: 1px solid rgba(0, 0, 0, 0.1);
                border-radius: 12px;
                padding: 20px;
            }
        """)
        
        layout = QHBoxLayout(frame)
        layout.setSpacing(20)
        
        # Pie chart - Warehouse Status
        pie_frame = QFrame()
        pie_frame.setStyleSheet("""
            QFrame {
                background-color: #fafafa;
                border-radius: 8px;
                padding: 10px;
            }
        """)
        pie_layout = QVBoxLayout(pie_frame)
        pie_layout.setContentsMargins(5, 5, 5, 5)
        
        pie_title = QLabel("📈 Trạng Thái Kho")
        pie_title.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: 700;
                color: #31302e;
                padding-bottom: 8px;
            }
        """)
        pie_layout.addWidget(pie_title)
        
        self.pie_chart = PieChartCanvas(
            parent=pie_frame,
            data={},
            title="",
            colors=['#1aae39', '#ff9800', '#757575'],
            width=4,
            height=3.5,
            dpi=80
        )
        pie_layout.addWidget(self.pie_chart)
        
        layout.addWidget(pie_frame, 1)
        
        # Bar chart - Fill Rate by Warehouse
        bar_frame = QFrame()
        bar_frame.setStyleSheet("""
            QFrame {
                background-color: #fafafa;
                border-radius: 8px;
                padding: 10px;
            }
        """)
        bar_layout = QVBoxLayout(bar_frame)
        bar_layout.setContentsMargins(5, 5, 5, 5)
        
        bar_title = QLabel("📊 Tỷ Lệ Lấp Đầy Theo Kho")
        bar_title.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: 700;
                color: #31302e;
                padding-bottom: 8px;
            }
        """)
        bar_layout.addWidget(bar_title)
        
        self.bar_chart = FillRateBarChart(
            parent=bar_frame,
            data={},
            title="",
            width=5,
            height=3.5,
            dpi=80
        )
        bar_layout.addWidget(self.bar_chart)
        
        layout.addWidget(bar_frame, 1)
        
        return frame
    
    def _create_legend_item(self, label: str, color: str) -> QLabel:
        """Create legend item"""
        label_widget = QLabel(f"⬤ {label}")
        label_widget.setStyleSheet(f"""
            QLabel {{
                color: {color};
                font-size: 13px;
            }}
        """)
        return label_widget
    
    def _create_alerts_section(self) -> QFrame:
        """Create alerts section for overcrowded warehouses"""
        frame = QFrame()
        frame.setFrameShape(QFrame.Shape.StyledPanel)
        frame.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border: 1px solid rgba(0, 0, 0, 0.1);
                border-radius: 12px;
                padding: 20px;
            }
        """)
        
        layout = QVBoxLayout(frame)
        layout.setSpacing(16)
        
        # Title
        title = QLabel("⚠️ Cảnh Báo")
        title.setStyleSheet("""
            QLabel {
                font-size: 20px;
                font-weight: 700;
                color: #31302e;
            }
        """)
        layout.addWidget(title)
        
        # Alerts list
        self.alerts_layout = QVBoxLayout()
        self.alerts_layout.setSpacing(12)
        layout.addLayout(self.alerts_layout)
        
        # No alerts placeholder
        self.no_alerts_label = QLabel("✅ Không có cảnh báo nào")
        self.no_alerts_label.setStyleSheet("""
            QLabel {
                color: #615d59;
                font-size: 14px;
                padding: 20px;
                text-align: center;
            }
        """)
        self.alerts_layout.addWidget(self.no_alerts_label)
        
        return frame
    
    def _create_activity_section(self) -> QFrame:
        """Create recent activity section"""
        frame = QFrame()
        frame.setFrameShape(QFrame.Shape.StyledPanel)
        frame.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border: 1px solid rgba(0, 0, 0, 0.1);
                border-radius: 12px;
                padding: 20px;
            }
        """)
        
        layout = QVBoxLayout(frame)
        layout.setSpacing(16)
        
        # Title
        title = QLabel("🕐 Hoạt Động Gần Đây")
        title.setStyleSheet("""
            QLabel {
                font-size: 20px;
                font-weight: 700;
                color: #31302e;
            }
        """)
        layout.addWidget(title)
        
        # Placeholder
        placeholder = QLabel("Tính năng sẽ được cập nhật...")
        placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        placeholder.setStyleSheet("""
            QLabel {
                color: #757575;
                font-size: 14px;
                padding: 40px;
            }
        """)
        layout.addWidget(placeholder)
        
        return frame
    
    def load_data(self):
        """Load dashboard data"""
        try:
            # Load warehouses
            khos = self.kho_service.get_all(limit=100)
            
            # Calculate metrics
            tong_kho = len(khos)
            kho_hoat_dong = sum(1 for k in khos if k.trang_thai == TrangThaiKhoEnum.HOAT_DONG)
            
            # Load all positions
            all_vi_tris = []
            for kho in khos:
                vi_tris = self.vi_tri_service.get_vi_tri_by_kho(kho.ma_kho)
                all_vi_tris.extend(vi_tris)
            
            tong_vi_tri = len(all_vi_tris)
            vi_tri_trong = sum(1 for v in all_vi_tris if str(v.trang_thai) == 'trong')
            
            # Update metrics
            self._update_metric(self.metric_tong_kho, str(tong_kho))
            self._update_metric(self.metric_kho_hoat_dong, str(kho_hoat_dong))
            self._update_metric(self.metric_tong_vi_tri, str(tong_vi_tri))
            self._update_metric(self.metric_vi_tri_trong, str(vi_tri_trong))
            
            # Update warehouse list
            self._update_warehouse_list(khos)
            
            # Update fill rate
            self._update_fill_rate(khos)
            
            # Update charts
            self._update_charts(khos)
            
            # Update alerts
            self._update_alerts(khos)
            
        except Exception as e:
            MessageDialog.error(self, "Lỗi", f"Không thể tải dashboard:\n{str(e)}")
    
    def _update_metric(self, card: QFrame, value: str):
        """Update metric card value"""
        value_label = card.findChild(QLabel, value)
        for child in card.findChildren(QLabel):
            if child.styleSheet() and "font-size: 32px" in child.styleSheet():
                child.setText(value)
                break
    
    def _update_warehouse_list(self, khos: List[Kho]):
        """Update warehouse list with fill rates"""
        # Clear existing
        while self.warehouse_list_layout.count():
            item = self.warehouse_list_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # Add warehouse cards
        total_fill_rate = 0
        
        for kho in khos:
            if kho.trang_thai == TrangThaiKhoEnum.NGUNG:
                continue
            
            fill_rate = self.kho_service.calculate_fill_rate(kho.ma_kho)
            total_fill_rate += fill_rate
            
            card = self._create_warehouse_card(kho, fill_rate)
            self.warehouse_list_layout.addWidget(card)
        
        # Update average
        avg_fill_rate = total_fill_rate / len(khos) if khos else 0
        self.avg_fill_rate.setText(f"{avg_fill_rate:.1f}%")
        self.fill_rate_progress.setValue(int(avg_fill_rate))
    
    def _create_warehouse_card(self, kho: Kho, fill_rate: float) -> QFrame:
        """Create warehouse card with fill rate"""
        card = QFrame()
        card.setFrameShape(QFrame.Shape.StyledPanel)
        card.setStyleSheet("""
            QFrame {
                background-color: #f6f5f4;
                border-radius: 8px;
                padding: 12px;
            }
        """)
        
        layout = QVBoxLayout(card)
        layout.setSpacing(8)
        
        # Header
        header_layout = QHBoxLayout()
        
        name_label = QLabel(f"🏭 {kho.ten_kho}")
        name_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: 600;
                color: #31302e;
            }
        """)
        header_layout.addWidget(name_label)
        
        fill_rate_label = QLabel(f"{fill_rate:.1f}%")
        fill_rate_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: 700;
                color: #ff9800;
            }
        """)
        header_layout.addWidget(fill_rate_label)
        
        layout.addLayout(header_layout)
        
        # Progress bar
        progress = QProgressBar()
        progress.setMinimum(0)
        progress.setMaximum(100)
        progress.setValue(int(fill_rate))
        progress.setFormat("%p%")
        progress.setStyleSheet(self._get_progress_style(fill_rate))
        layout.addWidget(progress)
        
        # Details
        details = self.kho_service.get_available_capacity(kho.ma_kho)
        details_label = QLabel(
            f"Đã sử dụng: {details.get('da_su_dung', 0):,.0f} m³ / "
            f"Tổng: {details.get('tong_dien_tich', 0):,.0f} m³ | "
            f"Vị trí trống: {details.get('so_vi_tri_trong', 0)}"
        )
        details_label.setStyleSheet("""
            QLabel {
                color: #615d59;
                font-size: 13px;
            }
        """)
        layout.addWidget(details_label)
        
        return card
    
    def _get_progress_style(self, fill_rate: float) -> str:
        """Get progress bar style based on fill rate"""
        if fill_rate < 50:
            color = "#4caf50"  # Green
        elif fill_rate < 75:
            color = "#ff9800"  # Orange
        else:
            color = "#f44336"  # Red
        
        return f"""
            QProgressBar {{
                background-color: #e0e0e0;
                border: none;
                border-radius: 6px;
                height: 12px;
                text-align: center;
            }}
            QProgressBar::chunk {{
                background-color: {color};
                border-radius: 6px;
            }}
        """
    
    def _update_fill_rate(self, khos: List[Kho]):
        """Update fill rate visualization"""
        total_fill_rate = 0
        
        for kho in khos:
            if kho.trang_thai != TrangThaiKhoEnum.NGUNG:
                fill_rate = self.kho_service.calculate_fill_rate(kho.ma_kho)
                total_fill_rate += fill_rate
        
        avg_fill_rate = total_fill_rate / len(khos) if khos else 0
        
        self.avg_fill_rate.setText(f"{avg_fill_rate:.1f}%")
        self.fill_rate_progress.setValue(int(avg_fill_rate))
    
    def _update_charts(self, khos: List[Kho]):
        """Update pie and bar charts with warehouse data"""
        # Pie chart data - Warehouse status distribution
        status_counts = {
            'Hoạt Động': 0,
            'Bảo Trì': 0,
            'Ngừng': 0
        }
        
        fill_rate_data = {}
        
        for kho in khos:
            # Count by status
            if kho.trang_thai == TrangThaiKhoEnum.HOAT_DONG:
                status_counts['Hoạt Động'] += 1
            elif kho.trang_thai == TrangThaiKhoEnum.BAO_TRI:
                status_counts['Bảo Trì'] += 1
            elif kho.trang_thai == TrangThaiKhoEnum.NGUNG:
                status_counts['Ngừng'] += 1
            
            # Fill rate for bar chart
            if kho.trang_thai != TrangThaiKhoEnum.NGUNG:
                fill_rate = self.kho_service.calculate_fill_rate(kho.ma_kho)
                fill_rate_data[kho.ten_kho] = fill_rate
        
        # Remove zero values from pie chart
        pie_data = {k: v for k, v in status_counts.items() if v > 0}
        
        # Update charts
        self.pie_chart.update_data(pie_data)
        self.bar_chart.update_data(fill_rate_data)
    
    def _update_alerts(self, khos: List[Kho]):
        """Update alerts for overcrowded warehouses"""
        # Clear existing alerts
        while self.alerts_layout.count():
            item = self.alerts_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # Find overcrowded warehouses
        overcrowded = []
        for kho in khos:
            if kho.trang_thai == TrangThaiKhoEnum.NGUNG:
                continue
            
            fill_rate = self.kho_service.calculate_fill_rate(kho.ma_kho)
            if fill_rate > 90:
                overcrowded.append((kho, fill_rate))
        
        if not overcrowded:
            # Show no alerts message
            self.no_alerts_label = QLabel("✅ Không có cảnh báo nào")
            self.no_alerts_label.setStyleSheet("""
                QLabel {
                    color: #615d59;
                    font-size: 14px;
                    padding: 20px;
                    text-align: center;
                }
            """)
            self.alerts_layout.addWidget(self.no_alerts_label)
        else:
            # Show alerts
            for kho, fill_rate in overcrowded:
                alert_card = self._create_alert_card(kho, fill_rate)
                self.alerts_layout.addWidget(alert_card)
    
    def _create_alert_card(self, kho: Kho, fill_rate: float) -> QFrame:
        """Create alert card for overcrowded warehouse"""
        card = QFrame()
        card.setFrameShape(QFrame.Shape.StyledPanel)
        card.setStyleSheet("""
            QFrame {
                background-color: #ffebee;
                border-left: 4px solid #f44336;
                border-radius: 8px;
                padding: 12px;
            }
        """)
        
        layout = QHBoxLayout(card)
        
        # Icon
        icon = QLabel("⚠️")
        icon.setStyleSheet("font-size: 32px;")
        layout.addWidget(icon)
        
        # Content
        content_layout = QVBoxLayout()
        
        title = QLabel(f"Kho {kho.ten_kho} quá tải!")
        title.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: 700;
                color: #d32f2f;
            }
        """)
        content_layout.addWidget(title)
        
        details = QLabel(
            f"Tỷ lệ lấp đầy: {fill_rate:.1f}% | "
            f"Địa chỉ: {kho.dia_chi}"
        )
        details.setStyleSheet("""
            QLabel {
                color: #b71c1c;
                font-size: 13px;
            }
        """)
        content_layout.addWidget(details)
        
        layout.addLayout(content_layout)
        
        # Action button
        action_btn = QPushButton("Xem chi tiết")
        action_btn.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #d32f2f;
            }
        """)
        layout.addWidget(action_btn)
        
        return card
    
    def refresh_data(self):
        """Refresh dashboard data"""
        self.load_data()


__all__ = ['DashboardView']
