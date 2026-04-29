"""
Test suite cho Kho Model
"""
import pytest
from datetime import date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.models import Kho, ViTri, Base, TrangThaiKhoEnum


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
def sample_kho_data():
    """Sample warehouse data for testing"""
    return {
        'ma_kho': 'KHO001',
        'ten_kho': 'Kho Tân Bình',
        'dia_chi': '123 Nguyễn Văn Linh, Q7, TP.HCM',
        'dien_tich': 1000.0,
        'suc_chua': 5000.0,
        'da_su_dung': 2000.0,
        'trang_thai': TrangThaiKhoEnum.HOAT_DONG,
    }


class TestKhoModel:
    """Test Kho model"""
    
    def test_create_kho(self, test_session, sample_kho_data):
        """Test creating a warehouse"""
        kho = Kho(**sample_kho_data)
        test_session.add(kho)
        test_session.commit()
        
        assert kho.ma_kho == 'KHO001'
        assert kho.ten_kho == 'Kho Tân Bình'
        assert kho.dien_tich == 1000.0
        assert kho.suc_chua == 5000.0
        assert kho.da_su_dung == 2000.0
        assert kho.trang_thai == TrangThaiKhoEnum.HOAT_DONG
    
    def test_ty_le_lap_day(self, test_session, sample_kho_data):
        """Test warehouse fill rate calculation"""
        kho = Kho(**sample_kho_data)
        test_session.add(kho)
        test_session.commit()
        
        # Fill rate = (da_su_dung / suc_chua) * 100
        expected = (2000.0 / 5000.0) * 100
        assert kho.ty_le_lap_day == expected
    
    def test_ty_le_lap_day_zero_suc_chua(self, test_session, sample_kho_data):
        """Test fill rate when capacity is zero"""
        sample_kho_data['suc_chua'] = 0
        kho = Kho(**sample_kho_data)
        test_session.add(kho)
        test_session.commit()
        
        assert kho.ty_le_lap_day == 0
    
    def test_dung_tich_con_lai(self, test_session, sample_kho_data):
        """Test remaining capacity calculation"""
        kho = Kho(**sample_kho_data)
        test_session.add(kho)
        test_session.commit()
        
        expected = 5000.0 - 2000.0  # suc_chua - da_su_dung
        assert kho.dung_tich_con_lai == expected
    
    def test_kho_hoat_dong(self, test_session, sample_kho_data):
        """Test warehouse with active status"""
        sample_kho_data['trang_thai'] = TrangThaiKhoEnum.HOAT_DONG
        kho = Kho(**sample_kho_data)
        test_session.add(kho)
        test_session.commit()
        
        assert kho.trang_thai == TrangThaiKhoEnum.HOAT_DONG
    
    def test_kho_bao_tri(self, test_session, sample_kho_data):
        """Test warehouse under maintenance"""
        sample_kho_data['trang_thai'] = TrangThaiKhoEnum.BAO_TRI
        kho = Kho(**sample_kho_data)
        test_session.add(kho)
        test_session.commit()
        
        assert kho.trang_thai == TrangThaiKhoEnum.BAO_TRI
    
    def test_kho_ngung(self, test_session, sample_kho_data):
        """Test warehouse stopped"""
        sample_kho_data['trang_thai'] = TrangThaiKhoEnum.NGUNG
        kho = Kho(**sample_kho_data)
        test_session.add(kho)
        test_session.commit()
        
        assert kho.trang_thai == TrangThaiKhoEnum.NGUNG
    
    def test_to_dict(self, test_session, sample_kho_data):
        """Test model to dictionary conversion"""
        kho = Kho(**sample_kho_data)
        test_session.add(kho)
        test_session.commit()
        
        data = kho.to_dict()
        
        assert 'ma_kho' in data
        assert 'ten_kho' in data
        assert 'dia_chi' in data
        assert 'dien_tich' in data
        assert 'suc_chua' in data
        assert 'da_su_dung' in data
        assert 'trang_thai' in data
    
    def test_repr(self, test_session, sample_kho_data):
        """Test string representation"""
        kho = Kho(**sample_kho_data)
        test_session.add(kho)
        test_session.commit()
        
        assert 'Kho' in repr(kho)
        assert 'KHO001' in repr(kho)
    
    def test_ngay_tao_auto(self, test_session, sample_kho_data):
        """Test auto-generated creation date"""
        kho = Kho(**sample_kho_data)
        test_session.add(kho)
        test_session.commit()
        
        assert kho.ngay_tao is not None


class TestKhoModelValidation:
    """Test Kho model validation"""
    
    def test_missing_required_field_ten_kho(self, test_session, sample_kho_data):
        """Test missing required field 'ten_kho'"""
        del sample_kho_data['ten_kho']
        kho = Kho(**sample_kho_data)
        test_session.add(kho)
        
        # SQLAlchemy will raise an error on commit
        with pytest.raises(Exception):
            test_session.commit()
    
    def test_missing_required_field_dia_chi(self, test_session, sample_kho_data):
        """Test missing required field 'dia_chi'"""
        del sample_kho_data['dia_chi']
        kho = Kho(**sample_kho_data)
        test_session.add(kho)
        
        with pytest.raises(Exception):
            test_session.commit()
    
    def test_negative_dien_tich(self, test_session, sample_kho_data):
        """Test negative area value"""
        sample_kho_data['dien_tich'] = -100.0
        kho = Kho(**sample_kho_data)
        test_session.add(kho)
        
        # Should allow but may cause issues in real usage
        # This depends on business rules
        test_session.commit()
        assert kho.dien_tich == -100.0
    
    def test_zero_suc_chua(self, test_session, sample_kho_data):
        """Test zero capacity"""
        sample_kho_data['suc_chua'] = 0
        kho = Kho(**sample_kho_data)
        test_session.add(kho)
        test_session.commit()
        
        assert kho.suc_chua == 0
        assert kho.ty_le_lap_day == 0  # Should handle zero safely


# Run tests with: pytest tests/test_models/test_kho_model.py -v
