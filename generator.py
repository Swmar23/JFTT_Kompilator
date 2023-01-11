import sys, enum

class Errors:

  @staticmethod
  def redeclaration(name, lineno):
    print(f'Błąd (wiersz {lineno}): redeklaracja zmiennej {name}', file=sys.stderr)
    exit(1)

  @staticmethod
  def undeclared(name, lineno):
    print(f'Błąd (wiersz {lineno}): użycie niezadeklarowanej zmiennej {name}', file=sys.stderr)
    exit(2)

  @staticmethod
  def uninitiated(name, lineno):
    print(f'Błąd (wiersz {lineno}): użycie niezainicjalizowanej zmiennej {name}', file=sys.stderr)
    exit(3)

  @staticmethod
  def unknown_procedure(name, lineno):
    print(f'Błąd (wiersz {lineno}): użycie nieznanej procedury {name}', file = sys.stderr)
    exit(4)


class Variable:

  def __init__(self, name, in_main, is_initiated=False):
    self.name = name
    self.in_main = in_main
    self.is_initiated = is_initiated

  def __hash__(self):
    return hash((self.name, self.in_main))

  def __eq__(self, other):
    return (self.name, self.in_main) == (other.name, other.in_main)

  def __ne__(self, other):
        return not(self == other)


class Command(enum.Enum):
  PROGRAM_HALT = 1
  PROCEDURES_VAR = 2
  PROCEDURES = 3
  PROCEDURES_EMPTY = 4
  MAIN_VAR = 5
  MAIN = 6
  COMMANDS_COMMAND = 7
  COMMANDS = 8
  COMMAND_ASSIGN = 9
  COMMAND_IF_ELSE = 10
  COMMAND_IF = 11
  COMMAND_WHILE = 12
  COMMAND_REPEAT = 13
  COMMAND_PROC_CALL = 14
  COMMAND_READ = 15
  COMMAND_WRITE = 16
  PROC_HEAD_PROC = 17
  PROC_HEAD_CALL = 18
  DECLARATIONS_PROC_LONG = 19
  DECLARATIONS_PROC = 20
  DECLARATIONS_MAIN_LONG = 21
  DECLARATIONS_MAIN = 22
  DECLARATIONS_CALL_LONG = 23
  DECLARATIONS_CALL = 24
  EXPRESSION_VALUE = 25
  EXPRESSION_PLUS = 26
  EXPRESSION_MINUS = 27
  EXPRESSION_TIMES = 28
  EXPRESSION_DIV = 29
  EXPRESSION_MOD = 30
  CONDITION_EQ = 31
  CONDITION_NEQ = 32
  CONDITION_GT = 33
  CONDITION_LT = 34
  CONDITION_GEQ = 35
  CONDITION_LEQ = 36
  VALUE_NUM = 37
  VALUE_IDENTIFIER = 38

class Code:

  def __init__(self, name, offset=None):
    self.name = name
    self.offset = offset
  
  def __str__(self):
    if self.offset != None:
      return f'{self.name} {self.offset}'
    else:
      return self.name
    

