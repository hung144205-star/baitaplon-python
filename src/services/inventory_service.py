#!/usr/bin/env python3
"""
Inventory Management Service - Quản lý tồn kho và cảnh báo
"""
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from enum import Enum

from src.services import HangHoaService, HopDongService
from src.models import HangHoa


class StockAlertLevel(Enum):
    """Mức độ cảnh báo tồn kho"""
    OK = 'ok'  # > 20 items
    LOW = 'low'  # 11-20 items
    CRITICAL = 'critical'  # 1-10 items
    EMPTY = 'empty'  # 0 items


class StockAlert:
    """Đối tượng cảnh báo tồn kho"""
    def __init__(self, hang_hoa: HangHoa, level: StockAlertLevel):
        self.hang_hoa = hang_hoa
        self.level = level
        self.current_stock = hang_hoa.so_luong
        self.threshold = self._get_threshold()
    
    def _get_threshold(self) -> int:
        """Get threshold for alert level"""
        if self.level == StockAlertLevel.CRITICAL:
            return 10
        elif self.level == StockAlertLevel.LOW:
            return 20
        return 0
    
    def get_message(self) -> str:
        """Get alert message"""
        if self.level == StockAlertLevel.EMPTY:
            return f"❌ HẾT HÀNG: {self.hang_hoa.ten_hang} (Mã: {self.hang_hoa.ma_hang_hoa})"
        elif self.level == StockAlertLevel.CRITICAL:
            return f"⚠️ TỒN KHO THẤP: {self.hang_hoa.ten_hang} - Còn {self.current_stock} {self.hang_hoa.don_vi}"
        elif self.level == StockAlertLevel.LOW:
            return f"🔶 SẮP HẾT: {self.hang_hoa.ten_hang} - Còn {self.current_stock} {self.hang_hoa.don_vi}"
        return ""
    
    def get_priority(self) -> str:
        """Get alert priority"""
        if self.level == StockAlertLevel.EMPTY:
            return 'critical'
        elif self.level == StockAlertLevel.CRITICAL:
            return 'high'
        elif self.level == StockAlertLevel.LOW:
            return 'medium'
        return 'low'


