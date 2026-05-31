# BaoCaoView Dashboard Expansion Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Mở rộng giao diện báo cáo thống kê để hiển thị đầy đủ thông tin về Kho, Khách hàng, Hàng hóa

**Architecture:** Thêm các method mới vào BaoCaoView để tạo extended summary cards và detail panels. Dữ liệu từ ReportService.get_dashboard_summary() đã có sẵn.

**Tech Stack:** PyQt6, Python, ReportService

---

## File Structure

- Modify: `src/gui/views/bao_cao_view.py` - Thêm các method và cập nhật UI

---

## Task 1: Thêm Extended Summary Section

**Files:**
- Modify: `src/gui/views/bao_cao_view.py` - Thêm `_create_extended_summary_section()` và cập nhật `_create_dashboard_content()`

- [ ] **Step 1: Thêm method `_create_extended_summary_section()`**

Thêm sau `_create_summary_section()` (sau dòng 246):

```python
def _create_extended_summary_section(self) -> QFrame:
    """Create extended summary section with 4 cards: Kho, Ty le lap day, Mat hang, Gia tri"""
    frame = QFrame()
    frame.setStyleSheet("""
        QFrame {
            background-color: #ffffff;
            border: 1px solid rgba(0, 0, 0, 0.08);
            border-radius: 10px;
            padding: 12px;
        }
    """)
    layout = QHBoxLayout(frame)
    layout.setSpacing(16)
    layout.setContentsMargins(16, 12, 16, 12)

    # Card 1: Tong so kho
    kho_card = self._create_stat_card('kho', '🏭', 'Tổng số kho', '#1976d2')
    layout.addWidget(kho_card)

    # Card 2: Ty le lap day
    fill_card = self._create_stat_card('fill_rate', '📊', 'Tỷ lệ lấp đầy TB', '#ff9800')
    layout.addWidget(fill_card)

    # Card 3: Tong mat hang
    mat_hang_card = self._create_stat_card('mat_hang', '📦', 'Tổng mặt hàng', '#9c27b0')
    layout.addWidget(mat_hang_card)

    # Card 4: Gia tri ton kho
    gia_tri_card = self._create_stat_card('gia_tri', '💰', 'Giá trị tồn kho', '#43a047', is_currency=True)
    layout.addWidget(gia_tri_card)

    return frame
```

- [ ] **Step 2: Cập nhật `_create_dashboard_content()` để gọi extended summary**

Sau dòng 140 (sau `self.content_layout.addWidget(summary_section)`), thêm:

```python
# Extended summary section (4 cards)
extended_summary = self._create_extended_summary_section()
self.content_layout.addWidget(extended_summary)
```

- [ ] **Step 3: Run test**

Run: Chạy app và kiểm tra xem 4 card mới có hiển thị không

- [ ] **Step 4: Commit**

```bash
git add src/gui/views/bao_cao_view.py
git commit -m "feat: add extended summary cards to BaoCaoView"
```

---

## Task 2: Thêm Panel Chi Tiết Kho

**Files:**
- Modify: `src/gui/views/bao_cao_view.py`

- [ ] **Step 1: Thêm method `_create_kho_detail_panel()`**

Thêm sau `_create_growth_chart()` (sau dòng 331):

```python
def _create_kho_detail_panel(self) -> QFrame:
    """Create detailed panel for warehouse statistics"""
    frame = QFrame()
    frame.setStyleSheet("""
        QFrame {
            background-color: #ffffff;
            border: 1px solid rgba(0, 0, 0, 0.08);
            border-radius: 10px;
            padding: 16px;
        }
    """)

    layout = QVBoxLayout(frame)
    layout.setContentsMargins(12, 12, 12, 12)
    layout.setSpacing(8)

    # Title
    title = QLabel("🏭 Thông tin Kho")
    title.setStyleSheet("font-size: 14px; font-weight: 600; color: #31302e; padding-bottom: 8px;")
    layout.addWidget(title)

    # Content grid
    grid = QVBoxLayout()
    grid.setSpacing(6)

    self.kho_labels = {
        'total': QLabel("0"),
        'active': QLabel("0"),
        'dien_tich': QLabel("0 m²"),
        'suc_chua': QLabel("0 m³"),
        'fill_rate': QLabel("0%")
    }

    # Row 1
    row1 = QHBoxLayout()
    row1.addWidget(QLabel("Tổng số kho:"))
    row1.addWidget(self.kho_labels['total'])
    row1.addWidget(QLabel("| Đang hoạt động:"))
    row1.addWidget(self.kho_labels['active'])
    row1.addStretch()
    grid.addLayout(row1)

    # Row 2
    row2 = QHBoxLayout()
    row2.addWidget(QLabel("Tổng diện tích:"))
    row2.addWidget(self.kho_labels['dien_tich'])
    row2.addWidget(QLabel("| Tổng sức chứa:"))
    row2.addWidget(self.kho_labels['suc_chua'])
    row2.addStretch()
    grid.addLayout(row2)

    # Row 3
    row3 = QHBoxLayout()
    row3.addWidget(QLabel("Tỷ lệ lấp đầy TB:"))
    row3.addWidget(self.kho_labels['fill_rate'])
    row3.addStretch()
    grid.addLayout(row3)

    layout.addLayout(grid)
    return frame
```

