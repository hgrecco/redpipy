"""
    redpipy.common
    ~~~~~~~~~~~~~~

    Common functions and classes.


    :copyright: 2024 by redpipy Authors, see AUTHORS for more details.
    :license: BSD, see LICENSE for more details.
"""
from __future__ import annotations

from typing import Generic, TypeVar

K = TypeVar("K")
V = TypeVar("V")


class TwoWayDict(Generic[K, V]):
    def __init__(self, d: dict[K, V]):
        self._d = d
        self._inv = {v: k for k, v in d.items()}

    def __getitem__(self, __key: K) -> V:
        return self._d[__key]

    @property
    def inv(self) -> dict[V, K]:
        return self._inv
