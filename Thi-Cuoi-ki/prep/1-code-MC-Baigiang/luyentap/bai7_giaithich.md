# Monte Carlo 6 chiều cho năng lượng tĩnh điện tự thân của quả cầu tích điện đều

## 1. Bài toán

Ta cần tính tích phân 6 chiều:

$$
I =
\int_{\text{cầu}}
\int_{\text{cầu}}
\frac{1}{|\mathbf r' - \mathbf r|}
, dV , dV'
$$

trong đó:

$$
\mathbf r = (x,y,z)
$$

và:

$$
\mathbf r' = (x',y',z')
$$

là hai điểm bất kỳ nằm trong quả cầu bán kính (R).

Sau khi có (I), ta tính trung bình:

$$
\left\langle
\frac{1}{|\mathbf r' - \mathbf r|}
\right\rangle
=============

\frac{I}{V_{\text{cầu}}^2}
$$

với:

$$
V_{\text{cầu}} = \frac{4}{3}\pi R^3
$$

Đối với quả cầu tích điện đều, năng lượng tĩnh điện tự thân là:

$$
U =
\frac{1}{2}
\frac{Q^2}{4\pi\varepsilon_0}
\left\langle
\frac{1}{|\mathbf r' - \mathbf r|}
\right\rangle
$$

---

## 2. Ý tưởng Monte Carlo

Tích phân cần tính là tích phân theo hai biến vector 3 chiều:

$$
\mathbf r = (x,y,z)
$$

và:

$$
\mathbf r' = (x',y',z')
$$

Do đó bài toán là một tích phân 6 chiều.

Thay vì lấy mẫu trực tiếp trong quả cầu, ta lấy mẫu trong hình hộp bao quanh quả cầu:

$$
x,y,z \in [-R,R]
$$

và:

$$
x',y',z' \in [-R,R]
$$

Như vậy miền lấy mẫu đầy đủ là hình hộp 6 chiều:

$$
[-R,R]^6
$$

Thể tích của hình hộp 6 chiều này là:

$$
V_{\text{hộp 6D}} = (2R)^6
$$

Tuy nhiên, tích phân thật chỉ lấy trên miền:

$$
\text{cầu} \times \text{cầu}
$$

nên ta chỉ cộng những mẫu thỏa mãn đồng thời:

$$
x^2 + y^2 + z^2 \le R^2
$$

và:

$$
{x'}^2 + {y'}^2 + {z'}^2 \le R^2
$$

Tức là cả hai điểm (\mathbf r) và (\mathbf r') đều phải nằm trong quả cầu.

---

## 3. Công thức Monte Carlo dùng trong code

Ta viết tích phân dưới dạng tích phân trên hộp 6 chiều có thêm điều kiện lọc:

$$
I =
\int_{[-R,R]^6}
\chi(\mathbf r,\mathbf r')
\frac{1}{|\mathbf r' - \mathbf r|}
, d^3r , d^3r'
$$

Trong đó:

$$
\chi(\mathbf r,\mathbf r') =
\begin{cases}
1, & \mathbf r \in \text{cầu và } \mathbf r' \in \text{cầu} \
0, & \text{ngược lại}
\end{cases}
$$

Theo Monte Carlo:

$$
I \approx
V_{\text{hộp 6D}}
\frac{1}{N}
\sum_{i=1}^{N}
\chi(\mathbf r_i,\mathbf r_i')
\frac{1}{|\mathbf r_i' - \mathbf r_i|}
$$

Vì:

$$
V_{\text{hộp 6D}} = (2R)^6
$$

nên:

$$
I \approx
(2R)^6
\frac{1}{N}
\sum_{i=1}^{N}
\chi(\mathbf r_i,\mathbf r_i')
\frac{1}{|\mathbf r_i' - \mathbf r_i|}
$$

Trong code, những điểm không nằm trong quả cầu sẽ không được cộng vào tổng. Điều này tương đương với việc nhân thêm hàm chỉ thị (\chi).

---

## 4. Thuật toán

Thuật toán Monte Carlo được thực hiện như sau:

1. Khởi tạo tổng tích phân:

$$
S = 0
$$

2. Lặp (N) lần.

3. Ở mỗi lần lặp, sinh ngẫu nhiên một điểm thứ nhất:

$$
\mathbf r = (x,y,z)
$$

với:

$$
x,y,z \sim U(-R,R)
$$

4. Sinh ngẫu nhiên một điểm thứ hai:

$$
\mathbf r' = (x',y',z')
$$

với:

$$
x',y',z' \sim U(-R,R)
$$

5. Kiểm tra xem cả hai điểm có nằm trong quả cầu hay không:

$$
x^2+y^2+z^2 \le R^2
$$

và:

$$
{x'}^2+{y'}^2+{z'}^2 \le R^2
$$

6. Nếu cả hai điểm đều nằm trong quả cầu, tính khoảng cách:

$$
|\mathbf r' - \mathbf r|
========================

\sqrt{
(x'-x)^2
+
(y'-y)^2
+
(z'-z)^2
}
$$

7. Cộng vào tổng:

$$
S \leftarrow S +
\frac{1}{|\mathbf r' - \mathbf r|}
$$

8. Sau khi lặp xong, tích phân được xấp xỉ bởi:

$$
I \approx
(2R)^6 \frac{S}{N}
$$

9. Tính thể tích quả cầu:

$$
V_{\text{cầu}} =
\frac{4}{3}\pi R^3
$$

10. Tính trung bình:

$$
\left\langle
\frac{1}{|\mathbf r' - \mathbf r|}
\right\rangle
=============

\frac{I}{V_{\text{cầu}}^2}
$$

---

## 5. Code Python

```python
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('sci.mplstyle')
import time

def tinh_MC_quacau(N):
    global R

    tich_phan = 0

    for i in range(N):
        x = np.random.uniform(-R, R)
        y = np.random.uniform(-R, R)
        z = np.random.uniform(-R, R)

        x_prime = np.random.uniform(-R, R)
        y_prime = np.random.uniform(-R, R)
        z_prime = np.random.uniform(-R, R)

        if (
            x**2 + y**2 + z**2 <= R**2
            and
            x_prime**2 + y_prime**2 + z_prime**2 <= R**2
        ):
            dV = 1 / np.sqrt(
                (x_prime - x)**2
                + (y_prime - y)**2
                + (z_prime - z)**2
            )

            tich_phan = tich_phan + dV

    V_hop_6D = (2*R)**6

    I = tich_phan * V_hop_6D / N

    return I
```

Trong đó, biến:

```python
V_hop_6D = (2*R)**6
```

là thể tích của hình hộp 6 chiều bao quanh miền tích phân.

---

## 6. Tính giá trị trung bình

Sau khi tính được tích phân (I), ta chia cho bình phương thể tích quả cầu:

```python
R = 1
N = 10**5

I = tinh_MC_quacau(N)

V_cau = 4/3 * np.pi * R**3

trungbinh_r_prime_minus_r = I / V_cau**2

print("<1/|r' - r|> = ", trungbinh_r_prime_minus_r)
```

Giá trị in ra chính là:

$$
\left\langle
\frac{1}{|\mathbf r' - \mathbf r|}
\right\rangle
$$

---

## 7. So sánh với kết quả giải tích

Với quả cầu bán kính (R), kết quả giải tích là:

$$
\left\langle
\frac{1}{|\mathbf r' - \mathbf r|}
\right\rangle
=============

\frac{6}{5R}
$$

Với (R=1), ta có:

$$
\left\langle
\frac{1}{|\mathbf r' - \mathbf r|}
\right\rangle
=============

# \frac{6}{5}

1.2
$$

Do đó kết quả Monte Carlo nên dao động gần giá trị:

```python
1.2
```

Khi tăng số mẫu (N), sai số thống kê sẽ giảm dần.

---

## 8. Nhận xét về code

Code này đang dùng phương pháp Monte Carlo kiểu ném điểm vào hình hộp bao quanh miền tích phân.

Ưu điểm:

* Dễ hiểu.
* Gần với ý tưởng tích phân Monte Carlo thông thường.
* Không cần sinh trực tiếp điểm đều trong quả cầu.

Nhược điểm:

* Có nhiều điểm bị loại bỏ vì không nằm trong quả cầu.
* Vì đây là tích phân 6 chiều nên số mẫu cần khá lớn để kết quả ổn định.
* Tốc độ hội tụ của Monte Carlo thường có dạng:

$$
\text{sai số} \sim \frac{1}{\sqrt{N}}
$$

Do đó muốn giảm sai số 10 lần thì cần tăng số mẫu khoảng 100 lần.

---

## 9. Kết luận

Bài toán năng lượng tự thân của quả cầu tích điện đều dẫn đến tích phân 6 chiều vì ta phải xét tương tác giữa mọi cặp điểm điện tích trong quả cầu.

Trong code này, mỗi mẫu Monte Carlo gồm một cặp điểm:

$$
(\mathbf r, \mathbf r')
$$

Cả hai điểm đều được sinh trong hình hộp bao quanh quả cầu, sau đó chỉ giữ lại những cặp điểm mà cả hai điểm đều nằm trong quả cầu.

Từ đó ta tính:

$$
I =
\int_{\text{cầu}}
\int_{\text{cầu}}
\frac{1}{|\mathbf r' - \mathbf r|}
, dV , dV'
$$

rồi suy ra:

$$
\left\langle
\frac{1}{|\mathbf r' - \mathbf r|}
\right\rangle
=============

\frac{I}{V_{\text{cầu}}^2}
$$

Kết quả đúng giải tích để kiểm tra chương trình là:

$$
\left\langle
\frac{1}{|\mathbf r' - \mathbf r|}
\right\rangle
=============

\frac{6}{5R}
$$

và với (R=1), kết quả phải gần:

$$
1.2
$$
