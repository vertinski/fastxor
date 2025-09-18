# Makefile for fastxor C extension
# Alternative to setup.py for users who prefer make

# Python configuration
PYTHON := python3
PYTHON_CONFIG := python3-config
PYTHON_INCLUDE := $(shell $(PYTHON_CONFIG) --includes)
PYTHON_LDFLAGS := $(shell $(PYTHON_CONFIG) --ldflags)

# Compiler configuration
CC := gcc
CFLAGS := -O3 -march=native -std=c99 -Wall -Wextra -fPIC $(PYTHON_INCLUDE)
LDFLAGS := -shared $(PYTHON_LDFLAGS)

# File configuration
SOURCE := fastxor.c
TARGET := fastxor$(shell $(PYTHON_CONFIG) --extension-suffix)

# Default target
all: $(TARGET)

# Build the extension
$(TARGET): $(SOURCE)
	@echo "Building fastxor C extension..."
	@echo "Compiler: $(CC)"
	@echo "Python includes: $(PYTHON_INCLUDE)"
	$(CC) $(CFLAGS) $(SOURCE) -o $(TARGET) $(LDFLAGS)
	@echo "✓ Build complete: $(TARGET)"

# Test the built module
test: $(TARGET)
	@echo "Testing fastxor module..."
	$(PYTHON) -c "import fastxor; print('✓ Import successful'); print('Info:', fastxor.get_info())"
	@echo "✓ Basic test passed"

# Performance benchmark
benchmark: $(TARGET)
	@echo "Running performance benchmark..."
	@if [ -f fastxor_usage.py ]; then \
		$(PYTHON) fastxor_usage.py; \
	else \
		echo "fastxor_usage.py not found - skipping benchmark"; \
	fi

# Clean build artifacts
clean:
	@echo "Cleaning build artifacts..."
	rm -f $(TARGET)
	rm -f *.o
	rm -rf build/
	rm -rf __pycache__/
	@echo "✓ Clean complete"

# Show build info
info:
	@echo "Build Information:"
	@echo "  Python: $(PYTHON)"
	@echo "  Python config: $(PYTHON_CONFIG)"
	@echo "  Python includes: $(PYTHON_INCLUDE)"
	@echo "  Python ldflags: $(PYTHON_LDFLAGS)"
	@echo "  Compiler: $(CC)"
	@echo "  Source: $(SOURCE)"
	@echo "  Target: $(TARGET)"
	@echo "  CFLAGS: $(CFLAGS)"
	@echo "  LDFLAGS: $(LDFLAGS)"

# Install dependencies (Ubuntu/Debian)
install-deps-ubuntu:
	@echo "Installing build dependencies for Ubuntu/Debian..."
	sudo apt update
	sudo apt install -y python3-dev build-essential

# Install dependencies (CentOS/RHEL)
install-deps-centos:
	@echo "Installing build dependencies for CentOS/RHEL..."
	sudo yum install -y python3-devel gcc

# Help
help:
	@echo "FastXOR C Extension Makefile"
	@echo ""
	@echo "Targets:"
	@echo "  all           - Build the extension (default)"
	@echo "  test          - Build and test the extension"
	@echo "  benchmark     - Run performance benchmark"
	@echo "  clean         - Remove build artifacts"
	@echo "  info          - Show build configuration"
	@echo "  help          - Show this help"
	@echo ""
	@echo "Dependency installation:"
	@echo "  install-deps-ubuntu  - Install deps on Ubuntu/Debian"
	@echo "  install-deps-centos  - Install deps on CentOS/RHEL"
	@echo ""
	@echo "Usage examples:"
	@echo "  make                 # Build extension"
	@echo "  make test            # Build and test"
	@echo "  make benchmark       # Run full benchmark"
	@echo "  make clean           # Clean up"

.PHONY: all test benchmark clean info help install-deps-ubuntu install-deps-centos