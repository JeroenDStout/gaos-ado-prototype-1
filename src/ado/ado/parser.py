import lark
from lark import Lark
from lark import Transformer
from .ado_parsing_data import *

def get_version():
  return [ 
    f"Ado parser v0",
    f"Using lark v" + lark.__version__
  ]
  
ado_grammar = r"""
  ?start: (value)*
  
  ?value: subset
        | using_decl
        | group_decl
        | operator_decl
        
  subset        : "{" [ value *] "}"
  group_decl    : "group" identifier
  using_decl    : "using" identifier "=" using_var_type
  operator_decl : identifier ":=" operator_arg_list "->" operator_arg_list
  
  ?using_var_type: identifier
                | using_var_type_group
  using_var_type_group: "[" [identifier ("," identifier)*] "]"
  
  operator_arg_list: "(" [operator_arg ("," operator_arg)*] ")"
  operator_arg: [identifier identifier operator_arg_modifier*]
  ?operator_arg_modifier: "[" identifier ("," identifier)* "]"
  
  COMMENT: "//" /[^\n]*/ _NEWLINE
  _NEWLINE: "\n"
  
  ?identifier: CNAME
          
  %import common.WS
  %import common.CNAME
  %ignore WS
  %ignore COMMENT
  %ignore " "
"""


class AdoTransformer(Transformer):
  def list(self, items):
      return list(items)
  def pair(self, key_value):
      k, v = key_value
      return k, v
  def dict(self, items):
      return dict(items)
      
  def start(self, items):
    return items
    
  def subset(self, items):
    return DescSubset(items)
    
  def using_decl(self, items):
    return DescUsing(
      str(items[0]),                        # Using name
      list(map(str, items[1].children))     # List of options
    )
    
  def group_decl(self, items):
    return DescGroup(str(items[0]))
      
  def operator_decl(self, items):
    operator = DescOperator(items[0])       # Base operator
    operator.arg_in  = items[1].children    # Arguments in
    operator.arg_out = items[2].children    # Arguments out
      
    return operator
    
  def operator_arg(self, items):
    arg = DescOperatorArgument(
      items[0],                             # Type
      items[1]                              # Name
    )
  
    for elem in items[2:]:                  # Modifiers
      if elem == 'optional':
        arg.is_optional = True
      
    return arg

def parse(data):
  return Lark(ado_grammar, start='start', parser='lalr', transformer=AdoTransformer()).parse(data)