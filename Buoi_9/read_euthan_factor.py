import pyreadstat
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

# ====== 1️⃣ ĐỌC FILE SPSS ======
file_path = "euthan.sav"
df, meta = pyreadstat.read_sav(file_path)

print("✅ Đọc thành công:")
print(f"📊 Số quan sát (rows): {df.shape[0]}, Số biến (columns): {df.shape[1]}")
print("📋 Một vài biến đầu tiên:", list(df.columns[:10]))
print()

# ====== 2️⃣ CHỌN BIẾN SỐ (LIKERT) ======
likert_cols = [col for col in df.columns if df[col].dtype in ['float64', 'int64']]
df_likert = df[likert_cols]

print(f"🧩 Chọn {len(likert_cols)} biến Likert (dạng số).")

# ====== 3️⃣ CHUẨN HÓA DỮ LIỆU ======
scaler = StandardScaler()
df_scaled = scaler.fit_transform(df_likert)

# ====== 4️⃣ PHÂN TÍCH NHÂN TỐ (PCA) ======
pca = PCA()
pca.fit(df_scaled)

# ====== 5️⃣ VẼ BIỂU ĐỒ SCREE PLOT ======
plt.figure(figsize=(8, 5))
plt.plot(range(1, len(pca.explained_variance_ratio_) + 1),
         pca.explained_variance_ratio_.cumsum(),
         marker='o', linestyle='--')
plt.title('📈 Scree Plot – Tỷ lệ phương sai tích lũy')
plt.xlabel('Số lượng nhân tố (components)')
plt.ylabel('Tỷ lệ phương sai tích lũy')
plt.grid(True)
plt.tight_layout()
plt.savefig("./charts/scree_plot.png", dpi=200)
plt.close()

# ====== 6️⃣ XÁC ĐỊNH SỐ NHÂN TỐ HỢP LÝ (Kaiser Criterion) ======
n_factors = sum(pca.explained_variance_ > 1)
print(f"📊 Số nhân tố có Eigenvalue > 1: {n_factors}")

# ====== 7️⃣ LẤY TẢI NHÂN TỐ (Factor Loadings) ======
loadings = pd.DataFrame(
    pca.components_[:n_factors].T,
    columns=[f"Factor{i+1}" for i in range(n_factors)],
    index=likert_cols
)

# ====== 8️⃣ LƯU BẢNG TẢI NHÂN TỐ ======
loadings_rounded = loadings.round(3)
loadings_rounded.to_excel("euthan_factor_loadings.xlsx", index=True)

print("\n🧾 Bảng tải nhân tố (Factor Loadings – 5 biến đầu):")
print(loadings_rounded.head())

# ====== 9️⃣ VẼ HEATMAP TƯƠNG QUAN ======
corr = df_likert.corr()
plt.figure(figsize=(12, 10))
sns.heatmap(corr, cmap="coolwarm", center=0)
plt.title("🔥 Ma trận tương quan giữa các biến Likert")
plt.tight_layout()
plt.savefig("./charts/correlation_heatmap.png", dpi=200)
plt.close()

# ====== 🔟 GIẢI THÍCH GỢI Ý ======
print("\n💡 Gợi ý diễn giải:")
print(f"- Bạn có thể xem file 'euthan_factor_loadings.xlsx' để nhận diện nhóm biến tải cao vào cùng 1 nhân tố.")
print(f"- Nếu e1–e5 tải mạnh vào Factor1 → nhóm 'Ủng hộ đạo đức'.")
print(f"- Nếu e20–e25 tải vào Factor2 → nhóm 'Phản đối tôn giáo'.")
print(f"- Scree Plot lưu trong './charts/scree_plot.png' giúp bạn xác định số nhân tố hợp lý.")
print(f"- Heatmap tương quan giữa 31 biến lưu trong './charts/correlation_heatmap.png'.")
print("\n📂 File tải nhân tố đã được lưu: euthan_factor_loadings.xlsx")
print("🎯 Phân tích nhân tố hoàn tất!")
