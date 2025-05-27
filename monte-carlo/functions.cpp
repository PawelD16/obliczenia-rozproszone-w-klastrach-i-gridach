#include "functions.h"

std::mt19937 randomGenerator()
{
    std::random_device r;
    std::seed_seq seed{r(), r(), r(), r(), r(), r(), r(), r()};

    return std::mt19937{seed};
}


double f(double x)
{
    return sin(x);
}

double monteCarlo(double a, double b, long long samples)
{
    auto gen{randomGenerator()};
    std::uniform_real_distribution<> dist(a, b);

    double sum = 0.0;
    for (long long i = 0; i < samples; ++i)
    {
        double x = dist(gen);
        sum += f(x);
    }

    return (b - a) * sum / samples;
}

std::tuple<double, double, long long> readParams(int argc, char *argv[])
{
    if (argc != 4) 
    {
        throw std::invalid_argument("Expected 3 arguments [a, b, samples], got " + argc - 1 );
    }

    double a = std::atof(argv[1]);
    double b = std::atof(argv[2]);
    long long samples = std::atoll(argv[3]);

    return {a, b, samples};
}