#include <iostream>
#include <chrono>

#include "functions.h"

int main(int argc, char *argv[])
{
    try
    {
        auto [radius, samples] = readArgs(argc, argv);

        auto result = monteCarlo( radius,  samples);

        std::cout << result << std::endl;
    }
    catch (...)
    {
        return 1;
    }

    return 0;
}
