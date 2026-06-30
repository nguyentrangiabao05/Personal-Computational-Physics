#!/usr/bin/env python3
"""
Tạo GIF phân bố nhiệt độ dọc theo thanh từ file dữ liệu `truyen_nhiet.dat`.

Định dạng file mong đợi:
    j   i   t   x   u

Ví dụ:
    python3 create_heat_gif.py
    python3 create_heat_gif.py -i truyen_nhiet.dat -o truyen_nhiet.gif --frame-step 10 --fps 8
"""

import argparse
import numpy as np
import matplotlib

# Dùng backend không tương tác để chạy ổn trên terminal / server
matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter


# =========================================================
# Mặc định
# =========================================================
DEFAULT_INPUT = "truyen_nhiet.dat"
DEFAULT_OUTPUT = "truyen_nhiet.gif"

FIG_WIDTH_CM = 20.0
FIG_HEIGHT_CM = 6.0
ROD_THICKNESS = 1.0
N_REPEAT_Y = 40
CMAP = "coolwarm"


# =========================================================
# Đọc dữ liệu
# =========================================================
def load_heat_data(filename: str):
    data = np.loadtxt(filename, comments="#")

    if data.ndim == 1:
        data = data.reshape(1, -1)

    if data.shape[1] < 5:
        raise ValueError("File dữ liệu phải có ít nhất 5 cột: j, i, t, x, u")

    # Sắp xếp theo (j, i) để reshape chắc chắn đúng
    order = np.lexsort((data[:, 1], data[:, 0]))
    data = data[order]

    j_col = data[:, 0].astype(int)
    i_col = data[:, 1].astype(int)
    t_col = data[:, 2]
    x_col = data[:, 3]
    u_col = data[:, 4]

    j_vals = np.unique(j_col)
    i_vals = np.unique(i_col)

    n_time = len(j_vals)
    n_x = len(i_vals)

    if data.shape[0] != n_time * n_x:
        raise ValueError(
            "Số dòng dữ liệu không khớp với lưới (N_time x N_x). "
            "Kiểm tra lại file output."
        )

    U = u_col.reshape(n_time, n_x)
    t_vals = t_col.reshape(n_time, n_x)[:, 0]
    x_vals = x_col.reshape(n_time, n_x)[0, :]

    return x_vals, t_vals, U


# =========================================================
# Tạo ảnh 2D từ profile nhiệt độ 1D
# =========================================================
def make_rod_image(u_1d: np.ndarray, n_repeat_y: int = N_REPEAT_Y) -> np.ndarray:
    return np.repeat(u_1d[np.newaxis, :], n_repeat_y, axis=0)


