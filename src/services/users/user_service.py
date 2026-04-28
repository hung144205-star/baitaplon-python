#!/usr/bin/env python3
"""
User Management Service - Dịch vụ quản lý người dùng/nhân viên
"""
from typing import List, Optional, Dict, Any
from datetime import datetime

from src.models import NhanVien, TrangThaiNhanVienEnum
from src.services.auth.auth_service import AuthService
from src.database import get_session


class UserService:
    """
    Service xử lý quản lý người dùng (nhân viên)
    """
    
    def __init__(self):
        self.auth_service = AuthService()
    
    def create_user(self, data: Dict[str, Any]) -> NhanVien:
        """
        Tạo người dùng mới
        
        Args:
            data: Dictionary chứa thông tin người dùng
                - ma_nhan_vien (str): Mã nhân viên (auto-generate nếu không có)
                - ho_ten (str): Họ tên đầy đủ
                - email (str): Email
                - so_dien_thoai (str): Số điện thoại
                - vai_tro (str): Vai trò (admin, manager, staff, guest)
                - mat_khau (str): Mật khẩu (sẽ được mã hóa)
        
        Returns:
            NhanVien: Người dùng đã tạo
        
        Raises:
            ValueError: Nếu dữ liệu không hợp lệ hoặc email đã tồn tại
        """
        session = get_session()
        try:
            # Validate data
            self._validate_user_data(data, is_create=True)
            
            # Check duplicate email
            existing_email = session.query(NhanVien).filter(
                NhanVien.email == data['email']
            ).first()
            if existing_email:
                raise ValueError(f"Email '{data['email']}' đã tồn tại")
            
            # Generate ma_nhan_vien if not provided
            if not data.get('ma_nhan_vien'):
                data['ma_nhan_vien'] = self._generate_ma_nhan_vien()
            
            # Check duplicate ma_nhan_vien
            existing_ma = session.query(NhanVien).filter(
                NhanVien.ma_nhan_vien == data['ma_nhan_vien']
            ).first()
            if existing_ma:
                raise ValueError(f"Mã nhân viên '{data['ma_nhan_vien']}' đã tồn tại")
            
            # Hash password
            if 'mat_khau' in data:
                data['mat_khau'] = self.auth_service.hash_password(data['mat_khau'])
            else:
                # Default password: same as ma_nhan_vien
                data['mat_khau'] = self.auth_service.hash_password(data['ma_nhan_vien'])
            
            # Set default values
            if 'trang_thai' not in data:
                data['trang_thai'] = TrangThaiNhanVienEnum.HOAT_DONG
            
            # Create user
            user = NhanVien(**data)
            user.ngay_tao = datetime.now()
            user.ngay_cap_nhat = datetime.now()
            
            session.add(user)
            session.commit()
            session.refresh(user)
            
            return user
            
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def get_user_by_id(self, ma_nhan_vien: str) -> Optional[NhanVien]:
        """
        Lấy người dùng theo mã nhân viên
        
        Args:
            ma_nhan_vien: Mã nhân viên
            
        Returns:
            NhanVien hoặc None nếu không tìm thấy
        """
        session = get_session()
        try:
            return session.query(NhanVien).filter(
                NhanVien.ma_nhan_vien == ma_nhan_vien
            ).first()
        finally:
            session.close()
    
    def get_all_users(self, skip: int = 0, limit: int = 100) -> List[NhanVien]:
        """
        Lấy tất cả người dùng với pagination
        
        Args:
            skip: Số bản ghi bỏ qua
            limit: Số bản ghi tối đa
            
        Returns:
            List[NhanVien]: Danh sách người dùng
        """
        session = get_session()
        try:
            return session.query(NhanVien).offset(skip).limit(limit).all()
        finally:
            session.close()
    
    def search_users(self, keyword: str) -> List[NhanVien]:
        """
        Tìm kiếm người dùng theo từ khóa
        
        Args:
            keyword: Từ khóa tìm kiếm (tìm trong họ tên, email, mã nhân viên)
            
        Returns:
            List[NhanVien]: Danh sách người dùng phù hợp
        """
        session = get_session()
        try:
            return session.query(NhanVien).filter(
                (NhanVien.ho_ten.ilike(f'%{keyword}%')) |
                (NhanVien.email.ilike(f'%{keyword}%')) |
                (NhanVien.ma_nhan_vien.ilike(f'%{keyword}%'))
            ).all()
        finally:
            session.close()
    
    def update_user(self, ma_nhan_vien: str, data: Dict[str, Any]) -> Optional[NhanVien]:
        """
        Cập nhật thông tin người dùng
        
        Args:
            ma_nhan_vien: Mã nhân viên cần cập nhật
            data: Dictionary chứa thông tin cần cập nhật
            
        Returns:
            NhanVien: Người dùng đã cập nhật hoặc None nếu không tìm thấy
        """
        session = get_session()
        try:
            user = self.get_user_by_id(ma_nhan_vien)
            if not user:
                return None
            
            # Validate data (excluding ma_nhan_vien)
            validate_data = {k: v for k, v in data.items() if k != 'ma_nhan_vien'}
            if validate_data:
                self._validate_user_data(validate_data, is_create=False)
            
            # Check duplicate email (if email is being updated)
            if 'email' in data and data['email'] != user.email:
                existing = session.query(NhanVien).filter(
                    NhanVien.email == data['email']
                ).first()
                if existing:
                    raise ValueError(f"Email '{data['email']}' đã tồn tại")
            
            # Update fields
            for key, value in data.items():
                if hasattr(user, key) and key != 'ma_nhan_vien':
                    if key == 'mat_khau':
                        # Hash new password
                        value = self.auth_service.hash_password(value)
                    setattr(user, key, value)
            
            user.ngay_cap_nhat = datetime.now()
            session.commit()
            session.refresh(user)
            
            return user
            
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def delete_user(self, ma_nhan_vien: str) -> bool:
        """
        Xóa người dùng (soft delete - cập nhật trạng thái)
        
        Args:
            ma_nhan_vien: Mã nhân viên cần xóa
            
        Returns:
            bool: True nếu xóa thành công
        """
        session = get_session()
        try:
            user = self.get_user_by_id(ma_nhan_vien)
            if not user:
                return False
            
            # Cannot delete current logged-in user (would need session validation)
            # For now, just update status to disabled
            user.trang_thai = TrangThaiNhanVienEnum.NGUNG_HOAT_DONG
            user.ngay_cap_nhat = datetime.now()
            session.commit()
            
            return True
            
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def change_user_password(self, ma_nhan_vien: str, new_password: str) -> bool:
        """
        Đổi mật khẩu người dùng
        
        Args:
            ma_nhan_vien: Mã nhân viên
            new_password: Mật khẩu mới
            
        Returns:
            bool: True nếu đổi thành công
        """
        session = get_session()
        try:
            user = self.get_user_by_id(ma_nhan_vien)
            if not user:
                return False
            
            user.mat_khau = self.auth_service.hash_password(new_password)
            user.ngay_doi_mat_khau = datetime.now()
            user.ngay_cap_nhat = datetime.now()
            session.commit()
            
            return True
            
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def assign_role(self, ma_nhan_vien: str, new_role: str) -> bool:
        """
        Gán vai trò mới cho người dùng
        
        Args:
            ma_nhan_vien: Mã nhân viên
            new_role: Vai trò mới (admin, manager, staff, guest)
            
        Returns:
            bool: True nếu gán thành công
        """
        # Validate role
        valid_roles = ['admin', 'manager', 'staff', 'guest']
        if new_role not in valid_roles:
            raise ValueError(f"Vai trò '{new_role}' không hợp lệ. Các vai trò hợp lệ: {valid_roles}")
        
        session = get_session()
        try:
            user = self.get_user_by_id(ma_nhan_vien)
            if not user:
                return False
            
            user.vai_tro = new_role
            user.ngay_cap_nhat = datetime.now()
            session.commit()
            
            return True
            
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def get_users_by_role(self, role: str) -> List[NhanVien]:
        """
        Lấy danh sách người dùng theo vai trò
        
        Args:
            role: Vai trò cần lọc
            
        Returns:
            List[NhanVien]: Danh sách người dùng
        """
        session = get_session()
        try:
            return session.query(NhanVien).filter(
                NhanVien.vai_tro == role
            ).all()
        finally:
            session.close()
    
    def get_active_users(self) -> List[NhanVien]:
        """
        Lấy danh sách người dùng đang hoạt động
        
        Returns:
            List[NhanVien]: Danh sách người dùng hoạt động
        """
        session = get_session()
        try:
            return session.query(NhanVien).filter(
                NhanVien.trang_thai == TrangThaiNhanVienEnum.HOAT_DONG
            ).all()
        finally:
            session.close()
    
    def _validate_user_data(self, data: Dict[str, Any], is_create: bool = True):
        """
        Validate dữ liệu người dùng
        
        Args:
            data: Dictionary chứa dữ liệu
            is_create: True nếu đang tạo mới, False nếu đang cập nhật
            
        Raises:
            ValueError: Nếu dữ liệu không hợp lệ
        """
        errors = []
        
        # Required fields for create
        if is_create:
            required_fields = ['ho_ten', 'email', 'vai_tro']
            for field in required_fields:
                if field not in data or not data[field]:
                    errors.append(f"Trường '{field}' là bắt buộc")
        
        # Validate email format
        if 'email' in data and data['email']:
            from src.utils.validators import validate_email
            try:
                validate_email(data['email'])
            except ValueError:
                errors.append("Định dạng email không hợp lệ")
        
        # Validate phone number (if provided)
        if 'so_dien_thoai' in data and data['so_dien_thoai']:
            from src.utils.validators import validate_phone
            try:
                validate_phone(data['so_dien_thoai'])
            except ValueError:
                errors.append("Định dạng số điện thoại không hợp lệ")
        
        # Validate role
        if 'vai_tro' in data and data['vai_tro']:
            valid_roles = ['admin', 'manager', 'staff', 'guest']
            if data['vai_tro'] not in valid_roles:
                errors.append(f"Vai trò phải là một trong: {', '.join(valid_roles)}")
        
        if errors:
            raise ValueError("; ".join(errors))
    
    def _generate_ma_nhan_vien(self) -> str:
        """
        Tự động sinh mã nhân viên
        
        Format: NV + YYYYMM + sequence
        Example: NV202604001
        
        Returns:
            str: Mã nhân viên
        """
        session = get_session()
        try:
            current_date = datetime.now()
            year_month = current_date.strftime('%Y%m')
            
            # Count existing employees with same year-month prefix
            prefix = f"NV{year_month}"
            count = session.query(NhanVien).filter(
                NhanVien.ma_nhan_vien.like(f"{prefix}%")
            ).count()
            
            sequence = count + 1
            return f"{prefix}{sequence:03d}"
            
        finally:
            session.close()


