set terminal pngcairo size 1000,700 enhanced font "Arial,18"
set output "KQ_MC_hinhxuyen.png"

set title "Dien the hinh xuyen"
set xlabel "d"
set ylabel "Voltage (V)"

set grid
set key top left

set xrange [0:100]
set yrange [0:2000]

filename = "../KQ_MC_hinhxuyen.txt"

plot filename using 1:2 with linespoints linewidth 2 pointtype 7 title "data"