import argparse
from commonutils import *
import os
import subprocess

if __name__ == "__main__":
    parser= argparse.ArgumentParser()
    parser.add_argument("--source",help="Folder containing original wav files", required=True)
    parser.add_argument("--dest",help="Folder to output transform", required=True)
    args = parser.parse_args()

    os.makedirs(os.path.dirname(f"{args.dest}/"), exist_ok=True)
    
    for f in os.listdir(args.source):
        keyname = f.removesuffix(".wav").removesuffix(".flac")
        fullpath = f"{args.source}/{f}"
        newfile = f"{args.dest}/{keyname}.freqs"
        cmd = ["./GetMaxFreqs", "-w", newfile, fullpath]
        popen = subprocess.Popen(cmd)
