set term pngcairo size 800,500
set output "yprime_equals_x_bai2.png"

set xrange [0:5]
set yrange [-20:10]

set xlabel "x"
set ylabel "y"

unset key


plot \
    "Euler_PT2.txt" using 2:3 with lines lw 2, \
    (x+1)**2 - 0.5*exp(x) with lines lw 2