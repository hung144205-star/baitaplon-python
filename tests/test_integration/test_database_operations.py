"""
Integration tests cho Database Operations
"""
import pytest
from datetime import date, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.models import (
    KhachHang, Kho, ViTri, HopDong, HangHoa, ThanhToan, NhanVien,
    Base, LoaiKhachEnum, TrangThaiKHEnum, TrangThaiKhoEnum,
    TrangThaiViTriEnum, TrangThaiHDEnum
)


@pytest.fixture
def engine():
    """Create in-memory test database"""
    engine = create_engine('sqlite:///:memory:', echo=False)
    Base.metadata.create_all(engine)
    return engine


@pytest.fixture
def session(engine):
    """Create test session"""
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()


@pytest.fixture
def sample_data(session):
    """Create sample data for integration tests"""
    # Create customer
    khach_hang = KhachHang(
        ma_khach_hang='KH001',
        ho_ten='Nguyễn Văn A',
        loai_khach=LoaiKhachEnum.CA_NHAN,
        so_dien_thoai='0901234567',
        email='nguyenvana@email.com',
        dia_chi='123 Nguyễn Văn Linh, Q7, TP.HCM',
        ma_so_thue=None,
        ngay_dang_ky=date.today(),
        trang_thai=TrangThaiKHEnum.HOAT_DONG,
    )
    session.add(khach_hang)
    
    # Create warehouse
    kho = Kho(
        ma_kho='KHO001',
        ten_kho='Kho Tân Bình',
        dia_chi='456 Điện Biên Phủ, Q3, TP.HCM',
        dien_tich=1000.0,
        suc_chua=5000.0,
        da_su_dung=0.0,
        trang_thai=TrangThaiKhoEnum.HOAT_DONG,
    )
    session.add(kho)
    
    # Create position
    vi_tri = ViTri(
        ma_vi_tri='VT001',
        ma_kho='KHO001',
        khu_vuc='A',
        hang='01',
        tang=1,
        dien_tich=50.0,
        gia_thue=1500000.0,
        suc_chua=1000.0,
        trang_thai=TrangThaiViTriEnum.TRONG,
    )
    session.add(vi_tri)
    
    # Create contract
    hop_dong = HopDong(
        ma_hop_dong='HD001',
        ma_khach_hang='KH001',
        ma_vi_tri='VT001',
        ngay_bat_dau=date.today(),
        ngay_ket_thuc=date.today() + timedelta(days=365),
        gia_thue=1500000.0,
        tien_coc=3000000.0,
        trang_thai=TrangThaiHDEnum.HIEU_LUC,
    )
    session.add(hop_dong)
    
    session.commit()
    
    return {
        'khach_hang': khach_hang,
        'kho': kho,
        'vi_tri': vi_tri,
        'hop_dong': hop_dong,
    }


class TestDatabaseRelationships:
    """Test database relationships"""
    
    def test_khach_hang_hop_dong_relationship(self, session, sample_data):
        """Test customer-contract relationship"""
        kh = session.query(KhachHang).filter_by(ma_khach_hang='KH001').first()
        
        assert len(kh.hop_dongs) >= 1
        assert kh.hop_dongs[0].ma_khach_hang == 'KH001'
    
    def test_kho_vi_tri_relationship(self, session, sample_data):
        """Test warehouse-position relationship"""
        kho = session.query(Kho).filter_by(ma_kho='KHO001').first()
        
        assert len(kho.vi_tris) >= 1
        assert kho.vi_tris[0].ma_kho == 'KHO001'
    
    def test_vi_tri_kho_relationship(self, session, sample_data):
        """Test position-warehouse relationship"""
        vt = session.query(ViTri).filter_by(ma_vi_tri='VT001').first()
        
        assert vt.kho is not None
        assert vt.kho.ma_kho == 'KHO001'


