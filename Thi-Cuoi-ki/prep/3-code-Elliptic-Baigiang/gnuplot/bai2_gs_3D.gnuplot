set terminal pngcairo size 1000,800 enhanced font "Arial,18"
set output "bai2_gs_3D.png"

set title "3D tinh dien"
set xlabel "x"
set ylabel "y"
set zlabel "V"

filename = "../bai2_gs_result.txt"

sp filename using 1:2:3 w l notitle