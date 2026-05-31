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
        data1 = sample_kho_data.copy()
        data1['ten_kho'] = 'Kho Test 1'
        kho1 = kho_service.create(data1)

        data2 = sample_kho_data.copy()
        data2['ten_kho'] = 'Kho Test 2'
        kho2 = kho_service.create(data2)

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

        with pytest.raises(ValueError, match="Trường 'ten_kho' là bắt buộc"):
            kho_service.create(data)

    def test_create_kho_invalid_dien_tich(self, kho_service, sample_kho_data):
        """Test creation with invalid dien_tich"""
        data = sample_kho_data.copy()
        data['dien_tich'] = 0
        data['ten_kho'] = 'Kho Invalid'

        with pytest.raises(ValueError, match="Trường 'dien_tich' là bắt buộc"):
            kho_service.create(data)

    def test_create_kho_invalid_suc_chua(self, kho_service, sample_kho_data):
        """Test creation with invalid suc_chua"""
        data = sample_kho_data.copy()
        data['suc_chua'] = -100
        data['ten_kho'] = 'Kho Invalid'

        with pytest.raises(ValueError, match="Sức chứa phải lớn hơn 0"):
            kho_service.create(data)


class TestKhoServiceGet:
    """Test KhoService retrieval methods"""

    def test_get_by_id_success(self, kho_service, sample_kho_data):
        """Test get_by_id with valid ID"""
        data = sample_kho_data.copy()
        data['ten_kho'] = 'Kho Get Test'
        created = kho_service.create(data)

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
        created = []
        for i in range(3):
            data = sample_kho_data.copy()
            data['ten_kho'] = f"Kho Test {i}"
            kho = kho_service.create(data)
            created.append(kho)

        khos = kho_service.get_all(limit=10)

        assert len(khos) >= 3

        # Cleanup
        for kho in created:
            kho_service.delete(kho.ma_kho)

    def test_get_all_with_pagination(self, kho_service, sample_kho_data):
        """Test get_all with pagination"""
        created = []
        for i in range(10):
            data = sample_kho_data.copy()
            data['ten_kho'] = f"Kho Test Page {i}"
            kho = kho_service.create(data)
            created.append(kho)

        page1 = kho_service.get_all(skip=0, limit=5)
        page2 = kho_service.get_all(skip=5, limit=5)

        assert len(page1) == 5
        assert len(page2) == 5

        # Cleanup
        for kho in created:
            kho_service.delete(kho.ma_kho)

    def test_get_all_filter_by_status(self, kho_service, sample_kho_data):
        """Test get_all with status filter"""
        data1 = sample_kho_data.copy()
        data1['ten_kho'] = 'Kho Active'
        active_kho = kho_service.create(data1)

        data2 = sample_kho_data.copy()
        data2['ten_kho'] = 'Kho Inactive'
        data2['trang_thai'] = TrangThaiKhoEnum.NGUNG
        inactive_kho = kho_service.create(data2)

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
        data = sample_kho_data.copy()
        data['ten_kho'] = 'Kho Test Search'
        kho = kho_service.create(data)

        results = kho_service.search('Kho Test')

        assert len(results) > 0
        assert any(k.ma_kho == kho.ma_kho for k in results)

        # Cleanup
        kho_service.delete(kho.ma_kho)

    def test_search_by_address(self, kho_service, sample_kho_data):
        """Test search by address"""
        data = sample_kho_data.copy()
        data['ten_kho'] = 'Kho Address Test'
        kho = kho_service.create(data)

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
        data = sample_kho_data.copy()
        data['ten_kho'] = 'Kho Update Test'
        created = kho_service.create(data)

        update_data = {
            'ten_kho': 'Kho Updated',
            'dien_tich': 1500.0,
        }

        updated = kho_service.update(created.ma_kho, update_data)

        assert updated.ten_kho == 'Kho Updated'
        assert updated.dien_tich == 1500.0
        assert updated.ma_kho == created.ma_kho

        # Cleanup
        kho_service.delete(created.ma_kho)

    def test_update_non_existent(self, kho_service):
        """Test update non-existent kho"""
        update_data = {'ten_kho': 'New Name'}

        result = kho_service.update('KHO999999', update_data)
        assert result is None


class TestKhoServiceDelete:
    """Test KhoService.delete()"""

    def test_delete_success(self, kho_service, sample_kho_data):
        """Test successful delete"""
        data = sample_kho_data.copy()
        data['ten_kho'] = 'Kho Delete Test'
        created = kho_service.create(data)

        success = kho_service.delete(created.ma_kho)
        assert success is True

        deleted = kho_service.get_by_id(created.ma_kho)
        assert deleted is None

    def test_delete_non_existent(self, kho_service):
        """Test delete non-existent kho"""
        success = kho_service.delete('KHO999999')
        assert success is False

    def test_delete_with_positions(self, kho_service, sample_kho_data):
        """Test delete kho with positions (should fail)"""
        from src.services import ViTriService

        data = sample_kho_data.copy()
        data['ten_kho'] = 'Kho With Position'
        created = kho_service.create(data)

        vi_tri_service = ViTriService()
        vi_tri_data = {
            'ma_kho': created.ma_kho,
            'khu_vuc': 'A',
            'hang': '01',
            'tang': 1,
            'dien_tich': 50.0,
            'gia_thue': 150000.0,
        }
        vi_tri = vi_tri_service.create(vi_tri_data)

        # Try to delete kho (should fail)
        with pytest.raises(ValueError, match="Không thể xóa kho"):
            kho_service.delete(created.ma_kho)

        # Cleanup
        vi_tri_service.delete(vi_tri.ma_vi_tri)
        kho_service.delete(created.ma_kho)


class TestKhoServiceBusinessLogic:
    """Test business logic methods"""

    def test_calculate_fill_rate(self, kho_service, sample_kho_data):
        """Test fill rate calculation"""
        data = sample_kho_data.copy()
        data['ten_kho'] = 'Kho Fill Rate'
        kho = kho_service.create(data)

        fill_rate = kho_service.calculate_fill_rate(kho.ma_kho)
        assert fill_rate == 0.0

        # Cleanup
        kho_service.delete(kho.ma_kho)

    def test_get_available_capacity(self, kho_service, sample_kho_data):
        """Test available capacity calculation"""
        data = sample_kho_data.copy()
        data['ten_kho'] = 'Kho Capacity'
        kho = kho_service.create(data)

        capacity = kho_service.get_available_capacity(kho.ma_kho)

        assert 'tong_dien_tich' in capacity
        assert 'da_su_dung' in capacity
        assert 'con_lai' in capacity
        assert 'so_vi_tri_trong' in capacity
        assert capacity['tong_dien_tich'] == 1000.0

        # Cleanup
        kho_service.delete(kho.ma_kho)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])