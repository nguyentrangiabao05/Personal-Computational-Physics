"""
Interactive viewer cho PT song 1D: u_tt = c^2 u_xx
- Slider keo thoi gian
- Nut Play/Pause de tu dong chay animation
- Nut Reset ve t=0

Chay: python wave_viewer.py
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button

# ============ Tham so ============
L       = 1.0      # Chieu dai day
c       = 1.0      # Van toc song
t_max   = 5.0      # Thoi gian mo phong
dx      = 0.005    # Buoc khong gian  -> 201 diem
dt      = 0.0025   # Buoc thoi gian   -> beta = c*dt/dx = 0.5 (on dinh)

# ============ Dieu kien ban dau ============
def f_x(x, l):
    """u(x, 0): day tam giac, dinh tai x = 0.8L, bien do 1"""
    return np.where(x <= 0.8*l, 1.25*x/l, 5.0 - 5.0*x/l)

def g_x(x, l):
    """u_t(x, 0) = 0: day tha tu trang thai tinh"""
    return np.zeros_like(x)

# ============ Giai PT song ============
def solve_wave(c, dt, dx, t_max, L):
    m = int(L / dx) + 1
    n = int(t_max / dt) + 1
    x = np.linspace(0, L, m)
    t = np.linspace(0, t_max, n)
    beta = c * dt / dx
    if beta > 1:
        raise ValueError(f"Khong on dinh: beta = {beta:.3f} > 1")
    print(f"beta = {beta:.3f} (<=1, on dinh)")

    u = np.zeros((n, m))
    # t = 0
    u[0, :] = f_x(x, L)
    # t = dt  (cong thuc bac 2 tu khai trien Taylor + PT song)
    u[1, 1:-1] = (u[0, 1:-1]
                  + dt * g_x(x[1:-1], L)
                  + 0.5 * beta**2 * (u[0, 2:] - 2*u[0, 1:-1] + u[0, :-2]))
    # Bien co dinh
    u[:, 0]  = 0.0
    u[:, -1] = 0.0
    # Vong lap chinh (vector hoa theo khong gian)
    for i in range(1, n-1):
        u[i+1, 1:-1] = (2*(1 - beta**2) * u[i, 1:-1]
                        + beta**2 * (u[i, 2:] + u[i, :-2])
                        - u[i-1, 1:-1])
    return u, x, t

print("Dang tinh nghiem...")
u, x, t = solve_wave(c, dt, dx, t_max, L)
print(f"Xong: {u.shape[0]} buoc thoi gian x {u.shape[1]} diem khong gian")

# ============ Plot interactive ============
fig, ax = plt.subplots(figsize=(10, 6))
plt.subplots_adjust(left=0.1, bottom=0.25, right=0.95, top=0.92)

# Duong song ban dau
(line,) = ax.plot(x, u[0, :], 'b-', lw=2, label='u(x, t)')
# Ve duong IC mo de tham chieu
ax.plot(x, u[0, :], 'k--', lw=0.8, alpha=0.3, label='IC: u(x, 0)')

u_max = np.abs(u).max()
ax.set_xlim(0, L)
ax.set_ylim(-1.2*u_max, 1.2*u_max)
ax.set_xlabel('x')
ax.set_ylabel('u(x, t)')
ax.axhline(0, color='k', lw=0.5)
ax.grid(True, alpha=0.3)
ax.legend(loc='upper right')
title = ax.set_title(f't = {t[0]:.3f}   (step 0 / {len(t)-1})')

# --- Slider thoi gian ---
ax_slider = plt.axes([0.1, 0.1, 0.65, 0.03])
slider = Slider(ax_slider, 'Thoi gian', 0, len(t)-1,
                valinit=0, valstep=1, valfmt='%0.0f')

def update(val):
    idx = int(slider.val)
    line.set_ydata(u[idx, :])
    title.set_text(f't = {t[idx]:.3f}   (step {idx} / {len(t)-1})')
    fig.canvas.draw_idle()

slider.on_changed(update)

# --- Nut Play/Pause ---
ax_play = plt.axes([0.8, 0.1, 0.08, 0.04])
btn_play = Button(ax_play, 'Play')

state = {'playing': False, 'speed': 4}  # speed = so step nhay moi frame

def toggle_play(event):
    state['playing'] = not state['playing']
    btn_play.label.set_text('Pause' if state['playing'] else 'Play')

btn_play.on_clicked(toggle_play)

# --- Nut Reset ---
ax_reset = plt.axes([0.89, 0.1, 0.06, 0.04])
btn_reset = Button(ax_reset, 'Reset')

def reset(event):
    slider.set_val(0)
    state['playing'] = False
    btn_play.label.set_text('Play')

btn_reset.on_clicked(reset)

# --- Timer cho animation ---
def on_timer():
    if state['playing']:
        idx = int(slider.val) + state['speed']
        if idx >= len(t):
            idx = 0                       # loop lai
        slider.set_val(idx)

timer = fig.canvas.new_timer(interval=30)   # ~33 fps
timer.add_callback(on_timer)
timer.start()

plt.show()