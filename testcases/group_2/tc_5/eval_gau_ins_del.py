import os
import sys
sys.path.insert(0, '../../../src')

import oracleTester
import gaussianCheck
import genAsblyAndOrcl

orgSq = 'insDelRef.fasta'
ipSq = 'insDelTest.fasta'
outputIndex = 'modIndex'
read1 = 'r1.fq'
read2 = 'r2.fq'
outputMatchBowtie = 'output.sam'
matchGaussian = 'match.txt'
oracleLocation = 'oracle'
accuracyLocation = 'result.txt'

#generate sequence
#genAsblyAndOrcl.generateValidation(orgSq, ipSq, oracleLocation, True, True)

#generate reads
#os.system('wgsim -1 40 -2 40 -R 0.0 -X 0.0 -e 0.0 -N 20000 -d 200 -s 5 ' + orgSq + ' ' + read1 + ' ' + read2 + ' >/dev/null')

#build index
#os.system('bowtie2-build ' + ipSq + ' ' + outputIndex + ' >/dev/null')

#align reads
#os.system('bowtie2 -x ' + outputIndex + ' -1 ' + read1 + ' -2 ' + read2 + ' -S ' + outputMatchBowtie + ' >/dev/null')

#evaluate the alignment using mate pair criterion
#gaussianCheck.gCk(outputMatchBowtie)

oracleTester.testOracle(matchGaussian, oracleLocation, accuracyLocation)
