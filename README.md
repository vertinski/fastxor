# FastXOR - High-Performance XOR Operations

A Python C extension module providing ultra-fast XOR operations optimized for 64-bit architectures. Designed for high-throughput applications such as cryptography, data processing, and stream ciphers.

## Features

✨ **Performance**: 5-20x faster than pure Python implementations  
🔧 **Flexible**: Handles any data size with automatic optimization  
🛡️ **Safe**: Comprehensive error handling and validation  
🧵 **Thread-safe**: Concurrent access without synchronization  
📊 **Memory-efficient**: Minimal memory overhead  

## Installation

### Quick Start

```bash
# Clone or download the source files
# Preferred build and install
python3 setup.py build_ext --inplace

# Alternative: Using make
make all test

# Alternative: Using build script
chmod +x build_and_test.sh
./build_and_test.sh
```

### Prerequisites

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install python3-dev build-essential
```

**CentOS/RHEL:**
```bash
sudo yum install python3-devel gcc
```

**macOS:**
```bash
xcode-select --install
```

## Usage

### Basic Operations

```python
import fastxor

# For data that's a multiple of 8 bytes (maximum performance)
data1 = b'Hello World!!!!!'  # 16 bytes
data2 = b'Secret Key 12345'  # 16 bytes
result = fastxor.xor64(data1, data2)

# For any size data (flexible, still optimized)
data1 = b'Any size data!'
data2 = b'Works with any!'
result = fastxor.xor(data1, data2)

# Get implementation info
info = fastxor.get_info()
print(f"Word size: {info['word_size']} bits")
print(f"Alignment: {info['alignment']} bytes")
```

### Performance Example

```python
import fastxor
import time
import os

# Generate test data
mb_size = 1024 * 1024  # 1MB
data1 = os.urandom(mb_size)
data2 = os.urandom(mb_size)

# Time the operation
start_time = time.time()
result = fastxor.xor(data1, data2)
elapsed = time.time() - start_time

throughput = (mb_size / (1024 * 1024)) / elapsed
print(f"Throughput: {throughput:.2f} MB/s")
```

### Integration with Existing Code

Replace your existing XOR functions:

```python
# Before: Slow Python implementation
def old_xor(chunk1, chunk2):
    return bytes(a ^ b for a, b in zip(chunk1, chunk2))

# After: Fast C implementation
def fast_xor(chunk1, chunk2):
    import fastxor
    return fastxor.xor(chunk1, chunk2)  # or xor64() for aligned data
```

## API Reference

### Functions

#### `fastxor.xor64(data1, data2) -> bytes`

**Maximum performance XOR for aligned data.**

- **Parameters:**
  - `data1` (bytes): First data array
  - `data2` (bytes): Second data array (same length as data1)
- **Requirements:**
  - Both inputs must be same length
  - Length must be multiple of 8 bytes
  - Minimum 8 bytes
- **Returns:** XOR result as bytes
- **Performance:** ~10-20x faster than Python

#### `fastxor.xor(data1, data2) -> bytes`

**Flexible XOR for any size data.**

- **Parameters:**
  - `data1` (bytes): First data array
  - `data2` (bytes): Second data array (same length as data1)
- **Requirements:**
  - Both inputs must be same length
- **Returns:** XOR result as bytes
- **Performance:** ~5-15x faster than Python

#### `fastxor.get_info() -> dict`

**Get implementation details.**

- **Returns:** Dictionary with implementation info
  - `word_size`: Native word size (64 bits)
  - `alignment`: Required alignment (8 bytes)
  - `version`: Module version
  - `description`: Capability description

### Constants

- `fastxor.WORD_SIZE`: Native word size (64)
- `fastxor.MIN_SIZE`: Minimum size for xor64() (8)

### Error Handling

| Exception | When Raised |
|-----------|-------------|
| `ValueError` | Mismatched input lengths, invalid sizes |
| `MemoryError` | Memory allocation failure |
| `RuntimeError` | Internal operation failure |

## Performance Benchmarks

Typical performance improvements over Python `bytes(a ^ b for a, b in zip(...))`:

| Data Size | Alignment | Speedup |
|-----------|-----------|---------|
| 1KB | 8-byte | 15-20x |
| 1MB | 8-byte | 10-15x |
| 1KB | Any | 8-12x |
| 1MB | Any | 5-10x |

*Results vary by CPU architecture and compiler optimizations.*

## Advanced Usage

### Cryptographic Applications

```python
import fastxor

def stream_cipher_encrypt(plaintext, keystream):
    """Fast stream cipher encryption using XOR."""
    if len(plaintext) != len(keystream):
        raise ValueError("Plaintext and keystream must be same length")
    
    # Use xor64 for maximum performance if data is aligned
    if len(plaintext) % 8 == 0 and len(plaintext) >= 8:
        return fastxor.xor64(plaintext, keystream)
    else:
        return fastxor.xor(plaintext, keystream)

def one_time_pad(message, key):
    """One-time pad encryption/decryption."""
    return fastxor.xor(message, key)
```

### Bulk Data Processing

```python
import fastxor

def process_chunks(data1_chunks, data2_chunks):
    """Process multiple data chunks efficiently."""
    results = []
    
    for chunk1, chunk2 in zip(data1_chunks, data2_chunks):
        # Automatically choose best function based on size
        if len(chunk1) >= 8 and len(chunk1) % 8 == 0:
            result = fastxor.xor64(chunk1, chunk2)
        else:
            result = fastxor.xor(chunk1, chunk2)
        results.append(result)
    
    return results
```

## Building from Source

### Using setup.py

```bash
python3 setup.py build_ext --inplace  # Build in current directory
python3 setup.py install              # Install system-wide
python3 setup.py bdist_wheel          # Create wheel package
```

### Using Makefile

```bash
make all        # Build extension
make test       # Build and test
make benchmark  # Run performance tests
make clean      # Clean build files
make info       # Show build configuration
```

### Compiler Flags

The module is built with aggressive optimizations:

- `-O3`: Maximum optimization
- `-march=native`: CPU-specific optimizations
- `-std=c99`: C99 standard compliance
- `-Wall -Wextra`: Enhanced warnings

## Troubleshooting

### Build Issues

**"Python.h not found"**
```bash
# Ubuntu/Debian
sudo apt install python3-dev

# CentOS/RHEL
sudo yum install python3-devel
```

**"gcc not found"**
```bash
# Ubuntu/Debian
sudo apt install build-essential

# CentOS/RHEL
sudo yum groupinstall "Development Tools"
```

### Runtime Issues

**"Module not found"**
- Ensure the .so file is in your Python path
- Try building with `--inplace` flag

**"ValueError: Input data must be at least 64 bits"**
- Use `fastxor.xor()` instead of `fastxor.xor64()` for small data
- Ensure data is at least 8 bytes for `xor64()`

### Performance Issues

**Lower than expected speedup:**
- Verify data is properly aligned (multiple of 8 bytes)
- Use larger data sizes for better amortization
- Check that compiler optimizations are enabled

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Changelog

### Version 1.0.0
- Initial release
- 64-bit optimized XOR operations
- Flexible fallback for any size data
- Comprehensive error handling
- Thread-safe implementation
