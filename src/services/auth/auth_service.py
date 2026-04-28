#!/usr/bin/env python3
"""
Authentication Service - Dịch vụ xác thực và phân quyền người dùng
"""
import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
from enum import Enum

try:
    import bcrypt
except ImportError:
    bcrypt = None

from src.models import NhanVien, TrangThaiNhanVienEnum
from src.database import get_session


class UserRole(Enum):
    """Các vai trò người dùng"""
    ADMIN = "admin"
    MANAGER = "manager" 
    STAFF = "staff"
    GUEST = "guest"


class AuthStatus(Enum):
    """Trạng thái xác thực"""
    SUCCESS = "success"
    INVALID_CREDENTIALS = "invalid_credentials"
    ACCOUNT_DISABLED = "account_disabled"
    ACCOUNT_LOCKED = "account_locked"
    SESSION_EXPIRED = "session_expired"


class AuthService:
    """
    Service xử lý xác thực và phân quyền
    """
    
    def __init__(self):
        self.session_timeout = timedelta(hours=8)  # Session timeout sau 8 giờ
        self.max_failed_attempts = 5  # Số lần đăng nhập sai tối đa
        self.lockout_duration = timedelta(minutes=30)  # Thời gian khóa tài khoản
    
    def login(self, username: str, password: str) -> Dict[str, Any]:
        """
        Xác thực đăng nhập
        
        Args:
            username: Tên đăng nhập (mã nhân viên hoặc email)
            password: Mật khẩu
            
        Returns:
            Dict chứa:
                - status: AuthStatus
                - user: Thông tin người dùng (nếu thành công)
                - session_token: Token phiên làm việc
                - message: Thông báo
        """
        session = get_session()
        try:
            # Tìm nhân viên theo mã nhân viên, email hoặc tài khoản
            user = session.query(NhanVien).filter(
                (NhanVien.ma_nhan_vien == username) | 
                (NhanVien.email == username) |
                (NhanVien.tai_khoan == username)
            ).first()
            
            if not user:
                return {
                    'status': AuthStatus.INVALID_CREDENTIALS,
                    'user': None,
                    'session_token': None,
                    'message': 'Tài khoản không tồn tại'
                }
            
            # Kiểm tra trạng thái tài khoản
            if user.trang_thai != TrangThaiNhanVienEnum.HOAT_DONG:
                return {
                    'status': AuthStatus.ACCOUNT_DISABLED,
                    'user': None,
                    'session_token': None,
                    'message': 'Tài khoản đã bị vô hiệu hóa'
                }
            
            # Kiểm tra số lần đăng nhập sai (nếu có các cột tương ứng)
            failed_attempts = getattr(user, 'so_lan_sai', 0) or 0
            lock_time = getattr(user, 'thoi_gian_khoa', None)
            if failed_attempts >= self.max_failed_attempts:
                if lock_time and datetime.now() < lock_time + self.lockout_duration:
                    return {
                        'status': AuthStatus.ACCOUNT_LOCKED,
                        'user': None,
                        'session_token': None,
                        'message': f'Tài khoản bị khóa do đăng nhập sai quá {self.max_failed_attempts} lần. Vui lòng thử lại sau.'
                    }
                else:
                    # Reset lockout sau thời gian khóa
                    if hasattr(user, 'so_lan_sai'):
                        user.so_lan_sai = 0
                    if hasattr(user, 'thoi_gian_khoa'):
                        user.thoi_gian_khoa = None
            
            # Xác minh mật khẩu
            if not self._verify_password(password, user.mat_khau):
                # Cập nhật số lần đăng nhập sai
                if hasattr(user, 'so_lan_sai'):
                    user.so_lan_sai = failed_attempts + 1
                    if user.so_lan_sai >= self.max_failed_attempts and hasattr(user, 'thoi_gian_khoa'):
                        user.thoi_gian_khoa = datetime.now()
                
                session.commit()
                return {
                    'status': AuthStatus.INVALID_CREDENTIALS,
                    'user': None,
                    'session_token': None,
                    'message': 'Mật khẩu không đúng'
                }
            
            # Reset số lần đăng nhập sai
            if hasattr(user, 'so_lan_sai'):
                user.so_lan_sai = 0
            if hasattr(user, 'thoi_gian_khoa'):
                user.thoi_gian_khoa = None
            user.lan_dang_nhap_cuoi = datetime.now().isoformat()
            if self._password_needs_rehash(user.mat_khau):
                user.mat_khau = self.hash_password(password)
            session.commit()
            
            # Tạo session token
            session_token = self._generate_session_token()
            
            return {
                'status': AuthStatus.SUCCESS,
                'user': {
                    'ma_nhan_vien': user.ma_nhan_vien,
                    'ho_ten': user.ho_ten,
                    'email': user.email,
                    'vai_tro': user.vai_tro,
                    'trang_thai': user.trang_thai,
                    'lan_dang_nhap_cuoi': user.lan_dang_nhap_cuoi
                },
                'session_token': session_token,
                'message': 'Đăng nhập thành công'
            }
            
        except Exception as e:
            return {
                'status': AuthStatus.INVALID_CREDENTIALS,
                'user': None,
                'session_token': None,
                'message': 'Lỗi hệ thống khi đăng nhập'
            }
        finally:
            session.close()
    
    def logout(self, session_token: str) -> bool:
        """
        Đăng xuất người dùng
        
        Args:
            session_token: Token phiên làm việc
            
        Returns:
            bool: True nếu đăng xuất thành công
        """
        # TODO: Implement session invalidation
        # Currently just returns True as sessions are stateless
        return True
    
    def get_current_user(self, session_token: str) -> Optional[Dict[str, Any]]:
        """
        Lấy thông tin người dùng hiện tại từ session token
        
        Args:
            session_token: Token phiên làm việc
            
        Returns:
            Dict thông tin người dùng hoặc None nếu không hợp lệ
        """
        # TODO: Implement session validation
        # For now, this would need to be implemented with proper session storage
        return None
    
    def check_permission(self, user_role: str, permission: str) -> bool:
        """
        Kiểm tra quyền truy cập
        
        Args:
            user_role: Vai trò người dùng
            permission: Quyền cần kiểm tra
            
        Returns:
            bool: True nếu có quyền
        """
        # Define permission matrix
        permission_matrix = {
            'admin': [
                'view_all', 'edit_all', 'delete_all', 'manage_users', 
                'manage_settings', 'view_reports', 'export_data'
            ],
            'manager': [
                'view_all', 'edit_own', 'delete_own', 'view_reports', 'export_data'
            ],
            'staff': [
                'view_own', 'edit_own', 'view_reports'
            ],
            'guest': [
                'view_own'
            ]
        }
        
        role_permissions = permission_matrix.get(user_role.lower(), [])
        return permission in role_permissions
    
    def hash_password(self, password: str) -> str:
        """
        Mã hóa mật khẩu
        
        Args:
            password: Mật khẩu gốc
            
        Returns:
            str: Mật khẩu đã mã hóa
        """
        if bcrypt is not None:
            hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds=12))
            return hashed.decode()
        # Fallback SHA-256 với salt nếu bcrypt chưa cài
        salt = secrets.token_hex(32)
        pwdhash = hashlib.sha256(salt.encode() + password.encode()).hexdigest()
        return f"{salt}${pwdhash}"

    def _is_bcrypt_hash(self, hashed_password: str) -> bool:
        return hashed_password.startswith(('$2a$', '$2b$', '$2y$'))

    def _password_needs_rehash(self, hashed_password: str) -> bool:
        if bcrypt is None:
            return False
        return not self._is_bcrypt_hash(hashed_password)
    
    def _verify_password(self, password: str, hashed_password: str) -> bool:
        """
        Xác minh mật khẩu
        
        Args:
            password: Mật khẩu gốc
            hashed_password: Mật khẩu đã mã hóa (định dạng salt$hash)
            
        Returns:
            bool: True nếu khớp
        """
        if not hashed_password:
            return False
        if self._is_bcrypt_hash(hashed_password):
            if bcrypt is None:
                return False
            try:
                return bcrypt.checkpw(password.encode(), hashed_password.encode())
            except ValueError:
                return False
        if '$' in hashed_password:
            try:
                salt, pwdhash = hashed_password.split('$', 1)
                return pwdhash == hashlib.sha256(salt.encode() + password.encode()).hexdigest()
            except ValueError:
                return False
        return secrets.compare_digest(password, hashed_password)
    
    def _generate_session_token(self) -> str:
        """
        Tạo session token ngẫu nhiên
        
        Returns:
            str: Session token
        """
        return secrets.token_urlsafe(32)
    
    def change_password(self, ma_nhan_vien: str, old_password: str, new_password: str) -> Dict[str, Any]:
        """
        Đổi mật khẩu
        
        Args:
            ma_nhan_vien: Mã nhân viên
            old_password: Mật khẩu cũ
            new_password: Mật khẩu mới
            
        Returns:
            Dict kết quả đổi mật khẩu
        """
        session = get_session()
        try:
            user = session.query(NhanVien).filter(
                NhanVien.ma_nhan_vien == ma_nhan_vien
            ).first()
            
            if not user:
                return {
                    'success': False,
                    'message': 'Nhân viên không tồn tại'
                }
            
            if not self._verify_password(old_password, user.mat_khau):
                return {
                    'success': False,
                    'message': 'Mật khẩu cũ không đúng'
                }
            
            user.mat_khau = self.hash_password(new_password)
            user.ngay_doi_mat_khau = datetime.now()
            session.commit()
            
            return {
                'success': True,
                'message': 'Đổi mật khẩu thành công'
            }
            
        except Exception as e:
            session.rollback()
            return {
                'success': False,
                'message': 'Lỗi khi đổi mật khẩu'
            }
        finally:
            session.close()


# Convenience functions
def login(username: str, password: str) -> Dict[str, Any]:
    """Đăng nhập"""
    service = AuthService()
    return service.login(username, password)


def logout(session_token: str) -> bool:
    """Đăng xuất"""
    service = AuthService()
    return service.logout(session_token)


def check_permission(user_role: str, permission: str) -> bool:
    """Kiểm tra quyền"""
    service = AuthService()
    return service.check_permission(user_role, permission)


def hash_password(password: str) -> str:
    """Mã hóa mật khẩu"""
    service = AuthService()
    return service.hash_password(password)


__all__ = [
    'AuthService',
    'UserRole',
    'AuthStatus',
    'login',
    'logout',
    'check_permission',
    'hash_password'
]