"""
Database initialization script
Khởi tạo database với SQLAlchemy models

Hệ thống Quản lý Dịch vụ Cho thuê Kho Lưu trữ Hàng Hóa
Nhóm 12 - Lập trình Python
"""
from sqlalchemy import create_engine, text, or_
from sqlalchemy.orm import sessionmaker, Session as OrmSession
from typing import Callable
import os
import sys

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

# Import models
from src.models import (
    Base, KhachHang, Kho, ViTri, HopDong, HangHoa, 
    ThanhToan, NhanVien, SystemLog, BaoCao,
    VaiTroNVEuum
)

# Default database path
DB_PATH = os.path.join(project_root, 'data', 'warehouse.db')

def get_database_url(db_path: str = None) -> str:
    """Get database URL"""
    if db_path is None:
        db_path = DB_PATH
    
    # Ensure directory exists
    db_dir = os.path.dirname(db_path)
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir)
    
    return f"sqlite:///{db_path}"

def init_db(db_path: str = None, echo: bool = False) -> tuple:
    """
    Khởi tạo database và tạo các bảng
    
    Args:
        db_path: Đường dẫn file database (default: data/warehouse.db)
        echo: Nếu True, in SQL commands ra console (cho debugging)
    
    Returns:
        Tuple (engine, Session)
    """
    database_url = get_database_url(db_path)
    print(f"📦 Kết nối database: {database_url}")
    
    # Create engine
    engine = create_engine(
        database_url,
        echo=echo,
        connect_args={'check_same_thread': False}  # For SQLite
    )
    
    # Create all tables
    print("📝 Đang tạo các bảng...")
    Base.metadata.create_all(engine)
    print("✅ Database đã được tạo thành công!")
    
    # Create session factory
    Session = sessionmaker(bind=engine)
    
    return engine, Session

def get_session(session_factory: Callable[[], OrmSession]) -> OrmSession:
    """Tạo session mới để làm việc với database"""
    return session_factory()

def create_indexes(engine):
    """Tạo indexes cho database"""
    print("📇 Đang tạo indexes...")
    
    indexes = [
        # Khach Hang
        "CREATE INDEX IF NOT EXISTS idx_khach_hang_so_dien_thoai ON khach_hang(so_dien_thoai)",
        "CREATE INDEX IF NOT EXISTS idx_khach_hang_email ON khach_hang(email)",
        "CREATE INDEX IF NOT EXISTS idx_khach_hang_trang_thai ON khach_hang(trang_thai)",
        
        # Kho
        "CREATE INDEX IF NOT EXISTS idx_kho_ten_kho ON kho(ten_kho)",
        "CREATE INDEX IF NOT EXISTS idx_kho_trang_thai ON kho(trang_thai)",
        
        # Vi Tri
        "CREATE INDEX IF NOT EXISTS idx_vi_tri_ma_kho ON vi_tri(ma_kho)",
        "CREATE INDEX IF NOT EXISTS idx_vi_tri_trang_thai ON vi_tri(trang_thai)",
        "CREATE INDEX IF NOT EXISTS idx_vi_tri_khu_vuc ON vi_tri(khu_vuc, hang, tang)",
        
        # Hop Dong
        "CREATE INDEX IF NOT EXISTS idx_hop_dong_ma_khach_hang ON hop_dong(ma_khach_hang)",
        "CREATE INDEX IF NOT EXISTS idx_hop_dong_ma_vi_tri ON hop_dong(ma_vi_tri)",
        "CREATE INDEX IF NOT EXISTS idx_hop_dong_ngay_ket_thuc ON hop_dong(ngay_ket_thuc)",
        "CREATE INDEX IF NOT EXISTS idx_hop_dong_trang_thai ON hop_dong(trang_thai)",
        "CREATE INDEX IF NOT EXISTS idx_hop_dong_kh_trang_thai ON hop_dong(ma_khach_hang, trang_thai)",
        
        # Hang Hoa
        "CREATE INDEX IF NOT EXISTS idx_hang_hoa_ma_hop_dong ON hang_hoa(ma_hop_dong)",
        "CREATE INDEX IF NOT EXISTS idx_hang_hoa_ten_hang ON hang_hoa(ten_hang)",
        "CREATE INDEX IF NOT EXISTS idx_hang_hoa_trang_thai ON hang_hoa(trang_thai)",
        "CREATE INDEX IF NOT EXISTS idx_hang_hoa_ngay_nhap ON hang_hoa(ngay_nhap)",
        "CREATE INDEX IF NOT EXISTS idx_hang_hoa_hd_trang_thai ON hang_hoa(ma_hop_dong, trang_thai)",
        
        # Thanh Toan
        "CREATE INDEX IF NOT EXISTS idx_thanh_toan_ma_hop_dong ON thanh_toan(ma_hop_dong)",
        "CREATE INDEX IF NOT EXISTS idx_thanh_toan_ngay_den_han ON thanh_toan(ngay_den_han)",
        "CREATE INDEX IF NOT EXISTS idx_thanh_toan_trang_thai ON thanh_toan(trang_thai)",
        "CREATE INDEX IF NOT EXISTS idx_thanh_toan_hd_trang_thai ON thanh_toan(ma_hop_dong, trang_thai)",
        
        # Nhan Vien
        "CREATE INDEX IF NOT EXISTS idx_nhan_vien_tai_khoan ON nhan_vien(tai_khoan)",
        "CREATE INDEX IF NOT EXISTS idx_nhan_vien_email ON nhan_vien(email)",
        "CREATE INDEX IF NOT EXISTS idx_nhan_vien_vai_tro ON nhan_vien(vai_tro)",
        
        # System Log
        "CREATE INDEX IF NOT EXISTS idx_system_log_thoi_gian ON system_log(thoi_gian)",
        "CREATE INDEX IF NOT EXISTS idx_system_log_ma_nhan_vien ON system_log(ma_nhan_vien)",
        "CREATE INDEX IF NOT EXISTS idx_system_log_hanh_dong ON system_log(hanh_dong)",
        "CREATE INDEX IF NOT EXISTS idx_system_log_ban_ghi ON system_log(ban_ghi)",
        
        # Bao Cao
        "CREATE INDEX IF NOT EXISTS idx_bao_cao_loai_bao_cao ON bao_cao(loai_bao_cao)",
        "CREATE INDEX IF NOT EXISTS idx_bao_cao_ngay_tao ON bao_cao(ngay_tao)",
    ]
    
    with engine.connect() as conn:
        for index_sql in indexes:
            conn.execute(text(index_sql))
        conn.commit()
    
    print("✅ Indexes đã được tạo!")

