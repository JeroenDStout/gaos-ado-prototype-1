import sys
import os

output_path = sys.argv[1]

stream = os.popen('git describe --tags')
essentialVersion = stream.read().strip()

stream = os.popen('git log -15 --oneline --decorate')
detailedVersionRaw = stream.read()

detailedVersion = []
longestPrefix = 0

print()
print("  Version: " + essentialVersion)
print()

for line in [ s.strip().split(" ", 1) for s in detailedVersionRaw.splitlines() ]:
  data = {}
  data["id"]       = line[0].strip()
  data["branches"] = []
  data["versions"] = []
  data["issues"]   = ''
  data["prefix"]   = ''
  
  if line[1][0] != '(':
    data["description"] = line[1]
  else:
    info = line[1].split(')', 1)
    
    all_issues   = []
    all_versions = []
    
    branches = info[0][1:].replace('HEAD ->', '').split(",")
    for branch in [ elem.strip() for elem in branches ]:
      if branch.startswith('gaos-'):
        all_issues.append(branch.split("--", 1)[0])
      if branch.startswith('tag:'):
        all_versions.append(branch[5:])
      if branch in ['release', 'develop']:
        data["branches"].append(branch)
        
    data["versions"]    = ' '.join(all_versions).lower()
    data["issues"]      = ' '.join(all_issues).upper()
    data["description"] = info[1].strip()
    
    prefix = data["prefix"] = data["versions"].strip()
    
    longestPrefix = max(longestPrefix, len(prefix))
  
  detailedVersion.append(data)

with open(output_path, 'w') as f:
  f.write( "/***************************************************************\n")
  f.write( " *                                                             *\n")
  f.write( " *            This file was automatically generated            *\n")
  f.write( " *                Please do not edit by hand                   *\n")
  f.write( " *                                                             *\n")
  f.write( " ***************************************************************/\n")
  f.write( "\n\n") 
  f.write( "#include <array>\n")
  f.write( "\n\n")
  f.write( "namespace Ado::Version {\n")
  f.write( "\n\n")
  f.write( "    constexpr char const * get_git_essential_version() {\n")
  f.write(f"        return \"{essentialVersion}\";\n")
  f.write( "    }\n")
  f.write( "\n\n")
  f.write( "    constexpr char const * get_git_history() {\n")
  f.write(f"        return\n")
  for version in detailedVersion:
    f.write(f"          \"{version['id']} {version['prefix'].ljust(longestPrefix)} {version['description']}")
    if len(version["issues"]) > 0:
      f.write(" (" + version["issues"] + ")")
    f.write( "\\n\"\n")
  f.write( "        ;\n")
  f.write( "    }\n")
  f.write( "\n\n")
  f.write( "}\n")