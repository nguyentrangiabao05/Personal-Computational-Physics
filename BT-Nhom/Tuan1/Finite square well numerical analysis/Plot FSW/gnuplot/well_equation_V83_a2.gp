set encoding utf8
# Xuất file PDF
set terminal pdfcairo size 5in, 3.5in enhanced font 'Arial,12'
set output 'WaveFunc_V83_a2.pdf'

# Thong so Vat Ly
a = 2.0
V0 = 83.0
z1 = 1.25264
z2 = 3.59675
E1 = -74.88
E2 = -16.04
z0 = 4.00444753

# Ham song
k(z) = z / a
kappa(z) = sqrt(z0**2 - z**2) / a


psi(x, z) = (x < -a) ? (cos(k(z)*a) * exp(kappa(z)*(x+a))) : \
            (x > a)  ? (cos(k(z)*a) * exp(-kappa(z)*(x-a))) : \
            cos(k(z)*x)

### Plot
set title "Giếng hữu hạn V_0 = 83(Mev), a = 2(fm)" font "Arial Bold,14"
set xlabel "x (fm)" font ",13"
set ylabel "Năng lượng (Mev)" font ",13"

set xrange [-6.5:6.5]
set yrange [-85:5]
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
set arrow from -6.5,0 to -a,0 nohead lc rgb "black" dt 2 lw 1.5
set arrow from a,0 to 6.5,0 nohead lc rgb "black" dt 2 lw 1.5

# Ve muc nang luong
set style line 10 lc rgb "blue" dt 3 lw 1.5
set style line 11 lc rgb "red" dt 3 lw 1.5
set arrow from -6.5,E1 to 6.5,E1 nohead ls 10
set arrow from -6.5,E2 to 6.5,E2 nohead ls 11

# Label tung nang luong
set label 1 sprintf("{/Symbol y}_1 : E_1 = %.2f(Mev)", E1) at 3.5, E1-5 tc rgb "blue" font ",10"
set label 2 sprintf("{/Symbol y}_2 : E_2 = %.2f(Mev)", E2) at 3.5, E2-5 tc rgb "red" font ",10"
set label 3 "V" at 6, -5 font "Arial,14"

# Ve ham song
scale = 15.0

plot E1 + psi(x, z1)*scale title "" lw 2.5 lc rgb "blue", \
     E2 + psi(x, z2)*scale title "" lw 2.5 lc rgb "red"

set output