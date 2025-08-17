#
# Optimization in High-Performance Computing
# Project: AoS vs. SoA Performance Benchmark
#

import numpy as np
import timeit
import sys

# --- Array of Structures (AoS) Implementation ---
# This implementation uses a NumPy structured array to create a true AoS layout
# where each element in the array is a struct containing all particle attributes.
# This is analogous to an array of structs in C/C++.

def create_particles_aos(n_particles):
    """
    Creates and initializes a NumPy structured array representing particles in an AoS layout.
    
    Args:
        n_particles (int): The number of particles to create.
        
    Returns:
        np.ndarray: A structured array where each element is a particle.
    """
    # Define the data type for a single particle (like a C struct)
    particle_dtype = np.dtype([('x', np.float64), 
                               ('y', np.float64), 
                               ('z', np.float64), 
                               ('mass', np.float64)])
    # Create a single contiguous array of these particle structures
    particles = np.zeros(n_particles, dtype=particle_dtype)
    
    # Initialize with random data for demonstration
    particles['x'] = np.random.rand(n_particles)
    particles['y'] = np.random.rand(n_particles)
    particles['z'] = np.random.rand(n_particles)
    particles['mass'] = np.random.rand(n_particles) * 10.0 + 0.1 # Avoid zero mass
    return particles

def center_of_mass_aos(particles):
    """
    Calculates the center of mass for a particle system stored in AoS layout.
    Accessing individual fields (e.g., particles['mass']) results in strided
    memory access, which is inefficient for the cache.
    """
    total_mass = particles['mass'].sum()
    if total_mass == 0:
        return 0.0, 0.0, 0.0
        
    com_x = np.sum(particles['x'] * particles['mass']) / total_mass
    com_y = np.sum(particles['y'] * particles['mass']) / total_mass
    com_z = np.sum(particles['z'] * particles['mass']) / total_mass
    return com_x, com_y, com_z

# --- Structure of Arrays (SoA) Implementation ---
# This implementation uses a class to hold separate, parallel NumPy arrays for each
# particle attribute. This creates an SoA layout.

class ParticleSystemSoA:
    """
    A class representing a particle system in an SoA layout.
    Each attribute (x, y, z, mass) is a separate, contiguous NumPy array.
    """
    def __init__(self, n_particles):
        self.n = n_particles
        # Create separate, contiguous arrays for each attribute
        self.x = np.random.rand(n_particles)
        self.y = np.random.rand(n_particles)
        self.z = np.random.rand(n_particles)
        self.mass = np.random.rand(n_particles) * 10.0 + 0.1 # Avoid zero mass

def center_of_mass_soa(particles):
    """
    Calculates the center of mass for a particle system stored in SoA layout.
    Accessing individual fields involves linear scans of contiguous arrays,
    which is highly cache-efficient.
    """
    total_mass = particles.mass.sum()
    if total_mass == 0:
        return 0.0, 0.0, 0.0
        
    com_x = np.sum(particles.x * particles.mass) / total_mass
    com_y = np.sum(particles.y * particles.mass) / total_mass
    com_z = np.sum(particles.z * particles.mass) / total_mass
    return com_x, com_y, com_z

# --- Benchmarking ---
def run_benchmark():
    """
    Runs the performance benchmark for both AoS and SoA implementations
    across a range of particle counts and prints the results in a table.
    """
    particle_counts = [10_000, 100_000, 1_000_000, 10_000_000]
    num_repeats = 5
    num_executions = 3 # Number of times to run the kernel within one repeat

    # Print Python and NumPy version for reproducibility
    print(f"Python version: {sys.version.split()}")
    print(f"NumPy version: {np.__version__}\n")

    print(f"{'N':>12} | {'AoS Time (s)':>15} | {'SoA Time (s)':>15} | {'Speedup':>10}")
    print("-" * 60)

    for n in particle_counts:
        # Setup strings for timeit to create data outside the timed loop
        setup_aos = f"from __main__ import create_particles_aos, center_of_mass_aos; p_aos = create_particles_aos({n})"
        setup_soa = f"from __main__ import ParticleSystemSoA, center_of_mass_soa; p_soa = ParticleSystemSoA({n})"

        # Time the AoS implementation
        aos_times = timeit.repeat(
            "center_of_mass_aos(p_aos)",
            setup=setup_aos,
            repeat=num_repeats,
            number=num_executions
        )
        aos_time_min = min(aos_times) / num_executions

        # Time the SoA implementation
        soa_times = timeit.repeat(
            "center_of_mass_soa(p_soa)",
            setup=setup_soa,
            repeat=num_repeats,
            number=num_executions
        )
        soa_time_min = min(soa_times) / num_executions
        
        speedup = aos_time_min / soa_time_min if soa_time_min > 0 else float('inf')

        print(f"{n:>12,} | {aos_time_min:15.6f} | {soa_time_min:15.6f} | {speedup:9.2f}x")

if __name__ == "__main__":
    run_benchmark()