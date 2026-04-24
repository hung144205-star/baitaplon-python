# Reference UI - Module Hợp đồng

## 📋 Tổng quan

Tài liệu này mapping các giao diện mẫu từ `stitch_ui_analysis_system/` sang các views đã implement trong project Phase 5.

---

## 📄 Hợp đồng References

### 1. **danh_muc_hop_dong/** - Danh mục hợp đồng

**Reference Files:**
- `screen.png` - Ảnh chụp giao diện
- `code.html` - HTML code

**Đã implement trong:** `src/gui/views/hop_dong_view.py`

**Features đã tích hợp:**

| Reference Feature | Status | Implementation |
|------------------|--------|----------------|
| Danh sách hợp đồng (table) | ✅ | DataTable với 8 columns |
| Statistics bar | ✅ | Tổng, Hiệu lực, Sắp hết hạn, Hết hạn |
| Search box | ✅ | Tìm theo mã, KH, vị trí |
| Filter theo trạng thái | ✅ | 4 states (Hiệu lực/Hết hạn/Chấm dứt/Gia hạn) |
| Filter theo ngày | ✅ | Date range picker |
| Toolbar (Thêm, Sửa, Xóa) | ✅ | DataTableWithToolbar |
| Custom actions (Gia hạn, Chấm dứt) | ✅ | 2 custom buttons |
| Highlight sắp hết hạn | ✅ | ⚠️ indicator cho < 7 ngày |

**Screenshot Comparison:**
```
Reference: danh_muc_hop_dong/screen.png
Implemented: HopDongView (hop_dong_view.py)
```

**Columns mapping:**
| Reference Column | Implemented Column |
|-----------------|-------------------|
| Mã hợp đồng | Mã HĐ |
| Khách hàng | Khách Hàng |
| Vị trí | Vị Trí |
| Ngày bắt đầu | Ngày BĐ |
| Ngày kết thúc | Ngày KT |
| Giá thuê | Giá Thuê |
| Số ngày còn lại | Còn Lại |
| Trạng thái | Trạng Thái |

---

### 2. **thiet_lap_hop_dong/** - Thiết lập hợp đồng

**Reference Files:**
- `screen.png`
- `code.html`

**Đã implement trong:** `src/gui/forms/hop_dong_form.py`

**Features đã tích hợp:**

| Reference Feature | Status | Implementation |
|------------------|--------|----------------|
| Form thêm/sửa hợp đồng | ✅ | HopDongForm dialog |
| Mã hợp đồng (auto) | ✅ | Read-only, auto-generate |
| Khách hàng (dropdown) | ✅ | ComboBox searchable |
| Vị trí (dropdown) | ✅ | Filter TRỐNG only |
| Ngày bắt đầu (picker) | ✅ | QDateEdit with calendar |
| Ngày kết thúc (picker) | ✅ | QDateEdit with validation |
| Giá thuê (input) | ✅ | DoubleSpinBox |
| Tiền cọc (input) | ✅ | DoubleSpinBox |
| Phương thức TT | ✅ | ComboBox (4 options) |
| Điều khoản (textarea) | ✅ | QTextEdit |
| Auto-calculate duration | ✅ | Live summary label |
| Validation | ✅ | Live validation |

**Form Groups:**
| Group | Fields |
|-------|--------|
| Thông tin cơ bản | Mã HĐ, Khách hàng, Vị trí |
| Thời hạn | Ngày BĐ, Ngày KT |
| Tài chính | Giá thuê, Tiền cọc, Phương thức TT |
| Summary | Thời hạn, Tổng tiền |
| Điều khoản | Textarea |

---

### 3. **chi_tiet_hop_dong_thanh_toan/** - Chi tiết hợp đồng & thanh toán

**Reference Files:**
- `screen.png`
- `code.html`

**Đã implement trong:** `src/gui/views/hop_dong_detail_view.py`

**Features đã tích hợp:**

| Reference Feature | Status | Implementation |
|------------------|--------|----------------|
| Tabbed interface | ✅ | 4 tabs |
| Tab 1: Thông tin HĐ | ✅ | Full contract info |
| Tab 2: Hàng hóa | ✅ | Goods table + total |
| Tab 3: Thanh toán | ✅ | Payment table + summary |
| Tab 4: Lịch sử | ✅ | Event timeline |
| Status indicators | ✅ | Color-coded with emoji |
| Scrollable content | ✅ | QScrollArea for long content |

**Tab 1 - Thông tin hợp đồng:**
| Section | Fields |
|---------|--------|
| Thông tin cơ bản | Mã HĐ, Trạng thái |
| Khách hàng & Vị trí | Tên KH, Địa chỉ vị trí |
| Thời hạn | Ngày BĐ, Ngày KT, Còn lại |
| Tài chính | Giá thuê, Cọc, PT TT, Tổng tiền |
| Điều khoản | Textarea |

