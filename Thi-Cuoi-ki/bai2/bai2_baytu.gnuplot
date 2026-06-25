set terminal pngcairo size 1000,800 enhanced font "Arial,18"
set output "bai2_baytu_3D.png"

set title "Quy dao trong bay tu (Gnuplot)"
set xlabel "x"
set ylabel "y"
set zlabel "z"

filename = "./KQ_bai2-baytu-RK4.txt"

sp filename using 2:3:4 w l notitle