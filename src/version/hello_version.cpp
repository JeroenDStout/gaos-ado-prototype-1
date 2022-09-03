#include "git_version.h"

#include <iostream>

int main() {
    std::cout
      << std::endl
      << "          * * * * * * * * * * * " << std::endl
      << "         * * * Ado version * * * " << std::endl
      << "          * * * * * * * * * * * " << std::endl
      << std::endl
      << Ado::Version::get_git_essential_version() << std::endl
      << Ado::Version::get_compile_stamp() << std::endl
      << std::endl
      << Ado::Version::get_git_history() << std::endl
      << std::endl
      << "That's it! Bye!"
    ;
    return 0;
}
