set terminal pngcairo size 1000,800 enhanced font "Arial,18"
set output "bai2_gs_map.png"

set title "Ban do mau tinh dien 2D"
set xlabel "x"
set ylabel "y"

set size ratio -1
set view map

set pm3d map
set palette rgbformulae 33,13,10
set colorbox
set cblabel "V"

filename = "../bai2_gs_result.txt"

splot filename using 1:2:3 with pm3d notitle