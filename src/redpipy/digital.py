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

_PIN_MAP = common.TwoWayDict[tuple[Literal["p", "n"], int], constants.Pin](
    {
        ("n", 0): constants.Pin.DIO0_N,
        ("n", 1): constants.Pin.DIO1_N,
        ("n", 2): constants.Pin.DIO2_N,
        ("n", 3): constants.Pin.DIO3_N,
        ("n", 4): constants.Pin.DIO4_N,
        ("n", 5): constants.Pin.DIO5_N,
        ("n", 6): constants.Pin.DIO6_N,
        ("n", 7): constants.Pin.DIO7_N,
        ("p", 0): constants.Pin.DIO0_P,
        ("p", 1): constants.Pin.DIO1_P,
        ("p", 2): constants.Pin.DIO2_P,
        ("p", 3): constants.Pin.DIO3_P,
        ("p", 4): constants.Pin.DIO4_P,
        ("p", 5): constants.Pin.DIO5_P,
        ("p", 6): constants.Pin.DIO6_P,
        ("p", 7): constants.Pin.DIO7_P,
    }
)

_STATE_MAP = common.TwoWayDict[bool, constants.PinState](
    {
        True: constants.PinState.HIGH,
        False: constants.PinState.LOW,
    }
)


class RPDO:
    def __init__(
        self,
        pin: tuple[Literal["n", "p"], int],
        state: bool = True,
    ):
        self.pin = _PIN_MAP[pin]
        rp.dpin_set_direction(self.pin, constants.PinDirection.OUT)
        self.set_state(state)

    @property
    def state(self):
        return _STATE_MAP.inv[self._get_state()]

    def _get_state(self):
        return rp.dpin_get_state(self.pin)

    def set_state(self, state: bool):
        rp.dpin_set_state(self.pin, _STATE_MAP[state])

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
        self.pin = _PIN_MAP[pin]
        rp.dpin_set_direction(self.pin, constants.PinDirection.IN)

    @property
    def state(self):
        return _STATE_MAP.inv[rp.dpin_get_state(self.pin)]

    def __str__(self):
        return str(self.state)
