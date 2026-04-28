#!/usr/bin/env python3
"""
User View - Giao diện quản lý người dùng
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QComboBox, QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSignal

from src.services.users.user_service import UserService
from src.models import NhanVien, TrangThaiNhanVienEnum
from src.gui.widgets import DataTableWithToolbar
from src.gui.dialogs import MessageDialog, ConfirmDialog
from src.gui.forms.users.user_form import UserForm
from src.services.auth.auth_middleware import require_permission


class UserView(QWidget):
    """
    Giao diện Quản lý Người dùng
    """
    
    # Signals
    user_selected = pyqtSignal(object)  # NhanVien object
    user_added = pyqtSignal(object)     # NhanVien object  
    user_updated = pyqtSignal(object)   # NhanVien object
    user_deleted = pyqtSignal(str)      # ma_nhan_vien
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.user_service = UserService()
        self.current_user: NhanVien = None
        self.setup_ui()
        self.setup_connections()
        self.load_data()
    
    def setup_ui(self):
        """Setup UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)
        
        # Title
        title = QLabel("👤 QUẢN LÝ NGƯỜI DÙNG")
        title.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: #1976d2;
                padding: 10px 0;
            }
        """)
        layout.addWidget(title)
        
        # Data table with toolbar
        self.table_with_toolbar = DataTableWithToolbar(
            headers=["Mã NV", "Họ tên", "Email", "SĐT", "Vai trò", "Trạng thái"]
        )
        layout.addWidget(self.table_with_toolbar, 1)
        
        # Info label
        self.info_label = QLabel("Đang tải dữ liệu...")
        self.info_label.setStyleSheet("color: #666; font-style: italic;")
        layout.addWidget(self.info_label)
    
    def setup_connections(self):
        """Setup signal connections"""
        self.table_with_toolbar.row_selected.connect(self._on_row_selected)
        self.table_with_toolbar.row_double_clicked.connect(self._on_row_double_clicked)
        self.table_with_toolbar.add_clicked.connect(self._on_add_clicked)
        self.table_with_toolbar.edit_clicked.connect(self._on_edit_clicked)
        self.table_with_toolbar.delete_clicked.connect(self._on_delete_clicked)
        self.table_with_toolbar.refresh_clicked.connect(self._on_refresh_clicked)
    
    def load_data(self):
        """Load data from database"""
        try:
            users = self.user_service.get_all_users()
            
            # Format data for table
            table_data = []
            for user in users:
                table_data.append({
                    'Mã NV': user.ma_nhan_vien,
                    'Họ tên': user.ho_ten,
                    'Email': user.email,
                    'SĐT': user.so_dien_thoai or '',
                    'Vai trò': self._format_role(user.vai_tro),
                    'Trạng thái': self._format_status(user.trang_thai)
                })
            
            self.table_with_toolbar.set_data(table_data)
            self.info_label.setText(f"Tổng số người dùng: {len(users)}")
            
        except Exception as e:
            MessageDialog(
                self,
                "Lỗi",
                f"Không thể tải dữ liệu người dùng:\n{str(e)}",
                "error"
            ).exec()
    
    def _format_role(self, role: str) -> str:
        """Format role for display"""
        role_mapping = {
            'admin': 'Admin',
            'manager': 'Quản lý',
            'staff': 'Nhân viên', 
            'guest': 'Khách'
        }
        return role_mapping.get(role, role)
    
    def _format_status(self, status) -> str:
        """Format status for display"""
        if hasattr(status, 'value'):
            status_value = status.value
        else:
            status_value = status
        
        status_mapping = {
            TrangThaiNhanVienEnum.HOAT_DONG.value: 'Hoạt động',
            TrangThaiNhanVienEnum.NGUNG_HOAT_DONG.value: 'Ngừng hoạt động'
        }
        return status_mapping.get(status_value, str(status_value))
    
    def _on_row_selected(self, row_idx: int, row_data: dict):
        """Handle row selection"""
        ma_nhan_vien = row_data.get('Mã NV')
        if ma_nhan_vien:
            user = self.user_service.get_user_by_id(ma_nhan_vien)
            if user:
                self.current_user = user
                self.user_selected.emit(user)
    
    def _on_row_double_clicked(self, row_idx: int, row_data: dict):
        """Handle row double click"""
        self._on_edit_clicked()
    
    @require_permission('create_user')
    def _on_add_clicked(self):
        """Handle add button click"""
        form = UserForm(parent=self)
        form.user_saved.connect(self._on_user_saved)
        form.exec()
    
    @require_permission('edit_user')
    def _on_edit_clicked(self):
        """Handle edit button click"""
        if not self.current_user:
            MessageDialog(
                self,
                "Cảnh báo",
                "Vui lòng chọn người dùng cần chỉnh sửa.",
                "warning"
            ).exec()
            return
        
        form = UserForm(parent=self, user=self.current_user)
        form.user_saved.connect(self._on_user_saved)
        form.exec()
    
    @require_permission('delete_user')
    def _on_delete_clicked(self):
        """Handle delete button click"""
        if not self.current_user:
            MessageDialog(
                self,
                "Cảnh báo", 
                "Vui lòng chọn người dùng cần xóa.",
                "warning"
            ).exec()
            return
        
        # Prevent deleting current logged-in user (would need session context)
        # For now, just confirm deletion
        confirmed = ConfirmDialog.show_confirm(
            self,
            "Xác nhận xóa",
            f"Bạn có chắc muốn xóa người dùng '{self.current_user.ho_ten}'?\n"
            f"Mã nhân viên: {self.current_user.ma_nhan_vien}\n\n"
            "Thao tác này sẽ ngừng hoạt động tài khoản (không thể khôi phục)."
        )
        
        if confirmed:
            try:
                success = self.user_service.delete_user(self.current_user.ma_nhan_vien)
                if success:
                    MessageDialog(
                        self,
                        "Thành công",
                        f"Đã xóa người dùng '{self.current_user.ho_ten}'",
                        "success"
                    ).exec()
                    self.load_data()
                    self.user_deleted.emit(self.current_user.ma_nhan_vien)
                else:
                    MessageDialog(
                        self,
                        "Lỗi",
                        "Không thể xóa người dùng.",
                        "error"
                    ).exec()
            except Exception as e:
                MessageDialog(
                    self,
                    "Lỗi",
                    f"Không thể xóa người dùng:\n{str(e)}",
                    "error"
                ).exec()
    
    def _on_refresh_clicked(self):
        """Handle refresh button click"""
        self.load_data()
    
    def _on_user_saved(self, user: NhanVien):
        """Handle user saved from form"""
        self.load_data()
        if self.is_edit_mode:
            self.user_updated.emit(user)
        else:
            self.user_added.emit(user)


# Add static method to ConfirmDialog if not exists
def show_confirm(parent, title: str, message: str) -> bool:
    """Show confirmation dialog"""
    dialog = ConfirmDialog(parent, title, message)
    return dialog.exec() == QMessageBox.StandardButton.Yes


# Patch ConfirmDialog if needed
if not hasattr(ConfirmDialog, 'show_confirm'):
    ConfirmDialog.show_confirm = staticmethod(show_confirm)


__all__ = ['UserView']