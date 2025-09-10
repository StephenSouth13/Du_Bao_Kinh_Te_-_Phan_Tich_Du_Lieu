# 📘 Ghi chú Hồi quy & Biến giả

## 🔹 Phân biệt đa cộng tuyến
- **Đa cộng tuyến (Multicollinearity)** xảy ra khi các biến độc lập trong mô hình hồi quy có quan hệ tuyến tính mạnh với nhau.  
- Ảnh hưởng:
  - Ước lượng hệ số hồi quy không ổn định.
  - Sai số chuẩn lớn → khó kiểm định ý nghĩa thống kê.
- Cách phát hiện:
  - Hệ số **VIF (Variance Inflation Factor)** > 10.
  - Hệ số tương quan giữa các biến độc lập cao.
- Cách xử lý:
  - Loại bỏ biến gây trùng lặp.
  - Sử dụng PCA, Ridge Regression, Lasso.

---

## 🔹 Hồi quy với biến giả (Dummy Variable Regression)

### Trường hợp biến định tính chỉ có **2 lựa chọn (Binary)**
- Ví dụ: Giới tính (Nam = 1, Nữ = 0).
- Mô hình:
Y = β0 + β1*D + ε

- Nếu D = 0 → Y = β0
- Nếu D = 1 → Y = β0 + β1
- 👉 **β1 thể hiện chênh lệch giá trị trung bình giữa 2 nhóm**.

---

## 🔹 Phân biệt 4 mô hình hồi quy và cách sử dụng

1. **Hồi quy tuyến tính đơn (Simple Linear Regression)**


Y = β0 + β1X + ε

- Dùng khi chỉ có 1 biến độc lập.

2. **Hồi quy tuyến tính bội (Multiple Linear Regression)**


Y = β0 + β1X1 + β2X2 + ... + βkXk + ε

- Dùng khi có nhiều biến độc lập định lượng.

3. **Hồi quy với biến giả (Dummy Regression)**
- Dùng để đưa **biến định tính** vào mô hình.
- Ví dụ: Khu vực (TPHCM = 1, Hà Nội = 0).

4. **Hồi quy hỗn hợp (Mixed Regression)**
- Kết hợp cả biến định lượng & biến định tính.
- Ví dụ:
  ```
  Y = β0 + β1*Thu nhập + β2*Giới_tính + ε
  ```

---

## 🔹 Trường hợp biến giả (Dummy Variable Trap)
- Nếu đưa tất cả các biến giả vào mô hình → xảy ra **bẫy biến giả** (hoàn toàn đa cộng tuyến).
- Nguyên tắc:
- Nếu biến định tính có **k nhóm** → chỉ đưa vào **k-1 biến giả**.
- Ví dụ:
- Biến "Khu vực" có 3 giá trị: Bắc, Trung, Nam.
- Ta tạo 2 biến giả:
 - D1 = 1 nếu Trung, 0 nếu khác.
 - D2 = 1 nếu Nam, 0 nếu khác.
- Nhóm Bắc sẽ được mặc định làm **nhóm tham chiếu (base group)**.

---
✨ **Tóm lại:**  
- Đa cộng tuyến làm sai lệch ước lượng.  
- Biến giả giúp mô hình hóa biến định tính.  
- Chỉ dùng `k-1` biến giả cho biến có `k` mức.  
- Chọn đúng loại mô hình hồi quy để phân tích chính xác.