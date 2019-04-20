module load gcc
for i in {1..10}
do
for j in {1..10}
do
python ../hlpiensemble.py -rna ../time_samples/rna_number_${i}.fasta -protein ../time_samples/protein_number_${j}.fasta -mode full -output number_rna_${i}_protein_${j} -taskname number_rna_${i}_protein_${j} --timing
cp number_rna_${i}_protein_${j}/timelog.tsv number_rna_${i}_protein_${j}.tsv
rm -r number_rna_${i}_protein_${j}
done
done

