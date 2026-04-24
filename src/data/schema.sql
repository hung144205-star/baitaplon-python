-- Schema SQL cho hệ thống Quản lý Kho Lưu trữ
-- Phiên bản: 1.0
-- Ngày: 23/04/2026
-- Nhóm 12 - Lập trình Python

-- Enable foreign keys
PRAGMA foreign_keys = ON;

-- ============================================================================
-- TABLES
-- ============================================================================

-- Bảng khách hàng
CREATE TABLE IF NOT EXISTS khach_hang (
    ma_khach_hang VARCHAR(20) PRIMARY KEY,
    ho_ten VARCHAR(200) NOT NULL,
    loai_khach VARCHAR(20) NOT NULL DEFAULT 'ca_nhan' CHECK (loai_khach IN ('ca_nhan', 'doanh_nghiep')),
    so_dien_thoai VARCHAR(20) NOT NULL,
    email VARCHAR(100) UNIQUE,
    dia_chi TEXT NOT NULL,
    ma_so_thue VARCHAR(20),
    ngay_dang_ky DATE NOT NULL DEFAULT (date('now')),
    trang_thai VARCHAR(20) NOT NULL DEFAULT 'hoat_dong' CHECK (trang_thai IN ('hoat_dong', 'tam_khoa', 'da_xoa')),
    ngay_tao DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ngay_cap_nhat DATETIME
);

-- Bảng kho
CREATE TABLE IF NOT EXISTS kho (
    ma_kho VARCHAR(20) PRIMARY KEY,
    ten_kho VARCHAR(200) NOT NULL,
    dia_chi TEXT NOT NULL,
    dien_tich DECIMAL(12,2) NOT NULL,
    suc_chua DECIMAL(12,2) NOT NULL,
    da_su_dung DECIMAL(12,2) NOT NULL DEFAULT 0,
    trang_thai VARCHAR(20) NOT NULL DEFAULT 'hoat_dong' CHECK (trang_thai IN ('hoat_dong', 'bao_tri', 'ngung')),
    ngay_tao DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ngay_cap_nhat DATETIME
);

-- Bảng vị trí
CREATE TABLE IF NOT EXISTS vi_tri (
    ma_vi_tri VARCHAR(30) PRIMARY KEY,
    ma_kho VARCHAR(20) NOT NULL,
    khu_vuc VARCHAR(50) NOT NULL,
    hang VARCHAR(10) NOT NULL,
    tang INTEGER NOT NULL DEFAULT 1,
    dien_tich DECIMAL(10,2) NOT NULL,
    gia_thue DECIMAL(12,2) NOT NULL,
    suc_chua DECIMAL(10,2),
    trang_thai VARCHAR(20) NOT NULL DEFAULT 'trong' CHECK (trang_thai IN ('trong', 'da_thue', 'bao_tri')),
    ngay_tao DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ngay_cap_nhat DATETIME,
    FOREIGN KEY (ma_kho) REFERENCES kho(ma_kho) ON DELETE RESTRICT
);

-- Bảng hợp đồng
CREATE TABLE IF NOT EXISTS hop_dong (
    ma_hop_dong VARCHAR(20) PRIMARY KEY,
    ma_khach_hang VARCHAR(20) NOT NULL,
    ma_vi_tri VARCHAR(30) NOT NULL,
    ngay_bat_dau DATE NOT NULL,
    ngay_ket_thuc DATE NOT NULL,
    gia_thue DECIMAL(12,2) NOT NULL,
    tien_coc DECIMAL(12,2) NOT NULL DEFAULT 0,
    phuong_thuc_thanh_toan VARCHAR(20) DEFAULT 'hang_thang',
    dieu_khoan TEXT,
    trang_thai VARCHAR(20) NOT NULL DEFAULT 'hieu_luc' CHECK (trang_thai IN ('hieu_luc', 'het_han', 'cham_dut', 'gia_han')),
    ly_do_cham_dut TEXT,
    ngay_cham_dut DATE,
    ngay_tao DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ngay_cap_nhat DATETIME,
    FOREIGN KEY (ma_khach_hang) REFERENCES khach_hang(ma_khach_hang),
    FOREIGN KEY (ma_vi_tri) REFERENCES vi_tri(ma_vi_tri)
);

-- Bảng hàng hóa
CREATE TABLE IF NOT EXISTS hang_hoa (
    ma_hang_hoa VARCHAR(30) PRIMARY KEY,
    ma_hop_dong VARCHAR(20) NOT NULL,
    ten_hang VARCHAR(200) NOT NULL,
    loai_hang VARCHAR(100) NOT NULL,
    so_luong INTEGER NOT NULL DEFAULT 0,
    don_vi VARCHAR(20) NOT NULL,
    trong_luong DECIMAL(10,2),
    kich_thuoc VARCHAR(50),
    gia_tri DECIMAL(12,2),
    ngay_nhap DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ngay_xuat DATETIME,
    trang_thai VARCHAR(20) NOT NULL DEFAULT 'trong_kho' CHECK (trang_thai IN ('trong_kho', 'da_xuat', 'hu_hong')),
    vi_tri_luu_tru VARCHAR(30),
    ghi_chu TEXT,
    hinh_anh TEXT,
    ngay_tao DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ngay_cap_nhat DATETIME,
    FOREIGN KEY (ma_hop_dong) REFERENCES hop_dong(ma_hop_dong) ON DELETE CASCADE
);

