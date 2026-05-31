# Spec: Mở rộng giao diện Báo cáo Thống kê

**Date:** 2026-05-31
**Status:** Approved

---

## Overview

Mở rộng giao diện báo cáo thống kê (BaoCaoView) để hiển thị đầy đủ thông tin về Kho, Khách hàng, Hàng hóa.

---

## Layout Structure

### 1. Summary Row (giữ nguyên)
- Doanh thu tháng | Hợp đồng đang hoạt động | Hợp đồng sắp hết hạn | Tổng khách hàng

### 2. Extended Summary (4 card mới)
- Tổng số kho | Tỷ lệ lấp đầy TB
- Tổng mặt hàng | Giá trị tồn kho

### 3. Detail Panels (3 panels)

**Panel Kho:**
- Tổng số kho: X | Đang hoạt động: X
- Tổng diện tích: X m² | Tổng sức chứa: X m³
- Tỷ lệ lấp đầy trung bình: X%

**Panel Khách hàng:**
- Tổng khách hàng: X | Đang hoạt động: X
- Khách hàng không hoạt động: X

**Panel Hàng hóa:**
- Tổng mặt hàng: X | Đang trong kho: X
- Tổng giá trị: X đ

### 4. Biểu đồ tăng trưởng (giữ nguyên)
- Bar chart doanh thu theo tháng

### 5. Bảng hợp đồng gần đây (giữ nguyên)

---

## Components

### Extended Summary Cards
- 4 card nhỏ trên 2 hàng (2x2 grid)
- Style: background #f8f9fa, border 1px #e0e0e0, border-radius 8px
- Icon + Value + Label

### Detail Panels
- 3 panel nằm ngang (QHBoxLayout)
- Mỗi panel: background white, border-radius 10px, padding 16px
- Tiêu đề + nội dung dạng grid

---

## Data Source

Dữ liệu từ `ReportService.get_dashboard_summary()`:
- `kho`: total, active, total_dien_tich, total_suc_chua, avg_fill_rate
- `khach_hang`: total, active, inactive
- `hang_hoa`: total_items, in_stock, total_value

---

## Implementation Plan

1. Thêm `_create_extended_summary_section()` - 4 card nhỏ
2. Thêm `_create_kho_detail_panel()` - panel chi tiết kho
3. Thêm `_create_khach_hang_detail_panel()` - panel chi tiết khách hàng
4. Thêm `_create_hang_hoa_detail_panel()` - panel chi tiết hàng hóa
5. Cập nhật `_create_dashboard_content()` để gọi các method mới
6. Cập nhật `load_dashboard_summary()` để populate dữ liệu mới

---

## Acceptance Criteria

- [ ] Hiển thị đầy đủ 4 card mới: Kho, Tỷ lệ lấp đầy, Mặt hàng, Giá trị
- [ ] Hiển thị 3 panel chi tiết: Kho, Khách hàng, Hàng hóa
- [ ] Dữ liệu được load đúng từ ReportService
- [ ] Giao diện responsive, không bị cắt text
- [ ] Style thống nhất với design hiện tại