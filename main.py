from parse import compile
from error import CompileError, TokenError
import sys
import pysound
import numpy as np
import scipy.io.wavfile

def write(file,data):
    max_data = np.max(np.abs(data))
    scaled_data = 8000*data/max_data
    scipy.io.wavfile.write(
        filename = file,
        rate = pysound.fs,
        data = scaled_data.astype(np.int16)
    )


from instruments.guitar import Guitar

if len(sys.argv) < 2:
    print("Need at least one argument")
    sys.exit(-1)

if not ".sht" in sys.argv[1]:
    print("Expecting .sht file for first argument")
    sys.exit(-1)

shtfile = open(sys.argv[1])
sheet = shtfile.read()
shtfile.close()

# try:
#     score = compile(sheet)
# except CompileError as err:
#     print(err)
#     sys.exit(-1)
# except TokenError as err:
#     print(err)
#     sys.exit(-1)

guitar = Guitar()
track = compile(guitar,sheet)

if (len(sys.argv) >= 3) and (".wav" in sys.argv[2]):
    outpath = sys.argv[2]
else:
    outpath = "out.wav"


write(outpath,track)


sys.exit(0)