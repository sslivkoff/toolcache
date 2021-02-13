"""toolcache allows for customizing how decorated functions' inputs are hashed

can use custom hash functions or merely select which inputs should be used
"""
import toolcache


#
# # use custom hash function
#

import hashlib


def md5_hash(raw_bytes):
    """this function returns the md5sum of its inputs"""
    return hashlib.md5(raw_bytes).hexdigest()


# each input-output pair to this function will be cached by md5summing the input

@toolcache.cache('memory', f_hash=md5_hash)
def f(raw_bytes):
    return some_expensive_operation(raw_bytes)


#
# # custom hash functions need to have same signature as decorated function
#

def multi_input_hash(raw_bytes, arg1, arg2):
    return md5_hash(raw_bytes) + '__' + str(arg1) + '__' + str(arg2)


@toolcache.cache('memory', f_hash=multi_input_hash)
def f(raw_bytes, arg1, arg2):
    return some_expensive_operation(raw_bytes, arg1, arg2)


#
# # decide which function args to hash via hash_include_args / hash_exclude_args
#

@toolcache.cache('memory', hash_include_args=['a', 'b'])
def f(a, b, c):
    """only args a and b will be used to compute a hash of function inputs"""
    return a * b * c


@toolcache.cache('memory', hash_exclude_args=['a', 'b'])
def f(a, b, c):
    """only arg c will be used to compute a hash of function inputs"""
    return a * b * c


#
# # hash input normalization makes positional and keyword arguments equivalent
#

@toolcache.cache('memory')
def f(a, b, c):
    return a * b * c

# these calls will be treated as different to the cache
f(1, 2, 3)
f(1, 2, c=3)
f(a=1, b=2, c=3)
print(f.cache.get_cache_size())
# output: 3


@toolcache.cache('memory', normalize_hash_inputs=True)
def f_normalized(a, b, c):
    return a * b * c

# these calls will be treated identically by the cache
f_normalized(1, 2, 3)
f_normalized(1, 2, c=3)
f_normalized(a=1, b=2, c=3)
print(f_normalized.cache.get_cache_size())
# output: 1

