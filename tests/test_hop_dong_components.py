#!/usr/bin/env python3
"""
Tests for HangHoaService and ThanhToanService
"""
import pytest
import sys
from pathlib import Path
from datetime import date

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.services import HangHoaService, ThanhToanService, HopDongService, TrangThaiTTEnum


@pytest.fixture
def hang_hoa_service():
    """Create HangHoaService instance"""
    return HangHoaService()


@pytest.fixture
def thanh_toan_service():
    """Create ThanhToanService instance"""
    return ThanhToanService()


@pytest.fixture
def hop_dong_service():
    """Create HopDongService instance"""
    return HopDongService()


@pytest.fixture
def sample_hop_dong(hop_dong_service):
    """Create a sample contract for testing"""
    data = {
        'ma_khach_hang': 'KH001',
        'ma_vi_tri': 'KHO001-A-01-01-001',
        'ngay_bat_dau': date(2026, 1, 1),
        'ngay_ket_thuc': date(2026, 12, 31),
        'gia_thue': 1500000.0,
        'tien_coc': 3000000.0,
        'phuong_thuc_thanh_toan': 'hang_thang',
    }
    hop_dong = hop_dong_service.create(data)
    yield hop_dong
    # Cleanup
    try:
        hop_dong_service.delete(hop_dong.ma_hop_dong)
    except:
        pass


@pytest.fixture
def sample_hang_hoa_data(sample_hop_dong):
    """Sample goods data for testing"""
    return {
        'ma_hop_dong': sample_hop_dong.ma_hop_dong,
        'ten_hang_hoa': 'Hàng hóa test',
        'so_luong': 100,
        'don_vi_tinh': 'cái',
        'gia_tri': 5000000.0,
        'ghi_chu': 'Test goods'
    }


@pytest.fixture
def sample_thanh_toan_data(sample_hop_dong):
    """Sample payment data for testing"""
    return {
        'ma_hop_dong': sample_hop_dong.ma_hop_dong,
        'ky_thanh_toan': 'Kỳ 1',
        'den_han': date(2026, 2, 1),
        'so_tien': 1500000.0,
        'trang_thai': TrangThaiTTEnum.CHUA_THANH_TOAN,
    }


class TestHangHoaServiceCreate:
    """Test HangHoaService.create()"""
    
    def test_create_hang_hoa_success(self, hang_hoa_service, sample_hang_hoa_data):
        """Test successful goods creation"""
        hang_hoa = hang_hoa_service.create(sample_hang_hoa_data)
        
        assert hang_hoa is not None
        assert hang_hoa.ma_hang_hoa.startswith(sample_hang_hoa_data['ma_hop_dong'])
        assert hang_hoa.ten_hang_hoa == sample_hang_hoa_data['ten_hang_hoa']
        assert hang_hoa.so_luong == sample_hang_hoa_data['so_luong']
        
        # Cleanup
        hang_hoa_service.delete(hang_hoa.ma_hang_hoa)
    
    def test_create_hang_hoa_auto_generate_id(self, hang_hoa_service, sample_hang_hoa_data):
        """Test auto-generation of goods ID"""
        hang_hoa1 = hang_hoa_service.create(sample_hang_hoa_data)
        
        sample_hang_hoa_data['ten_hang_hoa'] = 'Hàng hóa test 2'
        hang_hoa2 = hang_hoa_service.create(sample_hang_hoa_data)
        
        assert hang_hoa1.ma_hang_hoa != hang_hoa2.ma_hang_hoa
        assert hang_hoa1.ma_hang_hoa.endswith('001')
        assert hang_hoa2.ma_hang_hoa.endswith('002')
        
        # Cleanup
        hang_hoa_service.delete(hang_hoa1.ma_hang_hoa)
        hang_hoa_service.delete(hang_hoa2.ma_hang_hoa)
    
    def test_create_hang_hoa_missing_hop_dong(self, hang_hoa_service):
        """Test creation with missing contract"""
        data = {
            'ten_hang_hoa': 'Test',
            'so_luong': 10,
        }
        
        with pytest.raises(ValueError, match="Thiếu trường bắt buộc"):
            hang_hoa_service.create(data)


