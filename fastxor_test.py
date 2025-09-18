#!/usr/bin/env python3
"""
Usage example and performance test for the fastxor C extension module.

First, build and install the module:
    python setup.py build_ext --inplace

Then run this test:
    python fastxor_usage.py
"""

import time
import os

def test_fastxor_performance():
    """Test the fastxor module performance against Python implementations"""
    
    try:
        import fastxor
        print("✓ fastxor module imported successfully")
        print("Module info:", fastxor.get_info())
        print()
    except ImportError:
        print("❌ fastxor module not found!")
        print("Build it first with: python setup.py build_ext --inplace")
        return
    
    # Test configuration
    mb_size = 1024 * 1024  # 1MB
    chunk_size = 128       # 128 bytes (16 x 64-bit words)
    
    print(f"=== FastXOR Performance Test ===")
    print(f"Data size: {mb_size:,} bytes")
    print(f"Chunk size: {chunk_size} bytes")
    print(f"Chunks: {mb_size // chunk_size:,}")
    print()
    
    # Generate test data
    print("Generating test data...")
    data1 = os.urandom(mb_size)
    data2 = os.urandom(mb_size)
    
    chunks1 = [data1[i:i+chunk_size] for i in range(0, len(data1), chunk_size)]
    chunks2 = [data2[i:i+chunk_size] for i in range(0, len(data2), chunk_size)]
    print(f"Created {len(chunks1)} chunks")
    print()
    
    # Test 1: Python byte-wise XOR
    print("=== Test 1: Python Byte-wise XOR ===")
    start_time = time.time()
    
    python_results = []
    for c1, c2 in zip(chunks1, chunks2):
        result = bytes(a ^ b for a, b in zip(c1, c2))
        python_results.append(result)
    
    python_time = time.time() - start_time
    print(f"Time: {python_time:.4f} seconds")
    print(f"Throughput: {(mb_size / (1024*1024)) / python_time:.2f} MB/s")
    print()
    
    # Test 2: FastXOR C extension (strict 64-bit)
    print("=== Test 2: FastXOR xor64() ===")
    start_time = time.time()
    
    fastxor_results = []
    try:
        for c1, c2 in zip(chunks1, chunks2):
            result = fastxor.xor64(c1, c2)
            fastxor_results.append(result)
        
        fastxor_time = time.time() - start_time
        print(f"Time: {fastxor_time:.4f} seconds")
        print(f"Throughput: {(mb_size / (1024*1024)) / fastxor_time:.2f} MB/s")
        
        # Verify results match
        if python_results == fastxor_results:
            print("✓ Results verified - identical to Python implementation")
            speedup = python_time / fastxor_time
            print(f"🚀 Speedup: {speedup:.2f}x faster than Python")
        else:
            print("❌ Results don't match Python implementation!")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        fastxor_time = float('inf')
        fastxor_results = []
    
    print()
    
    # Test 3: FastXOR flexible (handles any size)
    print("=== Test 3: FastXOR xor() (flexible) ===")
    start_time = time.time()
    
    flexible_results = []
    try:
        for c1, c2 in zip(chunks1, chunks2):
            result = fastxor.xor(c1, c2)
            flexible_results.append(result)
        
        flexible_time = time.time() - start_time
        print(f"Time: {flexible_time:.4f} seconds")
        print(f"Throughput: {(mb_size / (1024*1024)) / flexible_time:.2f} MB/s")
        
        if python_results == flexible_results:
            print("✓ Results verified - identical to Python implementation")
            speedup = python_time / flexible_time
            print(f"🚀 Speedup: {speedup:.2f}x faster than Python")
        else:
            print("❌ Results don't match Python implementation!")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        flexible_time = float('inf')
    
    print()
    
    # Summary
    print("=== Performance Summary ===")
    print(f"Python byte-wise:    {(mb_size / (1024*1024)) / python_time:.2f} MB/s")
    if fastxor_time != float('inf'):
        print(f"FastXOR xor64():     {(mb_size / (1024*1024)) / fastxor_time:.2f} MB/s")
        print(f"FastXOR xor():       {(mb_size / (1024*1024)) / flexible_time:.2f} MB/s")
        print()
        print(f"Best improvement:    {max(python_time / fastxor_time, python_time / flexible_time):.2f}x")
    print()
    
    # Test edge cases
    print("=== Edge Case Tests ===")
    
    # Test small data (should fail for xor64)
    small_data = b"1234567"  # 7 bytes
    try:
        fastxor.xor64(small_data, small_data)
        print("❌ xor64() should have failed on 7-byte data")
    except ValueError as e:
        print(f"✓ xor64() correctly rejected 7-byte data: {e}")
    
    # Test mismatched sizes
    try:
        fastxor.xor64(b"12345678", b"1234567890")
        print("❌ xor64() should have failed on mismatched sizes")
    except ValueError as e:
        print(f"✓ xor64() correctly rejected mismatched sizes: {e}")
    
    # Test flexible function with small data
    try:
        result = fastxor.xor(small_data, small_data)
        expected = bytes(a ^ b for a, b in zip(small_data, small_data))
        if result == expected:
            print(f"✓ xor() handles small data correctly: {len(result)} bytes")
        else:
            print("❌ xor() produced incorrect result for small data")
    except Exception as e:
        print(f"❌ xor() failed on small data: {e}")

def integration_example():
    """Show how to integrate fastxor into the existing performance test"""
    
    print("\n" + "="*50)
    print("INTEGRATION EXAMPLE")
    print("="*50)
    print("""
To integrate fastxor into your existing performance test, add this function:

def xor_chunk_fastxor(chunk1, chunk2):
    '''Ultra-fast C extension XOR'''
    import fastxor
    return fastxor.xor64(chunk1, chunk2)  # or fastxor.xor() for flexibility

Then add a new test section:

# ===== TEST 3: FastXOR C Extension =====
print("=== TEST 3: FastXOR C Extension ===")
start_time = time.time()

fastxor_result_chunks = []
for chunk1, chunk2 in zip(chunks1, chunks2):
    xor_chunk = xor_chunk_fastxor(chunk1, chunk2)
    fastxor_result_chunks.append(xor_chunk)

fastxor_time = time.time() - start_time
print(f"FastXOR time: {fastxor_time:.4f} seconds")
print(f"FastXOR throughput: {(mb_size / (1024*1024)) / fastxor_time:.2f} MB/s")

Expected performance: 5-20x faster than Python byte-wise operations!
""")

if __name__ == "__main__":
    test_fastxor_performance()
    integration_example()