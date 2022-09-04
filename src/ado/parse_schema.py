info_prefix = "Ado-ps:"

import sys

# We get our extra include paths as an argument
sys.path += sys.argv[1].split(';')

# Get the path data and further arguments
( path_in, path_out ) = sys.argv[2:4]
arguments = sys.argv[4:]
print(f"{info_prefix} Parsing {path_in}")

# Get the lark submodule for parsing
import lark
print(f"{info_prefix} Using lark v" + lark.__version__)

# Temp define operators
operator_submodule = [ 'operator1', 'operator2' ]

# We gaurantee these files exist
all_imp_out = [ x + '_imp.cpp' for x in operator_submodule ]
all_def_out = [ x + '_def.h'   for x in operator_submodule ]
all_hpp_out = [ x + '.hpp'     for x in operator_submodule ]

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
    
  out_imp = f"{out_dir}/{module}_imp.cpp"
  out_def = f"{out_dir}/{module}_def.h"

  with open(f"{out_imp}-tmp", 'w') as f:
    f.write( "\n\n")
    f.write( "     /***************************************************************\n")
    f.write( "      *                                                             *\n")
    f.write( "      *            This file was automatically generated            *\n")
    f.write( "      *                Please do not edit by hand                   *\n")
    f.write( "      *                                                             *\n")
    f.write( "      ***************************************************************/\n")
    f.write( "\n\n")
    f.write(f'// This is a placeholder file explicitly implementing {module}, hooray')
  if replace_file_if_different(f"{out_imp}-tmp", out_imp):
    print(f"{info_prefix} Updated {module}_imp.cpp")
    
  with open(f"{out_def}-tmp", 'w') as f:
    f.write( "\n\n")
    f.write( "     /***************************************************************\n")
    f.write( "      *                                                             *\n")
    f.write( "      *            This file was automatically generated            *\n")
    f.write( "      *                Please do not edit by hand                   *\n")
    f.write( "      *                                                             *\n")
    f.write( "      ***************************************************************/\n")
    f.write( "\n\n")
    f.write(f'// This is a placeholder file defining {module}, hooray')
  if replace_file_if_different(f"{out_def}-tmp", out_def):
    print(f"{info_prefix} Updated {module}_def.h")
    
print(f"{info_prefix} Done")
