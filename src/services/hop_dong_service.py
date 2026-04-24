#!/usr/bin/env python3
"""
Hợp đồng Service - Business logic for contract management
"""
from datetime import datetime, date, timedelta
from typing import List, Optional, Dict, Any
from dateutil.relativedelta import relativedelta

from src.models import HopDong, TrangThaiHDEnum, KhachHang, ViTri, TrangThaiViTriEnum
from src.database import SessionLocal


class HopDongService:
    """
    Service layer for HopDong (Contract) management
    Handles business logic and database operations
    """
    
    def __init__(self):
        self.db = SessionLocal()
    
    def __del__(self):
        if hasattr(self, 'db') and self.db:
            self.db.close()
    
    # ==================== CRUD Operations ====================
    
    def create(self, data: Dict[str, Any]) -> HopDong:
        """
        Create a new contract
        
        Args:
            data: Dict with contract data
            
        Returns:
            Created HopDong object
            
        Raises:
            ValueError: If validation fails
        """
        # Validate required fields
        required_fields = ['ma_khach_hang', 'ma_vi_tri', 'ngay_bat_dau', 'ngay_ket_thuc', 'gia_thue']
        for field in required_fields:
            if field not in data or not data[field]:
                raise ValueError(f"Thiếu trường bắt buộc: {field}")
        
        # Validate customer exists
        khach_hang = self.db.query(KhachHang).filter(
            KhachHang.ma_khach_hang == data['ma_khach_hang']
        ).first()
        if not khach_hang:
            raise ValueError("Không tìm thấy khách hàng")
        
        # Validate position exists and is available
        vi_tri = self.db.query(ViTri).filter(
            ViTri.ma_vi_tri == data['ma_vi_tri']
        ).first()
        if not vi_tri:
            raise ValueError("Không tìm thấy vị trí")
        
        if vi_tri.trang_thai != TrangThaiViTriEnum.TRONG:
            raise ValueError("Vị trí đã được thuê hoặc đang bảo trì")
        
        # Validate dates
        if data['ngay_ket_thuc'] <= data['ngay_bat_dau']:
            raise ValueError("Ngày kết thúc phải sau ngày bắt đầu")
        
        # Validate price
        if data['gia_thue'] <= 0:
            raise ValueError("Giá thuê phải lớn hơn 0")
        
        # Auto-generate contract ID
        ma_hop_dong = self._auto_generate_ma_hop_dong()
        
        # Create contract
        hop_dong = HopDong(
            ma_hop_dong=ma_hop_dong,
            ma_khach_hang=data['ma_khach_hang'],
            ma_vi_tri=data['ma_vi_tri'],
            ngay_bat_dau=data['ngay_bat_dau'],
            ngay_ket_thuc=data['ngay_ket_thuc'],
            gia_thue=data['gia_thue'],
            tien_coc=data.get('tien_coc', 0),
            phuong_thuc_thanh_toan=data.get('phuong_thuc_thanh_toan', 'hang_thang'),
            dieu_khoan=data.get('dieu_khoan', ''),
            trang_thai=TrangThaiHDEnum.HIEU_LUC
        )
        
        # Update position status
        vi_tri.trang_thai = TrangThaiViTriEnum.DA_THUE
        
        self.db.add(hop_dong)
        self.db.commit()
        self.db.refresh(hop_dong)
        
        return hop_dong
    
    def get_by_id(self, ma_hop_dong: str) -> Optional[HopDong]:
        """
        Get contract by ID
        
        Args:
            ma_hop_dong: Contract ID
            
        Returns:
            HopDong object or None
        """
        hop_dong = self.db.query(HopDong).filter(
            HopDong.ma_hop_dong == ma_hop_dong
        ).first()
        
        if hop_dong:
            self.db.refresh(hop_dong)
        return hop_dong
    
    def get_all(self, skip: int = 0, limit: int = 100, 
                trang_thai: Optional[TrangThaiHDEnum] = None) -> List[HopDong]:
        """
        Get all contracts with pagination and filter
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records
            trang_thai: Filter by status
            
        Returns:
            List of HopDong objects
        """
        query = self.db.query(HopDong)
        
        if trang_thai:
            query = query.filter(HopDong.trang_thai == trang_thai)
        
        contracts = query.offset(skip).limit(limit).all()
        
        for contract in contracts:
            self.db.refresh(contract)
        
        return contracts
    
    def update(self, ma_hop_dong: str, data: Dict[str, Any]) -> HopDong:
        """
        Update contract
        
        Args:
            ma_hop_dong: Contract ID
            data: Dict with updated data
            
        Returns:
            Updated HopDong object
            
        Raises:
            ValueError: If contract not found or validation fails
        """
        hop_dong = self.get_by_id(ma_hop_dong)
        if not hop_dong:
            raise ValueError("Không tìm thấy hợp đồng")
        
        # Update fields
        if 'ngay_bat_dau' in data:
            hop_dong.ngay_bat_dau = data['ngay_bat_dau']
        if 'ngay_ket_thuc' in data:
            if data['ngay_ket_thuc'] <= hop_dong.ngay_bat_dau:
                raise ValueError("Ngày kết thúc phải sau ngày bắt đầu")
            hop_dong.ngay_ket_thuc = data['ngay_ket_thuc']
        if 'gia_thue' in data:
            if data['gia_thue'] <= 0:
                raise ValueError("Giá thuê phải lớn hơn 0")
            hop_dong.gia_thue = data['gia_thue']
        if 'tien_coc' in data:
            hop_dong.tien_coc = data['tien_coc']
        if 'phuong_thuc_thanh_toan' in data:
            hop_dong.phuong_thuc_thanh_toan = data['phuong_thuc_thanh_toan']
        if 'dieu_khoan' in data:
            hop_dong.dieu_khoan = data['dieu_khoan']
        
        self.db.commit()
        self.db.refresh(hop_dong)
        
        return hop_dong
    
    def delete(self, ma_hop_dong: str) -> bool:
        """
        Delete contract
        
        Args:
            ma_hop_dong: Contract ID
            
        Returns:
            True if deleted, False otherwise
            
        Raises:
            ValueError: If contract has active payments or goods
        """
        hop_dong = self.get_by_id(ma_hop_dong)
        if not hop_dong:
            return False
        
        # Check if contract has active payments
        from src.models import ThanhToan
        payments = self.db.query(ThanhToan).filter(
            ThanhToan.ma_hop_dong == ma_hop_dong,
            ThanhToan.trang_thai == 'da_thanh_toan'
        ).count()
        
        if payments > 0:
            raise ValueError("Không thể xóa hợp đồng đã có thanh toán")
        
        # Delete related goods
        from src.models import HangHoa
        self.db.query(HangHoa).filter(
            HangHoa.ma_hop_dong == ma_hop_dong
        ).delete()
        
        # Delete related payments
        self.db.query(ThanhToan).filter(
            ThanhToan.ma_hop_dong == ma_hop_dong
        ).delete()
        
        # Update position status
        vi_tri = self.db.query(ViTri).filter(
            ViTri.ma_vi_tri == hop_dong.ma_vi_tri
        ).first()
        if vi_tri:
            vi_tri.trang_thai = TrangThaiViTriEnum.TRONG
        
        # Delete contract
        self.db.delete(hop_dong)
        self.db.commit()
        
        return True
    
    # ==================== Query Methods ====================
    
    def get_by_customer(self, ma_khach_hang: str, 
                        active_only: bool = True) -> List[HopDong]:
        """
        Get contracts by customer
        
        Args:
            ma_khach_hang: Customer ID
            active_only: Only return active contracts
            
        Returns:
            List of HopDong objects
        """
        query = self.db.query(HopDong).filter(
            HopDong.ma_khach_hang == ma_khach_hang
        )
        
        if active_only:
            query = query.filter(HopDong.trang_thai == TrangThaiHDEnum.HIEU_LUC)
        
        contracts = query.all()
        
        for contract in contracts:
            self.db.refresh(contract)
        
        return contracts
    
    def get_by_location(self, ma_vi_tri: str) -> List[HopDong]:
        """
        Get contracts by location
        
        Args:
            ma_vi_tri: Position ID
            
        Returns:
            List of HopDong objects
        """
        contracts = self.db.query(HopDong).filter(
            HopDong.ma_vi_tri == ma_vi_tri
        ).all()
        
        for contract in contracts:
            self.db.refresh(contract)
        
        return contracts
    
    def get_expiring_soon(self, days: int = 30) -> List[HopDong]:
        """
        Get contracts expiring soon
        
        Args:
            days: Number of days to check
            
        Returns:
            List of HopDong objects expiring within specified days
        """
        today = date.today()
        future_date = today + timedelta(days=days)
        
        contracts = self.db.query(HopDong).filter(
            HopDong.trang_thai == TrangThaiHDEnum.HIEU_LUC,
            HopDong.ngay_ket_thuc >= today,
            HopDong.ngay_ket_thuc <= future_date
        ).all()
        
        for contract in contracts:
            self.db.refresh(contract)
        
        return contracts
    
    def search(self, keyword: str, limit: int = 100) -> List[HopDong]:
        """
        Search contracts
        
        Args:
            keyword: Search keyword
            limit: Maximum results
            
        Returns:
            List of matching HopDong objects
        """
        # Search by contract ID, customer name, or location
        contracts = self.db.query(HopDong).filter(
            (HopDong.ma_hop_dong.contains(keyword)) |
            (HopDong.ma_khach_hang.contains(keyword)) |
            (HopDong.ma_vi_tri.contains(keyword))
        ).limit(limit).all()
        
        for contract in contracts:
            self.db.refresh(contract)
        
        return contracts
    
    # ==================== Business Logic ====================
    
    def renew(self, ma_hop_dong: str, data: Dict[str, Any]) -> HopDong:
        """
        Renew contract
        
        Args:
            ma_hop_dong: Contract ID
            data: Renewal data (ngay_ket_thuc_moi, gia_thue_moi, etc.)
            
        Returns:
            Updated HopDong object
            
        Raises:
            ValueError: If contract not found or not eligible for renewal
        """
        hop_dong = self.get_by_id(ma_hop_dong)
        if not hop_dong:
            raise ValueError("Không tìm thấy hợp đồng")
        
        if hop_dong.trang_thai not in [TrangThaiHDEnum.HIEU_LUC, TrangThaiHDEnum.HET_HAN]:
            raise ValueError("Hợp đồng không thể gia hạn")
        
        # Update contract
        if 'ngay_ket_thuc_moi' in data:
            hop_dong.ngay_ket_thuc = data['ngay_ket_thuc_moi']
        if 'gia_thue_moi' in data:
            hop_dong.gia_thue = data['gia_thue_moi']
        
        hop_dong.trang_thai = TrangThaiHDEnum.GIA_HAN
        
        self.db.commit()
        self.db.refresh(hop_dong)
        
        return hop_dong
    
    def terminate(self, ma_hop_dong: str, ly_do: str) -> bool:
        """
        Terminate contract
        
        Args:
            ma_hop_dong: Contract ID
            ly_do: Reason for termination
            
        Returns:
            True if terminated, False otherwise
            
        Raises:
            ValueError: If contract not found
        """
        hop_dong = self.get_by_id(ma_hop_dong)
        if not hop_dong:
            raise ValueError("Không tìm thấy hợp đồng")
        
        hop_dong.trang_thai = TrangThaiHDEnum.CHAM_DUT
        hop_dong.ly_do_cham_dut = ly_do
        hop_dong.ngay_cham_dut = date.today()
        
        # Update position status
        vi_tri = self.db.query(ViTri).filter(
            ViTri.ma_vi_tri == hop_dong.ma_vi_tri
        ).first()
        if vi_tri:
            vi_tri.trang_thai = TrangThaiViTriEnum.TRONG
        
        self.db.commit()
        
        return True
    
    def get_remaining_days(self, ma_hop_dong: str) -> Optional[int]:
        """
        Get remaining days of contract
        
        Args:
            ma_hop_dong: Contract ID
            
        Returns:
            Number of remaining days or None
        """
        hop_dong = self.get_by_id(ma_hop_dong)
        if not hop_dong:
            return None
        
        today = date.today()
        remaining = (hop_dong.ngay_ket_thuc - today).days
        
        return max(0, remaining)
    
    def get_contract_duration_months(self, ma_hop_dong: str) -> Optional[int]:
        """
        Get contract duration in months
        
        Args:
            ma_hop_dong: Contract ID
            
        Returns:
            Number of months or None
        """
        hop_dong = self.get_by_id(ma_hop_dong)
        if not hop_dong:
            return None
        
        delta = relativedelta(hop_dong.ngay_ket_thuc, hop_dong.ngay_bat_dau)
        return delta.years * 12 + delta.months
    
    def calculate_total_amount(self, ma_hop_dong: str) -> Optional[Dict[str, float]]:
        """
        Calculate total contract amount
        
        Args:
            ma_hop_dong: Contract ID
            
        Returns:
            Dict with total_rent, deposit, total or None
        """
        hop_dong = self.get_by_id(ma_hop_dong)
        if not hop_dong:
            return None
        
        duration_months = self.get_contract_duration_months(ma_hop_dong)
        total_rent = duration_months * hop_dong.gia_thue
        
        return {
            'tong_tien_thue': total_rent,
            'tien_coc': hop_dong.tien_coc,
            'tong_cong': total_rent + hop_dong.tien_coc
        }
    
    def get_statistics(self, ma_khach_hang: Optional[str] = None) -> Dict[str, Any]:
        """
        Get contract statistics
        
        Args:
            ma_khach_hang: Optional customer ID filter
            
        Returns:
            Dict with statistics
        """
        query = self.db.query(HopDong)
        
        if ma_khach_hang:
            query = query.filter(HopDong.ma_khach_hang == ma_khach_hang)
        
        total = query.count()
        active = query.filter(HopDong.trang_thai == TrangThaiHDEnum.HIEU_LUC).count()
        expired = query.filter(HopDong.trang_thai == TrangThaiHDEnum.HET_HAN).count()
        terminated = query.filter(HopDong.trang_thai == TrangThaiHDEnum.CHAM_DUT).count()
        
        # Get expiring soon
        expiring_soon = len(self.get_expiring_soon(30))
        
        return {
            'tong_so_hop_dong': total,
            'so_hop_dong_dang_hieu_luc': active,
            'so_hop_dong_het_han': expired,
            'so_hop_dong_cham_dut': terminated,
            'so_hop_dong_sap_het_han': expiring_soon
        }
    
    # ==================== Helper Methods ====================
    
    def _auto_generate_ma_hop_dong(self) -> str:
        """
        Auto-generate contract ID
        
        Format: HD + YYYYMM + XXX (e.g., HD202604001)
        
        Returns:
            Generated contract ID
        """
        today = date.today()
        prefix = f"HD{today.strftime('%Y%m')}"
        
        # Get last contract of this month
        last_contract = self.db.query(HopDong).filter(
            HopDong.ma_hop_dong.startswith(prefix)
        ).order_by(HopDong.ma_hop_dong.desc()).first()
        
        if last_contract:
            # Extract sequence number and increment
            try:
                seq = int(last_contract.ma_hop_dong[-3:])
                new_seq = seq + 1
            except (ValueError, IndexError):
                new_seq = 1
        else:
            new_seq = 1
        
        return f"{prefix}{new_seq:03d}"


# Convenience functions
def create_hop_dong(data: Dict[str, Any]) -> HopDong:
    """Create a new contract"""
    service = HopDongService()
    return service.create(data)


def get_hop_dong_by_id(ma_hop_dong: str) -> Optional[HopDong]:
    """Get contract by ID"""
    service = HopDongService()
    return service.get_by_id(ma_hop_dong)


def get_all_hop_dongs(skip: int = 0, limit: int = 100) -> List[HopDong]:
    """Get all contracts"""
    service = HopDongService()
    return service.get_all(skip=skip, limit=limit)


def get_hop_dongs_by_customer(ma_khach_hang: str) -> List[HopDong]:
    """Get contracts by customer"""
    service = HopDongService()
    return service.get_by_customer(ma_khach_hang)


def get_expiring_contracts(days: int = 30) -> List[HopDong]:
    """Get contracts expiring soon"""
    service = HopDongService()
    return service.get_expiring_soon(days=days)


__all__ = [
    'HopDongService',
    'TrangThaiHDEnum',
    'create_hop_dong',
    'get_hop_dong_by_id',
    'get_all_hop_dongs',
    'get_hop_dongs_by_customer',
    'get_expiring_contracts',
]
