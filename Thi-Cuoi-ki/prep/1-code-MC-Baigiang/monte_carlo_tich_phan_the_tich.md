# Monte Carlo trong tích phân và tính thể tích

## 1. Ý tưởng chính

Phương pháp Monte Carlo dùng số ngẫu nhiên để xấp xỉ một đại lượng toán học hoặc vật lý.

Trong tích phân, thay vì chia miền thành lưới đều như phương pháp số thông thường, ta lấy mẫu ngẫu nhiên nhiều điểm trong miền cần tính, rồi lấy trung bình giá trị hàm tại các điểm đó.

Nếu số điểm lấy mẫu đủ lớn, kết quả Monte Carlo sẽ tiến gần đến giá trị đúng.

---

## 2. Tích phân một chiều

Giả sử cần tính

$$
I = \int_a^b f(x)\,dx.
$$

Ta sinh ngẫu nhiên $N$ điểm $x_i$ phân bố đều trong đoạn $[a,b]$.

Khi đó

$$
I \approx (b-a)\frac{1}{N}\sum_{i=1}^N f(x_i).
$$

Nói cách khác:

$$
I \approx \text{độ dài miền} \times \text{giá trị trung bình của hàm}.
$$

### Code Python

```python
import numpy as np

N = 100000
a = 0
b = 1

x = np.random.uniform(a, b, N)
f = x**2

I = (b - a) * np.mean(f)
print(I)
```

Giá trị đúng là

$$
\int_0^1 x^2 dx = \frac{1}{3}.
$$

---

## 3. Tích phân nhiều chiều

Với tích phân ba chiều:

$$
I = \int_{x_1}^{x_2}\int_{y_1}^{y_2}\int_{z_1}^{z_2} f(x,y,z)\,dz\,dy\,dx.
$$

Thể tích hộp lấy mẫu là

$$
V_{box} = (x_2-x_1)(y_2-y_1)(z_2-z_1).
$$

Sinh ngẫu nhiên các điểm $(x_i,y_i,z_i)$ trong hộp đó. Khi đó

$$
I \approx V_{box}\frac{1}{N}\sum_{i=1}^N f(x_i,y_i,z_i).
$$

### Code Python

```python
import numpy as np

N = 100000

x1, x2 = -1, 1
y1, y2 = -1, 1
z1, z2 = -1, 1

x = np.random.uniform(x1, x2, N)
y = np.random.uniform(y1, y2, N)
z = np.random.uniform(z1, z2, N)

f = x**2 + y**2 + z**2

Vbox = (x2 - x1) * (y2 - y1) * (z2 - z1)
I = Vbox * np.mean(f)

print(I)
```

---

## 4. Tính thể tích hình bất kỳ bằng Monte Carlo

Giả sử có một vật thể nằm trong hộp chữ nhật. Ta muốn tính thể tích của vật thể đó.

Ý tưởng:

1. Bao vật thể bằng một hộp đơn giản.
2. Sinh ngẫu nhiên $N$ điểm trong hộp.
3. Đếm số điểm rơi vào bên trong vật thể.
4. Lấy tỉ lệ điểm bên trong nhân với thể tích hộp.

Nếu $N_{in}$ là số điểm nằm trong vật thể, thì

$$
V \approx V_{box}\frac{N_{in}}{N}.
$$

---

## 5. Hàm chỉ thị

Ta có thể viết thể tích dưới dạng tích phân:

$$
V = \iiint \chi(x,y,z)\,dV,
$$

trong đó $\chi$ là hàm chỉ thị:

$$
\chi(x,y,z)=
\begin{cases}
1, & \text{nếu điểm nằm trong vật thể},\\
0, & \text{nếu điểm nằm ngoài vật thể}.
\end{cases}
$$

Khi đó Monte Carlo cho ta:

$$
V \approx V_{box}\langle \chi \rangle.
$$

Vì $\langle \chi \rangle = N_{in}/N$, nên công thức trở thành

$$
V \approx V_{box}\frac{N_{in}}{N}.
$$

---

## 6. Ví dụ: thể tích hình cầu

Hình cầu bán kính $R$ được xác định bởi

$$
x^2+y^2+z^2 \le R^2.
$$

Ta bao hình cầu bằng hộp:

$$
x,y,z \in [-R,R].
$$

Thể tích hộp là

$$
V_{box} = (2R)^3 = 8R^3.
$$

Code Monte Carlo:

```python
import numpy as np

R = 1.0
N = 1000000

x = np.random.uniform(-R, R, N)
y = np.random.uniform(-R, R, N)
z = np.random.uniform(-R, R, N)

inside = x**2 + y**2 + z**2 <= R**2
Nin = np.sum(inside)

Vbox = (2 * R)**3
V_MC = Vbox * Nin / N

print("Monte Carlo:", V_MC)
print("Exact:", 4/3 * np.pi * R**3)
```

Giá trị chính xác là

$$
V = \frac{4}{3}\pi R^3.
$$

---

## 7. Ví dụ: hình trụ

Hình trụ bán kính $R$, chiều cao $h$:

$$
x^2+y^2 \le R^2,
$$

và

$$
-\frac{h}{2} \le z \le \frac{h}{2}.
$$

Ta có thể bao nó bằng hộp:

$$
x,y \in [-R,R], \qquad z\in[-h/2,h/2].
$$

Code:

```python
import numpy as np

R = 1.0
h = 2.0
N = 1000000

x = np.random.uniform(-R, R, N)
y = np.random.uniform(-R, R, N)
z = np.random.uniform(-h/2, h/2, N)

inside = x**2 + y**2 <= R**2
Nin = np.sum(inside)

Vbox = (2 * R) * (2 * R) * h
V_MC = Vbox * Nin / N

print("Monte Carlo:", V_MC)
print("Exact:", np.pi * R**2 * h)
```

Giá trị đúng là

$$
V = \pi R^2h.
$$

---

## 8. Sai số Monte Carlo

Sai số của Monte Carlo thường giảm theo quy luật

$$
\text{sai số} \sim \frac{1}{\sqrt{N}}.
$$

Điều này nghĩa là nếu muốn sai số giảm 10 lần, ta cần tăng số điểm lên 100 lần.

Ví dụ:

- $N = 10^4$: sai số cỡ $10^{-2}$
- $N = 10^6$: sai số cỡ $10^{-3}$
- $N = 10^8$: sai số cỡ $10^{-4}$

Monte Carlo hội tụ chậm, nhưng rất hữu ích cho tích phân nhiều chiều vì không bị nổ số điểm như phương pháp chia lưới thông thường.

---

## 9. Tổng kết

Công thức quan trọng nhất:

$$
I \approx V_{domain}\frac{1}{N}\sum_{i=1}^N f(\mathbf r_i).
$$

Với tính thể tích:

$$
V \approx V_{box}\frac{N_{in}}{N}.
$$

Trong đó:

- $V_{box}$ là thể tích hộp bao ngoài.
- $N$ là tổng số điểm lấy mẫu.
- $N_{in}$ là số điểm nằm trong vật thể.
- Điều kiện `inside` quyết định điểm có nằm trong hình hay không.

Monte Carlo đặc biệt mạnh khi miền tích phân phức tạp hoặc số chiều lớn.
