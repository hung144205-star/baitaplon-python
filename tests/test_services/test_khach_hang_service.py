"""
Test suite cho KhachHang Service
"""
import pytest
from datetime import date, datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.models import KhachHang, Base, LoaiKhachEnum, TrangThaiKHEnum
from src.services import KhachHangService, create_khach_hang, get_khach_hang


# Test database setup
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
def khach_hang_service(test_session):
    """Create KhachHangService with test session"""
    return KhachHangService(session=test_session)


@pytest.fixture
def sample_khach_hang_data():
    """Sample customer data for testing"""
    return {
        'ho_ten': 'Nguyễn Văn A',
        'loai_khach': LoaiKhachEnum.CA_NHAN,
        'so_dien_thoai': '0901234567',
        'email': 'nguyenvana@email.com',
        'dia_chi': '123 Nguyễn Văn Linh, Q7, TP.HCM',
        'ma_so_thue': None,
        'ngay_dang_ky': date.today(),
        'trang_thai': TrangThaiKHEnum.HOAT_DONG,
    }


class TestKhachHangServiceCreate:
    """Test KhachHangService.create()"""
    
    def test_create_success(self, khach_hang_service, sample_khach_hang_data):
        """Test successful creation"""
        kh = khach_hang_service.create(sample_khach_hang_data)
        
        assert kh.ma_khach_hang.startswith('KH')
        assert kh.ho_ten == sample_khach_hang_data['ho_ten']
        assert kh.so_dien_thoai == sample_khach_hang_data['so_dien_thoai']
        assert kh.email == sample_khach_hang_data['email']
    
    def test_create_auto_generate_ma(self, khach_hang_service, sample_khach_hang_data):
        """Test auto-generate customer ID"""
        kh1 = khach_hang_service.create(sample_khach_hang_data)
        
        sample_khach_hang_data['email'] = 'test2@email.com'
        sample_khach_hang_data['so_dien_thoai'] = '0909876543'
        kh2 = khach_hang_service.create(sample_khach_hang_data)
        
        assert kh1.ma_khach_hang != kh2.ma_khach_hang
        assert kh1.ma_khach_hang.startswith('KH')
        assert kh2.ma_khach_hang.startswith('KH')
    
    def test_create_duplicate_email(self, khach_hang_service, sample_khach_hang_data):
        """Test duplicate email validation"""
        khach_hang_service.create(sample_khach_hang_data)
        
        # Try to create with same email
        sample_khach_hang_data['ho_ten'] = 'Nguyễn Văn B'
        sample_khach_hang_data['so_dien_thoai'] = '0909876543'
        
        with pytest.raises(ValueError, match="Email.*đã được sử dụng"):
            khach_hang_service.create(sample_khach_hang_data)
    
    def test_create_invalid_email(self, khach_hang_service, sample_khach_hang_data):
        """Test invalid email validation"""
        sample_khach_hang_data['email'] = 'invalid-email'
        
        with pytest.raises(ValueError, match="Email không đúng định dạng"):
            khach_hang_service.create(sample_khach_hang_data)
    
    def test_create_invalid_phone(self, khach_hang_service, sample_khach_hang_data):
        """Test invalid phone validation"""
        sample_khach_hang_data['so_dien_thoai'] = '123456'  # Too short
        
        with pytest.raises(ValueError, match="Số điện thoại không đúng định dạng"):
            khach_hang_service.create(sample_khach_hang_data)
    
    def test_create_missing_required_field(self, khach_hang_service, sample_khach_hang_data):
        """Test missing required field"""
        sample_khach_hang_data['ho_ten'] = ''  # Required field
        
        with pytest.raises(ValueError):
            khach_hang_service.create(sample_khach_hang_data)


