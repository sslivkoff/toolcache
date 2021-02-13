import pytest

import toolcache


cachetypes = ['memory', 'disk']


@pytest.mark.parametrize('cachetype', cachetypes)
def test_cache_methods(cachetype):

    function_call_count = {}

    class TestClass:
        @toolcache.cache(cachetype=cachetype)
        def test_method(self, a, b, c):
            function_call_count.setdefault(self.test_method, 0)
            function_call_count[self.test_method] += 1
            return a * b * c

        @classmethod
        @toolcache.cache(cachetype=cachetype)
        def test_class_method(cls, a, b, c):
            function_call_count.setdefault(cls.test_class_method, 0)
            function_call_count[cls.test_class_method] += 1
            return a * b * c

        @staticmethod
        @toolcache.cache(cachetype=cachetype)
        def test_static_method(a, b, c):
            function_call_count.setdefault(TestClass.test_static_method, 0)
            function_call_count[TestClass.test_static_method] += 1
            return a * b * c

    _run_test_class_tests(
        TestClass=TestClass, function_call_count=function_call_count
    )


def _run_test_class_tests(TestClass, function_call_count):

    g1 = TestClass()
    g2 = TestClass()

    # instance method
    g1.test_method(1, 2, 3)
    g2.test_method(1, 2, 3)
    assert function_call_count[g1.test_method] == 1
    assert function_call_count[g2.test_method] == 1
    g1.test_method(1, 2, 3)
    assert function_call_count[g1.test_method] == 1
    assert function_call_count[g2.test_method] == 1
    g1.test_method(1, 2, 4)
    assert function_call_count[g1.test_method] == 2
    assert function_call_count[g2.test_method] == 1

    # class method
    TestClass.test_class_method(1, 2, 3)
    assert function_call_count[TestClass.test_class_method] == 1
    TestClass.test_class_method(1, 2, 3)
    assert function_call_count[TestClass.test_class_method] == 1
    TestClass.test_class_method(1, 2, 4)
    assert function_call_count[TestClass.test_class_method] == 2

    # staticmethod
    TestClass.test_static_method(1, 2, 3)
    assert function_call_count[TestClass.test_static_method] == 1
    TestClass.test_static_method(1, 2, 3)
    assert function_call_count[TestClass.test_static_method] == 1
    TestClass.test_static_method(1, 2, 4)
    assert function_call_count[TestClass.test_static_method] == 2

