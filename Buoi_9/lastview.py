# lastview.py
import pandas as pd
from pyvis.network import Network

# === 1. Đọc dữ liệu thật từ Excel ===
# === Đọc loadings từ Excel ===
file_path = "euthan_factor_loadings.xlsx"
df = pd.read_excel(file_path, index_col=0)

print("📘 Loaded Data:")
print(df.head())

# === 2. Chuẩn bị mô hình SEM từ EFA loadings ===
# - Cột: Factor1..Factor6 (latent)
# - Dòng: e1..c18 (observed)
# - Dòng phát triển 
factors = df.columns.tolist()
variables = df.index.tolist()

# === 3. Tạo network interactive ===
net = Network(height="850px", width="100%", directed=True, bgcolor="#FFFFFF", font_color="black")

# Thêm latent variables (ellipse, màu vàng cam)
for f in factors:
    net.add_node(f, label=f, shape="ellipse", color="#FFB84C", size=45, title=f"<b>Latent Variable:</b> {f}")

# Thêm observed variables (chữ nhật, màu xanh)
for v in variables:
    net.add_node(v, label=v, shape="box", color="#91D8E4", size=30, title=f"<b>Observed Variable:</b> {v}")

# === 4. Thêm cạnh có trọng số thật (standardized loadings) ===
threshold = 0.25  # chỉ vẽ các loading mạnh
for v in variables:
    for f in factors:
        weight = df.loc[v, f]
        if abs(weight) >= threshold:
            net.add_edge(f, v, value=abs(weight), title=f"<b>{f} → {v}</b><br>Estimate: {weight:.2f}",
                         color="#555555" if weight > 0 else "#AA0000", width=3 + abs(weight) * 5)

# === 5. (Tuỳ chọn) Vẽ mối quan hệ giữa các latent factors ===
# Giả lập cấu trúc latent ảnh hưởng lẫn nhau (Factor1 → Factor6)
for i in range(len(factors) - 1):
    net.add_edge(factors[i], factors[i + 1],
                 title=f"<b>{factors[i]} → {factors[i+1]}</b>",
                 color="#888888", width=2, arrows="to")

# === 6. Xuất HTML interactive ===
net.set_options("""
var options = {
  "nodes": {
    "font": {"size": 18, "face": "Arial"},
    "borderWidth": 2,
    "shadow": true
  },
  "edges": {
    "color": {"inherit": false},
    "smooth": {"type": "cubicBezier"},
    "arrows": {"to": {"enabled": true, "scaleFactor": 1.2}},
    "shadow": true
  },
  "physics": {
    "stabilization": true,
    "barnesHut": {"gravitationalConstant": -3500}
  }
}
""")

output_file = "sem_interactive.html"
net.write_html(output_file)
print(f"✅ Interactive SEM graph saved to: {output_file}")

#==6