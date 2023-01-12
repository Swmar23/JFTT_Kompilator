from sly import Parser

from lexer import MyLexer
from generator import CodeGenerator, Command

class MyParser(Parser):
  tokens = MyLexer.tokens
  start = 'program_all'

  def __init__(self):
    self.code_generator = CodeGenerator()
  
  precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIV', 'MOD')
  )

  # PRODUKCJE

  # program_all *****************************
  @_('procedures main')
  def program_all(self, t):
    # tu zmień na stringi
    return self.code_generator.generate_code(Command.PROGRAM_HALT, (t.procedures, t.main), t.lineno)
  
  # procedures ******************************
  @_('procedures PROCEDURE proc_head_proc IS VAR declarations_proc BEGIN commands END')
  def procedures(self, t):
    pass # 

  @_('procedures PROCEDURE proc_head_proc IS BEGIN commands END')
  def procedures(self, t):
    pass

  @_('')
  def procedures(self, t):
    pass
  
  # main *************************************
  @_('PROGRAM IS VAR declarations_main BEGIN commands END')
  def main(self, t):
    return self.code_generator.generate_code(Command.MAIN, (t.declarations_main, t.commands), t.lineno)

  @_('PROGRAM IS BEGIN commands END')
  def main(self, t):
    pass

  # commands **********************************
  @_('commands command')
  def commands(self, t):
    return self.code_generator.generate_code(Command.COMMANDS_COMMAND, (t.commands, t.command), t.lineno)

  @_('command')
  def commands(self, t):
    return self.code_generator.generate_code(Command.COMMANDS, t.command, t.lineno)

  # command ************************************
  @_('IDENTIFIER ASSIGN expression SEMICOLON')
  def command(self, t):
    return self.code_generator.generate_code(Command.COMMAND_ASSIGN, (t.IDENTIFIER, t.expression), t.lineno)
  
  @_('IF condition THEN commands ELSE commands ENDIF')
  def command(self, t):
    pass

  @_('IF condition THEN commands ENDIF')
  def command(self, t):
    pass

  @_('WHILE condition DO commands ENDWHILE')
  def command(self, t):
    pass

  @_('REPEAT commands UNTIL condition SEMICOLON')
  def command(self, t):
    pass

  @_('proc_head_call SEMICOLON')
  def command(self, t):
    pass

  @_('READ IDENTIFIER SEMICOLON')
  def command(self, t):
    return self.code_generator.generate_code(Command.COMMAND_READ, t.IDENTIFIER, t.lineno)

  @_('WRITE value SEMICOLON')
  def command(self, t):
    return self.code_generator.generate_code(Command.COMMAND_WRITE, t.value, t.lineno)

  # proc_head_proc *********************************
  @_('IDENTIFIER LPAREN declarations_proc RPAREN')
  def proc_head_proc(self, t):
    pass

  # #proc_head_main **********************************
  # @_('IDENTIFIER LPAREN declarations_main RPAREN')
  # def proc_head_main(self, t):
  #   pass

  # proc_head_call ***********************************
  @_('IDENTIFIER LPAREN declarations_call RPAREN')
  def proc_head_call(self, t):
    pass

  # declarations_proc ********************************
  @_('declarations_proc COMMA IDENTIFIER')
  def declarations_proc(self, t):
    pass

  @_('IDENTIFIER')
  def declarations_proc(self, t):
    pass

  # declarations_main *********************************
  @_('declarations_main COMMA IDENTIFIER')
  def declarations_main(self, t):
    return self.code_generator.generate_code(Command.DECLARATIONS_MAIN, t.IDENTIFIER, t.lineno)

  @_('IDENTIFIER')
  def declarations_main(self, t):
    return self.code_generator.generate_code(Command.DECLARATIONS_MAIN, t.IDENTIFIER, t.lineno)

  # declarations_call ***********************************
  @_('declarations_call COMMA IDENTIFIER')
  def declarations_call(self, t):
    pass

  @_('IDENTIFIER')
  def declarations_call(self, t):
    pass

  # expression *******************************************
  @_('value')
  def expression(self, t):
    return self.code_generator.generate_code(Command.EXPRESSION_VALUE, t.value, t.lineno)

  @_('value PLUS value')
  def expression(self, t):
    return self.code_generator.generate_code(Command.EXPRESSION_PLUS, (t.value0, t.value1), t.lineno)

  @_('value MINUS value')
  def expression(self, t):
    return self.code_generator.generate_code(Command.EXPRESSION_MINUS, (t.value0, t.value1), t.lineno)

  @_('value TIMES value')
  def expression(self, t):
    pass

  @_('value DIV value')
  def expression(self, t):
    pass

  @_('value MOD value')
  def expression(self, t):
    pass

  # condition **********************************************
  @_('value EQ value')
  def condition(self, t):
    pass

  @_('value NEQ value')
  def condition(self, t):
    pass

  @_('value GT value')
  def condition(self, t):
    pass

  @_('value LT value')
  def condition(self, t):
    pass

  @_('value GEQ value')
  def condition(self, t):
    pass

  @_('value LEQ value')
  def condition(self, t):
    pass

  # value ******************************************
  @_('NUM')
  def value(self, t):
    pass

  @_('IDENTIFIER')
  def value(self, t):
    return self.code_generator.generate_code(Command.VALUE_IDENTIFIER, t.IDENTIFIER, t.lineno)

  # *******************************
  def error(self, p):
    if p:
      print(f'Błąd składni przy tokenie {p.type}')
    else:
      print("Błąd składni przy końcu pliku (czegoś brakuje?)")
    exit(5)