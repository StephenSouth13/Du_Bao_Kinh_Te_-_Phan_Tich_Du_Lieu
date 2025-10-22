import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# === 1. Đọc file và chuẩn hóa dữ liệu ===
df = pd.read_excel("euthan_factor_loadings.xlsx")

# Nếu cột đầu tiên không có tên, đặt lại tên là "Variable"
if df.columns[0].startswith("Unnamed"):
    df.rename(columns={df.columns[0]: "Variable"}, inplace=True)

print(f"✅ Đọc thành công: {df.shape[0]} biến × {df.shape[1]-1} nhân tố")

# === 2. Tìm hệ số loading cao nhất cho từng biến ===
assignments = []
for _, row in df.iterrows():
    var = row["Variable"]
    best_factor = row[1:].astype(float).idxmax()  # cột có loading cao nhất
    best_loading = row[best_factor]
    assignments.append((var, best_factor, best_loading))

assign_df = pd.DataFrame(assignments, columns=["Variable", "Factor", "Loading"])

# === 3. Tạo mô hình SEM đơn giản ===
G = nx.DiGraph()

# Thêm node cho các nhân tố và biến
factors = sorted(assign_df["Factor"].unique())
for f in factors:
    G.add_node(f, color="#4A90E2", size=1500)

for _, row in assign_df.iterrows():
    G.add_node(row["Variable"], color="#F5A623", size=1000)
    G.add_edge(row["Factor"], row["Variable"], weight=row["Loading"])

# === 4. Vẽ sơ đồ đẹp và rõ ===
plt.figure(figsize=(12, 9))
pos = nx.spring_layout(G, seed=42, k=0.8)  # layout đẹp và tự nhiên

# Node colors
node_colors = [G.nodes[n]["color"] for n in G.nodes()]
node_sizes = [G.nodes[n]["size"] for n in G.nodes()]

# Vẽ node và edges
nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color=node_colors, alpha=0.9)
nx.draw_networkx_labels(G, pos, font_size=11, font_family="Arial", font_color="white")

# Vẽ các mũi tên (hệ số standardized)
edge_labels = { (u, v): f"{d['weight']:.2f}" for u, v, d in G.edges(data=True) }
nx.draw_networkx_edges(G, pos, arrows=True, arrowstyle="->", width=2, alpha=0.6)
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=9, font_color="black")

plt.title("Sơ đồ EFA - Kết quả Standardized Factor Loadings", fontsize=14, weight="bold")
plt.axis("off")
plt.tight_layout()
plt.show()
