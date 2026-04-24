"""
Base Repository Pattern
Cung cấp interface chung cho tất cả repositories
"""
from sqlalchemy.orm import Session, joinedload
from typing import TypeVar, Generic, List, Optional, Type, Dict, Any
from datetime import datetime

T = TypeVar('T')

class BaseRepository(Generic[T]):
    """
    Base repository với CRUD operations cơ bản
    
    Usage:
        class KhachHangRepository(BaseRepository[KhachHang]):
            def __init__(self, session: Session):
                super().__init__(session, KhachHang)
    """
    
    def __init__(self, session: Session, model: Type[T]):
        """
        Khởi tạo repository
        
        Args:
            session: Database session
            model: Model class
        """
        self.session = session
        self.model = model
    
    def create(self, data: Dict[str, Any]) -> T:
        """
        Tạo bản ghi mới
        
        Args:
            data: Dictionary chứa data
        
        Returns:
            Model instance
        """
        obj = self.model(**data)
        self.session.add(obj)
        self.session.commit()
        self.session.refresh(obj)
        return obj
    
    def get_by_id(self, id_value: Any) -> Optional[T]:
        """
        Lấy bản ghi theo ID
        
        Args:
            id_value: Primary key value
        
        Returns:
            Model instance or None
        """
        return self.session.query(self.model).filter(
            self.model.__table__.primary_key.columns.values()[0] == id_value
        ).first()
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[T]:
        """
        Lấy tất cả bản ghi với pagination
        
        Args:
            skip: Số bản ghi bỏ qua
            limit: Số bản ghi tối đa
        
        Returns:
            List of model instances
        """
        return self.session.query(self.model).offset(skip).limit(limit).all()
    
    def update(self, id_value: Any, data: Dict[str, Any]) -> Optional[T]:
        """
        Cập nhật bản ghi
        
        Args:
            id_value: Primary key value
            data: Dictionary chứa data cần update
        
        Returns:
            Updated model instance or None
        """
        obj = self.get_by_id(id_value)
        if obj:
            for key, value in data.items():
                if hasattr(obj, key):
                    setattr(obj, key, value)
            self.session.commit()
            self.session.refresh(obj)
        return obj
    
    def delete(self, id_value: Any) -> bool:
        """
        Xóa bản ghi
        
        Args:
            id_value: Primary key value
        
        Returns:
            True if deleted, False if not found
        """
        obj = self.get_by_id(id_value)
        if obj:
            self.session.delete(obj)
            self.session.commit()
            return True
        return False
    
    def count(self) -> int:
        """
        Đếm số bản ghi
        
        Returns:
            Total count
        """
        return self.session.query(self.model).count()
    
    def exists(self, id_value: Any) -> bool:
        """
        Kiểm tra bản ghi có tồn tại
        
        Args:
            id_value: Primary key value
        
        Returns:
            True if exists
        """
        return self.get_by_id(id_value) is not None


class SoftDeleteRepository(BaseRepository[T]):
    """
    Repository hỗ trợ soft delete
    Yêu cầu model có cột 'trang_thai'
    """
    
    def delete(self, id_value: Any) -> bool:
        """
        Soft delete - cập nhật trạng thái thay vì xóa
        
        Args:
            id_value: Primary key value
        
        Returns:
            True if deleted
        """
        obj = self.get_by_id(id_value)
        if obj and hasattr(obj, 'trang_thai'):
            obj.trang_thai = 'da_xoa'
            self.session.commit()
            return True
        return False
    
    def get_all_active(self, skip: int = 0, limit: int = 100) -> List[T]:
        """
        Lấy tất cả bản ghi đang active (không bị xóa)
        
        Args:
            skip: Số bản ghi bỏ qua
            limit: Số bản ghi tối đa
        
        Returns:
            List of active model instances
        """
        if hasattr(self.model, 'trang_thai'):
            return self.session.query(self.model).filter(
                self.model.trang_thai != 'da_xoa'
            ).offset(skip).limit(limit).all()
        return self.get_all(skip, limit)


class TimestampRepository(BaseRepository[T]):
    """
    Repository tự động quản lý created_at/updated_at
    """
    
    def create(self, data: Dict[str, Any]) -> T:
        """Tạo với tự động set ngày tạo"""
        if hasattr(self.model, 'ngay_tao') and 'ngay_tao' not in data:
            data['ngay_tao'] = datetime.now()
        return super().create(data)
    
    def update(self, id_value: Any, data: Dict[str, Any]) -> Optional[T]:
        """Cập nhật với tự động set ngày cập nhật"""
        obj = self.get_by_id(id_value)
        if obj and hasattr(obj, 'ngay_cap_nhat'):
            obj.ngay_cap_nhat = datetime.now()
        return super().update(id_value, data)

__all__ = [
    'BaseRepository',
    'SoftDeleteRepository',
    'TimestampRepository'
]
