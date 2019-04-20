module load gcc
for i in 100 200 300 400 500 600 700 800 900 1000
do
for j in 100 200 300 400 500 600 700 800 900 1000
do
python ../hlpiensemble.py -rna ../time_samples/rna_length_${i}.fasta -protein ../time_samples/protein_length_${j}.fasta -mode full -output length_rna_${i}_protein_${j} -taskname length_rna_${i}_protein_${j} --timing
cp length_rna_${i}_protein_${j}/timelog.tsv length_rna_${i}_protein_${j}.tsv
rm -r length_rna_${i}_protein_${j}
done
done

