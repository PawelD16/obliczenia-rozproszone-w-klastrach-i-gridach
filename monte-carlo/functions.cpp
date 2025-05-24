#include "functions.h"

std::mt19937 createRandomGenerator()
{
    std::random_device r;
    std::seed_seq seed{r(), r(), r(), r(), r(), r(), r(), r()};
    std::mt19937 gen{seed};

    return gen;
}

double f(double x)
{
    return sin(x);
}

double monte_carlo(double a, double b, long long samples)
{
    auto gen{createRandomGenerator()};
    std::uniform_real_distribution<> dist(a, b);

    double sum = 0.0;
    for (long long i = 0; i < samples; ++i)
    {
        double x = dist(gen);
        sum += f(x);
    }

    return (b - a) * sum / samples;
}