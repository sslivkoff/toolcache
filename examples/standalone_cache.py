"""toolcache can use standalone caches when there is no function to decorate"""

import toolcache


cache = toolcache.DiskCache()

# first obtain data to be hashed
entry_data = some_expensive_operation(...)
entry_hash = '<some data identifier>'

# save data
cache.save_entry(entry_hash, entry_data)

# load data
loaded_data = cache.load_entry(entry_hash)

# data in will equal data out
assert entry_data == loaded_data

