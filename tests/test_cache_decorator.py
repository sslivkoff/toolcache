import pytest

import toolcache


cachetypes = ['memory', 'disk']


@pytest.mark.parametrize('cachetype', cachetypes)
def test_cachetype_memory(cachetype):

    function_call_count = {}

    @toolcache.cache(cachetype=cachetype)
    def test_function(a, b, c):
        function_call_count.setdefault(test_function, 0)
        function_call_count[test_function] += 1
        return a * b * c

    output1 = test_function(1, 2, 3)
    assert function_call_count[test_function] == 1
    output2 = test_function(1, 2, 3)
    assert function_call_count[test_function] == 1
    assert output1 == output2


@pytest.mark.parametrize('cachetype', cachetypes)
def test_cache_varkw(cachetype):

    function_call_count = {}

    @toolcache.cache(cachetype=cachetype)
    def test_function(**kwargs):
        function_call_count.setdefault(test_function, 0)
        function_call_count[test_function] += 1
        return sum(kwargs.values())

    output1 = test_function(a=1, b=2, c=3)
    assert function_call_count[test_function] == 1
    output2 = test_function(a=1, b=2, c=3)
    assert function_call_count[test_function] == 1
    assert output1 == output2
    output3 = test_function(a=1, b=2, c=4)
    assert function_call_count[test_function] == 2
    assert output3 == 7
    output4 = test_function(a=1, b=2)
    assert function_call_count[test_function] == 3
    assert output4 == 3


@pytest.mark.parametrize('cachetype', cachetypes)
def test_cache_complex_signature(cachetype):

    function_call_count = {}

    @toolcache.cache(cachetype=cachetype, normalize_hash_inputs=True)
    def f(a, b=88, *, c, d=99, **extra_kwargs):
        function_call_count.setdefault(f, 0)
        function_call_count[f] += 1
        return (a, b, c, d, extra_kwargs)

    f(0, c=2)
    assert function_call_count[f] == 1
    f(a=0, c=2)
    assert function_call_count[f] == 1


@pytest.mark.parametrize('cachetype', cachetypes)
def test_cache_unhashable_input(cachetype):

    function_call_count = {}

    @toolcache.cache(cachetype=cachetype)
    def f(a, b):
        function_call_count.setdefault(f, 0)
        function_call_count[f] += 1
        return (a, b)

    f(0, b={'a': 4})
    assert function_call_count[f] == 1
    f(0, b={'a': 4})
    assert function_call_count[f] == 1


@pytest.mark.parametrize('cachetype', cachetypes)
def test_cache_hashable_object(cachetype):

    function_call_count = {}

    @toolcache.cache(cachetype=cachetype)
    def f(a, b):
        function_call_count.setdefault(f, 0)
        function_call_count[f] += 1
        return a

    class InputObject:
        pass

    g = InputObject()
    f(0, b=g)
    assert function_call_count[f] == 1
    f(0, b=g)
    assert function_call_count[f] == 1


#
# # test particular parameters given to toolcache.cache()
#

@pytest.mark.parametrize('cachetype', cachetypes)
def test_parameter_cache_hash_include_args(cachetype):
    @toolcache.cache(cachetype=cachetype, hash_include_args=['a', 'b'])
    def test_function(a, b, c):
        return a * b * c

    cache_instance = test_function.cache
    assert cache_instance.get_cache_size() == 0
    test_function(1, 2, 3)
    assert cache_instance.get_cache_size() == 1
    test_function(1, 2, 3)
    assert cache_instance.get_cache_size() == 1
    test_function(1, 2, 4)
    assert cache_instance.get_cache_size() == 1
    test_function(1, 2, 5)
    assert cache_instance.get_cache_size() == 1
    test_function(2, 2, 4)
    assert cache_instance.get_cache_size() == 2
    test_function(2, 2, 4)
    assert cache_instance.get_cache_size() == 2
    test_function(2, 3, 4)
    assert cache_instance.get_cache_size() == 3
    test_function(2, 3, 4)
    assert cache_instance.get_cache_size() == 3


@pytest.mark.parametrize('cachetype', cachetypes)
def test_parameter_cache_hash_exclude_args(cachetype):
    @toolcache.cache(cachetype=cachetype, hash_exclude_args=['a', 'b'])
    def test_function(a, b, c):
        return a * b * c

    cache_instance = test_function.cache
    assert cache_instance.get_cache_size() == 0
    test_function(1, 2, 3)
    assert cache_instance.get_cache_size() == 1
    test_function(1, 2, 3)
    assert cache_instance.get_cache_size() == 1
    test_function(1, 2, 4)
    assert cache_instance.get_cache_size() == 2
    test_function(1, 2, 5)
    assert cache_instance.get_cache_size() == 3
    test_function(2, 2, 4)
    assert cache_instance.get_cache_size() == 3

