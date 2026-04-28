#!/usr/bin/env python3
"""
Authorization Service - Dịch vụ phân quyền theo vai trò người dùng
"""
from typing import List, Dict, Any, Optional
from enum import Enum

from src.services.auth.auth_service import UserRole


class Permission(Enum):
    """Các quyền truy cập hệ thống"""
    # Customer Management
    VIEW_CUSTOMERS = "view_customers"
    CREATE_CUSTOMER = "create_customer" 
    EDIT_CUSTOMER = "edit_customer"
    DELETE_CUSTOMER = "delete_customer"
    
    # Warehouse Management  
    VIEW_WAREHOUSES = "view_warehouses"
    CREATE_WAREHOUSE = "create_warehouse"
    EDIT_WAREHOUSE = "edit_warehouse"
    DELETE_WAREHOUSE = "delete_warehouse"
    
    # Position Management
    VIEW_POSITIONS = "view_positions"
    CREATE_POSITION = "create_position"
    EDIT_POSITION = "edit_position"
    DELETE_POSITION = "delete_position"
    
    # Contract Management
    VIEW_CONTRACTS = "view_contracts"
    CREATE_CONTRACT = "create_contract"
    EDIT_CONTRACT = "edit_contract"
    DELETE_CONTRACT = "delete_contract"
    RENEW_CONTRACT = "renew_contract"
    TERMINATE_CONTRACT = "terminate_contract"
    
    # Goods Management
    VIEW_GOODS = "view_goods"
    CREATE_GOODS = "create_goods"
    EDIT_GOODS = "edit_goods"
    DELETE_GOODS = "delete_goods"
    
    # Payment Management
    VIEW_PAYMENTS = "view_payments"
    CREATE_PAYMENT = "create_payment"
    EDIT_PAYMENT = "edit_payment"
    
    # Report Management
    VIEW_REPORTS = "view_reports"
    EXPORT_REPORTS = "export_reports"
    
    # User Management
    VIEW_USERS = "view_users"
    CREATE_USER = "create_user"
    EDIT_USER = "edit_user"
    DELETE_USER = "delete_user"
    ASSIGN_ROLES = "assign_roles"
    
    # System Settings
    MANAGE_SETTINGS = "manage_settings"


