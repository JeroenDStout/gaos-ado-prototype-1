init_directory(Ado)

# Project
init_project(Ado)

# Python requirements
python_cpm_package(lark GITHUB_REPOSITORY lark-parser/lark GIT_TAG 1.1.2)

# Sources
setup_project_source(Ado "Experiment"
  hello_world.cpp
)

# Target
configure_project_executable(Ado)
configure_cxx_target(Ado)
