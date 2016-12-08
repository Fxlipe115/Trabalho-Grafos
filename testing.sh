if [ ! -d "results" ];
    then
    mkdir results
fi
for entry in "tests"/*
do
    echo "$entry" >> results/tests.txt
    ./grafo.py -f $entry >> results/tests.txt
    echo "" >> results/tests.txt
done
