set terminal pdfcairo size 5in, 3.5in enhanced font 'Verdana,12'
set output 'do_thi_z0_V83_a2.pdf'

z0 = 4.00444753
set title sprintf("z_0 = %.8f", z0) font "Arial Bold,14" offset 0,-0.5
f(x) = tan(x)
g(x) = sqrt((z0/x)**2 - 1)

set xrange [0:3*pi/2]
set yrange [0:5]
set samples 5000 
set clip one

# Dinh dang truc
set key at 4.3, 4.8 samplen 2 spacing 1.2
set xtics ("0" 0, "{/Symbol p}/2" pi/2, "2{/Symbol p}/2" pi, "3{/Symbol p}/2" 3*pi/2)
set xlabel "z"

# Duong tiem can
set style line 1 lc rgb 'gray' lt 2 lw 0.5
set arrow from pi/2,0 to pi/2,5 nohead ls 1
set arrow from pi,0 to pi,5 nohead ls 1

# diem giao nhau
z1 = 1.25264
z2 = 3.59675
set label 1 sprintf("z_1=%.5f", z1) at z1+0.1, f(z1)
set label 2 sprintf("z_2=%.5f", z2) at z2+0.1, f(z2)
set object 1 circle at z1, f(z1) size 0.04 fillcolor rgb "blue" lw 0 fillstyle solid
set object 2 circle at z2, f(z2) size 0.04 fillcolor rgb "blue" lw 0 fillstyle solid

# Ve line
# Sử dụng 'set term' để ngắt các đường dọc (asymptotes) tự động
set linestyle 1 lw 2 lc rgb "blue"
set linestyle 2 lw 2 lc rgb "red"

plot f(x) with lines linestyle 1 title "tan(z)", \
     (x <= z0 ? g(x) : 1/0) with lines linestyle 2 title "sqrt((z_0/z)^2 - 1)"

set output