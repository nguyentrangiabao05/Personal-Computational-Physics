import numpy as np

###########################################
N_time = 6000
N_x = 200
x_t0 = 100 #Do C
t_x0 = 0 #Do C
t_xl = 0 #Do C

# Tham so bai toan
kappa  = 210
C = 900
rho = 2700
l = 1
t_max = 1800

tol  = 1e-6
N_max = 10000
###########################################

def dieukienbien(N_time,N_x,x_t0,t_x0,t_xl):
    u = np.zeros((N_x,N_time),dtype=float)

    #bien dau la t, bien thu 2 la x
    #x_t0 la tai thoi diem ban dau T = 100

    for i in range(N_time):
        u[N_x-1][i] = (t_xl)

    for i in range(N_time):
        u[0][i] = (t_x0)

    for i in range(N_x):
        u[i][0] = (x_t0)

    return u

def hamso(kappa,C, rho, N_x, N_time,l,t_max):
    h = l/(N_x-1)
    k = t_max/(N_time-1)
    alpha = np.sqrt(kappa/(C*rho))
    eta  = alpha ** 2 * k / h**2

    beta1 = eta/(2*eta+1)
    beta2 = 1/(2*eta+1)
    return beta1, beta2, h, k

def luufile(u, N_x, N_time, l, t_max,h,k):
    filename = "truyen_nhiet.dat"
    with open(filename, "w", encoding="utf-8") as file:
            file.write("# Bai toan truyen nhiet 1D\n")
            file.write("# Phuong phap sai phan huu han hien\n")
            file.write("#\n")
            file.write(f"# N_x    = {N_x}\n")
            file.write(f"# N_time = {N_time}\n")
            file.write(f"# l      = {l}\n")
            file.write(f"# t_max  = {t_max}\n")
            file.write("#\n")
            file.write("# Cot du lieu: j   i   t   x   u\n")

            for j in range(N_time):
                t = j * k
                for i in range(N_x):
                    x = i * h
                    file.write(f"{j:5d} {i:5d} {t:15.8e} {x:15.8e} {u[i][j]:15.8e}\n")
                file.write("\n")

def tinhtoan_backward(u, kappa, C, rho, N_x, N_time, l, t_max, N_max,tol):
    beta1, beta2, h, k  = hamso(kappa,C, rho, N_x, N_time,l,t_max)
    filename = f"ketqua_hoitu.dat"
    with open(filename, "w", encoding="utf-8") as file:
        for j in range (1,N_time):
            err = np.zeros(N_x-2)
            for q in range (1,N_max):
                u_old = u.copy()
                for i in range(1,N_x-1):
                    u[i][j] = beta1 * (u[i+1][j] + u[i-1][j]) + beta2 * u[i][j-1]   
                    err[i-1] = abs(u[i][j] - u_old[i][j])
                if max(err) < tol:
                    file.write(f"Ket qua hoi tu tai vong lap thu: {q} tai buoc thoi gian thu: {j}.\n")
                    if np.mod(j, 50) == 0:
                        print(f"Ket qua hoi tu tai vong lap thu: {q} tai buoc thoi gian thu: {j}.\n")
                    break
                else:
                    continue
        luufile(u, N_x, N_time, l, t_max,h,k)
    return u

u = dieukienbien(N_time,N_x,x_t0,t_x0,t_xl)
solution  = tinhtoan_backward(u, kappa,C, rho, N_x, N_time,l,t_max, N_max,tol)