#!/usr/bin/env python3
"""
Tests for InventoryService and Stock Alerts (Phase 6.5)
"""
import pytest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.utils.inventory_service import (
    InventoryService, StockAlertLevel, StockAlert,
    get_inventory_stats, get_low_stock_alerts, generate_inventory_report
)
from src.services import HangHoaService, HopDongService


@pytest.fixture
def inventory_service():
    """Create InventoryService instance"""
    return InventoryService()


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
def create_test_inventory(hang_hoa_service, sample_hop_dong):
    """Create test inventory with various stock levels"""
    created = []
    
    # OK stock (> 20)
    for i in range(3):
        data = {
            'ma_hop_dong': sample_hop_dong.ma_hop_dong,
            'ten_hang': f'Hàng OK {i+1}',
            'loai_hang': 'Điện tử',
            'so_luong': 50,
            'don_vi': 'cái',
            'gia_tri': 1000000.0
        }
        hh = hang_hoa_service.create(data)
        created.append(hh)
    
    # LOW stock (11-20)
    for i in range(2):
        data = {
            'ma_hop_dong': sample_hop_dong.ma_hop_dong,
            'ten_hang': f'Hàng LOW {i+1}',
            'loai_hang': 'May mặc',
            'so_luong': 15,
            'don_vi': 'cái',
            'gia_tri': 500000.0
        }
        hh = hang_hoa_service.create(data)
        created.append(hh)
    
    # CRITICAL stock (1-10)
    for i in range(2):
        data = {
            'ma_hop_dong': sample_hop_dong.ma_hop_dong,
            'ten_hang': f'Hàng CRITICAL {i+1}',
            'loai_hang': 'Thực phẩm',
            'so_luong': 5,
            'don_vi': 'hộp',
            'gia_tri': 200000.0
        }
        hh = hang_hoa_service.create(data)
        created.append(hh)
    
    # EMPTY stock (0)
    data = {
        'ma_hop_dong': sample_hop_dong.ma_hop_dong,
        'ten_hang': 'Hàng EMPTY',
        'loai_hang': 'Khác',
        'so_luong': 0,
        'don_vi': 'cái',
        'gia_tri': 100000.0
    }
    hh = hang_hoa_service.create(data)
    created.append(hh)
    
    yield created
    
    # Cleanup
    for hh in created:
        try:
            hang_hoa_service.delete(hh.ma_hang_hoa)
        except:
            pass


class TestStockAlertLevel:
    """Test StockAlertLevel enum"""
    
    def test_alert_levels(self):
        """Test alert level values"""
        assert StockAlertLevel.OK.value == 'ok'
        assert StockAlertLevel.LOW.value == 'low'
        assert StockAlertLevel.CRITICAL.value == 'critical'
        assert StockAlertLevel.EMPTY.value == 'empty'


class TestStockAlert:
    """Test StockAlert class"""
    
    def test_stock_alert_empty(self, sample_hop_dong):
        """Test alert for empty stock"""
        hang_hoa = type('HangHoa', (), {
            'ma_hang_hoa': 'HD001-HH001',
            'ten_hang': 'Test',
            'loai_hang': 'Test',
            'so_luong': 0,
            'don_vi': 'cái',
            'ma_hop_dong': sample_hop_dong.ma_hop_dong
        })()
        
        alert = StockAlert(hang_hoa, StockAlertLevel.EMPTY)
        
        assert alert.level == StockAlertLevel.EMPTY
        assert alert.current_stock == 0
        assert alert.get_priority() == 'critical'
        assert 'HẾT HÀNG' in alert.get_message()
    
    def test_stock_alert_critical(self, sample_hop_dong):
        """Test alert for critical stock"""
        hang_hoa = type('HangHoa', (), {
            'ma_hang_hoa': 'HD001-HH001',
            'ten_hang': 'Test',
            'loai_hang': 'Test',
            'so_luong': 5,
            'don_vi': 'cái',
            'ma_hop_dong': sample_hop_dong.ma_hop_dong
        })()
        
        alert = StockAlert(hang_hoa, StockAlertLevel.CRITICAL)
        
        assert alert.level == StockAlertLevel.CRITICAL
        assert alert.current_stock == 5
        assert alert.get_priority() == 'high'
        assert 'TỒN KHO THẤP' in alert.get_message()
    
    def test_stock_alert_low(self, sample_hop_dong):
        """Test alert for low stock"""
        hang_hoa = type('HangHoa', (), {
            'ma_hang_hoa': 'HD001-HH001',
            'ten_hang': 'Test',
            'loai_hang': 'Test',
            'so_luong': 15,
            'don_vi': 'cái',
            'ma_hop_dong': sample_hop_dong.ma_hop_dong
        })()
        
        alert = StockAlert(hang_hoa, StockAlertLevel.LOW)
        
        assert alert.level == StockAlertLevel.LOW
        assert alert.current_stock == 15
        assert alert.get_priority() == 'medium'
        assert 'SẮP HẾT' in alert.get_message()


