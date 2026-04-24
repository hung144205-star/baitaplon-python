#!/usr/bin/env python3
"""
Pytest configuration and fixtures
"""
import pytest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))


@pytest.fixture(scope='session')
def test_database():
    """
    Setup test database
    Use a separate database for testing to avoid modifying production data
    """
    # TODO: Configure test database connection
    # For now, tests will use the production database
    # In the future, we should use an in-memory SQLite or separate test DB
    yield 'test_db'


@pytest.fixture(scope='function')
def cleanup_test_data():
    """
    Cleanup test data after each test
    """
    yield
    # Cleanup logic will be in individual test fixtures
    # This is a placeholder for future cleanup implementation
    pass


def pytest_configure(config):
    """Configure pytest"""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )


@pytest.fixture
def sample_kho_data():
    """Sample kho data for testing"""
    return {
        'ten_kho': 'Kho Test',
        'dia_chi': '123 Test St',
        'dien_tich': 1000.0,
        'suc_chua': 5000.0,
        'trang_thai': 'hoat_dong',
        'ghi_chu': 'Test kho'
    }


@pytest.fixture
def sample_vi_tri_data():
    """Sample vi_tri data for testing"""
    return {
        'ma_kho': 'KHO001',
        'khu_vuc': 'A',
        'hang': '01',
        'tang': 1,
        'dien_tich': 50.0,
        'chieu_cao': 3.0,
        'gia_thue': 150000.0,
        'trang_thai': 'trong'
    }
