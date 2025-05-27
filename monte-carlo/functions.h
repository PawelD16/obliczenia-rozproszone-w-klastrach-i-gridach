#pragma once

#include <random>
#include <cmath>
#include <cstdlib>

std::mt19937 randomGenerator();

double f(double x);

double monteCarlo(double a, double b, long long samples);
