#!/usr/bin/env python3
"""
Tests for ViTriService
"""
import pytest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.services import ViTriService, KhoService
from src.models import ViTri, Kho, TrangThaiViTriEnum, TrangThaiKhoEnum


@pytest.fixture
def vi_tri_service():
    """Create ViTriService instance"""
    return ViTriService()


@pytest.fixture
def kho_service():
    """Create KhoService instance"""
    return KhoService()


@pytest.fixture
def sample_kho(kho_service):
    """Create a sample kho for testing"""
    kho_data = {
        'ten_kho': 'Kho Test',
        'dia_chi': '123 Test St',
        'dien_tich': 1000.0,
        'suc_chua': 5000.0,
        'trang_thai': TrangThaiKhoEnum.HOAT_DONG,
    }
    kho = kho_service.create(kho_data)
    yield kho
    # Cleanup
    try:
        kho_service.delete(kho.ma_kho)
    except:
        pass


@pytest.fixture
def sample_vi_tri_data(sample_kho):
    """Sample vi_tri data for testing"""
    return {
        'ma_kho': sample_kho.ma_kho,
        'khu_vuc': 'A',
        'hang': '01',
        'tang': 1,
        'dien_tich': 50.0,
        'chieu_cao': 3.0,
        'gia_thue': 150000.0,
        'trang_thai': TrangThaiViTriEnum.TRONG,
    }


class TestViTriServiceCreate:
    """Test ViTriService.create()"""
    
    def test_create_vi_tri_success(self, vi_tri_service, sample_vi_tri_data):
        """Test successful vi_tri creation"""
        vi_tri = vi_tri_service.create(sample_vi_tri_data)
        
        assert vi_tri is not None
        assert vi_tri.ma_vi_tri.startswith('KHO')
        assert vi_tri.khu_vuc == sample_vi_tri_data['khu_vuc']
        assert vi_tri.hang == sample_vi_tri_data['hang']
        assert vi_tri.tang == sample_vi_tri_data['tang']
        assert vi_tri.dien_tich == sample_vi_tri_data['dien_tich']
        
        # Cleanup
        vi_tri_service.delete(vi_tri.ma_vi_tri)
    
    def test_create_vi_tri_auto_generate_ma_vi_tri(self, vi_tri_service, sample_vi_tri_data):
        """Test auto-generation of ma_vi_tri"""
        vi_tri1 = vi_tri_service.create(sample_vi_tri_data)
        
        # Modify position slightly for second creation
        sample_vi_tri_data['hang'] = '02'
        vi_tri2 = vi_tri_service.create(sample_vi_tri_data)
        
        assert vi_tri1.ma_vi_tri != vi_tri2.ma_vi_tri
        assert vi_tri1.ma_vi_tri.startswith('KHO')
        assert vi_tri2.ma_vi_tri.startswith('KHO')
        
        # Cleanup
        vi_tri_service.delete(vi_tri1.ma_vi_tri)
        vi_tri_service.delete(vi_tri2.ma_vi_tri)
    
    def test_create_vi_tri_missing_ma_kho(self, vi_tri_service):
        """Test creation with missing ma_kho"""
        data = {
            'khu_vuc': 'A',
            'hang': '01',
            'tang': 1,
            'dien_tich': 50.0,
        }
        
        with pytest.raises(ValueError, match="Mã kho không được để trống"):
            vi_tri_service.create(data)
    
    def test_create_vi_tri_invalid_dien_tich(self, vi_tri_service, sample_vi_tri_data):
        """Test creation with invalid dien_tich"""
        sample_vi_tri_data['dien_tich'] = 0
        
        with pytest.raises(ValueError, match="Diện tích phải lớn hơn 0"):
            vi_tri_service.create(sample_vi_tri_data)
    
    def test_create_vi_tri_invalid_gia_thue(self, vi_tri_service, sample_vi_tri_data):
        """Test creation with invalid gia_thue"""
        sample_vi_tri_data['gia_thue'] = -1000
        
        with pytest.raises(ValueError, match="Giá thuê không được âm"):
            vi_tri_service.create(sample_vi_tri_data)
    
    def test_create_vi_tri_kho_not_found(self, vi_tri_service, sample_vi_tri_data):
        """Test creation with non-existent kho"""
        sample_vi_tri_data['ma_kho'] = 'KHO999999'
        
        with pytest.raises(ValueError, match="Không tìm thấy kho"):
            vi_tri_service.create(sample_vi_tri_data)


