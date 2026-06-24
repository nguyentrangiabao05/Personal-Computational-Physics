# Forward Euler và Backward Euler với biên Neumann trong bài toán truyền nhiệt 1D

Tài liệu này tập trung vào **công thức** và **thuật toán** khi thêm điều kiện biên Neumann, tức biên cách nhiệt, vào bài toán truyền nhiệt 1D.

Phương trình truyền nhiệt 1D:

$$
\frac{\partial u}{\partial t}
=============================

\alpha^2 \frac{\partial^2 u}{\partial x^2}
$$

với:

$$
\alpha^2 = \frac{\kappa}{C\rho}
$$

Đặt:

$$
\eta = \frac{\alpha^2 k}{h^2}
$$

trong đó:

* (h): bước không gian
* (k): bước thời gian
* (u_{i,j}): nhiệt độ tại vị trí (i), thời điểm (j)
* (i = 0, 1, 2, \ldots, N_x-1)
* (j = 0, 1, 2, \ldots, N_t-1)

Trong code:

```python
u[i, j]
```

nghĩa là nhiệt độ tại điểm không gian `i` và thời điểm `j`.

---

# 1. Điều kiện biên thường và biên Neumann khác nhau như thế nào?

## 1.1 Biên Dirichlet

Biên Dirichlet là biên giữ nhiệt độ cố định.

Ví dụ:

$$
u(0,t)=T_\text{trái}
$$

$$
u(L,t)=T_\text{phải}
$$

Trong code, nếu đầu trái giữ 0 độ C:

```python
u[0, j] = 0.0
```

Nếu đầu phải giữ 0 độ C:

```python
u[N_x - 1, j] = 0.0
```

Đây là kiểu điều kiện biên thường dùng trong các bài ban đầu.

---

## 1.2 Biên Neumann

Biên Neumann cách nhiệt là:

$$
\frac{\partial u}{\partial x}=0
$$

Nghĩa vật lý: không có dòng nhiệt đi qua biên.

Ở đầu trái:

$$
\left.\frac{\partial u}{\partial x}\right|_{x=0}=0
$$

Dùng ghost point:

$$
\frac{u_{1,j}-u_{-1,j}}{2h}=0
$$

suy ra:

$$
u_{-1,j}=u_{1,j}
$$

Ở đầu phải:

$$
\left.\frac{\partial u}{\partial x}\right|_{x=L}=0
$$

Dùng ghost point:

$$
\frac{u_{N_x,j}-u_{N_x-2,j}}{2h}=0
$$

suy ra:

$$
u_{N_x,j}=u_{N_x-2,j}
$$

---

# 2. Lỗi thường gặp khi viết biên cách nhiệt

Không nên viết:

```python
u[0, j] = u[0, j - 1]
```

hoặc:

```python
u[N_x - 1, j] = u[N_x - 1, j - 1]
```

Vì lệnh này có ý nghĩa là nhiệt độ tại biên không đổi theo thời gian:

$$
\frac{\partial u}{\partial t}=0
$$

Trong khi biên cách nhiệt cần:

$$
\frac{\partial u}{\partial x}=0
$$

Ngoài ra, tại `j = 0`, lệnh:

```python
u[0, j - 1]
```

trở thành:

```python
u[0, -1]
```

Trong Python, `-1` là phần tử cuối cùng của mảng. Vì vậy code sẽ lấy nhầm giá trị ở thời điểm cuối cùng, trong khi thời điểm đó chưa được tính.

Do đó, biên Neumann phải được đưa vào bằng công thức sai phân theo không gian, không phải bằng cách copy theo thời gian.

---

# 3. Forward Euler không có biên Neumann

Trước hết xét trường hợp bình thường: hai đầu đều là Dirichlet.

Ví dụ:

$$
u(0,t)=T_\text{trái}
$$

$$
u(L,t)=T_\text{phải}
$$

Công thức Forward Euler cho điểm bên trong là:

$$
u_{i,j+1}
=========

(1-2\eta)u_{i,j}
+
\eta(u_{i+1,j}+u_{i-1,j})
$$

với:

