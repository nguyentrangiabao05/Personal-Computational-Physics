set term pngcairo size 800,500
set output "plot_tatca_gnu.png"

set xrange [0:5]
set yrange [-20:10]

set xlabel "x"
set ylabel "y"

set key top left

plot \
    "Euler_PT2.txt" using 2:3 with lines lw 2 title "Euler", \
    "RK2_PT2.txt"   using 2:3 with lines lw 2 title "RK2", \
    "RK3_PT2.txt"   using 2:3 with lines lw 2 title "RK3", \
    "RK4_PT2.txt"   using 2:3 with lines lw 2 title "RK4", \
    (x+1)**2 - 0.5*exp(x) with lines lw 2 title "Calculus"