"""
    redpipy.acq_axi
    ~~~~~~~~~~~~~~~

    Pythonic wrapper for the rp package.

    original file: rp_acq_axi.h
    commit id: 1f7b7c35070dce637ac699d974d3648b45672f89

    :copyright: 2024 by redpipy Authors, see AUTHORS for more details.
    :license: BSD, see LICENSE for more details.
"""
from __future__ import annotations

import numpy as np
import numpy.typing as npt
import rp

from . import constants
from .constants import StatusCode
from .error import RPPError


def _to_debug(values=tuple()):
    VALID = (int, float, str, bool)
    return tuple(value if isinstance(value, VALID) else type(value) for value in values)


def get_buffer_fill_state(channel: constants.Channel) -> bool:
    """Indicates whether the ADC AXI buffer was full of data.

    Parameters
    ----------
    channel
        Channel index
    state
        Returns status

    """

    __status_code, __state = rp.rp_AcqAxiGetBufferFillState(channel.value)

    if __status_code != StatusCode.OK.value:
        raise RPPError(
            "rp_AcqAxiGetBufferFillState", _to_debug(channel.value), __status_code
        )

    return __state


def set_decimation_factor(decimation: constants.Decimation) -> None:
    """Sets the decimation used at acquiring signal for AXI. You can specify
    values in the range (1,2,4,8,16-65536)

    Parameters
    ----------
    decimation
        Decimation values

    """

    __status_code = rp.rp_AcqAxiSetDecimationFactor(decimation.value)

    if __status_code != StatusCode.OK.value:
        raise RPPError(
            "rp_AcqAxiSetDecimationFactor", _to_debug(decimation), __status_code
        )

    return


def get_decimation_factor() -> int:
    """Gets the decimation used at acquiring signal.

    Parameters
    ----------
    decimation
        Decimation values

    """

    __status_code, __decimation = rp.rp_AcqAxiGetDecimationFactor()

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_AcqAxiGetDecimationFactor", _to_debug(), __status_code)

    return __decimation


def set_trigger_delay(channel: constants.Channel, decimated_data_num: int) -> None:
    """Sets the number of decimated data after trigger written into memory.

    Parameters
    ----------
    channel
        Channel index
    decimated_data_num
        Number of decimated data. It must not be higher than the ADC
        buffer size.

    """

    __status_code = rp.rp_AcqAxiSetTriggerDelay(channel.value, decimated_data_num)

    if __status_code != StatusCode.OK.value:
        raise RPPError(
            "rp_AcqAxiSetTriggerDelay",
            _to_debug(channel.value, decimated_data_num),
            __status_code,
        )

    return


def get_trigger_delay(channel: constants.Channel) -> int:
    """Gets the number of decimated data after trigger written into memory.

    Parameters
    ----------
    channel
        Channel index
    decimated_data_num
        Number of decimated data. It must not be higher than the ADC
        buffer size.

    """

    __status_code, __decimated_data_num = rp.rp_AcqAxiGetTriggerDelay(channel.value)

    if __status_code != StatusCode.OK.value:
        raise RPPError(
            "rp_AcqAxiGetTriggerDelay", _to_debug(channel.value), __status_code
        )

    return __decimated_data_num


def get_write_pointer(channel: constants.Channel) -> int:
    """Returns current position of AXI ADC write pointer.

    Parameters
    ----------
    channel
        Channel index
    pos
        Write pointer position

    """

    __status_code, __pos = rp.rp_AcqAxiGetWritePointer(channel.value)

    if __status_code != StatusCode.OK.value:
        raise RPPError(
            "rp_AcqAxiGetWritePointer", _to_debug(channel.value), __status_code
        )

    return __pos


def get_write_pointer_at_trig(channel: constants.Channel) -> int:
    """Returns position of AXI ADC write pointer at time when trigger
    arrived.

    Parameters
    ----------
    channel
        Channel index
    pos
        Write pointer position

    """

    __status_code, __pos = rp.rp_AcqAxiGetWritePointerAtTrig(channel.value)

    if __status_code != StatusCode.OK.value:
        raise RPPError(
            "rp_AcqAxiGetWritePointerAtTrig", _to_debug(channel.value), __status_code
        )

    return __pos


