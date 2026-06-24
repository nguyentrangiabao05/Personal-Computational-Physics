# Ôn thi Computational Physics: Hyperbolic PDE - Wave Equation 1D

> File này chỉ tập trung vào **code mẫu thuật toán** và **ví dụ cách sử dụng** từ code bạn gửi.  
> Bỏ bớt phần vẽ hình dài và phần trình bày báo cáo.

---

## 1. Bài toán mẫu

Phương trình sóng 1D:

$$
\frac{\partial^2 u}{\partial t^2}
=
c^2 \frac{\partial^2 u}{\partial x^2}
$$

Miền:

$$
0 < x < L, \qquad t > 0
$$

Điều kiện đầu:

$$
u(x,0)=f(x)
$$

Điều kiện vận tốc đầu:

$$
\frac{\partial u(x,0)}{\partial t}=g(x)
$$

Điều kiện biên cố định hai đầu dây:

$$
u(0,t)=u(L,t)=0
$$

Vận tốc sóng:

$$
c = \sqrt{\frac{T}{\rho}}
$$

Trong code:

```python
T = 40
rho = 0.01
c = np.sqrt(T / rho)
```

---

## 2. Quy ước mảng trong code

Trong code bạn gửi, mảng nghiệm có dạng:

```python
u[time_index, space_index]
```

Tức là:

```python
u[i, j] = u(t_i, x_j)
```

Trong đó:

```python
i  # chỉ số thời gian
j  # chỉ số không gian
```

Kích thước:

```python
n = int(tmax / dt) + 1   # số điểm thời gian
m = int(L / dx) + 1      # số điểm không gian

u = np.zeros((n, m))
x = np.linspace(0, L, m)
t = np.linspace(0, tmax, n)
```

---

## 3. Điều kiện ổn định Courant

Đặt:

$$
\beta = \frac{ck}{h}
$$

với:

```python
k = dt
h = dx
```

Điều kiện ổn định:

$$
\beta \le 1
$$

Code kiểm tra nên viết như sau để luôn trả về giá trị, kể cả khi không ổn định:

```python
def tinh_beta(c, k, h):
    beta = c * k / h

    if beta > 1:
        print("Canh bao: beta =", beta, "> 1. Phuong phap co the khong on dinh.")
        ondinh = False
    else:
        print("Gia tri beta =", beta, "<= 1. Phuong phap on dinh.")
        ondinh = True

    return beta, ondinh
```

Ghi nhớ nhanh:

```python
beta = c * delta_t / delta_x
```

Muốn ổn định thì có thể:

```python
# giảm delta_t
# hoặc tăng delta_x
# hoặc giảm c nếu bài toán cho phép
```

---

## 4. Khởi tạo nghiệm: cách cơ bản

Cách cơ bản dùng:

$$
u_i^1 = u_i^0 + k g(x_i)
$$

Code:

```python
def khoitao_u(dt, dx, tmax, L, f_x, g_x):
    n = int(tmax / dt) + 1   # thời gian
    m = int(L / dx) + 1      # không gian

    u = np.zeros((n, m))
    x = np.linspace(0, L, m)
    t = np.linspace(0, tmax, n)

    # Điều kiện đầu: u(0, x) = f(x)
    for j in range(m):
        u[0, j] = f_x(x[j], L)

    # Điều kiện vận tốc đầu: u[1, j] = u[0, j] + dt*g(x_j)
    for j in range(m):
        u[1, j] = u[0, j] + dt * g_x(x[j], L)

    # Điều kiện biên cố định hai đầu dây
    u[:, 0] = 0.0
    u[:, -1] = 0.0

    return u, x, t
```

Chú ý: công thức này chỉ bậc thấp theo thời gian, nhưng dễ nhớ và đúng với code mẫu.

---

## 5. Thuật toán forward difference không ma sát

Công thức rời rạc:

$$
u_i^{j+1}
=
2(1-\beta^2)u_i^j
+
\beta^2(u_{i+1}^j+u_{i-1}^j)
-
u_i^{j-1}
$$

Trong code của bạn, vì dùng:

```python
u[time, space]
```

nên công thức thành:

