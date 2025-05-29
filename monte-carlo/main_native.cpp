#include <iostream>
#include <chrono>

#include "functions.h"

int main(int argc, char *argv[])
{
    try
    {
        auto [lower_bound, upper_bound, samples] = readArgs(argc, argv);

        auto result = monteCarlo(lower_bound, upper_bound, samples);

        std::cout << result << std::endl;
    }
    catch (...)
    {
        return 1;
    }

    return 0;
}
