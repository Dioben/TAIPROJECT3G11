import argparse
from commonutils import *
import os
import subprocess

if __name__ == "__main__":
    parser= argparse.ArgumentParser()
    parser.add_argument("--sample",help="File containing unknown sound", required=True)
    parser.add_argument("--db",help="Folder with known songs", required=True)
    parser.set_defaults(algorithm="gzip")
    parser.add_argument("--gzip",dest="algorithm",action="store_const",const="gzip")
    parser.add_argument("--lzma",dest="algorithm",action="store_const",const="lzma")
    parser.add_argument("--bzip2",dest="algorithm",action="store_const",const="bzip2")
    args = parser.parse_args()

    if args.algorithm == "gzip":
        from gzip import compress
    elif args.algorithm =="lzma":
        from lzma import compress
    elif args.algorithm =="bzip2":
        from bz2 import compress
    else:
        raise Exception("Unknown compression algorithm")

    tempfilename = "./tempfile"
    tempfilenum = 0
    while os.path.exists(f"{tempfilename}{tempfilenum}.freqs"):
        tempfilenum+=1
    tempfilename+=str(tempfilenum)+".freqs"

    cmd = ["./GetMaxFreqs", "-w", tempfilename, args.sample]
    popen = subprocess.Popen(cmd)
    popen.wait()
    with open(tempfilename, "rb") as f:
        trans = f.read()
    
    results = {}
    filelist = os.listdir(args.db)
    filelist = [ f for f in filelist if not os.path.isdir(f"{args.db}/{f}")] # remove dirs from consideration
    for f in filelist:
        keyname = f.removesuffix(".freqs")
        fullpath = f"{args.db}/{f}"
        with open(fullpath,"rb") as tmpfile:
            modelbytes = tmpfile.read()
        results[keyname] = calculateDistance(trans,modelbytes,compress)
    
    if os.path.exists(tempfilename):
        os.remove(tempfilename)

    print("Ranked choices (top 10):")
    keys = sorted(results.keys(),key=lambda x:results[x])[:10]
    for x in keys:
        print(f"{x}, distance: {results[x]}")