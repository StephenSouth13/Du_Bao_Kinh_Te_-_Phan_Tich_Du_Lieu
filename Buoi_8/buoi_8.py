# Yêu cầu cài trước:
# pip install pyreadstat pandas numpy openpyxl

import pyreadstat
import pandas as pd
import numpy as np
import os

# ---- 1. Đọc file .sav ----


file_path = r"D:\Website\học tập\Du_Bao_Kinh_Te_-_Phan_Tich_Du_Lieu\Du_Bao_Kinh_Te_-_Phan_Tich_Du_Lieu\Buoi_8\output.xlsx"
df = pd.read_excel(file_path, sheet_name="Data")  # hoặc "Describe"


# ---- 2. Chọn thang đo (Scale) ----
# Ví dụ: nhóm đo "Lòng trung thành" (LOYALTY)
items = ["Ioy1", "Ioy2", "Ioy3"]

# Kiểm tra xem các biến có tồn tại trong dữ liệu không
for item in items:
    if item not in df.columns:
        print(f"⚠️ Cảnh báo: {item} không có trong dữ liệu!")

# Lọc dữ liệu theo các biến trên
scale_df = df[items].dropna()

# ---- 3. Hàm tính Cronbach’s Alpha ----
def cronbach_alpha(dataframe):
    df_corr = dataframe.corr()
    n_items = len(df_corr.columns)
    mean_corr = df_corr.values[np.triu_indices(n_items, 1)].mean()
    alpha = (n_items * mean_corr) / (1 + (n_items - 1) * mean_corr)
    return alpha

# ---- 4. Tính tổng hợp ----
alpha_total = cronbach_alpha(scale_df)

# ---- 5. Tính “Alpha if item deleted” ----
alpha_if_deleted = {}
for col in items:
    temp_df = scale_df.drop(columns=[col])
    alpha_if_deleted[col] = cronbach_alpha(temp_df)

# ---- 6. Tính tương quan item-total ----
item_total_corr = {}
total_score = scale_df.sum(axis=1)
for col in items:
    item_total_corr[col] = scale_df[col].corr(total_score - scale_df[col])

# ---- 7. Xuất kết quả ----
result = pd.DataFrame({
    "Item": items,
    "Item-Total Corr": [item_total_corr[i] for i in items],
    "Alpha if Deleted": [alpha_if_deleted[i] for i in items]
})

print("\n=== Reliability Analysis ===")
print(f"Cronbach’s Alpha (Tổng): {alpha_total:.4f}\n")
print(result)

# ---- 8. Xuất ra Excel ----
output_path = os.path.join(os.getcwd(), "Buoi_8_reliability.xlsx")
with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
    scale_df.to_excel(writer, sheet_name="RawData", index=False)
    result.to_excel(writer, sheet_name="Reliability", index=False)

print(f"\n✅ Đã xuất kết quả tại: {output_path}")
