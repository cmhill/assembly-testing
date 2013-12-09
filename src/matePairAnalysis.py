#!/usr/bin/python

import argparse
import hashlib
import os
import time

def createSAM(fastaFileName, reads1, reads2, baseName, samFileName):
    os.system("bowtie2-build %s %s &> /dev/null" % (fastaFileName, baseName))
    if samFileName.endswith(".sam"):
        if reads1.endswith(".fasta"):
            os.system("bowtie2 -f -x %s -1 %s -2 %s -S %s &> /dev/null" % (baseName, reads1, reads2, samFileName))
        else:
            os.system("bowtie2 -x %s -1 %s -2 %s -S %s &> /dev/null" % (baseName, reads1, reads2, samFileName))
    else:
        os.system("bowtie2 -x %s -1 %s -2 %s -S %s.sam &> /dev/null" % (baseName, reads1, reads2, samFileName))

    os.system("rm %s.*" % (baseName,))

def createBAM(samFileName, bamFileName):
    os.system("samtools view -bS %s > %s 2> /dev/null" % (samFileName, bamFileName))

def createSortedBAM(bamFileName, sortedBamFileNamePrefix):
    os.system("samtools sort %s %s &> /dev/null" % (bamFileName, sortedBamFileNamePrefix))

def createBAI(sortedBamFileName):
    os.system("samtools index %s &> /dev/null" % (sortedBamFileName))

def createRandomNamesDict():
    h = hashlib.md5()
    h.update(str(time.time()))
    baseName = h.hexdigest()

    h.update("SAM")
    samFileName = h.hexdigest() + ".sam"
    bamFileName = samFileName.replace(".sam", ".bam")
    randomNamesDict = {
        "baseName": baseName,
        "samFileName": samFileName,
        "bamFileName": bamFileName,
        "sortedBamFileNamePrefix": bamFileName.replace(".bam", ".sorted"),
        "sortedBamFileName": bamFileName.replace(".bam", ".sorted") + ".bam",
        "bamIndexFileName": bamFileName.replace(".bam", ".sorted") + ".bam.bai" 
        }

    return randomNamesDict

parser = argparse.ArgumentParser(description="Software to find misassemblies by doing mate-pair analysis")
parser.add_argument("--fasta", dest="fastaFileName", required=True, help="fasta file name holding genome reference sequences")
parser.add_argument("-1", dest="readFile1", required=True, help="first part of the mate-pair reads")
parser.add_argument("-2", dest="readFile2", required=True, help="second part of the mate-pair reads")
parser.add_argument("--gmb", dest="gmb", action="store_true", help="if present, do good minus bad analysis.")
parser.add_argument("--ce", dest="ce", action="store_true", help="if present, do ce Statistic")
parser.add_argument("--gau", dest="gau", action="store_true", help="if present, do gaussian analysis")

args = parser.parse_args()

# Create random names that we will use as file names for sam/bam/index
randomNamesDict = createRandomNamesDict()

# TODO: We can update random names dictionary with user provided values if we want

# Create necessary files
createSAM(args.fastaFileName, args.readFile1, args.readFile2, randomNamesDict["baseName"], randomNamesDict["samFileName"])
createBAM(randomNamesDict["samFileName"], randomNamesDict["bamFileName"])
createSortedBAM(randomNamesDict["bamFileName"], randomNamesDict["sortedBamFileNamePrefix"])
createBAI(randomNamesDict["sortedBamFileName"])

misassemblyRegionList = []
if args.gmb:
    import gmb
    g = gmb.GoodMinusBadScorer(args.fastaFileName, randomNamesDict["sortedBamFileName"])
    misassemblyRegionList = g.findMisassemblyRegions()

if args.gau:
    import gaussianCheck
    gaussianErrorList = gaussianCheck.gCk(randomNamesDict["samFileName"])
    misassemblyRegionList.extend(gaussianErrorList)

if args.ce:
    import ceStatitic
    ce = ceStatistic.CE()
    ce_result = ce.doCEStatistic(args.fastaFileName, args.ce)
    misassemblyRegionList.extend(ce_result)

for misassemblyRegion in misassemblyRegionList:
    print str(misassemblyRegion)