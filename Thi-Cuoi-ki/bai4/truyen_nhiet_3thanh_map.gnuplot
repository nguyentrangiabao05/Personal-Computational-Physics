set terminal pngcairo size 1000,800 enhanced font "Arial,18"
set output "bai4_3thanh_map.png"

set title "Ban do mau tinh dien 2D"
set xlabel "Time (t)"
set ylabel "x"

set size ratio -1
set view map

set pm3d map
set palette rgbformulae 33,13,10
set colorbox
set cblabel "Temp"

filename = "./truyen_nhiet_3thanh_backward_result.txt"

splot filename using 3:4:5 with pm3d notitle