"""
Transaction Context for Multi-Service Operations

Provides shared session management for operations that span multiple services.
"""
from contextlib import contextmanager
from functools import wraps
from typing import Optional, Callable, Any
from sqlalchemy.orm import Session

from src.database import get_connection, get_session


class TransactionContext:
    """
    Manages shared database sessions for multi-service operations.

    This is a singleton that provides transaction-aware session management.

    Usage:
        # Simple usage
        with TransactionContext() as session:
            hop_dong_service = HopDongService(session=session)
            thanh_toan_service = ThanhToanService(session=session)
            # Both services share the same session - commit together or rollback together

        # Decorator usage for functions that need transactional behavior
        @transactional
        def create_contract_with_payment(session: Session, contract_data: dict, payment_data: dict):
            hop_dong_service = HopDongService(session=session)
            thanh_toan_service = ThanhToanService(session=session)
            # ...
    """

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._session = None
        return cls._instance

    @contextmanager
    def begin(self, db_path: str = None):
        """
        Begin a transaction with shared session.

        Usage:
            with tx.begin() as session:
                service1 = Service1(session=session)
                service2 = Service2(session=session)
                # operations

        Args:
            db_path: Optional database path override

        Yields:
            Session: Shared database session

        Raises:
            Exception: Re-raises after rollback on error
        """
        connection = get_connection(db_path)
        self._session = connection.get_session()

        try:
            yield self._session
            self._session.commit()
        except Exception as e:
            self._session.rollback()
            raise e
        finally:
            self._session.close()
            self._session = None

    def get_session(self) -> Optional[Session]:
        """Get the current shared session if inside a transaction."""
        return self._session

    def is_active(self) -> bool:
        """Check if there's an active transaction."""
        return self._session is not None


# Global transaction manager instance
tx = TransactionContext()


def transactional(func: Callable) -> Callable:
    """
    Decorator for functions that need transactional behavior.

    Usage:
        @transactional
        def my_operation(session: Session, arg1, arg2):
            service = MyService(session=session)
            service.create(arg1)
            # ...

    Args:
        func: Function that takes session as first or keyword argument

    Returns:
        Wrapped function that automatically handles transaction lifecycle
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        session = kwargs.get('session')
        if session is None:
            # Check if there's already an active transaction
            if tx.is_active():
                # Use existing transaction
                kwargs['session'] = tx.get_session()
                return func(*args, **kwargs)
            else:
                # Create new transaction
                with tx.begin() as new_session:
                    kwargs['session'] = new_session
                    return func(*args, **kwargs)
        else:
            # Session provided - use as-is (caller manages transaction)
            return func(*args, **kwargs)

    return wrapper


__all__ = ['TransactionContext', 'tx', 'transactional']