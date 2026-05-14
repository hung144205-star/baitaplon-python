#!/usr/bin/env python3
"""
Loại Hàng Form - Dialog thêm/sửa loại hàng hóa
"""
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QDialogButtonBox, QFormLayout, QFrame, QTextEdit,
    QListWidget, QListWidgetItem, QPushButton, QWidget
)
from PyQt6.QtCore import Qt, pyqtSignal, QSize
from typing import Optional

from src.services import LoaiHangService
from src.models import LoaiHang
from src.gui.dialogs import MessageDialog


class LoaiHangForm(QDialog):
    """
    Dialog form để thêm/sửa loại hàng hóa
    """

    loai_hang_saved = pyqtSignal(object)

    def __init__(self, parent=None, loai_hang: Optional[LoaiHang] = None):
        super().__init__(parent)
        self.service = LoaiHangService()
        self.loai_hang = loai_hang
        self.is_edit_mode = loai_hang is not None
        self.setup_ui()
        self.setup_connections()

        if self.is_edit_mode:
            self.load_data()
            self.setWindowTitle("✏️ Chỉnh sửa loại hàng")
        else:
            self.setWindowTitle("➕ Thêm loại hàng mới")

    def setup_ui(self):
        """Setup UI"""
        self.setMinimumWidth(450)
        self.setModal(True)

        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(20, 20, 20, 20)

        # Title
        title = QLabel("📂 THÔNG TIN LOẠI HÀNG" if self.is_edit_mode else "📂 THÊM LOẠI HÀNG MỚI")
        title.setStyleSheet("""
            QLabel {
                font-size: 20px;
                font-weight: 700;
                color: #31302e;
                padding: 10px 0;
            }
        """)
        layout.addWidget(title)

        # Form container
        form_container = QFrame()
        form_container.setFrameShape(QFrame.Shape.StyledPanel)
        form_container.setStyleSheet("""
            QFrame {
                background-color: #f6f5f4;
                border-radius: 8px;
                padding: 16px;
            }
        """)

        form_layout = QFormLayout(form_container)
        form_layout.setSpacing(12)

        # Mã loại
        self.ma_loai_input = QLineEdit()
        self.ma_loai_input.setPlaceholderText("Tự động tạo (LH001)")
        if self.is_edit_mode:
            self.ma_loai_input.setReadOnly(True)
            self.ma_loai_input.setStyleSheet("""
                QLineEdit {
                    background-color: #e0e0e0;
                    padding: 8px;
                    border-radius: 4px;
                    border: 1px solid #bdbdbd;
                }
            """)
        else:
            self.ma_loai_input.setStyleSheet("""
                QLineEdit {
                    padding: 8px;
                    border-radius: 4px;
                    border: 1px solid #bdbdbd;
                }
                QLineEdit:focus {
                    border: 2px solid #1976d2;
                }
            """)
        form_layout.addRow("Mã loại:", self.ma_loai_input)

        # Tên loại
        self.ten_loai_input = QLineEdit()
        self.ten_loai_input.setPlaceholderText("VD: Điện tử, May mặc, Thực phẩm...")
        self.ten_loai_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border-radius: 4px;
                border: 1px solid #bdbdbd;
            }
            QLineEdit:focus {
                border: 2px solid #1976d2;
            }
        """)
        form_layout.addRow("Tên loại:", self.ten_loai_input)

        # Mô tả
        self.mo_ta_input = QTextEdit()
        self.mo_ta_input.setPlaceholderText("Mô tả chi tiết về loại hàng...")
        self.mo_ta_input.setMaximumHeight(80)
        self.mo_ta_input.setStyleSheet("""
            QTextEdit {
                padding: 8px;
                border-radius: 4px;
                border: 1px solid #bdbdbd;
            }
            QTextEdit:focus {
                border: 2px solid #1976d2;
            }
        """)
        form_layout.addRow("Mô tả:", self.mo_ta_input)

        # Ghi chú
        self.ghi_chu_input = QTextEdit()
        self.ghi_chu_input.setPlaceholderText("Ghi chú khác (tùy chọn)...")
        self.ghi_chu_input.setMaximumHeight(60)
        self.ghi_chu_input.setStyleSheet("""
            QTextEdit {
                padding: 8px;
                border-radius: 4px;
                border: 1px solid #bdbdbd;
            }
            QTextEdit:focus {
                border: 2px solid #1976d2;
            }
        """)
        form_layout.addRow("Ghi chú:", self.ghi_chu_input)

        layout.addWidget(form_container)

        # Buttons
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save |
            QDialogButtonBox.StandardButton.Cancel
        )
        button_box.button(QDialogButtonBox.StandardButton.Save).setText("💾 Lưu")
        button_box.button(QDialogButtonBox.StandardButton.Cancel).setText("❌ Hủy")
        button_box.setStyleSheet("""
            QPushButton {
                padding: 10px 20px;
                border-radius: 6px;
                font-weight: 600;
                font-size: 14px;
            }
            QPushButton[objectName="applyButton"] {
                background-color: #1976d2;
                color: white;
            }
            QPushButton[objectName="applyButton"]:hover {
                background-color: #1565c0;
            }
            QPushButton[objectName="rejectButton"] {
                background-color: #757575;
                color: white;
            }
            QPushButton[objectName="rejectButton"]:hover {
                background-color: #616161;
            }
        """)
        layout.addWidget(button_box)

        self.save_button = button_box.button(QDialogButtonBox.StandardButton.Save)
        self.cancel_button = button_box.button(QDialogButtonBox.StandardButton.Cancel)

        self.save_button.clicked.connect(self._on_save)
        self.cancel_button.clicked.connect(self.reject)

    def setup_connections(self):
        """Setup signal connections"""
        self.ten_loai_input.textChanged.connect(self._validate_form)

    def load_data(self):
        """Load existing data into form"""
        if not self.loai_hang:
            return

        self.ma_loai_input.setText(self.loai_hang.ma_loai)
        self.ten_loai_input.setText(self.loai_hang.ten_loai)
        if self.loai_hang.mo_ta:
            self.mo_ta_input.setPlainText(self.loai_hang.mo_ta)
        if self.loai_hang.ghi_chu:
            self.ghi_chu_input.setPlainText(self.loai_hang.ghi_chu)

    def _validate_form(self) -> bool:
        """Validate form fields"""
        ten_loai = self.ten_loai_input.text().strip()

        if not ten_loai:
            self.save_button.setEnabled(False)
            return False

        self.save_button.setEnabled(True)
        return True

    def _on_save(self):
        """Handle save button click"""
        ten_loai = self.ten_loai_input.text().strip()
        if not ten_loai:
            MessageDialog.warning(self, "Cảnh báo", "Vui lòng nhập tên loại hàng")
            self.ten_loai_input.setFocus()
            return

        try:
            data = {
                'ten_loai': ten_loai,
                'mo_ta': self.mo_ta_input.toPlainText().strip() or None,
                'ghi_chu': self.ghi_chu_input.toPlainText().strip() or None
            }

            if self.is_edit_mode:
                data['ma_loai'] = self.ma_loai_input.text().strip()
                loai_hang = self.service.update(self.loai_hang.ma_loai, data)
                MessageDialog.success(self, "Thành công", f"Đã cập nhật loại hàng {loai_hang.ten_loai}")
            else:
                ma_loai = self.ma_loai_input.text().strip()
                if ma_loai:
                    data['ma_loai'] = ma_loai
                loai_hang = self.service.create(data)
                MessageDialog.success(self, "Thành công", f"Đã thêm loại hàng {loai_hang.ten_loai}")

            self.loai_hang_saved.emit(loai_hang)
            self.accept()

        except ValueError as e:
            MessageDialog.error(self, "Lỗi", str(e))
        except Exception as e:
            MessageDialog.error(self, "Lỗi", f"Không thể lưu loại hàng:\n{str(e)}")


class LoaiHangManagerDialog(QDialog):
    """
    Dialog quản lý danh sách loại hàng - Add, Edit, Delete
    """

    loai_hang_changed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.service = LoaiHangService()
        self.current_loai_hang = None
        self.setup_ui()
        self.load_data()

    def setup_ui(self):
        """Setup UI"""
        self.setWindowTitle("📂 Quản lý Loại Hàng Hóa")
        self.setMinimumWidth(600)
        self.setMinimumHeight(450)
        self.setModal(True)

        self.setStyleSheet("""
            QDialog {
                background-color: #ffffff;
            }
            QLabel {
                color: #31302e;
            }
            QPushButton {
                padding: 8px 16px;
                border-radius: 6px;
                font-weight: 600;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(20, 20, 20, 20)

        # Header
        header = QLabel("📂 QUẢN LÝ LOẠI HÀNG HÓA")
        header.setStyleSheet("""
            QLabel {
                font-size: 20px;
                font-weight: 700;
                color: #31302e;
            }
        """)
        layout.addWidget(header)

        # Description
        desc = QLabel("Thêm, sửa, xóa các loại hàng hóa trong hệ thống")
        desc.setStyleSheet("font-size: 13px; color: #615d59;")
        layout.addWidget(desc)

        # Button row
        btn_row = QHBoxLayout()
        btn_row.setSpacing(12)

        self.add_btn = QPushButton("➕ Thêm mới")
        self.add_btn.setStyleSheet("""
            QPushButton {
                background-color: #4caf50;
                color: white;
                border: none;
            }
            QPushButton:hover {
                background-color: #43a047;
            }
        """)
        self.add_btn.clicked.connect(self._on_add)

        self.edit_btn = QPushButton("✏️ Sửa")
        self.edit_btn.setEnabled(False)
        self.edit_btn.setStyleSheet("""
            QPushButton {
                background-color: #1976d2;
                color: white;
                border: none;
            }
            QPushButton:hover {
                background-color: #1565c0;
            }
            QPushButton:disabled {
                background-color: #bdbdbd;
            }
        """)
        self.edit_btn.clicked.connect(self._on_edit)

        self.delete_btn = QPushButton("🗑️ Xóa")
        self.delete_btn.setEnabled(False)
        self.delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                border: none;
            }
            QPushButton:hover {
                background-color: #d32f2f;
            }
            QPushButton:disabled {
                background-color: #bdbdbd;
            }
        """)
        self.delete_btn.clicked.connect(self._on_delete)

        self.refresh_btn = QPushButton("🔄 Làm mới")
        self.refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #ff9800;
                color: white;
                border: none;
            }
            QPushButton:hover {
                background-color: #f57c00;
            }
        """)
        self.refresh_btn.clicked.connect(self.load_data)

        btn_row.addWidget(self.add_btn)
        btn_row.addWidget(self.edit_btn)
        btn_row.addWidget(self.delete_btn)
        btn_row.addStretch()
        btn_row.addWidget(self.refresh_btn)
        layout.addLayout(btn_row)

        # List widget for categories
        from PyQt6.QtWidgets import QListWidget, QListWidgetItem

        self.list_widget = QListWidget()
        self.list_widget.setSpacing(2)
        self.list_widget.itemClicked.connect(self._on_item_clicked)
        self.list_widget.itemDoubleClicked.connect(self._on_edit)
        layout.addWidget(self.list_widget, 1)

        # Close button
        close_btn = QPushButton("Đóng")
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #757575;
                color: white;
                border: none;
                padding: 12px 24px;
            }
            QPushButton:hover {
                background-color: #616161;
            }
        """)
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)

    def load_data(self):
        """Load categories from database"""
        self.list_widget.clear()

        try:
            loai_hangs = self.service.get_all(limit=100)

            for lh in loai_hangs:
                item = QListWidgetItem()
                item.setData(Qt.ItemDataRole.UserRole, lh.ma_loai)
                self.list_widget.addItem(item)

                # Create a simple widget with hbox layout for horizontal display
                w = QWidget()
                h = QHBoxLayout(w)
                h.setContentsMargins(10, 8, 10, 8)
                h.setSpacing(20)

                name = QLabel(f"{lh.ten_loai}")
                name.setMinimumWidth(150)
                h.addWidget(name)

                code = QLabel(f"({lh.ma_loai})")
                code.setStyleSheet("color: #888;")
                h.addWidget(code)

                if lh.mo_ta:
                    desc = QLabel(lh.mo_ta)
                    desc.setWordWrap(True)
                    h.addWidget(desc, 1)
                else:
                    h.addStretch(1)

                self.list_widget.setItemWidget(item, w)

            if not loai_hangs:
                self.list_widget.addItem("Chua co loai hang nao. Click 'Them moi' de tao.")

            if not loai_hangs:
                self.list_widget.addItem("Chưa có loại hàng nào. Click 'Thêm mới' để tạo.")

        except Exception as e:
            from src.gui.dialogs import MessageDialog
            MessageDialog.error(self, "Lỗi", f"Không thể tải danh sách loại hàng:\n{str(e)}")

    def _on_item_clicked(self, item: QListWidgetItem):
        """Handle item selection"""
        ma_loai = item.data(Qt.ItemDataRole.UserRole)
        if ma_loai:
            self.current_loai_hang = self.service.get_by_id(ma_loai)
            self.edit_btn.setEnabled(True)
            self.delete_btn.setEnabled(True)
        else:
            self.current_loai_hang = None
            self.edit_btn.setEnabled(False)
            self.delete_btn.setEnabled(False)

    def _on_add(self):
        """Handle add button click"""
        dialog = LoaiHangForm(self)
        dialog.loai_hang_saved.connect(lambda lh: self._on_saved(lh, is_new=True))
        dialog.exec()

    def _on_edit(self):
        """Handle edit button click"""
        if not self.current_loai_hang:
            return

        dialog = LoaiHangForm(self, loai_hang=self.current_loai_hang)
        dialog.loai_hang_saved.connect(lambda lh: self._on_saved(lh, is_new=False))
        dialog.exec()

    def _on_delete(self):
        """Handle delete button click"""
        if not self.current_loai_hang:
            return

        from src.gui.dialogs import ConfirmDialog
        confirmed = ConfirmDialog.ask_delete(
            self,
            f"{self.current_loai_hang.ten_loai} ({self.current_loai_hang.ma_loai})"
        )

        if confirmed:
            try:
                self.service.delete(self.current_loai_hang.ma_loai)
                self.loai_hang_changed.emit()
                self.load_data()
                self.current_loai_hang = None
                self.edit_btn.setEnabled(False)
                self.delete_btn.setEnabled(False)
                from src.gui.dialogs import MessageDialog
                MessageDialog.success(self, "Thành công", "Đã xóa loại hàng")
            except Exception as e:
                from src.gui.dialogs import MessageDialog
                MessageDialog.error(self, "Lỗi", f"Không thể xóa loại hàng:\n{str(e)}")

    def _on_saved(self, loai_hang, is_new: bool):
        """Handle saved event"""
        self.loai_hang_changed.emit()
        self.load_data()


__all__ = ['LoaiHangForm', 'LoaiHangManagerDialog']