"""class specifying a cache that stores entries on disk"""

import os
import pathlib
import pickle
import tempfile
import time

import orjson

from . import base_cache


class DiskCache(base_cache.BaseCache):
    """a DiskCache is a cache that saves its entries to disk as files"""

    suffix = '.pycache'

    def __init__(
        self,
        cache_dir=None,
        file_format=None,
        f_disk_save=None,
        f_disk_load=None,
        **super_kwargs
    ):
        """initialize a DiskCache

        for complete list of cache configuration options refer to BaseCache

        ## Disk Cache Options
        - cache_dir: str of path where cache should reside, if None use tmpdir
        - file_format: str name of format used to save data
            - one of 'pickle' or 'json'
        - f_disk_save: custom function for saving data to disk
            - function should take `entry_path` and `entry_data` as arguments
        - f_disk_load: custom function for loading data from disk
            - function should take `entry_path` as an argument
        - super_kwargs: kwargs passed on to BaseCache.__init__()
        """

        # determine cache directory
        if cache_dir is None:
            cache_dir = tempfile.mkdtemp()
        self.cache_dir = cache_dir

        # determine file format
        if file_format is None:
            file_format = 'pickle'
        if file_format not in ['json', 'pickle']:
            if f_disk_load is None or f_disk_save is None:
                raise Exception('unsupported file format: ' + str(file_format))
        self.file_format = file_format

        # set save data function
        if f_disk_save is not None:
            self.f_disk_save = f_disk_save
        else:
            self.f_disk_save = self._default_f_disk_save

        # set load data function
        if f_disk_load is not None:
            self.f_disk_load = f_disk_load
        else:
            self.f_disk_load = self._default_f_disk_load

        # set hash_mode
        hash_mode = super_kwargs.get('hash_mode')
        if hash_mode is not None and hash_mode != 'json_digest':
            raise Exception('need custom f_hash hash_mode=\'json_digest\'')
        elif super_kwargs.get('f_hash') is None:
            super_kwargs['hash_mode'] = 'json_digest'

        # run BaseCache init
        super().__init__(**super_kwargs)

        # read access times and creation times from disk
        for entry_hash in self.get_all_entry_hashes():
            if self.track_access_times:
                age = self.get_entry_access_time_from_disk(entry_hash)
                self.entry_creation_times[entry_hash] = age
            if self.track_creation_times:
                age = self.get_entry_create_time_from_disk(entry_hash)
                self.entry_creation_times[entry_hash] = age

    #
    # # crud operations
    #

    def _save(self, entry_hash, entry_data):

        # determine save path
        cache_path = self._get_cache_path(entry_hash)
        parent_dir = os.path.dirname(cache_path)
        if not os.path.isdir(parent_dir):
            os.makedirs(parent_dir)

        # save data
        self.f_disk_save(cache_path=cache_path, entry_data=entry_data)

        # touch file so that modification time is proxy for access time
        pathlib.Path(cache_path).touch()

    def _exists(self, entry_hash):
        cache_path = self._get_cache_path(entry_hash)
        return os.path.isfile(cache_path)

    def _get_all(self):
        len_suffix = len(self.suffix)
        all_entries = [
            os.path.basename(path)[:-len_suffix]
            for path in self._get_all_entry_paths()
        ]
        return all_entries

    def _load(self, entry_hash):
        cache_path = self._get_cache_path(entry_hash)
        return self.f_disk_load(cache_path=cache_path)

    def _delete(self, entry_hash):
        cache_path = self._get_cache_path(entry_hash=entry_hash)
        if os.path.isfile(cache_path):
            os.remove(cache_path)

    def _delete_all(self):
        cache_paths = self._get_all_entry_paths()
        for cache_path in cache_paths:
            if os.path.isfile(cache_path):
                os.remove(cache_path)

    #
    # # disk io methods
    #

    def _default_f_disk_save(self, cache_path, entry_data):
        """default function for saving entries to disk

        ## Inputs
        - cache_path: str path at which to save entry_data
        - entry_data: data to save at cache_path
        """
        if self.file_format == 'pickle':
            with open(cache_path, 'wb') as file:
                pickle.dump(entry_data, file)
        elif self.file_format == 'json':
            with open(cache_path, 'wb') as file:
                file.write(orjson.dumps(entry_data))
        else:
            raise Exception('unknown file format: ' + str(self.file_format))

    def _default_f_disk_load(self, cache_path):
        """default function for loading entries from disk"""
        if self.file_format == 'pickle':
            with open(cache_path, 'rb') as file:
                return pickle.load(file)
        elif self.file_format == 'json':
            with open(cache_path, 'r') as file:
                return orjson.loads(file.read())
        else:
            raise Exception('unknown file format: ' + str(self.file_format))

    #
    # # introspection
    #

    def _print_save_summary(self, entry_hash, entry_data):
        """print summary of entry being saved to disk

        ## Inputs
        - entry_hash: hash of entry to be saved
        - entry_data: data of entry to be saved
        """
        print('[cache]', self.cache_name, 'saving to cache', self.cache_dir)

    def _print_load_summary(self, entry_hash):
        print('[cache]', self.cache_name, 'loading from cache', self.cache_dir)

    #
    # # path processing methods
    #

    def _get_cache_path(self, entry_hash):
        """return file path associated with a particular entry_hash"""
        if isinstance(entry_hash, tuple):
            entry_hash = '__'.join(str(value) for value in entry_hash)
        return os.path.join(self.cache_dir, str(entry_hash) + self.suffix)

    def _get_all_entry_paths(self):
        """return list of file paths corresponding to entries in the cache"""
        paths = []
        for filename in os.listdir(self.cache_dir):
            if filename.endswith(self.suffix):
                cache_path = os.path.join(self.cache_dir, filename)
                paths.append(cache_path)
        return paths

    #
    # # file-related time methods
    #

    def get_entry_age_from_disk(self, entry_hash):
        """use file creation time to determine age of cache entry"""
        cache_path = self._get_cache_path(entry_hash)
        return time.time() - os.path.getctime(cache_path)

    def get_entry_access_time_from_disk(self, entry_hash):
        """use file update time to determine age of cache entry

        file update time is updated every time file is accessed
        - this allows file update time to be a proxy for access time
        """
        cache_path = self._get_cache_path(entry_hash)
        return os.path.getmtime(cache_path)

    def get_entry_creation_time_from_disk(self, entry_hash):
        """use file creation time to determine creation time of cache entry"""
        cache_path = self._get_cache_path(entry_hash)
        return os.path.getctime(cache_path)
