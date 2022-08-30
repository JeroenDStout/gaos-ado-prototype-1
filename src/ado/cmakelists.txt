#Define the Ado Project
project(Ado)

set(source_experiment
  hello_world.cpp
)

source_group("Experiment" FILES ${source_experiment})

add_executable(Ado
  ${source_experiment}
)
configure_cxx_project(Ado)
