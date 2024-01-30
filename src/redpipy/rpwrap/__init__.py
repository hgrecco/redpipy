"""
    redpipy.rpwrap
    ~~~~~~~~~~~~~~

    A Pythonic wrapper around RedPitaya's rp Python package.

    :copyright: 2024 by redpipy Authors, see AUTHORS for more details.
    :license: BSD, see LICENSE for more details.
"""

import atexit

from . import acq, acq_axi, constants, gen, rp


def init():
    """Initialize redpitay underlying library and register it's release
    on exit.
    """
    rp.init()
    atexit.register(rp.release)


__all__ = ["acq_axi", "acq", "constants", "gen", "rp"]
