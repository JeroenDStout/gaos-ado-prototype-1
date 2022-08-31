init_directory(Version)

# Define the Version project
init_project(Version)

# Sources static
setup_project_source(Version "Backend"
  touch.txt
  generate_git_version.py
)
setup_project_source(Version "Version"
  hello_version.cpp
  git_version.h GENERATED
  git_version.hpp
)

# Target
configure_project_executable(Version)
configure_cxx_target(Version)
