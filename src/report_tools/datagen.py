import argparse
import os
from shutil import rmtree
import random
import sys
import gzip
import lzma
import bz2
import csv
sys.path.append("../")
from commonutils import calculateDistance
from compile import main as compile
from makesamples import main as makesamples

def main(args):
    random.seed(9317993391)
    compressors = [("gzip",gzip.compress), ("lzma",lzma.compress), ("bzip2",bz2.compress)]
    noises = [1, 0.5, 0.25, 0.1, 0.05, 0.01, 0.001, 0.0001, 0]
    sizes = [1, 5, 10, 20, 30, "full"]
    sourceDir = args.source
    dbDir = f"{args.compile_dest}/db"
    samplesDir = f"{args.compile_dest}/samples"
    samplesdbDir = f"{args.compile_dest}/samplesdb"
    
    if not args.skip_compile:
        compile(argparse.Namespace(
                source = sourceDir,
                dest = dbDir
            ),True,"./../GetMaxFreqs")
    
    if not args.skip_samples:
        for size in sizes:
            for noise in noises:
                makesamples(argparse.Namespace(
                        source = sourceDir,
                        dest = samplesDir,
                        min_length = size,
                        max_length = size,
                        samples_per_track = args.samples_per_track if size!="full" else 1,
                        noise = noise
                    ),size=="full")
                compile(argparse.Namespace(
                        source = samplesDir,
                        dest = f"{samplesdbDir}/{size}/{noise}"
                    ),True,"./../GetMaxFreqs")
                rmtree(samplesDir) # delete samples because they use too much storage

    with open(f"{args.dest}.tsv", "w") as output:
        writer = csv.writer(output, delimiter="\t")
        writer.writerow(["sample", "compressor", "size", "noise", "correct"])
        models = dict()
        for model in os.listdir(dbDir):
            with open(f"{dbDir}/{model}","rb") as tmpfile:
                models[model.removesuffix(".freqs")] = tmpfile.read()
        for size in sizes:
            for noise in noises:
                for target in os.listdir(f"{samplesdbDir}/{size}/{noise}"):
                    targetName = target.removesuffix(".freqs").rstrip("1234567890")
                    with open(f"{samplesdbDir}/{size}/{noise}/{target}", "rb") as targetFile:
                        targetBytes = targetFile.read()
                        for compressor in compressors:
                            results = {}
                            for modelName, modelBytes in models.items():
                                results[modelName] = calculateDistance(targetBytes, modelBytes, compressor[1])
                            correct = targetName == sorted(results.keys(),key=lambda x:results[x])[0]
                            writer.writerow([targetName, compressor[0], size, noise, correct])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--source",help="Folder containing original wav files", required=True)
    parser.add_argument("--compile-dest",help="Folder to output transform", required=True)
    parser.add_argument("--samples-per-track",help="Samples obtained for each track" ,type=int,default=10)
    parser.add_argument("--dest",help="Prefix of output file", required=True)
    parser.add_argument("--dest",help="Prefix of output file", required=True)
    parser.add_argument("--skip-compile",dest="skip_compile",help="Skip the compiling phase",action="store_true")
    parser.add_argument("--skip-samples",dest="skip_samples",help="Skip the sampling phase",action="store_true")
    parser.set_defaults(skip_compile=False, skip_samples=False)
    args = parser.parse_args()
    main(args)