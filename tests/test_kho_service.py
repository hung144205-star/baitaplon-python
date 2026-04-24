#!/usr/bin/env python3
"""
Tests for KhoService
"""
import pytest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.services import KhoService
from src.models import Kho, TrangThaiKhoEnum


@pytest.fixture
def kho_service():
    """Create KhoService instance"""
    return KhoService()


@pytest.fixture
def sample_kho_data():
    """Sample kho data for testing"""
    return {
        'ten_kho': 'Kho Test A',
        'dia_chi': '123 Đường Test, Quận 7, TP.HCM',
        'dien_tich': 1000.0,
        'suc_chua': 5000.0,
        'trang_thai': TrangThaiKhoEnum.HOAT_DONG,
        'ghi_chu': 'Kho test unit tests'
    }


class TestKhoServiceCreate:
    """Test KhoService.create()"""
    
    def test_create_kho_success(self, kho_service, sample_kho_data):
        """Test successful kho creation"""
        kho = kho_service.create(sample_kho_data)
        
        assert kho is not None
        assert kho.ma_kho.startswith('KHO')
        assert kho.ten_kho == sample_kho_data['ten_kho']
        assert kho.dia_chi == sample_kho_data['dia_chi']
        assert kho.dien_tich == sample_kho_data['dien_tich']
        assert kho.suc_chua == sample_kho_data['suc_chua']
        assert kho.trang_thai == sample_kho_data['trang_thai']
        
        # Cleanup
        kho_service.delete(kho.ma_kho)
    
    def test_create_kho_auto_generate_ma_kho(self, kho_service, sample_kho_data):
        """Test auto-generation of ma_kho"""
        kho1 = kho_service.create(sample_kho_data)
        kho2 = kho_service.create(sample_kho_data)
        
        assert kho1.ma_kho != kho2.ma_kho
        assert kho1.ma_kho.startswith('KHO')
        assert kho2.ma_kho.startswith('KHO')
        
        # Cleanup
        kho_service.delete(kho1.ma_kho)
        kho_service.delete(kho2.ma_kho)
    
    def test_create_kho_missing_ten_kho(self, kho_service):
        """Test creation with missing ten_kho"""
        data = {
            'dia_chi': '123 Test St',
            'dien_tich': 100.0,
            'suc_chua': 500.0,
        }
        
        with pytest.raises(ValueError, match="Tên kho không được để trống"):
            kho_service.create(data)
    
    def test_create_kho_invalid_dien_tich(self, kho_service, sample_kho_data):
        """Test creation with invalid dien_tich"""
        sample_kho_data['dien_tich'] = 0
        
        with pytest.raises(ValueError, match="Diện tích phải lớn hơn 0"):
            kho_service.create(sample_kho_data)
    
    def test_create_kho_invalid_suc_chua(self, kho_service, sample_kho_data):
        """Test creation with invalid suc_chua"""
        sample_kho_data['suc_chua'] = -100
        
        with pytest.raises(ValueError, match="Sức chứa phải lớn hơn 0"):
            kho_service.create(sample_kho_data)


class TestKhoServiceGet:
    """Test KhoService retrieval methods"""
    
    def test_get_by_id_success(self, kho_service, sample_kho_data):
        """Test get_by_id with valid ID"""
        created = kho_service.create(sample_kho_data)
        
        retrieved = kho_service.get_by_id(created.ma_kho)
        
        assert retrieved is not None
        assert retrieved.ma_kho == created.ma_kho
        assert retrieved.ten_kho == created.ten_kho
        
        # Cleanup
        kho_service.delete(created.ma_kho)
    
    def test_get_by_id_not_found(self, kho_service):
        """Test get_by_id with invalid ID"""
        kho = kho_service.get_by_id('KHO999999')
        assert kho is None
    
    def test_get_all_success(self, kho_service, sample_kho_data):
        """Test get_all"""
        # Create test data
        created = []
        for i in range(3):
            data = sample_kho_data.copy()
            data['ten_kho'] = f"Kho Test {i}"
            kho = kho_service.create(data)
            created.append(kho)
        
        # Get all
        khos = kho_service.get_all(limit=10)
        
        assert len(khos) >= 3
        
        # Cleanup
        for kho in created:
            kho_service.delete(kho.ma_kho)
    
    def test_get_all_with_pagination(self, kho_service, sample_kho_data):
        """Test get_all with pagination"""
        # Create test data
        created = []
        for i in range(10):
            data = sample_kho_data.copy()
            data['ten_kho'] = f"Kho Test {i}"
            kho = kho_service.create(data)
            created.append(kho)
        
        # Get first page
        page1 = kho_service.get_all(skip=0, limit=5)
        page2 = kho_service.get_all(skip=5, limit=5)
        
        assert len(page1) == 5
        assert len(page2) == 5
        
        # Cleanup
        for kho in created:
            kho_service.delete(kho.ma_kho)
    
    def test_get_all_filter_by_status(self, kho_service, sample_kho_data):
        """Test get_all with status filter"""
        # Create test data with different statuses
        active_kho = kho_service.create(sample_kho_data)
        
        inactive_data = sample_kho_data.copy()
        inactive_data['ten_kho'] = 'Kho Inactive'
        inactive_data['trang_thai'] = TrangThaiKhoEnum.NGUNG
        inactive_kho = kho_service.create(inactive_data)
        
        # Get active only
        active_khos = kho_service.get_all(trang_thai=TrangThaiKhoEnum.HOAT_DONG)
        assert len(active_khos) >= 1
        assert any(k.ma_kho == active_kho.ma_kho for k in active_khos)
        
        # Cleanup
        kho_service.delete(active_kho.ma_kho)
        kho_service.delete(inactive_kho.ma_kho)


