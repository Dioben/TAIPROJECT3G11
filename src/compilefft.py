import argparse
import commonutils
import os
import scipy.io.wavfile as wavfile

if __name__ == "__main__":
    parser= argparse.ArgumentParser()
    parser.add_argument("--source",help="Folder containing original wav files", required=True)
    parser.add_argument("--dest",help="Folder to output transform", required=True)
    args = parser.parse_args()

    os.makedirs(os.path.dirname(args.dest), exist_ok=True)
    
    for f in os.listdir(args.source):
        keyname = f.removesuffix(".wav")
        fullpath = f"{args.source}/{f}"
        fs_rate,signal = wavfile.read(fullpath)
        transform = commonutils.windowedFFT(fs_rate,signal,10,2)
        with open(f"{args.dest}/{keyname}.fft","wb") as tmpfile:
            tmpfile.write(transform.tobytes())