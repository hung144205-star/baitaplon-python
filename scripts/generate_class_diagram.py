"""
Script tạo file class diagram cho hệ thống quản lý kho
Định dạng: Draw.io XML (app.diagrams.net)
"""
import base64
import zlib
import re
import urllib.parse

# Định nghĩa các class model
models = [
    {
        "name": "«abstract»\nBaseModel",
        "fields": "+ ngay_tao: DateTime\n+ ngay_cap_nhat: DateTime",
        "methods": "+ to_dict() → dict\n+ to_json() → str",
        "x": 370, "y": 40, "width": 180, "height": 120,
        "style": "swimlane;html=1;fontStyle=2;align=center;verticalAlign=top;childLayout=stackLayout;horizontal=1;startSize=32;horizontalStack=0;resizeParent=1;resizeLast=0;collapsible=1;marginBottom=0;swimlaneFillColor=#E8F4FD;rounded=1;shadow=0;comic=0;labelBackgroundColor=none;strokeWidth=2;fillColor=#DAEEF3;fontFamily=Verdana;fontSize=11;fontColor=#444444;strokeColor=#333333;"
    },
    {
        "name": "KhachHang\n(bang: khach_hang)",
        "fields": "+ ma_khach_hang: str (PK)\n+ ho_ten: str\n+ loai_khach: LoaiKhachEnum\n+ so_dien_thoai: str\n+ email: str (unique)\n+ dia_chi: str\n+ ma_so_thue: str\n+ ngay_dang_ky: date\n+ trang_thai: TrangThaiKHEnum",
        "methods": "+ __repr__() → str",
        "x": 50, "y": 220, "width": 210, "height": 290,
        "style": "swimlane;html=1;fontStyle=1;align=center;verticalAlign=top;childLayout=stackLayout;horizontal=1;startSize=32;horizontalStack=0;resizeParent=1;resizeLast=0;collapsible=1;marginBottom=0;swimlaneFillColor=#ffffff;rounded=1;shadow=0;comic=0;labelBackgroundColor=none;strokeWidth=1;fillColor=#F5F5F5;fontFamily=Verdana;fontSize=11;fontColor=#444444;strokeColor=#666666;"
    },
    {
        "name": "Kho\n(bang: kho)",
        "fields": "+ ma_kho: str (PK)\n+ ten_kho: str\n+ dia_chi: str\n+ dien_tich: float\n+ suc_chua: float\n+ da_su_dung: float\n+ trang_thai: TrangThaiKhoEnum",
        "methods": "+ ty_le_lap_day() → float\n+ dung_tich_con_lai() → float",
        "x": 370, "y": 220, "width": 180, "height": 280,
        "style": "swimlane;html=1;fontStyle=1;align=center;verticalAlign=top;childLayout=stackLayout;horizontal=1;startSize=32;horizontalStack=0;resizeParent=1;resizeLast=0;collapsible=1;marginBottom=0;swimlaneFillColor=#ffffff;rounded=1;shadow=0;comic=0;labelBackgroundColor=none;strokeWidth=1;fillColor=#F5F5F5;fontFamily=Verdana;fontSize=11;fontColor=#444444;strokeColor=#666666;"
    },
    {
        "name": "LoaiHang\n(bang: loai_hang)",
        "fields": "+ ma_loai: str (PK)\n+ ten_loai: str\n+ mo_ta: text\n+ ghi_chu: text",
        "methods": "",
        "x": 660, "y": 220, "width": 180, "height": 160,
        "style": "swimlane;html=1;fontStyle=1;align=center;verticalAlign=top;childLayout=stackLayout;horizontal=1;startSize=32;horizontalStack=0;resizeParent=1;resizeLast=0;collapsible=1;marginBottom=0;swimlaneFillColor=#ffffff;rounded=1;shadow=0;comic=0;labelBackgroundColor=none;strokeWidth=1;fillColor=#F5F5F5;fontFamily=Verdana;fontSize=11;fontColor=#444444;strokeColor=#666666;"
    },
    {
        "name": "HopDong\n(bang: hop_dong)",
        "fields": "+ ma_hop_dong: str (PK)\n+ ma_khach_hang: str (FK)\n+ ma_vi_tri: str (FK)\n+ ngay_bat_dau: date\n+ ngay_ket_thuc: date\n+ gia_thue: float\n+ tien_coc: float\n+ phuong_thuc_thanh_toan: str\n+ dieu_khoan: text\n+ trang_thai: TrangThaiHDEnum",
        "methods": "+ __repr__() → str",
        "x": 50, "y": 580, "width": 220, "height": 330,
        "style": "swimlane;html=1;fontStyle=1;align=center;verticalAlign=top;childLayout=stackLayout;horizontal=1;startSize=32;horizontalStack=0;resizeParent=1;resizeLast=0;collapsible=1;marginBottom=0;swimlaneFillColor=#ffffff;rounded=1;shadow=0;comic=0;labelBackgroundColor=none;strokeWidth=1;fillColor=#FFF8E1;fontFamily=Verdana;fontSize=11;fontColor=#444444;strokeColor=#666666;"
    },
    {
        "name": "ViTri\n(bang: vi_tri)",
        "fields": "+ ma_vi_tri: str (PK)\n+ ma_kho: str (FK)\n+ khu_vuc: str\n+ hang: str\n+ tang: int\n+ dien_tich: float\n+ gia_thue: float\n+ suc_chua: float\n+ trang_thai: TrangThaiViTriEnum",
        "methods": "+ __repr__() → str",
        "x": 400, "y": 580, "width": 190, "height": 300,
        "style": "swimlane;html=1;fontStyle=1;align=center;verticalAlign=top;childLayout=stackLayout;horizontal=1;startSize=32;horizontalStack=0;resizeParent=1;resizeLast=0;collapsible=1;marginBottom=0;swimlaneFillColor=#ffffff;rounded=1;shadow=0;comic=0;labelBackgroundColor=none;strokeWidth=1;fillColor=#FFF8E1;fontFamily=Verdana;fontSize=11;fontColor=#444444;strokeColor=#666666;"
    },
    {
        "name": "HangHoa\n(bang: hang_hoa)",
        "fields": "+ ma_hang_hoa: str (PK)\n+ ma_hop_dong: str (FK)\n+ ten_hang: str\n+ loai_hang: str\n+ so_luong: int\n+ don_vi: str\n+ trong_luong: float\n+ kich_thuoc: str\n+ gia_tri: float\n+ ngay_nhap: datetime\n+ ngay_xuat: datetime\n+ trang_thai: TrangThaiHHEnum\n+ vi_tri_luu_tru: str",
        "methods": "+ __repr__() → str",
        "x": 690, "y": 580, "width": 200, "height": 370,
        "style": "swimlane;html=1;fontStyle=1;align=center;verticalAlign=top;childLayout=stackLayout;horizontal=1;startSize=32;horizontalStack=0;resizeParent=1;resizeLast=0;collapsible=1;marginBottom=0;swimlaneFillColor=#ffffff;rounded=1;shadow=0;comic=0;labelBackgroundColor=none;strokeWidth=1;fillColor=#FFF8E1;fontFamily=Verdana;fontSize=11;fontColor=#444444;strokeColor=#666666;"
    },
    {
        "name": "ThanhToan\n(bang: thanh_toan)",
        "fields": "+ ma_thanh_toan: str (PK)\n+ ma_hop_dong: str (FK)\n+ loai_phi: LoaiPhiEnum\n+ so_tien: float\n+ ky_thanh_toan: str\n+ ngay_den_han: date\n+ ngay_thanh_toan: date\n+ phuong_thuc: str\n+ trang_thai: TrangThaiTTEnum\n+ phi_phat: float",
        "methods": "+ __repr__() → str",
        "x": 50, "y": 980, "width": 210, "height": 320,
        "style": "swimlane;html=1;fontStyle=1;align=center;verticalAlign=top;childLayout=stackLayout;horizontal=1;startSize=32;horizontalStack=0;resizeParent=1;resizeLast=0;collapsible=1;marginBottom=0;swimlaneFillColor=#ffffff;rounded=1;shadow=0;comic=0;labelBackgroundColor=none;strokeWidth=1;fillColor=#E8F5E9;fontFamily=Verdana;fontSize=11;fontColor=#444444;strokeColor=#666666;"
    },
    {
        "name": "NhanVien\n(bang: nhan_vien)",
        "fields": "+ ma_nhan_vien: str (PK)\n+ ho_ten: str\n+ email: str (unique)\n+ so_dien_thoai: str\n+ vai_tro: VaiTroNhanVienEnum\n+ tai_khoan: str (unique)\n+ mat_khau: str\n+ trang_thai: TrangThaiNhanVienEnum",
        "methods": "+ __repr__() → str",
        "x": 380, "y": 980, "width": 200, "height": 270,
        "style": "swimlane;html=1;fontStyle=1;align=center;verticalAlign=top;childLayout=stackLayout;horizontal=1;startSize=32;horizontalStack=0;resizeParent=1;resizeLast=0;collapsible=1;marginBottom=0;swimlaneFillColor=#ffffff;rounded=1;shadow=0;comic=0;labelBackgroundColor=none;strokeWidth=1;fillColor=#E8F5E9;fontFamily=Verdana;fontSize=11;fontColor=#444444;strokeColor=#666666;"
    },
    {
        "name": "BaoCao\n(bang: bao_cao)",
        "fields": "+ ma_bao_cao: str (PK)\n+ nguoi_tao: str (FK)\n+ loai_bao_cao: str\n+ ngay_bat_dau: date\n+ ngay_ket_thuc: date\n+ du_lieu: text\n+ file_path: str\n+ trang_thai: str\n+ ghi_chu: text",
        "methods": "+ __repr__() → str",
        "x": 690, "y": 1020, "width": 190, "height": 270,
        "style": "swimlane;html=1;fontStyle=1;align=center;verticalAlign=top;childLayout=stackLayout;horizontal=1;startSize=32;horizontalStack=0;resizeParent=1;resizeLast=0;collapsible=1;marginBottom=0;swimlaneFillColor=#ffffff;rounded=1;shadow=0;comic=0;labelBackgroundColor=none;strokeWidth=1;fillColor=#E8F5E9;fontFamily=Verdana;fontSize=11;fontColor=#444444;strokeColor=#666666;"
    },
    {
        "name": "SystemLog\n(bang: system_log)",
        "fields": "+ ma_log: int (PK, auto)\n+ ma_nhan_vien: str (FK)\n+ thoi_gian: datetime\n+ hanh_dong: HanhDongLogEnum\n+ ban_ghi: str\n+ gia_tri_cu: text\n+ gia_tri_moi: text\n+ ip_address: str\n+ ghi_chu: text",
        "methods": "+ __repr__() → str",
        "x": 690, "y": 1360, "width": 200, "height": 270,
        "style": "swimlane;html=1;fontStyle=1;align=center;verticalAlign=top;childLayout=stackLayout;horizontal=1;startSize=32;horizontalStack=0;resizeParent=1;resizeLast=0;collapsible=1;marginBottom=0;swimlaneFillColor=#ffffff;rounded=1;shadow=0;comic=0;labelBackgroundColor=none;strokeWidth=1;fillColor=#F3E5F5;fontFamily=Verdana;fontSize=11;fontColor=#444444;strokeColor=#666666;"
    },
]


