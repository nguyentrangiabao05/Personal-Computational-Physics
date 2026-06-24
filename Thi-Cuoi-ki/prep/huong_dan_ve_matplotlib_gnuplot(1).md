# Hướng dẫn vẽ tọa độ cực, 2D line, 3D line, heatmap bằng Matplotlib và Gnuplot

Tài liệu này dùng cho Computational Physics: vẽ dữ liệu số, nghiệm ODE/PDE, bản đồ nhiệt, quỹ đạo pha và quỹ đạo chaos. Mỗi phần có ví dụ bằng **Python/Matplotlib** và **Gnuplot**.

---

## 0. Chuẩn bị môi trường

### Python

Cài thư viện:

```bash
pip install numpy matplotlib
```

Cấu trúc cơ bản:

```python
import numpy as np
import matplotlib.pyplot as plt
```

Lưu hình:

```python
plt.savefig("figure.png", dpi=300, bbox_inches="tight")
plt.savefig("figure.pdf", bbox_inches="tight")
```

### Gnuplot

Cài trên Ubuntu/Linux:

```bash
sudo apt install gnuplot
```

Chạy file script:

```bash
gnuplot plot.gp
```

Xuất hình PNG/PDF thường dùng:

```gnuplot
set terminal pngcairo size 1200,900 enhanced font "Arial,18"
set output "figure.png"
```

hoặc:

```gnuplot
set terminal pdfcairo enhanced color font "Arial,14"
set output "figure.pdf"
```

---

# 1. Vẽ đồ thị đường 2D line

## 1.1 Ý tưởng

Đồ thị 2D line dùng để vẽ một hàm hoặc dữ liệu dạng:

\[
y = f(x)
\]

Ví dụ trong vật lý:

- Dao động điều hòa: \(x(t)=A\cos(\omega t)\)
- Phân rã phóng xạ: \(N(t)=N_0e^{-\lambda t}\)
- Nhiệt độ tại một điểm theo thời gian
- Nghiệm số ODE bằng Euler/RK4

---

## 1.2 Matplotlib: vẽ hàm sin và cos

```python
import numpy as np
import matplotlib.pyplot as plt

# Tạo mảng thời gian
t = np.linspace(0, 10, 1000)

# Hai hàm cần vẽ
y1 = np.sin(t)
y2 = np.cos(t)

plt.figure(figsize=(8, 5))
plt.plot(t, y1, label=r"$\sin(t)$", linewidth=2)
plt.plot(t, y2, label=r"$\cos(t)$", linewidth=2, linestyle="--")

plt.xlabel("t")
plt.ylabel("y")
plt.title("Đồ thị 2D line: sin và cos")
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig("line2d_matplotlib.png", dpi=300)
plt.show()
```

---

## 1.3 Gnuplot: vẽ hàm sin và cos

Tạo file `line2d.gp`:

```gnuplot
set terminal pngcairo size 1200,800 enhanced font "Arial,18"
set output "line2d_gnuplot.png"

set title "Đồ thị 2D line: sin và cos"
set xlabel "t"
set ylabel "y"
set grid
set key top right

plot sin(x) with lines linewidth 3 title "sin(t)", \
     cos(x) with lines linewidth 3 dashtype 2 title "cos(t)"
```

Chạy:

```bash
gnuplot line2d.gp
```

---

## 1.4 Đọc dữ liệu từ file rồi vẽ

Giả sử file `data.txt` có dạng:

```text
# t     y
0.0     0.0
0.1     0.0998
0.2     0.1987
```

### Matplotlib

```python
import numpy as np
import matplotlib.pyplot as plt

t, y = np.loadtxt("data.txt", comments="#", unpack=True)

plt.figure(figsize=(8, 5))
plt.plot(t, y, "o-", label="data")
plt.xlabel("t")
plt.ylabel("y")
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig("data_line2d.png", dpi=300)
plt.show()
```

### Gnuplot

```gnuplot
set terminal pngcairo size 1200,800 enhanced font "Arial,18"
set output "data_line2d_gnuplot.png"

set xlabel "t"
set ylabel "y"
set grid

plot "data.txt" using 1:2 with linespoints linewidth 2 pointtype 7 title "data"
```

---

# 2. Vẽ tọa độ cực polar plot

## 2.1 Ý tưởng

