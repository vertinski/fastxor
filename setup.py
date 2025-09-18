#!/usr/bin/env python3

from setuptools import setup, Extension
import sys
import os

# Read the README for the long description
def read_file(filename):
    """Read file contents for use in setup.py"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return ""

# Define the extension module with comprehensive documentation
fastxor_extension = Extension(
    'fastxor',
    sources=['fastxor.c'],
    extra_compile_args=[
        '-O3',              # Maximum optimization
        '-march=native',    # Optimize for current CPU architecture
        '-std=c99',         # Use C99 standard
        '-Wall',            # Enable all warnings
        '-Wextra',          # Extra warnings
    ],
    extra_link_args=[
        '-O3'
    ],
    define_macros=[
        ('MODULE_VERSION', '"1.0.0"'),
    ]
)

setup(
    name='fastxor',
    version='1.0.0',
    description='High-performance 64-bit XOR operations for Python bytes objects',
    long_description=read_file('README.md'),
    long_description_content_type='text/markdown',
    author='Performance Engineering Team',
    author_email='performance@example.com',
    url='https://github.com/yourorg/fastxor',
    project_urls={
        'Bug Reports': 'https://github.com/yourorg/fastxor/issues',
        'Source': 'https://github.com/yourorg/fastxor',
        'Documentation': 'https://github.com/yourorg/fastxor/blob/main/README.md',
    },
    ext_modules=[fastxor_extension],
    python_requires='>=3.6',
    keywords=['xor', 'cryptography', 'performance', 'bitwise', 'crypto', 'stream-cipher'],
    classifiers=[
        # Development Status
        'Development Status :: 4 - Beta',
        
        # Intended Audience
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Information Technology',
        
        # License
        'License :: OSI Approved :: MIT License',
        
        # Programming Languages
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: C',
        
        # Topics
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Scientific/Engineering',
        'Topic :: Security :: Cryptography',
        'Topic :: System :: Hardware',
        
        # Operating Systems
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        
        # Environment
        'Environment :: Console',
        'Natural Language :: English',
    ],
    zip_safe=False,
    
    # Package data and additional files
    package_data={
        '': ['*.md', '*.txt', '*.pyi'],
    },
    include_package_data=True,
    
    # Entry points for command-line tools (if any)
    entry_points={
        'console_scripts': [
            # 'fastxor-benchmark=fastxor.benchmark:main',  # If you add CLI tools
        ],
    },
    
    # Development dependencies
    extras_require={
        'dev': [
            'pytest>=6.0',
            'pytest-benchmark>=3.4',
            'black>=22.0',
            'flake8>=4.0',
        ],
        'test': [
            'pytest>=6.0',
            'pytest-benchmark>=3.4',
        ],
        'benchmark': [
            'matplotlib>=3.0',
            'numpy>=1.18',
        ],
    },
    
    # Test suite
    test_suite='tests',
    
    # Minimal dependencies (C extension has no Python deps)
    install_requires=[],
    
    # Platform-specific options
    options={
        'build_ext': {
            'parallel': True,  # Parallel compilation if supported
        }
    },
)

# Post-installation message
if __name__ == '__main__':
    print()
    print("=" * 60)
    print("🚀 FastXOR C Extension")
    print("=" * 60)
    print()
    print("High-performance 64-bit XOR operations now available!")
    print()
    print("Quick start:")
    print("  >>> import fastxor")
    print("  >>> result = fastxor.xor64(data1, data2)  # For aligned data")
    print("  >>> result = fastxor.xor(data1, data2)    # For any size data")
    print("  >>> info = fastxor.get_info()             # Implementation details")
    print()
    print("Performance:")
    print("  • 5-20x faster than pure Python XOR operations")
    print("  • Optimized for 64-bit architectures")
    print("  • Thread-safe concurrent operations")
    print()
    print("Documentation:")
    print("  • Full API documentation in docstrings")
    print("  • Type hints in fastxor.pyi")
    print("  • Examples in README.md")
    print()
    print("For performance benchmarks:")
    print("  python fastxor_usage.py")
    print()
    print("=" * 60)
