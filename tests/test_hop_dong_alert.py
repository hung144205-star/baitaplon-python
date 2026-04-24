#!/usr/bin/env python3
"""
Tests for HopDongAlertService and export utilities
"""
import pytest
import sys
from pathlib import Path
from datetime import date, timedelta

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.utils.hop_dong_alert import HopDongAlertService, HopDongAlert, get_all_alerts
from src.utils.hop_dong_export import calculate_total_rent, export_hop_dong_to_pdf, generate_hop_dong_preview
from src.services import HopDongService, TrangThaiHDEnum


@pytest.fixture
def alert_service():
    """Create HopDongAlertService instance"""
    return HopDongAlertService()


@pytest.fixture
def hop_dong_service():
    """Create HopDongService instance"""
    return HopDongService()


@pytest.fixture
def sample_hop_dong(hop_dong_service):
    """Create a sample contract for testing"""
    today = date.today()
    data = {
        'ma_khach_hang': 'KH001',
        'ma_vi_tri': 'KHO001-A-01-01-001',
        'ngay_bat_dau': today,
        'ngay_ket_thuc': today + timedelta(days=30),
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


class TestHopDongAlert:
    """Test HopDongAlert class"""
    
    def test_alert_priority_critical(self, sample_hop_dong):
        """Test critical priority (overdue)"""
        # Make contract overdue
        sample_hop_dong.ngay_ket_thuc = date.today() - timedelta(days=5)
        alert = HopDongAlert(sample_hop_dong, -5, 'overdue')
        
        assert alert.priority == 'critical'
    
    def test_alert_priority_high(self, sample_hop_dong):
        """Test high priority (<= 7 days)"""
        alert = HopDongAlert(sample_hop_dong, 5, 'expiring_soon')
        
        assert alert.priority == 'high'
    
    def test_alert_priority_medium(self, sample_hop_dong):
        """Test medium priority (8-30 days)"""
        alert = HopDongAlert(sample_hop_dong, 15, 'expiring_soon')
        
        assert alert.priority == 'medium'
    
    def test_alert_priority_low(self, sample_hop_dong):
        """Test low priority (> 30 days)"""
        alert = HopDongAlert(sample_hop_dong, 45, 'expiring_soon')
        
        assert alert.priority == 'low'
    
    def test_alert_message_expiring_soon(self, sample_hop_dong):
        """Test alert message for expiring soon"""
        alert = HopDongAlert(sample_hop_dong, 15, 'expiring_soon')
        message = alert.get_message()
        
        assert 'còn' in message
        assert 'ngày' in message
        assert 'hết hạn' in message
    
    def test_alert_message_overdue(self, sample_hop_dong):
        """Test alert message for overdue"""
        alert = HopDongAlert(sample_hop_dong, -5, 'overdue')
        message = alert.get_message()
        
        assert 'quá hạn' in message


class TestHopDongAlertService:
    """Test HopDongAlertService methods"""
    
    def test_get_expiring_contracts(self, alert_service, sample_hop_dong, hop_dong_service):
        """Test get_expiring_contracts"""
        # Create contract expiring in 15 days
        today = date.today()
        data = {
            'ma_khach_hang': 'KH002',
            'ma_vi_tri': 'KHO001-A-01-01-002',
            'ngay_bat_dau': today,
            'ngay_ket_thuc': today + timedelta(days=15),
            'gia_thue': 1500000.0,
            'tien_coc': 3000000.0,
            'phuong_thuc_thanh_toan': 'hang_thang',
        }
        expiring_hd = hop_dong_service.create(data)
        
        # Get expiring contracts
        alerts = alert_service.get_expiring_contracts(days=30)
        
        assert len(alerts) >= 1
        assert any(a.hop_dong.ma_hop_dong == expiring_hd.ma_hop_dong for a in alerts)
        
        # Cleanup
        hop_dong_service.delete(expiring_hd.ma_hop_dong)
    
    def test_get_expired_contracts(self, alert_service, hop_dong_service):
        """Test get_expired_contracts"""
        # Create contract expiring today
        today = date.today()
        data = {
            'ma_khach_hang': 'KH003',
            'ma_vi_tri': 'KHO001-A-01-01-003',
            'ngay_bat_dau': today - timedelta(days=30),
            'ngay_ket_thuc': today,
            'gia_thue': 1500000.0,
            'tien_coc': 3000000.0,
            'phuong_thuc_thanh_toan': 'hang_thang',
        }
        expired_hd = hop_dong_service.create(data)
        
        # Get expired contracts
        alerts = alert_service.get_expired_contracts()
        
        assert len(alerts) >= 1
        assert any(a.hop_dong.ma_hop_dong == expired_hd.ma_hop_dong for a in alerts)
        
        # Cleanup
        hop_dong_service.delete(expired_hd.ma_hop_dong)
    
    def test_get_overdue_contracts(self, alert_service, hop_dong_service):
        """Test get_overdue_contracts"""
        # Create overdue contract
        today = date.today()
        data = {
            'ma_khach_hang': 'KH004',
            'ma_vi_tri': 'KHO001-A-01-01-004',
            'ngay_bat_dau': today - timedelta(days=60),
            'ngay_ket_thuc': today - timedelta(days=5),
            'gia_thue': 1500000.0,
            'tien_coc': 3000000.0,
            'phuong_thuc_thanh_toan': 'hang_thang',
        }
        overdue_hd = hop_dong_service.create(data)
        
        # Get overdue contracts
        alerts = alert_service.get_overdue_contracts()
        
        assert len(alerts) >= 1
        assert any(a.hop_dong.ma_hop_dong == overdue_hd.ma_hop_dong for a in alerts)
        
        # Cleanup
        hop_dong_service.delete(overdue_hd.ma_hop_dong)
    
    def test_get_alert_statistics(self, alert_service):
        """Test get_alert_statistics"""
        stats = alert_service.get_alert_statistics(days=30)
        
        assert 'total_alerts' in stats
        assert 'critical' in stats
        assert 'high' in stats
        assert 'medium' in stats
        assert 'low' in stats
        assert 'expiring_soon' in stats
        assert 'expired_today' in stats
        assert 'overdue' in stats
    
    def test_generate_alert_report(self, alert_service):
        """Test generate_alert_report"""
        import os
        
        # Generate report
        report_path = alert_service.generate_alert_report()
        
        # Check file exists
        assert os.path.exists(report_path)
        
        # Check file size > 0
        assert os.path.getsize(report_path) > 0
        
        # Cleanup
        os.remove(report_path)


class TestCalculateTotalRent:
    """Test calculate_total_rent utility"""
    
    def test_calculate_total_rent_12_months(self, sample_hop_dong):
        """Test calculate total rent for 12 months"""
        sample_hop_dong.ngay_bat_dau = date(2026, 1, 1)
        sample_hop_dong.ngay_ket_thuc = date(2026, 12, 31)
        sample_hop_dong.gia_thue = 1000000.0
        
        total = calculate_total_rent(sample_hop_dong)
        
        # 11 months difference (Jan to Dec)
        assert total == 11000000.0
    
    def test_calculate_total_rent_6_months(self, sample_hop_dong):
        """Test calculate total rent for 6 months"""
        sample_hop_dong.ngay_bat_dau = date(2026, 1, 1)
        sample_hop_dong.ngay_ket_thuc = date(2026, 6, 30)
        sample_hop_dong.gia_thue = 2000000.0
        
        total = calculate_total_rent(sample_hop_dong)
        
        # 5 months difference
        assert total == 10000000.0


class TestExportHopDong:
    """Test export utilities"""
    
    def test_export_hop_dong_to_pdf(self, sample_hop_dong):
        """Test export contract to file"""
        import os
        
        # Export
        output_path = export_hop_dong_to_pdf(sample_hop_dong)
        
        # Check file exists
        assert os.path.exists(output_path)
        
        # Check file size > 0
        assert os.path.getsize(output_path) > 0
        
        # Cleanup
        os.remove(output_path)
    
    def test_generate_hop_dong_preview(self, sample_hop_dong):
        """Test generate HTML preview"""
        html = generate_hop_dong_preview(sample_hop_dong)
        
        assert '<html>' in html
        assert '</html>' in html
        assert sample_hop_dong.ma_hop_dong in html
        assert 'HỢP ĐỒNG THUÊ KHO' in html


class TestGetAllAlerts:
    """Test convenience functions"""
    
    def test_get_all_alerts(self, alert_service):
        """Test get_all_alerts"""
        alerts = get_all_alerts(days=30)
        
        assert isinstance(alerts, list)
        
        # All alerts should have required attributes
        for alert in alerts:
            assert hasattr(alert, 'hop_dong')
            assert hasattr(alert, 'days_remaining')
            assert hasattr(alert, 'alert_type')
            assert hasattr(alert, 'priority')
            assert hasattr(alert, 'get_message')


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
