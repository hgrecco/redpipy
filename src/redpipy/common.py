"""
    redpipy.common
    ~~~~~~~~~~~~~~

    Common functions and classes.


    :copyright: 2024 by redpipy Authors, see AUTHORS for more details.
    :license: BSD, see LICENSE for more details.
"""
from __future__ import annotations

from typing import Generic, Literal, TypeAlias, TypeVar

from .rpwrap import constants

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


DECIMATION_VALUES: TypeAlias = Literal[
    1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768, 65536
]

DECIMATION_MAP = TwoWayDict[DECIMATION_VALUES, constants.Decimation](
    {
        1: constants.Decimation.DEC_1,
        2: constants.Decimation.DEC_2,
        4: constants.Decimation.DEC_4,
        8: constants.Decimation.DEC_8,
        16: constants.Decimation.DEC_16,
        32: constants.Decimation.DEC_32,
        64: constants.Decimation.DEC_64,
        128: constants.Decimation.DEC_128,
        512: constants.Decimation.DEC_512,
        1024: constants.Decimation.DEC_1024,
        2048: constants.Decimation.DEC_2048,
        4096: constants.Decimation.DEC_4096,
        8192: constants.Decimation.DEC_8192,
        16384: constants.Decimation.DEC_16384,
        32768: constants.Decimation.DEC_32768,
        65536: constants.Decimation.DEC_65536,
    }
)


TRIGGER_MAP = TwoWayDict[
    tuple[Literal["ch1", "ch2", "ext", "int"], bool], constants.AcqTriggerSource
](
    {
        ("ch1", True): constants.AcqTriggerSource.CHA_PE,
        ("ch1", False): constants.AcqTriggerSource.CHA_NE,
        ("ch2", True): constants.AcqTriggerSource.CHB_PE,
        ("ch2", False): constants.AcqTriggerSource.CHB_PE,
        ("ext", True): constants.AcqTriggerSource.EXT_PE,
        ("ext", False): constants.AcqTriggerSource.EXT_NE,
        ("int", True): constants.AcqTriggerSource.AWG_PE,
        ("int", False): constants.AcqTriggerSource.AWG_NE,
    }
)

TRIGGER_CH_MAP = TwoWayDict[
    Literal["ch1", "ch2", "ext", "int"], constants.TriggerChannel
](
    {
        "ch1": constants.TriggerChannel.CH_1,
        "ch2": constants.TriggerChannel.CH_2,
        "ext": constants.TriggerChannel.CH_EXT,
        "int": constants.TriggerChannel.CH_1,
    }
)


PIN_MAP = TwoWayDict[tuple[Literal["p", "n"], int], constants.Pin](
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

STATE_MAP = TwoWayDict[bool, constants.PinState](
    {
        True: constants.PinState.HIGH,
        False: constants.PinState.LOW,
    }
)
