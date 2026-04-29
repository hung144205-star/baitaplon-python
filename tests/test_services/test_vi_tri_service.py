"""
Test suite cho ViTri Service
"""
import pytest
from datetime import date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.models import Kho, ViTri, Base, TrangThaiKhoEnum, TrangThaiViTriEnum
from src.services import ViTriService


@pytest.fixture
def test_engine():
    """Create in-memory test database"""
    engine = create_engine('sqlite:///:memory:', echo=False)
    Base.metadata.create_all(engine)
    return engine


@pytest.fixture
def test_session(test_engine):
    """Create test session"""
    Session = sessionmaker(bind=test_engine)
    session = Session()
    yield session
    session.close()


@pytest.fixture
def sample_kho(test_session):
    """Create sample warehouse"""
    kho = Kho(
        ma_kho='KHO001',
        ten_kho='Kho Test',
        dia_chi='123 Test St',
        dien_tich=1000.0,
        suc_chua=5000.0,
        da_su_dung=0.0,
        trang_thai=TrangThaiKhoEnum.HOAT_DONG,
    )
    test_session.add(kho)
    test_session.commit()
    return kho


@pytest.fixture
def vi_tri_service(test_session):
    """Create ViTriService with test session"""
    return ViTriService(session=test_session)


@pytest.fixture
def sample_vi_tri_data():
    """Sample position data for testing"""
    return {
        'ma_vi_tri': 'VT001',
        'ma_kho': 'KHO001',
        'khu_vuc': 'A',
        'hang': '01',
        'tang': 1,
        'dien_tich': 50.0,
        'gia_thue': 1500000.0,
        'suc_chua': 1000.0,
        'trang_thai': TrangThaiViTriEnum.TRONG,
    }


class TestViTriServiceCreate:
    """Test ViTriService.create()"""
    
    def test_create_success(self, vi_tri_service, sample_vi_tri_data):
        """Test successful creation"""
        vt = vi_tri_service.create(sample_vi_tri_data)
        
        assert vt.ma_vi_tri == 'VT001'
        assert vt.khu_vuc == 'A'
        assert vt.hang == '01'
        assert vt.tang == 1
        assert vt.dien_tich == 50.0
        assert vt.gia_thue == 1500000.0
    
    def test_create_auto_generate_ma(self, vi_tri_service, sample_vi_tri_data, sample_kho):
        """Test auto-generate position ID"""
        # Remove ma_vi_tri to trigger auto-generate
        del sample_vi_tri_data['ma_vi_tri']
        
        vt = vi_tri_service.create(sample_vi_tri_data)
        
        assert vt.ma_vi_tri is not None
        assert 'VT' in vt.ma_vi_tri or 'A' in vt.ma_vi_tri  # Depends on generator
    
    def test_create_invalid_kho(self, vi_tri_service, sample_vi_tri_data):
        """Test creation with non-existent warehouse"""
        sample_vi_tri_data['ma_kho'] = 'KHO_NON_EXISTENT'
        
        with pytest.raises(ValueError, match="không tồn tại"):
            vi_tri_service.create(sample_vi_tri_data)
    
    def test_create_duplicate_ma(self, vi_tri_service, sample_vi_tri_data, sample_kho):
        """Test duplicate position ID"""
        vi_tri_service.create(sample_vi_tri_data)
        
        # Try to create another with same ma_vi_tri
        sample_vi_tri_data['khu_vuc'] = 'B'
        with pytest.raises(ValueError, match="đã tồn tại"):
            vi_tri_service.create(sample_vi_tri_data)