- [ ] **Step 2: Cập nhật `_create_dashboard_content()`**

Sau `extended_summary`, thêm:

```python
# Detail panels
detail_panels_container = QFrame()
detail_panels_layout = QHBoxLayout(detail_panels_container)
detail_panels_layout.setSpacing(12)

# Kho panel
kho_panel = self._create_kho_detail_panel()
detail_panels_layout.addWidget(kho_panel, 1)

# Khach hang panel
khach_hang_panel = self._create_khach_hang_detail_panel()
detail_panels_layout.addWidget(khach_hang_panel, 1)

# Hang hoa panel
hang_hoa_panel = self._create_hang_hoa_detail_panel()
detail_panels_layout.addWidget(hang_hoa_panel, 1)

self.content_layout.addWidget(detail_panels_container)
```

- [ ] **Step 3: Run test**

Kiểm tra panel Kho có hiển thị đúng vị trí

- [ ] **Step 4: Commit**

```bash
git add src/gui/views/bao_cao_view.py
git commit -m "feat: add Kho detail panel to BaoCaoView"
```

---

## Task 3: Thêm Panel Chi Tiết Khách Hàng

**Files:**
- Modify: `src/gui/views/bao_cao_view.py`

- [ ] **Step 1: Thêm method `_create_khach_hang_detail_panel()`**

Thêm sau `_create_kho_detail_panel()`:

```python
def _create_khach_hang_detail_panel(self) -> QFrame:
    """Create detailed panel for customer statistics"""
    frame = QFrame()
    frame.setStyleSheet("""
        QFrame {
            background-color: #ffffff;
            border: 1px solid rgba(0, 0, 0, 0.08);
            border-radius: 10px;
            padding: 16px;
        }
    """)

    layout = QVBoxLayout(frame)
    layout.setContentsMargins(12, 12, 12, 12)
    layout.setSpacing(8)

    # Title
    title = QLabel("👥 Thông tin Khách hàng")
    title.setStyleSheet("font-size: 14px; font-weight: 600; color: #31302e; padding-bottom: 8px;")
    layout.addWidget(title)

    # Content grid
    grid = QVBoxLayout()
    grid.setSpacing(6)

    self.khach_hang_labels = {
        'total': QLabel("0"),
        'active': QLabel("0"),
        'inactive': QLabel("0")
    }

    # Row 1
    row1 = QHBoxLayout()
    row1.addWidget(QLabel("Tổng khách hàng:"))
    row1.addWidget(self.khach_hang_labels['total'])
    row1.addWidget(QLabel("| Đang hoạt động:"))
    row1.addWidget(self.khach_hang_labels['active'])
    row1.addStretch()
    grid.addLayout(row1)

    # Row 2
    row2 = QHBoxLayout()
    row2.addWidget(QLabel("Không hoạt động:"))
    row2.addWidget(self.khach_hang_labels['inactive'])
    row2.addStretch()
    grid.addLayout(row2)

    layout.addLayout(grid)
    return frame
```

- [ ] **Step 2: Run test**

Kiểm tra panel Khách hàng có hiển thị

- [ ] **Step 3: Commit**

```bash
git add src/gui/views/bao_cao_view.py
git commit -m "feat: add KhachHang detail panel to BaoCaoView"
```

---

## Task 4: Thêm Panel Chi Tiết Hàng Hóa

**Files:**
- Modify: `src/gui/views/bao_cao_view.py`

- [ ] **Step 1: Thêm method `_create_hang_hoa_detail_panel()`**

Thêm sau `_create_khach_hang_detail_panel()`:

