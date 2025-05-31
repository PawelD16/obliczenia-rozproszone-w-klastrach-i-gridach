#pragma once

#include <random>
#include <cmath>
#include <cstdlib>
#include <tuple>
#include <stdexcept>

std::mt19937 randomGenerator();

double f(double x);

double monteCarlo(double a, long long samples);

std::tuple<double, long long> readArgs(int argc, char *argv[]);
