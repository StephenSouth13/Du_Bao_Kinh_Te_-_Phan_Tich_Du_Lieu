# ============================================================
# 📘 EUTHANASIA DATA EXPLORATION TOOL
# Author: Yasou x GPT-5
# Mô tả: Đọc dữ liệu SPSS (.sav), phân tích thống kê & xuất file Excel
# ============================================================

import pyreadstat
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Cấu hình hiển thị
pd.set_option("display.max_columns", None)
plt.style.use("ggplot")

# ====== 1️⃣ ĐỌC FILE SPSS ======
file_path = "euthan.sav"  # 🔁 Đặt file .sav cùng thư mục với script
df, meta = pyreadstat.read_sav(file_path)

print("✅ Đọc thành công:")
print(f"📊 Số quan sát (rows): {df.shape[0]}, Số biến (columns): {df.shape[1]}")
print("📋 Một vài biến đầu tiên:", list(df.columns[:10]))
print()

# ====== 2️⃣ TRÍCH METADATA ======
types = []
for var in meta.column_names:
    # 1 = Scale → Numeric, 2 hoặc 3 → Categorical/String
    measure_type = meta.variable_measure.get(var)
    if measure_type == 1:
        types.append("Numeric")
    else:
        types.append("Categorical")

meta_df = pd.DataFrame({
    "Variable Name": meta.column_names,
    "Variable Label": meta.column_labels,
    "Type": types,
    "Value Labels": [meta.value_labels.get(var, None) for var in meta.column_names]
})

print("🧾 Thông tin metadata (10 biến đầu):")
print(meta_df.head(10))
print()

# ====== 3️⃣ KIỂM TRA GIÁ TRỊ THIẾU ======
missing_summary = df.isna().sum().reset_index()
missing_summary.columns = ["Variable", "Missing Values"]
missing_summary["Missing (%)"] = (missing_summary["Missing Values"] / len(df) * 100).round(2)
print("🚨 Tóm tắt giá trị thiếu:")
print(missing_summary.sort_values(by="Missing Values", ascending=False).head(10))
print()

# ====== 4️⃣ THỐNG KÊ MÔ TẢ (CHO BIẾN SỐ) ======
desc_stats = df.describe(include='number').T
desc_stats["missing"] = df.isna().sum()
print("📈 Thống kê mô tả cho biến số:")
print(desc_stats.head(10))
print()

# ====== 5️⃣ BIẾN PHÂN LOẠI (CATEGORICAL) ======
cat_cols = [col for col in df.columns if df[col].dtype == 'object' or len(df[col].unique()) < 10]
cat_summary = {}
for col in cat_cols:
    cat_summary[col] = df[col].value_counts(dropna=False).to_dict()

print("📊 Thống kê tần suất cho biến phân loại (5 biến đầu):")
for k, v in list(cat_summary.items())[:5]:
    print(f"\n🔸 {k}: {v}")

# ====== 6️⃣ BIỂU ĐỒ TRỰC QUAN HÓA ======
output_dir = "charts"
os.makedirs(output_dir, exist_ok=True)

# Biểu đồ phân bố biến số
numeric_cols = df.select_dtypes(include='number').columns
for col in numeric_cols[:5]:  # chỉ vẽ 5 biến đầu để tránh quá nhiều hình
    plt.figure(figsize=(7, 4))
    sns.histplot(df[col].dropna(), kde=True, color="skyblue")
    plt.title(f"Phân bố biến: {col}")
    plt.xlabel(col)
    plt.ylabel("Tần suất")
    plt.tight_layout()
    plt.savefig(f"{output_dir}/{col}_hist.png")
    plt.close()

# Biểu đồ missing values
plt.figure(figsize=(10, 4))
sns.barplot(x="Variable", y="Missing (%)",
            data=missing_summary.sort_values(by="Missing (%)", ascending=False).head(15),
            palette="coolwarm")
plt.xticks(rotation=75)
plt.title("Top 15 biến có dữ liệu thiếu")
plt.tight_layout()
plt.savefig(f"{output_dir}/missing_summary.png")
plt.close()

print("\n📊 Biểu đồ đã được lưu trong thư mục ./charts/")
print()

# ====== 7️⃣ GỢI Ý CHUẨN BỊ MÔ HÌNH ======
print("💡 Gợi ý chuẩn bị mô hình:")
print("- Xác định biến phụ thuộc (VD: thái độ, đồng ý với hành vi, ...)")
print("- Mã hóa biến phân loại (OneHotEncoder / LabelEncoder)")
print("- Chuẩn hóa dữ liệu số (StandardScaler)")
print("- Áp dụng hồi quy tuyến tính / logistic / PCA hoặc mô hình ML khác.")
print()

# ====== 8️⃣ XUẤT FILE EXCEL PHÂN TÍCH ======
output_file = "euthan_full_analysis.xlsx"
with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
    df.to_excel(writer, sheet_name="Raw Data", index=False)
    meta_df.to_excel(writer, sheet_name="Metadata", index=False)
    missing_summary.to_excel(writer, sheet_name="Missing Summary", index=False)
    desc_stats.to_excel(writer, sheet_name="Descriptive Stats")

print(f"📂 File phân tích chi tiết đã được lưu: {output_file}")
print("\n🎯 Phân tích hoàn tất! Bạn có thể mở file Excel hoặc xem hình trong thư mục 'charts'.")
