from sheet import compile
from error import CompileError, TokenError
import sys

if len(sys.argv) < 2:
    print("Need at least one argument")
    sys.exit(-1)

if not ".sht" in sys.argv[1]:
    print("Expecting .sht file for first argument")
    sys.exit(-1)

shtfile = open(sys.argv[1])
sheet = shtfile.read()
shtfile.close()

try:
    score = compile(sheet)
except CompileError as err:
    print(err)
    sys.exit(-1)
except TokenError as err:
    print(err)
    sys.exit(-1)



if (len(sys.argv) >= 3) and (".sco" in sys.argv[2]):
    outpath = sys.argv[2]
else:
    outpath = "out.sco"

out = open(outpath,'w')
out.write(score)
out.close()

sys.exit(0)