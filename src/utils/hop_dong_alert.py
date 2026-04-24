#!/usr/bin/env python3
"""
Alert Service - Cảnh báo hợp đồng sắp hết hạn
"""
from datetime import datetime, date, timedelta
from typing import List, Dict, Any, Optional

from src.services import HopDongService
from src.models import HopDong, TrangThaiHDEnum


class HopDongAlert:
    """Contract alert object"""
    def __init__(self, hop_dong: HopDong, days_remaining: int, alert_type: str):
        self.hop_dong = hop_dong
        self.days_remaining = days_remaining
        self.alert_type = alert_type  # 'expiring_soon', 'expired', 'overdue'
        self.priority = self._calculate_priority()
    
    def _calculate_priority(self) -> str:
        """Calculate alert priority"""
        if self.alert_type == 'overdue':
            return 'critical'
        elif self.days_remaining <= 7:
            return 'high'
        elif self.days_remaining <= 30:
            return 'medium'
        else:
            return 'low'
    
    def get_message(self) -> str:
        """Get alert message"""
        if self.alert_type == 'expiring_soon':
            return f"Hợp đồng {self.hop_dong.ma_hop_dong} còn {self.days_remaining} ngày là hết hạn"
        elif self.alert_type == 'expired':
            return f"Hợp đồng {self.hop_dong.ma_hop_dong} đã hết hạn hôm nay"
        elif self.alert_type == 'overdue':
            return f"Hợp đồng {self.hop_dong.ma_hop_dong} đã quá hạn {-self.days_remaining} ngày"
        return ""