**Tab 2 - Hàng hóa:**
| Column | Data |
|--------|------|
| Mã HH | HD202604001-HH001 |
| Tên hàng hóa | Product name |
| Số lượng | 100 |
| ĐVT | cái/thùng/kg |
| Giá trị | 1.500.000 ₫ |
| Ghi chú | Notes |

**Tab 3 - Thanh toán:**
| Column | Data |
|--------|------|
| Mã TT | HD202604001-TT001 |
| Kỳ thanh toán | Kỳ 1, Kỳ 2... |
| Đến hạn | 23/04/2026 |
| Số tiền | 1.500.000 ₫ |
| Trạng thái | ⏳/✅/❌ (color-coded) |

**Tab 4 - Lịch sử:**
| Column | Data |
|--------|------|
| STT | 1, 2, 3... |
| Ngày | 23/04/2026 |
| Sự kiện | 📝 created, 💰 payment... |
| Mô tả | Description |

---

## 🎨 Design System Integration

### Colors
```css
/* Contract-specific colors */
Primary Blue: #1976d2    /* Actions, links */
Success Green: #1aae39   /* Active contracts */
Warning Orange: #ff9800  /* Expiring soon */
Danger Red: #f44336     /* Overdue, terminated */
Info Blue: #2196f3      /* Renewed */
```

### Status Indicators
| Status | Emoji | Color |
|--------|-------|-------|
| Hiệu lực | ✅ | Green (#1aae39) |
| Hết hạn | ⏰ | Orange (#ff9800) |
| Chấm dứt | ❌ | Red (#f44336) |
| Gia hạn | 🔄 | Blue (#2196f3) |

### Payment Status
| Status | Label | Color |
|--------|-------|-------|
| Chưa thanh toán | ⏳ Chưa TT | Orange |
| Đã thanh toán | ✅ Đã TT | Green |
| Quá hạn | ❌ Quá hạn | Red |

### Alert Priorities
| Priority | Color | Condition |
|----------|-------|-----------|
| Critical | Red | Overdue contracts |
| High | Orange | ≤ 7 days remaining |
| Medium | Yellow | 8-30 days remaining |
| Low | Green | > 30 days remaining |

---

## ✅ Implementation Status

| Reference | Folder | Implemented In | Status |
|-----------|--------|----------------|--------|
| Danh mục hợp đồng | danh_muc_hop_dong/ | hop_dong_view.py | ✅ 100% |
| Thiết lập hợp đồng | thiet_lap_hop_dong/ | hop_dong_form.py | ✅ 100% |
| Chi tiết & Thanh toán | chi_tiet_hop_dong_thanh_toan/ | hop_dong_detail_view.py | ✅ 95% |

---

## 📝 Notes

### Đã làm tốt:
- ✅ Full CRUD với validation
- ✅ Renewal wizard (3 bước)
- ✅ Termination wizard với penalty calculator
- ✅ 4 tabs detail view
- ✅ Color-coded status & alerts
- ✅ Auto-calculate totals
- ✅ Export to text/HTML
- ✅ Alert system

### Có thể cải thiện:
- ⏳ PDF export (cần reportlab/weasyprint)
- ⏳ Email/SMS notifications (cần service config)
- ⏳ Payment schedule auto-generation (đã có service)
- ⏳ Goods management full UI (placeholder)
- ⏳ History persistence (cần database table)

---

## 🚀 Next Steps

### Phase 5.7 - Testing:
- [ ] Test HopDongService
- [ ] Test HangHoaService
- [ ] Test ThanhToanService
- [ ] Test wizards
- [ ] GUI tests
- [ ] Integration tests

### Future Enhancements:
- [ ] PDF export với reportlab
- [ ] Email notifications
- [ ] SMS reminders
- [ ] Batch operations
- [ ] Dashboard widgets
- [ ] Advanced reporting

---

## 📊 Phase 5 Summary

### Files Created:
| Category | Count | Total Size |
|----------|-------|------------|
| Models | 1 | 1.7 KB |
| Services | 4 | 34.8 KB |
| Views | 2 | 44.6 KB |
| Forms | 1 | 21.4 KB |
| Wizards | 2 | 21.7 KB |
| Utils | 3 | 21.5 KB |
| Tests | 0 | 0 KB |
| **Total** | **13** | **145.7 KB** |

### Features Implemented:
- ✅ Auto-generate mã hợp đồng
- ✅ CRUD operations
- ✅ Renewal wizard
- ✅ Termination wizard với penalty
- ✅ Payment tracking
- ✅ Goods management
- ✅ History tracking
- ✅ Alert system
- ✅ Export (text/HTML)
- ✅ Statistics & reporting

---

**Cập nhật:** 23/04/2026  
**Nhóm 12 - Lập trình Python**  
**Module:** Hợp đồng (Phase 5)  
**Status:** 90% Complete (chờ testing)
