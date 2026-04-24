# Reference UI - Module Kho Hàng

## 📋 Tổng quan

Tài liệu này mapping các giao diện mẫu từ `stitch_ui_analysis_system/` sang các views đã implement trong project.

---

## 🏭 Kho Hàng References

### 1. **danh_sach_kho/** - Danh sách kho

**Reference Files:**
- `screen.png` - Ảnh chụp giao diện
- `code.html` - HTML code

**Đã implement trong:** `src/gui/views/kho_view.py`

**Features đã tích hợp:**
| Reference Feature | Status | Implementation |
|------------------|--------|----------------|
| Danh sách kho (table) | ✅ | DataTable với 8 columns |
| Statistics bar | ✅ | Tổng kho, Hoạt động, Lấp đầy TB |
| Search box | ✅ | Tìm theo tên, mã, địa chỉ |
| Filter theo trạng thái | ✅ | ComboBox: Tất cả/Hoạt động/Bảo trì/Ngừng |
| Toolbar (Thêm, Sửa, Xóa) | ✅ | DataTableWithToolbar |
| Row selection | ✅ | Signal `kho_selected` |
| Double-click to edit | ✅ | `_on_row_double_clicked` |

**Screenshot Comparison:**
```
Reference: danh_sach_kho/screen.png
Implemented: KhoView (kho_view.py)
```

---

### 2. **chi_tiet_kho/** - Chi tiết kho

**Reference Files:**
- `screen.png`
- `code.html`

**Đã implement trong:** 
- `src/gui/views/kho_view.py` (info label)
- `src/services/kho_service.py` (get_available_capacity)

**Features đã tích hợp:**
| Reference Feature | Status | Implementation |
|------------------|--------|----------------|
| Thông tin kho | ✅ | Kho model với đầy đủ fields |
| Danh sách vị trí | ✅ | ViTriService.get_vi_tri_by_kho() |
| Tỷ lệ lấp đầy | ✅ | KhoService.calculate_fill_rate() |
| Sức chứa còn lại | ✅ | KhoService.get_available_capacity() |

**Planned:** Chi tiết kho full view (Phase 4.4 Detail View)

---

### 3. **thong_tin_kho_hang/** - Thông tin kho hàng

**Reference Files:**
- `screen.png`
- `code.html`

**Đã implement trong:** 
- `src/gui/views/dashboard_view.py`
- `src/services/kho_service.py`

**Features đã tích hợp:**
| Reference Feature | Status | Implementation |
|------------------|--------|----------------|
| Thống kê tổng quan | ✅ | Dashboard metrics cards |
| Fill rate visualization | ✅ | Progress bars với color coding |
| Cảnh báo kho quá tải | ✅ | Alerts section (>90% fill rate) |
| Danh sách vị trí | ✅ | ViTriView |

---

## 📦 Vị Trí References

### 4. **Position Management** (không có folder riêng)

**Đã implement trong:** `src/gui/views/vi_tri_view.py`

**Features tạo mới:**
| Feature | Status | Implementation |
|---------|--------|----------------|
| Kho selector | ✅ | Dropdown chọn kho |
| Statistics bar | ✅ | Tổng, Trống, Đã thuê, Tỷ lệ |
| Search vị trí | ✅ | Tìm theo mã, khu vực, hàng |
| Filter theo status | ✅ | Trống/Đã thuê/Bảo trì |
| Auto-generate mã VT | ✅ | Format: KHO001-A-01-01-001 |

---

## 📊 Dashboard References

### 5. **Dashboard Integration** (tổng hợp từ nhiều references)

**Đã implement trong:** `src/gui/views/dashboard_view.py`

**Features đã tích hợp:**
| Reference Feature | Source | Implementation |
|------------------|--------|----------------|
| Key metrics cards | danh_sach_kho | 4 cards: Kho, Vị trí, Trống, % |
| Fill rate chart | thong_tin_kho_hang | Progress bar + legend |
| Overcrowded alerts | chi_tiet_kho | Alert cards >90% |
| Warehouse list | danh_sach_kho | List với progress bars |

---

## 🎨 Design System Integration

### Colors
```css
/* Notion-inspired color palette */
Primary Blue: #1976d2    /* Actions, links */
Success Green: #1aae39   /* Available, active */
Warning Orange: #ff9800  /* Fill rate, rented */
Danger Red: #f44336     /* Overcrowded, alerts */
Warm Gray: #f6f5f4      /* Backgrounds */
```

### Typography
```css
Title: 24-28px, weight 700
Subtitle: 20px, weight 600
Body: 14-16px, weight 400-500
Metrics: 32px, weight 700
```

### Components
- **Cards:** Border-radius 8-12px, subtle shadows
- **Progress Bars:** Color-coded, rounded
- **Buttons:** Pill-shaped, icon + text
- **Tables:** Alternating row colors, hover effects

---

## ✅ Implementation Status

| Reference | Folder | Implemented In | Status |
|-----------|--------|----------------|--------|
| Danh sách kho | danh_sach_kho/ | kho_view.py | ✅ 100% |
| Chi tiết kho | chi_tiet_kho/ | kho_service.py | ✅ 80% |
| Thông tin kho | thong_tin_kho_hang/ | dashboard_view.py | ✅ 90% |
| Vị trí (new) | - | vi_tri_view.py | ✅ 100% |
| Dashboard | (tổng hợp) | dashboard_view.py | ✅ 95% |

---

## 📝 Notes

### Đã làm tốt:
- ✅ Statistics bar với real-time data
- ✅ Color-coded progress bars
- ✅ Search & filter functionality
- ✅ Auto-refresh dashboard (30s)
- ✅ Overcrowded alerts

### Có thể cải thiện:
- ⏳ Chi tiết kho full view (chưa có)
- ⏳ Import/Export slips (phieu_nhap_kho, phieu_xuat_kho)
- ⏳ Activity timeline
- ⏳ Export to PDF/Excel cho dashboard

---

## 🚀 Next Steps

### Phase 4.7 - Forms:
- [ ] Form thêm/sửa kho
- [ ] Form thêm/sửa vị trí
- [ ] Form import/export kho

### Phase 4.8 - Features:
- [ ] Export dashboard to PDF
- [ ] Print position labels
- [ ] Batch operations

### Phase 4.9 - Testing:
- [ ] Unit tests for services
- [ ] GUI tests
- [ ] Integration tests

---

**Cập nhật:** 23/04/2026  
**Nhóm 12 - Lập trình Python**  
**Module:** Kho Hàng (Phase 4)
