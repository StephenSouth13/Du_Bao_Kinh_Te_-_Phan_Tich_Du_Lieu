import pyreadstat
import pandas as pd
import os

# Đọc file .sav
file_path = r"D:\Website\học tập\Du_Bao_Kinh_Te_-_Phan_Tich_Du_Lieu\Du_Bao_Kinh_Te_-_Phan_Tich_Du_Lieu\buoi_7\chat luong khoa hoc thac si va su hai long cua hoc vien.sav"
df, meta = pyreadstat.read_sav(file_path)

# Đường dẫn xuất file Excel (đặt cùng thư mục script cho chắc)
output_path = os.path.join(os.getcwd(), "output.xlsx")

# Ghi ra Excel với nhiều sheet
with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
    df.to_excel(writer, sheet_name="Data", index=False)
    df.describe(include="all").to_excel(writer, sheet_name="Describe")

print("✅ Đã xuất file Excel tại:", output_path)