Tọa độ cực dùng hai biến:

\[
r = r(\theta)
\]

trong đó:

- \(r\): bán kính
- \(\theta\): góc

Ứng dụng:

- Quỹ đạo hành tinh gần tròn
- Hình hoa thị
- Mẫu bức xạ anten
- Dao động góc
- Phân bố cường độ theo hướng

---

## 2.2 Matplotlib: vẽ hình hoa thị

Ví dụ:

\[
r(\theta)=1+0.5\cos(5\theta)
\]

```python
import numpy as np
import matplotlib.pyplot as plt

theta = np.linspace(0, 2*np.pi, 1000)
r = 1 + 0.5*np.cos(5*theta)

plt.figure(figsize=(6, 6))
ax = plt.subplot(111, projection="polar")
ax.plot(theta, r, linewidth=2)

ax.set_title(r"Polar plot: $r=1+0.5\cos(5\theta)$")
ax.grid(True)
plt.tight_layout()
plt.savefig("polar_matplotlib.png", dpi=300)
plt.show()
```

---

## 2.3 Matplotlib: quỹ đạo Kepler dạng cực

Quỹ đạo ellipse trong tọa độ cực:

\[
r(\theta)=\frac{a(1-e^2)}{1+e\cos\theta}
\]

```python
import numpy as np
import matplotlib.pyplot as plt

a = 1.0      # bán trục lớn
e = 0.5      # độ lệch tâm

theta = np.linspace(0, 2*np.pi, 1000)
r = a*(1 - e**2)/(1 + e*np.cos(theta))

plt.figure(figsize=(6, 6))
ax = plt.subplot(111, projection="polar")
ax.plot(theta, r, linewidth=2)
ax.set_title("Quỹ đạo Kepler trong tọa độ cực")
ax.grid(True)
plt.tight_layout()
plt.savefig("kepler_polar.png", dpi=300)
plt.show()
```

---

## 2.4 Gnuplot: polar plot

Tạo file `polar.gp`:

```gnuplot
set terminal pngcairo size 900,900 enhanced font "Arial,18"
set output "polar_gnuplot.png"

set polar
set size square
set grid polar
set title "Polar plot: r = 1 + 0.5 cos(5 theta)"

set samples 1000
plot [t=0:2*pi] 1 + 0.5*cos(5*t) with lines linewidth 3 title "r(theta)"
```

Chạy:

```bash
gnuplot polar.gp
```

---

# 3. Vẽ đường 3D line

## 3.1 Ý tưởng

Đồ thị 3D line dùng dữ liệu dạng:

\[
x=x(t),\quad y=y(t),\quad z=z(t)
\]

Ứng dụng:

- Quỹ đạo hạt trong không gian
- Đường xoắn ốc
- Không gian pha 3D
- Hệ Lorenz chaos
- Quỹ đạo trong từ trường

---

## 3.2 Matplotlib: đường xoắn ốc 3D

```python
import numpy as np
import matplotlib.pyplot as plt

# Tạo tham số t
t = np.linspace(0, 10*np.pi, 2000)

# Đường xoắn ốc
x = np.cos(t)
y = np.sin(t)
z = t/(2*np.pi)

fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection="3d")

ax.plot(x, y, z, linewidth=2)

ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("z")
ax.set_title("Đường xoắn ốc 3D")

plt.tight_layout()
plt.savefig("line3d_matplotlib.png", dpi=300)
plt.show()
```

---

## 3.3 Gnuplot: đường xoắn ốc 3D

Tạo dữ liệu bằng Python:

```python
import numpy as np

t = np.linspace(0, 10*np.pi, 2000)
x = np.cos(t)
y = np.sin(t)
z = t/(2*np.pi)

np.savetxt("helix.txt", np.column_stack([x, y, z]), header="x y z")
```

Tạo file `line3d.gp`:

```gnuplot
set terminal pngcairo size 1200,900 enhanced font "Arial,18"
set output "line3d_gnuplot.png"

set title "Đường xoắn ốc 3D"
set xlabel "x"
set ylabel "y"
set zlabel "z"
set grid
set view 60, 35

splot "helix.txt" using 1:2:3 with lines linewidth 3 title "helix"
```

Chạy:

```bash
gnuplot line3d.gp
```

---