# =========================================================
# Tạo GIF
# =========================================================
def create_gif(
    input_file: str,
    output_file: str,
    frame_step: int,
    fps: int,
    cmap: str,
    repeat_y: int,
    fig_width_cm: float,
    fig_height_cm: float,
    rod_thickness: float,
):
    x_vals, t_vals, U = load_heat_data(input_file)

    if frame_step <= 0:
        raise ValueError("frame_step phải là số nguyên dương")
    if fps <= 0:
        raise ValueError("fps phải là số nguyên dương")

    frame_indices = np.arange(0, len(t_vals), frame_step, dtype=int)
    if len(frame_indices) == 0:
        frame_indices = np.array([0], dtype=int)

    if frame_indices[-1] != len(t_vals) - 1:
        frame_indices = np.append(frame_indices, len(t_vals) - 1)

    vmin = np.min(U)
    vmax = np.max(U)

    fig = plt.figure(figsize=(fig_width_cm / 2.54, fig_height_cm / 2.54))
    ax = fig.add_axes([0.08, 0.22, 0.78, 0.65])

    rod0 = make_rod_image(U[frame_indices[0]], n_repeat_y=repeat_y)

    im = ax.imshow(
        rod0,
        origin="lower",
        aspect="auto",
        cmap=cmap,
        extent=[x_vals[0], x_vals[-1], 0.0, rod_thickness],
        vmin=vmin,
        vmax=vmax,
        interpolation="nearest",
    )

    ax.set_xlabel("x")
    ax.set_yticks([])
    title = ax.set_title(
        f"Temperature distribution at t = {t_vals[frame_indices[0]]:.6e}"
    )

    time_text = fig.text(
        0.08,
        0.10,
        f"t = {t_vals[frame_indices[0]]:.6e}   (j = {frame_indices[0]})",
        fontsize=10,
    )

    cbar = fig.colorbar(im, ax=ax, pad=0.02)
    cbar.set_label("Temperature")

    def update(frame_no: int):
        idx = frame_indices[frame_no]
        rod_img = make_rod_image(U[idx], n_repeat_y=repeat_y)
        im.set_data(rod_img)
        title.set_text(f"Temperature distribution at t = {t_vals[idx]:.6e}")
        time_text.set_text(f"t = {t_vals[idx]:.6e}   (j = {idx})")
        return [im, title, time_text]

    anim = FuncAnimation(
        fig,
        update,
        frames=len(frame_indices),
        interval=1000 / fps,
        blit=False,
        repeat=True,
    )

    writer = PillowWriter(fps=fps)
    anim.save(output_file, writer=writer)
    plt.close(fig)

    return {
        "input_file": input_file,
        "output_file": output_file,
        "n_time": len(t_vals),
        "n_x": len(x_vals),
        "n_frames": len(frame_indices),
        "frame_step": frame_step,
        "fps": fps,
        "t_min": float(np.min(t_vals)),
        "t_max": float(np.max(t_vals)),
        "u_min": float(vmin),
        "u_max": float(vmax),
    }


def build_parser():
    parser = argparse.ArgumentParser(
        description="Tạo GIF phân bố nhiệt độ từ file truyen_nhiet.dat"
    )
    parser.add_argument(
        "-i", "--input", default=DEFAULT_INPUT, help="Tên file dữ liệu đầu vào"
    )
    parser.add_argument(
        "-o", "--output", default=DEFAULT_OUTPUT, help="Tên file GIF đầu ra"
    )
    parser.add_argument(
        "--frame-step",
        type=int,
        default=10,
        help="Lấy mỗi frame_step bước thời gian một frame",
    )
    parser.add_argument(
        "--fps",
        type=int,
        default=8,
        help="Số frame mỗi giây của GIF",
    )
    parser.add_argument(
        "--cmap",
        default=CMAP,
        help="Colormap matplotlib, ví dụ: coolwarm, hot, plasma, inferno",
    )
    parser.add_argument(
        "--repeat-y",
        type=int,
        default=N_REPEAT_Y,
        help="Số lần lặp theo trục y để thanh nhiệt dày hơn",
    )
    parser.add_argument(
        "--fig-width-cm",
        type=float,
        default=FIG_WIDTH_CM,
        help="Độ rộng hình (cm)",
    )
    parser.add_argument(
        "--fig-height-cm",
        type=float,
        default=FIG_HEIGHT_CM,
        help="Độ cao hình (cm)",
    )
    parser.add_argument(
        "--rod-thickness",
        type=float,
        default=ROD_THICKNESS,
        help="Độ dày thanh trong hệ trục vẽ",
    )
    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    info = create_gif(
        input_file=args.input,
        output_file=args.output,
        frame_step=args.frame_step,
        fps=args.fps,
        cmap=args.cmap,
        repeat_y=args.repeat_y,
        fig_width_cm=args.fig_width_cm,
        fig_height_cm=args.fig_height_cm,
        rod_thickness=args.rod_thickness,
    )

    print("Đã tạo GIF thành công.")
    print(f"Input file : {info['input_file']}")
    print(f"Output file: {info['output_file']}")
    print(f"N_time     : {info['n_time']}")
    print(f"N_x        : {info['n_x']}")
    print(f"Số frame   : {info['n_frames']}")
    print(f"frame_step : {info['frame_step']}")
    print(f"fps        : {info['fps']}")
    print(f"Khoảng t   : [{info['t_min']:.6e}, {info['t_max']:.6e}]")
    print(f"Khoảng u   : [{info['u_min']:.6e}, {info['u_max']:.6e}]")


if __name__ == "__main__":
    main()
