while read p; do
  python connective_experiments_brute.py $p >> brute_output 
done <iterations