# 4. Ví dụ chaos: hệ Lorenz

## 4.1 Phương trình Lorenz

Hệ Lorenz là hệ ODE 3 chiều:

\[
\frac{dx}{dt}=\sigma(y-x)
\]

\[
\frac{dy}{dt}=x(\rho-z)-y
\]

\[
\frac{dz}{dt}=xy-\beta z
\]

Với bộ tham số kinh điển:

\[
\sigma=10,\quad \rho=28,\quad \beta=\frac{8}{3}
\]

hệ có quỹ đạo chaos.

---

## 4.2 Matplotlib: tích phân RK4 và vẽ Lorenz attractor

```python
import numpy as np
import matplotlib.pyplot as plt

sigma = 10.0
rho = 28.0
beta = 8.0/3.0

def f(t, Y):
    x, y, z = Y
    dxdt = sigma*(y - x)
    dydt = x*(rho - z) - y
    dzdt = x*y - beta*z
    return np.array([dxdt, dydt, dzdt])

def RK4(f, t0, tf, Y0, N):
    t = np.linspace(t0, tf, N + 1)
    h = (tf - t0)/N
    Y = np.zeros((N + 1, len(Y0)))
    Y[0] = Y0

    for i in range(N):
        k1 = f(t[i], Y[i])
        k2 = f(t[i] + h/2, Y[i] + h*k1/2)
        k3 = f(t[i] + h/2, Y[i] + h*k2/2)
        k4 = f(t[i] + h, Y[i] + h*k3)
        Y[i+1] = Y[i] + h*(k1 + 2*k2 + 2*k3 + k4)/6

    return t, Y

t, Y = RK4(f, 0, 40, np.array([1.0, 1.0, 1.0]), 20000)

x = Y[:, 0]
y = Y[:, 1]
z = Y[:, 2]

fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection="3d")
ax.plot(x, y, z, linewidth=0.6)

ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("z")
ax.set_title("Lorenz attractor")

plt.tight_layout()
plt.savefig("lorenz_matplotlib.png", dpi=300)
plt.show()
```

---

## 4.3 Xuất dữ liệu Lorenz để vẽ bằng Gnuplot

Thêm dòng này vào cuối code Python trên:

```python
np.savetxt("lorenz.txt", np.column_stack([x, y, z]), header="x y z")
```

Tạo file `lorenz.gp`:

```gnuplot
set terminal pngcairo size 1200,900 enhanced font "Arial,18"
set output "lorenz_gnuplot.png"

set title "Lorenz attractor"
set xlabel "x"
set ylabel "y"
set zlabel "z"
set grid
set view 65, 35

splot "lorenz.txt" using 1:2:3 with lines linewidth 1 title "Lorenz"
```

Chạy:

```bash
gnuplot lorenz.gp
```

---

# 5. Heatmap bằng Matplotlib và Gnuplot

## 5.1 Ý tưởng

Heatmap dùng để biểu diễn hàm hai biến:

\[
z=f(x,y)
\]

bằng màu sắc.

Ứng dụng:

- Phân bố nhiệt độ trên thanh/tấm
- Mật độ xác suất \(|\psi(x,t)|^2\)
- Cường độ trường điện
- Năng lượng theo hai tham số
- Sai số số học theo bước lưới

---

# 6. Ví dụ truyền nhiệt 1D: heatmap \(T(x,t)\)

## 6.1 Phương trình truyền nhiệt

Phương trình truyền nhiệt 1D:

\[
\frac{\partial T}{\partial t}=\alpha\frac{\partial^2 T}{\partial x^2}
\]

Điều kiện biên:

\[
T(0,t)=T(L,t)=0
\]

Điều kiện đầu:

\[
T(x,0)=\sin\left(\frac{\pi x}{L}\right)
\]

Nghiệm giải tích:

\[
T(x,t)=\sin\left(\frac{\pi x}{L}\right)
\exp\left[-\alpha\left(\frac{\pi}{L}\right)^2t\right]
\]

---

## 6.2 Matplotlib: vẽ heatmap truyền nhiệt

