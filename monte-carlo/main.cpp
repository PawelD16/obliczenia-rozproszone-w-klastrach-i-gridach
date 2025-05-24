#include <iostream>
#include <chrono>

#include "functions.h"

int main(int argc, char *argv[])
{
    if (argc != 4)
    {
        std::cerr << "Expected amount of arguments was 3 [a, b, samples]";
        return 1;
    }

    double a = std::atof(argv[1]);
    double b = std::atof(argv[2]);
    long long samples = std::atoll(argv[3]);

    auto start = std::chrono::high_resolution_clock::now();
    double result = monte_carlo(a, b, samples);
    auto end = std::chrono::high_resolution_clock::now();

    std::chrono::duration<double> elapsed = end - start;

    std::cout << "Integral estimate: " << result << "\n";
    std::cout << "Time taken: " << elapsed.count() << " seconds\n";

    return 0;
}
