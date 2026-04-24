#!/usr/bin/env python3
"""
Tests for HangHoaService (Phase 6)
"""
import pytest
import sys
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.services import HangHoaService, HopDongService
from src.models import HangHoa


@pytest.fixture
def hang_hoa_service():
    """Create HangHoaService instance"""
    return HangHoaService()


@pytest.fixture
def hop_dong_service():
    """Create HopDongService instance"""
    return HopDongService()


@pytest.fixture
def sample_hop_dong(hop_dong_service):
    """Create a sample contract for testing"""
    from datetime import date
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
        'ten_hang': 'Laptop Dell XPS 15',
        'loai_hang': 'Điện tử',
        'so_luong': 10,
        'don_vi': 'cái',
        'trong_luong': 2.0,
        'kich_thuoc': '35x24x2 cm',
        'gia_tri': 25000000.0,
        'vi_tri_luu_tru': 'KHO001-A-01-01-001',
        'ghi_chu': 'Hàng mới 100%'
    }


class TestHangHoaServiceCreate:
    """Test HangHoaService.create()"""
    
    def test_create_hang_hoa_success(self, hang_hoa_service, sample_hang_hoa_data):
        """Test successful goods creation"""
        hang_hoa = hang_hoa_service.create(sample_hang_hoa_data)
        
        assert hang_hoa is not None
        assert hang_hoa.ma_hang_hoa.startswith(sample_hang_hoa_data['ma_hop_dong'])
        assert hang_hoa.ten_hang == sample_hang_hoa_data['ten_hang']
        assert hang_hoa.so_luong == sample_hang_hoa_data['so_luong']
        assert hang_hoa.loai_hang == sample_hang_hoa_data['loai_hang']
        
        # Cleanup
        hang_hoa_service.delete(hang_hoa.ma_hang_hoa)
    
    def test_create_hang_hoa_auto_generate_id(self, hang_hoa_service, sample_hang_hoa_data):
        """Test auto-generation of goods ID"""
        hang_hoa1 = hang_hoa_service.create(sample_hang_hoa_data)
        
        sample_hang_hoa_data['ten_hang'] = 'Laptop HP EliteBook'
        hang_hoa2 = hang_hoa_service.create(sample_hang_hoa_data)
        
        assert hang_hoa1.ma_hang_hoa != hang_hoa2.ma_hang_hoa
        assert hang_hoa1.ma_hang_hoa.endswith('001')
        assert hang_hoa2.ma_hang_hoa.endswith('002')
        
        # Cleanup
        hang_hoa_service.delete(hang_hoa1.ma_hang_hoa)
        hang_hoa_service.delete(hang_hoa2.ma_hang_hoa)
    
    def test_create_hang_hoa_missing_required_fields(self, hang_hoa_service, sample_hop_dong):
        """Test creation with missing required fields"""
        data = {
            'ma_hop_dong': sample_hop_dong.ma_hop_dong,
            # Missing ten_hang, loai_hang, so_luong, don_vi
        }
        
        with pytest.raises(ValueError, match="Thiếu trường bắt buộc"):
            hang_hoa_service.create(data)
    
    def test_create_hang_hoa_invalid_quantity(self, hang_hoa_service, sample_hang_hoa_data):
        """Test creation with invalid quantity"""
        sample_hang_hoa_data['so_luong'] = 0
        
        with pytest.raises(ValueError, match="Số lượng phải lớn hơn 0"):
            hang_hoa_service.create(sample_hang_hoa_data)
    
    def test_create_hang_hoa_invalid_contract(self, hang_hoa_service):
        """Test creation with non-existent contract"""
        data = {
            'ma_hop_dong': 'HD999999',
            'ten_hang': 'Test',
            'loai_hang': 'Test',
            'so_luong': 10,
            'don_vi': 'cái',
        }
        
        with pytest.raises(ValueError, match="Không tìm thấy hợp đồng"):
            hang_hoa_service.create(data)


