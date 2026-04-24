"""
Kho Service - Business logic cho Quản lý Kho hàng
"""
from typing import List, Optional, Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import or_

from src.models import Kho, ViTri, TrangThaiKhoEnum, TrangThaiViTriEnum
from src.database import get_session


class KhoService:
    """
    Service layer cho Kho hàng
    Cung cấp các thao tác CRUD và business logic
    """
    
    def __init__(self, session: Session = None):
        """
        Khởi tạo service
        
        Args:
            session: Database session (optional, sẽ tự tạo nếu không có)
        """
        self.session = session
        self._external_session = session is not None
    
    def _get_session(self) -> Session:
        """Get session (tự tạo nếu chưa có)"""
        if self.session is None:
            return get_session()
        return self.session
    
    def _close_session(self, session: Session):
        """Close session nếu tự tạo"""
        if not self._external_session and session:
            session.close()
    
    def create(self, data: Dict[str, Any]) -> Kho:
        """
        Tạo kho mới
        
        Args:
            data: Dictionary chứa thông tin kho
                - ma_kho (str): Mã kho (auto-generate nếu không có)
                - ten_kho (str): Tên kho
                - dia_chi (str): Địa chỉ
                - dien_tich (float): Tổng diện tích
                - suc_chua (float): Sức chứa tối đa
        
        Returns:
            Kho: Kho đã tạo
        
        Raises:
            ValueError: Nếu dữ liệu không hợp lệ hoặc mã kho đã tồn tại
        """
        session = self._get_session()
        try:
            # Validate data
            self._validate_data(data)
            
            # Check duplicate ma_kho
            if data.get('ma_kho'):
                self._check_duplicate_ma_kho(data['ma_kho'])
            else:
                data['ma_kho'] = self._generate_ma_kho()
            
            # Create object
            kho = Kho(**data)
            
            # Add to database
            session.add(kho)
            session.commit()
            session.refresh(kho)
            
            return kho
            
        except Exception as e:
            session.rollback()
            raise e
        finally:
            self._close_session(session)
    
    def get_by_id(self, ma_kho: str) -> Optional[Kho]:
        """
        Lấy kho theo mã
        
        Args:
            ma_kho: Mã kho
        
        Returns:
            Kho hoặc None nếu không tìm thấy
        """
        session = self._get_session()
        try:
            return session.query(Kho).filter(Kho.ma_kho == ma_kho).first()
        finally:
            self._close_session(session)
    
    def get_all(self, skip: int = 0, limit: int = 100, 
                trang_thai: str = None) -> List[Kho]:
        """
        Lấy tất cả kho với pagination
        
        Args:
            skip: Số bản ghi bỏ qua
            limit: Số bản ghi tối đa
            trang_thai: Filter theo trạng thái (optional)
        
        Returns:
            List[Kho]: Danh sách kho
        """
        session = self._get_session()
        try:
            query = session.query(Kho)
            
            if trang_thai:
                query = query.filter(Kho.trang_thai == trang_thai)
            
            return query.offset(skip).limit(limit).all()
        finally:
            self._close_session(session)
    
    def search(self, keyword: str, skip: int = 0, limit: int = 50) -> List[Kho]:
        """
        Tìm kiếm kho theo từ khóa
        
        Args:
            keyword: Từ khóa tìm kiếm
            skip: Số bản ghi bỏ qua
            limit: Số bản ghi tối đa
        
        Returns:
            List[Kho]: Danh sách kho tìm được
        """
        session = self._get_session()
        try:
            search_pattern = f"%{keyword}%"
            
            results = session.query(Kho).filter(
                Kho.trang_thai != TrangThaiKhoEnum.NGUNG,
                or_(
                    Kho.ma_kho.ilike(search_pattern),
                    Kho.ten_kho.ilike(search_pattern),
                    Kho.dia_chi.ilike(search_pattern)
                )
            ).offset(skip).limit(limit).all()
            
            return results
        finally:
            self._close_session(session)
    
    def update(self, ma_kho: str, data: Dict[str, Any]) -> Optional[Kho]:
        """
        Cập nhật thông tin kho
        
        Args:
            ma_kho: Mã kho cần update
            data: Dictionary chứa thông tin cần update
        
        Returns:
            Kho: Kho đã update hoặc None nếu không tìm thấy
        """
        session = self._get_session()
        try:
            kho = self.get_by_id(ma_kho)
            if not kho:
                return None
            
            # Validate data (excluding ma_kho)
            exclude_fields = ['ma_kho']
            validate_data = {k: v for k, v in data.items() if k not in exclude_fields}
            if validate_data:
                self._validate_data(validate_data, is_update=True)
            
            # Update fields
            for key, value in data.items():
                if hasattr(kho, key) and key not in exclude_fields:
                    setattr(kho, key, value)
            
            kho.ngay_cap_nhat = datetime.now()
            session.commit()
            session.refresh(kho)
            
            return kho
            
        except Exception as e:
            session.rollback()
            raise e
        finally:
            self._close_session(session)
    
    def delete(self, ma_kho: str) -> bool:
        """
        Xóa kho (chỉ allowed nếu không có vị trí nào)
        
        Args:
            ma_kho: Mã kho cần xóa
        
        Returns:
            bool: True nếu xóa thành công
        
        Raises:
            ValueError: Nếu kho còn vị trí
        """
        session = self._get_session()
        try:
            kho = self.get_by_id(ma_kho)
            if not kho:
                return False
            
            # Check for existing positions
            vi_tri_count = session.query(ViTri).filter(
                ViTri.ma_kho == ma_kho
            ).count()
            
            if vi_tri_count > 0:
                raise ValueError(
                    f"Không thể xóa kho có {vi_tri_count} vị trí lưu trữ"
                )
            
            # Hard delete (no positions exist)
            session.delete(kho)
            session.commit()
            
            return True
            
        except Exception as e:
            session.rollback()
            raise e
        finally:
            self._close_session(session)
    
    def calculate_fill_rate(self, ma_kho: str) -> float:
        """
        Tính tỷ lệ lấp đầy của kho
        
        Args:
            ma_kho: Mã kho
        
        Returns:
            float: Tỷ lệ lấp đầy (0-100)
        """
        session = self._get_session()
        try:
            kho = self.get_by_id(ma_kho)
            if not kho:
                return 0.0
            
            # Calculate used capacity from positions
            used_capacity = session.query(
                ViTri.dien_tich
            ).filter(
                ViTri.ma_kho == ma_kho,
                ViTri.trang_thai == TrangThaiViTriEnum.DA_THUE
            ).all()
            
            total_used = sum([v[0] for v in used_capacity]) if used_capacity else 0
            
            if kho.suc_chua == 0:
                return 0.0
            
            fill_rate = (total_used / kho.suc_chua) * 100
            return round(fill_rate, 2)
            
        finally:
            self._close_session(session)
    
    def get_available_capacity(self, ma_kho: str) -> Dict[str, Any]:
        """
        Lấy thông tin dung tích còn lại
        
        Args:
            ma_kho: Mã kho
        
        Returns:
            Dict với:
                - tong_dien_tich: Total area
                - da_su_dung: Used area
                - con_lai: Remaining area
                - ty_le_lap_day: Fill rate %
                - so_vi_tri_trong: Number of empty positions
        """
        session = self._get_session()
        try:
            kho = self.get_by_id(ma_kho)
            if not kho:
                return {}
            
            # Get position statistics
            vi_tri_stats = session.query(
                ViTri.trang_thai,
                ViTri.dien_tich
            ).filter(
                ViTri.ma_kho == ma_kho
            ).all()
            
            da_su_dung = sum([v[1] for v in vi_tri_stats if v[0] == TrangThaiViTriEnum.DA_THUE])
            so_vi_tri_trong = sum([1 for v in vi_tri_stats if v[0] == TrangThaiViTriEnum.TRONG])
            
            return {
                'tong_dien_tich': kho.dien_tich,
                'da_su_dung': da_su_dung,
                'con_lai': kho.dien_tich - da_su_dung,
                'ty_le_lap_day': round((da_su_dung / kho.dien_tich) * 100, 2) if kho.dien_tich > 0 else 0,
                'so_vi_tri_trong': so_vi_tri_trong,
            }
            
        finally:
            self._close_session(session)
    
    def get_overcrowded_khos(self, threshold: float = 90.0) -> List[Kho]:
        """
        Lấy danh sách kho có tỷ lệ lấp đầy > threshold
        
        Args:
            threshold: Percentage threshold (default: 90%)
        
        Returns:
            List[Kho]: Danh sách kho quá tải
        """
        session = self._get_session()
        try:
            khos = session.query(Kho).filter(
                Kho.trang_thai == TrangThaiKhoEnum.HOAT_DONG
            ).all()
            
            overcrowded = []
            for kho in khos:
                fill_rate = self.calculate_fill_rate(kho.ma_kho)
                if fill_rate > threshold:
                    overcrowded.append(kho)
            
            return overcrowded
            
        finally:
            self._close_session(session)
    
    def _validate_data(self, data: Dict[str, Any], is_update: bool = False):
        """
        Validate dữ liệu kho
        
        Args:
            data: Dictionary chứa dữ liệu
            is_update: Nếu True thì bỏ qua validate required
        
        Raises:
            ValueError: Nếu dữ liệu không hợp lệ
        """
        errors = []
        
        # Validate required fields
        if not is_update:
            required_fields = ['ten_kho', 'dia_chi', 'dien_tich', 'suc_chua']
            for field in required_fields:
                if field not in data or not data[field]:
                    errors.append(f"Trường '{field}' là bắt buộc")
        
        # Validate dien_tich
        if 'dien_tich' in data and data['dien_tich']:
            try:
                if float(data['dien_tich']) <= 0:
                    errors.append("Diện tích phải lớn hơn 0")
            except (TypeError, ValueError):
                errors.append("Diện tích phải là số")
        
        # Validate suc_chua
        if 'suc_chua' in data and data['suc_chua']:
            try:
                if float(data['suc_chua']) <= 0:
                    errors.append("Sức chứa phải lớn hơn 0")
            except (TypeError, ValueError):
                errors.append("Sức chứa phải là số")
        
        if errors:
            raise ValueError("; ".join(errors))
    
    def _check_duplicate_ma_kho(self, ma_kho: str):
        """
        Check if ma_kho already exists
        
        Raises:
            ValueError: If ma_kho already exists
        """
        session = self._get_session()
        try:
            existing = session.query(Kho).filter(Kho.ma_kho == ma_kho).first()
            if existing:
                raise ValueError(f"Mã kho '{ma_kho}' đã tồn tại")
        finally:
            self._close_session(session)
    
    def _generate_ma_kho(self) -> str:
        """
        Generate mã kho tự động
        
        Format: KHO + XXX (3 số sequence)
        
        Returns:
            str: Mã kho
        """
        from src.utils.helpers import generate_code
        return generate_code(prefix="KHO", length=3, include_date=False, separator="")


