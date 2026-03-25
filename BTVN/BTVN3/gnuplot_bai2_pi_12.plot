set term pngcairo size 800,500
set output "bai2_pi_12.png"

set xrange [0:10]
set yrange [-0.5:0.5]

set xlabel "t(time)"
set ylabel "theta (rad)"

set key top right

plot \
    "cau2_rk4_pi_12_pt1.txt" using 2:3 with lines lw 2 lc rgb "red" title "PT [1]", \
    "cau2_rk4_pi_12_pt2.txt" using 2:3 with lines lw 2 lc rgb "blue" title "PT [2]"