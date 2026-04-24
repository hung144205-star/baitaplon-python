"""
Database connection module
Quản lý kết nối database và session
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from contextlib import contextmanager
import os

# Get project root
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH = os.path.join(project_root, 'data', 'warehouse.db')

def get_database_url(db_path: str = None) -> str:
    """Get database URL"""
    if db_path is None:
        db_path = DB_PATH
    
    # Ensure directory exists
    db_dir = os.path.dirname(db_path)
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir)
    
    return f"sqlite:///{db_path}"

class DatabaseConnection:
    """
    Quản lý kết nối database
    Singleton pattern để đảm bảo chỉ có 1 engine
    """
    _instance = None
    _engine = None
    _SessionLocal = None
    
    def __new__(cls, db_path: str = None, echo: bool = False):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
        return cls._instance
    
    def __init__(self, db_path: str = None, echo: bool = False):
        if self._engine is None:
            self.db_path = db_path or DB_PATH
            self.echo = echo
            self._init_engine()
    
    def _init_engine(self):
        """Khởi tạo engine"""
        database_url = get_database_url(self.db_path)
        
        self._engine = create_engine(
            database_url,
            echo=self.echo,
            connect_args={'check_same_thread': False},  # For SQLite
            pool_pre_ping=True  # Enable connection health checks
        )
        
        # Create session factory
        self._SessionLocal = sessionmaker(bind=self._engine, autoflush=False, autocommit=False)
    
    def get_engine(self):
        """Lấy engine"""
        return self._engine
    
    def get_session(self) -> Session:
        """Lấy session mới"""
        return self._SessionLocal()
    
    @contextmanager
    def session_scope(self):
        """
        Context manager cho session
        Tự động commit nếu thành công, rollback nếu có lỗi
        """
        session = self._SessionLocal()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def close(self):
        """Đóng kết nối"""
        if self._engine:
            self._engine.dispose()

# Global instance
db_connection = None
_session_factory = None

def SessionLocal():
    """
    Get a new database session
    Compatibility function for services expecting SessionLocal
    
    Returns:
        Database session
    """
    conn = get_connection()
    return conn.get_session()

def get_connection(db_path: str = None, echo: bool = False) -> DatabaseConnection:
    """
    Lấy database connection (singleton)
    
    Args:
        db_path: Path to database file
        echo: If True, print SQL statements
    
    Returns:
        DatabaseConnection instance
    """
    global db_connection
    if db_connection is None:
        db_connection = DatabaseConnection(db_path, echo)
    return db_connection

def get_engine(db_path: str = None, echo: bool = False):
    """
    Get SQLAlchemy engine
    
    Args:
        db_path: Path to database file
        echo: If True, print SQL statements
    
    Returns:
        SQLAlchemy engine
    """
    conn = get_connection(db_path, echo)
    return conn.get_engine()

def get_session() -> Session:
    """
    Get database session
    
    Returns:
        Database session
    """
    conn = get_connection()
    return conn.get_session()

@contextmanager
def session_scope():
    """
    Context manager cho session
    Tự động commit/rollback/close
    
    Usage:
        with session_scope() as session:
            # do something with session
            session.add(obj)
    """
    conn = get_connection()
    with conn.session_scope() as session:
        yield session

__all__ = [
    'DatabaseConnection',
    'get_connection',
    'get_engine',
    'get_session',
    'session_scope',
    'get_database_url',
    'db_connection'
]