# Convenience functions
def create_user(data: Dict[str, Any]) -> NhanVien:
    """Tạo người dùng mới"""
    service = UserService()
    return service.create_user(data)


def get_user(ma_nhan_vien: str) -> Optional[NhanVien]:
    """Lấy người dùng theo mã"""
    service = UserService()
    return service.get_user_by_id(ma_nhan_vien)


def get_all_users(skip: int = 0, limit: int = 100) -> List[NhanVien]:
    """Lấy tất cả người dùng"""
    service = UserService()
    return service.get_all_users(skip, limit)


def search_users(keyword: str) -> List[NhanVien]:
    """Tìm kiếm người dùng"""
    service = UserService()
    return service.search_users(keyword)


def update_user(ma_nhan_vien: str, data: Dict[str, Any]) -> Optional[NhanVien]:
    """Cập nhật người dùng"""
    service = UserService()
    return service.update_user(ma_nhan_vien, data)


def delete_user(ma_nhan_vien: str) -> bool:
    """Xóa người dùng"""
    service = UserService()
    return service.delete_user(ma_nhan_vien)


def change_user_password(ma_nhan_vien: str, new_password: str) -> bool:
    """Đổi mật khẩu người dùng"""
    service = UserService()
    return service.change_user_password(ma_nhan_vien, new_password)


def assign_role(ma_nhan_vien: str, new_role: str) -> bool:
    """Gán vai trò cho người dùng"""
    service = UserService()
    return service.assign_role(ma_nhan_vien, new_role)


__all__ = [
    'UserService',
    'create_user',
    'get_user',
    'get_all_users',
    'search_users',
    'update_user',
    'delete_user',
    'change_user_password',
    'assign_role'
]