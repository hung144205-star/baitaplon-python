#!/usr/bin/env python3
"""
Hàng hóa Service - Business logic for goods management (Phase 6 Enhanced)
"""
from datetime import datetime
from typing import List, Optional, Dict, Any

from src.models import HangHoa, HopDong
from src.database import SessionLocal


class HangHoaService:
    """
    Service layer for HangHoa (Goods) management
    Enhanced version for Phase 6 with import/export features
    """
    
    def __init__(self):
        self.db = SessionLocal()
    
    def __del__(self):
        if hasattr(self, 'db') and self.db:
            self.db.close()
    
    # ==================== CRUD Operations ====================
    
    def create(self, data: Dict[str, Any]) -> HangHoa:
        """
        Create new goods
        
        Args:
            data: Dict with goods data
            
        Returns:
            Created HangHoa object
            
        Raises:
            ValueError: If validation fails
        """
        # Validate required fields
        required_fields = ['ma_hop_dong', 'ten_hang', 'loai_hang', 'so_luong', 'don_vi']
        for field in required_fields:
            if field not in data or not data[field]:
                raise ValueError(f"Thiếu trường bắt buộc: {field}")
        
        # Validate contract exists
        hop_dong = self.db.query(HopDong).filter(
            HopDong.ma_hop_dong == data['ma_hop_dong']
        ).first()
        if not hop_dong:
            raise ValueError("Không tìm thấy hợp đồng")
        
        # Validate quantity
        if data['so_luong'] <= 0:
            raise ValueError("Số lượng phải lớn hơn 0")
        
        # Auto-generate ID
        ma_hang_hoa = self._auto_generate_ma_hang_hoa(data['ma_hop_dong'])
        
        # Create goods
        hang_hoa = HangHoa(
            ma_hang_hoa=ma_hang_hoa,
            ma_hop_dong=data['ma_hop_dong'],
            ten_hang=data['ten_hang'],
            loai_hang=data['loai_hang'],
            so_luong=data['so_luong'],
            don_vi=data['don_vi'],
            trong_luong=data.get('trong_luong'),
            kich_thuoc=data.get('kich_thuoc'),
            gia_tri=data.get('gia_tri', 0),
            ngay_nhap=data.get('ngay_nhap', datetime.now()),
            trang_thai=data.get('trang_thai', 'trong_kho'),
            vi_tri_luu_tru=data.get('vi_tri_luu_tru'),
            ghi_chu=data.get('ghi_chu', ''),
            hinh_anh=data.get('hinh_anh', '[]')
        )
        
        self.db.add(hang_hoa)
        self.db.commit()
        self.db.refresh(hang_hoa)
        
        return hang_hoa
    
    def get_by_id(self, ma_hang_hoa: str) -> Optional[HangHoa]:
        """
        Get goods by ID
        
        Args:
            ma_hang_hoa: Goods ID
            
        Returns:
            HangHoa object or None
        """
        hang_hoa = self.db.query(HangHoa).filter(
            HangHoa.ma_hang_hoa == ma_hang_hoa
        ).first()
        
        if hang_hoa:
            self.db.refresh(hang_hoa)
        
        return hang_hoa
    
    def get_by_hop_dong(self, ma_hop_dong: str) -> List[HangHoa]:
        """
        Get all goods by contract
        
        Args:
            ma_hop_dong: Contract ID
            
        Returns:
            List of HangHoa objects
        """
        hang_hoas = self.db.query(HangHoa).filter(
            HangHoa.ma_hop_dong == ma_hop_dong
        ).all()
        
        for hh in hang_hoas:
            self.db.refresh(hh)
        
        return hang_hoas
    
    def get_all(self, skip: int = 0, limit: int = 100,
                trang_thai: Optional[str] = None,
                loai_hang: Optional[str] = None) -> List[HangHoa]:
        """
        Get all goods with filters
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records
            trang_thai: Filter by status
            loai_hang: Filter by type
            
        Returns:
            List of HangHoa objects
        """
        query = self.db.query(HangHoa)
        
        if trang_thai:
            query = query.filter(HangHoa.trang_thai == trang_thai)
        
        if loai_hang:
            query = query.filter(HangHoa.loai_hang == loai_hang)
        
        goods = query.offset(skip).limit(limit).all()
        
        for hh in goods:
            self.db.refresh(hh)
        
        return goods
    
    def get_inventory(self, ma_hop_dong: Optional[str] = None) -> List[HangHoa]:
        """
        Get current inventory
        
        Args:
            ma_hop_dong: Optional contract filter
            
        Returns:
            List of goods in warehouse
        """
        query = self.db.query(HangHoa).filter(
            HangHoa.trang_thai == 'trong_kho'
        )
        
        if ma_hop_dong:
            query = query.filter(HangHoa.ma_hop_dong == ma_hop_dong)
        
        goods = query.all()
        
        for hh in goods:
            self.db.refresh(hh)
        
        return goods
    
    def update(self, ma_hang_hoa: str, data: Dict[str, Any]) -> HangHoa:
        """
        Update goods
        
        Args:
            ma_hang_hoa: Goods ID
            data: Dict with updated data
            
        Returns:
            Updated HangHoa object
            
        Raises:
            ValueError: If goods not found or validation fails
        """
        hang_hoa = self.db.query(HangHoa).filter(
            HangHoa.ma_hang_hoa == ma_hang_hoa
        ).first()
        if not hang_hoa:
            raise ValueError("Không tìm thấy hàng hóa")
        
        # Update fields
        if 'ten_hang' in data:
            hang_hoa.ten_hang = data['ten_hang']
        if 'loai_hang' in data:
            hang_hoa.loai_hang = data['loai_hang']
        if 'so_luong' in data:
            if data['so_luong'] < 0:
                raise ValueError("Số lượng không được âm")
            hang_hoa.so_luong = data['so_luong']
        if 'don_vi' in data:
            hang_hoa.don_vi = data['don_vi']
        if 'trong_luong' in data:
            hang_hoa.trong_luong = data['trong_luong']
        if 'kich_thuoc' in data:
            hang_hoa.kich_thuoc = data['kich_thuoc']
        if 'gia_tri' in data:
            hang_hoa.gia_tri = data['gia_tri']
        if 'trang_thai' in data:
            hang_hoa.trang_thai = data['trang_thai']
        if 'vi_tri_luu_tru' in data:
            hang_hoa.vi_tri_luu_tru = data['vi_tri_luu_tru']
        if 'ghi_chu' in data:
            hang_hoa.ghi_chu = data['ghi_chu']
        if 'hinh_anh' in data:
            hang_hoa.hinh_anh = data['hinh_anh']
        
        self.db.commit()
        self.db.refresh(hang_hoa)
        
        return hang_hoa
    
    def delete(self, ma_hang_hoa: str) -> bool:
        """
        Delete goods
        
        Args:
            ma_hang_hoa: Goods ID
            
        Returns:
            True if deleted, False otherwise
        """
        hang_hoa = self.db.query(HangHoa).filter(
            HangHoa.ma_hang_hoa == ma_hang_hoa
        ).first()
        if not hang_hoa:
            return False
        
        self.db.delete(hang_hoa)
        self.db.commit()
        return True
    
    # ==================== Import/Export Operations ====================
    
    def import_goods(self, data: Dict[str, Any]) -> HangHoa:
        """
        Import goods (nhập kho)
        
        Args:
            data: Dict with import data
            
        Returns:
            Created HangHoa object
        """
        # Set import-specific fields
        data['ngay_nhap'] = datetime.now()
        data['trang_thai'] = 'trong_kho'
        data['ngay_xuat'] = None
        
        # Check if goods already exists for this contract
        existing = self.db.query(HangHoa).filter(
            HangHoa.ma_hop_dong == data['ma_hop_dong'],
            HangHoa.ten_hang == data['ten_hang'],
            HangHoa.loai_hang == data['loai_hang']
        ).first()
        
        if existing:
            # Update existing goods quantity
            new_quantity = existing.so_luong + data['so_luong']
            return self.update(existing.ma_hang_hoa, {
                'so_luong': new_quantity,
                'ngay_nhap': data['ngay_nhap']
            })
        else:
            # Create new goods
            return self.create(data)
    
    def export_goods(self, ma_hang_hoa: str, so_luong: int, data: Dict[str, Any] = None) -> bool:
        """
        Export goods (xuất kho)
        
        Args:
            ma_hang_hoa: Goods ID
            so_luong: Quantity to export
            data: Optional export data
            
        Returns:
            True if exported, False otherwise
            
        Raises:
            ValueError: If insufficient quantity
        """
        hang_hoa = self.get_by_id(ma_hang_hoa)
        if not hang_hoa:
            raise ValueError("Không tìm thấy hàng hóa")
        
        if so_luong <= 0:
            raise ValueError("Số lượng xuất phải lớn hơn 0")
        
        if hang_hoa.so_luong < so_luong:
            raise ValueError(f"Số lượng không đủ. Hiện có: {hang_hoa.so_luong} {hang_hoa.don_vi}")
        
        # Update quantity
        new_quantity = hang_hoa.so_luong - so_luong
        
        update_data = {
            'so_luong': new_quantity
        }
        
        # If all goods exported, mark as exported
        if new_quantity == 0:
            update_data['trang_thai'] = 'da_xuat'
            update_data['ngay_xuat'] = datetime.now()
        
        if data:
            if 'ghi_chu' in data:
                update_data['ghi_chu'] = data['ghi_chu']
        
        self.update(ma_hang_hoa, update_data)
        return True
    
    # ==================== Query Methods ====================
    
    def get_by_type(self, loai_hang: str, limit: int = 100) -> List[HangHoa]:
        """
        Get goods by type
        
        Args:
            loai_hang: Goods type
            limit: Maximum results
            
        Returns:
            List of HangHoa objects
        """
        goods = self.db.query(HangHoa).filter(
            HangHoa.loai_hang == loai_hang
        ).limit(limit).all()
        
        for hh in goods:
            self.db.refresh(hh)
        
        return goods
    
    def search(self, keyword: str, limit: int = 100) -> List[HangHoa]:
        """
        Search goods
        
        Args:
            keyword: Search keyword
            limit: Maximum results
            
        Returns:
            List of matching HangHoa objects
        """
        goods = self.db.query(HangHoa).filter(
            (HangHoa.ten_hang.contains(keyword)) |
            (HangHoa.loai_hang.contains(keyword)) |
            (HangHoa.ghi_chu.contains(keyword))
        ).limit(limit).all()
        
        for hh in goods:
            self.db.refresh(hh)
        
        return goods
    
    def get_low_stock(self, threshold: int = 10) -> List[HangHoa]:
        """
        Get goods with low stock
        
        Args:
            threshold: Minimum stock level alert
            
        Returns:
            List of goods with low stock
        """
        goods = self.db.query(HangHoa).filter(
            HangHoa.trang_thai == 'trong_kho',
            HangHoa.so_luong <= threshold
        ).all()
        
        for hh in goods:
            self.db.refresh(hh)
        
        return goods
    
    # ==================== Business Logic ====================
    
    def get_tong_gia_tri(self, ma_hop_dong: Optional[str] = None) -> float:
        """
        Get total value of goods
        
        Args:
            ma_hop_dong: Optional contract filter
            
        Returns:
            Total value
        """
        query = self.db.query(HangHoa)
        
        if ma_hop_dong:
            query = query.filter(HangHoa.ma_hop_dong == ma_hop_dong)
        
        goods = query.all()
        return sum(hh.gia_tri or 0 for hh in goods)
    
    def get_inventory_summary(self) -> Dict[str, Any]:
        """
        Get inventory summary
        
        Returns:
            Dict with summary statistics
        """
        all_goods = self.get_all()
        in_stock = self.get_inventory()
        low_stock = self.get_low_stock()
        
        # Group by type
        by_type = {}
        for hh in all_goods:
            if hh.loai_hang not in by_type:
                by_type[hh.loai_hang] = {'count': 0, 'so_luong': 0, 'gia_tri': 0}
            by_type[hh.loai_hang]['count'] += 1
            by_type[hh.loai_hang]['so_luong'] += hh.so_luong
            by_type[hh.loai_hang]['gia_tri'] += hh.gia_tri or 0
        
        return {
            'tong_so_mat_hang': len(all_goods),
            'so_mat_hang_trong_kho': len(in_stock),
            'so_mat_hang_low_stock': len(low_stock),
            'tong_gia_tri': self.get_tong_gia_tri(),
            'theo_loai': by_type
        }
    
    def get_stock_movement_history(self, ma_hang_hoa: str) -> List[Dict[str, Any]]:
        """
        Get stock movement history for goods
        
        Args:
            ma_hang_hoa: Goods ID
            
        Returns:
            List of movement events
        """
        hang_hoa = self.get_by_id(ma_hang_hoa)
        if not hang_hoa:
            return []
        
        history = []
        
        # Import event
        history.append({
            'ngay': hang_hoa.ngay_nhap.isoformat() if hang_hoa.ngay_nhap else None,
            'su_kien': 'Nhập kho',
            'so_luong': hang_hoa.so_luong,
            'ghi_chu': f'Nhập lần đầu: {hang_hoa.so_luong} {hang_hoa.don_vi}'
        })
        
        # Export event (if any)
        if hang_hoa.ngay_xuat:
            history.append({
                'ngay': hang_hoa.ngay_xuat.isoformat() if hang_hoa.ngay_xuat else None,
                'su_kien': 'Xuất kho',
                'so_luong': 0,
                'ghi_chu': f'Đã xuất hết'
            })
        
        # Sort by date
        history.sort(key=lambda x: x['ngay'] or '', reverse=True)
        
        return history
    
    # ==================== Helper Methods ====================
    
    def _auto_generate_ma_hang_hoa(self, ma_hop_dong: str) -> str:
        """
        Auto-generate goods ID
        
        Format: {MA_HOP_DONG}-HH{XXX} (e.g., HD202604001-HH001)
        
        Returns:
            Generated goods ID
        """
        prefix = f"{ma_hop_dong}-HH"
        
        # Get last goods of this contract
        last = self.db.query(HangHoa).filter(
            HangHoa.ma_hang_hoa.startswith(prefix)
        ).order_by(HangHoa.ma_hang_hoa.desc()).first()
        
        if last:
            try:
                seq = int(last.ma_hang_hoa.split('-HH')[-1]) + 1
            except (ValueError, IndexError):
                seq = 1
        else:
            seq = 1
        
        return f"{prefix}{seq:03d}"


