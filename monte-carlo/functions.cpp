#include "functions.h"
/**
 * unified generator to randomize numbers in the same way
 */
std::mt19937 randomGenerator()
{
    std::random_device r;
    std::seed_seq seed{r(), r(), r(), r(), r(), r(), r(), r()};

    return std::mt19937{seed};
}

/**
 * first check if randomized number are inside circle. If is outside circle, is outside square too
 */
bool check_if_inside_circle(double x, double y, double radius)
{
    return pow(x,2) + pow(y,2) <= pow(radius,2);
}

/**
 * check if previously randomized numbers are also inside square
 */
int check_if_inside_square(double side, double x, double y)
{
    return -side/2 <= x && x <= side/2 && -side/2 <= y && y <= side/2 ;
}

/**
 * function which estimates the area of square which is draw inside circle
 * circle is in coordinate system. Center of the circle is in the point (0,0)
 * parameter 1: Radius of the circle i
 * parameter 2: Samples are the number of points which we need to calculate to determine the area
 * estimation is done by the monte carlo method
 */
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
        if(check_if_inside_circle(x, y, radius))
        {
            inside_square += check_if_inside_square(side, x, y );
        }
    }

    return (static_cast<double>(1.0 * inside_square / samples)) * (pow(radius,2) * M_PI);
}

/**
 * arguments are given from outside source - different script
 * funtion which is reading this arguments and split them to monte carlo parameters
 */
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