```python
def _create_hang_hoa_detail_panel(self) -> QFrame:
    """Create detailed panel for goods statistics"""
    frame = QFrame()
    frame.setStyleSheet("""
        QFrame {
            background-color: #ffffff;
            border: 1px solid rgba(0, 0, 0, 0.08);
            border-radius: 10px;
            padding: 16px;
        }
    """)

    layout = QVBoxLayout(frame)
    layout.setContentsMargins(12, 12, 12, 12)
    layout.setSpacing(8)

    # Title
    title = QLabel("📦 Thông tin Hàng hóa")
    title.setStyleSheet("font-size: 14px; font-weight: 600; color: #31302e; padding-bottom: 8px;")
    layout.addWidget(title)

    # Content grid
    grid = QVBoxLayout()
    grid.setSpacing(6)

    self.hang_hoa_labels = {
        'total': QLabel("0"),
        'in_stock': QLabel("0"),
        'value': QLabel("0 đ")
    }

    # Row 1
    row1 = QHBoxLayout()
    row1.addWidget(QLabel("Tổng mặt hàng:"))
    row1.addWidget(self.hang_hoa_labels['total'])
    row1.addWidget(QLabel("| Đang trong kho:"))
    row1.addWidget(self.hang_hoa_labels['in_stock'])
    row1.addStretch()
    grid.addLayout(row1)

    # Row 2
    row2 = QHBoxLayout()
    row2.addWidget(QLabel("Tổng giá trị:"))
    row2.addWidget(self.hang_hoa_labels['value'])
    row2.addStretch()
    grid.addLayout(row2)

    layout.addLayout(grid)
    return frame
```

- [ ] **Step 2: Run test**

Kiểm tra panel Hàng hóa có hiển thị

- [ ] **Step 3: Commit**

```bash
git add src/gui/views/bao_cao_view.py
git commit -m "feat: add HangHoa detail panel to BaoCaoView"
```

---

## Task 5: Cập nhật load_dashboard_summary() để populate dữ liệu mới

**Files:**
- Modify: `src/gui/views/bao_cao_view.py`

- [ ] **Step 1: Cập nhật `load_dashboard_summary()`**

Tìm và cập nhật phần sau `self.summary_labels['total_customers'].setText(...)` (khoảng dòng 396), thêm:

```python
# Update kho labels
kho_data = summary.get('kho', {})
self.kho_labels['total'].setText(str(kho_data.get('total', 0)))
self.kho_labels['active'].setText(str(kho_data.get('active', 0)))
self.kho_labels['dien_tich'].setText(f"{kho_data.get('total_dien_tich', 0):,.0f} m²")
self.kho_labels['suc_chua'].setText(f"{kho_data.get('total_suc_chua', 0):,.0f} m³")
self.kho_labels['fill_rate'].setText(f"{kho_data.get('avg_fill_rate', 0):.1f}%")

# Update extended summary stat cards
self.stats_labels['kho_value'].setText(str(kho_data.get('total', 0)))
self.stats_labels['fill_rate_value'].setText(f"{kho_data.get('avg_fill_rate', 0):.1f}%")

# Update khach hang labels
kh_data = summary.get('khach_hang', {})
self.khach_hang_labels['total'].setText(str(kh_data.get('total', 0)))
self.khach_hang_labels['active'].setText(str(kh_data.get('active', 0)))
self.khach_hang_labels['inactive'].setText(str(kh_data.get('inactive', 0)))

# Update hang hoa labels
hh_data = summary.get('hang_hoa', {})
self.hang_hoa_labels['total'].setText(str(hh_data.get('total_items', 0)))
self.hang_hoa_labels['in_stock'].setText(str(hh_data.get('in_stock', 0)))
self.hang_hoa_labels['value'].setText(format_currency(hh_data.get('total_value', 0)))

# Update extended summary cards for hang hoa
self.stats_labels['mat_hang_value'].setText(str(hh_data.get('total_items', 0)))
self.stats_labels['gia_tri_value'].setText(format_currency(hh_data.get('total_value', 0)))
```

- [ ] **Step 2: Run test**

Kiểm tra tất cả dữ liệu hiển thị đúng

- [ ] **Step 3: Commit**

```bash
git add src/gui/views/bao_cao_view.py
git commit -m "feat: populate new dashboard panels with data"
```

---

## Self-Review Checklist

- [x] Spec coverage: Tất cả requirements đều được implement
- [x] Placeholder scan: Không có TBD/TODO
- [x] Type consistency: Các method và label names nhất quán

---

## Execution Options

**Plan complete and saved to `docs/superpowers/plans/2026-05-31-bao-cao-thong-ke-expansion.md`. Two execution options:**

**1. Subagent-Driven (recommended)** - I dispatch a fresh subagent per task, review between tasks, fast iteration

**2. Inline Execution** - Execute tasks in this session using executing-plans, batch execution with checkpoints

**Which approach?**