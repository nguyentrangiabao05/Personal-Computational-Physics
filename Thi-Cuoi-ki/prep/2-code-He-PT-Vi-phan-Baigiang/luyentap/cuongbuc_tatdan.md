# Con lắc cưỡng bức tắt dần hỗn loạn (Chaotic Driven Pendulum)

## Phương trình

Dạng không thứ nguyên:

\[
\ddot{\theta}
+\frac{1}{q}\dot{\theta}
+\sin\theta
=
g_d\cos(\omega_D t)
\]

Trong bài:

\[
q = 2,
\qquad
g_d = 1.5,
\qquad
\omega_D = \frac{2}{3}
\]

Viết thành hệ ODE bậc nhất:

\[
\dot{\theta} = \omega
\]

\[
\dot{\omega}
=
-\frac{1}{q}\omega
-\sin\theta
+g_d\cos(\omega_D t)
\]

---

# 1. Phase Portrait

## Khái niệm

Phase portrait là đồ thị trong không gian pha:

\[
(\theta,\omega)
\]

thay vì đồ thị theo thời gian.

Mỗi điểm biểu diễn trạng thái tức thời của hệ.

---

## Vì sao dùng \(\theta \bmod 2\pi\)?

Do góc có tính tuần hoàn:

\[
\theta
\equiv
\theta + 2n\pi
\]

Ví dụ:

\[
0,
\quad
2\pi,
\quad
4\pi
\]

đều chỉ cùng một hướng.

Nếu không lấy modulo:

```text
theta = 0 → 50π
```

đồ thị sẽ trải dài vô hạn.

Ta quy về:

\[
\theta_{\mathrm{mod}}
=
\theta \bmod 2\pi
\]

để thu được cấu trúc thật của không gian pha.

---

## Ý nghĩa hình dạng

### Tuần hoàn

Quỹ đạo đóng.

```text
O
```

### Quasi-periodic

Đường cong không đóng nhưng vẫn có cấu trúc đều.

```text
OOOOOOOO
```

### Chaos

Quỹ đạo không lặp lại và lấp đầy một vùng.

```text
***********
** * * ****
**** ** ***
```

---

# 2. Poincaré Section

## Vấn đề

Phase portrait là tập điểm liên tục trong thời gian.

Rất khó nhìn ra cấu trúc động lực học.

---

## Ý tưởng của Poincaré

Chỉ "chụp ảnh" hệ tại cùng một pha của lực cưỡng bức.

Lực cưỡng bức:

\[
g_d\cos(\omega_D t)
\]

có chu kỳ:

\[
T_D
=
\frac{2\pi}{\omega_D}
\]

Ta chỉ lấy nghiệm tại:

\[
t_n=nT_D
\]

với

\[
n=1,2,3,\dots
\]

---

## Các điểm lấy mẫu

\[
(\theta(nT_D),\omega(nT_D))
\]

Sau đó vẽ:

\[
(\theta \bmod 2\pi,\omega)
\]

---

## Ý nghĩa vật lý

### Period-1

Một điểm

```text
•
```

---

### Period-2

Hai điểm

```text
•     •
```

---

### Period-4

Bốn điểm

```text
•  •
•  •
```

---

### Chaos

Vô số điểm tạo cấu trúc fractal.

```text
•• • ••• ••
 •••• •• •
•• ••• •••
```

---

## Vì sao gọi là fractal?

Khi phóng to một vùng nhỏ của Poincaré section:

```text
toàn cục
   ↓
chi tiết nhỏ
   ↓
vẫn thấy cấu trúc tương tự
```

Đó là dấu hiệu của hỗn loạn xác định (deterministic chaos).

---

# 3. Lyapunov Exponent

## Ý tưởng

Kiểm tra độ nhạy với điều kiện đầu.

Xét hai nghiệm:

\[
\theta_1(0)=\theta_0
\]

\[
\theta_2(0)=\theta_0+10^{-4}
\]

Ban đầu gần như giống nhau.

---

## Sai khác

\[
\delta\theta(t)
=
\theta_2(t)-\theta_1(t)
\]

---

## Hệ hỗn loạn

Sai khác tăng theo hàm mũ:

\[
|\delta\theta(t)|
\approx
|\delta\theta(0)|e^{\lambda t}
\]

---

## Lấy log

\[
\ln|\delta\theta(t)|
=
\ln|\delta\theta(0)|
+\lambda t
\]

Đây là phương trình đường thẳng.

Độ dốc:

\[
\lambda
\]

chính là số mũ Lyapunov.

---

## Diễn giải

### \(\lambda < 0\)

Hai quỹ đạo tiến lại gần nhau.

Hệ ổn định.

---

### \(\lambda = 0\)

Sai khác giữ nguyên.

Hệ trung hòa.

---

### \(\lambda > 0\)

Sai khác tăng theo hàm mũ.

Hệ hỗn loạn.

---

## Ý nghĩa vật lý

Nếu

\[
\lambda = 0.1
\]

thì

\[
|\delta|
\sim e^{0.1t}
\]

Sau một thời gian đủ dài:

```text
Sai khác ban đầu:
0.0001

↓

0.001

↓

0.01

↓

0.1

↓

Hoàn toàn khác nhau
```

Dù phương trình hoàn toàn xác định.

Đây là đặc trưng quan trọng nhất của chaos.

---

# Dấu hiệu nhận biết Chaos trong bài

## Phase Portrait

- Không đóng.
- Quỹ đạo phủ kín một vùng.

## Poincaré Section

- Không phải vài điểm rời rạc.
- Xuất hiện đám điểm fractal.

## Lyapunov

\[
\lambda > 0
\]

---

# Chuỗi chuyển pha khi tăng \(g_d\)

Theo đề:

### \(g_d = 0.5\)

Tuần hoàn.

```text
1 điểm
```

---

### Tăng \(g_d\)

Period doubling:

```text
1 điểm
↓
2 điểm
↓
4 điểm
↓
8 điểm
↓
16 điểm
...
```

---

### \(g_d = 1.5\)

Chaos rõ rệt.

- Phase portrait hỗn loạn.
- Poincaré section dạng fractal.
- Lyapunov dương.