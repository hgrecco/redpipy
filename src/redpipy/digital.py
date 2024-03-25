"""
    redpipy.digital
    ~~~~~~~~~~~~~~~

    RedPitaya's digital pins control.


    :copyright: 2024 by redpipy Authors, see AUTHORS for more details.
    :license: BSD, see LICENSE for more details.
"""
from __future__ import annotations

import time
from typing import Literal

from . import common
from .rpwrap import constants, rp


class RPDO:
    def __init__(
        self,
        pin: tuple[Literal["n", "p"], int],
        state: bool = True,
    ):
        self.pin = common.PIN_MAP[pin]
        rp.dpin_set_direction(self.pin, constants.PinDirection.OUT)
        self.set_state(state)

    @property
    def state(self):
        return common.STATE_MAP.inv[self._get_state()]

    def _get_state(self):
        return rp.dpin_get_state(self.pin)

    def set_state(self, state: bool):
        rp.dpin_set_state(self.pin, common.STATE_MAP[state])

    def toggle(self):
        self.set_state(not self.state)

    def pulse(self, ontime: float, offtime: float, amount: int = 1):
        for _ in range(amount):
            self.toggle()
            # TODO: implement a better way to delay.
            # sleep is too unstable at ~1 micro seconds.
            time.sleep(ontime)
            self.toggle()
            time.sleep(offtime)

    def __str__(self):
        return str(self.state)


class RPDI:
    def __init__(self, pin: tuple[Literal["n", "p"], int]):
        self.pin = common.PIN_MAP[pin]
        rp.dpin_set_direction(self.pin, constants.PinDirection.IN)

    @property
    def state(self):
        return common.STATE_MAP.inv[rp.dpin_get_state(self.pin)]

    def __str__(self):
        return str(self.state)
