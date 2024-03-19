# Migrated from
# https://raw.githubusercontent.com/RedPitaya/RedPitaya/266a68ae60b09cc8667585ed5c9af348d36f3264/Examples/C/axi.c
from __future__ import annotations

import time

import numpy as np

from .rpwrap import acq, acq_axi, constants, rp
from . import common
from typing_extensions import Literal

# At most 32 buffer size (32 * 2**14)
DATA_SIZE = 524288

_DECIMATION_MAP = common.TwoWayDict[
    Literal[1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192,
            16384, 32768, 65536], constants.Decimation
](
    {
        1:constants.Decimation.DEC_1,
        2:constants.Decimation.DEC_2,
        4:constants.Decimation.DEC_4,
        8:constants.Decimation.DEC_8,
        16:constants.Decimation.DEC_16,
        32:constants.Decimation.DEC_32,
        64:constants.Decimation.DEC_64,
        128:constants.Decimation.DEC_128,
        512:constants.Decimation.DEC_512,
        1024:constants.Decimation.DEC_1024,
        2048:constants.Decimation.DEC_2048,
        4096:constants.Decimation.DEC_4096,
        8192:constants.Decimation.DEC_8192,
        16384:constants.Decimation.DEC_16384,
        32768:constants.Decimation.DEC_32768,
        65536:constants.Decimation.DEC_65536,
    }
)

def acquire(decimation: int):
    dsize = DATA_SIZE

    rp.init_reset(False)
    # Pretty sure that this function does not work.
    start, size = acq_axi.get_memory_region()

    print(f"Reserved memory start 0x{start:X} size 0x0x{size:X}")
    acq.reset_fpga()

    acq_axi.set_decimation_factor(_DECIMATION_MAP[decimation])

    acq_axi.set_trigger_delay(constants.Channel.CH_1, dsize)
    acq_axi.set_trigger_delay(constants.Channel.CH_2, dsize)

    acq_axi.set_buffer_samples(constants.Channel.CH_1, start, dsize)
    acq_axi.set_buffer_samples(constants.Channel.CH_2, start + size // 2, dsize)

    acq_axi.enable(constants.Channel.CH_1, True)
    acq_axi.enable(constants.Channel.CH_2, True)

    acq.set_gain(constants.Channel.CH_1, constants.PinState.HIGH)
    acq.set_gain(constants.Channel.CH_2, constants.PinState.HIGH)

    acq.set_trigger_level(constants.TriggerChannel.CH_1, 0.0)

    acq.start()

    acq.set_trigger_src(constants.AcqTriggerSource.CHA_PE)

    print("Waiting for trigger")
    while acq.get_trigger_state() == constants.AcqTriggerState.WAITING:
        time.sleep(0.001)

    print("Filling buffer")
    while not acq_axi.get_buffer_fill_state(constants.Channel.CH_1):
        time.sleep(0.001)

    acq.stop()

    timevec = np.arange(dsize)

    posChA = acq_axi.get_write_pointer_at_trig(constants.Channel.CH_1)
    posChB = acq_axi.get_write_pointer_at_trig(constants.Channel.CH_2)

    print(f"Tr pos1: 0x{posChA:X} pos2: 0x{posChB:X}")

    buff1 = acq_axi.get_data_raw(constants.Channel.CH_1, posChA, dsize)
    buff2 = acq_axi.get_data_raw(constants.Channel.CH_2, posChB, dsize)

    acq_axi.enable(constants.Channel.CH_1, False)
    acq_axi.enable(constants.Channel.CH_2, False)

    rp.release()

    return timevec, buff1, buff2


import matplotlib.pyplot as plt

t, ch1, ch2 = acquire(1)
plt.plot(t, ch1)
plt.plot(t, ch2)