class CodeGenerator:

  def __init__(self):
    self.variable_adresses = {}
    self.first_adress = 1

  # procedure_adresses = {}

  def generate_code(self, code, param, lineno):
    return {
      Command.PROGRAM_HALT: lambda x, l: self.__program_halt(x, l),
      Command.PROCEDURES_VAR: lambda x, l: self.__procedures_var(x, l),
      Command.PROCEDURES_EMPTY: lambda x, l: self.__procedures_empty(x, l),
      Command.MAIN_VAR: lambda x, l: self.__main_var(x, l),
      Command.MAIN: lambda x, l: self.__main(x, l),
      Command.COMMANDS_COMMAND: lambda x, l: self.__commands_command(x, l),
      Command.COMMANDS: lambda x, l: self.__commands(x, l),
      Command.COMMAND_ASSIGN: lambda x, l: self.__command_assign(x, l),
      Command.COMMAND_IF_ELSE: lambda x, l: self.__command_if_else(x, l),
      Command.COMMAND_IF: lambda x, l: self.__command_if(x, l),
      Command.COMMAND_WHILE: lambda x, l: self.__command_while(x, l),
      Command.COMMAND_REPEAT: lambda x, l: self.__command_repeat(x, l),
      Command.COMMAND_PROC_CALL: lambda x, l: self.__command_proc_call(x, l),
      Command.COMMAND_READ: lambda x, l: self.__command_read(x, l),
      Command.COMMAND_WRITE: lambda x, l: self.__command_write(x, l),
      Command.PROC_HEAD_PROC: lambda x, l: self.__proc_head_proc(x, l),
      Command.PROC_HEAD_CALL: lambda x, l: self.__proc_head_call(x, l),
      Command.DECLARATIONS_PROC_LONG: lambda x, l: self.__declarations_proc_long(x, l),
      Command.DECLARATIONS_PROC: lambda x, l: self.__declarations_proc(x, l),
      Command.DECLARATIONS_MAIN_LONG: lambda x, l: self.__declarations_main_long(x, l),
      Command.DECLARATIONS_MAIN: lambda x, l: self.__declarations_main(x, l),
      Command.DECLARATIONS_CALL_LONG: lambda x, l: self.__declarations_call_long(x, l),
      Command.DECLARATIONS_CALL: lambda x, l: self.__declarations_call(x, l),
      Command.EXPRESSION_PLUS: lambda x, l: self.__expression_plus(x, l),
      Command.EXPRESSION_MINUS: lambda x, l: self.__expression_minus(x, l),
      Command.EXPRESSION_TIMES: lambda x, l: self.__expression_times(x, l),
      Command.EXPRESSION_DIV: lambda x, l: self.__expression_div(x, l),
      Command.EXPRESSION_MOD: lambda x, l: self.__expression_mod(x, l),
      Command.CONDITION_EQ: lambda x, l: self.__condition_eq(x, l),
      Command.CONDITION_NEQ: lambda x, l: self.__condition_neq(x, l),
      Command.CONDITION_GT: lambda x, l: self.__condition_gt(x, l),
      Command.CONDITION_LT: lambda x, l: self.__condition_lt(x, l),
      Command.CONDITION_GEQ: lambda x, l: self.__condition_geq(x, l),
      Command.CONDITION_LEQ: lambda x, l: self.__condition_leq(x, l),
      Command.VALUE_NUM: lambda x, l: self.__value_num(x, l),
      Command.VALUE_IDENTIFIER: lambda x, l: self.__value_identifier(x, l)
    }[code](param, lineno)

  def __command_read(self, x, l):
    variable = Variable(x, True, True)
    if variable in self.variable_adresses:
      code = Code(f'GET {self.variable_adresses[variable]}' )
    else:
      Errors.undeclared(variable.name, l)
    varToChange = [k for k, v in self.variable_adresses.items() if v == self.variable_adresses[variable]][0]
    varToChange.is_initiated = True
    codes = [code]
    return codes

  def __command_write(self, x, l):
    variable = Variable(x[1], True, True)
    if variable in self.variable_adresses:
      varToCheck = [k for k, v in self.variable_adresses.items() if v == self.variable_adresses[variable]][0]
      if varToCheck.is_initiated:
        code = Code(f'PUT {self.variable_adresses[variable]}')
      else:
        Errors.uninitiated(varToCheck.name, l)
    else:
      Errors.undeclared(variable.name, l)
    codes = [code]
    return codes

  def __value_identifier(self, x, l):
    codes = []
    value_identifier = x
    return codes, value_identifier

  def __declarations_main(self, x, l):
    variable = Variable(x, True)
    if variable in self.variable_adresses:
      Errors.redeclaration(variable.name, l)
    self.variable_adresses[variable] = self.first_adress
    self.first_adress += 1
    codes = []
    return codes

  def __main(self, x, l):
    codes = x[1]
    return codes

  def __program_halt(self, x, l):
    strings = []
    for code in x[1]:
      string = str(code)
      strings += [string]
    strings += ["HALT"]
    return strings

  def __commands_command(self, x, l):
    codes = x[0]
    codes += x[1]
    return codes

  def __commands(self, x, l):
    return x


  # def __command_write(x, l):
  #   return