$$
i = 1,2,\ldots,N_x-2
$$

Code thuật toán:

```python
for j in range(N_time - 1):

    # 1. Cap nhat cac diem ben trong
    # Forward Euler dung nghiem tai thoi diem cu j
    # de tinh nghiem tai thoi diem moi j+1.
    for i in range(1, N_x - 1):
        u[i, j + 1] = (
            (1.0 - 2.0 * eta) * u[i, j]
            + eta * (u[i + 1, j] + u[i - 1, j])
        )

    # 2. Giu bien trai Dirichlet
    # Vi bien trai la nhiet do co dinh nen gan truc tiep.
    u[0, j + 1] = T_trai

    # 3. Giu bien phai Dirichlet
    # Vi bien phai la nhiet do co dinh nen gan truc tiep.
    u[N_x - 1, j + 1] = T_phai
```

Điểm chính:

* Chỉ cập nhật các điểm bên trong bằng công thức truyền nhiệt.
* Hai biên không dùng công thức truyền nhiệt.
* Hai biên được gán cố định theo Dirichlet.

---

# 4. Forward Euler có biên Neumann

Forward Euler là phương pháp tường minh.

Nghĩa là nghiệm tại thời điểm mới (j+1) được tính từ nghiệm tại thời điểm cũ (j).

Vì vậy, biên Neumann của Forward Euler cũng phải dùng giá trị tại thời điểm cũ (j).

---

## 4.1 Biên trái Neumann trong Forward Euler

Tại biên trái (i=0), nếu viết công thức Forward Euler hình thức:

$$
u_{0,j+1}
=========

(1-2\eta)u_{0,j}
+
\eta(u_{1,j}+u_{-1,j})
$$

Với biên Neumann:

$$
u_{-1,j}=u_{1,j}
$$

Thay vào:

$$
u_{0,j+1}
=========

(1-2\eta)u_{0,j}
+
2\eta u_{1,j}
$$

Code:

```python
u[0, j + 1] = (
    (1.0 - 2.0 * eta) * u[0, j]
    + 2.0 * eta * u[1, j]
)
```

Hoặc viết tương đương:

```python
u[0, j + 1] = (
    u[0, j]
    + 2.0 * eta * (u[1, j] - u[0, j])
)
```

Hai dạng này giống nhau.

---

## 4.2 Biên phải Neumann trong Forward Euler

Tại biên phải (i=N_x-1), dùng ghost point:

$$
u_{N_x,j}=u_{N_x-2,j}
$$

Công thức Forward Euler tại biên phải:

$$
u_{N_x-1,j+1}
=============

(1-2\eta)u_{N_x-1,j}
+
2\eta u_{N_x-2,j}
$$

Code:

```python
u[N_x - 1, j + 1] = (
    (1.0 - 2.0 * eta) * u[N_x - 1, j]
    + 2.0 * eta * u[N_x - 2, j]
)
```

Hoặc viết tương đương:

```python
u[N_x - 1, j + 1] = (
    u[N_x - 1, j]
    + 2.0 * eta * (u[N_x - 2, j] - u[N_x - 1, j])
)
```

---

# 5. Thuật toán Forward Euler khi có và không có Neumann

## 5.1 Hai đầu Dirichlet

Đây là trường hợp không có biên cách nhiệt.

```python
for j in range(N_time - 1):

    # Cap nhat cac diem ben trong
    for i in range(1, N_x - 1):
        u[i, j + 1] = (
            (1.0 - 2.0 * eta) * u[i, j]
            + eta * (u[i + 1, j] + u[i - 1, j])
        )

    # Bien trai Dirichlet
    u[0, j + 1] = T_trai

    # Bien phai Dirichlet
    u[N_x - 1, j + 1] = T_phai
```

Không có gì đặc biệt ở hai biên. Biên chỉ được giữ cố định.

---

## 5.2 Trái Neumann, phải Dirichlet

Trường hợp:

$$
\left.\frac{\partial u}{\partial x}\right|_{x=0}=0
$$

và:

$$
u(L,t)=T_\text{phải}
$$

Thuật toán:

