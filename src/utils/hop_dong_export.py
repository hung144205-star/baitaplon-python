#!/usr/bin/env python3
"""
Export Service - Export hợp đồng sang PDF
"""
from datetime import datetime
from typing import Optional
import io


def export_hop_dong_to_pdf(hop_dong, khach_hang=None, vi_tri=None, output_path: Optional[str] = None) -> str:
    """
    Export contract to PDF
    
    Note: This is a placeholder. Actual PDF generation requires:
    - reportlab or weasyprint library
    - Font support for Vietnamese
    
    For now, we'll create a text-based export
    """
    from src.utils.formatters import format_currency
    
    # Generate filename
    if output_path is None:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_path = f"data/exports/hop_dong_{hop_dong.ma_hop_dong}_{timestamp}.txt"
    
    # Create content
    content = f"""
================================================================================
                    CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
                    Độc lập - Tự do - Hạnh phúc
================================================================================

                        HỢP ĐỒNG THUÊ KHO
                        Số: {hop_dong.ma_hop_dong}
================================================================================

I. THÔNG TIN CÁC BÊN

BÊN CHO THUÊ (BÊN A):
  Tên công ty: [Your Company Name]
  Địa chỉ: [Your Address]
  Điện thoại: [Your Phone]
  Email: [Your Email]

BÊN THUÊ (BÊN B):
  Mã khách hàng: {hop_dong.ma_khach_hang}
  Tên: {khach_hang.ho_ten if khach_hang else '[Name]'}
  Địa chỉ: {khach_hang.dia_chi if khach_hang else '[Address]'}
  Điện thoại: {khach_hang.dien_thoai if khach_hang else '[Phone]'}

II. THÔNG TIN VỊ TRÍ CHO THUÊ

  Mã vị trí: {hop_dong.ma_vi_tri}
  Địa chỉ: {vi_tri.khu_vuc if vi_tri else '[Area]'} - Hàng {vi_tri.hang if vi_tri else '[Row]'} - Tầng {vi_tri.tang if vi_tri else '[Floor]'}
  Diện tích: {vi_tri.dien_tich if vi_tri else 0:,.0f} m²
  Sức chứa: {vi_tri.chieu_cao if vi_tri else 0:,.1f} m³

III. THỜI HẠN HỢP ĐỒNG

  Ngày bắt đầu: {hop_dong.ngay_bat_dau.strftime('%d/%m/%Y')}
  Ngày kết thúc: {hop_dong.ngay_ket_thuc.strftime('%d/%m/%Y')}
  Tổng thời gian: [Calculate months]

IV. GIÁ THUÊ VÀ PHƯƠNG THỨC THANH TOÁN

  Giá thuê: {format_currency(hop_dong.gia_thue)}/tháng
  Tiền cọc: {format_currency(hop_dong.tien_coc)}
  Phương thức thanh toán: {hop_dong.phuong_thuc_thanh_toan}
  
  Tổng tiền thuê ước tính: {format_currency(calculate_total_rent(hop_dong))}

V. ĐIỀU KHOẢN ĐẶC BIỆT

{hop_dong.dieu_khoan if hop_dong.dieu_khoan else 'Không có điều khoản đặc biệt'}

VI. CHỮ KÝ

BÊN A                                      BÊN B
(Ký, ghi rõ họ tên, đóng dấu)             (Ký, ghi rõ họ tên)



================================================================================
Ngày {datetime.now().strftime('%d')} tháng {datetime.now().strftime('%m')} năm {datetime.now().strftime('%Y')}
================================================================================
"""
    
    # Write to file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return output_path


def calculate_total_rent(hop_dong) -> float:
    """Calculate total rent for contract duration"""
    from dateutil.relativedelta import relativedelta
    
    delta = relativedelta(hop_dong.ngay_ket_thuc, hop_dong.ngay_bat_dau)
    months = delta.years * 12 + delta.months
    return months * hop_dong.gia_thue


def generate_hop_dong_preview(hop_dong, khach_hang=None, vi_tri=None) -> str:
    """Generate HTML preview of contract"""
    from src.utils.formatters import format_currency
    
    html = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; }}
            h1 {{ color: #1976d2; text-align: center; }}
            h2 {{ color: #31302e; border-bottom: 2px solid #1976d2; padding-bottom: 5px; }}
            .info {{ background-color: #f6f5f4; padding: 15px; border-radius: 8px; margin: 10px 0; }}
            .highlight {{ background-color: #e3f2fd; padding: 10px; border-left: 4px solid #1976d2; }}
            table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
            th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
            th {{ background-color: #1976d2; color: white; }}
            .footer {{ text-align: center; margin-top: 40px; color: #757575; }}
        </style>
    </head>
    <body>
        <h1>📋 HỢP ĐỒNG THUÊ KHO</h1>
        <p style="text-align: center; font-size: 18px;"><b>Số: {hop_dong.ma_hop_dong}</b></p>
        
        <h2>📄 Thông tin hợp đồng</h2>
        <table>
            <tr><th>Trạng thái</th><td>{hop_dong.trang_thai.value}</td></tr>
            <tr><th>Ngày bắt đầu</th><td>{hop_dong.ngay_bat_dau.strftime('%d/%m/%Y')}</td></tr>
            <tr><th>Ngày kết thúc</th><td>{hop_dong.ngay_ket_thuc.strftime('%d/%m/%Y')}</td></tr>
        </table>
        
        <h2>👤 Khách hàng</h2>
        <div class="info">
            <p><b>Mã:</b> {hop_dong.ma_khach_hang}</p>
            <p><b>Tên:</b> {khach_hang.ho_ten if khach_hang else 'N/A'}</p>
        </div>
        
        <h2>📍 Vị trí</h2>
        <div class="info">
            <p><b>Mã:</b> {hop_dong.ma_vi_tri}</p>
            <p><b>Vị trí:</b> {vi_tri.khu_vuc if vi_tri else 'N/A'} - Hàng {vi_tri.hang if vi_tri else 'N/A'} - Tầng {vi_tri.tang if vi_tri else 'N/A'}</p>
            <p><b>Diện tích:</b> {vi_tri.dien_tich if vi_tri else 0:,.0f} m²</p>
        </div>
        
        <h2>💰 Thông tin tài chính</h2>
        <table>
            <tr><th>Giá thuê</th><td>{format_currency(hop_dong.gia_thue)}/tháng</td></tr>
            <tr><th>Tiền cọc</th><td>{format_currency(hop_dong.tien_coc)}</td></tr>
            <tr><th>Phương thức TT</th><td>{hop_dong.phuong_thuc_thanh_toan}</td></tr>
            <tr><th>Tổng tiền thuê</th><td><b>{format_currency(calculate_total_rent(hop_dong))}</b></td></tr>
        </table>
        
        <h2>📝 Điều khoản</h2>
        <div class="highlight">
            {hop_dong.dieu_khoan if hop_dong.dieu_khoan else 'Không có điều khoản đặc biệt'}
        </div>
        
        <div class="footer">
            <p>Generated on {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>
        </div>
    </body>
    </html>
    """
    
    return html


__all__ = [
    'export_hop_dong_to_pdf',
    'generate_hop_dong_preview',
    'calculate_total_rent',
]
