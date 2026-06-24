set terminal pngcairo size 1000,800 enhanced font "Arial,18"
set output "truyennhiet_1thanh_3D.png"

set title "Truyen nhiet 1 thanh"
set xlabel "t"
set ylabel "x"
set zlabel "T"

filename = "../truyen_nhiet_1thanh_backward_result.txt"

sp filename using 3:4:5 w l notitle
