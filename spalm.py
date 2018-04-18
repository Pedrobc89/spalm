import csv

spalm = []
livraria = []
codigo_spalm = []


def match_string(s1, s2):
    """TODO: Docstring for match_string.
    :returns: TODO

    """
    ss = s1.split()
    return 0

with open('teste.csv', 'r') as csvfile:
    creader = csv.reader(csvfile, delimiter=';')
    for name, num in creader:
        print(name)


with open('teste2.csv', 'r') as csvfile:
    creader = csv.reader(csvfile, delimiter=';')
    for name in creader:
        print(name)