class TestInventoryServiceGetStockLevels:
    """Test InventoryService.get_stock_levels()"""
    
    def test_get_stock_levels(self, inventory_service, create_test_inventory):
        """Test getting stock levels"""
        stock_levels = inventory_service.get_stock_levels()
        
        assert len(stock_levels) >= 8
        
        # Check sorting (critical first)
        priorities = [item['priority'] for item in stock_levels]
        priority_order = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}
        sorted_priorities = sorted(priorities, key=lambda x: priority_order[x])
        assert priorities == sorted_priorities
    
    def test_get_stock_levels_by_contract(self, inventory_service, create_test_inventory, sample_hop_dong):
        """Test getting stock levels filtered by contract"""
        stock_levels = inventory_service.get_stock_levels(ma_hop_dong=sample_hop_dong.ma_hop_dong)
        
        assert len(stock_levels) >= 8
        assert all(item['ma_hop_dong'] == sample_hop_dong.ma_hop_dong for item in stock_levels)


class TestInventoryServiceAlerts:
    """Test InventoryService alert methods"""
    
    def test_get_low_stock_alerts(self, inventory_service, create_test_inventory):
        """Test getting low stock alerts"""
        alerts = inventory_service.get_low_stock_alerts(threshold=20)
        
        # Should include LOW, CRITICAL, and EMPTY
        assert len(alerts) >= 5
        
        # Check priorities
        priorities = [alert.get_priority() for alert in alerts]
        assert 'critical' in priorities
        assert 'high' in priorities
        assert 'medium' in priorities
    
    def test_get_alert_statistics(self, inventory_service, create_test_inventory):
        """Test getting alert statistics"""
        stats = inventory_service.get_alert_statistics()
        
        assert 'total_items' in stats
        assert 'ok' in stats
        assert 'low' in stats
        assert 'critical' in stats
        assert 'empty' in stats
        
        assert stats['total_items'] >= 8
        assert stats['ok'] >= 3
        assert stats['low'] >= 2
        assert stats['critical'] >= 2
        assert stats['empty'] >= 1


class TestInventoryServiceValuation:
    """Test InventoryService valuation methods"""
    
    def test_get_inventory_valuation(self, inventory_service, create_test_inventory):
        """Test getting inventory valuation"""
        valuation = inventory_service.get_inventory_valuation()
        
        assert 'total_value' in valuation
        assert 'total_items' in valuation
        assert 'total_types' in valuation
        assert 'by_type' in valuation
        assert 'by_contract' in valuation
        
        assert valuation['total_value'] > 0
        assert valuation['total_items'] > 0
        assert valuation['total_types'] >= 3  # Điện tử, May mặc, Thực phẩm, Khác
    
    def test_get_inventory_valuation_by_type(self, inventory_service, create_test_inventory):
        """Test valuation grouped by type"""
        valuation = inventory_service.get_inventory_valuation()
        
        by_type = valuation['by_type']
        
        assert 'Điện tử' in by_type
        assert 'May mặc' in by_type
        
        assert by_type['Điện tử']['count'] >= 3
        assert by_type['Điện tử']['value'] > 0


