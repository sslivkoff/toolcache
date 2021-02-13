"""toolcache allows for monitoring and reporting of cache usage statistics"""

import pprint

import toolcache


#
# # basic usage stat tracking is enabled by default
#

@toolcache.cache('memory')
def f(a):
    return 2 * a


f(1)
f(1)
f(2)
f(3)
f.cache.exists_in_cache(args=[1])
f.cache.exists_in_cache(args=[4])
f.cache.delete_entry(args=[2])
f.cache.delete_entry(args=[3])
pprint.pprint(f.cache.stats)
# output:
# {'n_checks': 6,
#  'n_deletes': 2,
#  'n_hashes': 8,
#  'n_hits': 2,
#  'n_loads': 1,
#  'n_misses': 4,
#  'n_saves': 3,
#  'n_size_evictions': 0,
#  'n_ttl_evictions': 0}


#
# # can also track creation time, access time, and access count of each entry
#

@toolcache.cache('memory', track_detailed_stats=True)
def f(a):
    return 2 * a


f(1)
f(1)
f(2)
f(3)
f.cache.exists_in_cache(args=[1])
f.cache.exists_in_cache(args=[4])
f.cache.delete_entry(args=[2])
f.cache.delete_entry(args=[3])
f.cache.print_cache_stats()

# stats for cache f
# current state:
#     - n_entries: 1
#     - ttl: None
#     - max_size: None
#     - max_size_policy: None
# usage:
#     - n_hashes: 8
#     - n_checks: 7
#     - n_hits: 3
#     - n_misses: 4
#     - n_loads: 1
#     - n_saves: 3
#     - n_deletes: 2
#     - n_size_evictions: 0
#     - n_ttl_evictions: 0
# detailed usage:
#     - tracking creation times: True
#     - tracking access times: True
#     - tracking access counts: True

entry_hash = f.cache.compute_entry_hash(args=[1])
creation_time = f.cache.get_entry_creation_time(entry_hash)
access_time = f.cache.get_entry_access_time(entry_hash)
access_count = f.cache.get_entry_access_count(entry_hash)

print('creation_time:', creation_time)
print('access_time:', access_time)
print('access_count:', access_count)

# output:
# creation_time: 1613191975.804925
# access_time: 1613191975.8049505
# access_count: 2