```python
for j in range(N_time - 1):

    # 1. Bien trai Neumann
    # Bien trai cach nhiet nen phai dung cong thuc ghost point.
    # Khong duoc gan u[0,j+1] = T_trai.
    u[0, j + 1] = (
        (1.0 - 2.0 * eta) * u[0, j]
        + 2.0 * eta * u[1, j]
    )

    # 2. Cap nhat cac diem ben trong
    for i in range(1, N_x - 1):
        u[i, j + 1] = (
            (1.0 - 2.0 * eta) * u[i, j]
            + eta * (u[i + 1, j] + u[i - 1, j])
        )

    # 3. Bien phai Dirichlet
    # Bien phai giu nhiet do co dinh.
    u[N_x - 1, j + 1] = T_phai
```

Thay đổi chính so với hai đầu Dirichlet:

```python
u[0, j + 1] = T_trai
```

được thay bằng:

```python
u[0, j + 1] = (
    (1.0 - 2.0 * eta) * u[0, j]
    + 2.0 * eta * u[1, j]
)
```

---

## 5.3 Trái Dirichlet, phải Neumann

Trường hợp:

$$
u(0,t)=T_\text{trái}
$$

và:

$$
\left.\frac{\partial u}{\partial x}\right|_{x=L}=0
$$

Thuật toán:

```python
for j in range(N_time - 1):

    # 1. Bien trai Dirichlet
    u[0, j + 1] = T_trai

    # 2. Cap nhat cac diem ben trong
    for i in range(1, N_x - 1):
        u[i, j + 1] = (
            (1.0 - 2.0 * eta) * u[i, j]
            + eta * (u[i + 1, j] + u[i - 1, j])
        )

    # 3. Bien phai Neumann
    # Bien phai cach nhiet nen dung ghost point:
    # u[N_x,j] = u[N_x-2,j]
    u[N_x - 1, j + 1] = (
        (1.0 - 2.0 * eta) * u[N_x - 1, j]
        + 2.0 * eta * u[N_x - 2, j]
    )
```

Thay đổi chính so với hai đầu Dirichlet:

```python
u[N_x - 1, j + 1] = T_phai
```

được thay bằng:

```python
u[N_x - 1, j + 1] = (
    (1.0 - 2.0 * eta) * u[N_x - 1, j]
    + 2.0 * eta * u[N_x - 2, j]
)
```

---

## 5.4 Hai đầu Neumann

Trường hợp hai đầu đều cách nhiệt:

$$
\left.\frac{\partial u}{\partial x}\right|_{x=0}=0
$$

và:

$$
\left.\frac{\partial u}{\partial x}\right|_{x=L}=0
$$

Thuật toán:

```python
for j in range(N_time - 1):

    # 1. Bien trai Neumann
    u[0, j + 1] = (
        (1.0 - 2.0 * eta) * u[0, j]
        + 2.0 * eta * u[1, j]
    )

    # 2. Cap nhat cac diem ben trong
    for i in range(1, N_x - 1):
        u[i, j + 1] = (
            (1.0 - 2.0 * eta) * u[i, j]
            + eta * (u[i + 1, j] + u[i - 1, j])
        )

    # 3. Bien phai Neumann
    u[N_x - 1, j + 1] = (
        (1.0 - 2.0 * eta) * u[N_x - 1, j]
        + 2.0 * eta * u[N_x - 2, j]
    )
```

Điểm nhớ của Forward Euler với Neumann:

* Tất cả vế phải dùng thời điểm cũ `j`.
* Kết quả mới được ghi vào thời điểm `j + 1`.
* Không dùng `u[0, j] = u[0, j - 1]`.
* Không dùng `u[N_x - 1, j] = u[N_x - 1, j - 1]`.

---

# 6. Backward Euler không có biên Neumann

Backward Euler là phương pháp ẩn.

Công thức:

$$
\frac{u_{i,j}-u_{i,j-1}}{k}
===========================

\alpha^2
\frac{
u_{i-1,j}
-2u_{i,j}
+u_{i+1,j}
}{h^2}
$$

Chú ý: vế không gian dùng nghiệm tại thời điểm mới (j), không phải (j-1).

