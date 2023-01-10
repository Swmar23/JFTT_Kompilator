from sly import Lexer

class MyLexer(Lexer):
  ignore = ' \t'
  ignore_comment = r'(\[)([^\[\]]|\n)*(\])'
  # noinspection PyUnboundLocalVariable,PyUnresolvedReferences
  tokens = {
    'IDENTIFIER', 'NUM',
    'PLUS', 'MINUS', 'TIMES', 'DIV', 'MOD',
    'ASSIGN', 'EQ', 'NEQ', 'GT', 'LT', 'GEQ', 'LEQ',
    'IF', 'THEN', 'ELSE', 'ENDIF',
    'WHILE', 'DO', 'ENDWHILE',
    'REPEAT', 'UNTIL',
    'READ', 'WRITE',
    'PROGRAM', 'PROCEDURE',
    'IS', 'VAR', 'BEGIN', 'END',
    'LPAREN', 'RPAREN', 'SEMICOLON', 'COMMA'
  }

  IDENTIFIER = r'[_a-z]+'
  NUM = r'\d+'

  PLUS = r'\+'
  MINUS = r'-'
  TIMES = r'\*'
  DIV = r'/'
  MOD = r'%'

  ASSIGN = r':='
  NEQ = r'!='
  GEQ = r'>='
  LEQ = r'<='
  EQ = r'='
  GT = r'>'
  LT = r'<'

  ENDIF = r'ENDIF'
  IF = r'IF'
  THEN = r'THEN'
  ELSE = r'ELSE'

  ENDWHILE = r'ENDWHILE'
  WHILE = r'WHILE'
  DO = r'DO'
  REPEAT = r'REPEAT'
  UNTIL = r'UNTIL'
  READ = r'READ'
  WRITE = r'WRITE'

  PROGRAM = r'PROGRAM'
  PROCEDURE = r'PROCEDURE'

  IS = r'IS'
  VAR = r'VAR'
  BEGIN = r'BEGIN'
  END = r'END'

  LPAREN = r'\('
  RPAREN = r'\)'
  SEMICOLON = r';'
  COMMA = r'\,'

  def error(self, t):
    print(f'Nieprawidłowy znak {t.value[0]}')
    self.index += 1
  
  # noinspection PyUnresolvedReferences
  @_(r'\n+')
  def ignore_newline(self, t):
    self.lineno += t.value.count('\n')

if __name__ == '__main__':
  data = """[ a ^ b mod c
? 1234567890
? 1234567890987654321
? 987654321
> 674106858
]
PROCEDURE power(a,b,c,d) IS
VAR pot,wyk,o
BEGIN
    d:=1;
    wyk:=b;
    pot:=a%c;
    WHILE wyk>0 DO
	o:=wyk%2;
	IF o=1 THEN
	    d:=d*pot;
	    d:=d%c;
	ENDIF
	wyk:=wyk/2;
	pot:=pot*pot;
	pot:=pot%c;
    ENDWHILE
END

PROGRAM IS
VAR a,b,c,d
BEGIN
   READ a;
   READ b;
   READ c;
   power(a,b,c,d);
   WRITE d;
END"""
  lexer = MyLexer()
  for tok in lexer.tokenize(data):
    print('type=%r, value=%r' % (tok.type, tok.value))

  