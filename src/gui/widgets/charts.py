#!/usr/bin/env python3
"""
Chart widgets for dashboard using matplotlib
"""
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for PyQt6
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from PyQt6.QtWidgets import QSizePolicy
from PyQt6.QtCore import Qt


class PieChartCanvas(FigureCanvasQTAgg):
    """Pie chart widget for displaying distribution data"""
    
    def __init__(self, parent=None, data=None, title="", colors=None, width=5, height=4, dpi=100):
        """
        Initialize pie chart
        
        Args:
            parent: Parent widget
            data: dict of {label: value}
            title: Chart title
            colors: list of hex color strings
            width: Figure width in inches
            height: Figure height in inches
            dpi: Dots per inch
        """
        self.fig, self.ax = plt.subplots(figsize=(width, height), dpi=dpi)
        super().__init__(self.fig)
        self.setParent(parent)
        
        self.data = data or {}
        self.title = title
        self.colors = colors or ['#1976d2', '#1aae39', '#ff9800', '#f44336', '#9c27b0', '#00bcd4']
        
        FigureCanvasQTAgg.setSizePolicy(self, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        FigureCanvasQTAgg.updateGeometry(self)
        
        self.plot()
    
    def plot(self):
        """Draw the pie chart"""
        self.ax.clear()
        
        if not self.data:
            self.ax.text(0.5, 0.5, 'Không có dữ liệu', 
                        ha='center', va='center', fontsize=12, color='#757575')
            self.ax.axis('off')
            self.draw()
            return
        
        labels = list(self.data.keys())
        values = list(self.data.values())
        
        # Create pie chart
        wedges, texts, autotexts = self.ax.pie(
            values,
            labels=None,
            autopct='%1.1f%%',
            colors=self.colors[:len(values)],
            startangle=90,
            wedgeprops={'edgecolor': 'white', 'linewidth': 2},
            textprops={'fontsize': 10}
        )
        
        # Style autopct text
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
            autotext.set_fontsize(9)
        
        # Add title
        if self.title:
            self.ax.set_title(self.title, fontsize=12, fontweight='bold', pad=10, color='#31302e')
        
        # Add legend
        self.ax.legend(wedges, labels, loc='lower center', bbox_to_anchor=(0.5, -0.12),
                      ncol=2, fontsize=9, frameon=False)
        
        self.fig.tight_layout()
        self.draw()
    
    def update_data(self, data, title=None):
        """Update chart data"""
        self.data = data
        if title:
            self.title = title
        self.plot()


class BarChartCanvas(FigureCanvasQTAgg):
    """Bar chart widget for comparing values"""
    
    def __init__(self, parent=None, data=None, title="", x_label="", y_label="", 
                 colors=None, width=6, height=4, dpi=100, horizontal=False):
        """
        Initialize bar chart
        
        Args:
            parent: Parent widget
            data: dict of {label: value}
            title: Chart title
            x_label: Label for x-axis
            y_label: Label for y-axis
            colors: list of hex color strings or single color
            width: Figure width in inches
            height: Figure height in inches
            dpi: Dots per inch
            horizontal: If True, bars are horizontal
        """
        self.fig, self.ax = plt.subplots(figsize=(width, height), dpi=dpi)
        super().__init__(self.fig)
        self.setParent(parent)
        
        self.data = data or {}
        self.title = title
        self.x_label = x_label
        self.y_label = y_label
        self.colors = colors or '#1976d2'
        self.horizontal = horizontal
        
        FigureCanvasQTAgg.setSizePolicy(self, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        FigureCanvasQTAgg.updateGeometry(self)
        
        self.plot()
    
    def plot(self):
        """Draw the bar chart"""
        self.ax.clear()
        
        if not self.data:
            self.ax.text(0.5, 0.5, 'Không có dữ liệu', 
                        ha='center', va='center', fontsize=12, color='#757575')
            self.ax.axis('off')
            self.draw()
            return
        
        labels = list(self.data.keys())
        values = list(self.data.values())
        
        if self.horizontal:
            bars = self.ax.barh(labels, values, color=self.colors, edgecolor='white', linewidth=1)
            # Add value labels
            for bar, val in zip(bars, values):
                self.ax.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2,
                           f'{val:.1f}', va='center', fontsize=9, fontweight='bold')
            self.ax.set_xlim(0, max(values) * 1.15)
        else:
            bars = self.ax.bar(labels, values, color=self.colors, edgecolor='white', linewidth=1)
            # Add value labels on top
            for bar, val in zip(bars, values):
                self.ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                           f'{val:.1f}', ha='center', va='bottom', fontsize=9, fontweight='bold')
            self.ax.set_ylim(0, max(values) * 1.15)
            self.ax.tick_params(axis='x', rotation=15)
        
        # Style
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        self.ax.spines['left'].set_color('#e0e0e0')
        self.ax.spines['bottom'].set_color('#e0e0e0')
        self.ax.tick_params(colors='#615d59')
        
        # Labels
        if self.title:
            self.ax.set_title(self.title, fontsize=12, fontweight='bold', pad=10, color='#31302e')
        if self.x_label:
            self.ax.set_xlabel(self.x_label, fontsize=10, color='#615d59')
        if self.y_label:
            self.ax.set_ylabel(self.y_label, fontsize=10, color='#615d59')
        
        self.fig.tight_layout()
        self.draw()
    
    def update_data(self, data, title=None):
        """Update chart data"""
        self.data = data
        if title:
            self.title = title
        self.plot()


