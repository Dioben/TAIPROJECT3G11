import argparse
from commonutils import *
import os
import scipy.io.wavfile as wavfile

if __name__ == "__main__":
    parser= argparse.ArgumentParser()
    parser.add_argument("--source",help="Folder containing original wav files", required=True)
    parser.add_argument("--dest",help="Folder to output transform", required=True)
    parser.add_argument("--window-size",help="FFT window size in seconds",type=float,default=10.0)
    parser.add_argument("--window-overlap",help="FFT window overlap with last sample in seconds",type=float,default=2.0)
    args = parser.parse_args()

    os.makedirs(os.path.dirname(args.dest), exist_ok=True)
    
    for f in os.listdir(args.source):
        keyname = f.removesuffix(".wav")
        fullpath = f"{args.source}/{f}"
        fs_rate,signal = wavfile.read(fullpath)
        transform = windowedFFT(fs_rate,signal,args.window_size,args.window_overlap)
        with open(f"{args.dest}/{keyname}.fft","wb") as tmpfile:
            tmpfile.write(transform.tobytes())