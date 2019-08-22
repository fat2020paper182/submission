PYTHON=python3
#PYTHON=pypy3 # preferred choice

echo "Generating custom dataset for approximate fair sampling"
$PYTHON src/generate_difficult_approx.py > datasets/approximate.dat

echo "Generating ground truth for approximate"
$PYTHON src/get_groundtruth.py approximate.dat 990

for ds in movielens.dat lastfm.dat;
do
    echo "Generating ground truth for "
    echo $ds
    $PYTHON src/get_groundtruth.py $ds
done

for r in 0.15 0.2 0.25 0.3;
do
    for i in 1 2 3 4 5 6;
    do
        $PYTHON src/experiment_minhash.py lastfm.dat $r 600 10 12043$i | tee -a results_lastfm_duplicated_headers.csv
    done
done
#
for r in 0.15 0.2 0.25;
do
    for i in 1 2 3 4 5 6;
    do
        $PYTHON src/experiment_minhash.py movielens.dat $r 400 11 $i | tee -a results_movielens_duplicated_headers.csv
    done
done

for i in `seq 40`;
do
    $PYTHON  src/experiment_minhash_approximate.py approximate.dat 0.9 1 10 1234$i 40 2 | tee -a results_difficult_duplicated_headers.csv
done

for ds in lastfm movielens difficult;
do
    $PYTHON clean_csv.py results_${ds}_duplicated_headers.csv > results_${ds}.csv
    rm results_${ds}_duplicated_headers.csv
done