def build_enum_box():
    """Tạo box enum chính"""
    enum_text = ("«enumeration»\nCacEnum\n\n"
                 "TrangThaiHDEnum:\nHIEU_LUC | HET_HAN | CHAM_DUT | GIA_HAN\n\n"
                 "TrangThaiTTEnum:\nDA_THANH_TOAN | CHUA_THANH_TOAN | QUA_HAN\n\n"
                 "TrangThaiViTriEnum:\nTRONG | DA_THUE | BAO_TRI\n\n"
                 "TrangThaiKhoEnum:\nHOAT_DONG | BAO_TRI | NGUNG\n\n"
                 "LoaiKhachEnum:\nCA_NHAN | DOANH_NGHIEP\n\n"
                 "TrangThaiKHEnum:\nHOAT_DONG | TAM_KHOA | DA_XOA\n\n"
                 "LoaiPhiEnum:\nTIEN_COC | THUE_THANG | PHU_PHI | PHI_PHAT\n\n"
                 "TrangThaiHHEnum:\nTRONG_KHO | DA_XUAT\n\n"
                 "VaiTroNhanVienEnum:\nQUAN_TRI | KINH_DOANH | KHO | KE_TOAN\n\n"
                 "TrangThaiNhanVienEnum:\nHOAT_DONG | NGUNG_HOAT_DONG\n\n"
                 "HanhDongLogEnum:\nTHEM | SUA | XOA | DANG_NHAP | DANG_XUAT")
    return {
        "name": enum_text,
        "x": 1000, "y": 220, "width": 340, "height": 450,
        "style": "swimlane;html=1;fontStyle=0;align=left;verticalAlign=top;childLayout=stackLayout;horizontal=1;startSize=24;horizontalStack=0;resizeParent=1;resizeLast=0;collapsible=1;marginBottom=0;swimlaneFillColor=#FEF9E7;rounded=1;shadow=0;comic=0;labelBackgroundColor=none;strokeWidth=1;fillColor=#FFFDE7;fontFamily=Consolas;fontSize=9;fontColor=#444444;strokeColor=#999999;"
    }


