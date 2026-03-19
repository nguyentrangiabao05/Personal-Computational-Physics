set term pngcairo size 800,500
set output "yprime_equals_x.png"

set xrange [0:10]
set yrange [0:50]

set xlabel "x"
set ylabel "y"

unset key


plot \
    "Euler_PT1.txt" using 2:3 with lines lw 2, \
    x**2/2 with lines lw 2