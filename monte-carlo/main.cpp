#include <iostream>
#include <chrono>

#include "functions.h"

int main(int argc, char *argv[])
{
    if (argc != 4)
    {
        std::cerr << "Expected amount of arguments was 3 [a, b, samples], but actually it was " << argc << std::endl ;
        return 1;
    }

    double a = std::atof(argv[1]);
    double b = std::atof(argv[2]);
    long long samples = std::atoll(argv[3]);

    double result = monte_carlo(a, b, samples);

    std::cout << result << std::endl;

    return 0;
}
