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

editoras = ["COEDIT", "Conselho", "Outros"]
statuses = ["OK", "Erro", "Descontinuado", "Duplicado"]
spalm = []
done = []
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

def write_csv(filename, *args):
    """TODO: Write args into file
    :returns: nothing
    
    """
    with open(filename, 'a') as csvfile:
        wrtr = csv.writer( csvfile, delimiter=';', lineterminator='\n' )
        wrtr.writerow(args)

    pass

def read_csv(filename):
    print('Reading', filename)
    with open(filename, 'r') as csvfile:
        rows = csv.reader(csvfile, delimiter=';')
        #  Skips header
        next(rows, None)
        for row in rows:
            yield row

for row in read_csv('spalm.csv'):
    title = row[0]
    number = row[1]
    spalm.append([title, number])

for row in read_csv('done.csv'):
    done.append(row)
#  assert(false)

for index, row in enumerate(read_csv('livraria.csv')):
    print('--------------------------------------------------------------')
    if len(done) > index and done[index] == row:
        print('O título abaixo já foi processado')
        print(row)
        continue
    title, sku, price, qtd, enabled, _, _ = row
    kw = find_keywords(title)
    livraria[title] = kw
    matches = []
    for spalm_title, num in spalm:
        match = match_string(spalm_title, kw)
        if match > 1:
            v = [match, spalm_title, num]
            matches.append(v) 
            #  print(v, len(matches))
            #  sleep(5)
    matches = sorted(matches, key=lambda s :s[0], reverse=True)

    try:
        print("Título Livraria: {}".format(title))
        print("Palavras Chave: {}".format(kw))
        for i, match in enumerate(matches):
            print("{:0=2d} Score:{}, Título: {}, Código: {}".format(i+1, *match))

        choice = int(input("Escolha uma das alternativas:"))
        _, spalm_title, code = matches[choice-1]
        print("Você escolheu: {0} : {1}".format(spalm_title, code))
    except Exception as e:
        raise e

    try:
        for i, editor in enumerate(editoras):
            print("{:02}: {} ".format(i+1, editor))
        choice = int(input("Escolha a editora deste título: "))
        editor = editoras[choice-1]
    except Exception as e:
        raise e

    try:
        for i, status in enumerate(statuses):
            print("{:02}: {} ".format(i+1, status))
        choice = int(input("Escolha o status deste título: "))
        editor = status[choice-1]
    except Exception as e:
        raise e

    write_csv('out.csv', code, title, spalm_title, editor, status, enabled, qtd)
    write_csv('done.csv', *row)
