init_directory(Version)

# Define the Version project
init_project(Version)

# Sources static
setup_project_source(Version "Backend"
  ../touch
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

# Custom
add_custom_command(
  COMMENT			 "Generate version file"
  OUTPUT    		 ${abs_gen}/git_version.h
  COMMAND   		 ${Python3_EXECUTABLE}
                     ${abs_src}/generate_git_version.py
					 ${abs_gen}/git_version.h
  DEPENDS			 ${abs_src}/../touch
                     ${abs_src}/generate_git_version.py
  WORKING_DIRECTORY  ${project_root_dir}
  VERBATIM
)