#!/usr/bin/env python3
"""
Data Table Widget - QTableWidget wrapper với sorting, filtering, pagination
"""
from PyQt6.QtWidgets import (
    QTableWidget, QTableWidgetItem, QHeaderView, QHBoxLayout,
    QVBoxLayout, QWidget, QLineEdit, QPushButton, QLabel,
    QComboBox, QSpinBox, QFrame, QMenu, QCheckBox
)
from PyQt6.QtCore import Qt, pyqtSignal, QSortFilterProxyModel
from PyQt6.QtGui import QAction


class DataTable(QTableWidget):
    """
    Enhanced QTableWidget với features:
    - Sorting by clicking headers
    - Filtering/Search
    - Pagination
    - Row selection
    - Context menu
    - Export support
    """
    
    # Signals
    row_selected = pyqtSignal(int, dict)  # row_index, row_data
    row_double_clicked = pyqtSignal(int, dict)
    context_menu_requested = pyqtSignal(int, list)  # row_index, actions
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.setup_connections()
        
        # Data storage
        self._data = []
        self._headers = []
        self._sort_column = -1
        self._sort_order = Qt.SortOrder.AscendingOrder
        
        # Pagination
        self.current_page = 1
        self.page_size = 20
        self.total_pages = 1
    
    def setup_ui(self):
        """Setup UI"""
        self.setStyleSheet("""
            QTableWidget {
                background-color: #ffffff;
                alternate-background-color: #fafafa;
                border: 1px solid rgba(0, 0, 0, 0.1);
                border-radius: 8px;
                gridline-color: rgba(0, 0, 0, 0.05);
                selection-background-color: #e3f2fd;
                selection-color: #1976d2;
            }
            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid rgba(0, 0, 0, 0.05);
            }
            QTableWidget::item:hover {
                background-color: #f6f5f4;
            }
            QTableWidget::item:selected {
                background-color: #e3f2fd;
                color: #1976d2;
            }
            QHeaderView::section {
                background-color: #f6f5f4;
                color: #31302e;
                border: none;
                border-bottom: 1px solid rgba(0, 0, 0, 0.1);
                border-right: 1px solid rgba(0, 0, 0, 0.05);
                padding: 10px 12px;
                font-weight: 600;
                font-size: 13px;
            }
            QHeaderView::section:first {
                border-top-left-radius: 8px;
            }
            QHeaderView::section:last {
                border-top-right-radius: 8px;
                border-right: none;
            }
            QHeaderView::section:hover {
                background-color: #eeeeee;
            }
        """)
        
        # Enable sorting
        self.setSortingEnabled(True)
        
        # Selection mode
        self.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        
        # Alternating row colors
        self.setAlternatingRowColors(True)
        
        # Header configuration
        header = self.horizontalHeader()
        header.setStretchLastSection(True)
        header.setDefaultAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        
        # Hide vertical header
        self.verticalHeader().setVisible(False)
        
        # Enable context menu
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
    
    def setup_connections(self):
        """Setup signal connections"""
        self.cellDoubleClicked.connect(self._on_cell_double_clicked)
        self.customContextMenuRequested.connect(self._on_context_menu)
        self.itemSelectionChanged.connect(self._on_selection_changed)
    
    def set_data(self, data: list, headers: list = None):
        """
        Set table data
        
        Args:
            data: List of dicts
            headers: List of column headers (optional, will use dict keys if not provided)
        """
        if not data:
            self.clear()
            return
        
        self._data = data
        
        # Set headers
        if headers:
            self._headers = headers
        else:
            # Extract headers from first row
            self._headers = list(data[0].keys())
        
        # Set column count
        self.setColumnCount(len(self._headers))
        self.setHorizontalHeaderLabels(self._headers)
        
        # Set row count
        self.setRowCount(len(data))
        
        # Populate data
        for row_idx, row_data in enumerate(data):
            for col_idx, header in enumerate(self._headers):
                value = row_data.get(header, '')
                item = QTableWidgetItem(str(value))
                item.setData(Qt.ItemDataRole.UserRole, row_data)  # Store full row data
                self.setItem(row_idx, col_idx, item)
        
        # Auto-resize columns
        self.resizeColumnsToContents()
        
        # Update pagination
        self.update_pagination()
    
    def add_row(self, row_data: dict):
        """Add a single row"""
        self._data.append(row_data)
        row_idx = self.rowCount()
        self.setRowCount(row_idx + 1)
        
        for col_idx, header in enumerate(self._headers):
            value = row_data.get(header, '')
            item = QTableWidgetItem(str(value))
            item.setData(Qt.ItemDataRole.UserRole, row_data)
            self.setItem(row_idx, col_idx, item)
        
        self.update_pagination()
    
    def update_row(self, row_idx: int, row_data: dict):
        """Update a row"""
        if 0 <= row_idx < self.rowCount():
            self._data[row_idx] = row_data
            
            for col_idx, header in enumerate(self._headers):
                value = row_data.get(header, '')
                item = self.item(row_idx, col_idx)
                if item:
                    item.setText(str(value))
                    item.setData(Qt.ItemDataRole.UserRole, row_data)
    
    def delete_row(self, row_idx: int):
        """Delete a row"""
        if 0 <= row_idx < self.rowCount():
            self.removeRow(row_idx)
            if row_idx < len(self._data):
                self._data.pop(row_idx)
            self.update_pagination()
    
    def get_selected_row(self) -> dict:
        """Get selected row data"""
        selected = self.selectedItems()
        if selected:
            row_idx = selected[0].row()
            item = self.item(row_idx, 0)
            if item:
                return item.data(Qt.ItemDataRole.UserRole)
        return {}
    
    def get_selected_row_index(self) -> int:
        """Get selected row index"""
        selected = self.selectedItems()
        if selected:
            return selected[0].row()
        return -1
    
    def clear_selection(self):
        """Clear selection"""
        self.clearSelection()
    
    def clear_data(self):
        """Clear all data"""
        self.clear()
        self.setRowCount(0)
        self._data = []
        self.update_pagination()
    
    def filter_data(self, search_text: str, column: int = -1):
        """
        Filter data based on search text
        
        Args:
            search_text: Text to search
            column: Column to search (-1 for all columns)
        """
        search_text = search_text.lower().strip()
        
        if not search_text:
            # Show all rows
            for row in range(self.rowCount()):
                self.setRowHidden(row, False)
            return
        
        # Hide/show rows based on search
        for row in range(self.rowCount()):
            show_row = False
            
            if column >= 0:
                # Search in specific column
                item = self.item(row, column)
                if item and search_text in item.text().lower():
                    show_row = True
            else:
                # Search in all columns
                for col in range(self.columnCount()):
                    item = self.item(row, col)
                    if item and search_text in item.text().lower():
                        show_row = True
                        break
            
            self.setRowHidden(row, not show_row)
    
    def sort_by_column(self, column: int, order: Qt.SortOrder = Qt.SortOrder.AscendingOrder):
        """Sort by column"""
        self.sortItems(column, order)
        self._sort_column = column
        self._sort_order = order
    
    def update_pagination(self):
        """Update pagination info (for external use)"""
        total_rows = len(self._data)
        self.total_pages = max(1, (total_rows + self.page_size - 1) // self.page_size)
    
    def _on_cell_double_clicked(self, row: int, column: int):
        """Handle cell double click"""
        item = self.item(row, 0)
        if item:
            row_data = item.data(Qt.ItemDataRole.UserRole)
            self.row_double_clicked.emit(row, row_data)
    
    def _on_context_menu(self, pos):
        """Handle context menu"""
        row = self.rowAt(pos.y())
        if row >= 0:
            item = self.item(row, 0)
            row_data = item.data(Qt.ItemDataRole.UserRole) if item else {}
            actions = ['view', 'edit', 'delete']
            self.context_menu_requested.emit(row, actions)
    
    def _on_selection_changed(self):
        """Handle selection change"""
        row_idx = self.get_selected_row_index()
        if row_idx >= 0:
            row_data = self.get_selected_row()
            self.row_selected.emit(row_idx, row_data)
    
    def set_page_size(self, size: int):
        """Set page size"""
        self.page_size = size
        self.update_pagination()


class DataTableWithToolbar(QWidget):
    """
    DataTable với toolbar (search, filter, actions)
    """
    
    row_selected = pyqtSignal(int, dict)
    row_double_clicked = pyqtSignal(int, dict)
    add_clicked = pyqtSignal()
    edit_clicked = pyqtSignal()
    delete_clicked = pyqtSignal()
    refresh_clicked = pyqtSignal()
    export_clicked = pyqtSignal()
    
    def __init__(self, parent=None, headers: list = None):
        super().__init__(parent)
        self.headers = headers or []
        self.setup_ui()
        self.setup_connections()
    
    def setup_ui(self):
        """Setup UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)
        
        # Toolbar
        toolbar = self._create_toolbar()
        layout.addWidget(toolbar)
        
        # Table
        self.table = DataTable()
        if self.headers:
            self.table._headers = self.headers
        layout.addWidget(self.table, 1)
        
        # Pagination
        pagination = self._create_pagination()
        layout.addWidget(pagination)
    
    def _create_toolbar(self) -> QWidget:
        """Create toolbar"""
        self.toolbar = QWidget()
        layout = QHBoxLayout(self.toolbar)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)
        
        # Search box
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Tìm kiếm...")
        self.search_input.setStyleSheet("""
            QLineEdit {
                padding: 8px 12px;
                border: 1px solid rgba(0, 0, 0, 0.2);
                border-radius: 4px;
                min-width: 250px;
            }
            QLineEdit:focus {
                border-color: #1976d2;
            }
        """)
        layout.addWidget(self.search_input)
        
        # Column filter
        self.column_filter = QComboBox()
        self.column_filter.addItem("Tất cả cột", -1)
        layout.addWidget(self.column_filter)
        
        # Spacer
        layout.addStretch()
        
        # Action buttons
        self.add_btn = QPushButton("➕ Thêm")
        self.add_btn.setObjectName("actionButton")
        layout.addWidget(self.add_btn)
        
        self.edit_btn = QPushButton("✏️ Sửa")
        self.edit_btn.setStyleSheet("""
            QPushButton {
                background-color: #f6f5f4;
                color: #31302e;
                border: 1px solid rgba(0, 0, 0, 0.1);
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #eeeeee;
            }
        """)
        layout.addWidget(self.edit_btn)
        
        self.delete_btn = QPushButton("🗑️ Xóa")
        self.delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #f6f5f4;
                color: #d32f2f;
                border: 1px solid rgba(0, 0, 0, 0.1);
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #ffebee;
            }
        """)
        layout.addWidget(self.delete_btn)
        
        self.refresh_btn = QPushButton("🔄 Làm mới")
        self.refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #f6f5f4;
                color: #31302e;
                border: 1px solid rgba(0, 0, 0, 0.1);
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #eeeeee;
            }
        """)
        layout.addWidget(self.refresh_btn)
        
        self.export_btn = QPushButton("📊 Xuất Excel")
        self.export_btn.setStyleSheet("""
            QPushButton {
                background-color: #1976d2;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #1565c0;
            }
        """)
        layout.addWidget(self.export_btn)
        
        return self.toolbar
    
    def _create_pagination(self) -> QWidget:
        """Create pagination controls"""
        pagination = QWidget()
        layout = QHBoxLayout(pagination)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)
        
        # Info label
        self.page_info = QLabel("Trang 1 / 1 (0 rows)")
        layout.addWidget(self.page_info)
        
        # Page size
        layout.addWidget(QLabel("Số dòng:"))
        self.page_size_combo = QComboBox()
        self.page_size_combo.addItems(["10", "20", "50", "100"])
        self.page_size_combo.setCurrentText("20")
        layout.addWidget(self.page_size_combo)
        
        # Page controls
        self.prev_btn = QPushButton("◀ Trước")
        self.prev_btn.setEnabled(False)
        layout.addWidget(self.prev_btn)
        
        self.page_spin = QSpinBox()
        self.page_spin.setMinimum(1)
        self.page_spin.setMaximum(1)
        layout.addWidget(self.page_spin)
        
        self.next_btn = QPushButton("Sau ▶")
        self.next_btn.setEnabled(False)
        layout.addWidget(self.next_btn)
        
        layout.addStretch()
        
        return pagination
    
    def setup_connections(self):
        """Setup signal connections"""
        # Table signals
        self.table.row_selected.connect(self.row_selected.emit)
        self.table.row_double_clicked.connect(self.row_double_clicked.emit)
        
        # Toolbar signals
        self.search_input.textChanged.connect(self._on_search_changed)
        self.add_btn.clicked.connect(self.add_clicked.emit)
        self.edit_btn.clicked.connect(self.edit_clicked.emit)
        self.delete_btn.clicked.connect(self.delete_clicked.emit)
        self.refresh_btn.clicked.connect(self.refresh_clicked.emit)
        self.export_btn.clicked.connect(self.export_clicked.emit)
        
        # Pagination signals
        self.page_size_combo.currentTextChanged.connect(self._on_page_size_changed)
        self.prev_btn.clicked.connect(self._on_prev_page)
        self.next_btn.clicked.connect(self._on_next_page)
        self.page_spin.valueChanged.connect(self._on_page_changed)
    
    def set_data(self, data: list, headers: list = None):
        """Set table data"""
        if headers:
            self.headers = headers
            self.table._headers = headers
            
            # Update column filter
            self.column_filter.clear()
            self.column_filter.addItem("Tất cả cột", -1)
            for i, header in enumerate(headers):
                self.column_filter.addItem(header, i)
        
        self.table.set_data(data, headers)
        self._update_pagination_info()
    
    def get_selected_row(self) -> dict:
        """Get selected row"""
        return self.table.get_selected_row()
    
    def _on_search_changed(self, text: str):
        """Handle search"""
        column = self.column_filter.currentData()
        self.table.filter_data(text, column)
    
    def _on_page_size_changed(self, text: str):
        """Handle page size change"""
        self.table.set_page_size(int(text))
        self._update_pagination_info()
    
    def _on_prev_page(self):
        """Go to previous page"""
        if self.page_spin.value() > 1:
            self.page_spin.setValue(self.page_spin.value() - 1)
    
    def _on_next_page(self):
        """Go to next page"""
        if self.page_spin.value() < self.table.total_pages:
            self.page_spin.setValue(self.page_spin.value() + 1)
    
    def _on_page_changed(self, page: int):
        """Handle page change"""
        # Implement pagination logic here
        pass
    
    def _update_pagination_info(self):
        """Update pagination info"""
        total_rows = len(self.table._data)
        self.page_info.setText(f"Tổng: {total_rows} dòng")
        self.page_spin.setMaximum(max(1, self.table.total_pages))


__all__ = ['DataTable', 'DataTableWithToolbar']
