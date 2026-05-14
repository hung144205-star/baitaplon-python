"""
Loại Hàng Service - Business logic cho Quản lý Loại hàng hóa
"""
from typing import List, Optional, Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session

from src.models import LoaiHang
from src.database import get_session


class LoaiHangService:
    """
    Service layer cho Loại hàng hóa
    """

    def __init__(self, session: Session = None):
        self.session = session
        self._external_session = session is not None

    def _get_session(self) -> Session:
        if self.session is None:
            return get_session()
        return self.session

    def _close_session(self, session: Session):
        if not self._external_session and session:
            session.close()

    def create(self, data: Dict[str, Any]) -> LoaiHang:
        """Tạo loại hàng mới"""
        session = self._get_session()
        try:
            # Check duplicate
            if data.get('ma_loai'):
                existing = session.query(LoaiHang).filter(
                    LoaiHang.ma_loai == data['ma_loai']
                ).first()
                if existing:
                    raise ValueError(f"Mã loại '{data['ma_loai']}' đã tồn tại")
            else:
                data['ma_loai'] = self._generate_ma_loai()

            loai_hang = LoaiHang(**data)
            session.add(loai_hang)
            session.commit()
            session.refresh(loai_hang)
            return loai_hang

        except Exception as e:
            session.rollback()
            raise e
        finally:
            self._close_session(session)

    def get_by_id(self, ma_loai: str) -> Optional[LoaiHang]:
        """Lấy loại hàng theo mã"""
        session = self._get_session()
        try:
            return session.query(LoaiHang).filter(
                LoaiHang.ma_loai == ma_loai
            ).first()
        finally:
            self._close_session(session)

    def get_all(self, skip: int = 0, limit: int = 100) -> List[LoaiHang]:
        """Lấy tất cả loại hàng"""
        session = self._get_session()
        try:
            return session.query(LoaiHang).offset(skip).limit(limit).all()
        finally:
            self._close_session(session)

    def search(self, keyword: str, skip: int = 0, limit: int = 50) -> List[LoaiHang]:
        """Tìm kiếm loại hàng"""
        session = self._get_session()
        try:
            search_pattern = f"%{keyword}%"
            return session.query(LoaiHang).filter(
                LoaiHang.ma_loai.ilike(search_pattern) |
                LoaiHang.ten_loai.ilike(search_pattern)
            ).offset(skip).limit(limit).all()
        finally:
            self._close_session(session)

    def update(self, ma_loai: str, data: Dict[str, Any]) -> Optional[LoaiHang]:
        """Cập nhật loại hàng"""
        session = self._get_session()
        try:
            loai_hang = session.query(LoaiHang).filter(
                LoaiHang.ma_loai == ma_loai
            ).first()
            if not loai_hang:
                return None

            for key, value in data.items():
                if hasattr(loai_hang, key) and key not in ['ma_loai']:
                    setattr(loai_hang, key, value)

            loai_hang.ngay_cap_nhat = datetime.now()
            session.commit()
            session.refresh(loai_hang)
            return loai_hang

        except Exception as e:
            session.rollback()
            raise e
        finally:
            self._close_session(session)

    def delete(self, ma_loai: str) -> bool:
        """Xóa loại hàng"""
        session = self._get_session()
        try:
            loai_hang = self.get_by_id(ma_loai)
            if not loai_hang:
                return False

            session.delete(loai_hang)
            session.commit()
            return True

        except Exception as e:
            session.rollback()
            raise e
        finally:
            self._close_session(session)

    def get_by_ten_loai(self, ten_loai: str) -> Optional[LoaiHang]:
        """Lấy loại hàng theo tên"""
        session = self._get_session()
        try:
            return session.query(LoaiHang).filter(
                LoaiHang.ten_loai == ten_loai
            ).first()
        finally:
            self._close_session(session)

    def _generate_ma_loai(self) -> str:
        """Generate mã loại tự động"""
        session = self._get_session()
        try:
            last = session.query(LoaiHang).order_by(
                LoaiHang.ma_loai.desc()
            ).first()

            if last:
                try:
                    num = int(last.ma_loai.replace('LH', '')) + 1
                    return f"LH{num:03d}"
                except ValueError:
                    pass
            return "LH001"
        finally:
            self._close_session(session)


# Convenience functions
def create_loai_hang(data: Dict[str, Any]) -> LoaiHang:
    service = LoaiHangService()
    return service.create(data)


def get_loai_hang(ma_loai: str) -> Optional[LoaiHang]:
    service = LoaiHangService()
    return service.get_by_id(ma_loai)


def get_all_loai_hangs() -> List[LoaiHang]:
    service = LoaiHangService()
    return service.get_all()


def update_loai_hang(ma_loai: str, data: Dict[str, Any]) -> Optional[LoaiHang]:
    service = LoaiHangService()
    return service.update(ma_loai, data)


def delete_loai_hang(ma_loai: str) -> bool:
    service = LoaiHangService()
    return service.delete(ma_loai)


__all__ = [
    'LoaiHangService',
    'create_loai_hang',
    'get_loai_hang',
    'get_all_loai_hangs',
    'update_loai_hang',
    'delete_loai_hang',
]