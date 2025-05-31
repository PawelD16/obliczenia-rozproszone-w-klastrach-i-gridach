#include "functions.h"

std::mt19937 randomGenerator()
{
    std::random_device r;
    std::seed_seq seed{r(), r(), r(), r(), r(), r(), r(), r()};

    return std::mt19937{seed};
}

bool check(double x, double y, double radius)
{
    return pow(x,2) + pow(y,2) <= pow(radius,2);
}

int f(double side, double x, double y)
{
    return -side/2 <= x && x <= side/2 && -side/2 <= y && y <= side/2;
}

double monteCarlo(double radius, long long samples)
{
    auto gen{randomGenerator()};
    std::uniform_real_distribution<> dist(-radius, radius);

    double side = radius * sqrt(2);
    long long inside_square = 0;
    for (long long i = 0; i < samples; ++i)
    {
        double x = dist(gen);
        double y = dist(gen);
        if(check(x, y, radius))
        {
            inside_square += f(side, x, y );
        }
    }

    return (inside_square / samples) * (pow(radius,2) * M_PI);
}

std::tuple<double, long long> readArgs(int argc, char *argv[])
{
    if (argc != 3)
    {
        throw std::invalid_argument("Expected 2 arguments [radius, samples], got " + argc - 1);
    }

    double radius = std::atof(argv[1]);
    long long samples = std::atoll(argv[2]);

    if (samples <= 0)
    {
        throw std::invalid_argument("Amount of samples must be a positive number");
    }

    return {radius, samples};
}
