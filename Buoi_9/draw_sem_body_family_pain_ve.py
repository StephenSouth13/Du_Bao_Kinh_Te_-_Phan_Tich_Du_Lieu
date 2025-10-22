import networkx as nx
import matplotlib.pyplot as plt

# === 1. Định nghĩa các mối quan hệ (chuẩn hóa từ mô hình bạn chụp) ===
relations = [
    ("Body1", "Pain1", 0.426),
    ("Family1", "Pain1", 0.335),
    ("Pain1", "VE", 0.508),
    ("Body1", "VE", 0.126),
    ("Family1", "VE", 0.088),
]

# === 2. Khởi tạo đồ thị ===
G = nx.DiGraph()

for source, target, weight in relations:
    G.add_edge(source, target, weight=weight)

# === 3. Định nghĩa layout tùy chỉnh (cho đẹp và chuẩn SEM) ===
pos = {
    "Body1": (-1, 0.5),
    "Family1": (-1, -0.5),
    "Pain1": (0.5, 0.0),
    "VE": (1.8, 0.0)
}

# === 4. Vẽ node ===
plt.figure(figsize=(9, 6))
node_colors = {
    "Body1": "#4A90E2",
    "Family1": "#7B61FF",
    "Pain1": "#F5A623",
    "VE": "#50E3C2",
}
node_sizes = 2500

nx.draw_networkx_nodes(
    G, pos,
    node_size=node_sizes,
    node_color=[node_colors[n] for n in G.nodes()],
    alpha=0.95,
    edgecolors="white",
    linewidths=1.5
)
nx.draw_networkx_labels(G, pos, font_size=12, font_color="white", font_weight="bold")

# === 5. Vẽ mũi tên và hệ số standardized ===
edges = G.edges(data=True)
edge_labels = {(u, v): f"{d['weight']:.3f}" for u, v, d in edges}

nx.draw_networkx_edges(
    G, pos,
    edgelist=G.edges(),
    width=2.5,
    alpha=0.75,
    arrows=True,
    arrowstyle="-|>",
    min_target_margin=15
)
nx.draw_networkx_edge_labels(
    G, pos, edge_labels=edge_labels,
    font_color="black", font_size=11, font_weight="bold"
)

# === 6. Trang trí ===
plt.title("SEM Path Diagram: Body, Family, Pain → VE", fontsize=14, weight="bold", pad=15)
plt.axis("off")
plt.tight_layout()

# === 7. Lưu ảnh ===
plt.savefig("SEM_Body_Family_Pain_VE.png", dpi=300, bbox_inches="tight")
plt.show()