# Relationships (edges) between classes
# Format: [source_id, target_id, style, label]
# source/target are 0-based indexes into models list
relationships = [
    # Inheritance: BaseModel -> all models (using dashed arrows with hollow triangle)
    # Use route points to spread inheritance lines
    # Target model x-positions: 1=50, 2=370, 3=660, 4=50, 5=400, 6=690, 7=50, 8=380, 9=690, 10=690
    # Routes split into left/middle/right groups
    # Group L (target x ~50-200): KhachHang(1), HopDong(4), ThanhToan(7)
    {"from": 0, "to": 1, "label": "", "style": "edgeStyle=orthogonalEdgeStyle;html=1;rounded=0;dashed=1;startArrow=none;startFill=0;endArrow=block;endFill=0;endSize=12;fontFamily=Verdana;fontSize=10;strokeColor=#333333;",
     "points": [[180,180],[120,180],[120,220]]},
    # Group LM (target x ~370-400): Kho(2), ViTri(5), NhanVien(8)
    {"from": 0, "to": 2, "label": "", "style": "edgeStyle=orthogonalEdgeStyle;html=1;rounded=0;dashed=1;startArrow=none;startFill=0;endArrow=block;endFill=0;endSize=12;fontFamily=Verdana;fontSize=10;strokeColor=#333333;",
     "points": [[370,180],[370,180]]},
    # Group RM (target x ~660): LoaiHang(3)
    {"from": 0, "to": 3, "label": "", "style": "edgeStyle=orthogonalEdgeStyle;html=1;rounded=0;dashed=1;startArrow=none;startFill=0;endArrow=block;endFill=0;endSize=12;fontFamily=Verdana;fontSize=10;strokeColor=#333333;",
     "points": [[660,160],[660,220]]},
    # Group L -> HopDong(4) - go down through left area
    {"from": 0, "to": 4, "label": "", "style": "edgeStyle=orthogonalEdgeStyle;html=1;rounded=0;dashed=1;startArrow=none;startFill=0;endArrow=block;endFill=0;endSize=12;fontFamily=Verdana;fontSize=10;strokeColor=#333333;",
     "points": [[190,200],[100,200],[100,580]]},
    # Group LM -> ViTri(5)
    {"from": 0, "to": 5, "label": "", "style": "edgeStyle=orthogonalEdgeStyle;html=1;rounded=0;dashed=1;startArrow=none;startFill=0;endArrow=block;endFill=0;endSize=12;fontFamily=Verdana;fontSize=10;strokeColor=#333333;",
     "points": [[380,200],[420,200],[420,580]]},
    # Group RM -> HangHoa(6)
    {"from": 0, "to": 6, "label": "", "style": "edgeStyle=orthogonalEdgeStyle;html=1;rounded=0;dashed=1;startArrow=none;startFill=0;endArrow=block;endFill=0;endSize=12;fontFamily=Verdana;fontSize=10;strokeColor=#333333;",
     "points": [[670,200],[750,200],[750,580]]},
    # Group L -> ThanhToan(7) - further down
    {"from": 0, "to": 7, "label": "", "style": "edgeStyle=orthogonalEdgeStyle;html=1;rounded=0;dashed=1;startArrow=none;startFill=0;endArrow=block;endFill=0;endSize=12;fontFamily=Verdana;fontSize=10;strokeColor=#333333;",
     "points": [[170,210],[80,210],[80,980]]},
    # Group LM -> NhanVien(8)
    {"from": 0, "to": 8, "label": "", "style": "edgeStyle=orthogonalEdgeStyle;html=1;rounded=0;dashed=1;startArrow=none;startFill=0;endArrow=block;endFill=0;endSize=12;fontFamily=Verdana;fontSize=10;strokeColor=#333333;",
     "points": [[390,210],[440,210],[440,980]]},
    # Group RM -> BaoCao(9) - via right side
    {"from": 0, "to": 9, "label": "", "style": "edgeStyle=orthogonalEdgeStyle;html=1;rounded=0;dashed=1;startArrow=none;startFill=0;endArrow=block;endFill=0;endSize=12;fontFamily=Verdana;fontSize=10;strokeColor=#333333;",
     "points": [[680,210],[780,210],[780,1020]]},
    # Group RM -> SystemLog(10)
    {"from": 0, "to": 10, "label": "", "style": "edgeStyle=orthogonalEdgeStyle;html=1;rounded=0;dashed=1;startArrow=none;startFill=0;endArrow=block;endFill=0;endSize=12;fontFamily=Verdana;fontSize=10;strokeColor=#333333;",
     "points": [[700,220],[800,220],[800,1360]]},
    # Association relationships
    # Kho 1 -- N ViTri
    {"from": 2, "to": 5, "label": "1 - N", "style": "edgeStyle=orthogonalEdgeStyle;html=1;rounded=0;startArrow=none;startFill=0;endArrow=openThin;endFill=0;endSize=12;fontFamily=Verdana;fontSize=10;strokeColor=#666666;"},
    # KhachHang 1 -- N HopDong
    {"from": 1, "to": 4, "label": "1 - N", "style": "edgeStyle=orthogonalEdgeStyle;html=1;rounded=0;startArrow=none;startFill=0;endArrow=openThin;endFill=0;endSize=12;fontFamily=Verdana;fontSize=10;strokeColor=#666666;"},
    # ViTri 1 -- N HopDong
    {"from": 5, "to": 4, "label": "1 - N", "style": "edgeStyle=orthogonalEdgeStyle;html=1;rounded=0;startArrow=none;startFill=0;endArrow=openThin;endFill=0;endSize=12;fontFamily=Verdana;fontSize=10;strokeColor=#666666;"},
    # HopDong 1 -- N HangHoa
    {"from": 4, "to": 6, "label": "1 - N", "style": "edgeStyle=orthogonalEdgeStyle;html=1;rounded=0;startArrow=none;startFill=0;endArrow=openThin;endFill=0;endSize=12;fontFamily=Verdana;fontSize=10;strokeColor=#666666;"},
    # HopDong 1 -- N ThanhToan
    {"from": 4, "to": 7, "label": "1 - N", "style": "edgeStyle=orthogonalEdgeStyle;html=1;rounded=0;startArrow=none;startFill=0;endArrow=openThin;endFill=0;endSize=12;fontFamily=Verdana;fontSize=10;strokeColor=#666666;"},
    # NhanVien 1 -- N BaoCao
    {"from": 8, "to": 9, "label": "1 - N", "style": "edgeStyle=orthogonalEdgeStyle;html=1;rounded=0;startArrow=none;startFill=0;endArrow=openThin;endFill=0;endSize=12;fontFamily=Verdana;fontSize=10;strokeColor=#666666;"},
    # NhanVien 1 -- N SystemLog
    {"from": 8, "to": 10, "label": "1 - N", "style": "edgeStyle=orthogonalEdgeStyle;html=1;rounded=0;startArrow=none;startFill=0;endArrow=openThin;endFill=0;endSize=12;fontFamily=Verdana;fontSize=10;strokeColor=#666666;"},
]


