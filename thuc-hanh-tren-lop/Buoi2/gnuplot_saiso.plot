set term pngcairo size 800,500
set output "montecarlo_pi_hoitu.png"

set xrange [1e2:1e5]
set yrange [2.9:3.4]

set xlabel "N"
set ylabel "Estimate pi"

set logscale x 10
unset key

plot \
        "Ketquahoitu.txt" using 1:2 with lines lw 2, \
        3.14159265359 with line lw 2