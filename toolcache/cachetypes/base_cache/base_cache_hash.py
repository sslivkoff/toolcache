import inspect

from ... import hash_utils


class BaseCacheHash:
    def _initialize_hash_config(
        self,
        normalize_hash_inputs,
        hash_include_args,
        hash_exclude_args,
        old_f,
        hash_mode,
        f_hash,
    ):
        """initialize cache attributes related to hashing

        see BaseCache.__init__ docstring for full description of each argument
        """

        # determine args to include or exclude
        include_not_none = hash_include_args is not None
        exclude_not_none = hash_exclude_args is not None
        if normalize_hash_inputs is None:
            normalize_hash_inputs = include_not_none or exclude_not_none
        if not normalize_hash_inputs and (include_not_none or exclude_not_none):
            raise Exception(
                'must use normalize_hash_inputs if'
                'using hash_exclude_args or hash_exclude_args'
            )
        if include_not_none and exclude_not_none:
            raise Exception(
                'should specify at most one of'
                'hash_include_args or hash_exclude_args'
            )
        self.normalize_hash_inputs = normalize_hash_inputs
        self.hash_include_args = hash_include_args
        self.hash_exclude_args = hash_exclude_args

        # determine hash function
        if hash_mode is not None and f_hash is not None:
            raise Exception(
                'must specify at most one of hash_mode or f_hash'
            )
        if hash_mode is None and f_hash is None:
            hash_mode = 'json'
        if f_hash is not None:
            self.f_hash = f_hash
        elif hash_mode is not None:
            if hash_mode == 'json':
                self.f_hash = hash_utils.compute_hash_json
            elif hash_mode == 'json_digest':
                self.f_hash = hash_utils.compute_hash_json_digest
            else:
                raise Exception('unknown hash mode: ' + str(hash_mode))
        else:
            raise Exception('could not determine f_hash funciton')

        # get argspec of old_f
        if old_f is not None:
            self.old_f_argspec = inspect.getfullargspec(old_f)
        else:
            self.old_f_argspec = None

    def compute_entry_hash(self, args=None, kwargs=None):
        """create hash for an entry give a set of args and kwargs

        ## Inputs
        - args: list of positional args in a function call
        - kwargs: dict of keyword args in a function call
        """

        if args is None:
            args = []
        if kwargs is None:
            kwargs = {}

        if self.normalize_hash_inputs:
            entry_hash = hash_utils.get_function_input_hash(
                argspec=self.old_f_argspec,
                f_hash=self.f_hash,
                args=args,
                kwargs=kwargs,
                include_args=self.hash_include_args,
                exclude_args=self.hash_exclude_args,
            )
        else:
            entry_hash = self.f_hash(*args, **kwargs)

        if self.stats is not None:
            self.stats['n_hashes'] += 1

        return entry_hash

