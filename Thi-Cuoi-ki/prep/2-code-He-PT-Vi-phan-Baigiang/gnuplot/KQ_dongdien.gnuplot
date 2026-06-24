set terminal pngcairo size 1000,700 enhanced font "Arial,18"
set output "Dong_dien_giai_ptvp.png"

set title "Dong dien giai RK4"
set xlabel "Time (t)"
set ylabel "Voltage (V)"

set grid
set key top left

#set xrange [0:40]
set yrange [0:3]

filename_dondien = "../KQ_dongdien-RK4.txt"

plot filename_dondien using 1:2 with linespoints linewidth 2 pointtype 7 linecolor rgb "red" title "I1", \
     filename_dondien using 1:3 with linespoints linewidth 2 pointtype 5 linecolor rgb "blue" title "I2"