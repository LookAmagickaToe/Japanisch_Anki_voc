#Made form maxime christian, feel free to contact me on github when having issues

import json
import genanki
import PyPDF2 as pdf
import pdfplumber
import os
import re

def einfügen(einträge, fn):
    
    pfad = r"C:\Users\maxim\Desktop\TUM\Japanisch\\"    # CHANGE THIS DIRECTORY (DONT FORGET \\ AT THE END)
    
    my_deck = genanki.Deck(1607392320, name = fn, description = 'genereated Deck from '+fn+" file")
    for key in einträge.keys():
        my_note = genanki.Note(genanki.BASIC_AND_REVERSED_CARD_MODEL, fields = [key, einträge.get(key)])
        my_deck.add_note(my_note)
    genanki.Package(my_deck).write_to_file(pfad+fn+'.apkg')
    print("All done: ",pfad+fn+'.apkg\n')
    
def dict_erstellen():
    t = text.split("\n")
    zeichen = [65339, 65341,65288, 65289]        #weird brackets [] used in some pdfs (have different ascii code)
    
    for phrase in t:
        phrase = phrase.split(" ")
        ej = ""                     #japanese entry
        eg = ""                     #translation entry
        
        for w in range(len(phrase)):
            word = phrase[w]
            f = 2
            for c in word:
                if ord(c) > 6000 and ord(c) not in zeichen:
                    if (ord(c)<13000):
                        f = 1
                        break
                    else:
                        f = 0
                        break
            #found Japanese
            if f==1 : #and w<6
                if len(eg.strip()) > 0:
                    #create entry and restart (bcs 2 entrys in one line
                    if len(ej) > 0 and len(eg) > 0 :                        
                        einträge[eg.strip()] = ej.strip()
                    ej = ""
                    eg = ""
                if word not in ej:
                    ej +=word + " "
                    
            #found Kanji (Delete if you want to keep Kanjis)
            elif f == 0:
                continue
            
            else:
                if word.strip() != "" and word not in ej:      #in some cases there is only the japaneseword (not used here)
                    eg += word+" "
                
        if len(ej) > 0 and len(eg) > 0 :                        #create Dict.entry only if we have a translation and entry
            einträge[eg.strip()] = ej.strip()

def find_files(path, name, st, end):
   return [f for f in os.listdir(path) if f.startswith(name) and
           int(re.compile(r'\d{1,10}').findall(f)[0])>=st and int(re.compile(r'\d{1,10}').findall(f)[0])<=end]

path = r"C:\Users\maxim\Desktop\Codes\Anki_Automation"      #CHANGE LOC OF PDF
zeichen = ["[", "]"]
while True:
    fn_o = input("Enter File name: (q for exit)")
    
    if fn_o == "q":
        break
    
    fn = fn_o.split(" ")
    st = 0
    end = 0
    einträge = {}

    if len(fn)==2:
        if fn[1] != "":
            st, end = fn[1].split("-")
            st, end = int(st), int(end)
            
            for name in find_files(path, fn[0].split(".")[0], st, end):   #concatinating all files in range st to end+1 matching name
                with pdfplumber.open(name) as temp:
                    for n in range(len(temp.pages)):    
                        text = temp.pages[n].extract_text()
                        dict_erstellen()
        else:
            print("Wrong input format e.g: voc 1-10")
            continue
    elif len(fn) == 1:
        fn = fn[0]
        try:
            with pdfplumber.open(fn) as temp:
                for n in range(len(temp.pages)):
                    text = temp.pages[n].extract_text()     #get text
                    dict_erstellen()                        #add to dictionary
        except:
            print("file not found")
            continue
    else:
        print("Wrong input format or file")
        continue
    
    print("Anzahl erstellter Einträge:", len(einträge.keys()))
    e = input("einträge anzeigen?(y)")
    if e == "y":
        for key in einträge.keys():
            print(key," ",einträge.get(key))
    e = input("Deck erstellen? (y)")
    if e == "y":
        einfügen(einträge, fn.split(".")[0])