class TestHangHoaServiceGet:
    """Test HangHoaService retrieval methods"""
    
    def test_get_by_id_success(self, hang_hoa_service, sample_hang_hoa_data):
        """Test get_by_id with valid ID"""
        created = hang_hoa_service.create(sample_hang_hoa_data)
        
        retrieved = hang_hoa_service.get_by_id(created.ma_hang_hoa)
        
        assert retrieved is not None
        assert retrieved.ma_hang_hoa == created.ma_hang_hoa
        assert retrieved.ten_hang == created.ten_hang
        
        # Cleanup
        hang_hoa_service.delete(created.ma_hang_hoa)
    
    def test_get_by_id_not_found(self, hang_hoa_service):
        """Test get_by_id with invalid ID"""
        hang_hoa = hang_hoa_service.get_by_id('HD202604001-HH999')
        assert hang_hoa is None
    
    def test_get_by_hop_dong(self, hang_hoa_service, sample_hang_hoa_data):
        """Test get_by_hop_dong"""
        # Create multiple goods
        created = []
        for i in range(3):
            data = sample_hang_hoa_data.copy()
            data['ten_hang'] = f'Hàng {i+1}'
            hang_hoa = hang_hoa_service.create(data)
            created.append(hang_hoa)
        
        # Get by contract
        hang_hoas = hang_hoa_service.get_by_hop_dong(sample_hang_hoa_data['ma_hop_dong'])
        
        assert len(hang_hoas) >= 3
        assert all(hh.ma_hop_dong == sample_hang_hoa_data['ma_hop_dong'] for hh in hang_hoas)
        
        # Cleanup
        for hh in created:
            hang_hoa_service.delete(hh.ma_hang_hoa)
    
    def test_get_all_with_filters(self, hang_hoa_service, sample_hang_hoa_data):
        """Test get_all with filters"""
        # Create test data
        for i in range(5):
            data = sample_hang_hoa_data.copy()
            data['ten_hang'] = f'Hàng {i+1}'
            data['loai_hang'] = 'Điện tử' if i < 3 else 'May mặc'
            data['trang_thai'] = 'trong_kho' if i < 4 else 'da_xuat'
            hang_hoa_service.create(data)
        
        # Get all
        all_goods = hang_hoa_service.get_all(limit=10)
        assert len(all_goods) >= 5
        
        # Filter by type
        dien_tu = hang_hoa_service.get_all(loai_hang='Điện tử', limit=10)
        assert len(dien_tu) >= 3
        
        # Filter by status
        trong_kho = hang_hoa_service.get_all(trang_thai='trong_kho', limit=10)
        assert len(trong_kho) >= 4
        
        # Cleanup
        for hh in all_goods:
            hang_hoa_service.delete(hh.ma_hang_hoa)


class TestHangHoaServiceImportExport:
    """Test HangHoaService import/export operations"""
    
    def test_import_goods_new(self, hang_hoa_service, sample_hang_hoa_data):
        """Test import_goods for new goods"""
        hang_hoa = hang_hoa_service.import_goods(sample_hang_hoa_data)
        
        assert hang_hoa is not None
        assert hang_hoa.so_luong == sample_hang_hoa_data['so_luong']
        assert hang_hoa.trang_thai == 'trong_kho'
        assert hang_hoa.ngay_nhap is not None
        
        # Cleanup
        hang_hoa_service.delete(hang_hoa.ma_hang_hoa)
    
    def test_import_goods_merge(self, hang_hoa_service, sample_hang_hoa_data):
        """Test import_goods merging with existing"""
        # First import
        hang_hoa1 = hang_hoa_service.import_goods(sample_hang_hoa_data)
        initial_qty = hang_hoa1.so_luong
        
        # Second import (same name & type)
        import_data = sample_hang_hoa_data.copy()
        import_data['so_luong'] = 5
        hang_hoa2 = hang_hoa_service.import_goods(import_data)
        
        assert hang_hoa2.ma_hang_hoa == hang_hoa1.ma_hang_hoa
        assert hang_hoa2.so_luong == initial_qty + 5
        
        # Cleanup
        hang_hoa_service.delete(hang_hoa1.ma_hang_hoa)
    
    def test_export_goods_success(self, hang_hoa_service, sample_hang_hoa_data):
        """Test successful goods export"""
        # Create goods
        hang_hoa = hang_hoa_service.create(sample_hang_hoa_data)
        initial_qty = hang_hoa.so_luong
        
        # Export
        success = hang_hoa_service.export_goods(hang_hoa.ma_hang_hoa, 3)
        
        assert success is True
        
        # Verify quantity reduced
        updated = hang_hoa_service.get_by_id(hang_hoa.ma_hang_hoa)
        assert updated.so_luong == initial_qty - 3
        
        # Cleanup
        hang_hoa_service.delete(hang_hoa.ma_hang_hoa)
    
    def test_export_goods_insufficient_stock(self, hang_hoa_service, sample_hang_hoa_data):
        """Test export with insufficient stock"""
        hang_hoa = hang_hoa_service.create(sample_hang_hoa_data)
        
        # Try to export more than available
        with pytest.raises(ValueError, match="Số lượng không đủ"):
            hang_hoa_service.export_goods(hang_hoa.ma_hang_hoa, 100)
        
        # Cleanup
        hang_hoa_service.delete(hang_hoa.ma_hang_hoa)
    
    def test_export_goods_zero_quantity(self, hang_hoa_service, sample_hang_hoa_data):
        """Test export with zero quantity"""
        hang_hoa = hang_hoa_service.create(sample_hang_hoa_data)
        
        with pytest.raises(ValueError, match="Số lượng xuất phải lớn hơn 0"):
            hang_hoa_service.export_goods(hang_hoa.ma_hang_hoa, 0)
        
        # Cleanup
        hang_hoa_service.delete(hang_hoa.ma_hang_hoa)
    
    def test_export_all_stock(self, hang_hoa_service, sample_hang_hoa_data):
        """Test export all stock"""
        sample_hang_hoa_data['so_luong'] = 5
        hang_hoa = hang_hoa_service.create(sample_hang_hoa_data)
        
        # Export all
        success = hang_hoa_service.export_goods(hang_hoa.ma_hang_hoa, 5)
        
        assert success is True
        
        # Verify status changed
        updated = hang_hoa_service.get_by_id(hang_hoa.ma_hang_hoa)
        assert updated.so_luong == 0
        assert updated.trang_thai == 'da_xuat'
        assert updated.ngay_xuat is not None
        
        # Cleanup
        hang_hoa_service.delete(hang_hoa.ma_hang_hoa)