Sắp xếp lại:

$$
-\eta u_{i-1,j}
+
(1+2\eta)u_{i,j}
----------------

# \eta u_{i+1,j}

u_{i,j-1}
$$

Nếu giải lặp Gauss-Seidel, ta viết:

$$
u_{i,j}
=======

\frac{\eta}{1+2\eta}
(u_{i+1,j}+u_{i-1,j})
+
\frac{1}{1+2\eta}u_{i,j-1}
$$

Đặt:

$$
\beta_1 = \frac{\eta}{1+2\eta}
$$

$$
\beta_2 = \frac{1}{1+2\eta}
$$

Khi đó:

$$
u_{i,j}
=======

\beta_1(u_{i+1,j}+u_{i-1,j})
+
\beta_2 u_{i,j-1}
$$

---

## 6.1 Thuật toán Backward Euler với hai đầu Dirichlet

Trường hợp không có Neumann:

$$
u(0,t)=T_\text{trái}
$$

$$
u(L,t)=T_\text{phải}
$$

Thuật toán:

```python
for j in range(1, N_time):

    # 1. Lay nghiem o buoc truoc lam gia tri doan ban dau
    # cho nghiem tai thoi diem moi j.
    for i in range(N_x):
        u[i, j] = u[i, j - 1]

    # 2. Gan bien Dirichlet
    # Hai bien nay giu co dinh trong suot qua trinh lap.
    u[0, j] = T_trai
    u[N_x - 1, j] = T_phai

    # 3. Lap Gauss-Seidel tai thoi diem j
    for q in range(1, N_max + 1):

        # Luu nghiem cu de kiem tra hoi tu
        u_old = u[:, j].copy()

        # Cap nhat cac diem ben trong
        # Bien trai va bien phai khong cap nhat vi la Dirichlet.
        for i in range(1, N_x - 1):
            u[i, j] = (
                beta1 * (u[i + 1, j] + u[i - 1, j])
                + beta2 * u[i, j - 1]
            )

        # Gan lai bien Dirichlet sau moi vong lap
        # De dam bao bien khong bi thay doi.
        u[0, j] = T_trai
        u[N_x - 1, j] = T_phai

        # Kiem tra hoi tu
        max_err = np.max(np.abs(u[:, j] - u_old))

        if max_err < tol:
            break
```

Điểm chính:

* Backward Euler cần lặp để tìm nghiệm tại thời điểm mới `j`.
* Nếu biên là Dirichlet, biên không được cập nhật bằng công thức truyền nhiệt.
* Chỉ cập nhật các điểm bên trong `i = 1` đến `N_x - 2`.

---

# 7. Backward Euler có biên Neumann

Với Backward Euler, Neumann phải dùng nghiệm tại thời điểm mới (j).

Do đó biên Neumann phải được đặt **bên trong vòng lặp hội tụ**.

Không được cập nhật biên Neumann một lần ở ngoài vòng lặp.

---

## 7.1 Biên trái Neumann trong Backward Euler

Tại biên trái:

$$
\frac{u_{0,j}-u_{0,j-1}}{k}
===========================

\alpha^2
\frac{
u_{-1,j}
-2u_{0,j}
+u_{1,j}
}{h^2}
$$

Với Neumann:

$$
u_{-1,j}=u_{1,j}
$$

Thay vào:

$$
\frac{u_{0,j}-u_{0,j-1}}{k}
===========================

\alpha^2
\frac{
2u_{1,j}
-2u_{0,j}
}{h^2}
$$

Suy ra:

$$
u_{0,j}-u_{0,j-1}
=================

2\eta(u_{1,j}-u_{0,j})
$$

Chuyển vế:

$$
(1+2\eta)u_{0,j}
================

2\eta u_{1,j}
+
u_{0,j-1}
$$

Chia cho (1+2\eta):

$$
u_{0,j}
=======

2\beta_1 u_{1,j}
+
\beta_2u_{0,j-1}
$$

Code:

```python
u[0, j] = (
    2.0 * beta1 * u[1, j]
    + beta2 * u[0, j - 1]
)
```

---