class TestHangHoaServiceGet:
    """Test HangHoaService retrieval methods"""
    
    def test_get_by_hop_dong(self, hang_hoa_service, sample_hang_hoa_data):
        """Test get_by_hop_dong"""
        # Create multiple goods
        created = []
        for i in range(3):
            data = sample_hang_hoa_data.copy()
            data['ten_hang_hoa'] = f'Hàng {i+1}'
            hang_hoa = hang_hoa_service.create(data)
            created.append(hang_hoa)
        
        # Get by contract
        hang_hoas = hang_hoa_service.get_by_hop_dong(sample_hang_hoa_data['ma_hop_dong'])
        
        assert len(hang_hoas) >= 3
        assert all(hh.ma_hop_dong == sample_hang_hoa_data['ma_hop_dong'] for hh in hang_hoas)
        
        # Cleanup
        for hh in created:
            hang_hoa_service.delete(hh.ma_hang_hoa)
    
    def test_get_tong_gia_tri(self, hang_hoa_service, sample_hang_hoa_data):
        """Test get_tong_gia_tri"""
        hang_hoa1 = hang_hoa_service.create(sample_hang_hoa_data)
        
        sample_hang_hoa_data['ten_hang_hoa'] = 'Hàng 2'
        sample_hang_hoa_data['gia_tri'] = 3000000.0
        hang_hoa2 = hang_hoa_service.create(sample_hang_hoa_data)
        
        total = hang_hoa_service.get_tong_gia_tri(sample_hang_hoa_data['ma_hop_dong'])
        
        assert total == 5000000.0 + 3000000.0
        
        # Cleanup
        hang_hoa_service.delete(hang_hoa1.ma_hang_hoa)
        hang_hoa_service.delete(hang_hoa2.ma_hang_hoa)


class TestHangHoaServiceUpdate:
    """Test HangHoaService.update()"""
    
    def test_update_success(self, hang_hoa_service, sample_hang_hoa_data):
        """Test successful update"""
        created = hang_hoa_service.create(sample_hang_hoa_data)
        
        update_data = {
            'so_luong': 200,
            'gia_tri': 10000000.0,
        }
        
        updated = hang_hoa_service.update(created.ma_hang_hoa, update_data)
        
        assert updated.so_luong == 200
        assert updated.gia_tri == 10000000.0
        
        # Cleanup
        hang_hoa_service.delete(created.ma_hang_hoa)


class TestHangHoaServiceDelete:
    """Test HangHoaService.delete()"""
    
    def test_delete_success(self, hang_hoa_service, sample_hang_hoa_data):
        """Test successful delete"""
        created = hang_hoa_service.create(sample_hang_hoa_data)
        
        success = hang_hoa_service.delete(created.ma_hang_hoa)
        assert success is True
        
        # Verify deleted
        deleted = hang_hoa_service.get_by_hop_dong(sample_hang_hoa_data['ma_hop_dong'])
        assert len(deleted) == 0


class TestThanhToanServiceCreate:
    """Test ThanhToanService.create()"""
    
    def test_create_thanh_toan_success(self, thanh_toan_service, sample_thanh_toan_data):
        """Test successful payment creation"""
        thanh_toan = thanh_toan_service.create(sample_thanh_toan_data)
        
        assert thanh_toan is not None
        assert thanh_toan.ma_thanh_toan.startswith(sample_thanh_toan_data['ma_hop_dong'])
        assert thanh_toan.ky_thanh_toan == sample_thanh_toan_data['ky_thanh_toan']
        assert thanh_toan.so_tien == sample_thanh_toan_data['so_tien']
        
        # Cleanup
        thanh_toan_service.delete(thanh_toan.ma_thanh_toan)
    
    def test_create_thanh_toan_auto_generate_id(self, thanh_toan_service, sample_thanh_toan_data):
        """Test auto-generation of payment ID"""
        thanh_toan1 = thanh_toan_service.create(sample_thanh_toan_data)
        
        sample_thanh_toan_data['ky_thanh_toan'] = 'Kỳ 2'
        thanh_toan2 = thanh_toan_service.create(sample_thanh_toan_data)
        
        assert thanh_toan1.ma_thanh_toan != thanh_toan2.ma_thanh_toan
        assert thanh_toan1.ma_thanh_toan.endswith('001')
        assert thanh_toan2.ma_thanh_toan.endswith('002')
        
        # Cleanup
        thanh_toan_service.delete(thanh_toan1.ma_thanh_toan)
        thanh_toan_service.delete(thanh_toan2.ma_thanh_toan)


