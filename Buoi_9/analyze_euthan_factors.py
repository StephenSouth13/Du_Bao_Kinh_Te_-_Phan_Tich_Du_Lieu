import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from math import pi
import os

# ==============================
# 1️⃣ Đọc dữ liệu
# ==============================
file_path = "euthan_factor_loadings.xlsx"
if not os.path.exists(file_path):
    raise FileNotFoundError(f"Không tìm thấy file: {file_path}")

df = pd.read_excel(file_path)
print(f"✅ Đã đọc {df.shape[0]} biến và {df.shape[1]-1} nhân tố.")

# ==============================
# 2️⃣ Chuẩn hóa & tìm nhân tố mạnh nhất
# ==============================
df = df.rename(columns={df.columns[0]: "Variable"})  # cột đầu tiên là tên biến
numeric_cols = df.columns[1:]
df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')

df["MaxLoading"] = df[numeric_cols].abs().max(axis=1)
df["MaxFactor"] = df[numeric_cols].abs().idxmax(axis=1)

# ==============================
# 3️⃣ Gom nhóm theo nhân tố
# ==============================
grouped = df.groupby("MaxFactor")["Variable"].apply(list)

report = []
report.append("# 🧩 PHÂN TÍCH NHÂN TỐ EUTHANASIA – TÓM TẮT DIỄN GIẢI\n")
report.append(f"- Số biến gốc: {len(df)}")
report.append(f"- Số nhân tố trích được: {len(grouped)}\n")
report.append("## 📘 Kết quả nhóm biến theo từng nhân tố:\n")

for i, (factor, vars_list) in enumerate(grouped.items(), 1):
    joined_vars = ", ".join(map(str, vars_list))
    report.append(f"### 🔹 {factor} – Nhóm {i}")
    report.append(f"**Biến tải mạnh:** {joined_vars}\n")
    report.append(f"**Gợi ý diễn giải:**\n")
    if "e1" in joined_vars or "e5" in joined_vars:
        report.append("- Có thể là nhóm **Ủng hộ đạo đức – chấp nhận cái chết nhân đạo**.")
    elif "e20" in joined_vars or "e25" in joined_vars:
        report.append("- Có thể là nhóm **Phản đối dựa trên tôn giáo hoặc chuẩn mực xã hội**.")
    elif "e10" in joined_vars or "e15" in joined_vars:
        report.append("- Có thể là nhóm **Trung lập – nhận thức xã hội**.")
    else:
        report.append("- Nhóm thể hiện **các khía cạnh tâm lý hoặc nhận thức khác**.")
    report.append("")  # dòng trống

# ==============================
# 4️⃣ Xuất file Markdown báo cáo
# ==============================
output_md = "euthan_factor_summary.md"
with open(output_md, "w", encoding="utf-8") as f:
    f.write("\n".join(report))

print(f"📄 Báo cáo Markdown đã lưu tại: {output_md}")

# ==============================
# 5️⃣ Tạo biểu đồ Radar (Spider Chart)
# ==============================
print("📈 Đang vẽ biểu đồ Radar cho các nhân tố...")

# Tính trung bình giá trị tải cho mỗi nhân tố
factor_means = df.groupby("MaxFactor")[numeric_cols].mean()

# Thiết lập radar chart
categories = factor_means.columns
N = len(categories)

# Tạo thư mục lưu hình
os.makedirs("charts", exist_ok=True)

for factor_name, row in factor_means.iterrows():
    values = row.values.flatten().tolist()
    values += values[:1]  # vòng tròn

    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]

    plt.figure(figsize=(6,6))
    plt.polar(angles, values, linewidth=2, linestyle='solid')
    plt.fill(angles, values, alpha=0.25)
    plt.title(f"🌟 Biểu đồ Radar – {factor_name}", size=14, weight='bold', pad=20)
    plt.xticks(angles[:-1], categories, size=8)
    plt.tight_layout()
    plt.savefig(f"./charts/radar_{factor_name}.png", dpi=200)
    plt.close()

print("✅ Biểu đồ Radar đã lưu trong thư mục ./charts/")
print("🎯 Phân tích & trực quan hóa hoàn tất!")
