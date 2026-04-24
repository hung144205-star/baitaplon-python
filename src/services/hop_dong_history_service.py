#!/usr/bin/env python3
"""
Hợp đồng History Service - Track contract changes and events
"""
from datetime import datetime, date
from typing import List, Optional, Dict, Any
from enum import Enum

from src.models import HopDong, TrangThaiHDEnum
from src.database import SessionLocal


class EventType(Enum):
    """Contract event types"""
    CREATED = 'created'
    UPDATED = 'updated'
    RENEWED = 'renewed'
    TERMINATED = 'terminated'
    PAYMENT_RECEIVED = 'payment_received'
    GOODS_ADDED = 'goods_added'
    GOODS_REMOVED = 'goods_removed'


class HopDongHistory:
    """Contract history log (not persisted, just for display)"""
    def __init__(self, id: int, ma_hop_dong: str, event_type: str, 
                 event_date: date, description: str, user: str = "System"):
        self.id = id
        self.ma_hop_dong = ma_hop_dong
        self.event_type = event_type
        self.event_date = event_date
        self.description = description
        self.user = user


class HopDongHistoryService:
    """
    Service layer for contract history tracking
    """
    
    def __init__(self):
        self.db = SessionLocal()
    
    def __del__(self):
        if hasattr(self, 'db') and self.db:
            self.db.close()
    
    def get_history(self, ma_hop_dong: str) -> List[HopDongHistory]:
        """
        Get contract history
        
        This combines multiple sources:
        - Contract creation and updates
        - Status changes
        - Payment events
        - Goods events
        """
        history = []
        event_id = 0
        
        # Get contract
        hop_dong = self.db.query(HopDong).filter(
            HopDong.ma_hop_dong == ma_hop_dong
        ).first()
        
        if not hop_dong:
            return history
        
        # 1. Contract creation event
        event_id += 1
        history.append(HopDongHistory(
            id=event_id,
            ma_hop_dong=ma_hop_dong,
            event_type=EventType.CREATED.value,
            event_date=hop_dong.ngay_bat_dau,
            description=f"Tạo hợp đồng - Mã: {ma_hop_dong}",
            user="System"
        ))
        
        # 2. Status change events (if any)
        if hop_dong.trang_thai == TrangThaiHDEnum.GIA_HAN:
            event_id += 1
            history.append(HopDongHistory(
                id=event_id,
                ma_hop_dong=ma_hop_dong,
                event_type=EventType.RENEWED.value,
                event_date=hop_dong.ngay_bat_dau,  # Would be better with actual renew date
                description="Gia hạn hợp đồng",
                user="System"
            ))
        
        if hop_dong.trang_thai == TrangThaiHDEnum.CHAM_DUT:
            event_id += 1
            history.append(HopDongHistory(
                id=event_id,
                ma_hop_dong=ma_hop_dong,
                event_type=EventType.TERMINATED.value,
                event_date=hop_dong.ngay_cham_dut or hop_dong.ngay_ket_thuc,
                description=f"Chấm dứt hợp đồng - Lý do: {hop_dong.ly_do_cham_dut or 'Không rõ'}",
                user="System"
            ))
        
        # 3. Payment events
        try:
            from src.models import ThanhToan
            payments = self.db.query(ThanhToan).filter(
                ThanhToan.ma_hop_dong == ma_hop_dong
            ).order_by(ThanhToan.ngay_thanh_toan).all()
            
            for payment in payments:
                if payment.trang_thai == 'da_thanh_toan' and payment.ngay_thanh_toan:
                    event_id += 1
                    history.append(HopDongHistory(
                        id=event_id,
                        ma_hop_dong=ma_hop_dong,
                        event_type=EventType.PAYMENT_RECEIVED.value,
                        event_date=payment.ngay_thanh_toan,
                        description=f"Nhận thanh toán {payment.ky_thanh_toan}: {payment.so_tien:,.0f}₫",
                        user="System"
                    ))
        except:
            pass  # ThanhToan table might not exist yet
        
        # 4. Goods events
        try:
            from src.models import HangHoa
            # For now, just show goods count
            goods_count = self.db.query(HangHoa).filter(
                HangHoa.ma_hop_dong == ma_hop_dong
            ).count()
            
            if goods_count > 0:
                event_id += 1
                history.append(HopDongHistory(
                    id=event_id,
                    ma_hop_dong=ma_hop_dong,
                    event_type=EventType.GOODS_ADDED.value,
                    event_date=hop_dong.ngay_bat_dau,
                    description=f"Đã đăng ký {goods_count} mặt hàng",
                    user="System"
                ))
        except:
            pass  # HangHoa table might not exist yet
        
        # Sort by date descending (newest first)
        history.sort(key=lambda x: x.event_date, reverse=True)
        
        return history
    
    def log_event(self, ma_hop_dong: str, event_type: EventType, 
                  description: str, user: str = "System") -> HopDongHistory:
        """
        Log a new event
        Note: This is temporary, would need a database table for persistence
        """
        # For now, just return a history object
        # In production, this would save to a hop_dong_history table
        event_id = len(self.get_history(ma_hop_dong)) + 1
        
        return HopDongHistory(
            id=event_id,
            ma_hop_dong=ma_hop_dong,
            event_type=event_type.value,
            event_date=date.today(),
            description=description,
            user=user
        )
    
    def get_statistics(self, ma_hop_dong: str) -> Dict[str, Any]:
        """Get contract statistics"""
        history = self.get_history(ma_hop_dong)
        
        stats = {
            'tong_su_kien': len(history),
            'so_lan_thanh_toan': sum(1 for h in history if h.event_type == EventType.PAYMENT_RECEIVED.value),
            'so_lan_gia_han': sum(1 for h in history if h.event_type == EventType.RENEWED.value),
            'so_mat_hang': 0,  # Would need to query HangHoa
        }
        
        # Count goods
        try:
            from src.models import HangHoa
            stats['so_mat_hang'] = self.db.query(HangHoa).filter(
                HangHoa.ma_hop_dong == ma_hop_dong
            ).count()
        except:
            pass
        
        return stats


__all__ = ['HopDongHistoryService', 'EventType', 'HopDongHistory']
