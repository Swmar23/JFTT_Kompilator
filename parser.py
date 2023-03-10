# Marek Świergoń 261750

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
    return self.code_generator.generate_code(Command.PROGRAM_HALT, (t.procedures, t.main), t.lineno)
  
  # procedures ******************************
  @_('procedures PROCEDURE proc_head_proc IS VAR declarations_proc_local BEGIN commands END')
  def procedures(self, t):
    return self.code_generator.generate_code(Command.PROCEDURES_VAR, (t.procedures, t.proc_head_proc, t.commands), t.lineno)

  @_('procedures PROCEDURE proc_head_proc IS BEGIN commands END')
  def procedures(self, t):
    return self.code_generator.generate_code(Command.PROCEDURES, (t.procedures, t.proc_head_proc, t.commands), t.lineno)

  @_('')
  def procedures(self, t):
    return []
  
  # main *************************************
  @_('PROGRAM IS VAR declarations_main BEGIN commands END')
  def main(self, t):
    return self.code_generator.generate_code(Command.MAIN_VAR, (t.declarations_main, t.commands), t.lineno)

  @_('PROGRAM IS BEGIN commands END')
  def main(self, t):
    return self.code_generator.generate_code(Command.MAIN, (None, t.commands), t.lineno)

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
    return self.code_generator.generate_code(Command.COMMAND_IF_ELSE, (t.condition, t.commands0, t.commands1), t.lineno)

  @_('IF condition THEN commands ENDIF')
  def command(self, t):
    return self.code_generator.generate_code(Command.COMMAND_IF, (t.condition, t.commands), t.lineno)

  @_('WHILE condition DO commands ENDWHILE')
  def command(self, t):
    return self.code_generator.generate_code(Command.COMMAND_WHILE, (t.condition, t.commands), t.lineno)

  @_('REPEAT commands UNTIL condition SEMICOLON')
  def command(self, t):
    return self.code_generator.generate_code(Command.COMMAND_REPEAT, (t.condition, t.commands), t.lineno)

  @_('proc_head_call SEMICOLON')
  def command(self, t):
    return self.code_generator.generate_code(Command.COMMAND_PROC_CALL, t.proc_head_call, t.lineno)

  @_('READ IDENTIFIER SEMICOLON')
  def command(self, t):
    return self.code_generator.generate_code(Command.COMMAND_READ, t.IDENTIFIER, t.lineno)

  @_('WRITE value SEMICOLON')
  def command(self, t):
    return self.code_generator.generate_code(Command.COMMAND_WRITE, t.value, t.lineno)

  # proc_head_proc *********************************
  @_('IDENTIFIER LPAREN declarations_proc RPAREN')
  def proc_head_proc(self, t):
    return self.code_generator.generate_code(Command.PROC_HEAD_PROC, (t.IDENTIFIER, t.declarations_proc), t.lineno)

  # proc_head_call ***********************************
  @_('IDENTIFIER LPAREN declarations_call RPAREN')
  def proc_head_call(self, t):
    return self.code_generator.generate_code(Command.PROC_HEAD_CALL, (t.IDENTIFIER, t.declarations_call), t.lineno)

  # declarations_proc ********************************
  @_('declarations_proc COMMA IDENTIFIER')
  def declarations_proc(self, t):
    return self.code_generator.generate_code(Command.DECLARATIONS_PROC_LONG, (t.declarations_proc, t.IDENTIFIER), t.lineno)

  @_('IDENTIFIER')
  def declarations_proc(self, t):
    return self.code_generator.generate_code(Command.DECLARATIONS_PROC, t.IDENTIFIER, t.lineno)

  # declarations_proc_local ***************************
  @_('declarations_proc_local COMMA IDENTIFIER')
  def declarations_proc_local(self, t):
    return self.code_generator.generate_code(Command.DECLARATIONS_PROC_LOCAL_LONG, t.IDENTIFIER, t.lineno)

  @_('IDENTIFIER')
  def declarations_proc_local(self, t):
    return self.code_generator.generate_code(Command.DECLARATIONS_PROC_LOCAL, t.IDENTIFIER, t.lineno)

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
    return self.code_generator.generate_code(Command.DECLARATIONS_CALL_LONG, (t.declarations_call, t.IDENTIFIER), t.lineno)

  @_('IDENTIFIER')
  def declarations_call(self, t):
    return self.code_generator.generate_code(Command.DECLARATIONS_CALL, t.IDENTIFIER, t.lineno)

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
    return self.code_generator.generate_code(Command.EXPRESSION_TIMES, (t.value0, t.value1), t.lineno)

  @_('value DIV value')
  def expression(self, t):
    return self.code_generator.generate_code(Command.EXPRESSION_DIV, (t.value0, t.value1), t.lineno)

  @_('value MOD value')
  def expression(self, t):
    return self.code_generator.generate_code(Command.EXPRESSION_MOD, (t.value0, t.value1), t.lineno)

  # condition **********************************************
  @_('value EQ value')
  def condition(self, t):
    return self.code_generator.generate_code(Command.CONDITION_EQ, (t.value0, t.value1), t.lineno)

  @_('value NEQ value')
  def condition(self, t):
    return self.code_generator.generate_code(Command.CONDITION_NEQ, (t.value0, t.value1), t.lineno)

  @_('value GT value')
  def condition(self, t):
    return self.code_generator.generate_code(Command.CONDITION_GT, (t.value0, t.value1), t.lineno)

  @_('value LT value')
  def condition(self, t):
    return self.code_generator.generate_code(Command.CONDITION_LT, (t.value0, t.value1), t.lineno)

  @_('value GEQ value')
  def condition(self, t):
    return self.code_generator.generate_code(Command.CONDITION_GEQ, (t.value0, t.value1), t.lineno)

  @_('value LEQ value')
  def condition(self, t):
    return self.code_generator.generate_code(Command.CONDITION_LEQ, (t.value0, t.value1), t.lineno)

  # value ******************************************
  @_('NUM')
  def value(self, t):
    return self.code_generator.generate_code(Command.VALUE_NUM, t.NUM, t.lineno)

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