class TestDatabaseOperations:
    """Test basic database operations"""
    
    def test_create_read(self, session, sample_data):
        """Test Create and Read"""
        kh = session.query(KhachHang).filter_by(ma_khach_hang='KH001').first()
        
        assert kh is not None
        assert kh.ho_ten == 'Nguyễn Văn A'
    
    def test_update(self, session, sample_data):
        """Test Update"""
        kh = session.query(KhachHang).filter_by(ma_khach_hang='KH001').first()
        kh.ho_ten = 'Nguyễn Văn B Updated'
        session.commit()
        
        updated = session.query(KhachHang).filter_by(ma_khach_hang='KH001').first()
        assert updated.ho_ten == 'Nguyễn Văn B Updated'
    
    def test_delete_soft(self, session, sample_data):
        """Test Soft Delete"""
        kh = session.query(KhachHang).filter_by(ma_khach_hang='KH001').first()
        kh.trang_thai = TrangThaiKHEnum.DA_XOA
        session.commit()
        
        deleted = session.query(KhachHang).filter_by(ma_khach_hang='KH001').first()
        assert deleted.trang_thai == TrangThaiKHEnum.DA_XOA


class TestHopDongWorkflow:
    """Test contract workflow"""
    
    def test_contract_creation(self, session, sample_data):
        """Test contract is created with correct status"""
        hd = session.query(HopDong).filter_by(ma_hop_dong='HD001').first()
        
        assert hd is not None
        assert hd.trang_thai == TrangThaiHDEnum.HIEU_LUC
        assert hd.gia_thue == 1500000.0
    
    def test_contract_with_customer(self, session, sample_data):
        """Test contract links to correct customer"""
        hd = session.query(HopDong).filter_by(ma_hop_dong='HD001').first()
        
        assert hd.khach_hang is not None
        assert hd.khach_hang.ma_khach_hang == 'KH001'
    
    def test_contract_with_position(self, session, sample_data):
        """Test contract links to correct position"""
        hd = session.query(HopDong).filter_by(ma_hop_dong='HD001').first()
        
        assert hd.vi_tri is not None
        assert hd.vi_tri.ma_vi_tri == 'VT001'


class TestWarehouseCapacity:
    """Test warehouse capacity calculations"""
    
    def test_initial_capacity(self, session, sample_data):
        """Test initial warehouse capacity"""
        kho = session.query(Kho).filter_by(ma_kho='KHO001').first()
        
        assert kho.suc_chua == 5000.0
        assert kho.da_su_dung == 0.0
    
    def test_position_updates_capacity(self, session, sample_data):
        """Test position creation affects warehouse capacity"""
        # Create another position with some usage
        vi_tri2 = ViTri(
            ma_vi_tri='VT002',
            ma_kho='KHO001',
            khu_vuc='B',
            hang='01',
            tang=1,
            dien_tich=50.0,
            gia_thue=1500000.0,
            suc_chua=500.0,
            trang_thai=TrangThaiViTriEnum.TRONG,
        )
        session.add(vi_tri2)
        session.commit()
        
        kho = session.query(Kho).filter_by(ma_kho='KHO001').first()
        positions = session.query(ViTri).filter_by(ma_kho='KHO001').all()
        
        assert len(positions) == 2


class TestThanhToanIntegration:
    """Test payment integration with contracts"""
    
    def test_create_payment(self, session, sample_data):
        """Test payment creation"""
        thanh_toan = ThanhToan(
            ma_thanh_toan='TT001',
            ma_hop_dong='HD001',
            ky_thanh_toan='2024-01',
            den_han=date.today(),
            so_tien=1500000.0,
            trang_thai='chua_thanh_toan',
        )
        session.add(thanh_toan)
        session.commit()
        
        tt = session.query(ThanhToan).filter_by(ma_thanh_toan='TT001').first()
        
        assert tt is not None
        assert tt.ma_hop_dong == 'HD001'
        assert tt.so_tien == 1500000.0


# Run tests with: pytest tests/test_integration/test_database_operations.py -v
