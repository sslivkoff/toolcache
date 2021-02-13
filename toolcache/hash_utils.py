import hashlib
import inspect

import orjson


json_compatible_types = (int, float, str, list, dict, type(None))


#
# # hash functions
#


def compute_hash_json(*args, **kwargs):
    """compute json hash of given args and kwargs"""

    # prehash any objects
    for a, arg in enumerate(args):
        if not isinstance(arg, json_compatible_types):
            if not isinstance(args, list):
                args = list(args)
            args[a] = hash(arg)
    for name, value in list(kwargs.items()):
        if not isinstance(value, json_compatible_types):
            kwargs[name] = hash(value)

    # compute hash of data
    hash_data = ({'args': args, 'kwargs': kwargs},)
    return orjson.dumps(hash_data, option=orjson.OPT_SORT_KEYS)


def compute_hash_json_digest(*args, **kwargs):
    """compute json hash of given args and kwargs and return md5 hex digest"""
    as_json = compute_hash_json(*args, **kwargs)
    return hashlib.md5(as_json).hexdigest()


#
# # function utils
#


def get_function_input_hash(
    f_hash,
    argspec=None,
    f=None,
    args=None,
    kwargs=None,
    include_args=None,
    exclude_args=None,
):
    """return hash of a function's inputs

    should specify either f or argspec of f

    ## Inputs
    - f_hash: hash function that takes same arguments as f
    - argspec: argspec of function as returned by inspect.getfullargspec(f)
    - f: function whose inputs will be hashed
    - args: list of positional arguments
    - kwargs: dict of keyword arguments
    - include_args: list of str names of args to include in hash
    - exclude_args: list of str names of args to exclude from hash
    """

    if argspec is None:
        if f is None:
            raise Exception('must specify f or argspec')
        argspec = inspect.getfullargspec(f)

    # get args by names
    args_by_names = _get_args_by_names(argspec=argspec, args=args, kwargs=kwargs)

    # take subset of args
    args_by_names = _get_args_subset(
        args_by_names=args_by_names,
        include_args=include_args,
        exclude_args=exclude_args,
    )

    # compute hash
    return f_hash(*args_by_names['varargs'], **args_by_names['kwargs'])


def _get_args_by_names(argspec, args, kwargs):
    """given the raw args and kwargs of a function call, return args by names

    ## Inputs
    - argspec: argspec of function as returned by inspect.getfullargspec(f)
    - args: list of positional arguments
    - kwargs: dict of keyword arguments
    """

    n_argspec_args = len(argspec.args)
    n_given_args = len(args)
    nonvarargs = args[:n_argspec_args]
    varargs = args[n_argspec_args:]

    # # add args
    kwargs = dict(kwargs)
    kwargs.update(dict(zip(argspec.args, nonvarargs)))

    # add defaults
    if n_given_args < n_argspec_args and argspec.defaults is not None:
        n_keep = len(argspec.defaults)
        for key, value in zip(argspec.args[-n_keep:], argspec.defaults):
            kwargs.setdefault(key, value)
    if argspec.kwonlydefaults is not None:
        for key, value in argspec.kwonlydefaults.items():
            kwargs.setdefault(key, value)

    args_by_names = {'kwargs': kwargs, 'varargs': varargs}

    return args_by_names


def _get_args_subset(args_by_names, include_args=None, exclude_args=None):
    """return subset of args

    ## Inputs
    - args_by_names: dict of args_by_names as returned by _get_args_by_names()
    - include_args: list of str names of args to include in hash
    - exclude_args: list of str names of args to exclude from hash
    """

    if include_args is not None and exclude_args is not None:
        raise Exception(
            'should specify at most one of'
            'hash_include_args or hash_exclude_args'
        )

    if include_args is not None:
        kwargs = {
            name: args_by_names['kwargs'][name] for name in include_args
        }
        return dict(varargs=[], kwargs=kwargs)

    elif exclude_args is not None:
        kwargs = {
            name: value
            for name, value in args_by_names['kwargs'].items()
            if name not in exclude_args
        }
        return dict(args_by_names, kwargs=kwargs)

    else:
        return args_by_names

