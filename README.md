# Japanisch_Anki_voc
Automated Creation of Anki Decks from given Voc.PDF

SETUP:
    make sure to have all libs shown below installed:
        import json
        import genanki
        import PyPDF2 as pdf
        import pdfplumber
    The Resulting Deck will be saved in a folder specified in ln 10
    The Deckname will be the name of the Inputfile

    You need to specify the location of the Pdf file/s in ln 65

INPUT:
    you can either put in the filename e.g. "voc6.pdf" or write a filename to match and afterwards the numeration. The result will be written into one package with the name of the last used file. 
    e.g. "voc 1-3" -> this will search for voc1.pdf voc2.pdf voc3.pdf
    You can also append a "-s" at the end to say that every file in range "x-y" shall we written into a own package
    e.g. "voc 1-3 -s"


ISSUES:
    issues are at the moment tableentrys that contain a japanese word on the right (the translation column)
        -> output will be a card as follwing: { "たまに" : "gelegentlich (seltener als" } where the last japanese word is missing
    たまに たまに gelegentlich (seltener als ときどき)
