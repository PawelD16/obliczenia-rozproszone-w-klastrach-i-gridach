#include <iostream>
#include <cstdlib>
#include <chrono>
#include <mpi.h>

#include "functions.h"

int main(int argc, char *argv[]) {
    MPI_Init(&argc, &argv); // initialize MPI environment

    // MPI_COMM_WORLD - communicator (contains all the processes)
    int rank, size;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);  // current process ID
    MPI_Comm_size(MPI_COMM_WORLD, &size);  // total number of processes
    
    if (argc != 4) 
    {
        if (rank == 0) 
        {
            std::cerr << "Expected 3 arguments [a, b, samples], got " << argc - 1 << std::endl;
        }

        MPI_Finalize(); // close the environment
        return 1;
    }

    double a = std::atof(argv[1]);
    double b = std::atof(argv[2]);
    long long samples = std::atoll(argv[3]);

    long long sample_size = samples / size;

    double local = monteCarlo(a, b, sample_size);

    double total = 0.0;

    // perform reduction with a sum operation (MPI_SUM), 
    // the type is double
    MPI_Reduce(&local, &total, 1, MPI_DOUBLE, MPI_SUM, 0, MPI_COMM_WORLD);

    if (rank == 0) 
    {
        total /= size;  // Average result from all processes
        std::cout << "Estimated integral: " << total << std::endl;
    }

    MPI_Finalize();
    return 0;
}