def escape_xml(s):
    """Escape XML special characters in the value string"""
    s = s.replace("&", "&amp;")
    s = s.replace("<", "&lt;")
    s = s.replace(">", "&gt;")
    s = s.replace("\"", "&quot;")
    s = s.replace("'", "&apos;")
    # Replace newlines with drawio line break format
    s = s.replace("\n", "&#xa;")
    return s


def build_mxgraph_xml():
    """Build the mxGraphModel XML"""
    parts = []
    parts.append('<mxGraphModel dx="2054" dy="1109" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1600" pageHeight="1800" math="0" shadow="0">')
    parts.append('<root>')
    parts.append('<mxCell id="0"/>')
    parts.append('<mxCell id="1" parent="0"/>')
    
    # Add model classes
    model_ids = []
    for i, m in enumerate(models):
        model_id = f"model-{i}"
        model_ids.append(model_id)
        
        # Parse fields and methods
        fields = m["fields"].split("\n") if m["fields"] else []
        methods = m["methods"].split("\n") if m["methods"] else []
        
        field_count = len(fields)
        method_count = len(methods)
        has_separator = field_count > 0 and method_count > 0
        total_rows = field_count + method_count + (1 if has_separator else 0)
        
        # Calculate height based on field/method rows
        row_height = 22
        header_height = m.get("startSize", 32)
        total_height = header_height + (total_rows * row_height) + 8
        if total_height < m["height"]:
            total_height = m["height"]
        
        # Class header cell (swimlane)
        value_escaped = escape_xml(m["name"])
        style = m["style"]
        parts.append(f'<mxCell id="{model_id}" parent="1" style="{style}" value="{value_escaped}" vertex="1">')
        parts.append(f'<mxGeometry height="{total_height}" width="{m["width"]}" x="{m["x"]}" y="{m["y"]}" as="geometry"/>')
        parts.append('</mxCell>')
        
        y_offset = header_height
        
        # Add field rows
        for field_idx, field in enumerate(fields):
            cell_id = f"{model_id}-f{field_idx}"
            escaped_field = escape_xml(field)
            parts.append(f'<mxCell id="{cell_id}" parent="{model_id}" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;whiteSpace=wrap;overflow=hidden;rotatable=0;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;fontFamily=Consolas;fontSize=9;fontColor=#333333;" value="{escaped_field}" vertex="1">')
            parts.append(f'<mxGeometry height="{row_height}" width="{m["width"]}" y="{y_offset}" as="geometry"/>')
            parts.append('</mxCell>')
            y_offset += row_height
        
        # Separator line between fields and methods
        if has_separator:
            parts.append(f'<mxCell id="{model_id}-sep" parent="{model_id}" style="line;html=1;strokeWidth=1;fillColor=none;align=left;verticalAlign=middle;spacingTop=-1;spacingLeft=3;spacingRight=3;rotatable=0;labelPosition=right;points=[];portConstraint=eastwest;fontFamily=Verdana;fontSize=11;" value="" vertex="1">')
            parts.append(f'<mxGeometry height="8" width="{m["width"]}" y="{y_offset}" as="geometry"/>')
            parts.append('</mxCell>')
            y_offset += 8
        
        # Add method rows
        for method_idx, method in enumerate(methods):
            cell_id = f"{model_id}-m{method_idx}"
            escaped_method = escape_xml(method)
            parts.append(f'<mxCell id="{cell_id}" parent="{model_id}" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;whiteSpace=wrap;overflow=hidden;rotatable=0;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;fontFamily=Consolas;fontSize=9;fontColor=#555555;fontStyle=2;" value="{escaped_method}" vertex="1">')
            parts.append(f'<mxGeometry height="{row_height}" width="{m["width"]}" y="{y_offset}" as="geometry"/>')
            parts.append('</mxCell>')
            y_offset += row_height
    
    # Add the legend/title box
    title_escaped = escape_xml(
        "Class Diagram - He Thong Quan Ly Cho Thue Kho\n\n"
        "PK: Primary Key\nFK: Foreign Key\n\n"
        "1-N: Quan he mot nhieu\n"
        "Mo ta: cac model ORM chinh\n"
        "Nen: SQLAlchemy + SQLite"
    )
    parts.append('<mxCell id="title-box" parent="1" style="swimlane;html=1;fontStyle=1;align=left;verticalAlign=top;childLayout=stackLayout;horizontal=1;startSize=26;horizontalStack=0;resizeParent=1;resizeLast=0;collapsible=1;marginBottom=0;swimlaneFillColor=#FAFAFA;rounded=1;shadow=0;comic=0;labelBackgroundColor=none;strokeWidth=1;fillColor=#FAFAFA;fontFamily=Verdana;fontSize=11;fontColor=#666666;strokeColor=#CCCCCC;" vertex="1">')
    parts.append('<mxGeometry height="150" width="250" x="50" y="40" as="geometry"/>')
    parts.append('</mxCell>')
    # Text child for title box
    parts.append('<mxCell id="title-box-text" parent="title-box" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=top;spacingLeft=4;spacingRight=4;whiteSpace=wrap;overflow=hidden;rotatable=0;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;fontFamily=Verdana;fontSize=9;fontColor=#888888;" value="Class Diagram - He Thong Quan Ly Cho Thue Kho&#xa;&#xa;PK: Primary Key | FK: Foreign Key&#xa;1-N: Quan he mot - nhieu&#xa;Nen: SQLAlchemy + SQLite" vertex="1">')
    parts.append('<mxGeometry height="150" width="250" y="26" as="geometry"/>')
    parts.append('</mxCell>')
    
    # Add relationships (edges)
    for rel_idx, rel in enumerate(relationships):
        edge_id = f"edge-{rel_idx}"
        source_id = model_ids[rel["from"]]
        target_id = model_ids[rel["to"]]
        label = rel["label"]
        style = rel["style"]
        
        escaped_label = escape_xml(label)
        parts.append(f'<mxCell id="{edge_id}" edge="1" parent="1" source="{source_id}" style="{style}" target="{target_id}" value="{escaped_label}">')
        # Add waypoints if specified
        if "points" in rel and rel["points"]:
            points_xml = ''.join(f'<mxPoint x="{p[0]}" y="{p[1]}"/>' for p in rel["points"])
            parts.append(f'<mxGeometry relative="1" as="geometry"><Array as="points">{points_xml}</Array></mxGeometry>')
        else:
            parts.append('<mxGeometry relative="1" as="geometry"/>')
        parts.append('</mxCell>')
    
    # Add enum box
    enum_model = build_enum_box()
    enum_id = "model-enum"
    model_ids.append(enum_id)
    
    value_escaped = escape_xml(enum_model["name"])
    parts.append(f'<mxCell id="{enum_id}" parent="1" style="{enum_model["style"]}" value="{value_escaped}" vertex="1">')
    parts.append(f'<mxGeometry height="{enum_model["height"]}" width="{enum_model["width"]}" x="{enum_model["x"]}" y="{enum_model["y"]}" as="geometry"/>')
    parts.append('</mxCell>')
    
    parts.append('</root>')
    parts.append('</mxGraphModel>')
    
    return "\n".join(parts)


