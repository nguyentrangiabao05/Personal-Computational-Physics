set terminal pngcairo size 1000,700 enhanced font "Arial,18"
set output "Sosanh_MC_Riemann_hinhxuyen.png"

set title "Dien the hinh xuyen so sanh MC va Riemann"
set xlabel "d"
set ylabel "Voltage (V)"

set grid
set key top left

set xrange [0:40]
set yrange [0:2000]

filename_MC = "../KQ_MC_hinhxuyen.txt"
filename_Riemann = "../KQ_Riemann_hinhxuyen.txt"

plot filename_MC using 1:2 with linespoints linewidth 2 pointtype 7 linecolor rgb "red" title "MC", \
     filename_Riemann using 1:2 with linespoints linewidth 2 pointtype 5 linecolor rgb "blue" title "Riemann"