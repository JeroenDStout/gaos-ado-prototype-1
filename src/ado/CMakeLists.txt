init_directory(Ado)

# Project
init_project(Ado)

# Sources
setup_project_source(Ado "Experiment"
  hello_world.cpp
)

# Target
configure_project_executable(Ado)
configure_cxx_target(Ado)