def create_views(engine):
    """Tạo các views hữu ích"""
    print("👁️ Đang tạo views...")
    
    views = [
        # View: Hợp đồng sắp hết hạn
        """
        CREATE VIEW IF NOT EXISTS v_hop_dong_sap_het_han AS
        SELECT 
            hd.ma_hop_dong,
            hd.ma_khach_hang,
            kh.ho_ten AS ten_khach_hang,
            hd.ma_vi_tri,
            hd.ngay_bat_dau,
            hd.ngay_ket_thuc,
            hd.gia_thue,
            hd.trang_thai,
            julianday(hd.ngay_ket_thuc) - julianday('now') AS so_ngay_con_lai
        FROM hop_dong hd
        JOIN khach_hang kh ON hd.ma_khach_hang = kh.ma_khach_hang
        WHERE hd.trang_thai = 'hieu_luc'
          AND hd.ngay_ket_thuc <= date('now', '+30 days')
          AND hd.ngay_ket_thuc >= date('now')
        ORDER BY hd.ngay_ket_thuc ASC
        """,
        
        # View: Công nợ chưa thanh toán
        """
        CREATE VIEW IF NOT EXISTS v_cong_no_chua_thanh_toan AS
        SELECT 
            tt.ma_thanh_toan,
            tt.ma_hop_dong,
            hd.ma_khach_hang,
            kh.ho_ten AS ten_khach_hang,
            tt.loai_phi,
            tt.so_tien,
            tt.phi_phat,
            tt.so_tien + tt.phi_phat AS tong_cong,
            tt.ngay_den_han,
            julianday('now') - julianday(tt.ngay_den_han) AS so_ngay_qua_han,
            tt.trang_thai
        FROM thanh_toan tt
        JOIN hop_dong hd ON tt.ma_hop_dong = hd.ma_hop_dong
        JOIN khach_hang kh ON hd.ma_khach_hang = kh.ma_khach_hang
        WHERE tt.trang_thai IN ('chua_thanh_toan', 'qua_han')
        ORDER BY tt.ngay_den_han ASC
        """,
        
        # View: Tỷ lệ lấp đầy kho
        """
        CREATE VIEW IF NOT EXISTS v_ty_le_lap_day_kho AS
        SELECT 
            k.ma_kho,
            k.ten_kho,
            k.dien_tich,
            k.suc_chua,
            COALESCE(SUM(v.dien_tich), 0) AS da_su_dung,
            ROUND((COALESCE(SUM(v.dien_tich), 0) * 100.0 / k.suc_chua), 2) AS ty_le_lap_day_phan_tram
        FROM kho k
        LEFT JOIN vi_tri v ON k.ma_kho = v.ma_kho AND v.trang_thai = 'da_thue'
        WHERE k.trang_thai = 'hoat_dong'
        GROUP BY k.ma_kho, k.ten_kho, k.dien_tich, k.suc_chua
        """,
    ]
    
    with engine.connect() as conn:
        for view_sql in views:
            conn.execute(text(view_sql))
        conn.commit()
    
    print("✅ Views đã được tạo!")

