
# Mary Had a Little Lamb
sheet = (
    "treble? 4/4 120bpm 50%"
    "| E4. D8 C4 D4 | E4 E4 E2 | D4 D4 D2 | E4 G4 G2 | E4. D8 C4 D4 | E4 E4 E4 E4 | D4 D4 E4 D4 | C |"
)

import re
from token import token
import notation


def preprocess(sheet):
    # ignore repeated measure bars
    sheet = re.sub("\|\s*\|","|",sheet)
    
    # replace all bars with space around bars to ensure whitespace
    sheet = re.sub("\|"," | ",sheet)
    
    # make all whitespace single space
    sheet = re.sub("\s+"," ",sheet)
    
    return sheet


# returns
# key signature
def clheader(header):
    print(header)


def clsheet(instrument,sheet):
    sheet = preprocess(sheet)
    
    # break out contents
    contents = sheet.split('|')
    header = contents[0]
    measures = contents[1:-1]
    
    # default 120 BPM
    tempo = 120
    
    # default 4/4 time
    beat = 4
    length = 4
    
    for token in header.split():
        print(token)
    
    for measure in measures[1:-1]:
        for token in measure.split():
            print(token)
            
compile(None,sheet)