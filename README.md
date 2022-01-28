# TAIPROJECT3G11

A video about this project can be found [here](https://youtu.be/2EWLtXofw-s)

## How to run
The project was implemented in python 3.9, the python3 interpreter, as well as the numpy extension are necessary to run all code.
Numpy can be installed as follows:
```bash
pip3 install numpy
```
The pandas and plotly extensions are required for plotting-related code.
These extensions can be installed as follows:
```bash
pip3 install pandas
pip3 install plotly
```
In order to run our ui code pyQT5-related packages are necessary. 
They can be installed as follows:
```bash
sudo apt-get install PyQT5
sudo apt-get install PyQT5-tools
```
Our sample compiler makes use of the scipy package, which must be installed as follows:
```bash
pip3 install scipy
```
All our programs can be executed as follows from within the */src/* folder context.
```bash
python3 <file> <options>
```

### The options for these scripts are as follows:

### compile.py
- **--source**: A folder containing WAV files
- **--dest**: A folder to output signatures to

### makesamples.py
- **--source**: A folder containing WAV files
- **--dest**: A folder to output signatures to
- **--min-length**: Lower bound on sample size in seconds, default is 5.0
- **--max-length**: Upper bound on sample size in seconds, default is 15.0
- **--samples-per-track**: Number of samples extracted per track, default is 10
- **--noise**: Noise signal multiplier, default is 0.01

### finder.py
- **--sample**: WAV or FLAC file to compare to database
- **--db**: Folder containing signatures
- **--gzip/lzma/bzip2**: Sets the program's compressor, default is gzip 

### finderUI.py
- **--db**: Folder containing signatures
- **--cache/no-cache**: Sets caching mechanism for signatures, default is disabled

*finderUI* allows for the compressor to be set during runtime via the menu bar.


## Running with options - examples
```bash
python3 compile.py --source /songs --dest /sigs
python3 makesamples.py --source /songs --dest /samples --min-length 8 --samples-per-track 15 --noise 0
python3 finderg.py --db /sigs --sample /samples/sample.wav --lzma
python3 finderUI.py  --db /sigs --cache
```
