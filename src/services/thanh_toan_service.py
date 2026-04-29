#!/usr/bin/env python3
"""
Thanh toán Service - Business logic for payment management
"""
from datetime import datetime, date
from typing import List, Optional, Dict, Any

from src.models import ThanhToan, HopDong, TrangThaiHDEnum
from src.database import SessionLocal


class TrangThaiTTEnum:
    """Payment status"""
    CHUA_THANH_TOAN = 'chua_thanh_toan'
    DA_THANH_TOAN = 'da_thanh_toan'
    QUA_HAN = 'qua_han'


class ThanhToanService:
    """
    Service layer for ThanhToan (Payment) management
    """
    
    def __init__(self):
        self.db = SessionLocal()
    
    def __del__(self):
        if hasattr(self, 'db') and self.db:
            self.db.close()
    
    def create(self, data: Dict[str, Any]) -> ThanhToan:
        """Create new payment"""
        # Validate required fields
        required = ['ma_hop_dong', 'ky_thanh_toan', 'ngay_den_han', 'so_tien']
        for field in required:
            if field not in data or not data[field]:
                raise ValueError(f"Thiếu trường bắt buộc: {field}")
        
        # Validate contract exists
        hop_dong = self.db.query(HopDong).filter(
            HopDong.ma_hop_dong == data['ma_hop_dong']
        ).first()
        if not hop_dong:
            raise ValueError("Không tìm thấy hợp đồng")
        
        # Auto-generate ID
        ma_thanh_toan = self._auto_generate_ma_thanh_toan(data['ma_hop_dong'])
        
        thanh_toan = ThanhToan(
            ma_thanh_toan=ma_thanh_toan,
            ma_hop_dong=data['ma_hop_dong'],
            ky_thanh_toan=data['ky_thanh_toan'],
            ngay_den_han=data['ngay_den_han'],
            so_tien=data['so_tien'],
            trang_thai=data.get('trang_thai', TrangThaiTTEnum.CHUA_THANH_TOAN),
            ngay_thanh_toan=data.get('ngay_thanh_toan'),
            ghi_chu=data.get('ghi_chu', '')
        )
        
        self.db.add(thanh_toan)
        self.db.commit()
        self.db.refresh(thanh_toan)
        
        return thanh_toan
    
    def get_by_hop_dong(self, ma_hop_dong: str) -> List[ThanhToan]:
        """Get all payments by contract"""
        payments = self.db.query(ThanhToan).filter(
            ThanhToan.ma_hop_dong == ma_hop_dong
        ).order_by(ThanhToan.ky_thanh_toan).all()
        
        for p in payments:
            self.db.refresh(p)
        
        # Auto-update overdue status
        today = date.today()
        for p in payments:
            if p.trang_thai == TrangThaiTTEnum.CHUA_THANH_TOAN and p.den_han < today:
                p.trang_thai = TrangThaiTTEnum.QUA_HAN
        self.db.commit()
        
        return payments
    
    def update(self, ma_thanh_toan: str, data: Dict[str, Any]) -> ThanhToan:
        """Update payment"""
        payment = self.db.query(ThanhToan).filter(
            ThanhToan.ma_thanh_toan == ma_thanh_toan
        ).first()
        if not payment:
            raise ValueError("Không tìm thấy thanh toán")
        
        if 'ky_thanh_toan' in data:
            payment.ky_thanh_toan = data['ky_thanh_toan']
        if 'ngay_den_han' in data:
            payment.ngay_den_han = data['ngay_den_han']
        if 'so_tien' in data:
            payment.so_tien = data['so_tien']
        if 'trang_thai' in data:
            payment.trang_thai = data['trang_thai']
        if 'ngay_thanh_toan' in data:
            payment.ngay_thanh_toan = data['ngay_thanh_toan']
        if 'ghi_chu' in data:
            payment.ghi_chu = data['ghi_chu']
        
        self.db.commit()
        self.db.refresh(payment)
        
        return payment
    
    def mark_as_paid(self, ma_thanh_toan: str, ngay_thanh_toan: Optional[date] = None) -> ThanhToan:
        """Mark payment as paid"""
        if ngay_thanh_toan is None:
            ngay_thanh_toan = date.today()
        
        return self.update(ma_thanh_toan, {
            'trang_thai': TrangThaiTTEnum.DA_THANH_TOAN,
            'ngay_thanh_toan': ngay_thanh_toan
        })
    
    def delete(self, ma_thanh_toan: str) -> bool:
        """Delete payment (permanent delete)"""
        payment = self.db.query(ThanhToan).filter(
            ThanhToan.ma_thanh_toan == ma_thanh_toan
        ).first()
        
        if not payment:
            raise ValueError("Không tìm thấy thanh toán")
        
        self.db.delete(payment)
        self.db.commit()
        return True
    
    def get_all(self) -> List[ThanhToan]:
        """Get all payments"""
        return self.db.query(ThanhToan).all()
    
    def get_tong_da_thanh_toan(self, ma_hop_dong: str) -> float:
        """Get total paid amount"""
        payments = self.get_by_hop_dong(ma_hop_dong)
        return sum(p.so_tien for p in payments if p.trang_thai == TrangThaiTTEnum.DA_THANH_TOAN)
    
    def get_tong_con_lai(self, ma_hop_dong: str) -> float:
        """Get remaining amount"""
        payments = self.get_by_hop_dong(ma_hop_dong)
        total = sum(p.so_tien for p in payments)
        paid = self.get_tong_da_thanh_toan(ma_hop_dong)
        return total - paid
    
    def _auto_generate_ma_thanh_toan(self, ma_hop_dong: str) -> str:
        """Auto-generate payment ID"""
        prefix = f"{ma_hop_dong}-TT"
        
        last = self.db.query(ThanhToan).filter(
            ThanhToan.ma_thanh_toan.startswith(prefix)
        ).order_by(ThanhToan.ma_thanh_toan.desc()).first()
        
        if last:
            try:
                seq = int(last.ma_thanh_toan.split('-')[-1]) + 1
            except:
                seq = 1
        else:
            seq = 1
        
        return f"{prefix}{seq:03d}"
    
    def generate_payment_schedule(self, ma_hop_dong: str) -> List[ThanhToan]:
        """Generate payment schedule based on contract"""
        from dateutil.relativedelta import relativedelta
        
        hop_dong = self.db.query(HopDong).filter(
            HopDong.ma_hop_dong == ma_hop_dong
        ).first()
        if not hop_dong:
            raise ValueError("Không tìm thấy hợp đồng")
        
        # Check if payments already exist
        existing = self.get_by_hop_dong(ma_hop_dong)
        if existing:
            raise ValueError("Hóa đơn thanh toán đã tồn tại")
        
        # Calculate payment schedule
        start_date = hop_dong.ngay_bat_dau
        end_date = hop_dong.ngay_ket_thuc
        
        # Determine payment frequency
        frequency = hop_dong.phuong_thuc_thanh_toan
        if frequency == 'hang_thang':
            delta = relativedelta(months=1)
        elif frequency == 'hang_quy':
            delta = relativedelta(months=3)
        elif frequency == 'hang_nam':
            delta = relativedelta(years=1)
        else:  # mot_lan
            delta = relativedelta(years=100)  # One payment
        
        # Generate payments
        current_date = start_date
        period = 1
        
        while current_date <= end_date:
            due_date = current_date
            
            payment = ThanhToan(
                ma_thanh_toan=self._auto_generate_ma_thanh_toan(ma_hop_dong),
                ma_hop_dong=ma_hop_dong,
                ky_thanh_toan=f"Kỳ {period}",
                ngay_den_han=due_date,
                so_tien=hop_dong.gia_thue,
                trang_thai=TrangThaiTTEnum.CHUA_THANH_TOAN
            )
            
            self.db.add(payment)
            current_date += delta
            period += 1
        
        self.db.commit()
        return self.get_by_hop_dong(ma_hop_dong)


__all__ = ['ThanhToanService', 'TrangThaiTTEnum']
