"""
    redpipy.rpwrap
    ~~~~~~~~~~~~~~

    A Pythonic wrapper around RedPitaya's rp Python package.

    :copyright: 2024 by redpipy Authors, see AUTHORS for more details.
    :license: BSD, see LICENSE for more details.
"""
from __future__ import annotations

import atexit

from . import acq, acq_axi, constants, gen, rp


def init():
    """Initialize redpitay underlying library and register it's release
    on exit.
    """
    rp.init()
    atexit.register(rp.release)


class RPBoard:
    def __init__(self) -> None:
        # TODO: see if rp can be initialized once (rp.is_api_init() not working properly).
        # Right now, rp has to be init manually in every script.
        self.device_metadata = {
            "FPGA Unique DNA": rp.id_get_dna(),
            "FPGA Synthesized ID": rp.id_get_id(),
            "Library Version": rp.get_version(),
        }
        pass


__all__ = ["acq_axi", "acq", "constants", "gen", "rp", "RPBoard"]
