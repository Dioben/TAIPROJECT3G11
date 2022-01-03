import scipy.io.wavfile as wavfile
import scipy
import scipy.fftpack
import numpy as np

def windowedFFT(filename,windowSpanSeconds,overlapSeconds):
    #returns concatenation of n-dimensional ffts
    fs_rate, signal_original = wavfile.read(filename)
    #calculate actual window spans
    windowSpanIndexes =  int(windowSpanSeconds*fs_rate)
    overlapIndexes = int(overlapSeconds*fs_rate)
    
    #start iterating windows
    data = signal_original[:windowSpanIndexes]
    currentOffset = windowSpanIndexes
    transforms = np.empty((0,2))
    while True:
        #scipy includes n-dimensional FFT so there is no need to consider how many channels we're using
        transforms = np.append(transforms, abs(scipy.fftpack.fftn(data)) ,axis=0)
        if currentOffset>=len(signal_original):
            break
        data = np.concatenate((data[:overlapIndexes],signal_original[currentOffset:currentOffset+windowSpanIndexes-overlapIndexes]))
        currentOffset+= windowSpanIndexes-overlapIndexes
    return transforms    


def applyNoise(filename,deviationCoefficient=0.0005):
    fs_rate, signal_original = wavfile.read(filename)
    signal_type = signal_original.dtype
    #how much distortion can we apply?
    if signal_type == np.int16:
        dev = 2**15 *deviationCoefficient
    elif signal_type==np.uint16:
        dev = 2**15 *deviationCoefficient
    elif signal_type==np.uint8:
        dev = 2**7 *deviationCoefficient
    elif signal_type==np.int32:
        dev = 2**31 *deviationCoefficient
    elif signal_type==np.float32:
        dev = 1*deviationCoefficient
    elif signal_type==np.float16:
        dev = 1*deviationCoefficient
    else:
        raise Exception(f"Unknown signal type {signal_type}")

    return fs_rate,signal_original+np.random.normal(0,dev,signal_original.shape) # add 0-centered noise to the original signal
