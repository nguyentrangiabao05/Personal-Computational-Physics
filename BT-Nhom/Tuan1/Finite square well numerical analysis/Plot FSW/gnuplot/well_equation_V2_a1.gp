set encoding utf8
# Xuất file PDF
set terminal pdfcairo size 5in, 3.5in enhanced font 'Arial,12'
set output 'WaveFunc_V2_a1.pdf'

# Thong so Vat Ly
a = 2.0
V0 = 1.0
z1 = 0.40414

E1 = -0.15
z0 = 0.43954522

# Ham song
k(z) = z / a
kappa(z) = sqrt(z0**2 - z**2) / a


psi(x, z) = (x < -a) ? (cos(k(z)*a) * exp(kappa(z)*(x+a))) : \
            (x > a)  ? (cos(k(z)*a) * exp(-kappa(z)*(x-a))) : \
            cos(k(z)*x)

### Plot
set title "Giếng hữu hạn V_0 = 1(Mev), a = 2(fm)" font "Arial Bold,14"
set xlabel "x (fm)" font ",13"
set ylabel "Năng lượng (Mev)" font ",13"

set xrange [-45:45]
set yrange [-1.05:0.05]
set samples 1000

# Tang kich thuoc so truc
set xtics font ",12"
set ytics font ",12"

# Ve cac vach chia
set mxtics 5
set mytics 5


# Ve gieng the
set arrow from -a,0 to -a,-V0 nohead lc rgb "black" dt 2 lw 1.5
set arrow from a,0 to a,-V0 nohead lc rgb "black" dt 2 lw 1.5
set arrow from -a,-V0 to a,-V0 nohead lc rgb "black" dt 2 lw 1.5
set arrow from -45,0 to -a,0 nohead lc rgb "black" dt 2 lw 1.5
set arrow from a,0 to 45,0 nohead lc rgb "black" dt 2 lw 1.5

# Ve muc nang luong
set style line 10 lc rgb "blue" dt 3 lw 1.5

set arrow from -45,E1 to 45,E1 nohead ls 10


# Label tung nang luong
set label 1 sprintf("{/Symbol y}_1 : E_1 = %.2f(Mev)", E1) at 20, E1-0.05 tc rgb "blue" font ",10"
set label 2 "V" at 40, -0.05 font "Arial,14"

# Ve ham song
scale = 0.1

plot E1 + psi(x, z1)*scale title "" lw 2.5 lc rgb "blue"

set output