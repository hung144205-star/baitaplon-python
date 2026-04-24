#!/usr/bin/env python3
"""
Export Service - Export data to Excel
"""
from typing import List, Dict, Any, Optional
from pathlib import Path
from datetime import datetime


class ExcelExporter:
    """
    Export data to Excel format
    """
    
    @staticmethod
    def export_kho_to_excel(khos: List[Dict[str, Any]], output_path: str) -> str:
        """
        Export warehouse list to Excel
        
        Args:
            kho: List of warehouse dicts
            output_path: Path to save Excel file
            
        Returns:
            Path to saved file
        """
        try:
            import pandas as pd
        except ImportError:
            raise ImportError("pandas is required for Excel export. Install with: pip install pandas openpyxl")
        
        # Prepare data
        data = []
        for kho in khos:
            row = {
                'Mã Kho': kho.get('ma_kho', ''),
                'Tên Kho': kho.get('ten_kho', ''),
                'Địa Chỉ': kho.get('dia_chi', ''),
                'Diện Tích (m²)': kho.get('dien_tich', 0),
                'Sức Chứa (m³)': kho.get('suc_chua', 0),
                'Trạng Thái': kho.get('trang_thai_label', ''),
                'Ghi Chú': kho.get('ghi_chu', ''),
            }
            data.append(row)
        
        # Create DataFrame
        df = pd.DataFrame(data)
        
        # Save to Excel
        df.to_excel(output_path, index=False, engine='openpyxl')
        
        return output_path
    
    @staticmethod
    def export_vi_tri_to_excel(vi_tris: List[Dict[str, Any]], output_path: str) -> str:
        """
        Export position list to Excel
        
        Args:
            vi_tris: List of position dicts
            output_path: Path to save Excel file
            
        Returns:
            Path to saved file
        """
        try:
            import pandas as pd
        except ImportError:
            raise ImportError("pandas is required for Excel export. Install with: pip install pandas openpyxl")
        
        # Prepare data
        data = []
        for vt in vi_tris:
            row = {
                'Mã Vị Trí': vt.get('ma_vi_tri', ''),
                'Mã Kho': vt.get('ma_kho', ''),
                'Khu Vực': vt.get('khu_vuc', ''),
                'Hàng': vt.get('hang', ''),
                'Tầng': vt.get('tang', 0),
                'Diện Tích (m²)': vt.get('dien_tich', 0),
                'Chiều Cao (m)': vt.get('chieu_cao', 0),
                'Giá Thuê (₫/tháng)': vt.get('gia_thue', 0),
                'Trạng Thái': vt.get('trang_thai_label', ''),
            }
            data.append(row)
        
        # Create DataFrame
        df = pd.DataFrame(data)
        
        # Save to Excel
        df.to_excel(output_path, index=False, engine='openpyxl')
        
        return output_path
    
    @staticmethod
    def export_dashboard_to_excel(
        khos: List[Dict[str, Any]],
        vi_tris: List[Dict[str, Any]],
        output_path: str
    ) -> str:
        """
        Export dashboard data to Excel with multiple sheets
        
        Args:
            khos: List of warehouse dicts
            vi_tris: List of position dicts
            output_path: Path to save Excel file
            
        Returns:
            Path to saved file
        """
        try:
            import pandas as pd
        except ImportError:
            raise ImportError("pandas is required for Excel export. Install with: pip install pandas openpyxl")
        
        # Create Excel writer with multiple sheets
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            # Sheet 1: Kho
            kho_data = []
            for kho in khos:
                row = {
                    'Mã Kho': kho.get('ma_kho', ''),
                    'Tên Kho': kho.get('ten_kho', ''),
                    'Địa Chỉ': kho.get('dia_chi', ''),
                    'Diện Tích (m²)': kho.get('dien_tich', 0),
                    'Sức Chứa (m³)': kho.get('suc_chua', 0),
                    'Trạng Thái': kho.get('trang_thai_label', ''),
                }
                kho_data.append(row)
            
            df_kho = pd.DataFrame(kho_data)
            df_kho.to_excel(writer, sheet_name='Kho', index=False)
            
            # Sheet 2: Vị Trí
            vt_data = []
            for vt in vi_tris:
                row = {
                    'Mã Vị Trí': vt.get('ma_vi_tri', ''),
                    'Mã Kho': vt.get('ma_kho', ''),
                    'Khu Vực': vt.get('khu_vuc', ''),
                    'Hàng': vt.get('hang', ''),
                    'Tầng': vt.get('tang', 0),
                    'Diện Tích (m²)': vt.get('dien_tich', 0),
                    'Chiều Cao (m)': vt.get('chieu_cao', 0),
                    'Giá Thuê (₫/tháng)': vt.get('gia_thue', 0),
                    'Trạng Thái': vt.get('trang_thai_label', ''),
                }
                vt_data.append(row)
            
            df_vt = pd.DataFrame(vt_data)
            df_vt.to_excel(writer, sheet_name='ViTri', index=False)
            
            # Sheet 3: Summary
            summary_data = {
                'Metric': ['Tổng số kho', 'Tổng vị trí', 'Vị trí trống', 'Vị trí đã thuê', 'Tỷ lệ lấp đầy'],
                'Value': [
                    len(khos),
                    len(vi_tris),
                    sum(1 for v in vi_tris if v.get('trang_thai') == 'trong'),
                    sum(1 for v in vi_tris if v.get('trang_thai') == 'da_thue'),
                    f"{(sum(1 for v in vi_tris if v.get('trang_thai') == 'da_thue') / len(vi_tris) * 100) if vi_tris else 0:.1f}%"
                ]
            }
            df_summary = pd.DataFrame(summary_data)
            df_summary.to_excel(writer, sheet_name='Summary', index=False)
        
        return output_path


# Convenience functions
def export_kho_to_excel(khos: List[Dict[str, Any]], output_path: Optional[str] = None) -> str:
    """Export warehouse list to Excel"""
    if output_path is None:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_path = f"data/exports/kho_export_{timestamp}.xlsx"
    
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    return ExcelExporter.export_kho_to_excel(khos, output_path)


def export_vi_tri_to_excel(vi_tris: List[Dict[str, Any]], output_path: Optional[str] = None) -> str:
    """Export position list to Excel"""
    if output_path is None:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_path = f"data/exports/vi_tri_export_{timestamp}.xlsx"
    
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    return ExcelExporter.export_vi_tri_to_excel(vi_tris, output_path)


def export_dashboard_to_excel(
    khos: List[Dict[str, Any]],
    vi_tris: List[Dict[str, Any]],
    output_path: Optional[str] = None
) -> str:
    """Export dashboard data to Excel"""
    if output_path is None:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_path = f"data/exports/dashboard_export_{timestamp}.xlsx"
    
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    return ExcelExporter.export_dashboard_to_excel(khos, vi_tris, output_path)


__all__ = [
    'ExcelExporter',
    'export_kho_to_excel',
    'export_vi_tri_to_excel',
    'export_dashboard_to_excel',
]
