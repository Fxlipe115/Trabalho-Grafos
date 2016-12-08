if [ ! -d "results" ];
    then
    mkdir results
fi
for entry in "tests"/*
do
	file=${entry##*/}
	base=${file%.*}
    ./grafo.py -f $entry >> results/"$base"_results.txt
    echo "" >> results/"$base"_results.txt
done
