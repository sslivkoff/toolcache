import toolcache


def test_null_cache():

    function_call_counts = {}

    @toolcache.cache('null')
    def f(a):
        function_call_counts.setdefault(a, 0)
        function_call_counts[a] += 1
        return a

    f(0)
    assert function_call_counts[0] == 1
    f(0)
    assert function_call_counts[0] == 2
    f(0)
    assert function_call_counts[0] == 3

