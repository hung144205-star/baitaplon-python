#!/usr/bin/env python3
"""
Tests for HopDongService
"""
import pytest
import sys
from pathlib import Path
from datetime import datetime, date

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.services import HopDongService, TrangThaiHDEnum
from src.models import HopDong


@pytest.fixture
def hop_dong_service():
    """Create HopDongService instance"""
    return HopDongService()


@pytest.fixture
def sample_hop_dong_data():
    """Sample contract data for testing"""
    return {
        'ma_khach_hang': 'KH001',
        'ma_vi_tri': 'KHO001-A-01-01-001',
        'ngay_bat_dau': date(2026, 1, 1),
        'ngay_ket_thuc': date(2026, 12, 31),
        'gia_thue': 1500000.0,
        'tien_coc': 3000000.0,
        'phuong_thuc_thanh_toan': 'hang_thang',
        'dieu_khoan': 'Test contract'
    }


class TestHopDongServiceCreate:
    """Test HopDongService.create()"""
    
    def test_create_hop_dong_success(self, hop_dong_service, sample_hop_dong_data):
        """Test successful contract creation"""
        hop_dong = hop_dong_service.create(sample_hop_dong_data)
        
        assert hop_dong is not None
        assert hop_dong.ma_hop_dong.startswith('HD')
        assert hop_dong.ma_khach_hang == sample_hop_dong_data['ma_khach_hang']
        assert hop_dong.ma_vi_tri == sample_hop_dong_data['ma_vi_tri']
        assert hop_dong.trang_thai == TrangThaiHDEnum.HIEU_LUC
        
        # Cleanup
        hop_dong_service.delete(hop_dong.ma_hop_dong)
    
    def test_create_hop_dong_auto_generate_id(self, hop_dong_service, sample_hop_dong_data):
        """Test auto-generation of contract ID"""
        hop_dong1 = hop_dong_service.create(sample_hop_dong_data)
        
        # Modify date for second contract
        sample_hop_dong_data['ngay_bat_dau'] = date(2026, 2, 1)
        hop_dong2 = hop_dong_service.create(sample_hop_dong_data)
        
        assert hop_dong1.ma_hop_dong != hop_dong2.ma_hop_dong
        assert hop_dong1.ma_hop_dong.startswith('HD202601')  # January 2026
        assert hop_dong2.ma_hop_dong.startswith('HD202602')  # February 2026
        
        # Cleanup
        hop_dong_service.delete(hop_dong1.ma_hop_dong)
        hop_dong_service.delete(hop_dong2.ma_hop_dong)
    
    def test_create_hop_dong_missing_customer(self, hop_dong_service):
        """Test creation with missing customer"""
        data = {
            'ma_vi_tri': 'KHO001-A-01-01-001',
            'ngay_bat_dau': date(2026, 1, 1),
            'ngay_ket_thuc': date(2026, 12, 31),
            'gia_thue': 1500000.0,
        }
        
        with pytest.raises(ValueError, match="Thiếu trường bắt buộc"):
            hop_dong_service.create(data)
    
    def test_create_hop_dong_invalid_dates(self, hop_dong_service, sample_hop_dong_data):
        """Test creation with invalid dates"""
        sample_hop_dong_data['ngay_ket_thuc'] = sample_hop_dong_data['ngay_bat_dau']
        
        with pytest.raises(ValueError, match="Ngày kết thúc phải sau ngày bắt đầu"):
            hop_dong_service.create(sample_hop_dong_data)
    
    def test_create_hop_dong_invalid_price(self, hop_dong_service, sample_hop_dong_data):
        """Test creation with invalid price"""
        sample_hop_dong_data['gia_thue'] = 0
        
        with pytest.raises(ValueError, match="Giá thuê phải lớn hơn 0"):
            hop_dong_service.create(sample_hop_dong_data)