```python
u[i+1, j] = (
    2 * (1 - beta**2) * u[i, j]
    + beta**2 * (u[i, j+1] + u[i, j-1])
    - u[i-1, j]
)
```

Code mẫu gọn:

```python
def ham_forward_khong_friction(c, k, h, tmax, L, f_x, g_x):
    u, x, t = khoitao_u(k, h, tmax, L, f_x, g_x)
    n, m = u.shape

    beta, ondinh = tinh_beta(c, k, h)

    if not ondinh:
        print("Phuong phap khong on dinh, khong tinh tiep.")
        return u, x, t, beta

    for i in range(1, n - 1):          # vòng lặp thời gian
        for j in range(1, m - 1):      # vòng lặp không gian, bỏ 2 biên
            u[i + 1, j] = (
                2 * (1 - beta**2) * u[i, j]
                + beta**2 * (u[i, j + 1] + u[i, j - 1])
                - u[i - 1, j]
            )

    return u, x, t, beta
```

Điểm cần nhớ khi thi:

```python
# Muốn tính bước thời gian mới i+1
# cần biết hai bước trước đó: i và i-1
```

---

## 6. Hàm ghi file kết quả

Format bạn dùng:

```text
t_step  x_step  t  x  u
```

Code mẫu:

```python
def ghifile(u, x, t, beta, filename):
    output = f"{filename}_beta_{beta:.2f}.txt"

    with open(output, "w", encoding="utf-8") as file:
        file.write("# Bai toan truyen song 1D\n")
        file.write("# Phuong phap sai phan huu han hien\n")
        file.write("#\n")
        file.write(f"# N_x    = {x.shape[0]}\n")
        file.write(f"# N_time = {t.shape[0]}\n")
        file.write(f"# L      = {x[-1]}\n")
        file.write(f"# t_max  = {t[-1]}\n")
        file.write(f"# beta   = {beta:.8e}\n")
        file.write("#\n")
        file.write(f"# {'t_step':>10s} {'x_step':>10s} {'t':>15s} {'x':>15s} {'u':>15s}\n")

        for t_step in range(t.shape[0]):
            for x_step in range(x.shape[0]):
                file.write(
                    f"  {t_step:10d} {x_step:10d} "
                    f"{t[t_step]:15.8e} {x[x_step]:15.8e} "
                    f"{u[t_step, x_step]:15.8e}\n"
                )
            file.write("\n\n")

    return output
```

Ví dụ dùng chung với solver:

```python
u, x, t, beta = ham_forward_khong_friction(c, delta_t, delta_x, t_max, L, f_x_bai1, g_x_bai1)
filename_out = ghifile(u, x, t, beta, "ketqua_bai1")
```

---

## 7. Ví dụ 1: dây gảy lệch về bên phải

Điều kiện đầu trong code:

```python
def f_x_bai1(x, L):
    if x <= 0.8 * L:
        return 1.25 * x / L
    else:
        return 5 - 5 * x / L
```

Vận tốc đầu bằng 0:

```python
def g_x_bai1(x, L):
    return 0.0
```

Chạy bài toán:

```python
import numpy as np

T = 40
rho = 0.01
c = np.sqrt(T / rho)

L = 1.0
t_max = 0.1
delta_x = 0.007
delta_t = 0.0001

u, x, t, beta = ham_forward_khong_friction(
    c=c,
    k=delta_t,
    h=delta_x,
    tmax=t_max,
    L=L,
    f_x=f_x_bai1,
    g_x=g_x_bai1,
)

filename_out = ghifile(u, x, t, beta, "ketqua_bai1")
print("Da luu:", filename_out)
```

Với các tham số trên:

```python
beta = c * delta_t / delta_x
```

xấp xỉ:

```text
beta ≈ 0.90
```

---

## 8. Đọc lại file kết quả

Vì file có các cột:

```text
t_step  x_step  t  x  u
```

nên đọc lại bằng:

```python
t_flat, x_flat, u_flat = np.loadtxt(
    "ketqua_bai1_beta_0.90.txt",
    comments="#",
    unpack=True,
    usecols=(2, 3, 4),
)
```

Nếu cần reshape về lưới 2D:

