test ! -e out && mkdir out
python main.py $1 out/mhall.sco &&
csound -odac instruments/instruments.orc out/mhall.sco