class TestKhoServiceSearch:
    """Test KhoService.search()"""
    
    def test_search_by_name(self, kho_service, sample_kho_data):
        """Test search by kho name"""
        kho = kho_service.create(sample_kho_data)
        
        results = kho_service.search('Kho Test')
        
        assert len(results) > 0
        assert any(k.ma_kho == kho.ma_kho for k in results)
        
        # Cleanup
        kho_service.delete(kho.ma_kho)
    
    def test_search_by_address(self, kho_service, sample_kho_data):
        """Test search by address"""
        kho = kho_service.create(sample_kho_data)
        
        results = kho_service.search('Quận 7')
        
        assert len(results) > 0
        assert any(k.ma_kho == kho.ma_kho for k in results)
        
        # Cleanup
        kho_service.delete(kho.ma_kho)
    
    def test_search_no_results(self, kho_service):
        """Test search with no results"""
        results = kho_service.search('KhoKhongTonTai12345')
        assert len(results) == 0


class TestKhoServiceUpdate:
    """Test KhoService.update()"""
    
    def test_update_success(self, kho_service, sample_kho_data):
        """Test successful update"""
        created = kho_service.create(sample_kho_data)
        
        update_data = {
            'ten_kho': 'Kho Updated',
            'dien_tich': 1500.0,
        }
        
        updated = kho_service.update(created.ma_kho, update_data)
        
        assert updated.ten_kho == 'Kho Updated'
        assert updated.dien_tich == 1500.0
        assert updated.ma_kho == created.ma_kho  # ma_kho should not change
        
        # Cleanup
        kho_service.delete(created.ma_kho)
    
    def test_update_non_existent(self, kho_service, sample_kho_data):
        """Test update non-existent kho"""
        update_data = {'ten_kho': 'New Name'}
        
        with pytest.raises(ValueError, match="Không tìm thấy kho"):
            kho_service.update('KHO999999', update_data)


class TestKhoServiceDelete:
    """Test KhoService.delete()"""
    
    def test_delete_success(self, kho_service, sample_kho_data):
        """Test successful delete"""
        created = kho_service.create(sample_kho_data)
        
        success = kho_service.delete(created.ma_kho)
        assert success is True
        
        # Verify deleted
        deleted = kho_service.get_by_id(created.ma_kho)
        assert deleted is None
    
    def test_delete_non_existent(self, kho_service):
        """Test delete non-existent kho"""
        success = kho_service.delete('KHO999999')
        assert success is False
    
    def test_delete_with_positions(self, kho_service, sample_kho_data):
        """Test delete kho with positions (should fail)"""
        from src.services import ViTriService
        
        created = kho_service.create(sample_kho_data)
        
        # Create a position in this kho
        vi_tri_service = ViTriService()
        vi_tri_data = {
            'ma_kho': created.ma_kho,
            'khu_vuc': 'A',
            'hang': '01',
            'tang': 1,
            'dien_tich': 50.0,
            'gia_thue': 150000.0,
        }
        vi_tri_service.create(vi_tri_data)
        
        # Try to delete kho (should fail)
        with pytest.raises(ValueError, match="Không thể xóa kho"):
            kho_service.delete(created.ma_kho)
        
        # Cleanup
        vi_tri_service.delete('KHO001-A-01-01-001')  # This might fail if ma_vi_tri is different
        kho_service.delete(created.ma_kho)


class TestKhoServiceBusinessLogic:
    """Test business logic methods"""
    
    def test_calculate_fill_rate(self, kho_service, sample_kho_data):
        """Test fill rate calculation"""
        kho = kho_service.create(sample_kho_data)
        
        # Initially fill rate should be 0
        fill_rate = kho_service.calculate_fill_rate(kho.ma_kho)
        assert fill_rate == 0.0
        
        # Cleanup
        kho_service.delete(kho.ma_kho)
    
    def test_get_available_capacity(self, kho_service, sample_kho_data):
        """Test available capacity calculation"""
        kho = kho_service.create(sample_kho_data)
        
        capacity = kho_service.get_available_capacity(kho.ma_kho)
        
        assert 'tong_dien_tich' in capacity
        assert 'da_su_dung' in capacity
        assert 'con_lai' in capacity
        assert 'so_vi_tri_trong' in capacity
        assert capacity['tong_dien_tich'] == 1000.0
        
        # Cleanup
        kho_service.delete(kho.ma_kho)


class TestKhoServiceGetByStatus:
    """Test KhoService.get_by_status()"""
    
    def test_get_by_status_success(self, kho_service, sample_kho_data):
        """Test get_by_status"""
        active_kho = kho_service.create(sample_kho_data)
        
        inactive_data = sample_kho_data.copy()
        inactive_data['ten_kho'] = 'Kho Inactive'
        inactive_data['trang_thai'] = TrangThaiKhoEnum.NGUNG
        inactive_kho = kho_service.create(inactive_data)
        
        # Get active
        active_khos = kho_service.get_by_status(TrangThaiKhoEnum.HOAT_DONG)
        assert len(active_khos) >= 1
        
        # Get inactive
        inactive_khos = kho_service.get_by_status(TrangThaiKhoEnum.NGUNG)
        assert len(inactive_khos) >= 1
        
        # Cleanup
        kho_service.delete(active_kho.ma_kho)
        kho_service.delete(inactive_kho.ma_kho)


class TestKhoServiceGetHistory:
    """Test KhoService.get_history()"""
    
    def test_get_history_success(self, kho_service, sample_kho_data):
        """Test get_history"""
        kho = kho_service.create(sample_kho_data)
        
        history = kho_service.get_history(kho.ma_kho)
        
        assert 'kho' in history
        assert 'so_vi_tri' in history
        assert 'fill_rate' in history
        
        # Cleanup
        kho_service.delete(kho.ma_kho)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