## 7.2 Biên phải Neumann trong Backward Euler

Tại biên phải:

$$
u_{N_x,j}=u_{N_x-2,j}
$$

Suy ra:

$$
u_{N_x-1,j}
===========

2\beta_1 u_{N_x-2,j}
+
\beta_2u_{N_x-1,j-1}
$$

Code:

```python
u[N_x - 1, j] = (
    2.0 * beta1 * u[N_x - 2, j]
    + beta2 * u[N_x - 1, j - 1]
)
```

---

# 8. Thuật toán Backward Euler khi có và không có Neumann

## 8.1 Hai đầu Dirichlet

Không có biên cách nhiệt.

```python
for j in range(1, N_time):

    # Gia tri doan ban dau
    for i in range(N_x):
        u[i, j] = u[i, j - 1]

    # Gan bien Dirichlet
    u[0, j] = T_trai
    u[N_x - 1, j] = T_phai

    for q in range(1, N_max + 1):

        u_old = u[:, j].copy()

        # Chi cap nhat diem ben trong
        for i in range(1, N_x - 1):
            u[i, j] = (
                beta1 * (u[i + 1, j] + u[i - 1, j])
                + beta2 * u[i, j - 1]
            )

        # Giu bien Dirichlet
        u[0, j] = T_trai
        u[N_x - 1, j] = T_phai

        max_err = np.max(np.abs(u[:, j] - u_old))

        if max_err < tol:
            break
```

---

## 8.2 Trái Neumann, phải Dirichlet

Trường hợp:

$$
\left.\frac{\partial u}{\partial x}\right|_{x=0}=0
$$

và:

$$
u(L,t)=T_\text{phải}
$$

Thuật toán:

```python
for j in range(1, N_time):

    # 1. Gia tri doan ban dau tai thoi diem j
    for i in range(N_x):
        u[i, j] = u[i, j - 1]

    # 2. Bien phai la Dirichlet nen gan co dinh
    u[N_x - 1, j] = T_phai

    # 3. Lap Gauss-Seidel
    for q in range(1, N_max + 1):

        u_old = u[:, j].copy()

        # 3.1 Bien trai Neumann
        # Bien trai cach nhiet phu thuoc vao u[1,j].
        # Vi u[1,j] la nghiem tai thoi diem moi,
        # nen cong thuc nay phai nam trong vong lap hoi tu.
        u[0, j] = (
            2.0 * beta1 * u[1, j]
            + beta2 * u[0, j - 1]
        )

        # 3.2 Cap nhat diem ben trong
        for i in range(1, N_x - 1):
            u[i, j] = (
                beta1 * (u[i + 1, j] + u[i - 1, j])
                + beta2 * u[i, j - 1]
            )

        # 3.3 Bien phai Dirichlet
        # Gan lai de dam bao bien phai khong doi.
        u[N_x - 1, j] = T_phai

        # 3.4 Kiem tra hoi tu
        max_err = np.max(np.abs(u[:, j] - u_old))

        if max_err < tol:
            break
```

Thay đổi chính so với hai đầu Dirichlet:

```python
u[0, j] = T_trai
```

không còn đúng nữa.

Thay vào đó, trong vòng lặp hội tụ ta dùng:

```python
u[0, j] = (
    2.0 * beta1 * u[1, j]
    + beta2 * u[0, j - 1]
)
```

---

## 8.3 Trái Dirichlet, phải Neumann

Trường hợp:

$$
u(0,t)=T_\text{trái}
$$

và:

$$
\left.\frac{\partial u}{\partial x}\right|_{x=L}=0
$$

Thuật toán:

