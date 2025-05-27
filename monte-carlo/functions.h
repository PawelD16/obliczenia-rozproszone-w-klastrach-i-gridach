#pragma once

#include <random>
#include <cmath>
#include <cstdlib>
#include <tuple>
#include <stdexcept>

std::mt19937 randomGenerator();

double f(double x);

double monteCarlo(double a, double b, long long samples);

std::tuple<double, double, long long> readParams(int argc, char *argv[]);