class TestKhachHangServiceGet:
    """Test KhachHangService.get_*() methods"""
    
    def test_get_by_id_success(self, khach_hang_service, sample_khach_hang_data):
        """Test get by ID"""
        kh = khach_hang_service.create(sample_khach_hang_data)
        
        retrieved = khach_hang_service.get_by_id(kh.ma_khach_hang)
        
        assert retrieved is not None
        assert retrieved.ma_khach_hang == kh.ma_khach_hang
        assert retrieved.ho_ten == kh.ho_ten
    
    def test_get_by_id_not_found(self, khach_hang_service):
        """Test get by ID with non-existent ID"""
        retrieved = khach_hang_service.get_by_id('KH_NON_EXISTENT')
        
        assert retrieved is None
    
    def test_get_all(self, khach_hang_service, sample_khach_hang_data):
        """Test get all customers"""
        # Create 5 customers
        for i in range(5):
            sample_khach_hang_data['email'] = f'test{i}@email.com'
            sample_khach_hang_data['so_dien_thoai'] = f'090123456{i}'
            khach_hang_service.create(sample_khach_hang_data)
        
        all_kh = khach_hang_service.get_all()
        
        assert len(all_kh) == 5
    
    def test_get_all_with_pagination(self, khach_hang_service, sample_khach_hang_data):
        """Test get all with pagination"""
        # Create 10 customers
        for i in range(10):
            sample_khach_hang_data['email'] = f'test{i}@email.com'
            sample_khach_hang_data['so_dien_thoai'] = f'090123456{i}'
            khach_hang_service.create(sample_khach_hang_data)
        
        # Get first page
        page1 = khach_hang_service.get_all(skip=0, limit=5)
        assert len(page1) == 5
        
        # Get second page
        page2 = khach_hang_service.get_all(skip=5, limit=5)
        assert len(page2) == 5
    
    def test_get_all_with_status_filter(self, khach_hang_service, sample_khach_hang_data):
        """Test get all with status filter"""
        # Create active customer
        khach_hang_service.create(sample_khach_hang_data)
        
        # Create tam_khoa customer
        sample_khach_hang_data['email'] = 'test2@email.com'
        sample_khach_hang_data['so_dien_thoai'] = '0909876543'
        sample_khach_hang_data['trang_thai'] = TrangThaiKHEnum.TAM_KHOA
        khach_hang_service.create(sample_khach_hang_data)
        
        # Get only active
        active = khach_hang_service.get_all(trang_thai='hoat_dong')
        assert len(active) == 1
        assert active[0].trang_thai == TrangThaiKHEnum.HOAT_DONG


class TestKhachHangServiceSearch:
    """Test KhachHangService.search()"""
    
    def test_search_by_name(self, khach_hang_service, sample_khach_hang_data):
        """Test search by name"""
        khach_hang_service.create(sample_khach_hang_data)
        
        results = khach_hang_service.search('Nguyễn')
        
        assert len(results) == 1
        assert results[0].ho_ten == 'Nguyễn Văn A'
    
    def test_search_by_phone(self, khach_hang_service, sample_khach_hang_data):
        """Test search by phone"""
        khach_hang_service.create(sample_khach_hang_data)
        
        results = khach_hang_service.search('0901234567')
        
        assert len(results) == 1
    
    def test_search_by_email(self, khach_hang_service, sample_khach_hang_data):
        """Test search by email"""
        khach_hang_service.create(sample_khach_hang_data)
        
        results = khach_hang_service.search('nguyenvana@email.com')
        
        assert len(results) == 1
    
    def test_search_no_results(self, khach_hang_service, sample_khach_hang_data):
        """Test search with no results"""
        khach_hang_service.create(sample_khach_hang_data)
        
        results = khach_hang_service.search('nonexistent')
        
        assert len(results) == 0
    
    def test_search_case_insensitive(self, khach_hang_service, sample_khach_hang_data):
        """Test case-insensitive search"""
        khach_hang_service.create(sample_khach_hang_data)
        
        results = khach_hang_service.search('nguyễn')  # lowercase
        
        assert len(results) == 1