class TestHopDongServiceGet:
    """Test HopDongService retrieval methods"""
    
    def test_get_by_id_success(self, hop_dong_service, sample_hop_dong_data):
        """Test get_by_id with valid ID"""
        created = hop_dong_service.create(sample_hop_dong_data)
        
        retrieved = hop_dong_service.get_by_id(created.ma_hop_dong)
        
        assert retrieved is not None
        assert retrieved.ma_hop_dong == created.ma_hop_dong
        
        # Cleanup
        hop_dong_service.delete(created.ma_hop_dong)
    
    def test_get_by_id_not_found(self, hop_dong_service):
        """Test get_by_id with invalid ID"""
        hop_dong = hop_dong_service.get_by_id('HD999999')
        assert hop_dong is None
    
    def test_get_all_success(self, hop_dong_service, sample_hop_dong_data):
        """Test get_all"""
        # Create test data
        created = []
        for i in range(3):
            data = sample_hop_dong_data.copy()
            data['ma_khach_hang'] = f'KH{i+1:03d}'
            hop_dong = hop_dong_service.create(data)
            created.append(hop_dong)
        
        # Get all
        hop_dongs = hop_dong_service.get_all(limit=10)
        
        assert len(hop_dongs) >= 3
        
        # Cleanup
        for hd in created:
            hop_dong_service.delete(hd.ma_hop_dong)


class TestHopDongServiceQuery:
    """Test HopDongService query methods"""
    
    def test_get_by_customer(self, hop_dong_service, sample_hop_dong_data):
        """Test get_by_customer"""
        hop_dong = hop_dong_service.create(sample_hop_dong_data)
        
        contracts = hop_dong_service.get_by_customer(sample_hop_dong_data['ma_khach_hang'])
        
        assert len(contracts) >= 1
        assert any(hd.ma_hop_dong == hop_dong.ma_hop_dong for hd in contracts)
        
        # Cleanup
        hop_dong_service.delete(hop_dong.ma_hop_dong)
    
    def test_get_by_location(self, hop_dong_service, sample_hop_dong_data):
        """Test get_by_location"""
        hop_dong = hop_dong_service.create(sample_hop_dong_data)
        
        contracts = hop_dong_service.get_by_location(sample_hop_dong_data['ma_vi_tri'])
        
        assert len(contracts) >= 1
        assert any(hd.ma_hop_dong == hop_dong.ma_hop_dong for hd in contracts)
        
        # Cleanup
        hop_dong_service.delete(hop_dong.ma_hop_dong)
    
    def test_get_expiring_soon(self, hop_dong_service, sample_hop_dong_data):
        """Test get_expiring_soon"""
        # Create contract expiring in 15 days
        from datetime import timedelta
        today = date.today()
        sample_hop_dong_data['ngay_bat_dau'] = today
        sample_hop_dong_data['ngay_ket_thuc'] = today + timedelta(days=15)
        
        hop_dong = hop_dong_service.create(sample_hop_dong_data)
        
        expiring = hop_dong_service.get_expiring_soon(days=30)
        
        assert len(expiring) >= 1
        assert any(hd.ma_hop_dong == hop_dong.ma_hop_dong for hd in expiring)
        
        # Cleanup
        hop_dong_service.delete(hop_dong.ma_hop_dong)


