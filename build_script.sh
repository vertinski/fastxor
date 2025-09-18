#!/bin/bash

# Build and test script for fastxor C extension
# Usage: ./build_and_test.sh

set -e  # Exit on any error

echo "==============================================="
echo "FastXOR C Extension Build and Test"
echo "==============================================="
echo

# Check if we have Python development headers
echo "Checking Python development environment..."
python3 -c "import sysconfig; print('Python include dir:', sysconfig.get_path('include'))" || {
    echo "❌ Error: Python development headers not found!"
    echo "Install them with:"
    echo "  Ubuntu/Debian: sudo apt install python3-dev"
    echo "  CentOS/RHEL:   sudo yum install python3-devel"
    echo "  macOS:         xcode-select --install"
    exit 1
}

# Check for required files
echo "Checking required files..."
for file in fastxor.c setup.py; do
    if [ ! -f "$file" ]; then
        echo "❌ Error: $file not found!"
        echo "Make sure you have saved the C source and setup script."
        exit 1
    fi
    echo "✓ Found $file"
done

echo

# Clean previous builds
echo "Cleaning previous builds..."
rm -rf build/
rm -f fastxor*.so
rm -f *.o
echo "✓ Cleaned"

echo

# Build the extension
echo "Building fastxor C extension..."
echo "This may take a moment..."

python3 setup.py build_ext --inplace || {
    echo "❌ Build failed!"
    echo
    echo "Common solutions:"
    echo "1. Install Python development headers (see above)"
    echo "2. Update your compiler: sudo apt install build-essential"
    echo "3. Check that you have a C compiler installed"
    exit 1
}

echo "✓ Build successful!"
echo

# Verify the module was created
if [ -f fastxor*.so ] || [ -f fastxor.pyd ]; then
    echo "✓ Extension module created:"
    ls -la fastxor*.so fastxor*.pyd 2>/dev/null || true
else
    echo "❌ No extension module found after build"
    exit 1
fi

echo

# Test the module
echo "Testing the fastxor module..."
python3 -c "
import fastxor
print('✓ Module imports successfully')
info = fastxor.get_info()
print('Module info:', info)

# Quick functionality test
test_data = b'12345678' * 16  # 128 bytes
result1 = fastxor.xor64(test_data, test_data)
result2 = fastxor.xor(test_data, test_data)

if result1 == b'\\x00' * len(test_data) and result2 == b'\\x00' * len(test_data):
    print('✓ XOR operations work correctly')
else:
    print('❌ XOR operations failed')
    exit(1)
"

echo

# Run performance test if available
if [ -f fastxor_usage.py ]; then
    echo "Running performance benchmark..."
    echo "(This will take about 10-30 seconds)"
    echo
    python3 fastxor_usage.py
else
    echo "Performance test script not found."
    echo "Create fastxor_usage.py to run benchmarks."
fi

echo
echo "==============================================="
echo "🎉 FastXOR C Extension Ready!"
echo "==============================================="
echo
echo "You can now use it in Python:"
echo "  import fastxor"
echo "  result = fastxor.xor64(bytes1, bytes2)"
echo "  result = fastxor.xor(bytes1, bytes2)"
echo
echo "Add it to your performance test with:"
echo "  def xor_chunk_fastxor(chunk1, chunk2):"
echo "      import fastxor"
echo "      return fastxor.xor64(chunk1, chunk2)"
echo