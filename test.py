def method1(method=None):
    if method is None:
        print(0)
    if method is not None:
        method()
        print(123)


def test_method():
    print(1)


method1(test_method())
