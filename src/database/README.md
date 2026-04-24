# Database Layer Documentation

## 📁 Cấu trúc

```
src/database/
├── __init__.py              # Exports
├── connection.py            # Connection management
├── repository.py            # Base repository pattern
└── migrate.py               # Migration script

src/models/
├── __init__.py              # Export tất cả models
├── base.py                  # BaseModel class
├── khach_hang.py            # Customer model
├── kho.py                   # Warehouse model
├── vi_tri.py                # Location model
├── hop_dong.py              # Contract model
├── hang_hoa.py              # Goods model
├── thanh_toan.py            # Payment model
├── nhan_vien.py             # Employee model
├── system_log.py            # Audit log model
└── bao_cao.py               # Report model
```

## 🔧 Usage

### Connection Management

```python
from src.database import get_session, session_scope, get_engine

# Cách 1: Sử dụng session_scope (recommended)
with session_scope() as session:
    customer = KhachHang(ma_khach_hang='KH001', ho_ten='Nguyen Van A', ...)
    session.add(customer)
    # Auto commit nếu không có lỗi
    # Auto rollback nếu có exception
    # Auto close session

# Cách 2: Sử dụng get_session thủ công
session = get_session()
try:
    customer = session.query(KhachHang).filter_by(ma_khach_hang='KH001').first()
    # ... do something
    session.commit()
except Exception as e:
    session.rollback()
    raise e
finally:
    session.close()

# Cách 3: Sử dụng get_engine cho raw SQL
engine = get_engine()
with engine.connect() as connection:
    result = connection.execute(text("SELECT * FROM khach_hang"))
```

### Repository Pattern

```python
from src.database import BaseRepository, get_session
from src.models import KhachHang

# Tạo repository cho KhachHang
class KhachHangRepository(BaseRepository[KhachHang]):
    def __init__(self, session):
        super().__init__(session, KhachHang)
    
    def find_by_email(self, email: str):
        return self.session.query(KhachHang).filter_by(email=email).first()
    
    def search(self, keyword: str):
        return self.session.query(KhachHang).filter(
            KhachHang.ho_ten.ilike(f'%{keyword}%')
        ).all()

# Sử dụng
with session_scope() as session:
    repo = KhachHangRepository(session)
    
    # CRUD operations
    customer = repo.create({
        'ma_khach_hang': 'KH001',
        'ho_ten': 'Nguyen Van A',
        'so_dien_thoai': '0901234567',
        'email': 'nguyenvana@email.com',
        'dia_chi': '123 Nguyen Van Linh, Q7, TP.HCM'
    })
    
    # Get by ID
    customer = repo.get_by_id('KH001')
    
    # Get all
    customers = repo.get_all(skip=0, limit=100)
    
    # Update
    repo.update('KH001', {'so_dien_thoai': '0909876543'})
    
    # Delete
    repo.delete('KH001')
    
    # Custom methods
    customer = repo.find_by_email('nguyenvana@email.com')
    customers = repo.search('Nguyen')
```

### Models

```python
from src.models import KhachHang, Kho, ViTri, HopDong
from src.database import get_session

session = get_session()

# Tạo khách hàng mới
customer = KhachHang(
    ma_khach_hang='KH001',
    ho_ten='Nguyen Van A',
    loai_khach='ca_nhan',
    so_dien_thoai='0901234567',
    email='nguyenvana@email.com',
    dia_chi='123 Nguyen Van Linh, Q7, TP.HCM'
)
session.add(customer)
session.commit()

# Query
customer = session.query(KhachHang).filter_by(ma_khach_hang='KH001').first()

# Relationships
contracts = customer.hop_dongs  # List of HopDong
for contract in contracts:
    print(f"Contract: {contract.ma_hop_dong}")
    print(f"Location: {contract.vi_tri.ma_vi_tri}")
    print(f"Goods: {len(contract.hang_hoas)} items")

# Convert to dict/json
data = customer.to_dict()
json_str = customer.to_json()
```

## 📊 Database Schema

### Tables
- `khach_hang` - Customers
- `kho` - Warehouses
- `vi_tri` - Storage locations
- `hop_dong` - Contracts
- `hang_hoa` - Goods/Inventory
- `thanh_toan` - Payments
- `nhan_vien` - Employees/Users
- `system_log` - Audit logs
- `bao_cao` - Reports

### Views
- `v_hop_dong_sap_het_han` - Contracts expiring within 30 days
- `v_cong_no_chua_thanh_toan` - Overdue payments
- `v_ty_le_lap_day_kho` - Warehouse fill rate

### Indexes
20+ indexes for performance on frequently queried columns.

## 🔐 Best Practices

1. **Luôn sử dụng session_scope()** để tự động quản lý commit/rollback
2. **Không giữ session mở** - luôn close sau khi dùng xong
3. **Sử dụng repository pattern** cho data access logic
4. **Validate data** trước khi insert/update
5. **Sử dụng transactions** cho operations liên quan đến nhiều bảng
6. **Handle exceptions** - luôn rollback khi có lỗi

## 📝 Migration

```bash
# Initialize migrations
python -m src.database.migrate init

# Create new migration
python -m src.database.migrate create add_column_to_khach_hang

# Edit the migration file in migrations/versions/

# Apply migrations
python -m src.database.migrate upgrade

# Check status
python -m src.database.migrate status
```

## 🐛 Troubleshooting

### "Database is locked"
- Close other connections
- Check for unclosed sessions
- Use `session_scope()` instead of manual session management

### "No such table"
- Run `python -m src.data.init_db` to create tables
- Check if models are imported correctly

### "Foreign key constraint failed"
- Ensure parent records exist before inserting child records
- Check foreign key relationships in models

---

**Updated:** 23/04/2026  
**Nhóm 12 - Lập trình Python**
