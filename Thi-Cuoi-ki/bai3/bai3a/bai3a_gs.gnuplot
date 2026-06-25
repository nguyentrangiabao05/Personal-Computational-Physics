set terminal pngcairo size 1000,800 enhanced font "Arial,18"
set output "bai3a_gs_map.png"

set title "Hieu dien the 2D (Gnuplot)"
set xlabel "x"
set ylabel "y"

set size ratio -1
set view map

set pm3d map
set palette rgbformulae 33,13,10
set colorbox
set cblabel "V"

filename = "./bai3a_gs_result.txt"

splot filename using 1:2:3 with pm3d notitle