```python
import numpy as np
import matplotlib.pyplot as plt

L = 1.0
alpha = 0.1

x = np.linspace(0, L, 300)
t = np.linspace(0, 5, 300)

X, Tgrid = np.meshgrid(x, t)
Temp = np.sin(np.pi*X/L)*np.exp(-alpha*(np.pi/L)**2*Tgrid)

plt.figure(figsize=(8, 5))
plt.imshow(
    Temp,
    extent=[x.min(), x.max(), t.min(), t.max()],
    origin="lower",
    aspect="auto"
)
plt.colorbar(label="Temperature T")
plt.xlabel("x")
plt.ylabel("t")
plt.title("Heatmap truyền nhiệt 1D: T(x,t)")
plt.tight_layout()
plt.savefig("heat_equation_heatmap.png", dpi=300)
plt.show()
```

Ghi chú:

- `imshow` phù hợp khi dữ liệu nằm trên lưới đều.
- `extent=[xmin,xmax,ymin,ymax]` dùng để gắn trục vật lý thay vì chỉ số mảng.
- `origin="lower"` để thời gian tăng từ dưới lên trên.
- `aspect="auto"` để hình không bị ép tỷ lệ vuông.

---

## 6.3 Xuất dữ liệu dạng ma trận cho Gnuplot

Gnuplot đọc heatmap tốt nhất khi dữ liệu có dạng 3 cột:

```text
x   t   T
```

Python tạo file:

```python
import numpy as np

L = 1.0
alpha = 0.1

x = np.linspace(0, L, 300)
t = np.linspace(0, 5, 300)

with open("heat_data.txt", "w") as file:
    for ti in t:
        for xi in x:
            Temp = np.sin(np.pi*xi/L)*np.exp(-alpha*(np.pi/L)**2*ti)
            file.write(f"{xi:20.10e} {ti:20.10e} {Temp:20.10e}\n")
        file.write("\n")
```

---

## 6.4 Gnuplot: heatmap truyền nhiệt

Tạo file `heatmap.gp`:

```gnuplot
set terminal pngcairo size 1200,800 enhanced font "Arial,18"
set output "heatmap_gnuplot.png"

set title "Heatmap truyền nhiệt 1D: T(x,t)"
set xlabel "x"
set ylabel "t"
set cblabel "Temperature T"

set pm3d map
set palette rgb 33,13,10

splot "heat_data.txt" using 1:2:3 notitle
```

Chạy:

```bash
gnuplot heatmap.gp
```

---

# 7. Heatmap 2D: phân bố nhiệt trên tấm phẳng

## 7.1 Hàm mẫu

Ví dụ phân bố nhiệt giả lập:

\[
T(x,y)=\exp[-5(x^2+y^2)]\cos(3x)\sin(3y)
\]

---

## 7.2 Matplotlib: `pcolormesh`

```python
import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(-2, 2, 300)
y = np.linspace(-2, 2, 300)

X, Y = np.meshgrid(x, y)
Z = np.exp(-5*(X**2 + Y**2))*np.cos(3*X)*np.sin(3*Y)

plt.figure(figsize=(7, 6))
plt.pcolormesh(X, Y, Z, shading="auto")
plt.colorbar(label="T(x,y)")
plt.xlabel("x")
plt.ylabel("y")
plt.title("Heatmap 2D bằng pcolormesh")
plt.axis("equal")
plt.tight_layout()
plt.savefig("heatmap2d_pcolormesh.png", dpi=300)
plt.show()
```

---

## 7.3 Matplotlib: `contourf`

```python
import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(-2, 2, 300)
y = np.linspace(-2, 2, 300)

X, Y = np.meshgrid(x, y)
Z = np.exp(-5*(X**2 + Y**2))*np.cos(3*X)*np.sin(3*Y)

plt.figure(figsize=(7, 6))
plt.contourf(X, Y, Z, levels=50)
plt.colorbar(label="T(x,y)")
plt.xlabel("x")
plt.ylabel("y")
plt.title("Heatmap 2D bằng contourf")
plt.axis("equal")
plt.tight_layout()
plt.savefig("heatmap2d_contourf.png", dpi=300)
plt.show()
```

---

## 7.4 Gnuplot: heatmap 2D

Tạo dữ liệu:

```python
import numpy as np

x = np.linspace(-2, 2, 300)
y = np.linspace(-2, 2, 300)

with open("heatmap2d.txt", "w") as file:
    for yi in y:
        for xi in x:
            Z = np.exp(-5*(xi**2 + yi**2))*np.cos(3*xi)*np.sin(3*yi)
            file.write(f"{xi:20.10e} {yi:20.10e} {Z:20.10e}\n")
        file.write("\n")
```

