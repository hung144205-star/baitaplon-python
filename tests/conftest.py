"""
Test configuration and fixtures
"""
import pytest
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))


@pytest.fixture(scope='function', autouse=True)
def reset_db_connection():
    """Reset database connection before each test"""
    import src.database.connection as db_conn
    # Reset singleton so each test gets fresh connection
    db_conn.db_connection = None
    yield
    # Cleanup after test
    db_conn.db_connection = None


@pytest.fixture(scope='function')
def clean_db():
    """Provide clean database for tests"""
    import src.database.connection as db_conn
    from src.models import Base

    # Reset connection
    db_conn.db_connection = None
    conn = db_conn.get_connection()

    # Create all tables
    Base.metadata.create_all(conn.get_engine())

    yield conn

    # Cleanup - drop all tables after test
    Base.metadata.drop_all(conn.get_engine())
    db_conn.db_connection = None