```python
x_vals = np.unique(x_flat)
t_vals = np.unique(t_flat)

nx = len(x_vals)
nt = len(t_vals)

T_grid = t_flat.reshape(nt, nx)
X_grid = x_flat.reshape(nt, nx)
U_grid = u_flat.reshape(nt, nx)
```

Trong code này:

```python
U_grid[time_index, space_index]
```

---

## 9. Vẽ nhanh mặt 3D

Code vẽ gọn, đủ để kiểm tra nghiệm:

```python
def ve_3d(t_flat, x_flat, u_flat, ax):
    x_vals = np.unique(x_flat)
    t_vals = np.unique(t_flat)

    nx = len(x_vals)
    nt = len(t_vals)

    T_grid = t_flat.reshape(nt, nx)
    X_grid = x_flat.reshape(nt, nx)
    U_grid = u_flat.reshape(nt, nx)

    surf = ax.plot_surface(T_grid, X_grid, U_grid, cmap="coolwarm", alpha=0.85)

    ax.set_xlabel("Thoi gian t (s)")
    ax.set_ylabel("Vi tri x (m)")
    ax.set_zlabel("Bien do u")

    return surf
```

Ví dụ dùng:

```python
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection="3d")

surf = ve_3d(t_flat, x_flat, u_flat, ax)
fig.colorbar(surf, ax=ax, shrink=0.6, label="u")

plt.tight_layout()
plt.savefig("wave_3d.pdf")
plt.show()
```

---

## 10. Ví dụ 2: điều kiện đầu là một mode sin

Mode cơ bản:

$$
f(x)=\sin\left(\frac{\pi x}{L}\right)
$$

Code:

```python
def f_x_sin_1(x, L):
    return np.sin(np.pi * x / L)


def g_x_zero(x, L):
    return 0.0
```

Chạy:

```python
u, x, t, beta = ham_forward_khong_friction(
    c=c,
    k=delta_t,
    h=delta_x,
    tmax=t_max,
    L=L,
    f_x=f_x_sin_1,
    g_x=g_x_zero,
)

ghifile(u, x, t, beta, "ketqua_sin_1")
```

Mode bậc 2 và 3:

```python
def f_x_sin_2(x, L):
    return np.sin(2 * np.pi * x / L)


def f_x_sin_3(x, L):
    return np.sin(3 * np.pi * x / L)
```

---

## 11. Ví dụ 3: tổng hai mode, xem hiện tượng phách

Điều kiện đầu là tổng hai mode gần nhau:

```python
def f_x_sin_1_cong_2(x, L):
    return np.sin(np.pi * x / L) + np.sin(2 * np.pi * x / L)


def f_x_sin_2_cong_3(x, L):
    return np.sin(2 * np.pi * x / L) + np.sin(3 * np.pi * x / L)
```

Chạy giống bài không ma sát:

```python
u, x, t, beta = ham_forward_khong_friction(
    c=c,
    k=delta_t,
    h=delta_x,
    tmax=t_max,
    L=L,
    f_x=f_x_sin_1_cong_2,
    g_x=g_x_zero,
)

ghifile(u, x, t, beta, "ketqua_sin_1_cong_2")
```

Ý tưởng ôn thi:

```text
Một mode riêng lẻ -> sóng đứng rõ.
Tổng nhiều mode -> hình dạng phức tạp hơn, có thể thấy phách hoặc gói sóng.
```

---

## 12. Ví dụ 4: dây gảy ở giữa

Điều kiện đầu đối xứng quanh giữa dây:

```python
def f_x_gay_giua(x, L):
    if x <= 0.5 * L:
        return 1.25 * x / L
    else:
        return 1.25 * (L - x) / L
```

Chạy:

```python
u, x, t, beta = ham_forward_khong_friction(
    c=c,
    k=delta_t,
    h=delta_x,
    tmax=t_max,
    L=L,
    f_x=f_x_gay_giua,
    g_x=g_x_zero,
)

ghifile(u, x, t, beta, "ketqua_gay_giua")
```

---

## 13. Sóng có ma sát

Phương trình có ma sát:

$$
\frac{\partial^2 u}{\partial t^2}
=
c^2\frac{\partial^2u}{\partial x^2}
-
\frac{2\kappa}{\rho}\frac{\partial u}{\partial t}
$$