class HopDongAlertService:
    """
    Service for managing contract expiration alerts
    """
    
    def __init__(self):
        self.service = HopDongService()
    
    def get_expiring_contracts(self, days: int = 30) -> List[HopDongAlert]:
        """
        Get contracts expiring within specified days
        
        Args:
            days: Number of days to check
            
        Returns:
            List of HopDongAlert objects
        """
        today = date.today()
        future_date = today + timedelta(days=days)
        
        # Get all active contracts
        hop_dongs = self.service.get_all(trang_thai=TrangThaiHDEnum.HIEU_LUC)
        
        alerts = []
        for hd in hop_dongs:
            days_remaining = (hd.ngay_ket_thuc - today).days
            
            if 0 <= days_remaining <= days:
                alert = HopDongAlert(hd, days_remaining, 'expiring_soon')
                alerts.append(alert)
        
        # Sort by days remaining (most urgent first)
        alerts.sort(key=lambda x: x.days_remaining)
        
        return alerts
    
    def get_expired_contracts(self) -> List[HopDongAlert]:
        """Get contracts that expired today"""
        today = date.today()
        
        hop_dongs = self.service.get_all(trang_thai=TrangThaiHDEnum.HIEU_LUC)
        
        alerts = []
        for hd in hop_dongs:
            if hd.ngay_ket_thuc == today:
                alert = HopDongAlert(hd, 0, 'expired')
                alerts.append(alert)
        
        return alerts
    
    def get_overdue_contracts(self) -> List[HopDongAlert]:
        """Get contracts that are past due date"""
        today = date.today()
        
        hop_dongs = self.service.get_all(trang_thai=TrangThaiHDEnum.HIEU_LUC)
        
        alerts = []
        for hd in hop_dongs:
            days_remaining = (hd.ngay_ket_thuc - today).days
            if days_remaining < 0:
                alert = HopDongAlert(hd, days_remaining, 'overdue')
                alerts.append(alert)
        
        # Sort by most overdue first
        alerts.sort(key=lambda x: x.days_remaining)
        
        return alerts
    
    def get_all_alerts(self, days: int = 30) -> List[HopDongAlert]:
        """
        Get all contract alerts
        
        Args:
            days: Days for expiring soon check
            
        Returns:
            List of all alerts sorted by priority
        """
        alerts = []
        alerts.extend(self.get_expiring_contracts(days))
        alerts.extend(self.get_expired_contracts())
        alerts.extend(self.get_overdue_contracts())
        
        # Sort by priority
        priority_order = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}
        alerts.sort(key=lambda x: (priority_order[x.priority], x.days_remaining))
        
        return alerts
    
    def get_alert_statistics(self, days: int = 30) -> Dict[str, Any]:
        """
        Get alert statistics
        
        Args:
            days: Days for expiring soon check
            
        Returns:
            Dict with statistics
        """
        alerts = self.get_all_alerts(days)
        
        return {
            'total_alerts': len(alerts),
            'critical': sum(1 for a in alerts if a.priority == 'critical'),
            'high': sum(1 for a in alerts if a.priority == 'high'),
            'medium': sum(1 for a in alerts if a.priority == 'medium'),
            'low': sum(1 for a in alerts if a.priority == 'low'),
            'expiring_soon': len(self.get_expiring_contracts(days)),
            'expired_today': len(self.get_expired_contracts()),
            'overdue': len(self.get_overdue_contracts()),
        }
    
    def send_email_notification(self, alert: HopDongAlert, email: str) -> bool:
        """
        Send email notification (placeholder)
        
        Note: Actual implementation requires email service configuration
        """
        # TODO: Implement email sending
        # For now, just return True
        return True
    
    def send_sms_notification(self, alert: HopDongAlert, phone: str) -> bool:
        """
        Send SMS notification (placeholder)
        
        Note: Actual implementation requires SMS service configuration
        """
        # TODO: Implement SMS sending
        # For now, just return True
        return True
    
    def generate_alert_report(self, output_path: Optional[str] = None) -> str:
        """
        Generate alert report
        
        Args:
            output_path: Path to save report
            
        Returns:
            Path to saved report
        """
        from datetime import datetime
        
        if output_path is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_path = f"data/exports/alert_report_{timestamp}.txt"
        
        alerts = self.get_all_alerts()
        stats = self.get_alert_statistics()
        
        report = f"""
================================================================================
                    BÁO CÁO CẢNH BÁO HỢP ĐỒNG
                    Ngày {datetime.now().strftime('%d/%m/%Y')}
================================================================================

THỐNG KÊ:
  Tổng số cảnh báo: {stats['total_alerts']}
  - Critical: {stats['critical']}
  - High: {stats['high']}
  - Medium: {stats['medium']}
  - Low: {stats['low']}

CHI TIẾT:
  - Sắp hết hạn (trong 30 ngày): {stats['expiring_soon']}
  - Hết hạn hôm nay: {stats['expired_today']}
  - Quá hạn: {stats['overdue']}

================================================================================
DANH SÁCH CẢNH BÁO:
================================================================================
"""
        
        for i, alert in enumerate(alerts, 1):
            report += f"""
{i}. {alert.hop_dong.ma_hop_dong}
   Khách hàng: {alert.hop_dong.ma_khach_hang}
   Vị trí: {alert.hop_dong.ma_vi_tri}
   Ngày kết thúc: {alert.hop_dong.ngay_ket_thuc.strftime('%d/%m/%Y')}
   Còn lại: {alert.days_remaining} ngày
   Mức độ: {alert.priority.upper()}
   Ghi chú: {alert.get_message()}
--------------------------------------------------------------------------------
"""
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        return output_path


# Convenience functions
def get_expiring_alerts(days: int = 30) -> List[HopDongAlert]:
    """Get contracts expiring soon"""
    service = HopDongAlertService()
    return service.get_expiring_contracts(days)


def get_expired_alerts() -> List[HopDongAlert]:
    """Get contracts expired today"""
    service = HopDongAlertService()
    return service.get_expired_contracts()


def get_overdue_alerts() -> List[HopDongAlert]:
    """Get overdue contracts"""
    service = HopDongAlertService()
    return service.get_overdue_contracts()


def get_all_alerts(days: int = 30) -> List[HopDongAlert]:
    """Get all alerts"""
    service = HopDongAlertService()
    return service.get_all_alerts(days)


__all__ = [
    'HopDongAlert',
    'HopDongAlertService',
    'get_expiring_alerts',
    'get_expired_alerts',
    'get_overdue_alerts',
    'get_all_alerts',
]
