#pragma once

#include <random>
#include <cmath>
#include <cstdlib>

std::mt19937 createRandomGenerator();

double f(double x);

double monte_carlo(double a, double b, long long samples);