```python
for j in range(1, N_time):

    # 1. Gia tri doan ban dau tai thoi diem j
    for i in range(N_x):
        u[i, j] = u[i, j - 1]

    # 2. Bien trai la Dirichlet
    u[0, j] = T_trai

    # 3. Lap Gauss-Seidel
    for q in range(1, N_max + 1):

        u_old = u[:, j].copy()

        # 3.1 Bien trai Dirichlet
        # Gan lai de bien trai khong doi.
        u[0, j] = T_trai

        # 3.2 Cap nhat cac diem ben trong
        for i in range(1, N_x - 1):
            u[i, j] = (
                beta1 * (u[i + 1, j] + u[i - 1, j])
                + beta2 * u[i, j - 1]
            )

        # 3.3 Bien phai Neumann
        # Bien phai cach nhiet phu thuoc vao u[N_x-2,j],
        # nen phai cap nhat trong vong lap hoi tu.
        u[N_x - 1, j] = (
            2.0 * beta1 * u[N_x - 2, j]
            + beta2 * u[N_x - 1, j - 1]
        )

        # 3.4 Kiem tra hoi tu
        max_err = np.max(np.abs(u[:, j] - u_old))

        if max_err < tol:
            break
```

Thay đổi chính so với hai đầu Dirichlet:

```python
u[N_x - 1, j] = T_phai
```

không còn đúng nữa.

Thay vào đó, trong vòng lặp hội tụ ta dùng:

```python
u[N_x - 1, j] = (
    2.0 * beta1 * u[N_x - 2, j]
    + beta2 * u[N_x - 1, j - 1]
)
```

---

## 8.4 Hai đầu Neumann

Trường hợp hai đầu đều cách nhiệt:

$$
\left.\frac{\partial u}{\partial x}\right|_{x=0}=0
$$

và:

$$
\left.\frac{\partial u}{\partial x}\right|_{x=L}=0
$$

Thuật toán:

```python
for j in range(1, N_time):

    # 1. Gia tri doan ban dau tai thoi diem j
    for i in range(N_x):
        u[i, j] = u[i, j - 1]

    # 2. Lap Gauss-Seidel
    for q in range(1, N_max + 1):

        u_old = u[:, j].copy()

        # 2.1 Bien trai Neumann
        # du/dx = 0 tai x = 0
        u[0, j] = (
            2.0 * beta1 * u[1, j]
            + beta2 * u[0, j - 1]
        )

        # 2.2 Cap nhat cac diem ben trong
        for i in range(1, N_x - 1):
            u[i, j] = (
                beta1 * (u[i + 1, j] + u[i - 1, j])
                + beta2 * u[i, j - 1]
            )

        # 2.3 Bien phai Neumann
        # du/dx = 0 tai x = L
        u[N_x - 1, j] = (
            2.0 * beta1 * u[N_x - 2, j]
            + beta2 * u[N_x - 1, j - 1]
        )

        # 2.4 Kiem tra hoi tu
        max_err = np.max(np.abs(u[:, j] - u_old))

        if max_err < tol:
            break
```

Điểm nhớ của Backward Euler với Neumann:

* Backward Euler dùng nghiệm tại thời điểm mới `j`.
* Biên Neumann cũng phải dùng nghiệm tại thời điểm mới `j`.
* Vì vậy biên Neumann phải nằm trong vòng lặp hội tụ.
* Không được dùng công thức Forward Euler cho biên của Backward Euler.

---

# 9. So sánh thay đổi chính giữa Dirichlet và Neumann

## 9.1 Với Forward Euler

Nếu biên trái là Dirichlet:

```python
u[0, j + 1] = T_trai
```

Nếu biên trái là Neumann:

```python
u[0, j + 1] = (
    (1.0 - 2.0 * eta) * u[0, j]
    + 2.0 * eta * u[1, j]
)
```

Nếu biên phải là Dirichlet:

```python
u[N_x - 1, j + 1] = T_phai
```

Nếu biên phải là Neumann:

```python
u[N_x - 1, j + 1] = (
    (1.0 - 2.0 * eta) * u[N_x - 1, j]
    + 2.0 * eta * u[N_x - 2, j]
)
```

---

## 9.2 Với Backward Euler

Nếu biên trái là Dirichlet:

```python
u[0, j] = T_trai
```

Nếu biên trái là Neumann:

```python
u[0, j] = (
    2.0 * beta1 * u[1, j]
    + beta2 * u[0, j - 1]
)
```

Nếu biên phải là Dirichlet:

```python
u[N_x - 1, j] = T_phai
```

Nếu biên phải là Neumann:

