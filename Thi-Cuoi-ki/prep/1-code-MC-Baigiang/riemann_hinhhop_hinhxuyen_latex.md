# Tổng Riemann cho hai hình dạng: hình hộp và hình xuyến

## 1. Ý tưởng chung

Điện thế tại điểm quan sát \(P=(0,0,d)\) do một vật tích điện đều gây ra là

$$
V(d)=k\rho \iiint_{\Omega}
\frac{dV'}{\sqrt{x^2+y^2+(z-d)^2}}.
$$

Trong đó:

- \(\Omega\) là miền vật thể tích điện.
- \(\rho\) là mật độ điện tích đều.
- \(k=\dfrac{1}{4\pi\varepsilon_0}\).
- \((x,y,z)\) là tọa độ điểm nguồn điện tích.
- \(d\) là tọa độ điểm quan sát trên trục \(z\).

Tổng Riemann thay tích phân bằng tổng trên lưới:

$$
V(d)\approx
k\rho
\sum_{\Omega}
\frac{\Delta V}
{\sqrt{x_i^2+y_j^2+(z_k-d)^2}},
$$

với

$$
\Delta V=\Delta x\,\Delta y\,\Delta z.
$$

---

# Phần A. Tổng Riemann cho hình hộp

## 2. Miền hình hộp

Giả sử hình hộp có kích thước

$$
R\times R\times h
$$

và được đặt tâm tại gốc tọa độ. Khi đó:

$$
x\in\left[-\frac{R}{2},\frac{R}{2}\right],
$$

$$
y\in\left[-\frac{R}{2},\frac{R}{2}\right],
$$

$$
z\in\left[-\frac{h}{2},\frac{h}{2}\right].
$$

Thể tích hình hộp là

$$
V_{\mathrm{box}}=R^2h.
$$

Nếu tổng điện tích là \(Q\), mật độ điện tích đều là

$$
\rho=\frac{Q}{R^2h}.
$$

---

## 3. Công thức Riemann cho hình hộp

Điện thế tại \(P=(0,0,d)\):

$$
V_{\mathrm{box}}(d)
=
k\rho
\iiint_{\mathrm{box}}
\frac{dxdydz}
{\sqrt{x^2+y^2+(z-d)^2}}.
$$

Tổng Riemann:

$$
V_{\mathrm{box}}(d)
\approx
k\rho
\sum_{i,j,k}
\frac{\Delta x\,\Delta y\,\Delta z}
{\sqrt{x_i^2+y_j^2+(z_k-d)^2}}.
$$

Vì toàn bộ lưới nằm trong hình hộp nên không cần điều kiện lọc điểm.

---

## 4. Code Python cho hình hộp

```python
import numpy as np

def tinh_Riemann_hinhhop(d, N):
    global k0, Q, R, h

    rho = Q/(R**2*h)

    x_arr = np.linspace(-R/2, R/2, N)
    y_arr = np.linspace(-R/2, R/2, N)
    z_arr = np.linspace(-h/2, h/2, N)

    dx = x_arr[1] - x_arr[0]
    dy = y_arr[1] - y_arr[0]
    dz = z_arr[1] - z_arr[0]

    dV = dx*dy*dz

    V = 0.0

    for x in x_arr:
        for y in y_arr:
            for z in z_arr:
                distance = np.sqrt(x**2 + y**2 + (z-d)**2)
                V += dV/distance

    V = k0*rho*V
    return V
```

---

# Phần B. Tổng Riemann cho hình xuyến

## 5. Miền hình xuyến

Hình xuyến có:

- Bán kính lớn: \(R\)
- Bán kính ống nhỏ: \(r\)

Một điểm \((x,y,z)\) nằm trong hình xuyến nếu thỏa điều kiện

$$
\left(R-\sqrt{x^2+y^2}\right)^2+z^2\le r^2.
$$

Trong Python:

```python
(R - np.sqrt(x**2 + y**2))**2 + z**2 <= r**2
```

---

## 6. Hộp bao hình xuyến

Hình xuyến nằm trong hộp bao:

$$
x\in[-(R+r),R+r],
$$

$$
y\in[-(R+r),R+r],
$$

$$
z\in[-r,r].
$$

Khác với hình hộp, ta không cộng tất cả điểm trong hộp bao. Ta chỉ cộng các điểm thỏa điều kiện hình xuyến.

---

## 7. Thể tích và mật độ điện tích của hình xuyến

Thể tích hình xuyến là

$$
V_{\mathrm{torus}}=2\pi^2Rr^2.
$$

Nếu tổng điện tích là \(Q\), mật độ điện tích đều là

$$
\rho=\frac{Q}{2\pi^2Rr^2}.
$$

---

## 8. Công thức Riemann cho hình xuyến

Điện thế tại \(P=(0,0,d)\):

$$
V_{\mathrm{torus}}(d)
=
k\rho
\iiint_{\mathrm{torus}}
\frac{dxdydz}
{\sqrt{x^2+y^2+(z-d)^2}}.
$$

Tổng Riemann:

$$
V_{\mathrm{torus}}(d)
\approx
k\rho
\sum_{\mathrm{inside}}
\frac{\Delta x\,\Delta y\,\Delta z}
{\sqrt{x_i^2+y_j^2+(z_k-d)^2}}.
$$

Trong đó \(\mathrm{inside}\) nghĩa là điểm lưới thỏa

$$
\left(R-\sqrt{x_i^2+y_j^2}\right)^2+z_k^2\le r^2.
$$

---

## 9. Code Python cho hình xuyến

```python
import numpy as np

def hinhxuyen(x, y, z):
    global R, r
    return (R - np.sqrt(x**2 + y**2))**2 + z**2

def tinh_Riemann_hinhxuyen(d, N):
    global k0, Q, R, r

    rho = Q/(2*np.pi**2*R*r**2)

    x_arr = np.linspace(-(R+r), R+r, N)
    y_arr = np.linspace(-(R+r), R+r, N)
    z_arr = np.linspace(-r, r, N)

    dx = x_arr[1] - x_arr[0]
    dy = y_arr[1] - y_arr[0]
    dz = z_arr[1] - z_arr[0]

    dV = dx*dy*dz

    V = 0.0

    for x in x_arr:
        for y in y_arr:
            for z in z_arr:

                inside = hinhxuyen(x, y, z) <= r**2

                if inside:
                    distance = np.sqrt(x**2 + y**2 + (z-d)**2)
                    V += dV/distance

    V = k0*rho*V
    return V
```

---

# 10. So sánh hai trường hợp

## Hình hộp

Miền tích phân chính là hình hộp:

$$
\left[-\frac{R}{2},\frac{R}{2}\right]
\times
\left[-\frac{R}{2},\frac{R}{2}\right]
\times
\left[-\frac{h}{2},\frac{h}{2}\right].
$$

Do đó ta cộng mọi điểm lưới:

```python
V += dV/distance
```

---

## Hình xuyến

Ta tạo lưới trong hộp bao:

$$
[-(R+r),R+r]
\times
[-(R+r),R+r]
\times
[-r,r].
$$

Nhưng chỉ cộng nếu

$$
\left(R-\sqrt{x^2+y^2}\right)^2+z^2\le r^2.
$$

Do đó trong code phải có:

```python
if inside:
    V += dV/distance
```

---

# 11. Khảo sát nhiều điểm trên trục \(z\)

Nếu cần khảo sát \(N_d\) điểm trên trục \(z\):

```python
N_d = 100
d_arr = np.linspace(d_min, d_max, N_d)

V_hop = np.zeros(N_d)
V_xuyen = np.zeros(N_d)

for i in range(N_d):
    V_hop[i] = tinh_Riemann_hinhhop(d_arr[i], N)
    V_xuyen[i] = tinh_Riemann_hinhxuyen(d_arr[i], N)
```

---

# 12. Lưu dữ liệu ra file

```python
data = np.column_stack((d_arr, V_hop, V_xuyen))

np.savetxt(
    "riemann_hop_xuyen.dat",
    data,
    header="d    V_hinh_hop    V_hinh_xuyen"
)
```

---

# 13. Gnuplot mẫu

```gnuplot
set xlabel "d"
set ylabel "V(d)"
set grid
set title "Dien the tinh bang tong Riemann"

plot "riemann_hop_xuyen.dat" using 1:2 with lines title "Hinh hop", \
     "riemann_hop_xuyen.dat" using 1:3 with lines title "Hinh xuyen"
```

---

# 14. Lưu ý quan trọng

## Với hình hộp

Phải nhân phần tử thể tích:

$$
\Delta V=\Delta x\,\Delta y\,\Delta z.
$$

Nếu thiếu \(\Delta V\), kết quả sẽ sai đơn vị và sai độ lớn.

---

## Với hình xuyến

Không được cộng toàn bộ hộp bao. Phải kiểm tra điều kiện:

$$
\left(R-\sqrt{x^2+y^2}\right)^2+z^2\le r^2.
$$

Nếu không lọc điều kiện này thì bạn đang tính điện thế của cả hộp bao, không phải hình xuyến.

---

# 15. Tóm tắt công thức

## Hình hộp

$$
V_{\mathrm{box}}(d)
\approx
k\frac{Q}{R^2h}
\sum_{i,j,k}
\frac{\Delta V}
{\sqrt{x_i^2+y_j^2+(z_k-d)^2}}.
$$

## Hình xuyến

$$
V_{\mathrm{torus}}(d)
\approx
k\frac{Q}{2\pi^2Rr^2}
\sum_{\mathrm{inside}}
\frac{\Delta V}
{\sqrt{x_i^2+y_j^2+(z_k-d)^2}}.
$$

với

$$
\left(R-\sqrt{x_i^2+y_j^2}\right)^2+z_k^2\le r^2.
$$