def create_sample_data(session_factory):
    """Tạo dữ liệu mẫu"""
    print("📊 Đang tạo dữ liệu mẫu...")
    
    session = get_session(session_factory)
    
    try:
        session.execute(text("UPDATE nhan_vien SET vai_tro = LOWER(vai_tro) WHERE vai_tro IS NOT NULL"))
        session.execute(text("UPDATE nhan_vien SET trang_thai = LOWER(trang_thai) WHERE trang_thai IS NOT NULL"))
        session.execute(text("UPDATE khach_hang SET loai_khach = LOWER(loai_khach) WHERE loai_khach IS NOT NULL"))
        session.execute(text("UPDATE khach_hang SET trang_thai = LOWER(trang_thai) WHERE trang_thai IS NOT NULL"))
        session.execute(text("UPDATE kho SET trang_thai = LOWER(trang_thai) WHERE trang_thai IS NOT NULL"))
        session.execute(text("UPDATE vi_tri SET trang_thai = LOWER(trang_thai) WHERE trang_thai IS NOT NULL"))
        session.execute(text("UPDATE hop_dong SET trang_thai = LOWER(trang_thai) WHERE trang_thai IS NOT NULL"))
        session.execute(text("UPDATE thanh_toan SET loai_phi = LOWER(loai_phi) WHERE loai_phi IS NOT NULL"))
        session.execute(text("UPDATE thanh_toan SET trang_thai = LOWER(trang_thai) WHERE trang_thai IS NOT NULL"))
        session.commit()

        # Tạo admin user (password: admin123 - properly generated bcrypt hash)
        admin = NhanVien(
            ma_nhan_vien='NV001',
            ho_ten='Administrator',
            email='admin@warehouse.local',
            vai_tro=VaiTroNVEuum.QUAN_TRI,
            tai_khoan='admin',
            mat_khau='$2b$12$tTbOaZ0plbpynu3c.SpLkOFsD3gzeyDB2GaMnSV1QK0SCeI81R9lO'
        )
        
        # Tạo kho mẫu
        kho1 = Kho(
            ma_kho='KHO001',
            ten_kho='Kho A - Quận 7',
            dia_chi='123 Đường Nguyễn Văn Linh, Quận 7, TP.HCM',
            dien_tich=1000.0,
            suc_chua=5000.0
        )
        
        # Tạo vị trí mẫu
        vi_tri1 = ViTri(
            ma_vi_tri='K01-A-01-01',
            ma_kho='KHO001',
            khu_vuc='A',
            hang='01',
            tang=1,
            dien_tich=50.0,
            gia_thue=150000.0
        )
        
        vi_tri2 = ViTri(
            ma_vi_tri='K01-A-01-02',
            ma_kho='KHO001',
            khu_vuc='A',
            hang='01',
            tang=1,
            dien_tich=75.0,
            gia_thue=150000.0
        )
        
        # Tạo khách hàng mẫu
        khach_hang1 = KhachHang(
            ma_khach_hang='KH001',
            ho_ten='Nguyễn Văn A',
            loai_khach='ca_nhan',
            so_dien_thoai='0901234567',
            email='nguyenvana@email.com',
            dia_chi='456 Đường ABC, Quận 1, TP.HCM'
        )
        
        # Thêm vào session nếu chưa tồn tại
        admin_exists = session.query(NhanVien).filter(
            or_(
                NhanVien.ma_nhan_vien == admin.ma_nhan_vien,
                NhanVien.email == admin.email,
                NhanVien.tai_khoan == admin.tai_khoan
            )
        ).first()
        if not admin_exists:
            session.add(admin)

        kho_exists = session.query(Kho).filter(Kho.ma_kho == kho1.ma_kho).first()
        if not kho_exists:
            session.add(kho1)

        vi_tri1_exists = session.query(ViTri).filter(ViTri.ma_vi_tri == vi_tri1.ma_vi_tri).first()
        if not vi_tri1_exists:
            session.add(vi_tri1)

        vi_tri2_exists = session.query(ViTri).filter(ViTri.ma_vi_tri == vi_tri2.ma_vi_tri).first()
        if not vi_tri2_exists:
            session.add(vi_tri2)

        khach_hang_exists = session.query(KhachHang).filter(
            or_(
                KhachHang.ma_khach_hang == khach_hang1.ma_khach_hang,
                KhachHang.email == khach_hang1.email
            )
        ).first()
        if not khach_hang_exists:
            session.add(khach_hang1)
        
        # Commit
        session.commit()
        print("✅ Dữ liệu mẫu đã được tạo!")
        
        # In thông tin
        print("\n📋 Thông tin đăng nhập mặc định:")
        print(f"   Username: admin")
        print(f"   Password: admin123")
        print(f"   ⚠️  Vui lòng đổi mật khẩu sau khi đăng nhập!")
        
    except Exception as e:
        session.rollback()
        print(f"❌ Lỗi khi tạo dữ liệu mẫu: {e}")
        raise
    finally:
        session.close()

def main():
    """Hàm main để khởi tạo database"""
    print("=" * 60)
    print("KHỞI TẠO DATABASE - QUẢN LÝ KHO LƯU TRỮ")
    print("=" * 60)
    
    # Initialize database
    engine, Session = init_db()
    
    # Create indexes
    create_indexes(engine)
    
    # Create views
    create_views(engine)
    
    # Create sample data
    create_sample_data(Session)
    
    print("\n" + "=" * 60)
    print("✅ HOÀN THÀNH KHỞI TẠO DATABASE!")
    print("=" * 60)

if __name__ == "__main__":
    main()
