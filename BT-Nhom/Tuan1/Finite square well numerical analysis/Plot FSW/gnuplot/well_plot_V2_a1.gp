set terminal pdfcairo size 5in, 3.5in enhanced font 'Verdana,12'
set output 'do_thi_z0_V2_a1.pdf'

z0 = 0.43954522
z1 = 0.40414

set title sprintf("z_0 = %.8f", z0) font "Arial Bold,14" offset 0,-0.5
f(x) = tan(x)
g(x) = sqrt((z0/x)**2 - 1)

set xrange [0:pi/2]
set yrange [0:2]
set samples 100000 # Tăng cao số lượng mẫu để đường cong mượt và sát tiệm cận hơn
set clip one

# Dinh dang truc
set key at 1.5, 1.8 samplen 2 spacing 1.2
set xtics ("0" 0, "{/Symbol p}/2" pi/2)
set xlabel "z"

# Duong tiem can
#set style line 1 lc rgb 'gray' lt 2 lw 0.5
#set arrow from pi/2,0 to pi/2,5 nohead ls 1
#set arrow from pi,0 to pi,5 nohead ls 1

# Giao nhau
set label 1 sprintf("z_1=%.5f", z1) at z1+0.1, f(z1)
set object 1 circle at z1, f(z1) size 0.01 fillcolor rgb "blue" lw 0 fillstyle solid

# Ve line
# Sử dụng 'set term' để ngắt các đường dọc (asymptotes) tự động
set linestyle 1 lw 2 lc rgb "blue"
set linestyle 2 lw 2 lc rgb "red"

plot f(x) with lines linestyle 1 title "tan(z)", \
     (x <= z0 ? g(x) : 1/0) with lines linestyle 2 title "sqrt((z_0/z)^2 - 1)"

set output