def encode_diagram(xml_content):
    """Encode mxGraphModel XML to base64 + raw deflate (drawio format)"""
    # URL encode the XML
    url_encoded = urllib.parse.quote(xml_content)
    # Compress with raw deflate (matching drawio template format)
    compressed = zlib.compress(url_encoded.encode('utf-8'))[2:-4]  # strip zlib header (2 bytes) and checksum (4 bytes)
    # Base64 encode
    b64 = base64.b64encode(compressed).decode('utf-8')
    return b64


def main():
    # Build the mxGraphModel XML
    xml_content = build_mxgraph_xml()
    
    # Encode to drawio format
    encoded = encode_diagram(xml_content)
    
    # Build the final mxfile
    mxfile = f'<?xml version="1.0" encoding="UTF-8"?>\n<mxfile host="app.diagrams.net"><diagram name="Page-1" id="class-diagram-warehouse">{encoded}</diagram></mxfile>'
    
    # Write to file
    output_path = "docs/diagram/class-diagram-systems.xml"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(mxfile)
    
    print(f"File saved to: {output_path}")
    
    # Verify by decoding back
    import re
    match = re.search(r'<diagram[^>]*>(.*?)</diagram>', mxfile, re.DOTALL)
    if match:
        encoded_back = match.group(1).strip()
        decoded_bytes = base64.b64decode(encoded_back)
        decompressed = zlib.decompress(decoded_bytes, -zlib.MAX_WBITS)
        decoded_xml = urllib.parse.unquote(decompressed.decode('utf-8'))
        print(f"Verification OK - decoded length: {len(decoded_xml)} chars")
        # Print first 200 chars
        print(f"First 200: {decoded_xml[:200]}")


if __name__ == "__main__":
    main()
