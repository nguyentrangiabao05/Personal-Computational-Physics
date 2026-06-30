
shopt -s nullglob

files=()

for f in *.txt; do
    [[ "$f" == *-xacxuat.txt || "$f" == *-xacsuat.txt ]] && continue
    files+=("$f")
done

echo "So file se ve: ${#files[@]}"

for f in "${files[@]}"; do
    out="${f%.txt}.png"
    rm -f "$out"

    if gnuplot <<EOF
set terminal pngcairo noenhanced size 1500,1000 font "Arial,18"
set output "$out"

set title "${f%.txt}"
set xlabel "t"
set ylabel "x"
set zlabel "|psi(x,t)|"

set view 60,30

splot "$f" u 1:2:5 w l lw 3 notitle

unset output
EOF
    then
        echo "Da tao: $out"
    else
        echo "Loi khi ve: $f"
        rm -f "$out"
    fi
done