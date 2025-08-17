# AoS vs. SoA Performance Benchmark

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![NumPy](https://img.shields.io/badge/NumPy-1.20+-green.svg)](https://numpy.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A high-performance computing benchmark that demonstrates the performance differences between **Array of Structures (AoS)** and **Structure of Arrays (SoA)** memory layouts in scientific computing applications.

## 🚀 Overview

This project benchmarks two different memory layout strategies commonly used in high-performance computing:

- **AoS (Array of Structures)**: Each particle is stored as a contiguous struct containing all attributes
- **SoA (Structure of Arrays)**: Each particle attribute is stored in a separate, parallel array

The benchmark measures the performance impact of these memory layouts on cache efficiency and vectorization capabilities.

## 📊 Benchmark Results

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    AoS vs. SoA Performance Benchmark                       ║
║              Array of Structures vs. Structure of Arrays                   ║
╚══════════════════════════════════════════════════════════════════════════════╝

System Information:
  Python: 3.12.4
  NumPy: 2.3.2
  Platform: win32

Benchmark Configuration:
  Particle counts: 10,000, 100,000, 1,000,000, 10,000,000
  Repeats: 5
  Executions per repeat: 3

╔══════════════════╦═══════════════════╦═══════════════════╦══════════════════╗
║       N          ║    AoS Time (s)  ║    SoA Time (s)   ║     Speedup     ║
╠══════════════════╬═══════════════════╬═══════════════════╬══════════════════╣
║          10,000  ║        0.000054  ║        0.000039  ║          1.37x  ║
║         100,000  ║        0.001384  ║        0.000873  ║          1.58x  ║
║       1,000,000  ║        0.013954  ║        0.010027  ║          1.39x  ║
║      10,000,000  ║        0.141391  ║        0.094339  ║          1.50x  ║
╚══════════════════╩═══════════════════╩═══════════════════╩══════════════════╝

Summary:
  Best speedup: 1.58x
  Worst speedup: 1.37x
  Average speedup: 1.48x
```

## 🔬 Key Findings

- **SoA consistently outperforms AoS** across all particle counts
- **Average speedup: 1.48x** - SoA is nearly 50% faster
- **Best performance gain: 1.58x** at 100,000 particles
- **Performance improvement scales** with larger datasets

## 🏗️ Architecture

### Array of Structures (AoS)
```python
# Each particle is a struct with all attributes
particle_dtype = np.dtype([
    ('x', np.float64), 
    ('y', np.float64), 
    ('z', np.float64), 
    ('mass', np.float64)
])
particles = np.zeros(n_particles, dtype=particle_dtype)
```

**Pros:**
- Intuitive data organization
- Easy to work with individual particles
- Natural for object-oriented designs

**Cons:**
- Poor cache locality for vectorized operations
- Strided memory access patterns
- Inefficient for SIMD operations

### Structure of Arrays (SoA)
```python
class ParticleSystemSoA:
    def __init__(self, n_particles):
        self.x = np.random.rand(n_particles)      # Contiguous x-coordinates
        self.y = np.random.rand(n_particles)      # Contiguous y-coordinates
        self.z = np.random.rand(n_particles)      # Contiguous z-coordinates
        self.mass = np.random.rand(n_particles)   # Contiguous masses
```

**Pros:**
- Excellent cache locality for vectorized operations
- Efficient SIMD processing
- Better memory bandwidth utilization
- Predictable memory access patterns

**Cons:**
- More complex data management
- Less intuitive for object-oriented designs
- Potential memory fragmentation

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- NumPy 1.20 or higher

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/aos-vs-soa-benchmark.git
cd aos-vs-soa-benchmark
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install numpy
```

### Running the Benchmark

```bash
python benchmark.py
```

## 📈 Performance Analysis

### Why SoA is Faster

1. **Cache Efficiency**: SoA provides better spatial locality when accessing the same attribute across multiple particles
2. **Vectorization**: Modern CPUs can process multiple data elements simultaneously when data is stored contiguously
3. **Memory Bandwidth**: Sequential memory access patterns maximize memory bandwidth utilization
4. **SIMD Operations**: Single Instruction, Multiple Data operations work optimally with SoA layouts

### When to Use Each Approach

**Use AoS when:**
- Working with individual particles as objects
- Data access patterns are random and unpredictable
- Memory usage is more important than performance
- Code readability and maintainability are priorities

**Use SoA when:**
- Performing bulk operations on particle attributes
- Vectorization and SIMD optimization are critical
- Cache performance significantly impacts overall performance
- Working with large datasets where memory bandwidth is a bottleneck

## 🔧 Customization

### Adding New Particle Attributes

To add new attributes to the benchmark:

1. **For AoS**: Add new fields to the `particle_dtype`
2. **For SoA**: Add new arrays to the `ParticleSystemSoA` class
3. **Update the center of mass calculation** to include the new attributes

### Modifying Benchmark Parameters

Adjust the following parameters in `benchmark.py`:

```python
particle_counts = [10_000, 100_000, 1_000_000, 10_000_000]  # Dataset sizes
num_repeats = 5                                               # Number of benchmark runs
num_executions = 3                                            # Executions per repeat
```

## 📚 Further Reading

- [Memory Layouts for High Performance Computing](https://en.wikipedia.org/wiki/AoS_and_SoA)
- [NumPy Structured Arrays](https://numpy.org/doc/stable/user/basics.rec.html)
- [Cache Locality and Performance](https://en.wikipedia.org/wiki/Locality_of_reference)
- [SIMD Programming](https://en.wikipedia.org/wiki/SIMD)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Inspired by high-performance computing optimization techniques
- Built with [NumPy](https://numpy.org/) for efficient numerical computing
- Designed for educational and research purposes

---

**Note**: Benchmark results may vary depending on your hardware, operating system, and Python/NumPy versions. The results shown above are from a Windows 10 system with Python 3.12.4 and NumPy 2.3.2.
