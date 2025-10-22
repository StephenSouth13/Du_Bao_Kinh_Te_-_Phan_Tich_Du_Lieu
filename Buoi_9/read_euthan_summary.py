# ======================================================
# 📊 Euthanasia Factor Summary Generator
# Version: 1.0 | Author: Yasou + ChatGPT
# ======================================================

import pandas as pd
import os

# ------------------------------------------------------
# 1️⃣ Đọc file loadings
# ------------------------------------------------------
file_path = "euthan_factor_loadings.xlsx"
if not os.path.exists(file_path):
    print("❌ Không tìm thấy file 'euthan_factor_loadings.xlsx'. Hãy chạy script phân tích nhân tố trước.")
    exit()

df = pd.read_excel(file_path, index_col=0)

print("✅ Đọc thành công file loadings:", file_path)
print("📊 Số biến:", df.shape[0], "| Số nhân tố:", df.shape[1])

# ------------------------------------------------------
# 2️⃣ Xác định nhân tố có tải cao nhất cho từng biến
# ------------------------------------------------------
df["MainFactor"] = df.abs().idxmax(axis=1)
df["MaxLoading"] = df.abs().max(axis=1)

# ------------------------------------------------------
# 3️⃣ Gom nhóm biến theo từng nhân tố
# ------------------------------------------------------
factor_groups = {}
for factor in df.columns[:-2]:  # bỏ cột phụ
    group = df[df["MainFactor"] == factor].index.tolist()
    factor_groups[factor] = group

# ------------------------------------------------------
# 4️⃣ Gợi ý đặt tên nhân tố (tùy chỉnh sau)
# ------------------------------------------------------
name_suggestions = {
    "Factor1": "Nhóm Ủng hộ đạo đức / Nhận thức tích cực",
    "Factor2": "Nhóm Phản đối tôn giáo / Niềm tin",
    "Factor3": "Nhóm Thái độ pháp lý / Quyền tự quyết",
    "Factor4": "Nhóm Ảnh hưởng xã hội / Gia đình",
    "Factor5": "Nhóm Cảm xúc cá nhân / Nỗi sợ",
    "Factor6": "Nhóm Nhận thức triết học / Tính nhân đạo",
}

# ------------------------------------------------------
# 5️⃣ Tạo nội dung Markdown
# ------------------------------------------------------
report_lines = [
    "# 🧩 Euthanasia Factor Analysis Summary",
    "",
    "Tổng hợp các nhóm nhân tố từ phân tích EFA (Exploratory Factor Analysis)",
    "",
    f"**Tổng số biến:** {df.shape[0]}",
    f"**Số nhân tố trích được:** {df.shape[1] - 2}",
    "",
    "---",
]

for factor, vars_in_factor in factor_groups.items():
    report_lines.append(f"## 🔹 {factor}: {name_suggestions.get(factor, 'Chưa đặt tên')}")
    report_lines.append("")
    report_lines.append(f"**Số biến:** {len(vars_in_factor)}")
    report_lines.append("")
    for var in vars_in_factor:
        loading_value = df.loc[var, factor]
        report_lines.append(f"- `{var}` → tải = {loading_value:.3f}")
    report_lines.append("")
    report_lines.append("**Gợi ý diễn giải:**")
    report_lines.append(f"> {name_suggestions.get(factor, 'Phân tích thủ công theo nội dung câu hỏi.')}")
    report_lines.append("\n---\n")

# ------------------------------------------------------
# 6️⃣ Xuất file Markdown
# ------------------------------------------------------
output_path = "euthan_factor_summary.md"
with open(output_path, "w", encoding="utf-8") as f:
    f.write("\n".join(report_lines))

print(f"📂 Báo cáo Markdown đã được lưu: {output_path}")
print("🎯 Bạn có thể mở file này trực tiếp bằng VS Code hoặc Markdown Preview.")

