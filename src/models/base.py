"""
Base model class với common methods
"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime
from datetime import datetime
import json

Base = declarative_base()

class BaseModel(Base):
    """
    Base class cho tất cả models
    Cung cấp các methods chung
    """
    __abstract__ = True
    
    # Common columns (có thể override trong model con)
    ngay_tao = Column(DateTime, nullable=False, default=datetime.now)
    ngay_cap_nhat = Column(DateTime, onupdate=datetime.now)
    
    def to_dict(self):
        """
        Chuyển model thành dictionary
        """
        data = {}
        for column in self.__table__.columns:
            value = getattr(self, column.name)
            if isinstance(value, datetime):
                value = value.isoformat()
            data[column.name] = value
        return data
    
    def to_json(self):
        """
        Chuyển model thành JSON string
        """
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)
    
    def __repr__(self):
        """
        String representation
        """
        return f"<{self.__class__.__name__}>"