Gần đúng:

$$
\frac{\partial u}{\partial t}
\approx
\frac{u_i^j-u_i^{j-1}}{k}
$$

Đặt:

$$
\gamma = \frac{2\kappa k}{\rho}
$$

Công thức cập nhật:

$$
u_i^{j+1}
=
(2-\gamma)u_i^j
+
(\gamma-1)u_i^{j-1}
+
\beta^2(u_{i+1}^j-2u_i^j+u_{i-1}^j)
$$

Code:

```python
def ham_forward_friction(c, k, h, tmax, L, f_x, g_x, kappa, rho):
    u, x, t = khoitao_u(k, h, tmax, L, f_x, g_x)
    n, m = u.shape

    beta, ondinh = tinh_beta(c, k, h)
    gamma = 2 * kappa * k / rho

    if not ondinh:
        print("Phuong phap khong on dinh, khong tinh tiep.")
        return u, x, t, beta

    for i in range(1, n - 1):
        for j in range(1, m - 1):
            lap = u[i, j + 1] - 2 * u[i, j] + u[i, j - 1]

            u[i + 1, j] = (
                (2 - gamma) * u[i, j]
                + (gamma - 1) * u[i - 1, j]
                + beta**2 * lap
            )

    return u, x, t, beta
```

Ví dụ chạy với nhiều `kappa`:

```python
kappa_list = [0.01, 1, 2, 5, 10]

for kappa in kappa_list:
    u, x, t, beta = ham_forward_friction(
        c=c,
        k=delta_t,
        h=delta_x,
        tmax=t_max,
        L=L,
        f_x=f_x_bai1,
        g_x=g_x_bai1,
        kappa=kappa,
        rho=rho,
    )

    ghifile(u, x, t, beta, f"ketqua_friction_kappa_{kappa}")
```

Ý nghĩa:

```text
kappa càng lớn -> dao động tắt dần càng nhanh.
```

---

## 14. Khởi tạo cải tiến cho bước thời gian đầu tiên

Cách cơ bản:

$$
u_i^1 = u_i^0 + k g(x_i)
$$

Cách cải tiến dùng thêm đạo hàm bậc hai theo không gian:

$$
u_i^1
=
(1-\beta^2)f_i
+
\frac{\beta^2}{2}(f_{i+1}+f_{i-1})
+
k g_i
$$

Code:

```python
def khoitao_u_caitien_vantoc(dt, dx, tmax, L, f_x, g_x, c):
    beta, ondinh = tinh_beta(c, dt, dx)

    if not ondinh:
        print("Phuong phap khong on dinh, khong khoi tao.")
        return None, None, None, beta

    n = int(tmax / dt) + 1
    m = int(L / dx) + 1

    u = np.zeros((n, m))
    x = np.linspace(0, L, m)
    t = np.linspace(0, tmax, n)

    # u[0, j] = f(x_j)
    for j in range(m):
        u[0, j] = f_x(x[j], L)

    # u[1, j] cải tiến, chỉ cập nhật điểm trong miền
    for j in range(1, m - 1):
        u[1, j] = (
            (1 - beta**2) * u[0, j]
            + (beta**2 / 2) * (u[0, j - 1] + u[0, j + 1])
            + dt * g_x(x[j], L)
        )

    # Điều kiện biên
    u[:, 0] = 0.0
    u[:, -1] = 0.0

    return u, x, t, beta
```

Nếu bài có ma sát và `g(x)` không bằng 0, công thức Taylor tổng quát có thêm hạng:

$$
-\frac{\kappa k^2}{\rho}g_i
$$

Nhưng trong code bạn đang xét đa số là:

```python
g_x = 0
```

nên hạng đó bằng 0.

---

## 15. Solver ma sát dùng khởi tạo cải tiến

```python
def ham_forward_friction_caitien(c, k, h, tmax, L, f_x, g_x, kappa, rho):
    u, x, t, beta = khoitao_u_caitien_vantoc(k, h, tmax, L, f_x, g_x, c)

    if u is None:
        return None, None, None, beta

    n, m = u.shape
    gamma = 2 * kappa * k / rho

    for i in range(1, n - 1):
        for j in range(1, m - 1):
            lap = u[i, j + 1] - 2 * u[i, j] + u[i, j - 1]

            u[i + 1, j] = (
                (2 - gamma) * u[i, j]
                + (gamma - 1) * u[i - 1, j]
                + beta**2 * lap
            )

    return u, x, t, beta
```

