Bộ euthan.sav là dữ liệu khảo sát xã hội về thái độ đối với hành vi “Euthanasia” (an tử).
Mỗi biến e1 → e31 là một phát biểu (statement), và người trả lời đánh giá mức độ đồng ý trên thang Likert 5 mức:

1 = Rất không đồng ý
2 = Không đồng ý
3 = Trung lập
4 = Đồng ý
5 = Rất đồng ý

Vì vậy:

Các biến đều có giá trị trung bình quanh 4, nghĩa là đa số đồng ý hoặc rất đồng ý.

Không có giá trị thiếu → dữ liệu sạch, rất phù hợp cho phân tích nhân tố.

📊 2️⃣ Thống kê mô tả bạn thấy
Biến	Mean	Std	Ý nghĩa
e1	4.01	1.16	Hầu hết đồng ý với phát biểu 1
e2	4.38	0.80	Đồng ý mạnh mẽ hơn nữa
e3	2.86	1.19	Phát biểu 3 có ý kiến chia rẽ, nhiều phản đối
e5	4.37	0.92	Đa số đồng ý mạnh
e9	4.08	1.05	Xu hướng đồng ý khá cao

👉 Như vậy có thể dự đoán các phát biểu e1–e10 thuộc một nhóm thái độ tích cực hoặc “ủng hộ an tử”, trong khi e3 hơi ngược chiều (phản đối).

📈 3️⃣ Gợi ý phân tích nâng cao (bước tiếp theo)

Nếu bạn muốn biến file này thành phiên bản “siêu đỉnh” mở rộng gồm:

Nhận diện thang đo Likert tự động

Phân tích nhân tố khám phá (EFA/PCA)

Xác định nhóm câu hỏi cùng yếu tố

Tạo bảng tương quan + heatmap

Xuất báo cáo PDF hoặc Excel với biểu đồ tự động

→ Mình có thể viết thêm read_euthan_factor.py để thực hiện:

Tự động chọn biến Likert (tất cả e1–e31)

Làm chuẩn hoá dữ liệu (mean=0, sd=1)

Chạy PCA hoặc Factor Analysis

Vẽ biểu đồ scree plot + heatmap

Gợi ý nhóm yếu tố (ví dụ: “Ủng hộ đạo đức”, “Phản đối tôn giáo”, …)
| Thành phần                             | Kết quả                                                                                                                                                                 |
| -------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Số quan sát (rows)**                 | 357                                                                                                                                                                     |
| **Số biến Likert (columns)**           | 31                                                                                                                                                                      |
| **Số nhân tố có Eigenvalue > 1**       | **6 nhân tố**                                                                                                                                                           |
| **Biểu đồ Scree Plot**                 | Lưu tại `./charts/scree_plot.png`                                                                                                                                       |
| **Heatmap tương quan**                 | Lưu tại `./charts/correlation_heatmap.png`                                                                                                                              |
| **Bảng tải nhân tố (Factor Loadings)** | Xuất ra file Excel `euthan_factor_loadings.xlsx`                                                                                                                        |
| **Gợi ý nhóm nhân tố**                 | - Factor1: nhóm biến e1–e5 → “Ủng hộ đạo đức”<br> - Factor2: nhóm e20–e25 → “Phản đối tôn giáo”<br> - (Các nhóm khác có thể đọc từ Excel để đặt tên theo tải mạnh nhất) |