def get_memory_region() -> tuple[int, int]:
    """Get reserved memory for DMA mode

    C Parameters
    ------------
    channel
        Channel index
    enable
        Enable state

    """

    __status_code, ___start, ___size = rp.rp_AcqAxiGetMemoryRegion()

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_AcqAxiGetMemoryRegion", _to_debug(), __status_code)

    return ___start, ___size


def enable(channel: constants.Channel, enable: bool) -> None:
    """Sets the AXI enable state.

    Parameters
    ----------
    channel
        Channel index
    enable
        Enable state

    """

    __status_code = rp.rp_AcqAxiEnable(channel.value, enable)

    if __status_code != StatusCode.OK.value:
        raise RPPError(
            "rp_AcqAxiEnable", _to_debug(channel.value, enable), __status_code
        )

    return


def get_data_raw(
    channel: constants.Channel, pos: int, size: int = constants.ADC_BUFFER_SIZE
) -> npt.NDArray[np.int16]:
    """Returns the AXI ADC buffer in raw units from specified position and
    desired size. Output buffer must be at least 'size' long.

    Parameters
    ----------
    channel
        Channel A or B for which we want to retrieve the ADC buffer.
    pos
        Starting position of the ADC buffer to retrieve.
    size
        Length of the ADC buffer to retrieve. Returns length of filled
        buffer. In case of too small buffer, required size is returned.
    buffer
        The output buffer gets filled with the selected part of the ADC
        buffer.

    """

    buffer = rp.iBuffer(size)

    __status_code, __size, __buffer = rp.rp_AcqAxiGetDataRaw(
        channel.value, pos, size, buffer
    )

    if __status_code != StatusCode.OK.value:
        raise RPPError(
            "rp_AcqAxiGetDataRaw",
            _to_debug(channel.value, pos, size, buffer),
            __status_code,
        )

    __arr_buffer = np.fromiter(buffer, dtype=np.int16, count=__size)

    return __arr_buffer


def get_datav(
    channel: constants.Channel, pos: int, size: int = constants.ADC_BUFFER_SIZE
) -> npt.NDArray[np.float32]:
    """Returns the AXI ADC buffer in Volt units from specified position and
    desired size. Output buffer must be at least 'size' long.

    Parameters
    ----------
    channel
        Channel A or B for which we want to retrieve the ADC buffer.
    pos
        Starting position of the ADC buffer to retrieve
    size
        Length of the ADC buffer to retrieve. Returns length of filled
        buffer. In case of too small buffer, required size is returned.
    buffer
        The output buffer gets filled with the selected part of the ADC
        buffer.

    """

    buffer = rp.fBuffer(size)

    __status_code, __size, __buffer = rp.rp_AcqAxiGetDataV(
        channel.value, pos, size, buffer
    )

    if __status_code != StatusCode.OK.value:
        raise RPPError(
            "rp_AcqAxiGetDataV",
            _to_debug(channel.value, pos, size, buffer),
            __status_code,
        )

    __arr_buffer = np.fromiter(buffer, dtype=np.float32, count=__size)

    return __arr_buffer


def set_buffer_samples(channel: constants.Channel, address: int, samples: int) -> None:
    """Sets the AXI ADC buffer address and size in samples.

    Parameters
    ----------
    channel
        Channel A or B for which we want to set the ADC buffer size.
    address
        Address of the ADC buffer.


    C Parameters
    ------------
    size
        Size of the ADC buffer in samples.

    """

    __status_code = rp.rp_AcqAxiSetBufferSamples(channel.value, address, samples)

    if __status_code != StatusCode.OK.value:
        raise RPPError(
            "rp_AcqAxiSetBufferSamples",
            _to_debug(channel.value, address, samples),
            __status_code,
        )

    return


def set_buffer_bytes(channel: constants.Channel, address: int, size: int) -> None:
    """Sets the AXI ADC buffer address and size in bytes. Buffer size must be
    a multiple of 2.

    Parameters
    ----------
    channel
        Channel A or B for which we want to set the ADC buffer bytes.
    address
        Address of the ADC buffer.
    size
        Size of the ADC buffer in samples.

    """

    __status_code = rp.rp_AcqAxiSetBufferBytes(channel.value, address, size)

    if __status_code != StatusCode.OK.value:
        raise RPPError(
            "rp_AcqAxiSetBufferBytes",
            _to_debug(channel.value, address, size),
            __status_code,
        )

    return
