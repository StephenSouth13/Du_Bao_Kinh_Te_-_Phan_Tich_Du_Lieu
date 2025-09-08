# 📝 Buổi 4 - Dự báo bằng mô hình nhân quả sản lượng (CPQC, Hoa hồng)

## 1️⃣ Mục tiêu
- Thực hành các phương pháp dự báo trong môn **Dự báo Kinh tế - Phân tích Dữ liệu**:
  - Q1: Hồi quy xu thế (Trend Regression).
  - Q2a: San bằng mũ (ETS) cho sản lượng.
  - Q2b: San bằng mũ (ETS) cho biến nguyên nhân (CPQC, Hoa hồng).
  - Q3: Hồi quy đa biến (t, CPQC, Hoahong, biến giả Q2–Q4).
  - Q4: So sánh mô hình (2) và (3) bằng MAPE holdout, AIC, R² và đưa ra khuyến nghị.

---

## 2️⃣ Cách chạy
1. Cài thư viện (một lần):
   ```bash
   pip install pandas numpy matplotlib scikit-learn statsmodels pyreadstat fpdf python-pptx pillow
Chạy script Python:

python buoi4.py --sav "Du bao bang mo hinh nhan qua san luong _ CPQC Hoahong quy.sav" --h 4 --outdir outputs


--sav : đường dẫn tới file .sav (phải đúng tên).

--h : số quý cần dự báo (default = 4).

--outdir : thư mục lưu kết quả (default = outputs).

3️⃣ Xem kết quả ở đâu?

Sau khi chạy xong, tất cả kết quả được lưu trong thư mục outputs/:

📈 Biểu đồ PNG:

q1_trend_regression.png → Hồi quy xu thế

q2a_ets_sanluong.png → ETS cho sản lượng

q2b_ets_cpqc.png, q2b_ets_hoahong.png → ETS cho CPQC, Hoa hồng

q3_multireg_forecast.png → Hồi quy đa biến

📊 Bảng & Kết quả:

q1_ols_summary.txt, q3_ols_summary.txt, q4_model2_summary.txt, q4_model3_summary.txt → Thông số mô hình OLS

q2a_sanluong_forecast.csv, q3_sanluong_forecast.csv → Dự báo giá trị tương lai

metrics_summary.csv → Bảng so sánh MAPE, Adj R², AIC giữa các mô hình

📑 Báo cáo:

report.pdf → Báo cáo tự động (có biểu đồ, bảng số liệu, kết luận)

report.pptx → Slide PowerPoint trình bày

4️⃣ Diễn giải nhanh (console output)

Khi chạy xong, màn hình sẽ in:

Khuyến nghị mô hình (Q4): chọn model nào dự báo tốt hơn.

Phương trình xu thế (Q1) dạng:

Sanluong = a + b*t + e


✅ Như vậy, bạn chỉ cần:

Mở file report.pdf nếu muốn đọc nhanh toàn bộ kết quả,

Hoặc mở thư mục outputs/ để coi chi tiết từng file (biểu đồ, CSV, TXT).