class InventoryService:
    """
    Service for inventory management and alerts
    """
    
    def __init__(self):
        self.hang_hoa_service = HangHoaService()
        self.hop_dong_service = HopDongService()
    
    # ==================== Stock Level Tracking ====================
    
    def get_stock_levels(self, ma_hop_dong: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get stock levels for all goods
        
        Args:
            ma_hop_dong: Optional contract filter
            
        Returns:
            List of stock level info
        """
        inventory = self.hang_hoa_service.get_inventory(ma_hop_dong)
        
        stock_levels = []
        for hh in inventory:
            level = self._get_alert_level(hh.so_luong)
            stock_levels.append({
                'ma_hang_hoa': hh.ma_hang_hoa,
                'ten_hang': hh.ten_hang,
                'loai_hang': hh.loai_hang,
                'so_luong': hh.so_luong,
                'don_vi': hh.don_vi,
                'level': level.value,
                'priority': self._get_priority(level),
                'ma_hop_dong': hh.ma_hop_dong
            })
        
        # Sort by priority (critical first)
        priority_order = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}
        stock_levels.sort(key=lambda x: (priority_order[x['priority']], x['so_luong']))
        
        return stock_levels
    
    def _get_alert_level(self, so_luong: int) -> StockAlertLevel:
        """Get alert level based on quantity"""
        if so_luong == 0:
            return StockAlertLevel.EMPTY
        elif so_luong <= 10:
            return StockAlertLevel.CRITICAL
        elif so_luong <= 20:
            return StockAlertLevel.LOW
        return StockAlertLevel.OK
    
    def _get_priority(self, level: StockAlertLevel) -> str:
        """Get priority string from level"""
        if level == StockAlertLevel.EMPTY:
            return 'critical'
        elif level == StockAlertLevel.CRITICAL:
            return 'high'
        elif level == StockAlertLevel.LOW:
            return 'medium'
        return 'low'
    
    # ==================== Low Stock Alerts ====================
    
    def get_low_stock_alerts(self, threshold: int = 20) -> List[StockAlert]:
        """
        Get all low stock alerts
        
        Args:
            threshold: Maximum quantity to consider as low stock
            
        Returns:
            List of StockAlert objects
        """
        inventory = self.hang_hoa_service.get_inventory()
        alerts = []
        
        for hh in inventory:
            if hh.so_luong <= threshold:
                level = self._get_alert_level(hh.so_luong)
                alert = StockAlert(hh, level)
                alerts.append(alert)
        
        # Sort by priority
        priority_order = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}
        alerts.sort(key=lambda x: (priority_order[x.get_priority()], x.current_stock))
        
        return alerts
    
    def get_alert_statistics(self) -> Dict[str, int]:
        """
        Get alert statistics
        
        Returns:
            Dict with counts by level
        """
        inventory = self.hang_hoa_service.get_inventory()
        
        stats = {
            'total_items': len(inventory),
            'ok': 0,
            'low': 0,
            'critical': 0,
            'empty': 0
        }
        
        for hh in inventory:
            level = self._get_alert_level(hh.so_luong)
            stats[level.value] += 1
        
        return stats
    
    # ==================== Inventory Valuation ====================
    
    def get_inventory_valuation(self, ma_hop_dong: Optional[str] = None) -> Dict[str, Any]:
        """
        Get inventory valuation
        
        Args:
            ma_hop_dong: Optional contract filter
            
        Returns:
            Dict with valuation data
        """
        inventory = self.hang_hoa_service.get_inventory(ma_hop_dong)
        
        total_value = sum(hh.gia_tri or 0 for hh in inventory)
        total_items = sum(hh.so_luong for hh in inventory)
        
        # Group by type
        by_type = {}
        for hh in inventory:
            if hh.loai_hang not in by_type:
                by_type[hh.loai_hang] = {
                    'count': 0,
                    'quantity': 0,
                    'value': 0
                }
            by_type[hh.loai_hang]['count'] += 1
            by_type[hh.loai_hang]['quantity'] += hh.so_luong
            by_type[hh.loai_hang]['value'] += hh.gia_tri or 0
        
        # Group by contract
        by_contract = {}
        for hh in inventory:
            if hh.ma_hop_dong not in by_contract:
                by_contract[hh.ma_hop_dong] = {
                    'count': 0,
                    'quantity': 0,
                    'value': 0
                }
            by_contract[hh.ma_hop_dong]['count'] += 1
            by_contract[hh.ma_hop_dong]['quantity'] += hh.so_luong
            by_contract[hh.ma_hop_dong]['value'] += hh.gia_tri or 0
        
        return {
            'total_value': total_value,
            'total_items': total_items,
            'total_types': len(set(hh.loai_hang for hh in inventory)),
            'by_type': by_type,
            'by_contract': by_contract,
            'as_of_date': datetime.now().isoformat()
        }
    
    # ==================== Stock Movement History ====================
    
    def get_stock_movement_history(self, ma_hang_hoa: str) -> List[Dict[str, Any]]:
        """
        Get stock movement history for specific goods
        
        Args:
            ma_hang_hoa: Goods ID
            
        Returns:
            List of movement events
        """
        return self.hang_hoa_service.get_stock_movement_history(ma_hang_hoa)
    
    def get_recent_movements(self, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Get recent stock movements across all goods
        
        Args:
            limit: Maximum number of records
            
        Returns:
            List of recent movements
        """
        inventory = self.hang_hoa_service.get_inventory()
        all_movements = []
        
        for hh in inventory:
            history = self.hang_hoa_service.get_stock_movement_history(hh.ma_hang_hoa)
            for movement in history:
                movement['ma_hang_hoa'] = hh.ma_hang_hoa
                movement['ten_hang'] = hh.ten_hang
                all_movements.append(movement)
        
        # Sort by date descending
        all_movements.sort(key=lambda x: x.get('ngay', ''), reverse=True)
        
        return all_movements[:limit]
    
    # ==================== Inventory Reports ====================
    
    def generate_inventory_report(self, output_path: Optional[str] = None) -> str:
        """
        Generate comprehensive inventory report
        
        Args:
            output_path: Path to save report
            
        Returns:
            Path to saved report
        """
        if output_path is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_path = f"data/exports/inventory_report_{timestamp}.txt"
        
        valuation = self.get_inventory_valuation()
        alerts = self.get_low_stock_alerts()
        stats = self.get_alert_statistics()
        
        report = f"""
================================================================================
                    BÁO CÁO TỒN KHO
                    Ngày {datetime.now().strftime('%d/%m/%Y %H:%M')}
================================================================================

I. TỔNG QUAN
─────────────────────────────────────────────────────────────────────────────────
  Tổng số mặt hàng: {stats['total_items']}
  Tổng giá trị: {valuation['total_value']:,.0f} ₫
  Số loại hàng: {valuation['total_types']}

II. CẢNH BÁO TỒN KHO
─────────────────────────────────────────────────────────────────────────────────
  ✅ Tốt (> 20): {stats['ok']}
  🔶 Thấp (11-20): {stats['low']}
  ⚠️ Rất thấp (1-10): {stats['critical']}
  ❌ Hết hàng (0): {stats['empty']}

III. CHI TIẾT CẢNH BÁO
─────────────────────────────────────────────────────────────────────────────────
"""
        
        if alerts:
            for i, alert in enumerate(alerts, 1):
                report += f"""
{i}. {alert.get_message()}
   Mã: {alert.hang_hoa.ma_hang_hoa}
   Loại: {alert.hang_hoa.loai_hang}
   Hợp đồng: {alert.hang_hoa.ma_hop_dong}
"""
        else:
            report += "\n  ✅ Không có cảnh báo nào\n"
        
        report += f"""
IV. GIÁ TRỊ THEO LOẠI
─────────────────────────────────────────────────────────────────────────────────
"""
        
        for loai, data in valuation['by_type'].items():
            report += f"""
  {loai}:
    - Số mặt hàng: {data['count']}
    - Số lượng: {data['quantity']}
    - Giá trị: {data['value']:,.0f} ₫
"""
        
        report += f"""
================================================================================
                    KẾT THÚC BÁO CÁO
================================================================================
"""
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        return output_path
    
    def generate_low_stock_report(self, output_path: Optional[str] = None) -> str:
        """
        Generate low stock report
        
        Args:
            output_path: Path to save report
            
        Returns:
            Path to saved report
        """
        if output_path is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_path = f"data/exports/low_stock_report_{timestamp}.txt"
        
        alerts = self.get_low_stock_alerts()
        
        report = f"""
================================================================================
                    BÁO CÁO HÀNG SẮP HẾT
                    Ngày {datetime.now().strftime('%d/%m/%Y %H:%M')}
================================================================================

Tổng số mặt hàng cần chú ý: {len(alerts)}

"""
        
        if alerts:
            for i, alert in enumerate(alerts, 1):
                priority_icon = {'critical': '❌', 'high': '⚠️', 'medium': '🔶', 'low': '✅'}
                icon = priority_icon.get(alert.get_priority(), '📌')
                
                report += f"""
{i}. {icon} {alert.get_message()}
   └─ Mã: {alert.hang_hoa.ma_hang_hoa}
   └─ Loại: {alert.hang_hoa.loai_hang}
   └─ Đơn vị: {alert.hang_hoa.don_vi}
   └─ Hợp đồng: {alert.hang_hoa.ma_hop_dong}
   └─ Giá trị: {alert.hang_hoa.gia_tri or 0:,.0f} ₫
"""
        else:
            report += "\n  ✅ Tất cả mặt hàng đều có tồn kho tốt\n"
        
        report += f"""
================================================================================
                    KHUYẾN NGHỊ
================================================================================
"""
        
        critical_count = sum(1 for a in alerts if a.get_priority() in ['critical', 'high'])
        if critical_count > 0:
            report += f"""
  ⚠️ CẦN HÀNH ĐỘNG NGAY: {critical_count} mặt hàng cần được nhập thêm
  - Liên hệ nhà cung cấp để đặt hàng
  - Kiểm tra hợp đồng và vị trí lưu trữ
"""
        
        report += f"""
================================================================================
"""
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        return output_path
    
    # ==================== Dashboard Statistics ====================
    
    def get_dashboard_stats(self) -> Dict[str, Any]:
        """
        Get statistics for inventory dashboard
        
        Returns:
            Dict with dashboard statistics
        """
        valuation = self.get_inventory_valuation()
        alerts = self.get_low_stock_alerts()
        stats = self.get_alert_statistics()
        
        return {
            'total_items': stats['total_items'],
            'total_value': valuation['total_value'],
            'low_stock_count': len(alerts),
            'critical_count': stats['critical'] + stats['empty'],
            'health_percentage': (stats['ok'] / stats['total_items'] * 100) if stats['total_items'] > 0 else 100,
            'by_type': valuation['by_type'],
            'top_low_stock': [
                {
                    'ma_hang_hoa': a.hang_hoa.ma_hang_hoa,
                    'ten_hang': a.hang_hoa.ten_hang,
                    'so_luong': a.current_stock,
                    'priority': a.get_priority()
                }
                for a in alerts[:5]  # Top 5
            ]
        }


# Convenience functions
def get_inventory_stats() -> Dict[str, Any]:
    """Get inventory statistics"""
    service = InventoryService()
    return service.get_dashboard_stats()


def get_low_stock_alerts(threshold: int = 20) -> List[StockAlert]:
    """Get low stock alerts"""
    service = InventoryService()
    return service.get_low_stock_alerts(threshold)


def generate_inventory_report() -> str:
    """Generate inventory report"""
    service = InventoryService()
    return service.generate_inventory_report()


__all__ = [
    'InventoryService',
    'StockAlertLevel',
    'StockAlert',
    'get_inventory_stats',
    'get_low_stock_alerts',
    'generate_inventory_report',
]
