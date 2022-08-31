#include "git_version.h"

#include <iostream>

int main() {
    std::cout << std::endl;
    std::cout << "          * * * * * * * * * * * " << std::endl;
    std::cout << "         * * * Ado version * * * " << std::endl;
    std::cout << "          * * * * * * * * * * * " << std::endl << std::endl;

    std::cout << Ado::Version::get_git_essential_version() << std::endl << std::endl;

    std::cout << Ado::Version::get_git_history() << std::endl;
    
    std::cout << "That's it! Bye!";
    return 0;
}