class TestInventoryServiceHistory:
    """Test InventoryService history methods"""
    
    def test_get_stock_movement_history(self, inventory_service, create_test_inventory):
        """Test getting stock movement history"""
        hang_hoa = create_test_inventory[0]
        
        history = inventory_service.get_stock_movement_history(hang_hoa.ma_hang_hoa)
        
        assert len(history) > 0
        assert any(event['su_kien'] == 'Nhập kho' for event in history)
    
    def test_get_recent_movements(self, inventory_service, create_test_inventory):
        """Test getting recent movements"""
        movements = inventory_service.get_recent_movements(limit=10)
        
        assert len(movements) <= 10
        assert len(movements) > 0
        
        # Check sorting (most recent first)
        dates = [m.get('ngay', '') for m in movements]
        assert dates == sorted(dates, reverse=True)


class TestInventoryServiceReports:
    """Test InventoryService report generation"""
    
    def test_generate_inventory_report(self, inventory_service, create_test_inventory):
        """Test generating inventory report"""
        import os
        
        report_path = inventory_service.generate_inventory_report()
        
        # Check file exists
        assert os.path.exists(report_path)
        
        # Check file size > 0
        assert os.path.getsize(report_path) > 0
        
        # Check content
        with open(report_path, 'r', encoding='utf-8') as f:
            content = f.read()
            assert 'BÁO CÁO TỒN KHO' in content
            assert 'TỔNG QUAN' in content
            assert 'CẢNH BÁO TỒN KHO' in content
        
        # Cleanup
        os.remove(report_path)
    
    def test_generate_low_stock_report(self, inventory_service, create_test_inventory):
        """Test generating low stock report"""
        import os
        
        report_path = inventory_service.generate_low_stock_report()
        
        # Check file exists
        assert os.path.exists(report_path)
        
        # Check file size > 0
        assert os.path.getsize(report_path) > 0
        
        # Check content
        with open(report_path, 'r', encoding='utf-8') as f:
            content = f.read()
            assert 'BÁO CÁO HÀNG SẮP HẾT' in content
            assert 'KHUYẾN NGHỊ' in content
        
        # Cleanup
        os.remove(report_path)


class TestInventoryServiceDashboard:
    """Test InventoryService dashboard statistics"""
    
    def test_get_dashboard_stats(self, inventory_service, create_test_inventory):
        """Test getting dashboard statistics"""
        stats = inventory_service.get_dashboard_stats()
        
        assert 'total_items' in stats
        assert 'total_value' in stats
        assert 'low_stock_count' in stats
        assert 'critical_count' in stats
        assert 'health_percentage' in stats
        assert 'top_low_stock' in stats
        
        assert stats['total_items'] >= 8
        assert stats['total_value'] > 0
        assert stats['low_stock_count'] >= 5
        assert stats['critical_count'] >= 3
        assert 0 <= stats['health_percentage'] <= 100
        assert len(stats['top_low_stock']) <= 5


class TestConvenienceFunctions:
    """Test convenience functions"""
    
    def test_get_inventory_stats(self):
        """Test get_inventory_stats function"""
        stats = get_inventory_stats()
        
        assert isinstance(stats, dict)
        assert 'total_items' in stats
        assert 'total_value' in stats
    
    def test_get_low_stock_alerts(self):
        """Test get_low_stock_alerts function"""
        alerts = get_low_stock_alerts(threshold=20)
        
        assert isinstance(alerts, list)
        
        # All alerts should be StockAlert objects
        for alert in alerts:
            assert isinstance(alert, StockAlert)
    
    def test_generate_inventory_report(self):
        """Test generate_inventory_report function"""
        import os
        
        report_path = generate_inventory_report()
        
        assert os.path.exists(report_path)
        
        # Cleanup
        os.remove(report_path)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
