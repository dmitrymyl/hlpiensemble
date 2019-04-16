CONST_LENGTH=200
CONST_NUMBER=5
#varing number of sequences
for i in {1..10}
do
    python ../generate_sequence.py -type rna -number $i -length $CONST_LENGTH -prefix rna_number_$i -out rna_number_$i.fasta
    python ../generate_sequence.py -type protein -number $i -length $CONST_LENGTH -prefix protein_number_$i -out protein_number_$i.fasta
done
# varing length of sequences
for i in 100 200 300 400 500 600 700 800 900 1000
do
    python ../generate_sequence.py -type rna -number $CONST_NUMBER -length $i -prefix rna_length_$i -out rna_length_$i.fasta
    python ../generate_sequence.py -type protein -number $CONST_NUMBER -length $i -prefix protein_length_$i -out protein_length_$i.fasta
done