class FillRateBarChart(FigureCanvasQTAgg):
    """Horizontal bar chart showing fill rates with color coding"""
    
    def __init__(self, parent=None, data=None, title="Tỷ Lệ Lấp Đầy Theo Kho", 
                 width=6, height=4, dpi=100):
        """
        Initialize fill rate bar chart
        
        Args:
            parent: Parent widget
            data: dict of {kho_name: fill_rate_percentage}
            title: Chart title
            width: Figure width in inches
            height: Figure height in inches
            dpi: Dots per inch
        """
        self.fig, self.ax = plt.subplots(figsize=(width, height), dpi=dpi)
        super().__init__(self.fig)
        self.setParent(parent)
        
        self.data = data or {}
        self.title = title
        
        FigureCanvasQTAgg.setSizePolicy(self, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        FigureCanvasQTAgg.updateGeometry(self)
        
        self.plot()
    
    def _get_color(self, value):
        """Get color based on fill rate value"""
        if value < 50:
            return '#4caf50'  # Green - Low
        elif value < 75:
            return '#ff9800'  # Orange - Medium
        elif value < 90:
            return '#ff5722'  # Deep Orange - High
        else:
            return '#f44336'  # Red - Critical
    
    def plot(self):
        """Draw the fill rate bar chart"""
        self.ax.clear()
        
        if not self.data:
            self.ax.text(0.5, 0.5, 'Không có dữ liệu', 
                        ha='center', va='center', fontsize=12, color='#757575')
            self.ax.axis('off')
            self.draw()
            return
        
        # Sort by fill rate
        sorted_data = sorted(self.data.items(), key=lambda x: x[1], reverse=True)
        labels = [item[0] for item in sorted_data]
        values = [item[1] for item in sorted_data]
        colors = [self._get_color(v) for v in values]
        
        # Create horizontal bars
        y_pos = range(len(labels))
        bars = self.ax.barh(y_pos, values, color=colors, edgecolor='white', linewidth=1, height=0.6)
        
        # Add percentage labels
        for bar, val in zip(bars, values):
            self.ax.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2,
                        f'{val:.1f}%', va='center', fontsize=9, fontweight='bold', color='#31302e')
        
        # Add y-axis labels
        self.ax.set_yticks(y_pos)
        self.ax.set_yticklabels(labels, fontsize=9)
        
        # Set limits
        self.ax.set_xlim(0, 105)
        self.ax.set_xlabel('Tỷ Lệ Lấp Đầy (%)', fontsize=10, color='#615d59')
        
        # Style
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        self.ax.spines['left'].set_color('#e0e0e0')
        self.ax.spines['bottom'].set_color('#e0e0e0')
        self.ax.tick_params(colors='#615d59')
        self.ax.invert_yaxis()  # Highest at top
        
        if self.title:
            self.ax.set_title(self.title, fontsize=12, fontweight='bold', pad=10, color='#31302e')
        
        # Add legend
        legend_items = [
            mpatches.Patch(color='#4caf50', label='Thấp (<50%)'),
            mpatches.Patch(color='#ff9800', label='TB (50-75%)'),
            mpatches.Patch(color='#ff5722', label='Cao (75-90%)'),
            mpatches.Patch(color='#f44336', label='Nguy hiểm (>90%)'),
        ]
        self.ax.legend(handles=legend_items, loc='lower right', fontsize=8, frameon=False)
        
        self.fig.tight_layout()
        self.draw()
    
    def update_data(self, data, title=None):
        """Update chart data"""
        self.data = data
        if title:
            self.title = title
        self.plot()


__all__ = ['PieChartCanvas', 'BarChartCanvas', 'FillRateBarChart']
