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

double monteCarlo(double lower_bound, double upper_bound, long long samples)
{
    auto gen{randomGenerator()};
    std::uniform_real_distribution<> dist(lower_bound, upper_bound);

    double sum = 0.0;
    for (long long i = 0; i < samples; ++i)
    {
        sum += f(dist(gen));
    }

    return (upper_bound - lower_bound) * sum / samples;
}

std::tuple<double, double, long long> readArgs(int argc, char *argv[])
{
    if (argc != 4)
    {
        throw std::invalid_argument("Expected 3 arguments [lower bound, upper bound, samples], got " + argc - 1);
    }

    double lower_bound = std::atof(argv[1]);
    double upper_bound = std::atof(argv[2]);
    long long samples = std::atoll(argv[3]);

    if (lower_bound >= upper_bound)
    {
        throw std::invalid_argument("Lower bound of range must be smaller than upper bound");
    }

    if (samples <= 0)
    {
        throw std::invalid_argument("Amount of samples must be a positive number");
    }

    return {lower_bound, upper_bound, samples};
}
