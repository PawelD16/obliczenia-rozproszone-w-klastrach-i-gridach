#include <iostream>
#include <chrono>

#include "functions.h"

int main(int argc, char *argv[])
{
    try
    {
        auto [a, b, samples] = readParams(argc, argv);

        auto result = monteCarlo(a, b, samples);

        std::cout << result << std::endl;
    }
    catch (...)
    {
        return 1;
    }

    return 0;  
}