Tạo file `heatmap2d.gp`:

```gnuplot
set terminal pngcairo size 1000,900 enhanced font "Arial,18"
set output "heatmap2d_gnuplot.png"

set title "Heatmap 2D"
set xlabel "x"
set ylabel "y"
set cblabel "Z"
set size square

set pm3d map
set palette rgb 33,13,10

splot "heatmap2d.txt" using 1:2:3 notitle
```

---

# 8. 3D surface plot

Heatmap chỉ là bản đồ màu 2D. Nếu muốn thấy dạng mặt trong không gian 3D, dùng surface plot.

## 8.1 Matplotlib: surface plot

```python
import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(-2, 2, 200)
y = np.linspace(-2, 2, 200)
X, Y = np.meshgrid(x, y)
Z = np.exp(-X**2 - Y**2)

fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection="3d")

surf = ax.plot_surface(X, Y, Z, cmap="viridis")
fig.colorbar(surf, ax=ax, shrink=0.7, label="Z")

ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("Z")
ax.set_title(r"Surface plot: $Z=e^{-x^2-y^2}$")

plt.tight_layout()
plt.savefig("surface_matplotlib.png", dpi=300)
plt.show()
```

---

## 8.2 Gnuplot: surface plot

```gnuplot
set terminal pngcairo size 1200,900 enhanced font "Arial,18"
set output "surface_gnuplot.png"

set title "Surface plot: exp(-x^2-y^2)"
set xlabel "x"
set ylabel "y"
set zlabel "Z"
set grid
set hidden3d
set view 60, 35

splot exp(-x*x-y*y) with lines title "surface"
```

---

# 9. Các lựa chọn quan trọng trong Matplotlib

## 9.1 Kích thước hình

```python
plt.figure(figsize=(8, 6))
```

## 9.2 Độ dày đường

```python
plt.plot(x, y, linewidth=2)
```

## 9.3 Kiểu đường

```python
plt.plot(x, y, linestyle="--")
plt.plot(x, y, linestyle=":")
plt.plot(x, y, linestyle="-.")
```

## 9.4 Marker

```python
plt.plot(x, y, "o-")
plt.plot(x, y, marker="s")
```

## 9.5 Giới hạn trục

```python
plt.xlim(0, 10)
plt.ylim(-1, 1)
```

## 9.6 Trục log

```python
plt.xscale("log")
plt.yscale("log")
```

## 9.7 Latex label

```python
plt.xlabel(r"$x$")
plt.ylabel(r"$E(k)$")
plt.title(r"$E=\hbar\omega$")
```

---

# 10. Các lựa chọn quan trọng trong Gnuplot

## 10.1 Đặt nhãn trục

```gnuplot
set xlabel "x"
set ylabel "y"
set zlabel "z"
```

## 10.2 Đặt giới hạn trục

```gnuplot
set xrange [0:10]
set yrange [-1:1]
```

## 10.3 Bật lưới

```gnuplot
set grid
```

## 10.4 Vẽ log scale

```gnuplot
set logscale x
set logscale y
```

## 10.5 Đổi góc nhìn 3D

```gnuplot
set view 60, 35
```

## 10.6 Vẽ nhiều cột từ file

File `data.txt`:

```text
# x y1 y2
0.0 0.0 1.0
0.1 0.1 0.995
```

Gnuplot:

```gnuplot
plot "data.txt" using 1:2 with lines title "y1", \
     "data.txt" using 1:3 with lines title "y2"
```

---

# 11. Template tổng quát cho bài Computational Physics

## 11.1 Python template

```python
import numpy as np
import matplotlib.pyplot as plt

# 1. Tạo hoặc đọc dữ liệu
x = np.linspace(0, 10, 1000)
y = np.sin(x)

# 2. Vẽ hình
plt.figure(figsize=(8, 5))
plt.plot(x, y, linewidth=2, label="data")

# 3. Trang trí
plt.xlabel("x")
plt.ylabel("y")
plt.title("Tên hình")
plt.grid(True, alpha=0.3)
plt.legend()

# 4. Lưu và hiển thị
plt.tight_layout()
plt.savefig("figure.png", dpi=300)
plt.show()
```

