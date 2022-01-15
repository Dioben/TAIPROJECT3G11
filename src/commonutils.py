import numpy as np

def applyNoise(signal,deviationCoefficient=0.0005):
    signal_type = signal.dtype
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

    return signal+np.random.normal(0,dev,signal.shape) # add 0-centered noise to the original signal


def sliceFileAtSeconds(fs_rate,signal,start,duration):
    windowSpan =  int(duration*fs_rate)
    windowOffset = int(start*fs_rate)
    return signal[windowOffset:windowOffset+windowSpan]


def calculateDistance(sample1,sample2,compressFunc):
    cs1 = compressFunc(sample1)
    cs2 = compressFunc(sample2)
    jointcompress = compressFunc(sample1+sample2)
    denominator = max(len(cs1),len(cs2))
    numerator = len(jointcompress) - min(len(cs1),len(cs2))
    return numerator/denominator