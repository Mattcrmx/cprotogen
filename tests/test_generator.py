import pytest  # type: ignore[import-not-found]
from cprotogen.generator import generate_prototypes


@pytest.fixture
def temp_c_file(tmp_path):
    c_file = tmp_path / "test.c"
    c_file.write_text(
        """
#include <stdio.h>

void hello_world() {
    printf("Hello, World!\\n");
}

int add_numbers(int a, int b) {
    return a + b;
}

struct Vector* vector_resize(struct Vector** vector, int new_capacity) {
    // Implementation details omitted
}
    """
    )
    return c_file


@pytest.fixture
def temp_h_file(tmp_path):
    return tmp_path / "test.h"


@pytest.fixture
def temp_empty_h_file(tmp_path):
    h_file = tmp_path / "test.h"
    h_file.touch()  # Create an empty file
    return h_file


def test_generate_prototypes_creates_header(temp_c_file, temp_h_file):
    generate_prototypes(str(temp_c_file), str(temp_h_file))
    assert temp_h_file.exists()


def test_generate_prototypes_content(temp_c_file, temp_h_file):
    generate_prototypes(str(temp_c_file), str(temp_h_file))
    content = temp_h_file.read_text()
    assert "#ifndef TEST_H" in content
    assert "#define TEST_H" in content
    assert "void hello_world(void);" in content
    assert "int add_numbers(int a, int b);" in content
    assert "struct Vector *vector_resize(struct Vector **vector, int new_capacity);" in content
    assert "#endif // TEST_H" in content


def test_generate_prototypes_without_header(temp_c_file):
    prototypes = generate_prototypes(str(temp_c_file))
    assert isinstance(prototypes, list)
    assert len(prototypes) == 3
    assert "void hello_world(void);" in prototypes[0]
    assert "int add_numbers(int a, int b);" in prototypes[1]
    assert (
        "struct Vector *vector_resize(struct Vector **vector, int new_capacity);" in prototypes[2]
    )


def test_generate_prototypes_overwrites_existing_header(temp_c_file, temp_h_file):
    # Create an initial header file
    temp_h_file.write_text(
        "#ifndef TEST_H\n#define TEST_H\n\nvoid old_function(void);\n\n#endif // TEST_H"
    )

    generate_prototypes(str(temp_c_file), str(temp_h_file), overwrite=True)
    content = temp_h_file.read_text()
    assert "void old_function(void);" not in content
    assert "void hello_world(void);" in content
    assert "int add_numbers(int a, int b);" in content
    assert "struct Vector *vector_resize(struct Vector **vector, int new_capacity);" in content


def test_generate_prototypes_preserves_order(temp_c_file, temp_h_file):
    generate_prototypes(str(temp_c_file), str(temp_h_file))
    content = temp_h_file.read_text()
    hello_world_index = content.index("void hello_world(void);")
    add_numbers_index = content.index("int add_numbers(int a, int b);")
    vector_resize_index = content.index(
        "struct Vector *vector_resize(struct Vector **vector, int new_capacity);"
    )
    assert hello_world_index < add_numbers_index < vector_resize_index


def test_generate_prototypes_handles_complex_types(temp_c_file, temp_h_file):
    temp_c_file.write_text(
        """
    struct ComplexStruct {
        int a;
        char* b;
    };

    struct ComplexStruct* create_complex_struct(int (*callback)(void*)){};
    """
    )

    generate_prototypes(str(temp_c_file), str(temp_h_file))
    content = temp_h_file.read_text()
    assert "struct ComplexStruct *create_complex_struct(int (*callback)(void *));" in content


def test_generate_prototypes_with_empty_header(temp_c_file, temp_empty_h_file):
    # Generate prototypes
    generate_prototypes(str(temp_c_file), str(temp_empty_h_file), overwrite=True)

    # Read the content of the header file
    with open(temp_empty_h_file) as f:
        content = f.read()

    # Check if the header file now contains the correct structure and prototypes
    assert "#ifndef TEST_H" in content
    assert "#define TEST_H" in content
    assert "void hello_world(void);" in content
    assert "int add_numbers(int a, int b);" in content
    assert "struct Vector *vector_resize(struct Vector **vector, int new_capacity);" in content
    assert "#endif // TEST_H" in content

    # Check if the content is properly formatted
    expected_content = """#ifndef TEST_H
#define TEST_H

void hello_world(void);
int add_numbers(int a, int b);
struct Vector *vector_resize(struct Vector **vector, int new_capacity);

#endif // TEST_H"""
    assert content.strip() == expected_content
