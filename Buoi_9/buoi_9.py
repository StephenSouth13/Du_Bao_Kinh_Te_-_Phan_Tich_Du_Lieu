import pyreadstat
import pandas as pd

# === 1️⃣ Đọc file .sav ===
file_path = "euthan.sav"
df, meta = pyreadstat.read_sav(file_path)

print(f"✅ Đọc thành công, có {df.shape[0]} dòng và {df.shape[1]} cột.")
print("📋 Một vài cột đầu tiên:", df.columns[:10].tolist())

# === 2️⃣ Lấy metadata (đảm bảo tương thích với mọi phiên bản pyreadstat) ===
info = pd.DataFrame({
    "Variable": meta.column_names,
    "Label": getattr(meta, "column_labels", [""] * len(meta.column_names)),
    "Format": getattr(meta, "formats", [""] * len(meta.column_names)),
    "Measure": getattr(meta, "column_measure_levels", [""] * len(meta.column_names)),
    "Value Labels": [meta.value_labels.get(v, "") for v in meta.column_names]
})

# === 3️⃣ Xuất dữ liệu và metadata ra Excel ===
output_file = "euthan_full.xlsx"
with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
    df.to_excel(writer, sheet_name="Data", index=False)
    info.to_excel(writer, sheet_name="Metadata", index=False)

print(f"💾 Đã xuất đầy đủ dữ liệu và metadata ra '{output_file}'.")
