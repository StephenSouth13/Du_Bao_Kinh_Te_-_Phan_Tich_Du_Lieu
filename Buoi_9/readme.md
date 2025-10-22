# 📊 Phân tích thái độ về An tử (Euthanasia)

Dự án này phân tích bộ dữ liệu `euthan.sav` để khám phá các yếu tố tiềm ẩn (factors) đằng sau thái độ của mọi người đối với hành vi an tử.

* **Dữ liệu:** `euthan.sav`
* **Quan sát:** 357 người trả lời
* **Biến:** 31 phát biểu (`e1` - `e31`)
* **Thang đo:** Likert 5 mức (1 = Rất không đồng ý → 5 = Rất đồng ý)
* **Đặc điểm:** Dữ liệu sạch, không có giá trị thiếu, lý tưởng cho Phân tích nhân tố (EFA).

---

## ⚙️ Luồng Phân tích tự động

Quy trình gồm 3 script chính để xử lý từ dữ liệu thô đến báo cáo:

### 1. Khám phá dữ liệu (`read_euthan_full.py`)

* **Mục tiêu:** Đọc file `.sav` và kiểm tra cấu trúc dữ liệu ban đầu.
* **Kết quả:** In ra thông tin tổng quan (số biến, số quan sát) để xác nhận dữ liệu.

### 2. Phân tích nhân tố (`read_euthan_factor.py`)

* **Mục tiêu:** Chạy Phân tích nhân tố khám phá (EFA) để nhóm 31 biến thành các yếu tố tiềm ẩn.
* **Kết quả (Xuất file):**
    * `euthan_factor_loadings.xlsx`: Ma trận tải nhân tố, cho thấy mỗi biến (`e1`) liên quan mạnh đến Factor (`Factor1`) nào.
    * `charts/scree_plot.png`: Biểu đồ Scree Plot (xác định 6 nhân tố).
    * `charts/correlation_heatmap.png`: Heatmap tương quan giữa các biến.

### 3. Tổng hợp báo cáo (`read_euthan_summary.py`)

* **Mục tiêu:** Đọc file `loadings.xlsx` và tự động tạo báo cáo diễn giải các nhân tố.
* **Kết quả (Xuất file):**
    * `euthan_factor_report.md`: Báo cáo tóm tắt các nhóm nhân tố (ví dụ: Factor 1 = "Ủng hộ đạo đức", Factor 2 = "Phản đối tôn giáo").

---
```markdown
# 📊 Phân tích thái độ về An tử (Euthanasia)

Dự án này phân tích bộ dữ liệu `euthan.sav` để khám phá các yếu tố tiềm ẩn (factors) đằng sau thái độ của mọi người đối với hành vi an tử.

* **Dữ liệu:** `euthan.sav`
* **Quan sát:** 357 người trả lời
* **Biến:** 31 phát biểu (`e1` - `e31`)
* **Thang đo:** Likert 5 mức (1 = Rất không đồng ý → 5 = Rất đồng ý)
* **Đặc điểm:** Dữ liệu sạch, không có giá trị thiếu, lý tưởng cho Phân tích nhân tố (EFA).

---

## ⚙️ Luồng Phân tích tự động

Quy trình gồm 3 script chính để xử lý từ dữ liệu thô đến báo cáo:

### 1. Khám phá dữ liệu (`read_euthan_full.py`)

* **Mục tiêu:** Đọc file `.sav` và kiểm tra cấu trúc dữ liệu ban đầu.
* **Kết quả:** In ra thông tin tổng quan (số biến, số quan sát) để xác nhận dữ liệu.

### 2. Phân tích nhân tố (`read_euthan_factor.py`)

* **Mục tiêu:** Chạy Phân tích nhân tố khám phá (EFA) để nhóm 31 biến thành các yếu tố tiềm ẩn.
* **Kết quả (Xuất file):**
    * `euthan_factor_loadings.xlsx`: Ma trận tải nhân tố, cho thấy mỗi biến (`e1`) liên quan mạnh đến Factor (`Factor1`) nào.
    * `charts/scree_plot.png`: Biểu đồ Scree Plot (xác định 6 nhân tố).
    * `charts/correlation_heatmap.png`: Heatmap tương quan giữa các biến.

### 3. Tổng hợp báo cáo (`read_euthan_summary.py`)

* **Mục tiêu:** Đọc file `loadings.xlsx` và tự động tạo báo cáo diễn giải các nhân tố.
* **Kết quả (Xuất file):**
    * `euthan_factor_report.md`: Báo cáo tóm tắt các nhóm nhân tố (ví dụ: Factor 1 = "Ủng hộ đạo đức", Factor 2 = "Phản đối tôn giáo").

---

## 🗺️ Sơ đồ luồng

```

euthan.sav                 \# Dữ liệu gốc
│
├── read\_euthan\_full.py    \# 1. Đọc và xem tổng quan
│
├── read\_euthan\_factor.py  \# 2. Chạy EFA
│   ├── euthan\_factor\_loadings.xlsx
│   ├── charts/scree\_plot.png
│   └── charts/correlation\_heatmap.png
│
└── read\_euthan\_summary.py   \# 3. Đọc loadings, xuất báo cáo
└── euthan\_factor\_report.md

```

---

## 📈 Kết quả chính

Phân tích EFA xác định được 6 nhân tố chính từ 31 biến quan sát.

| Thành phần | Kết quả |
| :--- | :--- |
| **Số quan sát** | 357 |
| **Số biến Likert** | 31 |
| **Số nhân tố (Eigenvalue > 1)** | **6 nhân tố** |
| **Biểu đồ Scree Plot** | `./charts/scree_plot.png` |
| **Heatmap tương quan** | `./charts/correlation_heatmap.png` |
| **Bảng tải nhân tố (Loadings)** | `euthan_factor_loadings.xlsx` |
| **Gợi ý nhóm nhân tố** | - **Factor1:** "Ủng hộ đạo đức" (e1–e5)<br> - **Factor2:** "Phản đối tôn giáo" (e20–e25) |
```