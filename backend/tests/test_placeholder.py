def add(a, b):
    """
    Adds two numbers and returns the result.
    """
    return a + b


def test_add():
    result = add(2, 3)
    assert result == 5  # Verify the function behavior
