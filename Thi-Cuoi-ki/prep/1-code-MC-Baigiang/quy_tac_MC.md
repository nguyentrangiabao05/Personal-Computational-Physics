# Quy tắc Monte Carlo cho tích phân trên miền quan tâm

Cần tính:

$$
I = \rho \int_{\Omega} f(x,y,z),dV
$$

với:

$$
f(x,y,z)=x^2+y^2
$$

Trong đó:

* (\Omega): miền quan tâm
* (D): vùng bao, với (\Omega \subset D)
* (V_\Omega): thể tích miền quan tâm
* (V_D): thể tích vùng bao

---

## 1. Nếu lấy mẫu trực tiếp trong miền quan tâm

Nếu các điểm random đều nằm trong (\Omega), thì:

$$
I \approx \rho \frac{V_\Omega}{N_\Omega}
\sum_{i=1}^{N_\Omega} f(x_i,y_i,z_i)
$$

Tức là:

$$
I \approx \rho \frac{V_\Omega}{N_\Omega}
\sum_{i=1}^{N_\Omega} (x_i^2+y_i^2)
$$

---

## 2. Nếu lấy mẫu trong vùng bao

Nếu random điểm trong vùng bao (D), rồi chỉ lấy các điểm thuộc (\Omega), thì:

$$
I \approx \rho \frac{V_D}{N_D}
\sum_{\text{điểm thuộc } \Omega} (x_i^2+y_i^2)
$$

Hoặc viết bằng hàm chỉ thị:

$$
I \approx \rho \frac{V_D}{N_D}
\sum_{i=1}^{N_D}
(x_i^2+y_i^2)\chi_\Omega(x_i,y_i,z_i)
$$

với:

$$
\chi_\Omega =
\begin{cases}
1, & \text{nếu điểm thuộc } \Omega \
0, & \text{nếu điểm ngoài } \Omega
\end{cases}
$$

---

## Ghi nhớ

Không dùng:

$$
\rho \frac{V_D}{N_D}
\sum_{\text{mọi điểm trong } D} (x_i^2+y_i^2)
$$

vì công thức này tính tích phân trên toàn vùng bao (D), không phải trên miền quan tâm (\Omega).