# Convenience functions
def create_kho(data: Dict[str, Any]) -> Kho:
    """Tạo kho mới"""
    service = KhoService()
    return service.create(data)


def get_kho(ma_kho: str) -> Optional[Kho]:
    """Lấy kho theo mã"""
    service = KhoService()
    return service.get_by_id(ma_kho)


def get_all_kho(skip: int = 0, limit: int = 100) -> List[Kho]:
    """Lấy tất cả kho"""
    service = KhoService()
    return service.get_all(skip, limit)


def search_kho(keyword: str, skip: int = 0, limit: int = 50) -> List[Kho]:
    """Tìm kiếm kho"""
    service = KhoService()
    return service.search(keyword, skip, limit)


def update_kho(ma_kho: str, data: Dict[str, Any]) -> Optional[Kho]:
    """Cập nhật kho"""
    service = KhoService()
    return service.update(ma_kho, data)


def delete_kho(ma_kho: str) -> bool:
    """Xóa kho"""
    service = KhoService()
    return service.delete(ma_kho)


def calculate_fill_rate(ma_kho: str) -> float:
    """Tính tỷ lệ lấp đầy"""
    service = KhoService()
    return service.calculate_fill_rate(ma_kho)


def get_available_capacity(ma_kho: str) -> Dict[str, Any]:
    """Lấy dung tích còn lại"""
    service = KhoService()
    return service.get_available_capacity(ma_kho)


__all__ = [
    'KhoService',
    'create_kho',
    'get_kho',
    'get_all_kho',
    'search_kho',
    'update_kho',
    'delete_kho',
    'calculate_fill_rate',
    'get_available_capacity',
]
