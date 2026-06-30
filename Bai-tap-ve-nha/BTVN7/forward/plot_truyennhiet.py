import matplotlib
matplotlib.use("TkAgg")

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# =========================================================
# Cau hinh
# =========================================================
DATA_FILE = "truyen_nhiet.dat"

FIG_WIDTH_CM = 10.0   # do rong hinh ~ 20 cm
FIG_HEIGHT_CM = 6.0   # chieu cao tong the cua hinh
ROD_THICKNESS = 1.0   # do day thanh trong he truc
N_REPEAT_Y = 40       # lap lai theo chieu y de thanh nhiet day hon

CMAP = "coolwarm"      # co the doi: viridis, plasma, coolwarm, hot, inferno

# =========================================================
# Doc du lieu tu file
# Dinh dang mong doi:
# j   i   t   x   u
# Co the co cac dong comment bat dau bang '#'
# =========================================================
def load_heat_data(filename):
    data = np.loadtxt(filename, comments="#")

    if data.ndim == 1:
        data = data.reshape(1, -1)

    if data.shape[1] < 5:
        raise ValueError("File du lieu phai co it nhat 5 cot: j, i, t, x, u")

    # Sap xep lai theo (j, i) de reshape cho chac chan
    order = np.lexsort((data[:, 1], data[:, 0]))
    data = data[order]

    j_col = data[:, 0].astype(int)
    i_col = data[:, 1].astype(int)
    t_col = data[:, 2]
    x_col = data[:, 3]
    u_col = data[:, 4]

    j_vals = np.unique(j_col)
    i_vals = np.unique(i_col)

    N_time = len(j_vals)
    N_x = len(i_vals)

    if data.shape[0] != N_time * N_x:
        raise ValueError(
            "So dong du lieu khong khop voi luoi (N_time x N_x). "
            "Kiem tra lai file output."
        )

    # Sau khi da sort theo (j, i), co the reshape truc tiep
    U = u_col.reshape(N_time, N_x)
    t_vals = t_col.reshape(N_time, N_x)[:, 0]
    x_vals = x_col.reshape(N_time, N_x)[0, :]

    return x_vals, t_vals, U


# =========================================================
# Tao anh 2D tu 1 profile nhiet do 1D
# =========================================================
def make_rod_image(u_1d, n_repeat_y=N_REPEAT_Y):
    return np.repeat(u_1d[np.newaxis, :], n_repeat_y, axis=0)


# =========================================================
# Main
# =========================================================
def main():
    x_vals, t_vals, U = load_heat_data(DATA_FILE)

    vmin = np.min(U)
    vmax = np.max(U)

    fig = plt.figure(figsize=(FIG_WIDTH_CM / 2.54, FIG_HEIGHT_CM / 2.54))
    ax = fig.add_axes([0.08, 0.32, 0.78, 0.55])   # [left, bottom, width, height]

    rod0 = make_rod_image(U[0])

    im = ax.imshow(
        rod0,
        origin="lower",
        aspect="auto",
        cmap=CMAP,
        extent=[x_vals[0], x_vals[-1], 0.0, ROD_THICKNESS],
        vmin=vmin,
        vmax=vmax,
        interpolation="nearest"
    )

    ax.set_xlabel("x")
    ax.set_yticks([])
    ax.set_title(f"Temperature distribution at t = {t_vals[0]:.6e}")

    cbar = fig.colorbar(im, ax=ax, pad=0.02)
    cbar.set_label("Temperature")

    # Slider cho chi so thoi gian
    ax_slider = fig.add_axes([0.12, 0.12, 0.68, 0.05])
    slider = Slider(
        ax=ax_slider,
        label="time step j",
        valmin=0,
        valmax=len(t_vals) - 1,
        valinit=0,
        valstep=1
    )

    # Hien thi gia tri thoi gian thuc
    time_text = fig.text(
        0.12, 0.20,
        f"t = {t_vals[0]:.6e}",
        fontsize=10
    )

    def update(val):
        idx = int(slider.val)
        rod_img = make_rod_image(U[idx])
        im.set_data(rod_img)
        ax.set_title(f"Temperature distribution at t = {t_vals[idx]:.6e}")
        time_text.set_text(f"t = {t_vals[idx]:.6e}")
        fig.canvas.draw_idle()

    slider.on_changed(update)

    plt.show()


if __name__ == "__main__":
    main()