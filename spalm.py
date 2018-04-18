import csv
import re
from time import sleep
from unicodedata import normalize

def remover_acentos(txt):
    return normalize('NFKD', txt).encode('ASCII', 'ignore').decode('ASCII')

def find_keywords(text):
    rv = regex.sub(' ', remover_acentos(text)).lower().split()
    rv = set(rv)
    rv = list(rv)
    return rv
    

spalm = []
livraria = {}
codigo_spalm = []
regex_out = ["a", "as", "na", "nas", "o", "os", "no", "nos", "e"]
regex_pattern = "[^A-Za-z0-9]+"
for s in regex_out:
    regex_pattern += (r"|\b{}\b".format(s))
regex = re.compile(regex_pattern, flags=re.IGNORECASE)

def match_string(s, kw1):

    kw2 = find_keywords(s)
    rv = 0
    for kw in kw1:
        rv += kw2.count(kw)
    return rv

def read_csv(filename):
    print('Reading', filename)
    with open(filename, 'r') as csvfile:
        rows = csv.reader(csvfile, delimiter=';')
        #  Skips header
        next(rows, None)
        for row in rows:
            yield row
            #  return

for row in read_csv('spalm.csv'):
    title = row[0]
    number = row[1]
    spalm.append([title, number])


for row in read_csv('livraria.csv'):
    title = row[0]
    kw = find_keywords(title)
    livraria[title] = kw
    print(title)
    print(kw)
    matches = []
    for spalm_title, num in spalm:
        match = match_string(spalm_title, kw)
        if match > 1:
            v = [match, spalm_title, num]
            matches.append(v) 
            #  print(v, len(matches))
            #  sleep(5)
    matches = sorted(matches, key=lambda s :s[0], reverse=True)
    for i, row in enumerate(matches):
        print("{:0=2d} Score:{}, Título: {}, Código: {}".format(i, *row))
    break

    #  spalm.append([title, number])