So sánh trước và sau cải tiến:

```python
kappa_bai3 = 0.5

u_truoc, x, t, beta = ham_forward_friction(
    c=c,
    k=delta_t,
    h=delta_x,
    tmax=t_max,
    L=L,
    f_x=f_x_bai1,
    g_x=g_x_bai1,
    kappa=kappa_bai3,
    rho=rho,
)

u_sau, x, t, beta = ham_forward_friction_caitien(
    c=c,
    k=delta_t,
    h=delta_x,
    tmax=t_max,
    L=L,
    f_x=f_x_bai1,
    g_x=g_x_bai1,
    kappa=kappa_bai3,
    rho=rho,
)

delta_u = np.abs(u_truoc - u_sau)

print("Sai so lon nhat:", np.max(delta_u))
print("Sai so trung binh:", np.mean(delta_u))
```

---

## 16. So sánh với nghiệm giải tích

Với dây hai đầu cố định và điều kiện đầu của bài dây gảy lệch, nghiệm giải tích dạng chuỗi sin:

$$
u(x,t)
=
\sum_{n=1}^{\infty}
B_n
\sin\left(\frac{n\pi x}{L}\right)
\cos\left(\frac{c n\pi t}{L}\right)
$$

với:

$$
B_n = \frac{12.5\sin(0.8n\pi)}{n^2\pi^2}
$$

Code dùng 200 số hạng:

```python
def nghiem_giai_tich(x, t, L, c, so_hang=200):
    u = 0.0

    for n in range(1, so_hang + 1):
        B_n = 12.5 * np.sin(0.8 * n * np.pi) / (n * np.pi)**2
        u += B_n * np.sin(n * np.pi * x / L) * np.cos(c * n * np.pi * t / L)

    return u
```

So sánh file số với giải tích:

```python
def sosanh_giaitich(filename, L, c):
    t_step, x_step, t_num, x_num, u_num = np.loadtxt(
        filename,
        comments="#",
        unpack=True,
        usecols=(0, 1, 2, 3, 4),
    )

    u_anal = nghiem_giai_tich(x_num, t_num, L, c, so_hang=200)
    delta_u = np.abs(u_num - u_anal)

    print("Sai so lon nhat:", np.max(delta_u))
    print("Sai so trung binh:", np.mean(delta_u))

    return t_step, x_step, t_num, x_num, u_num, u_anal, delta_u
```

Dùng:

```python
result = sosanh_giaitich("ketqua_bai1_beta_0.90.txt", L=L, c=c)
```

---

## 17. Ước lượng vận tốc sóng từ vị trí đỉnh

Ý tưởng:

1. Với mỗi thời điểm, tìm vị trí có `abs(u)` lớn nhất.
2. Lưu lại cặp `(t_peak, x_peak)`.
3. Fit tuyến tính `x_peak = c_num * t + b`.
4. Hệ số góc là vận tốc sóng số.

Code gọn:

```python
def tim_dinh_song(t_step, t_num, x_num, u_num):
    cac_buoc_t = np.unique(t_step)
    peaks = []

    for ts in cac_buoc_t:
        mask = t_step == ts

        x_t = x_num[mask]
        u_t = u_num[mask]
        t_val = t_num[mask][0]

        idx = np.argmax(np.abs(u_t))

        x_peak = x_t[idx]
        u_peak = u_t[idx]

        peaks.append((t_val, x_peak, u_peak))

    return np.array(peaks)
```

Fit vận tốc:

```python
def fit_van_toc(peaks, t_min, t_max):
    t_peak = peaks[:, 0]
    x_peak = peaks[:, 1]

    mask = (t_peak >= t_min) & (t_peak <= t_max)

    coef = np.polyfit(t_peak[mask], x_peak[mask], deg=1)
    c_num = coef[0]

    return c_num, coef
```

Ví dụ:

