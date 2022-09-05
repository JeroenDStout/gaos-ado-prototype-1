import copy
from .ado_parsing_data import *


class SplittedData:
  def __init__(self):
    self.groups = {}

  def __repr__(self):
    return str(self.groups)


class SplittedGroup:
  def __init__(self):
    self.operators = []

  def __repr__(self):
    child_strings = (',\n').join(list(map(str, self.operators)))
    child_strings = child_strings.replace('\n', '\n  ')
    return f"{{{', '.join(list(map(str, self.operators)))}}}"
  
  
class StackData:
  def __init__(self):
    self.group = ""
    self.using = {}


def split_recursive(out_split, stack, data):
  for elem in data:
    # For a subset, we deep copy our stack and recursively
    # call this function; as an easy form of push and popping
    if type(elem) is DescSubset:
      split_recursive(out_split, copy.deepcopy(stack), elem.children)
      
    # Set a using set
    elif type(elem) is DescUsing:
      stack.using[elem.name] = elem.types
      
    # Set current group by name
    elif type(elem) is DescGroup:
      stack.group = elem.name
      
    # Add an operator to the current group
    elif type(elem) is DescOperator:
      operator_copy = copy.deepcopy(elem)
      group = out_split.groups.setdefault(stack.group, SplittedGroup())
      group.operators += [ elem ]


# Create splitted data and return it
def split(data):
  out_split = SplittedData()
  stack     = StackData()
  
  split_recursive(out_split, stack, data)

  return out_split