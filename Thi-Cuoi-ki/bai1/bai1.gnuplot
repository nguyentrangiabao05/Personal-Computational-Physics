set terminal pngcairo size 1000,700 enhanced font "Arial,18"
set output "Sosanh_MC_Riemann_bai1.png"

set title "Bai 1: Gnuplot"
set xlabel "R_C/R"
set ylabel "Moment quan tinh (I_z)"

set grid
set key top left

set xrange [0:1]
set yrange [7.0:25]

filename_MC = "./KQ_MC_bai1.txt"
filename_Riemann = "./KQ_Riemann_bai1.txt"

plot filename_MC using 1:2 with linespoints linewidth 2 pointtype 7 linecolor rgb "red" title "MC", \
     filename_Riemann using 1:2 with linespoints linewidth 2 pointtype 5 linecolor rgb "blue" title "Riemann"