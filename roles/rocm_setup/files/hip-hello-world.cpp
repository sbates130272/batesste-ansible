#include <iostream>
#include <hip/hip_runtime.h>

// This is a HIP kernel that prints to standard output
__global__ void hello_world_kernel() {
    printf("Hello, World from GPU!\n");
}

int main() {
    // Launch the kernel on the device (GPU)
    // This syntax launches the kernel with a grid of 1 block and 1 thread per block
    hello_world_kernel<<<1, 1>>>();

    // Synchronize to make sure the kernel has finished executing before exiting
    hipDeviceSynchronize();

    // Print a confirmation from the host (CPU)
    std::cout << "Kernel execution finished." << std::endl;

    return 0;
}
