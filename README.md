# CProtoGen

A simple Python library and command-line tool for generating C function prototypes from source files.

## Installation

To install it, use pip:

```bash
pip install cprotogen
```

## Usage

### Library

You can use the exposed API:

```python
from cprotogen.generator import generate_prototypes

# Generate prototypes for multiple files
source_files = ["file1.c", "file2.c", "file3.c"]
for source in source_files:
    header = source.replace(".c", ".h")
    generate_prototypes(source, header, overwrite=True)
    print(f"Updated {header} with prototypes from {source}")
```

### As a Command-Line Tool

CProtoGen can be used directly from the command line:

```bash
# Generate prototypes and create/update a header file
cprotogen path/to/source.c --header path/to/header.h

# Generate prototypes and overwrite existing header file
cprotogen path/to/source.c --header path/to/existing_header.h --overwrite

# Show help
cprotogen -h
```

## Examples

### Generating Prototypes for a Simple File

```python
from cprotogen.generator import generate_prototypes

# Input file: hello.c
"""
#include <stdio.h>

void hello_world() {
    printf("Hello, World!\n");
}
"""

# Generate prototypes and create a header file
generate_prototypes("hello.c", "hello.h")

# Output file: hello.h
"""
#ifndef HELLO_H
#define HELLO_H

void hello_world();

#endif // HELLO_H
"""
```

### Updating Existing Header with New Function

```python
from cprotogen.generator import generate_prototypes

# Updated input file: hello.c
"""
#include <stdio.h>

void hello_world() {
    printf("Hello, World!\n");
}

int add_numbers(int a, int b) {
    return a + b;
}
"""

# Generate prototypes and update the header file
generate_prototypes("hello.c", "hello.h", overwrite=True)

# Updated output file: hello.h
"""
#ifndef HELLO_H
#define HELLO_H

void hello_world();
int add_numbers(int a, int b);

#endif // HELLO_H
"""
```

### Generating Prototypes Without Creating a Header File

```python
from cprotogen.generator import generate_prototypes

# Generate prototypes without creating a header file
prototypes = generate_prototypes("hello.c")
print(prototypes)
# Output:
# ['void hello_world();\n', 'int add_numbers(int a, int b);\n']
```