# Convenience functions
def create_hang_hoa(data: Dict[str, Any]) -> HangHoa:
    """Create new goods"""
    service = HangHoaService()
    return service.create(data)


def get_hang_hoa_by_id(ma_hang_hoa: str) -> Optional[HangHoa]:
    """Get goods by ID"""
    service = HangHoaService()
    return service.get_by_id(ma_hang_hoa)


def get_hang_hoa_by_contract(ma_hop_dong: str) -> List[HangHoa]:
    """Get goods by contract"""
    service = HangHoaService()
    return service.get_by_hop_dong(ma_hop_dong)


def get_inventory(ma_hop_dong: Optional[str] = None) -> List[HangHoa]:
    """Get current inventory"""
    service = HangHoaService()
    return service.get_inventory(ma_hop_dong)


def import_goods(data: Dict[str, Any]) -> HangHoa:
    """Import goods to warehouse"""
    service = HangHoaService()
    return service.import_goods(data)


def export_goods(ma_hang_hoa: str, so_luong: int, data: Dict[str, Any] = None) -> bool:
    """Export goods from warehouse"""
    service = HangHoaService()
    return service.export_goods(ma_hang_hoa, so_luong, data)


__all__ = [
    'HangHoaService',
    'create_hang_hoa',
    'get_hang_hoa_by_id',
    'get_hang_hoa_by_contract',
    'get_inventory',
    'import_goods',
    'export_goods',
]
