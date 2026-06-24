# Hệ phương trình vi phân bậc nhất

Một hệ ODE tổng quát có dạng:

$$
\frac{d\mathbf{Y}}{dt} = \mathbf{F}(t,\mathbf{Y})
$$

Trong đó:

- `Y`: vector trạng thái hiện tại.
- `dY_dt`: vector đạo hàm theo thời gian.
- `F(t, Y)`: hàm mô tả hệ phương trình vi phân.

Trong Python:

```python
def F(t, Y):
    ...
    return dY_dt
```

## Ví dụ: con lắc đơn góc nhỏ

Phương trình bậc hai:

$$
\frac{d^2\theta}{dt^2} + \frac{g}{l}\theta = 0
$$

Đặt:

$$
\omega = \frac{d\theta}{dt}
$$

Khi đó hệ bậc nhất là:

$$
\frac{d\theta}{dt} = \omega
$$

$$
\frac{d\omega}{dt} = -\frac{g}{l}\theta
$$

Vector trạng thái:

$$
Y = [\theta, \omega]
$$

Code Python:

```python
def conlac_daodong(t, Y):
    theta = Y[0]
    omega = Y[1]

    dtheta_dt = omega
    domega_dt = -(g/l) * theta

    return np.array([dtheta_dt, domega_dt])
```

Ví dụ điều kiện đầu:

```python
g = 9.81
l = 1.0

theta0 = 0.2
omega0 = 0.0

Y0 = np.array([theta0, omega0])
```

Sau đó truyền `conlac_daodong` vào Euler, RK2 hoặc RK4 để giải.
