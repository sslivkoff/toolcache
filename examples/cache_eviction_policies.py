"""toolcache can control when entries are evicted from the caceh

- evict entries once they become too old with `ttl`
- evict entries when the cache exceeds a certain size with `max_size`
- available size eviction policies include lru, fifo, and lfu
"""

import time

import toolcache


#
# # create a cache whose entries expire after a time-to-live age
#

@toolcache.cache('memory', ttl='10s')
def f(a, b, c):
    return a * b * c


f(1, 2, 3)
f(4, 5, 6)
print(f.cache.get_cache_size())
# output: 2

# waiting the ttl time will clear all cache entries
time.sleep(10)
print(f.cache.get_cache_size())
# output: 0


#
# # create a cache with a max_size eviction policy
#

# available eviction policies: 'lru', 'fifo', 'lfu'

@toolcache.cache('memory', max_size=3, max_size_policy='fifo')
def f(a):
    return a ** 10


f(1)
f(2)
f(3)
f(4)

print(f.cache.get_cache_size())
# output: 3


for i in [1, 2, 3, 4]:
    exists_in_cache = f.cache.exists_in_cache(args=[i])
    print(i, 'exists_in_cache:', exists_in_cache)

# output:
# 1 exists_in_cache: False
# 2 exists_in_cache: True
# 3 exists_in_cache: True
# 4 exists_in_cache: True