class TestKhachHangServiceUpdate:
    """Test KhachHangService.update()"""
    
    def test_update_success(self, khach_hang_service, sample_khach_hang_data):
        """Test successful update"""
        kh = khach_hang_service.create(sample_khach_hang_data)
        
        # Update
        updated = khach_hang_service.update(kh.ma_khach_hang, {
            'ho_ten': 'Nguyễn Văn B',
            'so_dien_thoai': '0909876543'
        })
        
        assert updated.ho_ten == 'Nguyễn Văn B'
        assert updated.so_dien_thoai == '0909876543'
    
    def test_update_not_found(self, khach_hang_service):
        """Test update non-existent customer"""
        result = khach_hang_service.update('KH_NON_EXISTENT', {'ho_ten': 'Test'})
        
        assert result is None
    
    def test_update_duplicate_email(self, khach_hang_service, sample_khach_hang_data):
        """Test update with duplicate email"""
        # Create two customers
        kh1 = khach_hang_service.create(sample_khach_hang_data)
        
        sample_khach_hang_data['email'] = 'test2@email.com'
        sample_khach_hang_data['so_dien_thoai'] = '0909876543'
        kh2 = khach_hang_service.create(sample_khach_hang_data)
        
        # Try to update kh2 with kh1's email
        with pytest.raises(ValueError, match="Email.*đã được sử dụng"):
            khach_hang_service.update(kh2.ma_khach_hang, {'email': 'nguyenvana@email.com'})
    
    def test_update_cannot_change_ma_khach_hang(self, khach_hang_service, sample_khach_hang_data):
        """Test that ma_khach_hang cannot be changed"""
        kh = khach_hang_service.create(sample_khach_hang_data)
        
        # Try to change ma_khach_hang (should be ignored)
        updated = khach_hang_service.update(kh.ma_khach_hang, {
            'ma_khach_hang': 'KH_NEW_ID'
        })
        
        assert updated.ma_khach_hang != 'KH_NEW_ID'


class TestKhachHangServiceDelete:
    """Test KhachHangService.delete()"""
    
    def test_delete_success(self, khach_hang_service, sample_khach_hang_data):
        """Test successful soft delete"""
        kh = khach_hang_service.create(sample_khach_hang_data)
        
        result = khach_hang_service.delete(kh.ma_khach_hang)
        
        assert result is True
        
        # Verify soft delete (status changed, not removed)
        deleted_kh = khach_hang_service.get_by_id(kh.ma_khach_hang)
        assert deleted_kh.trang_thai == TrangThaiKHEnum.DA_XOA
    
    def test_delete_not_found(self, khach_hang_service):
        """Test delete non-existent customer"""
        result = khach_hang_service.delete('KH_NON_EXISTENT')
        
        assert result is False
    
    def test_delete_with_active_contract(self, khach_hang_service, sample_khach_hang_data):
        """Test delete customer with active contract"""
        from src.models import HopDong
        
        kh = khach_hang_service.create(sample_khach_hang_data)
        
        # Create active contract
        hop_dong = HopDong(
            ma_hop_dong='HD001',
            ma_khach_hang=kh.ma_khach_hang,
            ma_vi_tri='VT001',
            ngay_bat_dau=date.today(),
            ngay_ket_thuc=date.today(),
            gia_thue=1000000,
            tien_coc=2000000,
            trang_thai='hieu_luc'
        )
        khach_hang_service._get_session().add(hop_dong)
        khach_hang_service._get_session().commit()
        
        # Try to delete
        with pytest.raises(ValueError, match="hợp đồng đang hoạt động"):
            khach_hang_service.delete(kh.ma_khach_hang)


class TestKhachHangServiceGetHistory:
    """Test KhachHangService.get_history()"""
    
    def test_get_history_success(self, khach_hang_service, sample_khach_hang_data):
        """Test get customer history"""
        kh = khach_hang_service.create(sample_khach_hang_data)
        
        history = khach_hang_service.get_history(kh.ma_khach_hang)
        
        assert 'thong_tin' in history
        assert 'hop_dongs' in history
        assert 'tong_hop_dong' in history
        assert 'tong_da_thanh_toan' in history
        assert 'tong_cong_no' in history
        assert history['thong_tin'].ma_khach_hang == kh.ma_khach_hang
    
    def test_get_history_not_found(self, khach_hang_service):
        """Test get history for non-existent customer"""
        history = khach_hang_service.get_history('KH_NON_EXISTENT')
        
        assert history == {}


class TestConvenienceFunctions:
    """Test convenience functions"""
    
    def test_create_khach_hang(self, test_session, sample_khach_hang_data):
        """Test create_khach_hang function"""
        # Create service to use same session
        service = KhachHangService(session=test_session)
        
        # Mock the global service (in real test, would use dependency injection)
        kh = service.create(sample_khach_hang_data)
        
        assert kh is not None
        assert kh.ma_khach_hang.startswith('KH')


# Run tests with: pytest tests/test_services/test_khach_hang_service.py -v
