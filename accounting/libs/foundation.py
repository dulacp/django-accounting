"""
Python helpers
"""

from collections import Mapping


def update(d, u, depth=-1):
    """
    Recursively merge or update dict-like objects.
    >>> update({'k1': {'k2': 2}}, {'k1': {'k2': {'k3': 3}}, 'k4': 4})
    {'k1': {'k2': {'k3': 3}}, 'k4': 4}
    """

    for k, v in u.iteritems():
        if isinstance(v, Mapping) and not depth == 0:
            r = update(d.get(k, {}), v, depth=max(depth - 1, -1))
            d[k] = r
        elif isinstance(d, Mapping):
            d[k] = u[k]
        else:
            d = {k: u[k]}
    return d
