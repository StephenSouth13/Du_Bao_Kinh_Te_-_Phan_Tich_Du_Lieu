# Bài Tập 1 – Dự báo Kinh tế & Phân tích Dữ liệu (UEH)

## 📌 Mục tiêu
Triển khai lại toàn bộ bài tập 1 trong môn *Dự báo kinh tế & Phân tích dữ liệu* bằng **Python** thay thế Stata:
- Phân tích dữ liệu mô tả và hồi quy OLS từ `Table1_1.dta`
- Ước lượng mô hình Logit và Probit từ `Table8_1.dta`
- So sánh kết quả hai mô hình nhị phân
- Xuất toàn bộ bảng, hình ảnh, log và báo cáo Word tự động

## 🗂 Cấu trúc dự án
Buoi_6/
│── bai6.py # Main Python script
│── Table1_1.dta # Dữ liệu 1 (OLS)
│── Table8_1.dta # Dữ liệu 2 (Logit/Probit)
│── output/
│ ├── logs/ # File log chi tiết quá trình chạy
│ ├── tables/ # Bảng kết quả CSV (OLS, Logit, Probit, Marginal Effects)
│ ├── figures/ # Hình vẽ (histogram, scatter, residual plots, …)
│ └── reports/ # Báo cáo Word (.docx) tổng hợp

r
Sao chép mã

## ⚙️ Cách chạy
1. Tạo môi trường ảo và cài gói cần thiết:
   ```bash
   pip install -r requirements.txt
(hoặc cài trực tiếp: pandas numpy statsmodels matplotlib seaborn tabulate python-docx)

Chạy script:

bash
Sao chép mã
python bai6.py
Kết quả sẽ xuất hiện trong thư mục output/.

📊 Các bước phân tích
Phần 1 – Descriptive & OLS (Table1_1.dta)
Mô tả dữ liệu

Thống kê mô tả

So sánh mean wage theo giới tính

Crosstab female × nonwhite

Histogram, scatter

T-test, ANOVA

Hồi quy OLS: wage ~ female + nonwhite + union + education + exper

Kiểm định F, VIF, Breusch–Pagan

Phần 2 – Logit & Probit (Table8_1.dta)
Frequency table smoker

Logit regression với biến tương tác (ageedu, eduincome)

Predict probability

Marginal effects (mean & tại điểm cụ thể)

Probit regression

So sánh logit vs probit

📝 Báo cáo
File Word output/reports/report.docx bao gồm:

Mô tả dữ liệu & hình minh họa

Kết quả hồi quy OLS

Kết quả Logit & Probit (bảng hệ số, marginal effects)

So sánh và diễn giải

👨‍💻 Tác giả
Nhóm The Next Generation – UEH

yaml
Sao chép mã
