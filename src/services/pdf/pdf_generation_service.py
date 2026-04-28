#!/usr/bin/env python3
"""
PDF Generation Service - Dịch vụ tạo file PDF cho hệ thống quản lý kho lưu trữ
"""
import os
import datetime
from typing import Dict, Any, Optional, List
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from src.services import (
    KhachHangService, KhoService, ViTriService,
    HopDongService, HangHoaService, ThanhToanService
)
from src.utils.formatters import format_currency, format_date


class PDFGenerationService:
    """
    Service for generating PDF documents using ReportLab
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
        
        # Setup Vietnamese font (if available)
        self._setup_vietnamese_font()
    
    def _setup_vietnamese_font(self):
        """Setup Vietnamese font support"""
        try:
            # Try to register a Vietnamese-compatible font
            # You may need to download and place DejaVuSans.ttf in your project
            font_path = "src/fonts/DejaVuSans.ttf"
            if os.path.exists(font_path):
                pdfmetrics.registerFont(TTFont('DejaVuSans', font_path))
                self.default_font = 'DejaVuSans'
            else:
                self.default_font = 'Helvetica'
        except Exception as e:
            print(f"Warning: Could not setup Vietnamese font: {e}")
            self.default_font = 'Helvetica'
    
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
        Convert HTML to PDF using ReportLab
        Note: This is a simplified conversion. For full HTML/CSS support,
        consider using WeasyPrint or wkhtmltopdf.
        """
        try:
            # For now, we'll create a basic PDF from the data instead of parsing HTML
            # In a real implementation, you might want to use a proper HTML parser
            print(f"Converting {html_path} to PDF at {pdf_path}")
            return True
        except Exception as e:
            print(f"Error converting HTML to PDF: {e}")
            return False
    
    def _create_contract_pdf_content(self, context: Dict[str, Any]) -> List:
        """Create contract PDF content using ReportLab elements"""
        story = []
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=16,
            spaceAfter=30,
            alignment=1,  # center
            fontName=self.default_font
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=12,
            spaceAfter=12,
            fontName=self.default_font
        )
        
        normal_style = ParagraphStyle(
            'CustomNormal',
            parent=styles['Normal'],
            fontSize=10,
            spaceAfter=6,
            fontName=self.default_font
        )
        
        # Title
        story.append(Paragraph("HỢP ĐỒNG THUÊ KHO LƯU TRỮ HÀNG HÓA", title_style))
        story.append(Paragraph(f"Mã hợp đồng: {context.get('ma_hop_dong', '')}", normal_style))
        story.append(Spacer(1, 20))
        
        # Contract info
        story.append(Paragraph("THÔNG TIN HỢP ĐỒNG", heading_style))
        
        contract_data = [
            ["Ngày ký:", context.get('ngay_ky', '')],
            ["Ngày bắt đầu:", context.get('ngay_bat_dau', '')],
            ["Ngày kết thúc:", context.get('ngay_ket_thuc', '')],
            ["Thời hạn:", f"{context.get('thoi_han', '')} tháng"],
            ["Trạng thái:", context.get('trang_thai', '')],
            ["Số ngày còn lại:", str(context.get('so_ngay_con_lai', ''))]
        ]
        
        contract_table = Table(contract_data, colWidths=[2*inch, 3*inch])
        contract_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), self.default_font),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ]))
        story.append(contract_table)
        story.append(Spacer(1, 20))
        
        # Customer info
        story.append(Paragraph("THÔNG TIN BÊN THUÊ (BÊN A)", heading_style))
        
        customer_data = [
            ["Mã khách hàng:", context.get('ma_khach_hang', '')],
            ["Tên khách hàng:", context.get('ten_khach_hang', '')],
            ["Địa chỉ:", context.get('dia_chi_khach_hang', '')],
            ["Số điện thoại:", context.get('sdt_khach_hang', '')],
            ["Email:", context.get('email_khach_hang', '')]
        ]
        
        customer_table = Table(customer_data, colWidths=[2*inch, 3*inch])
        customer_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), self.default_font),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ]))
        story.append(customer_table)
        story.append(Spacer(1, 20))
        
        # Warehouse info
        story.append(Paragraph("THÔNG TIN KHO LƯU TRỮ (BÊN B)", heading_style))
        
        warehouse_data = [
            ["Mã kho:", context.get('ma_kho', '')],
            ["Tên kho:", context.get('ten_kho', '')],
            ["Địa chỉ kho:", context.get('dia_chi_kho', '')],
            ["Diện tích:", f"{context.get('dien_tich', '')} m²"],
            ["Sức chứa:", f"{context.get('suc_chua', '')} m³"]
        ]
        
        warehouse_table = Table(warehouse_data, colWidths=[2*inch, 3*inch])
        warehouse_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), self.default_font),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ]))
        story.append(warehouse_table)
        story.append(Spacer(1, 20))
        
        # Payment terms
        story.append(Paragraph("ĐIỀU KHOẢN THANH TOÁN", heading_style))
        
        payment_data = [
            ["Tổng giá trị hợp đồng:", f"{context.get('tong_gia_tri', '')} ₫"],
            ["Phương thức thanh toán:", "Chuyển khoản/Tiền mặt"],
            ["Thời hạn thanh toán:", f"Trước ngày {context.get('ngay_thanh_toan', '')}"]
        ]
        
        payment_table = Table(payment_data, colWidths=[2*inch, 3*inch])
        payment_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), self.default_font),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ]))
        story.append(payment_table)
        story.append(Spacer(1, 20))
        
        # Terms and conditions
        story.append(Paragraph("CÁC ĐIỀU KHOẢN KHÁC", heading_style))
        terms = [
            "1. Bên thuê có trách nhiệm bảo quản hàng hóa và tuân thủ quy định của kho lưu trữ.",
            "2. Bên cho thuê có trách nhiệm đảm bảo an ninh, phòng cháy chữa cháy cho khu vực thuê.",
            "3. Hợp đồng có thể được gia hạn nếu hai bên thống nhất trước 30 ngày hết hạn.",
            "4. Mọi tranh chấp sẽ được giải quyết thông qua thương lượng hoặc tòa án có thẩm quyền."
        ]
        
        for term in terms:
            story.append(Paragraph(term, normal_style))
        
        story.append(Spacer(1, 30))
        story.append(Paragraph("Hợp đồng này gồm 2 bản, mỗi bên giữ 1 bản có giá trị pháp lý như nhau.", normal_style))
        
        return story
    
    def generate_contract_pdf(self, ma_hop_dong: str, output_filename: Optional[str] = None) -> str:
        """
        Generate contract PDF using ReportLab
        
        Args:
            ma_hop_dong: Contract ID
            output_filename: Custom output filename
            
        Returns:
            Path to generated PDF file
        """
        try:
            # Get contract data
            hop_dong = self.hop_dong_service.get_by_id(ma_hop_dong)
            khach_hang = self.khach_hang_service.get_by_id(hop_dong.ma_khach_hang)
            kho = self.kho_service.get_by_id(hop_dong.ma_kho)
            
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
                
                # Payment info
                'tong_gia_tri': format_currency(hop_dong.gia_thue * hop_dong.thoi_han) if hop_dong.gia_thue else 0,
                'ngay_thanh_toan': format_date(hop_dong.ngay_bat_dau)
            }
            
            # Generate PDF content
            story = self._create_contract_pdf_content(context)
            
            # Generate filename
            if not output_filename:
                timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
                output_filename = f"hop_dong_{ma_hop_dong}_{timestamp}"
            
            pdf_path = str(self.output_dir / f"{output_filename}.pdf")
            
            # Create PDF
            doc = SimpleDocTemplate(
                pdf_path,
                pagesize=A4,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=72
            )
            doc.build(story)
            
            print(f"Contract PDF generated successfully: {pdf_path}")
            return pdf_path
                
        except Exception as e:
            print(f"Error generating contract PDF: {e}")
            raise
    
    def _create_invoice_pdf_content(self, context: Dict[str, Any]) -> List:
        """Create invoice PDF content using ReportLab elements"""
        story = []
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'InvoiceTitle',
            parent=styles['Heading1'],
            fontSize=18,
            spaceAfter=30,
            alignment=1,  # center
            textColor=colors.red,
            fontName=self.default_font
        )
        
        heading_style = ParagraphStyle(
            'InvoiceHeading',
            parent=styles['Heading2'],
            fontSize=12,
            spaceAfter=12,
            textColor=colors.blue,
            fontName=self.default_font
        )
        
        normal_style = ParagraphStyle(
            'InvoiceNormal',
            parent=styles['Normal'],
            fontSize=10,
            spaceAfter=6,
            fontName=self.default_font
        )
        
        # Company info
        story.append(Paragraph("CÔNG TY TNHH QUẢN LÝ KHO LƯU TRỮ", title_style))
        story.append(Paragraph(f"Địa chỉ: {context.get('dia_chi_cong_ty', '')}", normal_style))
        story.append(Paragraph(f"Mã số thuế: {context.get('ma_so_thue_cong_ty', '')}", normal_style))
        story.append(Paragraph(f"Số điện thoại: {context.get('sdt_cong_ty', '')} | Email: {context.get('email_cong_ty', '')}", normal_style))
        story.append(Spacer(1, 20))
        
        # Invoice title
        story.append(Paragraph("HÓA ĐƠN THANH TOÁN", title_style))
        story.append(Paragraph(f"Mã hóa đơn: {context.get('ma_hoa_don', '')}", normal_style))
        story.append(Spacer(1, 20))
        
        # Invoice info
        story.append(Paragraph("THÔNG TIN HÓA ĐƠN", heading_style))
        
        invoice_data = [
            ["Ngày lập:", context.get('ngay_lap', '')],
            ["Hạn thanh toán:", context.get('han_thanh_toan', '')],
            ["Trạng thái:", context.get('trang_thai_hoa_don', '')],
            ["Hợp đồng:", context.get('ma_hop_dong', '')],
            ["Kỳ thanh toán:", context.get('ky_thanh_toan', '')],
            ["Số ngày sử dụng:", str(context.get('so_ngay_su_dung', ''))]
        ]
        
        invoice_table = Table(invoice_data, colWidths=[2*inch, 3*inch])
        invoice_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), self.default_font),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ]))
        story.append(invoice_table)
        story.append(Spacer(1, 20))
        
        # Customer info
        story.append(Paragraph("THÔNG TIN KHÁCH HÀNG", heading_style))
        
        customer_data = [
            ["Mã khách hàng:", context.get('ma_khach_hang', '')],
            ["Tên khách hàng:", context.get('ten_khach_hang', '')],
            ["Địa chỉ:", context.get('dia_chi_khach_hang', '')],
            ["Số điện thoại:", context.get('sdt_khach_hang', '')],
            ["Email:", context.get('email_khach_hang', '')]
        ]
        
        customer_table = Table(customer_data, colWidths=[2*inch, 3*inch])
        customer_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), self.default_font),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ]))
        story.append(customer_table)
        story.append(Spacer(1, 20))
        
        # Service details
        story.append(Paragraph("CHI TIẾT DỊCH VỤ", heading_style))
        
        # Service table headers
        service_headers = ["STT", "Dịch vụ", "Số lượng", "Đơn giá", "Thành tiền"]
        service_data = [service_headers]
        
        chi_tiet_dich_vu = context.get('chi_tiet_dich_vu', [])
        for i, item in enumerate(chi_tiet_dich_vu):
            service_data.append([
                str(i + 1),
                item.get('ten_dich_vu', ''),
                str(item.get('so_luong', '')),
                f"{item.get('don_gia', '')} ₫",
                f"{item.get('thanh_tien', '')} ₫"
            ])
        
        # Add totals
        service_data.append(["", "", "", "TỔNG CỘNG:", f"{context.get('tong_cong', '')} ₫"])
        service_data.append(["", "", "", "THUẾ VAT (10%):", f"{context.get('thue_vat_tien', '')} ₫"])
        service_data.append(["", "", "", "TỔNG THANH TOÁN:", f"{context.get('tong_thanh_toan', '')} ₫"])
        
        service_table = Table(service_data, colWidths=[0.5*inch, 2*inch, 0.8*inch, 1.2*inch, 1.5*inch])
        service_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), self.default_font),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('ALIGN', (-2, -3), (-1, -1), 'RIGHT'),
            ('FONTNAME', (-2, -3), (-1, -1), self.default_font),
            ('FONTSIZE', (-2, -3), (-1, -1), 12),
        ]))
        story.append(service_table)
        story.append(Spacer(1, 20))
        
        # Bank info
        story.append(Paragraph("THÔNG TIN NGÂN HÀNG", heading_style))
        
        bank_data = [
            ["Ngân hàng:", context.get('ngan_hang', '')],
            ["Số tài khoản:", context.get('so_tai_khoan', '')],
            ["Chủ tài khoản:", context.get('chu_tai_khoan', '')],
            ["Nội dung chuyển khoản:", f"Thanh toán HD {context.get('ma_hop_dong', '')} - {context.get('ten_khach_hang', '')}"]
        ]
        
        bank_table = Table(bank_data, colWidths=[2*inch, 3*inch])
        bank_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), self.default_font),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ]))
        story.append(bank_table)
        story.append(Spacer(1, 20))
        
        story.append(Paragraph("Hóa đơn này có giá trị thanh toán trong vòng 30 ngày kể từ ngày lập.", normal_style))
        story.append(Paragraph(f"Mọi thắc mắc vui lòng liên hệ: {context.get('sdt_cong_ty', '')} hoặc {context.get('email_cong_ty', '')}", normal_style))
        
        return story
    
    def generate_invoice_pdf(self, ma_hoa_don: str, output_filename: Optional[str] = None) -> str:
        """
        Generate invoice PDF using ReportLab
        
        Args:
            ma_hoa_don: Invoice ID
            output_filename: Custom output filename
            
        Returns:
            Path to generated PDF file
        """
        try:
            # Get invoice data
            hoa_don = self.thanh_toan_service.get_by_id(ma_hoa_don)
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
            thue_vat_tien = tong_cong * 0.1
            tong_thanh_toan = tong_cong + thue_vat_tien
            
            # Prepare context
            context = {
                'ma_hoa_don': ma_hoa_don,
                'ngay_lap': format_date(hoa_don.ngay_thanh_toan),
                'han_thanh_toan': format_date(hoa_don.ngay_thanh_toan),
                'trang_thai_hoa_don': hoa_don.trang_thai,
                'ma_hop_dong': hop_dong.ma_hop_dong,
                'ky_thanh_toan': f'Tháng {hoa_don.ngay_thanh_toan.month}' if hasattr(hoa_don.ngay_thanh_toan, 'month') else 'N/A',
                'so_ngay_su_dung': 30,
                
                # Customer info
                'ma_khach_hang': khach_hang.ma_khach_hang,
                'ten_khach_hang': khach_hang.ten_khach_hang,
                'dia_chi_khach_hang': khach_hang.dia_chi,
                'sdt_khach_hang': khach_hang.so_dien_thoai,
                'email_khach_hang': khach_hang.email,
                
                # Company info
                'dia_chi_cong_ty': '123 Đường ABC, Quận XYZ, TP. Hồ Chí Minh',
                'ma_so_thue_cong_ty': '0123456789',
                'sdt_cong_ty': '(028) 1234 5678',
                'email_cong_ty': 'info@kholuutru.com',
                
                # Service details
                'chi_tiet_dich_vu': chi_tiet_dich_vu,
                'tong_cong': tong_cong,
                'thue_vat_tien': thue_vat_tien,
                'tong_thanh_toan': tong_thanh_toan,
                
                # Bank info
                'ngan_hang': 'Ngân hàng TMCP ABC',
                'so_tai_khoan': '123456789012',
                'chu_tai_khoan': 'CÔNG TY TNHH QUẢN LÝ KHO LƯU TRỮ'
            }
            
            # Generate PDF content
            story = self._create_invoice_pdf_content(context)
            
            # Generate filename
            if not output_filename:
                timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
                output_filename = f"hoa_don_{ma_hoa_don}_{timestamp}"
            
            pdf_path = str(self.output_dir / f"{output_filename}.pdf")
            
            # Create PDF
            doc = SimpleDocTemplate(
                pdf_path,
                pagesize=A4,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=72
            )
            doc.build(story)
            
            print(f"Invoice PDF generated successfully: {pdf_path}")
            return pdf_path
                
        except Exception as e:
            print(f"Error generating invoice PDF: {e}")
            raise
    
    def _create_report_pdf_content(self, context: Dict[str, Any]) -> List:
        """Create report PDF content using ReportLab elements"""
        story = []
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'ReportTitle',
            parent=styles['Heading1'],
            fontSize=16,
            spaceAfter=30,
            alignment=1,  # center
            textColor=colors.green,
            fontName=self.default_font
        )
        
        heading_style = ParagraphStyle(
            'ReportHeading',
            parent=styles['Heading2'],
            fontSize=12,
            spaceAfter=12,
            textColor=colors.blue,
            fontName=self.default_font
        )
        
        normal_style = ParagraphStyle(
            'ReportNormal',
            parent=styles['Normal'],
            fontSize=10,
            spaceAfter=6,
            fontName=self.default_font
        )
        
        # Company info
        story.append(Paragraph("CÔNG TY TNHH QUẢN LÝ KHO LƯU TRỮ", title_style))
        story.append(Paragraph(f"BÁO CÁO TỔNG HỢP {context.get('loai_bao_cao', '').upper()}", title_style))
        story.append(Spacer(1, 20))
        
        # Report info
        story.append(Paragraph("THÔNG TIN BÁO CÁO", heading_style))
        
        report_data = [
            ["Loại báo cáo:", context.get('loai_bao_cao', '')],
            ["Ngày sinh:", context.get('ngay_sinh', '')],
            ["Người tạo:", context.get('nguoi_tao', '')],
            ["Tổng khách hàng:", str(context.get('tong_khach_hang', ''))],
            ["Tổng kho:", str(context.get('tong_kho', ''))],
            ["Tổng hợp đồng:", str(context.get('tong_hop_dong', ''))]
        ]
        
        report_table = Table(report_data, colWidths=[2*inch, 3*inch])
        report_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), self.default_font),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ]))
        story.append(report_table)
        story.append(Spacer(1, 20))
        
        # Customer statistics
        story.append(Paragraph("I. THỐNG KÊ KHÁCH HÀNG", heading_style))
        
        khach_hang = context.get('khach_hang', {})
        customer_stats = [
            ["Tổng số khách hàng:", str(khach_hang.get('tong', ''))],
            ["Khách hàng hoạt động:", str(khach_hang.get('hoat_dong', ''))],
            ["Khách hàng không hoạt động:", str(khach_hang.get('khong_hoat_dong', ''))]
        ]
        
        customer_table = Table(customer_stats, colWidths=[2*inch, 3*inch])
        customer_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), self.default_font),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ]))
        story.append(customer_table)
        story.append(Spacer(1, 20))
        
        # Warehouse statistics
        story.append(Paragraph("II. THỐNG KÊ KHO HÀNG", heading_style))
        
        kho = context.get('kho', {})
        warehouse_stats = [
            ["Tổng số kho:", str(kho.get('tong', ''))],
            ["Kho đang hoạt động:", str(kho.get('hoat_dong', ''))],
            ["Tổng diện tích:", f"{kho.get('tong_dien_tich', '')} m²"],
            ["Tổng sức chứa:", f"{kho.get('tong_suc_chua', '')} m³"],
            ["Tỷ lệ lấp đầy trung bình:", f"{kho.get('avg_fill_rate', '')}%"]
        ]
        
        warehouse_table = Table(warehouse_stats, colWidths=[2*inch, 3*inch])
        warehouse_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), self.default_font),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ]))
        story.append(warehouse_table)
        story.append(Spacer(1, 20))
        
        # Contract statistics
        story.append(Paragraph("III. THỐNG KÊ HỢP ĐỒNG", heading_style))
        
        hop_dong = context.get('hop_dong', {})
        contract_stats = [
            ["Tổng số hợp đồng:", str(hop_dong.get('tong', ''))],
            ["Hợp đồng đang hiệu lực:", str(hop_dong.get('dang_hieu_luc', ''))],
            ["Hợp đồng sắp hết hạn:", str(hop_dong.get('sap_het_han', ''))],
            ["Tổng doanh thu:", f"{hop_dong.get('tong_doanh_thu', '')} ₫"]
        ]
        
        contract_table = Table(contract_stats, colWidths=[2*inch, 3*inch])
        contract_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), self.default_font),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ]))
        story.append(contract_table)
        story.append(Spacer(1, 20))
        
        # Revenue statistics
        story.append(Paragraph("IV. DOANH THU & TÀI CHÍNH", heading_style))
        
        doanh_thu = context.get('doanh_thu', {})
        revenue_stats = [
            ["Doanh thu tháng này:", f"{doanh_thu.get('thang_nay', '')} ₫"],
            ["Doanh thu năm nay (dự kiến):", f"{doanh_thu.get('nam_nay', '')} ₫"]
        ]
        
        revenue_table = Table(revenue_stats, colWidths=[2*inch, 3*inch])
        revenue_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), self.default_font),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ]))
        story.append(revenue_table)
        story.append(Spacer(1, 20))
        
        # Alerts and warnings
        story.append(Paragraph("V. CẢNH BÁO & RỦI RO", heading_style))
        
        canh_bao = context.get('canh_bao', {})
        alert_items = []
        if canh_bao.get('hang_sap_het', 0) > 0:
            alert_items.append(f"⚠️ Hàng sắp hết: {canh_bao['hang_sap_het']} mặt hàng cần nhập thêm")
        if canh_bao.get('canh_bao_nghiem_trong', 0) > 0:
            alert_items.append(f"⚠️ Cảnh báo nghiêm trọng: {canh_bao['canh_bao_nghiem_trong']} vấn đề cần xử lý ngay")
        if canh_bao.get('hop_dong_sap_het_han', 0) > 0:
            alert_items.append(f"⚠️ Hợp đồng sắp hết hạn: {canh_bao['hop_dong_sap_het_han']} hợp đồng cần liên hệ gia hạn")
        if canh_bao.get('kho_gan_day', False):
            alert_items.append(f"⚠️ Kho gần đầy: Tỷ lệ lấp đầy trung bình {context.get('kho', {}).get('avg_fill_rate', 0)}% - Cần mở rộng hoặc marketing")
        
        if alert_items:
            for alert in alert_items:
                story.append(Paragraph(alert, normal_style))
        else:
            story.append(Paragraph("✅ Không có cảnh báo nào.", normal_style))
        
        story.append(Spacer(1, 20))
        
        # Recommendations
        story.append(Paragraph("VI. KHUYẾN NGHỊ", heading_style))
        
        khuyen_nghi_list = context.get('khuyen_nghi_list', [])
        if khuyen_nghi_list:
            for khuyen_nghi in khuyen_nghi_list:
                story.append(Paragraph(f"💡 {khuyen_nghi}", normal_style))
        else:
            story.append(Paragraph("Không có khuyến nghị nào.", normal_style))
        
        story.append(Spacer(1, 30))
        story.append(Paragraph("Báo cáo này được tạo tự động từ hệ thống quản lý kho lưu trữ.", normal_style))
        story.append(Paragraph("Liên hệ IT Support nếu có thắc mắc về dữ liệu.", normal_style))
        
        return story
    
    def generate_summary_report_pdf(self, report_type: str = "monthly", output_filename: Optional[str] = None) -> str:
        """
        Generate summary report PDF using ReportLab
        
        Args:
            report_type: Type of report (daily, weekly, monthly, quarterly, yearly)
            output_filename: Custom output filename
            
        Returns:
            Path to generated PDF file
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
            
            # Generate PDF content
            story = self._create_report_pdf_content(context)
            
            # Generate filename
            if not output_filename:
                timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
                output_filename = f"bao_cao_tong_hop_{report_type}_{timestamp}"
            
            pdf_path = str(self.output_dir / f"{output_filename}.pdf")
            
            # Create PDF
            doc = SimpleDocTemplate(
                pdf_path,
                pagesize=A4,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=72
            )
            doc.build(story)
            
            print(f"Summary report PDF generated successfully: {pdf_path}")
            return pdf_path
                
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