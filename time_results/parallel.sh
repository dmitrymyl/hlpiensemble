module load gcc
for i in {1..10}
do
python ../hlpiensemble.py -rna ../time_samples/rna_number_10.fasta -protein ../time_samples/protein_number_10.fasta -mode full -output parallel_${i} -cores $i -taskname parallel_${i} --timing
cp parallel_${i}/timelog.tsv parallel_cores_${i}.tsv
rm -r parallel_${i}
done

