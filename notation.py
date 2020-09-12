
# https://en.wikipedia.org/wiki/Tempo
tempo_markings = {
    "adagissimo" : 20,          # very slowly
    "larghissimo" : 24,         # very, very slow (24 bpm and under)
    "grave" : 35,               # very slow (25–45 bpm)
    "largo" : 50,               # broadly (40–60 bpm)
    "lento" : 60,               # slowly (45–60 bpm)
    "larghetto" : 66,           # rather broadly (60–66 bpm)
    "adagio" : 76,              # slowly with great expression[10] (66–76 bpm)
    "adagietto" : 80,           # slower than andante (72–76 bpm) or slightly faster than adagio (70–80 bpm)
    "andante" : 90,             # at a walking pace (76–108 bpm)
    "andantino" : 95,           # slightly faster than andante (although, in some cases, it can be taken to mean slightly slower than andante) (80–108 bpm)
    "marcia moderato" : 84,     # moderately, in the manner of a march[11][12] (83–85 bpm)
    "andante moderato" : 98,    # between andante and moderato (thus the name) (92–98 bpm)
    "moderato" : 105,           # at a moderate speed (98–112 bpm)
    "allegretto" : 110,         # by the mid-19th century, moderately fast (102–110 bpm); see paragraph above for earlier usage
    "allegro moderato" : 115,   # close to, but not quite allegro (116–120 bpm)
    "allegro" : 120,            # fast, quick, and bright (120–156 bpm) (molto allegro is slightly faster than allegro, but always in its range; 124-156 bpm)
    "vivace" : 160,             # lively and fast (156–176 bpm)
    "vivacissimo" : 175,        # very fast and lively (172–176 bpm)
    "allegrissimo" : 175,       # very fast (172–176 bpm)
    "allegro vivace" : 175,     # very fast (172–176 bpm)
    "presto" : 190,             # very, very fast (168–200 bpm)
    "prestissimo" : 200,        # even faster than presto (200 bpm and over)
}

"""
fortississimo	fff	very very loud
fortissimo	    ff	very loud
forte	        f	loud
mezzo-forte	    mf	average
mezzo-piano	    mp
piano	        p	soft
pianissimo	    pp	very soft
pianississimo	ppp	very very soft
"""

_12r2 = 2**(1/12)
equal_temperament = {
    "C" : _12r2**-9,
    "C#" : _12r2**-8,
    "Db" : _12r2**-8,
    "D" : _12r2**-7,
    "D#" : _12r2**-6,
    "Eb" : _12r2**-6,
    "E" : _12r2**-5,
    "F" : _12r2**-4,
    "F#" : _12r2**-3,
    "Gb" : _12r2**-3,
    "G" : _12r2**-2,
    "G#" : _12r2**-1,
    "Ab" : _12r2**-1,
    "A" : _12r2**0,
    "A#" : _12r2**1,
    "Bb" : _12r2**1,
    "B" : _12r2**2,
}