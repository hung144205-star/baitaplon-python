#!/usr/bin/env python3
"""
Report Service - Dịch vụ báo cáo và thống kê tổng hợp
"""
from datetime import datetime, date, timedelta
from typing import List, Dict, Any, Optional
from enum import Enum

from src.services import (
    KhachHangService, KhoService, ViTriService,
    HopDongService, HangHoaService, InventoryService
)


class ReportType(Enum):
    """Loại báo cáo"""
    DAILY = 'daily'
    WEEKLY = 'weekly'
    MONTHLY = 'monthly'
    QUARTERLY = 'quarterly'
    YEARLY = 'yearly'
    CUSTOM = 'custom'


class ReportService:
    """
    Service for generating comprehensive reports and analytics
    """
    
    def __init__(self):
        self.khach_hang_service = KhachHangService()
        self.kho_service = KhoService()
        self.vi_tri_service = ViTriService()
        self.hop_dong_service = HopDongService()
        self.hang_hoa_service = HangHoaService()
        self.inventory_service = InventoryService()
    
    # ==================== Dashboard Statistics ====================
    
    def get_dashboard_summary(self) -> Dict[str, Any]:
        """
        Get comprehensive dashboard summary
        
        Returns:
            Dict with all key metrics
        """
        return {
            'khach_hang': self._get_khach_hang_stats(),
            'kho': self._get_kho_stats(),
            'hop_dong': self._get_hop_dong_stats(),
            'hang_hoa': self._get_hang_hoa_stats(),
            'revenue': self._get_revenue_stats(),
            'alerts': self._get_alert_stats(),
            'generated_at': datetime.now().isoformat()
        }
    
    def _get_khach_hang_stats(self) -> Dict[str, Any]:
        """Get customer statistics"""
        try:
            khach_hangs = self.khach_hang_service.get_all(limit=1000)
            active = sum(1 for kh in khach_hangs if kh.trang_thai == 'hoat_dong')
            
            return {
                'total': len(khach_hangs),
                'active': active,
                'inactive': len(khach_hangs) - active
            }
        except:
            return {'total': 0, 'active': 0, 'inactive': 0}
    
    def _get_kho_stats(self) -> Dict[str, Any]:
        """Get warehouse statistics"""
        try:
            khos = self.kho_service.get_all(limit=100)
            active = sum(1 for k in khos if str(k.trang_thai) == 'hoat_dong')
            
            total_dien_tich = sum(k.dien_tich or 0 for k in khos)
            total_suc_chua = sum(k.suc_chua or 0 for k in khos)
            
            fill_rates = [self.kho_service.calculate_fill_rate(k.ma_kho) for k in khos if k.trang_thai == 'hoat_dong']
            avg_fill_rate = sum(fill_rates) / len(fill_rates) if fill_rates else 0
            
            return {
                'total': len(khos),
                'active': active,
                'total_dien_tich': total_dien_tich,
                'total_suc_chua': total_suc_chua,
                'avg_fill_rate': avg_fill_rate
            }
        except:
            return {'total': 0, 'active': 0, 'total_dien_tich': 0, 'total_suc_chua': 0, 'avg_fill_rate': 0}
    
    def _get_hop_dong_stats(self) -> Dict[str, Any]:
        """Get contract statistics"""
        try:
            hop_dongs = self.hop_dong_service.get_all(limit=1000)
            
            by_status = {}
            for hd in hop_dongs:
                status = str(hd.trang_thai)
                by_status[status] = by_status.get(status, 0) + 1
            
            # Expiring soon (within 30 days)
            today = date.today()
            expiring_soon = sum(
                1 for hd in hop_dongs
                if str(hd.trang_thai) == 'hieu_luc'
                and 0 <= (hd.ngay_ket_thuc - today).days <= 30
            )
            
            # Total revenue from contracts
            total_revenue = sum(
                self.hop_dong_service.calculate_total_amount(hd.ma_hop_dong)['tong_tien_thue']
                for hd in hop_dongs
                if str(hd.trang_thai) == 'hieu_luc'
            )
            
            return {
                'total': len(hop_dongs),
                'by_status': by_status,
                'expiring_soon': expiring_soon,
                'total_revenue': total_revenue
            }
        except:
            return {'total': 0, 'by_status': {}, 'expiring_soon': 0, 'total_revenue': 0}
    
    def _get_hang_hoa_stats(self) -> Dict[str, Any]:
        """Get goods statistics"""
        try:
            summary = self.hang_hoa_service.get_inventory_summary()
            return {
                'total_items': summary['tong_so_mat_hang'],
                'in_stock': summary['so_mat_hang_trong_kho'],
                'total_value': summary['tong_gia_tri'],
                'by_type': summary.get('theo_loai', {})
            }
        except:
            return {'total_items': 0, 'in_stock': 0, 'total_value': 0, 'by_type': {}}
    
    def _get_revenue_stats(self) -> Dict[str, Any]:
        """Get revenue statistics"""
        try:
            hop_dongs = self.hop_dong_service.get_all(limit=1000)
            
            # This month
            today = date.today()
            this_month_start = date(today.year, today.month, 1)
            
            monthly_revenue = 0
            yearly_revenue = 0
            
            for hd in hop_dongs:
                if str(hd.trang_thai) == 'hieu_luc':
                    # Simple calculation: monthly rent * months active
                    monthly_revenue += hd.gia_thue or 0
            
            yearly_revenue = monthly_revenue * 12
            
            return {
                'monthly_revenue': monthly_revenue,
                'yearly_revenue': yearly_revenue,
                'monthly_growth': 0  # Would need historical data
            }
        except:
            return {'monthly_revenue': 0, 'yearly_revenue': 0, 'monthly_growth': 0}
    
    def _get_alert_stats(self) -> Dict[str, Any]:
        """Get alert statistics"""
        try:
            inventory_stats = self.inventory_service.get_alert_statistics()
            
            return {
                'low_stock_count': inventory_stats.get('low', 0) + inventory_stats.get('critical', 0) + inventory_stats.get('empty', 0),
                'critical_alerts': inventory_stats.get('critical', 0) + inventory_stats.get('empty', 0),
                'expiring_contracts': self.hop_dong_service.get_expiring_soon(30).__len__() if hasattr(self.hop_dong_service, 'get_expiring_soon') else 0
            }
        except:
            return {'low_stock_count': 0, 'critical_alerts': 0, 'expiring_contracts': 0}
    
    # ==================== Custom Reports ====================
    
    def generate_summary_report(self, report_type: ReportType = ReportType.MONTHLY) -> Dict[str, Any]:
        """
        Generate summary report
        
        Args:
            report_type: Type of report
            
        Returns:
            Dict with report data
        """
        dashboard = self.get_dashboard_summary()
        
        return {
            'report_type': report_type.value,
            'generated_at': datetime.now().isoformat(),
            'summary': {
                'customers': dashboard['khach_hang'],
                'warehouses': dashboard['kho'],
                'contracts': dashboard['hop_dong'],
                'goods': dashboard['hang_hoa'],
                'revenue': dashboard['revenue'],
                'alerts': dashboard['alerts']
            },
            'highlights': self._get_highlights(dashboard),
            'recommendations': self._get_recommendations(dashboard)
        }
    
    def _get_highlights(self, dashboard: Dict[str, Any]) -> List[str]:
        """Get key highlights from dashboard"""
        highlights = []
        
        # Customer highlights
        if dashboard['khach_hang']['total'] > 0:
            highlights.append(f"✅ Tổng cộng {dashboard['khach_hang']['total']} khách hàng")
        
        # Warehouse highlights
        if dashboard['kho']['avg_fill_rate'] > 75:
            highlights.append(f"⚠️ Tỷ lệ lấp đầy kho cao: {dashboard['kho']['avg_fill_rate']:.1f}%")
        elif dashboard['kho']['avg_fill_rate'] < 50:
            highlights.append(f"💡 Tỷ lệ lấp đầy kho thấp: {dashboard['kho']['avg_fill_rate']:.1f}% - Cần marketing")
        
        # Contract highlights
        if dashboard['hop_dong']['expiring_soon'] > 0:
            highlights.append(f"⚠️ {dashboard['hop_dong']['expiring_soon']} hợp đồng sắp hết hạn")
        
        # Revenue highlights
        if dashboard['revenue']['monthly_revenue'] > 0:
            highlights.append(f"💰 Doanh thu tháng: {dashboard['revenue']['monthly_revenue']:,.0f}₫")
        
        return highlights
    
    def _get_recommendations(self, dashboard: Dict[str, Any]) -> List[str]:
        """Get recommendations based on dashboard"""
        recommendations = []
        
        # Low stock recommendations
        if dashboard['alerts']['low_stock_count'] > 0:
            recommendations.append(f"📦 Cần nhập thêm {dashboard['alerts']['low_stock_count']} mặt hàng sắp hết")
        
        # Expiring contract recommendations
        if dashboard['hop_dong']['expiring_soon'] > 0:
            recommendations.append(f"📋 Liên hệ gia hạn {dashboard['hop_dong']['expiring_soon']} hợp đồng sắp hết hạn")
        
        # Warehouse capacity recommendations
        if dashboard['kho']['avg_fill_rate'] > 90:
            recommendations.append("🏭 Kho gần đầy - Cân nhắc mở rộng hoặc xây kho mới")
        elif dashboard['kho']['avg_fill_rate'] < 30:
            recommendations.append("🏭 Kho còn nhiều chỗ trống - Cần chiến lược marketing")
        
        return recommendations
    
    # ==================== Export Functions ====================
    
    def export_summary_to_text(self, output_path: Optional[str] = None) -> str:
        """
        Export summary report to text file
        
        Args:
            output_path: Path to save report
            
        Returns:
            Path to saved file
        """
        if output_path is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_path = f"data/exports/summary_report_{timestamp}.txt"
        
        report = self.generate_summary_report()
        
        content = f"""
================================================================================
                    BÁO CÁO TỔNG HỢP
                    {datetime.now().strftime('%d/%m/%Y %H:%M')}
================================================================================

I. TỔNG QUAN
─────────────────────────────────────────────────────────────────────────────────
  Báo cáo loại: {report['report_type']}
  Ngày sinh: {report['generated_at']}

II. KHÁCH HÀNG
─────────────────────────────────────────────────────────────────────────────────
  Tổng số: {report['summary']['customers']['total']}
  Đang hoạt động: {report['summary']['customers']['active']}
  Không hoạt động: {report['summary']['customers']['inactive']}

III. KHO HÀNG
─────────────────────────────────────────────────────────────────────────────────
  Tổng số kho: {report['summary']['warehouses']['total']}
  Kho hoạt động: {report['summary']['warehouses']['active']}
  Tổng diện tích: {report['summary']['warehouses']['total_dien_tich']:,.0f} m²
  Tổng sức chứa: {report['summary']['warehouses']['total_suc_chua']:,.0f} m³
  Tỷ lệ lấp đầy TB: {report['summary']['warehouses']['avg_fill_rate']:.1f}%

IV. HỢP ĐỒNG
─────────────────────────────────────────────────────────────────────────────────
  Tổng số hợp đồng: {report['summary']['contracts']['total']}
  Sắp hết hạn (30 ngày): {report['summary']['contracts']['expiring_soon']}
  Tổng doanh thu: {report['summary']['contracts']['total_revenue']:,.0f}₫

V. HÀNG HÓA
─────────────────────────────────────────────────────────────────────────────────
  Tổng số mặt hàng: {report['summary']['goods']['total_items']}
  Đang trong kho: {report['summary']['goods']['in_stock']}
  Tổng giá trị: {report['summary']['goods']['total_value']:,.0f}₫

VI. DOANH THU
─────────────────────────────────────────────────────────────────────────────────
  Doanh thu tháng: {report['summary']['revenue']['monthly_revenue']:,.0f}₫
  Doanh thu năm (dự kiến): {report['summary']['revenue']['yearly_revenue']:,.0f}₫

VII. CẢNH BÁO
─────────────────────────────────────────────────────────────────────────────────
  Hàng sắp hết: {report['summary']['alerts']['low_stock_count']}
  Cảnh báo nghiêm trọng: {report['summary']['alerts']['critical_alerts']}
  Hợp đồng sắp hết hạn: {report['summary']['alerts']['expiring_contracts']}

VIII. ĐIỂM NỔI BẬT
─────────────────────────────────────────────────────────────────────────────────
"""
        
        for highlight in report['highlights']:
            content += f"  {highlight}\n"
        
        content += f"""
IX. KHUYẾN NGHỊ
─────────────────────────────────────────────────────────────────────────────────
"""
        
        for rec in report['recommendations']:
            content += f"  {rec}\n"
        
        content += f"""
================================================================================
                    KẾT THÚC BÁO CÁO
================================================================================
"""
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return output_path


# Convenience functions
def get_dashboard_summary() -> Dict[str, Any]:
    """Get dashboard summary"""
    service = ReportService()
    return service.get_dashboard_summary()


def generate_summary_report(report_type: ReportType = ReportType.MONTHLY) -> Dict[str, Any]:
    """Generate summary report"""
    service = ReportService()
    return service.generate_summary_report(report_type)


def export_summary_to_text() -> str:
    """Export summary to text file"""
    service = ReportService()
    return service.export_summary_to_text()


__all__ = [
    'ReportService',
    'ReportType',
    'get_dashboard_summary',
    'generate_summary_report',
    'export_summary_to_text',
]
