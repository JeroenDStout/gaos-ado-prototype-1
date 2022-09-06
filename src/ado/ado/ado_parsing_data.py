class DescSubset:
  def __init__(self, children):
    self.children = children

  def __repr__(self):
    child_strings = (',\n').join(list(map(str, self.children)))
    child_strings = child_strings.replace('\n', '\n  ')
    return "subset {\n  " + child_strings + "\n}"
    

class DescOperatorArgument:
  def __init__(self, arg_type, arg_name):
    self.arg_type     = arg_type
    self.arg_name     = arg_name
    self.is_optional  = False

  def __repr__(self):
    arg_mod = []
    if self.is_optional: arg_mod += [ 'optional' ]
    return f"{self.arg_type} {self.arg_name}" + (f" [{','.join(arg_mod)}]" if len(arg_mod) > 0 else "")


class DescOperator:
  def __init__(self, name):
    self.name = name
    self.arg_in = []
    self.arg_out = []
    self.using = {}

  def __str__(self):
    return (
        f"operator {self.name} "
      + f"({', '.join(map(str, self.arg_in))}) "
      + f"-> ({', '.join(map(str, self.arg_out))})"
      + f" using {self.using}"
    )
    
class DescGroup:
  def __init__(self, name):
    self.name = name

  def __repr__(self):
    return f"group {self.name}"
    

class DescUsing:
  def __init__(self, name, types):
    self.name = name
    self.types = types

  def __repr__(self):
    arg_mod = []
    return f"using {self.name} = [{','.join(self.types)}]"