import argparse
from commonutils import *
import os
import scipy.io.wavfile as wavfile
import random

if __name__ == "__main__":
    parser= argparse.ArgumentParser()
    parser.add_argument("--source",help="Folder containing original wav files", required=True)
    parser.add_argument("--dest",help="Folder to output transform", required=True)
    parser.add_argument("--min-length",help="Minimum sample length in seconds", type=float, default=5.0)
    parser.add_argument("--max-length",help="Maximum sample length in seconds", type=float, default=15.0)
    parser.add_argument("--samples-per-track",help="Samples obtained for each track" ,type=int,default=10)
    parser.add_argument("--noise",help="noise coefficient, values smaller than .01 recommended", type=float, default=0.01)
    args = parser.parse_args()

    os.makedirs(os.path.dirname(f"{args.dest}/"), exist_ok=True)
    
    for f in os.listdir(args.source):
        fullpath = f"{args.source}/{f}"
        keyname = f.removesuffix(".wav")
        fs_rate,track = wavfile.read(fullpath)
        length = int(len(track)/fs_rate)
        for iter in range(args.samples_per_track):

            startpoint = random.randint(0,length-args.max_length)
            duration = random.random()*(args.max_length-args.min_length)+args.min_length
            
            cut = sliceFileAtSeconds(fs_rate,track,startpoint,duration)
            noise = applyNoise(cut,args.noise)
            wavfile.write(f"{args.dest}/{keyname}{iter}.wav",fs_rate,noise)