class AuthorizationService:
    """
    Service xử lý phân quyền theo vai trò
    """
    
    def __init__(self):
        # Define permission matrix for each role
        self.permission_matrix = {
            UserRole.ADMIN.value: [
                Permission.VIEW_CUSTOMERS.value,
                Permission.CREATE_CUSTOMER.value,
                Permission.EDIT_CUSTOMER.value,
                Permission.DELETE_CUSTOMER.value,
                
                Permission.VIEW_WAREHOUSES.value,
                Permission.CREATE_WAREHOUSE.value,
                Permission.EDIT_WAREHOUSE.value,
                Permission.DELETE_WAREHOUSE.value,
                
                Permission.VIEW_POSITIONS.value,
                Permission.CREATE_POSITION.value,
                Permission.EDIT_POSITION.value,
                Permission.DELETE_POSITION.value,
                
                Permission.VIEW_CONTRACTS.value,
                Permission.CREATE_CONTRACT.value,
                Permission.EDIT_CONTRACT.value,
                Permission.DELETE_CONTRACT.value,
                Permission.RENEW_CONTRACT.value,
                Permission.TERMINATE_CONTRACT.value,
                
                Permission.VIEW_GOODS.value,
                Permission.CREATE_GOODS.value,
                Permission.EDIT_GOODS.value,
                Permission.DELETE_GOODS.value,
                
                Permission.VIEW_PAYMENTS.value,
                Permission.CREATE_PAYMENT.value,
                Permission.EDIT_PAYMENT.value,
                
                Permission.VIEW_REPORTS.value,
                Permission.EXPORT_REPORTS.value,
                
                Permission.VIEW_USERS.value,
                Permission.CREATE_USER.value,
                Permission.EDIT_USER.value,
                Permission.DELETE_USER.value,
                Permission.ASSIGN_ROLES.value,
                
                Permission.MANAGE_SETTINGS.value
            ],
            
            UserRole.MANAGER.value: [
                Permission.VIEW_CUSTOMERS.value,
                Permission.CREATE_CUSTOMER.value,
                Permission.EDIT_CUSTOMER.value,
                
                Permission.VIEW_WAREHOUSES.value,
                Permission.CREATE_WAREHOUSE.value,
                Permission.EDIT_WAREHOUSE.value,
                
                Permission.VIEW_POSITIONS.value,
                Permission.CREATE_POSITION.value,
                Permission.EDIT_POSITION.value,
                
                Permission.VIEW_CONTRACTS.value,
                Permission.CREATE_CONTRACT.value,
                Permission.EDIT_CONTRACT.value,
                Permission.RENEW_CONTRACT.value,
                Permission.TERMINATE_CONTRACT.value,
                
                Permission.VIEW_GOODS.value,
                Permission.CREATE_GOODS.value,
                Permission.EDIT_GOODS.value,
                
                Permission.VIEW_PAYMENTS.value,
                Permission.CREATE_PAYMENT.value,
                Permission.EDIT_PAYMENT.value,
                
                Permission.VIEW_REPORTS.value,
                Permission.EXPORT_REPORTS.value
            ],
            
            UserRole.STAFF.value: [
                Permission.VIEW_CUSTOMERS.value,
                Permission.CREATE_CUSTOMER.value,
                
                Permission.VIEW_WAREHOUSES.value,
                Permission.VIEW_POSITIONS.value,
                
                Permission.VIEW_CONTRACTS.value,
                Permission.CREATE_CONTRACT.value,
                
                Permission.VIEW_GOODS.value,
                Permission.CREATE_GOODS.value,
                
                Permission.VIEW_PAYMENTS.value,
                Permission.CREATE_PAYMENT.value,
                
                Permission.VIEW_REPORTS.value
            ],
            
            UserRole.GUEST.value: [
                Permission.VIEW_CUSTOMERS.value,
                Permission.VIEW_WAREHOUSES.value,
                Permission.VIEW_POSITIONS.value,
                Permission.VIEW_CONTRACTS.value,
                Permission.VIEW_GOODS.value,
                Permission.VIEW_PAYMENTS.value,
                Permission.VIEW_REPORTS.value
            ]
        }
    
    def has_permission(self, user_role: str, permission: str) -> bool:
        """
        Kiểm tra xem người dùng có quyền thực hiện hành động không
        
        Args:
            user_role: Vai trò người dùng (admin, manager, staff, guest)
            permission: Quyền cần kiểm tra
            
        Returns:
            bool: True nếu có quyền, False nếu không
        """
        if user_role not in self.permission_matrix:
            return False
        
        return permission in self.permission_matrix[user_role]
    
    def get_user_permissions(self, user_role: str) -> List[str]:
        """
        Lấy danh sách tất cả quyền của người dùng theo vai trò
        
        Args:
            user_role: Vai trò người dùng
            
        Returns:
            List[str]: Danh sách quyền
        """
        return self.permission_matrix.get(user_role, [])
    
    def get_menu_items_for_role(self, user_role: str) -> List[Dict[str, Any]]:
        """
        Lấy danh sách menu items cho vai trò cụ thể
        
        Args:
            user_role: Vai trò người dùng
            
        Returns:
            List[Dict]: Danh sách menu items với cấu trúc:
                {
                    'name': str,
                    'icon': str, 
                    'route': str,
                    'permissions': List[str]
                }
        """
        menu_config = [
            {
                'name': 'Khách hàng',
                'icon': '👥',
                'route': 'khach_hang',
                'permissions': [Permission.VIEW_CUSTOMERS.value]
            },
            {
                'name': 'Kho hàng',
                'icon': '🏭',
                'route': 'kho',
                'permissions': [Permission.VIEW_WAREHOUSES.value]
            },
            {
                'name': 'Hợp đồng',
                'icon': '📋',
                'route': 'hop_dong', 
                'permissions': [Permission.VIEW_CONTRACTS.value]
            },
            {
                'name': 'Hàng hóa',
                'icon': '📦',
                'route': 'hang_hoa',
                'permissions': [Permission.VIEW_GOODS.value]
            },
            {
                'name': 'Thanh toán',
                'icon': '💰',
                'route': 'thanh_toan',
                'permissions': [Permission.VIEW_PAYMENTS.value]
            },
            {
                'name': 'Báo cáo',
                'icon': '📊',
                'route': 'bao_cao',
                'permissions': [Permission.VIEW_REPORTS.value]
            },
            {
                'name': 'Người dùng',
                'icon': '👤',
                'route': 'nguoi_dung',
                'permissions': [Permission.VIEW_USERS.value],
                'admin_only': True
            },
            {
                'name': 'Cài đặt',
                'icon': '⚙️',
                'route': 'cai_dat',
                'permissions': [Permission.MANAGE_SETTINGS.value],
                'admin_only': True
            }
        ]
        
        # Filter menu items based on user permissions
        visible_menu = []
        for item in menu_config:
            # Check if user has required permissions
            has_required_perms = all(
                self.has_permission(user_role, perm) 
                for perm in item['permissions']
            )
            
            # Check admin-only restriction
            if item.get('admin_only', False) and user_role != UserRole.ADMIN.value:
                continue
                
            if has_required_perms:
                visible_menu.append(item)
        
        return visible_menu
    
    def get_button_permissions_for_role(self, user_role: str, module: str) -> Dict[str, bool]:
        """
        Lấy trạng thái hiển thị các nút chức năng cho vai trò cụ thể
        
        Args:
            user_role: Vai trò người dùng
            module: Module cụ thể (khach_hang, kho, hop_dong, etc.)
            
        Returns:
            Dict[str, bool]: Trạng thái các nút chức năng
        """
        button_config = {
            'khach_hang': {
                'add': self.has_permission(user_role, Permission.CREATE_CUSTOMER.value),
                'edit': self.has_permission(user_role, Permission.EDIT_CUSTOMER.value),
                'delete': self.has_permission(user_role, Permission.DELETE_CUSTOMER.value),
                'export': self.has_permission(user_role, Permission.EXPORT_REPORTS.value)
            },
            'kho': {
                'add': self.has_permission(user_role, Permission.CREATE_WAREHOUSE.value),
                'edit': self.has_permission(user_role, Permission.EDIT_WAREHOUSE.value),
                'delete': self.has_permission(user_role, Permission.DELETE_WAREHOUSE.value),
                'export': self.has_permission(user_role, Permission.EXPORT_REPORTS.value)
            },
            'vi_tri': {
                'add': self.has_permission(user_role, Permission.CREATE_POSITION.value),
                'edit': self.has_permission(user_role, Permission.EDIT_POSITION.value),
                'delete': self.has_permission(user_role, Permission.DELETE_POSITION.value)
            },
            'hop_dong': {
                'add': self.has_permission(user_role, Permission.CREATE_CONTRACT.value),
                'edit': self.has_permission(user_role, Permission.EDIT_CONTRACT.value),
                'delete': self.has_permission(user_role, Permission.DELETE_CONTRACT.value),
                'renew': self.has_permission(user_role, Permission.RENEW_CONTRACT.value),
                'terminate': self.has_permission(user_role, Permission.TERMINATE_CONTRACT.value),
                'export': self.has_permission(user_role, Permission.EXPORT_REPORTS.value)
            },
            'hang_hoa': {
                'add': self.has_permission(user_role, Permission.CREATE_GOODS.value),
                'edit': self.has_permission(user_role, Permission.EDIT_GOODS.value),
                'delete': self.has_permission(user_role, Permission.DELETE_GOODS.value),
                'export': self.has_permission(user_role, Permission.EXPORT_REPORTS.value)
            },
            'thanh_toan': {
                'add': self.has_permission(user_role, Permission.CREATE_PAYMENT.value),
                'edit': self.has_permission(user_role, Permission.EDIT_PAYMENT.value),
                'export': self.has_permission(user_role, Permission.EXPORT_REPORTS.value)
            },
            'bao_cao': {
                'export': self.has_permission(user_role, Permission.EXPORT_REPORTS.value)
            },
            'nguoi_dung': {
                'add': self.has_permission(user_role, Permission.CREATE_USER.value),
                'edit': self.has_permission(user_role, Permission.EDIT_USER.value),
                'delete': self.has_permission(user_role, Permission.DELETE_USER.value),
                'assign_role': self.has_permission(user_role, Permission.ASSIGN_ROLES.value)
            }
        }
        
        return button_config.get(module, {})
    
    def check_api_access(self, user_role: str, endpoint: str, method: str = 'GET') -> bool:
        """
        Kiểm tra quyền truy cập API endpoint
        
        Args:
            user_role: Vai trò người dùng
            endpoint: API endpoint path
            method: HTTP method (GET, POST, PUT, DELETE)
            
        Returns:
            bool: True nếu có quyền truy cập
        """
        # Map endpoints to permissions
        endpoint_permissions = {
            # Customer endpoints
            '/api/customers': {
                'GET': Permission.VIEW_CUSTOMERS.value,
                'POST': Permission.CREATE_CUSTOMER.value
            },
            '/api/customers/*': {
                'GET': Permission.VIEW_CUSTOMERS.value,
                'PUT': Permission.EDIT_CUSTOMER.value,
                'DELETE': Permission.DELETE_CUSTOMER.value
            },
            
            # Warehouse endpoints
            '/api/warehouses': {
                'GET': Permission.VIEW_WAREHOUSES.value,
                'POST': Permission.CREATE_WAREHOUSE.value
            },
            '/api/warehouses/*': {
                'GET': Permission.VIEW_WAREHOUSES.value,
                'PUT': Permission.EDIT_WAREHOUSE.value,
                'DELETE': Permission.DELETE_WAREHOUSE.value
            },
            
            # Position endpoints  
            '/api/positions': {
                'GET': Permission.VIEW_POSITIONS.value,
                'POST': Permission.CREATE_POSITION.value
            },
            '/api/positions/*': {
                'GET': Permission.VIEW_POSITIONS.value,
                'PUT': Permission.EDIT_POSITION.value,
                'DELETE': Permission.DELETE_POSITION.value
            },
            
            # Contract endpoints
            '/api/contracts': {
                'GET': Permission.VIEW_CONTRACTS.value,
                'POST': Permission.CREATE_CONTRACT.value
            },
            '/api/contracts/*/renew': {
                'POST': Permission.RENEW_CONTRACT.value
            },
            '/api/contracts/*/terminate': {
                'POST': Permission.TERMINATE_CONTRACT.value
            },
            '/api/contracts/*': {
                'GET': Permission.VIEW_CONTRACTS.value,
                'PUT': Permission.EDIT_CONTRACT.value,
                'DELETE': Permission.DELETE_CONTRACT.value
            },
            
            # Goods endpoints
            '/api/goods': {
                'GET': Permission.VIEW_GOODS.value,
                'POST': Permission.CREATE_GOODS.value
            },
            '/api/goods/*': {
                'GET': Permission.VIEW_GOODS.value,
                'PUT': Permission.EDIT_GOODS.value,
                'DELETE': Permission.DELETE_GOODS.value
            },
            
            # Payment endpoints
            '/api/payments': {
                'GET': Permission.VIEW_PAYMENTS.value,
                'POST': Permission.CREATE_PAYMENT.value
            },
            '/api/payments/*': {
                'GET': Permission.VIEW_PAYMENTS.value,
                'PUT': Permission.EDIT_PAYMENT.value
            },
            
            # User endpoints (admin only)
            '/api/users': {
                'GET': Permission.VIEW_USERS.value,
                'POST': Permission.CREATE_USER.value
            },
            '/api/users/*': {
                'GET': Permission.VIEW_USERS.value,
                'PUT': Permission.EDIT_USER.value,
                'DELETE': Permission.DELETE_USER.value
            },
            '/api/users/*/assign-role': {
                'POST': Permission.ASSIGN_ROLES.value
            }
        }
        
        # Find matching endpoint pattern
        for pattern, methods in endpoint_permissions.items():
            if self._matches_endpoint_pattern(endpoint, pattern):
                required_permission = methods.get(method, Permission.VIEW_REPORTS.value)
                return self.has_permission(user_role, required_permission)
        
        # Default: allow read access to reports
        if method == 'GET':
            return self.has_permission(user_role, Permission.VIEW_REPORTS.value)
        
        return False
    
    def _matches_endpoint_pattern(self, endpoint: str, pattern: str) -> bool:
        """
        Kiểm tra xem endpoint có khớp với pattern không
        Hỗ trợ wildcard (*) cho các segment
        """
        if pattern.endswith('/*'):
            base_pattern = pattern[:-2]
            return endpoint.startswith(base_pattern + '/')
        return endpoint == pattern


# Convenience functions
def has_permission(user_role: str, permission: str) -> bool:
    """Kiểm tra quyền truy cập"""
    service = AuthorizationService()
    return service.has_permission(user_role, permission)


def get_menu_items_for_role(user_role: str) -> List[Dict[str, Any]]:
    """Lấy menu items cho vai trò"""
    service = AuthorizationService()
    return service.get_menu_items_for_role(user_role)


def get_button_permissions_for_role(user_role: str, module: str) -> Dict[str, bool]:
    """Lấy quyền nút chức năng cho vai trò"""
    service = AuthorizationService()
    return service.get_button_permissions_for_role(user_role, module)


def check_api_access(user_role: str, endpoint: str, method: str = 'GET') -> bool:
    """Kiểm tra quyền truy cập API"""
    service = AuthorizationService()
    return service.check_api_access(user_role, endpoint, method)


__all__ = [
    'AuthorizationService',
    'Permission',
    'has_permission',
    'get_menu_items_for_role', 
    'get_button_permissions_for_role',
    'check_api_access'
]