class TestViTriServiceGet:
    """Test ViTriService retrieval methods"""
    
    def test_get_by_id_success(self, vi_tri_service, sample_vi_tri_data):
        """Test get_by_id with valid ID"""
        created = vi_tri_service.create(sample_vi_tri_data)
        
        retrieved = vi_tri_service.get_by_id(created.ma_vi_tri)
        
        assert retrieved is not None
        assert retrieved.ma_vi_tri == created.ma_vi_tri
        assert retrieved.khu_vuc == created.khu_vuc
        
        # Cleanup
        vi_tri_service.delete(created.ma_vi_tri)
    
    def test_get_by_id_not_found(self, vi_tri_service):
        """Test get_by_id with invalid ID"""
        vi_tri = vi_tri_service.get_by_id('KHO999-A-01-01-001')
        assert vi_tri is None
    
    def test_get_vi_tri_by_kho(self, vi_tri_service, sample_kho, sample_vi_tri_data):
        """Test get_vi_tri_by_kho"""
        # Create multiple positions
        created = []
        for i in range(3):
            data = sample_vi_tri_data.copy()
            data['hang'] = f'{i+1:02d}'
            vi_tri = vi_tri_service.create(data)
            created.append(vi_tri)
        
        # Get by kho
        vi_tris = vi_tri_service.get_vi_tri_by_kho(sample_kho.ma_kho)
        
        assert len(vi_tris) >= 3
        assert all(v.ma_kho == sample_kho.ma_kho for v in vi_tris)
        
        # Cleanup
        for vt in created:
            vi_tri_service.delete(vt.ma_vi_tri)
    
    def test_get_all_with_pagination(self, vi_tri_service, sample_kho, sample_vi_tri_data):
        """Test get_all with pagination"""
        # Create test data
        created = []
        for i in range(10):
            data = sample_vi_tri_data.copy()
            data['hang'] = f'{i+1:02d}'
            vi_tri = vi_tri_service.create(data)
            created.append(vi_tri)
        
        # Get first page
        page1 = vi_tri_service.get_all(skip=0, limit=5)
        page2 = vi_tri_service.get_all(skip=5, limit=5)
        
        assert len(page1) == 5
        assert len(page2) == 5
        
        # Cleanup
        for vt in created:
            vi_tri_service.delete(vt.ma_vi_tri)


class TestViTriServiceSearch:
    """Test ViTriService.search()"""
    
    def test_search_by_khu_vuc(self, vi_tri_service, sample_kho, sample_vi_tri_data):
        """Test search by khu_vuc"""
        created = vi_tri_service.create(sample_vi_tri_data)
        
        results = vi_tri_service.search('Khu A', sample_kho.ma_kho)
        
        assert len(results) > 0
        assert any(v.ma_vi_tri == created.ma_vi_tri for v in results)
        
        # Cleanup
        vi_tri_service.delete(created.ma_vi_tri)
    
    def test_search_no_results(self, vi_tri_service, sample_kho):
        """Test search with no results"""
        results = vi_tri_service.search('ViTriKhongTonTai12345', sample_kho.ma_kho)
        assert len(results) == 0


class TestViTriServiceUpdate:
    """Test ViTriService.update()"""
    
    def test_update_success(self, vi_tri_service, sample_vi_tri_data):
        """Test successful update"""
        created = vi_tri_service.create(sample_vi_tri_data)
        
        update_data = {
            'dien_tich': 75.0,
            'gia_thue': 200000.0,
        }
        
        updated = vi_tri_service.update(created.ma_vi_tri, update_data)
        
        assert updated.dien_tich == 75.0
        assert updated.gia_thue == 200000.0
        assert updated.ma_vi_tri == created.ma_vi_tri
        
        # Cleanup
        vi_tri_service.delete(created.ma_vi_tri)
    
    def test_update_non_existent(self, vi_tri_service, sample_vi_tri_data):
        """Test update non-existent vi_tri"""
        update_data = {'dien_tich': 100.0}
        
        with pytest.raises(ValueError, match="Không tìm thấy vị trí"):
            vi_tri_service.update('KHO999-A-01-01-001', update_data)


