# Điện thế của hình xuyến tích điện đều bằng tổng Riemann và Monte Carlo

## 1. Bài toán

Ta có một **hình xuyến tích điện đều** với:

- Bán kính lớn: \(R\)
- Bán kính ống nhỏ: \(r\)
- Tổng điện tích: \(Q\)
- Hằng số Coulomb:

\[
k=\frac{1}{4\pi\varepsilon_0}
\]

Cần tính điện thế tại điểm \(P\) nằm trên trục \(z\):

\[
P=(0,0,d)
\]

Trong bài:

\[
R=5,\qquad r=1,\qquad Q=10^{-6},\qquad k\approx 8.99\times 10^9
\]

---

## 2. Điều kiện một điểm nằm trong hình xuyến

Một điểm nguồn điện tích có tọa độ:

\[
\mathbf r'=(x,y,z)
\]

nằm trong hình xuyến nếu thỏa:

\[
\left(R-\sqrt{x^2+y^2}\right)^2+z^2 \le r^2
\]

Đây là điều kiện quan trọng nhất trong code.

---

## 3. Thể tích hình xuyến

Thể tích hình xuyến là:

\[
V_{\text{xuyến}} = 2\pi^2 Rr^2
\]

Với \(R=5,\ r=1\):

\[
V_{\text{xuyến}} = 10\pi^2
\]

Vì điện tích phân bố đều nên mật độ điện tích là:

\[
\rho = \frac{Q}{V_{\text{xuyến}}}
\]

---

## 4. Công thức điện thế

Điện thế tại điểm \(P=(0,0,d)\) là:

\[
V(d)=k\iiint_{\text{xuyến}}
\frac{\rho}{|\mathbf P-\mathbf r'|}\,dV'
\]

Trong đó:

\[
|\mathbf P-\mathbf r'|
=
\sqrt{x^2+y^2+(z-d)^2}
\]

Do đó:

\[
V(d)
=
k\rho
\iiint_{\text{xuyến}}
\frac{dxdydz}
{\sqrt{x^2+y^2+(z-d)^2}}
\]

---

# Phương pháp 1: Tổng Riemann

## 5. Ý tưởng

Ta chia miền không gian thành một lưới đều.

Vì hình xuyến nằm trong hộp:

\[
x\in[-(R+r),R+r]
\]

\[
y\in[-(R+r),R+r]
\]

\[
z\in[-r,r]
\]

nên ta quét các điểm trong hộp này.

Nhưng **chỉ cộng các điểm nằm trong hình xuyến**.

---

## 6. Công thức Riemann

Gọi thể tích mỗi ô nhỏ là:

\[
\Delta V = \Delta x \Delta y \Delta z
\]

Khi đó:

\[
V(d)
\approx
k\rho
\sum_{\text{điểm trong hình xuyến}}
\frac{\Delta V}
{\sqrt{x_i^2+y_i^2+(z_i-d)^2}}
\]

Trong đó điều kiện điểm thuộc hình xuyến là:

\[
\left(R-\sqrt{x_i^2+y_i^2}\right)^2+z_i^2 \le r^2
\]

---

## 7. Pseudocode Riemann

```python
V = 0

for x in xs:
    for y in ys:
        for z in zs:

            inside = (R - sqrt(x*x + y*y))**2 + z*z <= r*r

            if inside:
                distance = sqrt(x*x + y*y + (z - d)**2)
                V += dV / distance

V = k * rho * V
```

---

# Phương pháp 2: Monte Carlo

## 8. Ý tưởng

Monte Carlo không quét lưới đều.

Ta gieo ngẫu nhiên \(N\) điểm trong hộp bao hình xuyến:

\[
[-(R+r),R+r]\times[-(R+r),R+r]\times[-r,r]
\]

Sau đó chỉ giữ lại các điểm nằm trong hình xuyến.

---

## 9. Công thức Monte Carlo theo điểm trong hình xuyến

Nếu ta có \(N_{\text{in}}\) điểm ngẫu nhiên nằm trong hình xuyến, thì:

\[
V(d)
\approx
k\frac{Q}{N_{\text{in}}}
\sum_{i=1}^{N_{\text{in}}}
\frac{1}
{\sqrt{x_i^2+y_i^2+(z_i-d)^2}}
\]

Đây là dạng rất tiện vì không cần nhân thêm thể tích hình xuyến.

Lý do là:

\[
\rho=\frac{Q}{V_{\text{xuyến}}}
\]

và:

\[
\iiint_{\text{xuyến}} f(\mathbf r')\,dV'
\approx
V_{\text{xuyến}}
\frac{1}{N_{\text{in}}}
\sum_i f_i
\]

nên:

\[
k\rho V_{\text{xuyến}}
\frac{1}{N_{\text{in}}}
\sum_i f_i
=
k\frac{Q}{N_{\text{in}}}
\sum_i f_i
\]

---

## 10. Công thức Monte Carlo theo hộp bao

Cũng có thể viết trực tiếp theo hộp bao.

Thể tích hộp là:

\[
V_{\text{box}} = 2(R+r)\cdot 2(R+r)\cdot 2r
\]

Nếu gieo \(N\) điểm trong hộp, dùng hàm chỉ thị:

\[
I_i=
\begin{cases}
1, & \text{nếu điểm nằm trong hình xuyến}\\
0, & \text{nếu điểm nằm ngoài hình xuyến}
\end{cases}
\]

thì:

\[
V(d)
\approx
k\rho V_{\text{box}}
\frac{1}{N}
\sum_{i=1}^{N}
\frac{I_i}
{\sqrt{x_i^2+y_i^2+(z_i-d)^2}}
\]

Hai cách Monte Carlo này tương đương.

---

## 11. Pseudocode Monte Carlo

```python
sum_f = 0
Nin = 0

for i in range(N):

    x = random_uniform(-(R+r), R+r)
    y = random_uniform(-(R+r), R+r)
    z = random_uniform(-r, r)

    inside = (R - sqrt(x*x + y*y))**2 + z*z <= r*r

    if inside:
        distance = sqrt(x*x + y*y + (z - d)**2)
        sum_f += 1 / distance
        Nin += 1

V = k * Q * sum_f / Nin
```

---

# 12. So sánh Riemann và Monte Carlo

## Tổng Riemann

Ưu điểm:

- Dễ hiểu
- Kết quả ổn định
- Không có nhiễu ngẫu nhiên

Nhược điểm:

- Rất chậm trong không gian 3 chiều
- Nếu mỗi chiều lấy \(n\) điểm thì tổng số điểm là:

\[
N_{\text{grid}} = n^3
\]

Ví dụ \(n=300\):

\[
N_{\text{grid}} = 27\,000\,000
\]

rất tốn thời gian.

---

## Monte Carlo

Ưu điểm:

- Dễ áp dụng cho hình phức tạp
- Không cần tạo lưới dày
- Tốt cho tích phân nhiều chiều

Nhược điểm:

- Có sai số ngẫu nhiên
- Sai số giảm chậm:

\[
\text{sai số} \sim \frac{1}{\sqrt{N}}
\]

Muốn sai số giảm 10 lần thì cần tăng số điểm lên 100 lần.

---

# 13. Các điểm \(P\) trên trục \(z\)

Bài yêu cầu lấy 100 điểm \(P\) trên trục \(z\).

Ta có thể chọn:

\[
d\in[d_{\min},d_{\max}]
\]

Ví dụ:

\[
d\in[-10,10]
\]

Với mỗi giá trị \(d\), tính:

\[
V(d)
\]

rồi xuất dữ liệu ra file:

```text
d    V_Riemann    V_MC
```

Sau đó dùng Python hoặc Gnuplot để vẽ đồ thị.

---

# 14. Dạng dữ liệu xuất ra file

Ví dụ file `torus_potential.dat`:

```text
# d        V_Riemann        V_MC
-10.0      ...
-9.8       ...
-9.6       ...
...
10.0       ...
```

---

# 15. Gnuplot mẫu

```gnuplot
set xlabel "z"
set ylabel "V(z)"
set grid
set title "Dien the tren truc z cua hinh xuyen tich dien deu"

plot "torus_potential.dat" using 1:2 with lines title "Riemann", \
     "torus_potential.dat" using 1:3 with points title "Monte Carlo"
```

---

# 16. Ghi chú quan trọng

Không được lấy tổng trên toàn hộp nếu không nhân hàm chỉ thị.

Nói cách khác, tích phân đúng là trên hình xuyến:

\[
\iiint_{\text{xuyến}}
\]

chứ không phải trên toàn hộp.

Nếu quét toàn hộp, phải dùng:

\[
I(x,y,z)
\]

để loại các điểm nằm ngoài hình xuyến.

---

# 17. Tóm tắt công thức cần nhớ

Điều kiện hình xuyến:

\[
\left(R-\sqrt{x^2+y^2}\right)^2+z^2 \le r^2
\]

Khoảng cách đến điểm \(P=(0,0,d)\):

\[
s=\sqrt{x^2+y^2+(z-d)^2}
\]

Tổng Riemann:

\[
V(d)
\approx
k\rho
\sum_{\text{inside}}
\frac{\Delta V}{s_i}
\]

Monte Carlo:

\[
V(d)
\approx
k\frac{Q}{N_{\text{in}}}
\sum_{\text{inside}}
\frac{1}{s_i}
\]

với:

\[
\rho=\frac{Q}{2\pi^2Rr^2}
\]