class TestHopDongServiceBusinessLogic:
    """Test HopDongService business logic methods"""
    
    def test_renew_contract(self, hop_dong_service, sample_hop_dong_data):
        """Test contract renewal"""
        hop_dong = hop_dong_service.create(sample_hop_dong_data)
        
        # Renew
        from dateutil.relativedelta import relativedelta
        new_end_date = hop_dong.ngay_ket_thuc + relativedelta(months=6)
        
        updated = hop_dong_service.renew(hop_dong.ma_hop_dong, {
            'ngay_ket_thuc_moi': new_end_date
        })
        
        assert updated.ngay_ket_thuc == new_end_date
        assert updated.trang_thai == TrangThaiHDEnum.GIA_HAN
        
        # Cleanup
        hop_dong_service.delete(hop_dong.ma_hop_dong)
    
    def test_terminate_contract(self, hop_dong_service, sample_hop_dong_data):
        """Test contract termination"""
        hop_dong = hop_dong_service.create(sample_hop_dong_data)
        
        # Terminate
        success = hop_dong_service.terminate(hop_dong.ma_hop_dong, "Test termination")
        
        assert success is True
        
        # Verify status changed
        terminated = hop_dong_service.get_by_id(hop_dong.ma_hop_dong)
        assert terminated.trang_thai == TrangThaiHDEnum.CHAM_DUT
        
        # Cleanup
        hop_dong_service.delete(hop_dong.ma_hop_dong)
    
    def test_get_remaining_days(self, hop_dong_service, sample_hop_dong_data):
        """Test get_remaining_days"""
        from datetime import timedelta
        today = date.today()
        sample_hop_dong_data['ngay_bat_dau'] = today
        sample_hop_dong_data['ngay_ket_thuc'] = today + timedelta(days=30)
        
        hop_dong = hop_dong_service.create(sample_hop_dong_data)
        
        days = hop_dong_service.get_remaining_days(hop_dong.ma_hop_dong)
        
        assert days == 30
        
        # Cleanup
        hop_dong_service.delete(hop_dong.ma_hop_dong)
    
    def test_get_contract_duration_months(self, hop_dong_service, sample_hop_dong_data):
        """Test get_contract_duration_months"""
        sample_hop_dong_data['ngay_bat_dau'] = date(2026, 1, 1)
        sample_hop_dong_data['ngay_ket_thuc'] = date(2026, 12, 31)
        
        hop_dong = hop_dong_service.create(sample_hop_dong_data)
        
        months = hop_dong_service.get_contract_duration_months(hop_dong.ma_hop_dong)
        
        assert months == 11  # Jan to Dec is 11 months difference
        
        # Cleanup
        hop_dong_service.delete(hop_dong.ma_hop_dong)
    
    def test_calculate_total_amount(self, hop_dong_service, sample_hop_dong_data):
        """Test calculate_total_amount"""
        sample_hop_dong_data['ngay_bat_dau'] = date(2026, 1, 1)
        sample_hop_dong_data['ngay_ket_thuc'] = date(2026, 12, 31)
        sample_hop_dong_data['gia_thue'] = 1000000.0
        
        hop_dong = hop_dong_service.create(sample_hop_dong_data)
        
        total = hop_dong_service.calculate_total_amount(hop_dong.ma_hop_dong)
        
        assert 'tong_tien_thue' in total
        assert 'tien_coc' in total
        assert 'tong_cong' in total
        
        # Cleanup
        hop_dong_service.delete(hop_dong.ma_hop_dong)
    
    def test_get_statistics(self, hop_dong_service, sample_hop_dong_data):
        """Test get_statistics"""
        # Create multiple contracts
        for i in range(3):
            data = sample_hop_dong_data.copy()
            data['ma_khach_hang'] = f'KH{i+1:03d}'
            hop_dong_service.create(data)
        
        stats = hop_dong_service.get_statistics()
        
        assert 'tong_so_hop_dong' in stats
        assert 'so_hop_dong_dang_hieu_luc' in stats
        assert stats['tong_so_hop_dong'] >= 3


class TestHopDongServiceSearch:
    """Test HopDongService.search()"""
    
    def test_search_by_id(self, hop_dong_service, sample_hop_dong_data):
        """Test search by contract ID"""
        hop_dong = hop_dong_service.create(sample_hop_dong_data)
        
        results = hop_dong_service.search(hop_dong.ma_hop_dong)
        
        assert len(results) > 0
        assert any(hd.ma_hop_dong == hop_dong.ma_hop_dong for hd in results)
        
        # Cleanup
        hop_dong_service.delete(hop_dong.ma_hop_dong)
    
    def test_search_no_results(self, hop_dong_service):
        """Test search with no results"""
        results = hop_dong_service.search('HopDongKhongTonTai12345')
        assert len(results) == 0


class TestHopDongServiceUpdate:
    """Test HopDongService.update()"""
    
    def test_update_success(self, hop_dong_service, sample_hop_dong_data):
        """Test successful update"""
        created = hop_dong_service.create(sample_hop_dong_data)
        
        update_data = {
            'gia_thue': 2000000.0,
            'tien_coc': 4000000.0,
        }
        
        updated = hop_dong_service.update(created.ma_hop_dong, update_data)
        
        assert updated.gia_thue == 2000000.0
        assert updated.tien_coc == 4000000.0
        
        # Cleanup
        hop_dong_service.delete(created.ma_hop_dong)
    
    def test_update_non_existent(self, hop_dong_service, sample_hop_dong_data):
        """Test update non-existent contract"""
        update_data = {'gia_thue': 2000000.0}
        
        with pytest.raises(ValueError, match="Không tìm thấy hợp đồng"):
            hop_dong_service.update('HD999999', update_data)


class TestHopDongServiceDelete:
    """Test HopDongService.delete()"""
    
    def test_delete_success(self, hop_dong_service, sample_hop_dong_data):
        """Test successful delete"""
        created = hop_dong_service.create(sample_hop_dong_data)
        
        success = hop_dong_service.delete(created.ma_hop_dong)
        assert success is True
        
        # Verify deleted
        deleted = hop_dong_service.get_by_id(created.ma_hop_dong)
        assert deleted is None
    
    def test_delete_non_existent(self, hop_dong_service):
        """Test delete non-existent contract"""
        success = hop_dong_service.delete('HD999999')
        assert success is False


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
