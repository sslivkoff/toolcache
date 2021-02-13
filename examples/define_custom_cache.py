"""toolcache can use custom cache classes to utilize other storage backends

for example, a cloud object store, or a database
"""

import some_cloud_library
import toolcache


class CloudCache(toolcache.BaseCache):
    """this is a skeleton of what a cloud storage cache might look like"""

    def __init__(self, cloud_config, **super_kwargs):
        self.interface = some_cloud_library.get_cloud_interface(cloud_config)
        super().__init__(**super_kwargs)

    # defining the 5 methods below allows all `toolcache` features to be used

    def _save(self, entry_hash, entry_data):
        self.interface.save_to_cloud(path=entry_hash, data=entry_data)

    def _exists(self, entry_hash):
        return self.interface.exists_in_cloud(path=entry_hash)

    def _get_all(self):
        return some_cloud_library.get_all_cloud_objects()

    def _load(self, entry_hash):
        return self.interface.load_from_cloud(path=entry_hash)

    def _delete(self, entry_hash):
        return self.interface.delete_from_cloud(path=entry_hash)