```python
u[N_x - 1, j] = (
    2.0 * beta1 * u[N_x - 2, j]
    + beta2 * u[N_x - 1, j - 1]
)
```

---

# 10. Khác nhau quan trọng giữa Forward Euler và Backward Euler

## Forward Euler

Forward Euler có dạng:

$$
u^{j+1} = F(u^j)
$$

Nghĩa là dùng thời điểm cũ để tính thời điểm mới.

Vì vậy:

```python
u[0, j + 1]
```

được tính từ:

```python
u[0, j], u[1, j]
```

Biên Neumann Forward Euler:

```python
u[0, j + 1] = (
    (1.0 - 2.0 * eta) * u[0, j]
    + 2.0 * eta * u[1, j]
)
```

---

## Backward Euler

Backward Euler có dạng:

$$
u^j = F(u^j, u^{j-1})
$$

Nghĩa là nghiệm tại thời điểm mới xuất hiện ở cả hai vế.

Vì vậy:

```python
u[0, j]
```

phụ thuộc vào:

```python
u[1, j]
```

mà `u[1, j]` cũng là nghiệm đang cần tìm.

Biên Neumann Backward Euler:

```python
u[0, j] = (
    2.0 * beta1 * u[1, j]
    + beta2 * u[0, j - 1]
)
```

Vì phụ thuộc vào nghiệm mới, công thức này phải nằm trong vòng lặp hội tụ.

---

# 11. Kiểm tra bảo toàn nhiệt khi hai đầu cách nhiệt

Nếu hai đầu đều là Neumann, nhiệt không thoát ra ngoài. Tổng nhiệt trong thanh nên gần như được bảo toàn.

Với lưới đều, nên tính tổng nhiệt bằng quy tắc hình thang:

$$
S_j
===

h
\left[
\frac{1}{2}u_{0,j}
+
\sum_{i=1}^{N_x-2}u_{i,j}
+
\frac{1}{2}u_{N_x-1,j}
\right]
$$

Code:

```python
def kiem_tra_bao_toan_nhiet(u, h):
    N_x = u.shape[0]
    N_time = u.shape[1]

    S = np.zeros(N_time)

    for j in range(N_time):
        S[j] = h * (
            0.5 * u[0, j]
            + np.sum(u[1:N_x - 1, j])
            + 0.5 * u[N_x - 1, j]
        )

    return S
```

Nếu hai đầu đều cách nhiệt, `S` nên gần như không đổi theo thời gian.

Nếu `S` thay đổi mạnh, thường có lỗi ở một trong các chỗ sau:

1. Gán nhầm biên Neumann thành Dirichlet.
2. Dùng `u[0, j] = u[0, j - 1]`.
3. Quên cập nhật biên Neumann trong Backward Euler.
4. Dùng công thức Forward Euler cho biên của Backward Euler.
5. Forward Euler bị mất ổn định do (\eta > 0.5).

---

# 12. Tóm tắt ngắn nhất

Với Dirichlet, biên được gán trực tiếp:

```python
u[0, j] = T_trai
u[N_x - 1, j] = T_phai
```

Với Neumann, biên không được gán trực tiếp mà phải tính từ điểm lân cận.

Forward Euler:

```python
u[0, j + 1] = (
    (1.0 - 2.0 * eta) * u[0, j]
    + 2.0 * eta * u[1, j]
)

u[N_x - 1, j + 1] = (
    (1.0 - 2.0 * eta) * u[N_x - 1, j]
    + 2.0 * eta * u[N_x - 2, j]
)
```

Backward Euler:

```python
u[0, j] = (
    2.0 * beta1 * u[1, j]
    + beta2 * u[0, j - 1]
)

u[N_x - 1, j] = (
    2.0 * beta1 * u[N_x - 2, j]
    + beta2 * u[N_x - 1, j - 1]
)
```

Điểm khác biệt quan trọng nhất:

* Forward Euler cập nhật Neumann tại `j + 1` bằng dữ liệu cũ `j`.
* Backward Euler cập nhật Neumann tại `j` bằng dữ liệu mới `j`, nên phải đặt trong vòng lặp hội tụ.
