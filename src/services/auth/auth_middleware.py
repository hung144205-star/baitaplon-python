#!/usr/bin/env python3
"""
Authorization Middleware - Middleware xử lý phân quyền cho ứng dụng
"""
from typing import Optional, Dict, Any
from PyQt6.QtWidgets import QMessageBox

from src.services.auth.authorization_service import (
    AuthorizationService, has_permission, get_menu_items_for_role,
    get_button_permissions_for_role
)


class AuthMiddleware:
    """
    Middleware xử lý phân quyền cho giao diện người dùng
    """
    
    def __init__(self):
        self.auth_service = AuthorizationService()
        self.current_user = None
        self.current_role = None
    
    def set_current_user(self, user_info: Dict[str, Any]):
        """
        Thiết lập người dùng hiện tại
        
        Args:
            user_info: Thông tin người dùng từ login service
        """
        self.current_user = user_info
        self.current_role = user_info.get('vai_tro', 'guest')
    
    def get_current_role(self) -> str:
        """
        Lấy vai trò người dùng hiện tại
        
        Returns:
            str: Vai trò người dùng
        """
        return self.current_role or 'guest'
    
    def check_permission(self, permission: str) -> bool:
        """
        Kiểm tra quyền truy cập
        
        Args:
            permission: Quyền cần kiểm tra
            
        Returns:
            bool: True nếu có quyền
        """
        if not self.current_role:
            return False
        return has_permission(self.current_role, permission)
    
    def filter_menu_items(self) -> list:
        """
        Lọc menu items dựa trên vai trò người dùng
        
        Returns:
            list: Danh sách menu items được phép truy cập
        """
        if not self.current_role:
            return []
        return get_menu_items_for_role(self.current_role)
    
    def get_button_permissions(self, module: str) -> dict:
        """
        Lấy quyền nút chức năng cho module cụ thể
        
        Args:
            module: Tên module (khach_hang, kho, hop_dong, etc.)
            
        Returns:
            dict: Trạng thái các nút chức năng
        """
        if not self.current_role:
            return {}
        return get_button_permissions_for_role(self.current_role, module)
    
    def require_permission(self, permission: str, parent=None):
        """
        Decorator hoặc hàm kiểm tra quyền trước khi thực hiện hành động
        
        Args:
            permission: Quyền cần có
            parent: Widget cha để hiển thị thông báo lỗi
            
        Returns:
            bool: True nếu có quyền, False nếu không
        """
        if not self.check_permission(permission):
            if parent:
                from src.gui.dialogs import MessageDialog
                dialog = MessageDialog(
                    parent,
                    "Quyền truy cập",
                    "Bạn không có quyền thực hiện hành động này.",
                    "warning"
                )
                dialog.exec()
            return False
        return True
    
    def require_role(self, required_role: str, parent=None):
        """
        Kiểm tra vai trò người dùng
        
        Args:
            required_role: Vai trò yêu cầu
            parent: Widget cha để hiển thị thông báo lỗi
            
        Returns:
            bool: True nếu đúng vai trò, False nếu không
        """
        if self.current_role != required_role:
            if parent:
                from src.gui.dialogs import MessageDialog
                dialog = MessageDialog(
                    parent,
                    "Quyền truy cập",
                    f"Chức năng này chỉ dành cho vai trò {required_role}.",
                    "warning"
                )
                dialog.exec()
            return False
        return True


# Global middleware instance
_auth_middleware = None


def get_auth_middleware() -> AuthMiddleware:
    """Lấy instance middleware toàn cục"""
    global _auth_middleware
    if _auth_middleware is None:
        _auth_middleware = AuthMiddleware()
    return _auth_middleware


def set_current_user(user_info: Dict[str, Any]):
    """Thiết lập người dùng hiện tại"""
    middleware = get_auth_middleware()
    middleware.set_current_user(user_info)


def check_permission(permission: str) -> bool:
    """Kiểm tra quyền truy cập"""
    middleware = get_auth_middleware()
    return middleware.check_permission(permission)


def filter_menu_items() -> list:
    """Lọc menu items"""
    middleware = get_auth_middleware()
    return middleware.filter_menu_items()


def get_button_permissions(module: str) -> dict:
    """Lấy quyền nút chức năng"""
    middleware = get_auth_middleware()
    return middleware.get_button_permissions(module)


def require_permission(permission: str, parent=None) -> bool:
    """Yêu cầu quyền truy cập"""
    middleware = get_auth_middleware()
    return middleware.require_permission(permission, parent)


def require_role(required_role: str, parent=None) -> bool:
    """Yêu cầu vai trò cụ thể"""
    middleware = get_auth_middleware()
    return middleware.require_role(required_role, parent)


__all__ = [
    'AuthMiddleware',
    'get_auth_middleware',
    'set_current_user',
    'check_permission',
    'filter_menu_items',
    'get_button_permissions',
    'require_permission',
    'require_role'
]