-- Bảng thanh toán
CREATE TABLE IF NOT EXISTS thanh_toan (
    ma_thanh_toan VARCHAR(30) PRIMARY KEY,
    ma_hop_dong VARCHAR(20) NOT NULL,
    loai_phi VARCHAR(20) NOT NULL CHECK (loai_phi IN ('tien_coc', 'thue_thang', 'phu_phi', 'phi_phat')),
    so_tien DECIMAL(12,2) NOT NULL,
    ky_thanh_toan VARCHAR(20),
    ngay_den_han DATE NOT NULL,
    ngay_thanh_toan DATE,
    phuong_thuc VARCHAR(20) NOT NULL,
    so_giao_dich VARCHAR(50),
    trang_thai VARCHAR(20) NOT NULL DEFAULT 'chua_thanh_toan' CHECK (trang_thai IN ('da_thanh_toan', 'chua_thanh_toan', 'qua_han')),
    phi_phat DECIMAL(12,2) NOT NULL DEFAULT 0,
    ghi_chu TEXT,
    nguoi_thu VARCHAR(100),
    ngay_tao DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ngay_cap_nhat DATETIME,
    FOREIGN KEY (ma_hop_dong) REFERENCES hop_dong(ma_hop_dong)
);

-- Bảng nhân viên
CREATE TABLE IF NOT EXISTS nhan_vien (
    ma_nhan_vien VARCHAR(20) PRIMARY KEY,
    ho_ten VARCHAR(200) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    so_dien_thoai VARCHAR(20),
    vai_tro VARCHAR(20) NOT NULL CHECK (vai_tro IN ('quan_tri', 'kinh_doanh', 'kho', 'ke_toan')),
    tai_khoan VARCHAR(50) UNIQUE NOT NULL,
    mat_khau VARCHAR(255) NOT NULL,
    trang_thai VARCHAR(20) NOT NULL DEFAULT 'hoat_dong',
    ngay_tao DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ngay_cap_nhat DATETIME,
    lan_dang_nhap_cuoi DATETIME
);

-- Bảng system log
CREATE TABLE IF NOT EXISTS system_log (
    ma_log INTEGER PRIMARY KEY AUTOINCREMENT,
    thoi_gian DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ma_nhan_vien VARCHAR(20),
    hanh_dong VARCHAR(20) NOT NULL CHECK (hanh_dong IN ('THEM', 'SUA', 'XOA', 'DANG_NHAP', 'DANG_XUAT')),
    ban_ghi VARCHAR(100) NOT NULL,
    gia_tri_cu TEXT,
    gia_tri_moi TEXT,
    ip_address VARCHAR(45),
    ghi_chu TEXT,
    FOREIGN KEY (ma_nhan_vien) REFERENCES nhan_vien(ma_nhan_vien) ON DELETE SET NULL
);

-- Bảng báo cáo
CREATE TABLE IF NOT EXISTS bao_cao (
    ma_bao_cao VARCHAR(30) PRIMARY KEY,
    loai_bao_cao VARCHAR(50) NOT NULL,
    ngay_bat_dau DATE NOT NULL,
    ngay_ket_thuc DATE NOT NULL,
    ngay_tao DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    nguoi_tao VARCHAR(20),
    du_lieu TEXT,
    file_path VARCHAR(500),
    trang_thai VARCHAR(20) NOT NULL DEFAULT 'hoan_thanh',
    ghi_chu TEXT,
    FOREIGN KEY (nguoi_tao) REFERENCES nhan_vien(ma_nhan_vien) ON DELETE SET NULL
);

-- ============================================================================
-- INDEXES
-- ============================================================================

-- Khach Hang
CREATE INDEX IF NOT EXISTS idx_khach_hang_so_dien_thoai ON khach_hang(so_dien_thoai);
CREATE INDEX IF NOT EXISTS idx_khach_hang_email ON khach_hang(email);
CREATE INDEX IF NOT EXISTS idx_khach_hang_trang_thai ON khach_hang(trang_thai);

-- Kho
CREATE INDEX IF NOT EXISTS idx_kho_ten_kho ON kho(ten_kho);
CREATE INDEX IF NOT EXISTS idx_kho_trang_thai ON kho(trang_thai);

-- Vi Tri
CREATE INDEX IF NOT EXISTS idx_vi_tri_ma_kho ON vi_tri(ma_kho);
CREATE INDEX IF NOT EXISTS idx_vi_tri_trang_thai ON vi_tri(trang_thai);
CREATE INDEX IF NOT EXISTS idx_vi_tri_khu_vuc ON vi_tri(khu_vuc, hang, tang);

