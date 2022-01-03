import argparse
from commonutils import *
import os
import scipy.io.wavfile as wavfile

if __name__ == "__main__":
    parser= argparse.ArgumentParser()
    parser.add_argument("--sample",help="File containing unknown sound", required=True)
    parser.add_argument("--db",help="Folder with known songs", required=True)
    parser.add_argument("--window-size",help="FFT window size in seconds",type=float,default=10.0)
    parser.add_argument("--window-overlap",help="FFT window overlap with last sample in seconds",type=float,default=2.0)
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



    freq,track = wavfile.read(args.sample)
    trans = windowedFFT(freq,track,args.window_size,args.window_overlap).tobytes()
    
    results = {}

    for f in os.listdir(args.db):
        keyname = f.removesuffix(".fft")
        fullpath = f"{args.db}/{f}"
        with open(fullpath,"rb") as tmpfile:
            modelbytes = tmpfile.read()
        results[keyname] = calculateDistance(trans,modelbytes,compress)
    
    print("Ranked choices (top 10):")
    keys = sorted(results.keys(),key=lambda x:results[x])[:10]
    for x in keys:
        print(f"{x}, distance: {results[x]}")