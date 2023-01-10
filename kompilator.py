import sys
from parser import MyParser, MyLexer

if len(sys.argv) != 3:
  print('Wywołanie: python3 kompilator.py <plik_in> <plik_out>')
  exit(1)

path_in = sys.argv[1]
path_out = sys.argv[2]
lexer = MyLexer()
parser = MyParser()
with open(path_in) as file:
  text = file.read()
  codes = parser.parse(lexer.tokenize(text))
with open(path_out, "w") as file:
  if codes is not None:
    for code in codes:
      file.write(code + '\n')
print(f'Wynik kompilacji pliku {path_in} zapisany w pliku {path_out}.')