class TestHangHoaServiceQuery:
    """Test HangHoaService query methods"""
    
    def test_get_inventory(self, hang_hoa_service, sample_hang_hoa_data):
        """Test get_inventory"""
        # Create in-stock goods
        for i in range(3):
            data = sample_hang_hoa_data.copy()
            data['ten_hang'] = f'Hàng {i+1}'
            data['trang_thai'] = 'trong_kho'
            hang_hoa_service.create(data)
        
        # Create exported goods
        exported_data = sample_hang_hoa_data.copy()
        exported_data['ten_hang'] = 'Đã xuất'
        exported_data['trang_thai'] = 'da_xuat'
        hang_hoa_service.create(exported_data)
        
        # Get inventory (should only return in-stock)
        inventory = hang_hoa_service.get_inventory()
        
        assert len(inventory) >= 3
        assert all(hh.trang_thai == 'trong_kho' for hh in inventory)
        
        # Cleanup
        for hh in inventory:
            hang_hoa_service.delete(hh.ma_hang_hoa)
        hang_hoa_service.delete(exported_data['ma_hop_dong'] + '-HH004')
    
    def test_get_by_type(self, hang_hoa_service, sample_hang_hoa_data):
        """Test get_by_type"""
        # Create different types
        for loai in ['Điện tử', 'May mặc', 'Điện tử']:
            data = sample_hang_hoa_data.copy()
            data['loai_hang'] = loai
            data['ten_hang'] = f'Hàng {loai}'
            hang_hoa_service.create(data)
        
        # Get by type
        dien_tu = hang_hoa_service.get_by_type('Điện tử', limit=10)
        
        assert len(dien_tu) >= 2
        assert all(hh.loai_hang == 'Điện tử' for hh in dien_tu)
        
        # Cleanup
        for hh in dien_tu:
            hang_hoa_service.delete(hh.ma_hang_hoa)
    
    def test_search(self, hang_hoa_service, sample_hang_hoa_data):
        """Test search"""
        # Create goods with different names
        for name in ['Laptop Dell', 'Laptop HP', 'Điện thoại']:
            data = sample_hang_hoa_data.copy()
            data['ten_hang'] = name
            hang_hoa_service.create(data)
        
        # Search by keyword
        results = hang_hoa_service.search('Laptop', limit=10)
        
        assert len(results) >= 2
        assert all('Laptop' in hh.ten_hang for hh in results)
        
        # Cleanup
        for hh in results:
            hang_hoa_service.delete(hh.ma_hang_hoa)
    
    def test_get_low_stock(self, hang_hoa_service, sample_hang_hoa_data):
        """Test get_low_stock"""
        # Create low stock goods
        for qty in [5, 8, 15, 25]:
            data = sample_hang_hoa_data.copy()
            data['so_luong'] = qty
            data['ten_hang'] = f'Hàng SL={qty}'
            hang_hoa_service.create(data)
        
        # Get low stock (threshold=10)
        low_stock = hang_hoa_service.get_low_stock(threshold=10)
        
        assert len(low_stock) >= 2
        assert all(hh.so_luong <= 10 for hh in low_stock)
        
        # Cleanup
        for hh in low_stock:
            hang_hoa_service.delete(hh.ma_hang_hoa)


