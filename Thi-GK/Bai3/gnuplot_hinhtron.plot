set term pngcairo size 1200,1200
set output "montecarlo_pi.png"
set size ratio -1
set xrange [-1:1]
set yrange [-1:1]
set xlabel "x"
set ylabel "y"
unset key


set parametric
p \
    "bentrong.txt" u 2:3 every ::3 w p pt 14 ps 0.6, \
    "benngoai.txt" u 2:3 every ::3 w p pt 14 ps 0.6, \
    cos(t), sin(t) w l lw 4