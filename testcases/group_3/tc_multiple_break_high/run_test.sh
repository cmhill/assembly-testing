#!/bin/bash

#Generate assembly on short original with several errors (2000 out of 3000)
python ../../../errorgenerator/errorgen.py -a ../../../data/buchnera/3000/buchnera-udp.assembly.fasta -o multipleErrorAssembly.fasta -m oracle -e 250 -l 200

#Generate 5x read coverage over error assembly
wgsim -1 300 -2 300 -R 0.0 -X 0.0 -e 0.0 -N 100 multipleErrorAssembly.fasta multiple.1.fastq multiple.2.fastq

#Convert fastq to fasta
python ../../../errorgenerator/convertFASTQ.py multiple.1.fastq multipleReads.1.fasta

rm -f multiple.1.fastq 
rm -f multiple.2.fastq

python ../../../breakpoint-detection/generate_unaligned.py  ../../../data/buchnera/3000/buchnera-udp.assembly.fasta multipleReads.1.fasta multipleUnaligned.txt


#attempt to align 
python ../../../breakpoint-detection/breakpoint_indices.py -a ../../../data/buchnera/3000/buchnera-udp.assembly.fasta -u multipleUnaligned.txt -o errorDetected.txt --alpha 20

rm -f multipleUnaligned.txt
#rm -f multipleErrorAssembly.fasta
#rm -f multipleReads.1.fasta
rm -f *.sam


exit 0
