base_name = "ketqua_bai1_beta_0.63"
input_file = base_name . ".txt"
output_file = base_name . ".png"

set xlabel "Khong gian X"
set ylabel "Thoi gian T"
set zlabel "Bien do U"
set grid

set output output_file


splot input_file every :20 using 4:3:5 with lines

set output
print "Da luu file: " . output_file