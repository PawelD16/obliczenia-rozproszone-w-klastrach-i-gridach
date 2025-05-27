#include <iostream>
#include <cstdlib>
#include <chrono>
#include <mpi.h>

#include "functions.h"

const int PARENT_PROCESS_ID = 0;

int main(int argc, char *argv[])
{
    MPI_Init(&argc, &argv); // initialize MPI environment

    // MPI_COMM_WORLD - communicator (contains all the processes)
    int rank, size;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank); // current process ID
    MPI_Comm_size(MPI_COMM_WORLD, &size); // total number of processes

    try
    {
        auto [lower_bound, upper_bound, samples] = readArgs(argc, argv);

        long long sample_size = samples / size;
        double local = monteCarlo(lower_bound, upper_bound, sample_size);
        double total = 0.0;

        // perform reduction with a sum operation (MPI_SUM),
        // the type is double
        // 1 is the number of elements in the send buffer (1st param)
        // 0 is the rank of the root process
        MPI_Reduce(&local, &total, 1, MPI_DOUBLE, MPI_SUM, PARENT_PROCESS_ID, MPI_COMM_WORLD);

        if (rank == PARENT_PROCESS_ID)
        {
            total /= size; // Average result from all processes
            std::cout << "Estimated integral: " << total << std::endl;
        }
    }
    catch (...)
    {
        MPI_Finalize();
        return 1;
    }

    MPI_Finalize();
    return 0;
}
