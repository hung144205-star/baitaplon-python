"""
Vị trí Service - Business logic cho Quản lý Vị trí lưu trữ
"""
from typing import List, Optional, Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import or_

from src.models import ViTri, Kho, TrangThaiViTriEnum
from src.database import get_session


class ViTriService:
    """
    Service layer cho Vị trí lưu trữ
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
    
    def create(self, data: Dict[str, Any]) -> ViTri:
        """
        Tạo vị trí mới
        
        Args:
            data: Dictionary chứa thông tin vị trí
                - ma_vi_tri (str): Mã vị trí (auto-generate nếu không có)
                - ma_kho (str): Mã kho
                - khu_vuc (str): Khu vực
                - hang (str): Hàng/Zone
                - tang (int): Tầng
                - dien_tich (float): Diện tích
                - gia_thue (float): Giá thuê
                - suc_chua (float, optional): Sức chứa
        
        Returns:
            ViTri: Vị trí đã tạo
        
        Raises:
            ValueError: Nếu dữ liệu không hợp lệ hoặc mã kho không tồn tại
        """
        session = self._get_session()
        try:
            # Validate data
            self._validate_data(data)
            
            # Check if kho exists
            if not session.query(Kho).filter(Kho.ma_kho == data['ma_kho']).first():
                raise ValueError(f"Kho '{data['ma_kho']}' không tồn tại")
            
            # Generate ma_vi_tri if not provided
            if not data.get('ma_vi_tri'):
                data['ma_vi_tri'] = self._generate_ma_vi_tri(data['ma_kho'])
            else:
                # Check duplicate
                self._check_duplicate_ma_vi_tri(data['ma_vi_tri'])
            
            # Create object
            vi_tri = ViTri(**data)
            
            # Add to database
            session.add(vi_tri)
            session.commit()
            session.refresh(vi_tri)
            
            return vi_tri
            
        except Exception as e:
            session.rollback()
            raise e
        finally:
            self._close_session(session)
    
    def get_by_id(self, ma_vi_tri: str) -> Optional[ViTri]:
        """
        Lấy vị trí theo mã
        
        Args:
            ma_vi_tri: Mã vị trí
        
        Returns:
            ViTri hoặc None nếu không tìm thấy
        """
        session = self._get_session()
        try:
            return session.query(ViTri).filter(ViTri.ma_vi_tri == ma_vi_tri).first()
        finally:
            self._close_session(session)
    
    def get_by_kho(self, ma_kho: str, trang_thai: str = None) -> List[ViTri]:
        """
        Lấy tất cả vị trí theo kho
        
        Args:
            ma_kho: Mã kho
            trang_thai: Filter theo trạng thái (optional)
        
        Returns:
            List[ViTri]: Danh sách vị trí
        """
        session = self._get_session()
        try:
            query = session.query(ViTri).filter(ViTri.ma_kho == ma_kho)
            
            if trang_thai:
                query = query.filter(ViTri.trang_thai == trang_thai)
            
            return query.all()
        finally:
            self._close_session(session)
    
    def get_vi_tri_by_kho(self, ma_kho: str, trang_thai: str = None) -> List[ViTri]:
        """
        Alias for get_by_kho - compatibility method
        
        Args:
            ma_kho: Mã kho
            trang_thai: Filter theo trạng thái (optional)
        
        Returns:
            List[ViTri]: Danh sách vị trí
        """
        return self.get_by_kho(ma_kho, trang_thai)
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[ViTri]:
        """
        Lấy tất cả vị trí với pagination
        
        Args:
            skip: Số bản ghi bỏ qua
            limit: Số bản ghi tối đa
        
        Returns:
            List[ViTri]: Danh sách vị trí
        """
        session = self._get_session()
        try:
            return session.query(ViTri).offset(skip).limit(limit).all()
        finally:
            self._close_session(session)
    
    def get_available(self, ma_kho: str = None) -> List[ViTri]:
        """
        Lấy vị trí trống
        
        Args:
            ma_kho: Filter theo kho (optional)
        
        Returns:
            List[ViTri]: Danh sách vị trí trống
        """
        session = self._get_session()
        try:
            query = session.query(ViTri).filter(
                ViTri.trang_thai == TrangThaiViTriEnum.TRONG
            )
            
            if ma_kho:
                query = query.filter(ViTri.ma_kho == ma_kho)
            
            return query.all()
        finally:
            self._close_session(session)
    
    def update(self, ma_vi_tri: str, data: Dict[str, Any]) -> Optional[ViTri]:
        """
        Cập nhật thông tin vị trí
        
        Args:
            ma_vi_tri: Mã vị trí cần update
            data: Dictionary chứa thông tin cần update
        
        Returns:
            ViTri: Vị trí đã update hoặc None nếu không tìm thấy
        """
        session = self._get_session()
        try:
            # Always get fresh object from current session
            vi_tri = session.query(ViTri).filter(ViTri.ma_vi_tri == ma_vi_tri).first()
            if not vi_tri:
                return None
            
            # Validate data (excluding ma_vi_tri, ma_kho)
            exclude_fields = ['ma_vi_tri', 'ma_kho']
            validate_data = {k: v for k, v in data.items() if k not in exclude_fields}
            if validate_data:
                self._validate_data(validate_data, is_update=True)
            
            # Update fields
            for key, value in data.items():
                if hasattr(vi_tri, key) and key not in exclude_fields:
                    setattr(vi_tri, key, value)
            
            vi_tri.ngay_cap_nhat = datetime.now()
            session.commit()
            session.refresh(vi_tri)
            
            return vi_tri
            
        except Exception as e:
            session.rollback()
            raise e
        finally:
            self._close_session(session)
    
    def delete(self, ma_vi_tri: str) -> bool:
        """
        Xóa vị trí (chỉ allowed nếu chưa có hợp đồng)
        
        Args:
            ma_vi_tri: Mã vị trí cần xóa
        
        Returns:
            bool: True nếu xóa thành công
        
        Raises:
            ValueError: Nếu vị trí đang có hợp đồng
        """
        session = self._get_session()
        try:
            vi_tri = self.get_by_id(ma_vi_tri)
            if not vi_tri:
                return False
            
            # Check for active contracts
            from src.models import HopDong
            active_contracts = session.query(HopDong).filter(
                HopDong.ma_vi_tri == ma_vi_tri,
                HopDong.trang_thai == 'hieu_luc'
            ).count()
            
            if active_contracts > 0:
                raise ValueError(
                    f"Không thể xóa vị trí có {active_contracts} hợp đồng đang hoạt động"
                )
            
            # Hard delete
            session.delete(vi_tri)
            session.commit()
            
            return True
            
        except Exception as e:
            session.rollback()
            raise e
        finally:
            self._close_session(session)
    
    def update_status(self, ma_vi_tri: str, trang_thai: str) -> bool:
        """
        Cập nhật trạng thái vị trí
        
        Args:
            ma_vi_tri: Mã vị trí
            trang_thai: Trạng thái mới
        
        Returns:
            bool: True nếu thành công
        """
        session = self._get_session()
        try:
            vi_tri = self.get_by_id(ma_vi_tri)
            if not vi_tri:
                return False
            
            vi_tri.trang_thai = trang_thai
            vi_tri.ngay_cap_nhat = datetime.now()
            session.commit()
            
            return True
            
        except Exception as e:
            session.rollback()
            raise e
        finally:
            self._close_session(session)
    
    def find_available_by_requirements(self, ma_kho: str = None,
                                        dien_tich_min: float = None,
                                        gia_thue_max: float = None) -> List[ViTri]:
        """
        Tìm vị trí trống theo yêu cầu
        
        Args:
            ma_kho: Filter theo kho
            dien_tich_min: Diện tích tối thiểu
            gia_thue_max: Giá thuê tối đa
        
        Returns:
            List[ViTri]: Danh sách vị trí phù hợp
        """
        session = self._get_session()
        try:
            query = session.query(ViTri).filter(
                ViTri.trang_thai == TrangThaiViTriEnum.TRONG
            )
            
            if ma_kho:
                query = query.filter(ViTri.ma_kho == ma_kho)
            
            if dien_tich_min:
                query = query.filter(ViTri.dien_tich >= dien_tich_min)
            
            if gia_thue_max:
                query = query.filter(ViTri.gia_thue <= gia_thue_max)
            
            return query.all()
            
        finally:
            self._close_session(session)
    
    def get_statistics(self, ma_kho: str = None) -> Dict[str, Any]:
        """
        Lấy thống kê vị trí
        
        Args:
            ma_kho: Filter theo kho (optional)
        
        Returns:
            Dict với:
                - tong_so_vi_tri: Total positions
                - so_vi_tri_trong: Empty positions
                - so_vi_tri_da_thue: Rented positions
                - so_vi_tri_bao_tri: Maintenance positions
                - ty_le_trong: Empty rate %
                - ty_le_da_thue: Rented rate %
        """
        session = self._get_session()
        try:
            query = session.query(ViTri)
            
            if ma_kho:
                query = query.filter(ViTri.ma_kho == ma_kho)
            
            all_vi_tri = query.all()
            
            tong_so = len(all_vi_tri)
            so_trong = sum(1 for v in all_vi_tri if v.trang_thai == TrangThaiViTriEnum.TRONG)
            so_da_thue = sum(1 for v in all_vi_tri if v.trang_thai == TrangThaiViTriEnum.DA_THUE)
            so_bao_tri = sum(1 for v in all_vi_tri if v.trang_thai == TrangThaiViTriEnum.BAO_TRI)
            
            return {
                'tong_so_vi_tri': tong_so,
                'so_vi_tri_trong': so_trong,
                'so_vi_tri_da_thue': so_da_thue,
                'so_vi_tri_bao_tri': so_bao_tri,
                'ty_le_trong': round((so_trong / tong_so) * 100, 2) if tong_so > 0 else 0,
                'ty_le_da_thue': round((so_da_thue / tong_so) * 100, 2) if tong_so > 0 else 0,
            }
            
        finally:
            self._close_session(session)
    
    def _validate_data(self, data: Dict[str, Any], is_update: bool = False):
        """
        Validate dữ liệu vị trí
        
        Args:
            data: Dictionary chứa dữ liệu
            is_update: Nếu True thì bỏ qua validate required
        
        Raises:
            ValueError: Nếu dữ liệu không hợp lệ
        """
        errors = []
        
        # Validate required fields
        if not is_update:
            required_fields = ['ma_kho', 'khu_vuc', 'hang', 'tang', 'dien_tich', 'gia_thue']
            for field in required_fields:
                if field not in data or data[field] is None:
                    errors.append(f"Trường '{field}' là bắt buộc")
        
        # Validate ma_kho
        if 'ma_kho' in data and data['ma_kho']:
            session = self._get_session()
            kho_exists = session.query(Kho).filter(Kho.ma_kho == data['ma_kho']).first()
            if not kho_exists:
                errors.append(f"Kho '{data['ma_kho']}' không tồn tại")
        
        # Validate dien_tich
        if 'dien_tich' in data and data['dien_tich']:
            try:
                if float(data['dien_tich']) <= 0:
                    errors.append("Diện tích phải lớn hơn 0")
            except (TypeError, ValueError):
                errors.append("Diện tích phải là số")
        
        # Validate gia_thue
        if 'gia_thue' in data and data['gia_thue']:
            try:
                if float(data['gia_thue']) < 0:
                    errors.append("Giá thuê phải >= 0")
            except (TypeError, ValueError):
                errors.append("Giá thuê phải là số")
        
        if errors:
            raise ValueError("; ".join(errors))
    
    def _check_duplicate_ma_vi_tri(self, ma_vi_tri: str):
        """
        Check if ma_vi_tri already exists
        
        Raises:
            ValueError: If ma_vi_tri already exists
        """
        session = self._get_session()
        try:
            existing = session.query(ViTri).filter(ViTri.ma_vi_tri == ma_vi_tri).first()
            if existing:
                raise ValueError(f"Mã vị trí '{ma_vi_tri}' đã tồn tại")
        finally:
            self._close_session(session)
    
    def _generate_ma_vi_tri(self, ma_kho: str) -> str:
        """
        Generate mã vị trí tự động
        
        Format: {MA_KHO}-{KHU_VUC}-{HANG}-{TANG}-{STT}
        Example: KHO001-A-01-01-001
        
        Returns:
            str: Mã vị trí
        """
        session = self._get_session()
        try:
            # Get existing positions in the same warehouse
            existing = session.query(ViTri).filter(
                ViTri.ma_kho == ma_kho
            ).all()
            
            # Simple auto-increment
            stt = len(existing) + 1
            
            # Default values for area, row, floor
            khu_vuc = 'A'
            hang = '01'
            tang = 1
            
            return f"{ma_kho}-{khu_vuc}-{hang}-{tang:02d}-{stt:03d}"
            
        finally:
            self._close_session(session)


# Convenience functions
def create_vi_tri(data: Dict[str, Any]) -> ViTri:
    """Tạo vị trí mới"""
    service = ViTriService()
    return service.create(data)


def get_vi_tri(ma_vi_tri: str) -> Optional[ViTri]:
    """Lấy vị trí theo mã"""
    service = ViTriService()
    return service.get_by_id(ma_vi_tri)


def get_vi_tri_by_kho(ma_kho: str, trang_thai: str = None) -> List[ViTri]:
    """Lấy vị trí theo kho"""
    service = ViTriService()
    return service.get_by_kho(ma_kho, trang_thai)


def get_all_vi_tri(skip: int = 0, limit: int = 100) -> List[ViTri]:
    """Lấy tất cả vị trí"""
    service = ViTriService()
    return service.get_all(skip, limit)


def get_available_vi_tri(ma_kho: str = None) -> List[ViTri]:
    """Lấy vị trí trống"""
    service = ViTriService()
    return service.get_available(ma_kho)


def update_vi_tri(ma_vi_tri: str, data: Dict[str, Any]) -> Optional[ViTri]:
    """Cập nhật vị trí"""
    service = ViTriService()
    return service.update(ma_vi_tri, data)


def delete_vi_tri(ma_vi_tri: str) -> bool:
    """Xóa vị trí"""
    service = ViTriService()
    return service.delete(ma_vi_tri)


def update_vi_tri_status(ma_vi_tri: str, trang_thai: str) -> bool:
    """Cập nhật trạng thái vị trí"""
    service = ViTriService()
    return service.update_status(ma_vi_tri, trang_thai)


def find_available_vi_tri(ma_kho: str = None,
                          dien_tich_min: float = None,
                          gia_thue_max: float = None) -> List[ViTri]:
    """Tìm vị trí trống theo yêu cầu"""
    service = ViTriService()
    return service.find_available_by_requirements(ma_kho, dien_tich_min, gia_thue_max)


def get_vi_tri_statistics(ma_kho: str = None) -> Dict[str, Any]:
    """Lấy thống kê vị trí"""
    service = ViTriService()
    return service.get_statistics(ma_kho)


__all__ = [
    'ViTriService',
    'create_vi_tri',
    'get_vi_tri',
    'get_vi_tri_by_kho',
    'get_all_vi_tri',
    'get_available_vi_tri',
    'update_vi_tri',
    'delete_vi_tri',
    'update_vi_tri_status',
    'find_available_vi_tri',
    'get_vi_tri_statistics',
]
