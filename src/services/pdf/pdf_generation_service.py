#!/usr/bin/env python3
"""
PDF Generation Service - Dịch vụ tạo file PDF cho hệ thống quản lý kho lưu trữ
"""
import os
import datetime
from typing import Dict, Any, Optional, List
from pathlib import Path

from src.services import (
    KhachHangService, KhoService, ViTriService,
    HopDongService, HangHoaService, ThanhToanService
)
from src.utils.formatters import format_currency, format_date


class PDFGenerationService:
    """
    Service for generating PDF documents
    Note: This is a framework implementation. Actual PDF generation requires
    additional libraries like ReportLab, WeasyPrint, or wkhtmltopdf.
    """
    
    def __init__(self):
        self.template_dir = Path("src/templates/pdf")
        self.output_dir = Path("data/exports/pdf")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize services
        self.khach_hang_service = KhachHangService()
        self.kho_service = KhoService()
        self.vi_tri_service = ViTriService()
        self.hop_dong_service = HopDongService()
        self.hang_hoa_service = HangHoaService()
        self.thanh_toan_service = ThanhToanService()
    
    def _load_template(self, template_name: str) -> str:
        """Load HTML template"""
        template_path = self.template_dir / f"{template_name}_template.html"
        with open(template_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def _render_template(self, template: str, context: Dict[str, Any]) -> str:
        """Simple template rendering (basic placeholder replacement)"""
        rendered = template
        
        # Replace simple placeholders
        for key, value in context.items():
            placeholder = f"{{{{ {key} }}}}"
            if isinstance(value, (int, float)):
                rendered = rendered.replace(placeholder, str(value))
            elif value is None:
                rendered = rendered.replace(placeholder, "")
            else:
                rendered = rendered.replace(placeholder, str(value))
        
        # Handle number formatting
        rendered = rendered.replace("| number_format", "")
        
        return rendered
    
    def _save_html(self, content: str, filename: str) -> str:
        """Save HTML content to file"""
        html_path = self.output_dir / filename
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return str(html_path)
    
    def _convert_html_to_pdf(self, html_path: str, pdf_path: str) -> bool:
        """
        Convert HTML to PDF
        This is a placeholder method. Actual implementation would use
        libraries like ReportLab, WeasyPrint, or system tools like wkhtmltopdf.
        """
        # TODO: Implement actual PDF conversion when dependencies are available
        print(f"PDF conversion would convert {html_path} to {pdf_path}")
        print("This requires additional libraries like ReportLab or WeasyPrint")
        return False
    
    def generate_contract_pdf(self, ma_hop_dong: str, output_filename: Optional[str] = None) -> str:
        """
        Generate contract PDF
        
        Args:
            ma_hop_dong: Contract ID
            output_filename: Custom output filename
            
        Returns:
            Path to generated PDF file (or HTML if PDF conversion not available)
        """
        try:
            # Get contract data
            hop_dong = self.hop_dong_service.get_by_id(ma_hop_dong)
            khach_hang = self.khach_hang_service.get_by_id(hop_dong.ma_khach_hang)
            kho = self.kho_service.get_by_id(hop_dong.ma_kho)
            
            # Get vị trí list
            vi_tri_list = []
            # Note: This assumes hop_dong has vi_tri relationship
            # Adjust based on actual data model
            
            # Calculate remaining days
            today = datetime.date.today()
            so_ngay_con_lai = (hop_dong.ngay_ket_thuc - today).days if hop_dong.ngay_ket_thuc else 0
            
            # Prepare context
            context = {
                'ma_hop_dong': hop_dong.ma_hop_dong,
                'ngay_ky': format_date(hop_dong.ngay_ky) if hop_dong.ngay_ky else "",
                'ngay_bat_dau': format_date(hop_dong.ngay_bat_dau),
                'ngay_ket_thuc': format_date(hop_dong.ngay_ket_thuc),
                'thoi_han': hop_dong.thoi_han,
                'trang_thai': hop_dong.trang_thai,
                'so_ngay_con_lai': so_ngay_con_lai,
                
                # Customer info
                'ma_khach_hang': khach_hang.ma_khach_hang,
                'ten_khach_hang': khach_hang.ten_khach_hang,
                'dia_chi_khach_hang': khach_hang.dia_chi,
                'sdt_khach_hang': khach_hang.so_dien_thoai,
                'email_khach_hang': khach_hang.email,
                
                # Warehouse info
                'ma_kho': kho.ma_kho,
                'ten_kho': kho.ten_kho,
                'dia_chi_kho': kho.dia_chi,
                'dien_tich': kho.dien_tich,
                'suc_chua': kho.suc_chua,
                
                # Position list
                'vi_tri_list': [],  # Will be populated based on actual data model
                
                # Payment info
                'tong_gia_tri': format_currency(hop_dong.gia_thue * hop_dong.thoi_han) if hop_dong.gia_thue else 0,
                'ngay_thanh_toan': format_date(hop_dong.ngay_bat_dau)
            }
            
            # Load and render template
            template = self._load_template("contract")
            html_content = self._render_template(template, context)
            
            # Generate filenames
            if not output_filename:
                timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
                output_filename = f"hop_dong_{ma_hop_dong}_{timestamp}"
            
            html_path = self._save_html(html_content, f"{output_filename}.html")
            pdf_path = str(self.output_dir / f"{output_filename}.pdf")
            
            # Convert to PDF (placeholder)
            success = self._convert_html_to_pdf(html_path, pdf_path)
            
            if success:
                return pdf_path
            else:
                print(f"PDF generation not available. HTML saved at: {html_path}")
                return html_path
                
        except Exception as e:
            print(f"Error generating contract PDF: {e}")
            raise
    
    def generate_invoice_pdf(self, ma_hoa_don: str, output_filename: Optional[str] = None) -> str:
        """
        Generate invoice PDF
        
        Args:
            ma_hoa_don: Invoice ID
            output_filename: Custom output filename
            
        Returns:
            Path to generated PDF file (or HTML if PDF conversion not available)
        """
        try:
            # Get invoice data
            # Note: This assumes ThanhToanService has get_by_id method
            hoa_don = self.thanh_toan_service.get_by_id(ma_hoa_don)
            
            # Get related data
            hop_dong = self.hop_dong_service.get_by_id(hoa_don.ma_hop_dong)
            khach_hang = self.khach_hang_service.get_by_id(hop_dong.ma_khach_hang)
            
            # Prepare service details
            chi_tiet_dich_vu = [
                {
                    'ten_dich_vu': 'Thuê kho lưu trữ',
                    'so_luong': 1,
                    'don_gia': hop_dong.gia_thue,
                    'thanh_tien': hop_dong.gia_thue
                }
            ]
            
            # Calculate totals
            tong_cong = hop_dong.gia_thue
            thue_vat = 10  # 10% VAT
            thue_vat_tien = tong_cong * thue_vat / 100
            tong_thanh_toan = tong_cong + thue_vat_tien
            
            # Prepare context
            context = {
                'ma_hoa_don': ma_hoa_don,
                'ngay_lap': format_date(hoa_don.ngay_thanh_toan),
                'han_thanh_toan': format_date(hoa_don.ngay_thanh_toan),
                'trang_thai_hoa_don': hoa_don.trang_thai,
                'ma_hop_dong': hop_dong.ma_hop_dong,
                'ky_thanh_toan': 'Tháng ' + str(hoa_don.ngay_thanh_toan.month) if hasattr(hoa_don.ngay_thanh_toan, 'month') else 'N/A',
                'so_ngay_su_dung': 30,  # Assuming monthly billing
                
                # Customer info
                'ma_khach_hang': khach_hang.ma_khach_hang,
                'ten_khach_hang': khach_hang.ten_khach_hang,
                'dia_chi_khach_hang': khach_hang.dia_chi,
                'sdt_khach_hang': khach_hang.so_dien_thoai,
                'email_khach_hang': khach_hang.email,
                
                # Company info (hardcoded for now)
                'dia_chi_cong_ty': '123 Đường ABC, Quận XYZ, TP. Hồ Chí Minh',
                'ma_so_thue_cong_ty': '0123456789',
                'sdt_cong_ty': '(028) 1234 5678',
                'email_cong_ty': 'info@kholuutru.com',
                
                # Service details
                'chi_tiet_dich_vu': chi_tiet_dich_vu,
                'tong_cong': tong_cong,
                'thue_vat': thue_vat,
                'thue_vat_tien': thue_vat_tien,
                'tong_thanh_toan': tong_thanh_toan,
                
                # Bank info (hardcoded for now)
                'ngan_hang': 'Ngân hàng TMCP ABC',
                'so_tai_khoan': '123456789012',
                'chu_tai_khoan': 'CÔNG TY TNHH QUẢN LÝ KHO LƯU TRỮ'
            }
            
            # Load and render template
            template = self._load_template("invoice")
            html_content = self._render_template(template, context)
            
            # Generate filenames
            if not output_filename:
                timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
                output_filename = f"hoa_don_{ma_hoa_don}_{timestamp}"
            
            html_path = self._save_html(html_content, f"{output_filename}.html")
            pdf_path = str(self.output_dir / f"{output_filename}.pdf")
            
            # Convert to PDF (placeholder)
            success = self._convert_html_to_pdf(html_path, pdf_path)
            
            if success:
                return pdf_path
            else:
                print(f"PDF generation not available. HTML saved at: {html_path}")
                return html_path
                
        except Exception as e:
            print(f"Error generating invoice PDF: {e}")
            raise
    
    def generate_summary_report_pdf(self, report_type: str = "monthly", output_filename: Optional[str] = None) -> str:
        """
        Generate summary report PDF
        
        Args:
            report_type: Type of report (daily, weekly, monthly, quarterly, yearly)
            output_filename: Custom output filename
            
        Returns:
            Path to generated PDF file (or HTML if PDF conversion not available)
        """
        try:
            from src.services.report_service import ReportService
            
            # Get report data
            report_service = ReportService()
            report_data = report_service.generate_summary_report()
            
            # Prepare context
            context = {
                'loai_bao_cao': report_type,
                'ngay_bat_dau': '01/01/2026',  # Placeholder
                'ngay_ket_thuc': '31/01/2026',  # Placeholder
                'ngay_sinh': datetime.datetime.now().strftime('%d/%m/%Y %H:%M'),
                'nguoi_tao': 'Hệ thống tự động',
                
                # Summary counts
                'tong_khach_hang': report_data['summary']['customers']['total'],
                'tong_kho': report_data['summary']['warehouses']['total'],
                'tong_hop_dong': report_data['summary']['contracts']['total'],
                
                # Detailed sections
                'khach_hang': {
                    'tong': report_data['summary']['customers']['total'],
                    'hoat_dong': report_data['summary']['customers']['active'],
                    'khong_hoat_dong': report_data['summary']['customers']['inactive']
                },
                'kho': {
                    'tong': report_data['summary']['warehouses']['total'],
                    'hoat_dong': report_data['summary']['warehouses']['active'],
                    'tong_dien_tich': report_data['summary']['warehouses']['total_dien_tich'],
                    'tong_suc_chua': report_data['summary']['warehouses']['total_suc_chua'],
                    'avg_fill_rate': report_data['summary']['warehouses']['avg_fill_rate']
                },
                'hop_dong': {
                    'tong': report_data['summary']['contracts']['total'],
                    'dang_hieu_luc': report_data['summary']['contracts']['by_status'].get('hieu_luc', 0),
                    'sap_het_han': report_data['summary']['contracts']['expiring_soon'],
                    'tong_doanh_thu': report_data['summary']['contracts']['total_revenue'],
                    'theo_trang_thai': report_data['summary']['contracts']['by_status']
                },
                'hang_hoa': {
                    'tong_mat_hang': report_data['summary']['goods']['total_items'],
                    'trong_kho': report_data['summary']['goods']['in_stock'],
                    'tong_gia_tri': report_data['summary']['goods']['total_value'],
                    'theo_loai': report_data['summary']['goods']['by_type']
                },
                'doanh_thu': {
                    'thang_nay': report_data['summary']['revenue']['monthly_revenue'],
                    'nam_nay': report_data['summary']['revenue']['yearly_revenue']
                },
                'canh_bao': {
                    'hang_sap_het': report_data['summary']['alerts']['low_stock_count'],
                    'canh_bao_nghiem_trong': report_data['summary']['alerts']['critical_alerts'],
                    'hop_dong_sap_het_han': report_data['summary']['alerts']['expiring_contracts'],
                    'kho_gan_day': report_data['summary']['warehouses']['avg_fill_rate'] > 85
                },
                'khuyen_nghi_list': report_data['recommendations']
            }
            
            # Load and render template
            template = self._load_template("report")
            html_content = self._render_template(template, context)
            
            # Generate filenames
            if not output_filename:
                timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
                output_filename = f"bao_cao_tong_hop_{report_type}_{timestamp}"
            
            html_path = self._save_html(html_content, f"{output_filename}.html")
            pdf_path = str(self.output_dir / f"{output_filename}.pdf")
            
            # Convert to PDF (placeholder)
            success = self._convert_html_to_pdf(html_path, pdf_path)
            
            if success:
                return pdf_path
            else:
                print(f"PDF generation not available. HTML saved at: {html_path}")
                return html_path
                
        except Exception as e:
            print(f"Error generating summary report PDF: {e}")
            raise


# Convenience functions
def generate_contract_pdf(ma_hop_dong: str, output_filename: Optional[str] = None) -> str:
    """Generate contract PDF"""
    service = PDFGenerationService()
    return service.generate_contract_pdf(ma_hop_dong, output_filename)


def generate_invoice_pdf(ma_hoa_don: str, output_filename: Optional[str] = None) -> str:
    """Generate invoice PDF"""
    service = PDFGenerationService()
    return service.generate_invoice_pdf(ma_hoa_don, output_filename)


def generate_summary_report_pdf(report_type: str = "monthly", output_filename: Optional[str] = None) -> str:
    """Generate summary report PDF"""
    service = PDFGenerationService()
    return service.generate_summary_report_pdf(report_type, output_filename)


__all__ = [
    'PDFGenerationService',
    'generate_contract_pdf',
    'generate_invoice_pdf',
    'generate_summary_report_pdf'
]