class TestHangHoaServiceBusinessLogic:
    """Test HangHoaService business logic methods"""
    
    def test_get_tong_gia_tri(self, hang_hoa_service, sample_hang_hoa_data):
        """Test get_tong_gia_tri"""
        # Create goods with different values
        for value in [1000000, 2000000, 3000000]:
            data = sample_hang_hoa_data.copy()
            data['gia_tri'] = value
            data['ten_hang'] = f'Hàng {value}'
            hang_hoa_service.create(data)
        
        total = hang_hoa_service.get_tong_gia_tri()
        
        assert total == 6000000.0
        
        # Cleanup
        all_goods = hang_hoa_service.get_all(limit=10)
        for hh in all_goods:
            hang_hoa_service.delete(hh.ma_hang_hoa)
    
    def test_get_inventory_summary(self, hang_hoa_service, sample_hang_hoa_data):
        """Test get_inventory_summary"""
        # Create test data
        for i in range(5):
            data = sample_hang_hoa_data.copy()
            data['loai_hang'] = 'Điện tử' if i < 3 else 'May mặc'
            data['ten_hang'] = f'Hàng {i+1}'
            data['gia_tri'] = 1000000 * (i + 1)
            hang_hoa_service.create(data)
        
        summary = hang_hoa_service.get_inventory_summary()
        
        assert 'tong_so_mat_hang' in summary
        assert 'so_mat_hang_trong_kho' in summary
        assert 'tong_gia_tri' in summary
        assert 'theo_loai' in summary
        assert len(summary['theo_loai']) >= 2
        
        # Cleanup
        all_goods = hang_hoa_service.get_all(limit=10)
        for hh in all_goods:
            hang_hoa_service.delete(hh.ma_hang_hoa)
    
    def test_get_stock_movement_history(self, hang_hoa_service, sample_hang_hoa_data):
        """Test get_stock_movement_history"""
        hang_hoa = hang_hoa_service.create(sample_hang_hoa_data)
        
        # Get history
        history = hang_hoa_service.get_stock_movement_history(hang_hoa.ma_hang_hoa)
        
        assert len(history) > 0
        assert any(event['su_kien'] == 'Nhập kho' for event in history)
        
        # Cleanup
        hang_hoa_service.delete(hang_hoa.ma_hang_hoa)


class TestHangHoaServiceUpdate:
    """Test HangHoaService.update()"""
    
    def test_update_success(self, hang_hoa_service, sample_hang_hoa_data):
        """Test successful update"""
        created = hang_hoa_service.create(sample_hang_hoa_data)
        
        update_data = {
            'so_luong': 20,
            'gia_tri': 30000000.0,
            'ghi_chu': 'Updated notes'
        }
        
        updated = hang_hoa_service.update(created.ma_hang_hoa, update_data)
        
        assert updated.so_luong == 20
        assert updated.gia_tri == 30000000.0
        assert updated.ghi_chu == 'Updated notes'
        
        # Cleanup
        hang_hoa_service.delete(created.ma_hang_hoa)
    
    def test_update_negative_quantity(self, hang_hoa_service, sample_hang_hoa_data):
        """Test update with negative quantity"""
        created = hang_hoa_service.create(sample_hang_hoa_data)
        
        with pytest.raises(ValueError, match="Số lượng không được âm"):
            hang_hoa_service.update(created.ma_hang_hoa, {'so_luong': -5})
        
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
        deleted = hang_hoa_service.get_by_id(created.ma_hang_hoa)
        assert deleted is None


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
