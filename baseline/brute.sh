while read p; do
  python connective_experiments_brute.py >> brute_output $p
done <iterations
