mkdir -p results
for entry in "tests"/*
do
	file=${entry##*/}
	base=${file%.*}
    ./grafo.py -f $entry > results/"$base"_results.txt
done