class TestViTriServiceDelete:
    """Test ViTriService.delete()"""
    
    def test_delete_success(self, vi_tri_service, sample_vi_tri_data):
        """Test successful delete"""
        created = vi_tri_service.create(sample_vi_tri_data)
        
        success = vi_tri_service.delete(created.ma_vi_tri)
        assert success is True
        
        # Verify deleted
        deleted = vi_tri_service.get_by_id(created.ma_vi_tri)
        assert deleted is None
    
    def test_delete_non_existent(self, vi_tri_service):
        """Test delete non-existent vi_tri"""
        success = vi_tri_service.delete('KHO999-A-01-01-001')
        assert success is False


class TestViTriServiceBusinessLogic:
    """Test business logic methods"""
    
    def test_get_available_positions(self, vi_tri_service, sample_kho, sample_vi_tri_data):
        """Test get_available"""
        # Create positions with different statuses
        trong_data = sample_vi_tri_data.copy()
        trong_data['hang'] = '01'
        trong_data['trang_thai'] = TrangThaiViTriEnum.TRONG
        trong_vt = vi_tri_service.create(trong_data)
        
        da_thue_data = sample_vi_tri_data.copy()
        da_thue_data['hang'] = '02'
        da_thue_data['trang_thai'] = TrangThaiViTriEnum.DA_THUE
        da_thue_vt = vi_tri_service.create(da_thue_data)
        
        # Get available
        available = vi_tri_service.get_available(sample_kho.ma_kho)
        
        assert len(available) >= 1
        assert any(v.ma_vi_tri == trong_vt.ma_vi_tri for v in available)
        assert not any(v.ma_vi_tri == da_thue_vt.ma_vi_tri for v in available)
        
        # Cleanup
        vi_tri_service.delete(trong_vt.ma_vi_tri)
        vi_tri_service.delete(da_thue_vt.ma_vi_tri)
    
    def test_get_statistics(self, vi_tri_service, sample_kho, sample_vi_tri_data):
        """Test get_statistics"""
        # Create positions with different statuses
        for i in range(3):
            data = sample_vi_tri_data.copy()
            data['hang'] = f'{i+1:02d}'
            if i == 0:
                data['trang_thai'] = TrangThaiViTriEnum.TRONG
            else:
                data['trang_thai'] = TrangThaiViTriEnum.DA_THUE
            vi_tri_service.create(data)
        
        # Get statistics
        stats = vi_tri_service.get_statistics(sample_kho.ma_kho)
        
        assert 'tong_so_vi_tri' in stats
        assert 'so_vi_tri_trong' in stats
        assert 'so_vi_tri_da_thue' in stats
        assert 'ty_le_trong' in stats
        assert 'ty_le_da_thue' in stats
        
        assert stats['tong_so_vi_tri'] >= 3
        assert stats['so_vi_tri_trong'] >= 1
        assert stats['so_vi_tri_da_thue'] >= 2
    
    def test_update_status(self, vi_tri_service, sample_vi_tri_data):
        """Test update_status"""
        created = vi_tri_service.create(sample_vi_tri_data)
        
        # Update status
        updated = vi_tri_service.update_status(created.ma_vi_tri, TrangThaiViTriEnum.DA_THUE)
        
        assert updated.trang_thai == TrangThaiViTriEnum.DA_THUE
        
        # Cleanup
        vi_tri_service.delete(created.ma_vi_tri)


class TestViTriServiceFindAvailable:
    """Test ViTriService.find_available_by_requirements()"""
    
    def test_find_by_requirements(self, vi_tri_service, sample_kho, sample_vi_tri_data):
        """Test find_available_by_requirements"""
        # Create positions with different specs
        data1 = sample_vi_tri_data.copy()
        data1['hang'] = '01'
        data1['dien_tich'] = 50.0
        data1['gia_thue'] = 150000.0
        vt1 = vi_tri_service.create(data1)
        
        data2 = sample_vi_tri_data.copy()
        data2['hang'] = '02'
        data2['dien_tich'] = 100.0
        data2['gia_thue'] = 250000.0
        vt2 = vi_tri_service.create(data2)
        
        # Find with requirements
        results = vi_tri_service.find_available_by_requirements(
            ma_kho=sample_kho.ma_kho,
            dien_tich_min=50.0,
            gia_thue_max=200000.0
        )
        
        assert len(results) >= 1
        assert any(v.ma_vi_tri == vt1.ma_vi_tri for v in results)
        # vt2 should not be included (gia_thue > 200000)
        assert not any(v.ma_vi_tri == vt2.ma_vi_tri for v in results)
        
        # Cleanup
        vi_tri_service.delete(vt1.ma_vi_tri)
        vi_tri_service.delete(vt2.ma_vi_tri)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