class TestThanhToanServiceGet:
    """Test ThanhToanService retrieval methods"""
    
    def test_get_by_hop_dong(self, thanh_toan_service, sample_thanh_toan_data):
        """Test get_by_hop_dong"""
        # Create multiple payments
        created = []
        for i in range(3):
            data = sample_thanh_toan_data.copy()
            data['ky_thanh_toan'] = f'Kỳ {i+1}'
            thanh_toan = thanh_toan_service.create(data)
            created.append(thanh_toan)
        
        # Get by contract
        payments = thanh_toan_service.get_by_hop_dong(sample_thanh_toan_data['ma_hop_dong'])
        
        assert len(payments) >= 3
        assert all(p.ma_hop_dong == sample_thanh_toan_data['ma_hop_dong'] for p in payments)
        
        # Cleanup
        for p in created:
            thanh_toan_service.delete(p.ma_thanh_toan)
    
    def test_get_tong_da_thanh_toan(self, thanh_toan_service, sample_thanh_toan_data):
        """Test get_tong_da_thanh_toan"""
        # Create paid payment
        sample_thanh_toan_data['trang_thai'] = TrangThaiTTEnum.DA_THANH_TOAN
        thanh_toan1 = thanh_toan_service.create(sample_thanh_toan_data)
        
        # Create unpaid payment
        sample_thanh_toan_data['ky_thanh_toan'] = 'Kỳ 2'
        sample_thanh_toan_data['trang_thai'] = TrangThaiTTEnum.CHUA_THANH_TOAN
        thanh_toan2 = thanh_toan_service.create(sample_thanh_toan_data)
        
        total = thanh_toan_service.get_tong_da_thanh_toan(sample_thanh_toan_data['ma_hop_dong'])
        
        assert total == 1500000.0  # Only first payment
        
        # Cleanup
        thanh_toan_service.delete(thanh_toan1.ma_thanh_toan)
        thanh_toan_service.delete(thanh_toan2.ma_thanh_toan)


class TestThanhToanServiceMarkAsPaid:
    """Test ThanhToanService.mark_as_paid()"""
    
    def test_mark_as_paid_success(self, thanh_toan_service, sample_thanh_toan_data):
        """Test marking payment as paid"""
        thanh_toan = thanh_toan_service.create(sample_thanh_toan_data)
        
        # Mark as paid
        updated = thanh_toan_service.mark_as_paid(thanh_toan.ma_thanh_toan)
        
        assert updated.trang_thai == TrangThaiTTEnum.DA_THANH_TOAN
        assert updated.ngay_thanh_toan is not None
        
        # Cleanup
        thanh_toan_service.delete(thanh_toan.ma_thanh_toan)


class TestThanhToanServiceGenerateSchedule:
    """Test ThanhToanService.generate_payment_schedule()"""
    
    def test_generate_schedule_monthly(self, thanh_toan_service, sample_hop_dong):
        """Test generating monthly payment schedule"""
        # Set monthly payment
        sample_hop_dong.phuong_thuc_thanh_toan = 'hang_thang'
        
        # Generate schedule
        payments = thanh_toan_service.generate_payment_schedule(sample_hop_dong.ma_hop_dong)
        
        assert len(payments) > 0
        assert all(p.ma_hop_dong == sample_hop_dong.ma_hop_dong for p in payments)
        
        # Cleanup
        for p in payments:
            thanh_toan_service.delete(p.ma_thanh_toan)


class TestThanhToanServiceUpdate:
    """Test ThanhToanService.update()"""
    
    def test_update_success(self, thanh_toan_service, sample_thanh_toan_data):
        """Test successful update"""
        created = thanh_toan_service.create(sample_thanh_toan_data)
        
        update_data = {
            'so_tien': 2000000.0,
        }
        
        updated = thanh_toan_service.update(created.ma_thanh_toan, update_data)
        
        assert updated.so_tien == 2000000.0
        
        # Cleanup
        thanh_toan_service.delete(created.ma_thanh_toan)


class TestThanhToanServiceDelete:
    """Test ThanhToanService.delete()"""
    
    def test_delete_success(self, thanh_toan_service, sample_thanh_toan_data):
        """Test successful delete"""
        created = thanh_toan_service.create(sample_thanh_toan_data)
        
        success = thanh_toan_service.delete(created.ma_thanh_toan)
        assert success is True
        
        # Verify deleted
        deleted = thanh_toan_service.get_by_hop_dong(sample_thanh_toan_data['ma_hop_dong'])
        assert len(deleted) == 0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
