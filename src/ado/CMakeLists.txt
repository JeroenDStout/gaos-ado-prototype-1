include(ado.cmake)

init_directory(Ado)

# Project
init_project(Ado)

# Python requirements
python_cpm_package(lark GITHUB_REPOSITORY lark-parser/lark GIT_TAG 1.1.2)

# Base sources
setup_project_source(Ado "Base"
  hello_world.cpp
  experiment_1.ado-schema
)

# Ado schema
ado_add_schema(Ado
  ado_experiment
  ${abs_src}/experiment_1.ado-schema
)
setup_project_source_specific(Ado "Experiment" GENERATED ${ado_experiment_gen})
setup_project_source_specific(Ado "Experiment" NO        ${ado_experiment_src})

# Target
configure_project_executable(Ado)
configure_cxx_target(Ado)