-- Hop Dong
CREATE INDEX IF NOT EXISTS idx_hop_dong_ma_khach_hang ON hop_dong(ma_khach_hang);
CREATE INDEX IF NOT EXISTS idx_hop_dong_ma_vi_tri ON hop_dong(ma_vi_tri);
CREATE INDEX IF NOT EXISTS idx_hop_dong_ngay_ket_thuc ON hop_dong(ngay_ket_thuc);
CREATE INDEX IF NOT EXISTS idx_hop_dong_trang_thai ON hop_dong(trang_thai);
CREATE INDEX IF NOT EXISTS idx_hop_dong_kh_trang_thai ON hop_dong(ma_khach_hang, trang_thai);

-- Hang Hoa
CREATE INDEX IF NOT EXISTS idx_hang_hoa_ma_hop_dong ON hang_hoa(ma_hop_dong);
CREATE INDEX IF NOT EXISTS idx_hang_hoa_ten_hang ON hang_hoa(ten_hang);
CREATE INDEX IF NOT EXISTS idx_hang_hoa_trang_thai ON hang_hoa(trang_thai);
CREATE INDEX IF NOT EXISTS idx_hang_hoa_ngay_nhap ON hang_hoa(ngay_nhap);
CREATE INDEX IF NOT EXISTS idx_hang_hoa_hd_trang_thai ON hang_hoa(ma_hop_dong, trang_thai);

-- Thanh Toan
CREATE INDEX IF NOT EXISTS idx_thanh_toan_ma_hop_dong ON thanh_toan(ma_hop_dong);
CREATE INDEX IF NOT EXISTS idx_thanh_toan_ngay_den_han ON thanh_toan(ngay_den_han);
CREATE INDEX IF NOT EXISTS idx_thanh_toan_trang_thai ON thanh_toan(trang_thai);
CREATE INDEX IF NOT EXISTS idx_thanh_toan_hd_trang_thai ON thanh_toan(ma_hop_dong, trang_thai);

-- Nhan Vien
CREATE INDEX IF NOT EXISTS idx_nhan_vien_tai_khoan ON nhan_vien(tai_khoan);
CREATE INDEX IF NOT EXISTS idx_nhan_vien_email ON nhan_vien(email);
CREATE INDEX IF NOT EXISTS idx_nhan_vien_vai_tro ON nhan_vien(vai_tro);

-- System Log
CREATE INDEX IF NOT EXISTS idx_system_log_thoi_gian ON system_log(thoi_gian);
CREATE INDEX IF NOT EXISTS idx_system_log_ma_nhan_vien ON system_log(ma_nhan_vien);
CREATE INDEX IF NOT EXISTS idx_system_log_hanh_dong ON system_log(hanh_dong);
CREATE INDEX IF NOT EXISTS idx_system_log_ban_ghi ON system_log(ban_ghi);

-- Bao Cao
CREATE INDEX IF NOT EXISTS idx_bao_cao_loai_bao_cao ON bao_cao(loai_bao_cao);
CREATE INDEX IF NOT EXISTS idx_bao_cao_ngay_tao ON bao_cao(ngay_tao);

-- ============================================================================
-- VIEWS
-- ============================================================================

-- View: Hợp đồng sắp hết hạn
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
ORDER BY hd.ngay_ket_thuc ASC;

-- View: Công nợ chưa thanh toán
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
ORDER BY tt.ngay_den_han ASC;

-- View: Tỷ lệ lấp đầy kho
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
GROUP BY k.ma_kho, k.ten_kho, k.dien_tich, k.suc_chua;

-- ============================================================================
-- SAMPLE DATA
-- ============================================================================

-- Admin user (password: admin123 - bcrypt hash)
INSERT OR IGNORE INTO nhan_vien (ma_nhan_vien, ho_ten, email, vai_tro, tai_khoan, mat_khau)
VALUES ('NV001', 'Administrator', 'admin@warehouse.local', 'quan_tri', 'admin', 
        '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYILp92S.0i');

-- Sample warehouse
INSERT OR IGNORE INTO kho (ma_kho, ten_kho, dia_chi, dien_tich, suc_chua)
VALUES ('KHO001', 'Kho A - Quận 7', '123 Đường Nguyễn Văn Linh, Quận 7, TP.HCM', 1000.0, 5000.0);

-- Sample storage locations
INSERT OR IGNORE INTO vi_tri (ma_vi_tri, ma_kho, khu_vuc, hang, tang, dien_tich, gia_thue)
VALUES 
    ('K01-A-01-01', 'KHO001', 'A', '01', 1, 50.0, 150000.0),
    ('K01-A-01-02', 'KHO001', 'A', '01', 1, 75.0, 150000.0);

-- Sample customer
INSERT OR IGNORE INTO khach_hang (ma_khach_hang, ho_ten, loai_khach, so_dien_thoai, email, dia_chi)
VALUES ('KH001', 'Nguyễn Văn A', 'ca_nhan', '0901234567', 'nguyenvana@email.com', 
        '456 Đường ABC, Quận 1, TP.HCM');

-- ============================================================================
-- END OF SCHEMA
-- ============================================================================