```python
t_step, x_step, t_num, x_num, u_num = np.loadtxt(
    "ketqua_bai1_beta_0.90.txt",
    comments="#",
    unpack=True,
    usecols=(0, 1, 2, 3, 4),
)

peaks = tim_dinh_song(t_step, t_num, x_num, u_num)
c_num, coef = fit_van_toc(peaks, t_min=0.0001, t_max=0.0078)

print("Van toc song so:", c_num)
print("Van toc song ly thuyet:", c)
```

---

## 18. Bộ code tối thiểu nên nhớ khi đi thi

Đây là phần quan trọng nhất.

```python
import numpy as np


def tinh_beta(c, k, h):
    beta = c * k / h
    ondinh = beta <= 1
    return beta, ondinh


def khoitao_u(dt, dx, tmax, L, f_x, g_x):
    n = int(tmax / dt) + 1
    m = int(L / dx) + 1

    u = np.zeros((n, m))
    x = np.linspace(0, L, m)
    t = np.linspace(0, tmax, n)

    for j in range(m):
        u[0, j] = f_x(x[j], L)
        u[1, j] = u[0, j] + dt * g_x(x[j], L)

    u[:, 0] = 0.0
    u[:, -1] = 0.0

    return u, x, t


def solve_wave_1d(c, dt, dx, tmax, L, f_x, g_x):
    u, x, t = khoitao_u(dt, dx, tmax, L, f_x, g_x)
    n, m = u.shape

    beta, ondinh = tinh_beta(c, dt, dx)

    if not ondinh:
        print("Khong on dinh: beta =", beta)
        return u, x, t, beta

    for i in range(1, n - 1):
        for j in range(1, m - 1):
            u[i + 1, j] = (
                2 * (1 - beta**2) * u[i, j]
                + beta**2 * (u[i, j + 1] + u[i, j - 1])
                - u[i - 1, j]
            )

    return u, x, t, beta
```

Ví dụ dùng tối thiểu:

```python
def f_x(x, L):
    if x <= 0.8 * L:
        return 1.25 * x / L
    else:
        return 5 - 5 * x / L


def g_x(x, L):
    return 0.0


T = 40
rho = 0.01
c = np.sqrt(T / rho)

L = 1.0
tmax = 0.1
dx = 0.007
dt = 0.0001

u, x, t, beta = solve_wave_1d(c, dt, dx, tmax, L, f_x, g_x)

print("beta =", beta)
print("u.shape =", u.shape)
```

---

## 19. Checklist khi code bài phương trình sóng

```text
[ ] Xác định L, tmax, dx, dt
[ ] Tính c = sqrt(T/rho)
[ ] Tính beta = c*dt/dx
[ ] Kiểm tra beta <= 1
[ ] Khởi tạo u[0, :] = f(x)
[ ] Khởi tạo u[1, :] từ vận tốc đầu g(x)
[ ] Gán biên u[:, 0] = 0 và u[:, -1] = 0
[ ] Lặp thời gian từ i = 1 đến n-2
[ ] Lặp không gian từ j = 1 đến m-2
[ ] Cập nhật u[i+1, j]
[ ] Ghi file hoặc vẽ nghiệm
```

Lỗi dễ gặp:

```text
1. Nhầm trục: u[time, space] khác u[space, time].
2. Quên bỏ qua hai biên khi update.
3. beta > 1 nhưng vẫn chạy.
4. Hàm tinh_beta không return khi beta > 1.
5. Reshape sai thứ tự khi đọc file để vẽ 3D.
6. Dùng x_step, t_step lẫn với x, t thực.
```

---

## 20. Công thức cần thuộc

Không ma sát:

$$
u_i^{j+1}
=
2(1-\beta^2)u_i^j
+
\beta^2(u_{i+1}^j+u_{i-1}^j)
-
u_i^{j-1}
$$

Có ma sát:

$$
u_i^{j+1}
=
(2-\gamma)u_i^j
+
(\gamma-1)u_i^{j-1}
+
\beta^2(u_{i+1}^j-2u_i^j+u_{i-1}^j)
$$

Trong đó:

$$
\beta = \frac{c\Delta t}{\Delta x},
\qquad
\gamma = \frac{2\kappa\Delta t}{\rho}
$$

Điều kiện ổn định chính:

$$
\beta \le 1
$$
