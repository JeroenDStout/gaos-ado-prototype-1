info_prefix = "Ado-ps:"

import sys
import time

# We get our extra include paths as an argument
sys.path += sys.argv[1].split(';')

# Get the path data and further arguments
( path_in, path_out ) = sys.argv[2:4]
arguments = sys.argv[4:]
print(f"{info_prefix} Parsing {path_in}")

# Get the processor
import ado.parser   as ado_parser
import ado.splitter as ado_splitter
print("\n".join(f"{info_prefix} Version: {x}" for x in ado_parser.get_version()))

# Read and parse the schema
with open(path_in, 'r') as f:
  start_time = time.time()
  schema = ado_parser.parse(f.read())
print(f"{info_prefix} {str(int((time.time() - start_time) * 1000))}ms parsing complete")

# Split the data into the different groups
splitted_data = ado_splitter.split(schema)
print(f"{info_prefix} {str(int((time.time() - start_time) * 1000))}ms splitting complete")

# Define the submodules for operators
operator_submodule = [ key for key, value in splitted_data.groups.items() if len(value.operators) ]

# We gaurantee these files exist
all_imp_out = [ 'op_' + x + '_imp.cpp' for x in operator_submodule ]
all_def_out = [ 'op_' + x + '_def.h'   for x in operator_submodule ]
all_hpp_out = [ 'op_' + x + '.hpp'     for x in operator_submodule ]

# Get file util
import os
import filecmp
import shutil

out_dir = os.path.dirname(path_out)

# Util function to prevent timestamps changing
# when file write resulted in an identical file
def replace_file_if_different(path_in, path_out):
  if not os.path.exists(path_out):
    shutil.move(path_in, path_out)
    return True
    
  if not filecmp.cmp(path_out + '-tmp', path_out):
    os.remove(path_out)
    shutil.move(path_in, path_out)
    return True
    
  os.remove(path_in)
  return False

# Ensure output dir exists
if not os.path.isdir(out_dir):
  os.makedirs(out_dir)
  
# Write the manifest
with open(path_out + '-tmp', 'w') as f:
  for o in all_imp_out:
    f.write('gen: ' + o + '\n')
  for o in all_def_out:
    f.write('gen: ' + o + '\n')
  for o in all_hpp_out:
    f.write('def: ' + o + '\n')
    
if replace_file_if_different(path_out + '-tmp', path_out):
  print(f"{info_prefix} Manifest updated")
    
# In manifest only mode we stop after writing it
if '--manifest_only' in arguments:
  print(f"{info_prefix} Parser is in manifest-only mode, quitting")
  exit()
  