class TestViTriServiceGet:
    """Test ViTriService.get_*() methods"""
    
    def test_get_by_id_success(self, vi_tri_service, sample_vi_tri_data, sample_kho):
        """Test get by ID"""
        vi_tri_service.create(sample_vi_tri_data)
        
        vt = vi_tri_service.get_by_id('VT001')
        
        assert vt is not None
        assert vt.ma_vi_tri == 'VT001'
    
    def test_get_by_id_not_found(self, vi_tri_service):
        """Test get by non-existent ID"""
        vt = vi_tri_service.get_by_id('VT_NON_EXISTENT')
        
        assert vt is None
    
    def test_get_all(self, vi_tri_service, sample_vi_tri_data, sample_kho):
        """Test get all positions"""
        # Create multiple positions
        for i in range(5):
            sample_vi_tri_data['ma_vi_tri'] = f'VT00{i}'
            sample_vi_tri_data['khu_vuc'] = chr(ord('A') + i)
            vi_tri_service.create(sample_vi_tri_data)
        
        all_vt = vi_tri_service.get_all()
        
        assert len(all_vt) == 5
    
    def test_get_by_kho(self, vi_tri_service, sample_vi_tri_data, sample_kho):
        """Test get positions by warehouse"""
        vi_tri_service.create(sample_vi_tri_data)
        
        positions = vi_tri_service.get_by_kho('KHO001')
        
        assert len(positions) >= 1
        assert all(vt.ma_kho == 'KHO001' for vt in positions)


class TestViTriServiceUpdate:
    """Test ViTriService.update()"""
    
    def test_update_success(self, vi_tri_service, sample_vi_tri_data, sample_kho):
        """Test successful update"""
        vt = vi_tri_service.create(sample_vi_tri_data)
        
        updated = vi_tri_service.update('VT001', {
            'khu_vuc': 'B',
            'gia_thue': 2000000.0
        })
        
        assert updated.khu_vuc == 'B'
        assert updated.gia_thue == 2000000.0
    
    def test_update_not_found(self, vi_tri_service):
        """Test update non-existent position"""
        result = vi_tri_service.update('VT_NON_EXISTENT', {'khu_vuc': 'B'})
        
        assert result is None


class TestViTriServiceDelete:
    """Test ViTriService.delete()"""
    
    def test_delete_success(self, vi_tri_service, sample_vi_tri_data, sample_kho):
        """Test successful deletion"""
        vi_tri_service.create(sample_vi_tri_data)
        
        result = vi_tri_service.delete('VT001')
        
        assert result is True
        
        # Verify deleted
        vt = vi_tri_service.get_by_id('VT001')
        assert vt is None
    
    def test_delete_not_found(self, vi_tri_service):
        """Test delete non-existent position"""
        result = vi_tri_service.delete('VT_NON_EXISTENT')
        
        assert result is False


class TestViTriServiceSearch:
    """Test ViTriService.search()"""
    
    def test_search_by_khu_vuc(self, vi_tri_service, sample_vi_tri_data, sample_kho):
        """Test search by area"""
        vi_tri_service.create(sample_vi_tri_data)
        
        results = vi_tri_service.search('A')
        
        assert len(results) >= 1
    
    def test_search_no_results(self, vi_tri_service, sample_vi_tri_data, sample_kho):
        """Test search with no results"""
        vi_tri_service.create(sample_vi_tri_data)
        
        results = vi_tri_service.search('NON_EXISTENT')
        
        assert len(results) == 0


class TestViTriServiceStatus:
    """Test ViTriService status-related methods"""
    
    def test_get_trong(self, vi_tri_service, sample_vi_tri_data, sample_kho):
        """Test get available positions"""
        vi_tri_service.create(sample_vi_tri_data)
        
        available = vi_tri_service.get_trong()
        
        assert len(available) >= 1
        assert all(vt.trang_thai == TrangThaiViTriEnum.TRONG for vt in available)
    
    def test_get_da_thue(self, vi_tri_service, sample_vi_tri_data, sample_kho):
        """Test get rented positions"""
        # Create rented position
        sample_vi_tri_data['trang_thai'] = TrangThaiViTriEnum.DA_THUE
        vi_tri_service.create(sample_vi_tri_data)
        
        rented = vi_tri_service.get_da_thue()
        
        assert len(rented) >= 1
        assert all(vt.trang_thai == TrangThaiViTriEnum.DA_THUE for vt in rented)


# Run tests with: pytest tests/test_services/test_vi_tri_service.py -v
