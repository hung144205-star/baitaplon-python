"""
Base Service Class

Provides foundational session management and transaction support for all services.
"""
from abc import ABC, abstractmethod
from contextlib import contextmanager
from typing import Optional, Generic, TypeVar
from sqlalchemy.orm import Session

T = TypeVar('T')


class BaseService(ABC, Generic[T]):
    """
    Base service class with standardized session management.

    Features:
    - Accepts external session for transaction support
    - Creates own session if none provided (legacy compatibility)
    - Context manager support for transactions
    - Automatic cleanup

    Usage:
        class KhachHangService(BaseService[KhachHang]):
            def get_by_id(self, ma_khach_hang: str) -> Optional[KhachHang]:
                return self.session.query(KhachHang).filter(...)

        # Legacy usage (auto-creates session)
        service = KhachHangService()

        # Transaction-aware usage
        with transaction_context.begin() as session:
            service = KhachHangService(session=session)
            # operations use shared session
    """

    def __init__(self, session: Session = None):
        """Initialize service with optional external session.

        Args:
            session: Optional SQLAlchemy session. If not provided,
                    a new session will be created (legacy behavior).
        """
        self._session = session
        self._external_session = session is not None

    @property
    def session(self) -> Session:
        """Get the session, creating one if needed."""
        if self._session is None:
            from src.database import get_session
            self._session = get_session()
        return self._session

    def _close_session(self):
        """Close session if we created it ourselves."""
        if not self._external_session and self._session:
            self._session.close()
            self._session = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.session.rollback()
        self._close_session()
        return False

    def __del__(self):
        """Legacy cleanup (deprecated, use context manager)."""
        if hasattr(self, '_session') and self._session and not self._external_session:
            self._session.close()

    @contextmanager
    def transaction(self):
        """
        Context manager for explicit transactions.
        Use this for multi-service operations.

        Usage:
            with service.transaction() as session:
                # operations
                pass  # auto-commits on success

        Raises:
            Exception: Re-raises any exception after rollback
        """
        session = self.session
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise

    @abstractmethod
    def get_by_id(self, id_value) -> Optional[T]:
        """Get entity by primary key.

        Args:
            id_value: Primary key value

        Returns:
            Entity instance or None
        """
        pass