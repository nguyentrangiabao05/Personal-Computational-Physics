"""
Interactive viewer doc du lieu tu file ketqua.txt (output tu ham_forward).
- Tu dong parse header de lay N_x, N_time
- Tu cache ra .npz de lan doc sau nhanh hon (vai chuc giay -> <1s)
- Slider + Play/Pause + Reset

Chay:
    python wave_viewer_from_file.py                # doc ketqua.txt mac dinh
    python wave_viewer_from_file.py ten_file.txt   # doc file khac
"""

import sys
import os
import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button

# ============ Tham so hien thi ============
TIME_STRIDE  = 10   # Chi giu 1 tren mot so frame (10001 -> 1001 frame)
SPACE_STRIDE = 1    # Giu het diem khong gian

# ============ Parse header ============
def parse_header(filename):
    """Doc header '# N_x = ...' va '# N_time = ...'"""
    m, n = None, None
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            if not line.startswith('#'):
                break
            if 'N_x' in line:
                m = int(line.split('=')[1].strip())
            elif 'N_time' in line:
                n = int(line.split('=')[1].strip())
    if m is None or n is None:
        raise ValueError("Khong parse duoc N_x / N_time tu header")
    return m, n

# ============ Doc file (co cache) ============
def load_file(filename, time_stride=1, space_stride=1):
    cache_file = filename.rsplit('.', 1)[0] + '.npz'

    # Dung cache neu con moi
    if os.path.exists(cache_file):
        if os.path.getmtime(cache_file) >= os.path.getmtime(filename):
            print(f"[cache hit] Doc {cache_file}...")
            d = np.load(cache_file)
            return (d['u'][::time_stride, ::space_stride],
                    d['x'][::space_stride],
                    d['t'][::time_stride])

    # Parse header
    m, n = parse_header(filename)
    size_mb = os.path.getsize(filename) / 1e6
    print(f"[parse] N_space = {m}, N_time = {n}, file size = {size_mb:.1f} MB")
    print(f"[read]  Dang doc du lieu (co the mat 30-120s voi file lon)...")
    t0 = time.time()

    # Uu tien pandas (~10x nhanh hon loadtxt)
    try:
        import pandas as pd
        df = pd.read_csv(filename, comment='#', sep=r'\s+',
                         names=['t_step', 'x_step', 't', 'x', 'u'],
                         skip_blank_lines=True, engine='c')
        data = df[['t', 'x', 'u']].to_numpy()
    except ImportError:
        print("        (khong co pandas, fallback sang numpy.loadtxt - cham hon)")
        data = np.loadtxt(filename, comments='#', usecols=(2, 3, 4))

    print(f"[read]  Doc xong {data.shape[0]} dong trong {time.time()-t0:.1f}s")

    # Reshape: data[i*m + j] la (t_i, x_j, u_ij)
    t_all = data[:, 0].reshape(n, m)[:, 0]    # t chi phu thuoc i
    x_all = data[:, 1].reshape(n, m)[0, :]    # x chi phu thuoc j
    u_all = data[:, 2].reshape(n, m)

    # Luu cache
    print(f"[cache] Luu {cache_file} cho lan sau...")
    np.savez_compressed(cache_file, u=u_all, x=x_all, t=t_all)

    return (u_all[::time_stride, ::space_stride],
            x_all[::space_stride],
            t_all[::time_stride])

# ============ Main ============
filename = sys.argv[1] if len(sys.argv) > 1 else 'ketqua.txt'

if not os.path.exists(filename):
    print(f"Khong tim thay file: {filename}")
    sys.exit(1)

u, x, t = load_file(filename, TIME_STRIDE, SPACE_STRIDE)
print(f"[plot]  Hien thi {u.shape[0]} frame x {u.shape[1]} diem")

# ============ Plot interactive ============
fig, ax = plt.subplots(figsize=(10, 6))
plt.subplots_adjust(left=0.1, bottom=0.25, right=0.95, top=0.92)

(line,) = ax.plot(x, u[0, :], 'b-', lw=2, label='u(x, t)')
ax.plot(x, u[0, :], 'k--', lw=0.8, alpha=0.3, label='IC: u(x, 0)')

u_max = np.abs(u).max()
ax.set_xlim(x[0], x[-1])
ax.set_ylim(-1.2*u_max, 1.2*u_max)
ax.set_xlabel('x')
ax.set_ylabel('u(x, t)')
ax.axhline(0, color='k', lw=0.5)
ax.grid(True, alpha=0.3)
ax.legend(loc='upper right')
title = ax.set_title(f't = {t[0]:.4f}   (frame 0 / {len(t)-1})')

# --- Slider ---
ax_slider = plt.axes([0.1, 0.1, 0.65, 0.03])
slider = Slider(ax_slider, 'Frame', 0, len(t)-1,
                valinit=0, valstep=1, valfmt='%0.0f')

def update(val):
    idx = int(slider.val)
    line.set_ydata(u[idx, :])
    title.set_text(f't = {t[idx]:.4f}   (frame {idx} / {len(t)-1})')
    fig.canvas.draw_idle()

slider.on_changed(update)

# --- Play/Pause ---
ax_play = plt.axes([0.8, 0.1, 0.08, 0.04])
btn_play = Button(ax_play, 'Play')
state = {'playing': False, 'speed': 2}

def toggle_play(event):
    state['playing'] = not state['playing']
    btn_play.label.set_text('Pause' if state['playing'] else 'Play')

btn_play.on_clicked(toggle_play)

# --- Reset ---
ax_reset = plt.axes([0.89, 0.1, 0.06, 0.04])
btn_reset = Button(ax_reset, 'Reset')

def reset(event):
    slider.set_val(0)
    state['playing'] = False
    btn_play.label.set_text('Play')

btn_reset.on_clicked(reset)

# --- Timer ---
def on_timer():
    if state['playing']:
        idx = int(slider.val) + state['speed']
        if idx >= len(t):
            idx = 0
        slider.set_val(idx)

timer = fig.canvas.new_timer(interval=30)
timer.add_callback(on_timer)
timer.start()

plt.show()