## 11.2 Gnuplot template

```gnuplot
set terminal pngcairo size 1200,800 enhanced font "Arial,18"
set output "figure.png"

set title "Tên hình"
set xlabel "x"
set ylabel "y"
set grid
set key top right

plot "data.txt" using 1:2 with lines linewidth 3 title "data"
```

---

# 12. Khi nào dùng loại đồ thị nào?

| Loại đồ thị | Dữ liệu | Dùng khi |
|---|---|---|
| 2D line | \(y=f(x)\) | nghiệm ODE, dao động, phân rã, band structure |
| Polar plot | \(r=f(\theta)\) | quỹ đạo cực, mẫu bức xạ, đối xứng góc |
| 3D line | \((x(t),y(t),z(t))\) | quỹ đạo hạt, chaos, không gian pha |
| Heatmap | \(z=f(x,y)\) | nhiệt độ, mật độ, trường, sai số |
| Surface plot | \(z=f(x,y)\) | nhìn trực quan mặt 3D |

---

# 13. Lỗi thường gặp

## 13.1 Heatmap bị ngược trục thời gian

Trong Matplotlib, dùng:

```python
origin="lower"
```

nếu muốn giá trị thời gian nhỏ ở dưới.

---

## 13.2 Gnuplot heatmap không hiện đúng

Với dữ liệu lưới 3 cột `x y z`, nên để dòng trống giữa các hàng `y`:

```text
x1 y1 z11
x2 y1 z21
x3 y1 z31

x1 y2 z12
x2 y2 z22
x3 y2 z32
```

---

## 13.3 3D plot trong Matplotlib báo lỗi projection

Cần dùng:

```python
fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")
```

Không cần import riêng `Axes3D` trong các bản Matplotlib mới.

---

## 13.4 Hình bị cắt label

Dùng:

```python
plt.tight_layout()
plt.savefig("figure.png", dpi=300, bbox_inches="tight")
```

---

# 14. Bài tập tự luyện

## Bài 1: Phân rã phóng xạ

Vẽ:

\[
N(t)=N_0e^{-\lambda t}
\]

với \(N_0=1\), \(\lambda=0.5\), \(t\in[0,10]\). Vẽ bằng Matplotlib và Gnuplot.

---

## Bài 2: Quỹ đạo cực

Vẽ:

\[
r(\theta)=2+\sin(6\theta)
\]

trên miền \(\theta\in[0,2\pi]\).

---

## Bài 3: Đường xoắn ốc

Vẽ:

\[
x=\cos t,\quad y=\sin t,\quad z=0.1t
\]

với \(t\in[0,20\pi]\).

---

## Bài 4: Truyền nhiệt

Vẽ heatmap nghiệm:

\[
T(x,t)=\sin(2\pi x)e^{-4\pi^2\alpha t}
\]

với \(x\in[0,1]\), \(t\in[0,2]\), \(\alpha=0.05\).

---

## Bài 5: Lorenz chaos

Chạy hệ Lorenz với hai điều kiện đầu rất gần nhau:

\[
Y_0=(1,1,1),\quad Y_0'=(1.0001,1,1)
\]

Vẽ hai quỹ đạo 3D và quan sát sự tách quỹ đạo theo thời gian.

---

# 15. Gợi ý workflow tốt

Khi làm bài Computational Physics, nên chia thành 3 file:

```text
main.py          # tính toán và xuất dữ liệu
plot.py          # vẽ bằng matplotlib
plot.gp          # vẽ bằng gnuplot nếu cần
```

Ví dụ workflow:

```bash
python main.py
python plot.py
gnuplot plot.gp
```

Cách này giúp tách phần tính toán và phần vẽ, dễ debug hơn.

---

# 16. Kết luận

- Dùng **2D line** cho dữ liệu một biến.
- Dùng **polar plot** cho dữ liệu theo góc.
- Dùng **3D line** cho quỹ đạo trong không gian hoặc không gian pha.
- Dùng **heatmap** cho hàm hai biến hoặc dữ liệu dạng lưới.
- Matplotlib mạnh khi muốn tích hợp tính toán và vẽ trong Python.
- Gnuplot nhẹ, nhanh, tiện khi vẽ trực tiếp từ file dữ liệu số.
