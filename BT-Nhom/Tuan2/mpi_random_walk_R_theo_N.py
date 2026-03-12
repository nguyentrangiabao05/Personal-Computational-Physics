from mpi4py import MPI
import numpy as np


a = -1.0
b =  1.0
x0 = 0.0
y0 = 0.0

N_min = 1
N_max = 100000
step_N = 10


def chuanhoa_chuyendong(a, b, N, rng):
    delta_x = np.empty(N, dtype=np.float64)
    delta_y = np.empty(N, dtype=np.float64)

    for i in range(N):
        while True:
            delta_x_star = rng.uniform(a, b)
            delta_y_star = rng.uniform(a, b)
            L_star = np.sqrt(delta_x_star**2 + delta_y_star**2)

            if L_star > 0.0:
                delta_x[i] = delta_x_star / L_star
                delta_y[i] = delta_y_star / L_star
                break

    return delta_x, delta_y



def toado_moilan_chuyendong(a, b, N, x0, y0, rng):

    x = np.empty(N + 1, dtype=np.float64)
    y = np.empty(N + 1, dtype=np.float64)

    x[0] = x0
    y[0] = y0

    delta_x, delta_y = chuanhoa_chuyendong(a, b, N, rng)

    for i in range(N):
        x[i + 1] = x[i] + delta_x[i]
        y[i + 1] = y[i] + delta_y[i]

    return x, y



def tinh_khoangcachbinhphuong_khongfile(N, a, b, x0, y0, rng):
    number_of_RDW = max(1, int(np.sqrt(N)))

    R2_total = 0.0

    for _ in range(number_of_RDW):
        x, y = toado_moilan_chuyendong(a, b, N, x0, y0, rng)
        d = (x[-1] - x[0])**2 + (y[-1] - y[0])**2
        R2_total += d

    R2_mean = R2_total / number_of_RDW
    return R2_mean

def main():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    N_values = list(range(N_min, N_max, step_N))


    local_N_values = N_values[rank::size]

    rng = np.random.default_rng(seed=12345 + rank)

    local_results = []

    for N in local_N_values:
        R2_mean = tinh_khoangcachbinhphuong_khongfile(N, a, b, x0, y0, rng)
        R_mean = np.sqrt(R2_mean)
        local_results.append((N, np.sqrt(N), R_mean))

    gathered_results = comm.gather(local_results, root=0)

    if rank == 0:
        all_results = []
        for part in gathered_results:
            all_results.extend(part)

        all_results.sort(key=lambda x: x[0])

        with open("Tuong_quan_giua_sqrt(R2_mean)_voi_sqrt(N).txt", "w", encoding="utf-8") as file:
            file.write("# Tuong quan giua sqrt(R2_mean) voi sqrt(N)\n")
            file.write("#" * 60 + "\n")
            file.write(f"#{'N':>8s} {'sqrt(N)':>20s} {'R_mean':>20s}\n")

            for N, sqrtN, R_mean in all_results:
                file.write(f"{N:8d} {sqrtN:20.12f} {R_mean:20.12f}\n")

        print("Da ghi file: Tuong_quan_giua_sqrt(R2_mean)_voi_sqrt(N).txt")


if __name__ == "__main__":
    main()