# For each operator, write the generated files
for module in operator_submodule:
  print(f"{info_prefix} Module {module}") 
    
  out_imp = f"{out_dir}/op_{module}_imp.cpp"
  out_def = f"{out_dir}/op_{module}_def.h"

  # Write a implementation file
  with open(f"{out_imp}-tmp", 'w') as f:
    group = splitted_data.groups.get(module, None)
    if group == None:
      continue
    
    f.write( "\n\n")
    f.write( "     /***************************************************************\n")
    f.write( "      *                                                             *\n")
    f.write( "      *            This file was automatically generated            *\n")
    f.write( "      *                Please do not edit by hand                   *\n")
    f.write( "      *                                                             *\n")
    f.write( "      ***************************************************************/\n")
    f.write( "\n\n")
    f.write(f"// \n")
    f.write(f"// This file handles implementations for the operators in {module}\n")
    f.write(f"// \n")
    
    
    for elem in group.operators:
      f.write(f"//  * {str(elem)}\n")
    
    f.write(f"//\n\n")
    
    f.write(f'#include "op_{module}_def.h"\n')
    f.write(f'#include "op_{module}.hpp"\n')
    
    f.write(f"\n\n")
    
    f.write(f"void force_implementation_op_{module}() {{" + "\n")
    
    f.write(f"    using namespace ado_gen::{module};\n")
    f.write(f"    \n")
      
    for elem in group.operators:
      f.write(f"    op_{elem.name}_call_data_default {elem.name}_data;\n")
      f.write(f"    op_{elem.name}{{}}.exec({elem.name}_data);\n")
      
    f.write( "}\n")
    
    f.write( "\n\n")
    
  # Try to replace implementation file if changed
  if replace_file_if_different(f"{out_imp}-tmp", out_imp):
    print(f"{info_prefix} Updated {module}_imp.cpp")
    
  # Write a definition file
  with open(f"{out_def}-tmp", 'w') as f:
    group = splitted_data.groups.get(module, None)
    if group == None:
      # Impossible, ignore for now
      continue
    
    f.write( "#pragma once")
    f.write( "\n\n")
    f.write( "     /***************************************************************\n")
    f.write( "      *                                                             *\n")
    f.write( "      *            This file was automatically generated            *\n")
    f.write( "      *                Please do not edit by hand                   *\n")
    f.write( "      *                                                             *\n")
    f.write( "      ***************************************************************/\n")
    f.write( "\n\n")
    
    f.write( "// \n")
    f.write(f"// This file handles definitions for the operators in {module}\n")
    for elem in group.operators:
      f.write(f"//  * {str(elem)}\n")
    f.write( "// \n")
    f.write( "\n")
    
    f.write(f"namespace ado_gen::{module} {{\n\n")
    
    for elem in group.operators:
      getset_function_descs = []
      
      for arg in elem.arg_in:
        getset_function_descs.append([
          arg.arg_type, "stub_in_" + arg.arg_name,
          "inline", f"{arg.arg_type}_cref",
          f"read_{arg.arg_name}()", f"{{ return stub_in_{arg.arg_name}; }}"
        ])
      for arg in elem.arg_out:
        getset_function_descs.append([
          arg.arg_type, "stub_out_" + arg.arg_name,
          "inline", "void",
          f"write_{arg.arg_name}({arg.arg_type}_cref x)", f"{{ stub_out_{arg.arg_name} = x; }}"
        ])
        
      desc_lengths = [
        max(list(map(len, [ x[0] for x in getset_function_descs ]))),
        max(list(map(len, [ x[1] for x in getset_function_descs ]))),
        max(list(map(len, [ x[2] for x in getset_function_descs ]))),
        max(list(map(len, [ x[3] for x in getset_function_descs ]))),
        max(list(map(len, [ x[4] for x in getset_function_descs ]))),
        max(list(map(len, [ x[5] for x in getset_function_descs ])))
      ]
      
      getset_stub_var_descs = '\n'.join([
        f"{x[0].ljust(desc_lengths[0])} {(x[1]+';').ljust(desc_lengths[1])}"
          for x in getset_function_descs
      ])
      getset_call_function_descs = '\n'.join([
        f"{x[2].ljust(desc_lengths[2])} {x[3].ljust(desc_lengths[3])} {x[4].ljust(desc_lengths[4])} {x[5].ljust(desc_lengths[5])}"
          for x in getset_function_descs
      ])
    
      f.write( "    template<")
      f.write( "\n      ")
      f.write( ",\n      ".join([ f"typename {key}_t" for key in elem.using.keys()]))
      f.write( "\n    >\n")
      f.write(f"    struct op_{elem.name}_call_data_default_abstract {{" + "\n")
      f.write( "        " +
             "\n        ".join(sum([
                [  f"using {key}      = {key}_t;",
                   f"using {key}_ref  = {key} &;",
                   f"using {key}_cref = {key} const &;",
                ]
             for key in elem.using.keys()], [])) + "\n")
      f.write( "        \n")
      f.write( "        " + getset_call_function_descs.replace("\n", "\n        ") + "\n")
      f.write( "        \n")
      f.write( "        " + getset_stub_var_descs.replace("\n", "\n        ") + "\n")
      f.write( "    };\n")
      f.write(f"    using op_{elem.name}_call_data_default = op_{elem.name}_call_data_default_abstract<")
      f.write( ", ".join([ value[0] for value in elem.using.values()]) + ">;\n")
      f.write( "    \n\n")
      
      f.write(f"    struct op_{elem.name} {{" + "\n")
            
      for arg in elem.arg_in:
        f.write( "        struct {\n")
        f.write( "          struct {\n")
        f.write( "            template<typename call_data>\n")
        f.write(f"            typename call_data::{arg.arg_type}_cref operator()(call_data & data) {{ return data.read_{arg.arg_name}(); }}" + "\n")
        f.write( "          } read;\n")
        f.write(f"        }} {arg.arg_name};" + "\n")
            
      for arg in elem.arg_out:
        f.write( "        struct {\n")
        f.write( "          struct {\n")
        f.write( "            template<typename call_data>\n")
        f.write(f"            void operator()(call_data & data, typename call_data::{arg.arg_type}_cref {arg.arg_name}) {{ data.write_{arg.arg_name}({arg.arg_name}); }}" + "\n")
        f.write( "          } write;\n")
        f.write(f"        }} {arg.arg_name};" + "\n")
      
      f.write( "        \n")
      f.write( "        template<typename call_data>\n")
      f.write( "        inline void exec(call_data& data);\n")
      f.write( "    };\n\n\n")
      
    f.write( "}\n")
    
  # Try to replace definition file if changed
  if replace_file_if_different(f"{out_def}-tmp", out_def):
    print(f"{info_prefix} Updated {module}_def.h")
    
print(f"{info_prefix} Done")
