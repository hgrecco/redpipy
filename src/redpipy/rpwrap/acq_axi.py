"""
    redpipy.acq_axi
    ~~~~~~~~~~~~~~~

    Pythonic wrapper for the rp package.

    original file: rp_acq_axi.h
    commit id: 1f7b7c35070dce637ac699d974d3648b45672f89

    :copyright: 2024 by redpipy Authors, see AUTHORS for more details.
    :license: BSD, see LICENSE for more details.
"""

import numpy as np
import numpy.typing as npt
import rp

from . import constants
from .constants import StatusCode


def get_buffer_fill_state(channel: constants.Channel) -> bool:
    """Indicates whether the ADC AXI buffer was full of data.

    Parameters
    ----------
    channel
        Channel index

    C Parameters
    ------------
    state
        Returns status
    """

    __status_code, __value = rp.rp_AcqAxiGetBufferFillState(channel)

    if __status_code != StatusCode.OK:
        raise constants.RPPError(
            "rp_AcqAxiGetBufferFillState", (channel,), __status_code
        )

    return __value


def set_decimation_factor(decimation: int) -> None:
    """Sets the decimation used at acquiring signal for AXI. You can specify
    values in the range (1,2,4,8,16-65536)

    Parameters
    ----------
    decimation
        Decimation values
    """

    __status_code = rp.rp_AcqAxiSetDecimationFactor(decimation)

    if __status_code != StatusCode.OK:
        raise constants.RPPError(
            "rp_AcqAxiSetDecimationFactor", (decimation,), __status_code
        )


def get_decimation_factor() -> int:
    """Gets the decimation used at acquiring signal.

    C Parameters
    ------------
    decimation
        Decimation values
    """

    __status_code, __value = rp.rp_AcqAxiGetDecimationFactor()

    if __status_code != StatusCode.OK:
        raise constants.RPPError("rp_AcqAxiGetDecimationFactor", (), __status_code)

    return __value


def set_trigger_delay(channel: constants.Channel, decimated_data_num: int) -> None:
    """Sets the number of decimated data after trigger written into memory.

    Parameters
    ----------
    channel
        Channel indexdecimated_data_num
        Number of decimated data. It must not be higher than the ADC
        buffer size.
    """

    __status_code = rp.rp_AcqAxiSetTriggerDelay(channel, decimated_data_num)

    if __status_code != StatusCode.OK:
        raise constants.RPPError(
            "rp_AcqAxiSetTriggerDelay", (channel, decimated_data_num), __status_code
        )


def get_trigger_delay(channel: constants.Channel) -> int:
    """Gets the number of decimated data after trigger written into memory.

    Parameters
    ----------
    channel
        Channel index

    C Parameters
    ------------
    decimated_data_num
        Number of decimated data. It must not be higher than the ADC
        buffer size.
    """

    __status_code, __value = rp.rp_AcqAxiGetTriggerDelay(channel)

    if __status_code != StatusCode.OK:
        raise constants.RPPError("rp_AcqAxiGetTriggerDelay", (channel,), __status_code)

    return __value


def get_write_pointer(channel: constants.Channel) -> int:
    """Returns current position of AXI ADC write pointer.

    Parameters
    ----------
    channel
        Channel index

    C Parameters
    ------------
    pos
        Write pointer position
    """

    __status_code, __value = rp.rp_AcqAxiGetWritePointer(channel)

    if __status_code != StatusCode.OK:
        raise constants.RPPError("rp_AcqAxiGetWritePointer", (channel,), __status_code)

    return __value


def get_write_pointer_at_trig(channel: constants.Channel) -> int:
    """Returns position of AXI ADC write pointer at time when trigger
    arrived.

    Parameters
    ----------
    channel
        Channel index

    C Parameters
    ------------
    pos
        Write pointer position
    """

    __status_code, __value = rp.rp_AcqAxiGetWritePointerAtTrig(channel)

    if __status_code != StatusCode.OK:
        raise constants.RPPError(
            "rp_AcqAxiGetWritePointerAtTrig", (channel,), __status_code
        )

    return __value


def get_memory_region(_start: int, _size: int) -> tuple[int, int]:
    """Get reserved memory for DMA mode

    C Parameters
    ------------
    channel
        Channel indexenable
        Enable state
    """

    __status_code, __value = rp.rp_AcqAxiGetMemoryRegion(_start, _size)

    if __status_code != StatusCode.OK:
        raise constants.RPPError(
            "rp_AcqAxiGetMemoryRegion", ("<_start>", "<_size>"), __status_code
        )

    return __value


def enable(channel: constants.Channel, enable: bool) -> None:
    """Sets the AXI enable state.

    Parameters
    ----------
    channel
        Channel indexenable
        Enable state
    """

    __status_code = rp.rp_AcqAxiEnable(channel, enable)

    if __status_code != StatusCode.OK:
        raise constants.RPPError("rp_AcqAxiEnable", (channel, enable), __status_code)


def get_data_raw(channel: constants.Channel, pos: int) -> npt.NDArray[np.int16]:
    """Returns the AXI ADC buffer in raw units from specified position and
    desired size. Output buffer must be at least 'size' long.

    Parameters
    ----------
    channel
        Channel A or B for which we want to retrieve the ADC buffer.pos
        Starting position of the ADC buffer to retrieve.size
        Length of the ADC buffer to retrieve. Returns length of filled
        buffer. In case of too small buffer, required size is returned.buffer
        The output buffer gets filled with the selected part of the ADC
        buffer.
    """

    buffer = rp.iBuffer(constants.ADC_BUFFER_SIZE)

    __status_code, __value = rp.rp_AcqAxiGetDataRaw(
        channel, pos, constants.ADC_BUFFER_SIZE, buffer
    )

    if __status_code != StatusCode.OK:
        raise constants.RPPError(
            "rp_AcqAxiGetDataRaw",
            (channel, pos, constants.ADC_BUFFER_SIZE, buffer),
            __status_code,
        )

    return np.fromiter(buffer, dtype=np.int16, count=constants.ADC_BUFFER_SIZE)


def get_datav(channel: constants.Channel, pos: int) -> npt.NDArray[np.float32]:
    """Returns the AXI ADC buffer in Volt units from specified position and
    desired size. Output buffer must be at least 'size' long.

    Parameters
    ----------
    channel
        Channel A or B for which we want to retrieve the ADC buffer.pos
        Starting position of the ADC buffer to retrievesize
        Length of the ADC buffer to retrieve. Returns length of filled
        buffer. In case of too small buffer, required size is returned.buffer
        The output buffer gets filled with the selected part of the ADC
        buffer.
    """

    buffer = rp.fBuffer(constants.ADC_BUFFER_SIZE)

    __status_code, __value = rp.rp_AcqAxiGetDataV(
        channel, pos, constants.ADC_BUFFER_SIZE, buffer
    )

    if __status_code != StatusCode.OK:
        raise constants.RPPError(
            "rp_AcqAxiGetDataV",
            (channel, pos, constants.ADC_BUFFER_SIZE, buffer),
            __status_code,
        )

    return np.fromiter(buffer, dtype=np.float32, count=constants.ADC_BUFFER_SIZE)


def set_buffer_samples(channel: constants.Channel, address: int, samples: int) -> None:
    """Sets the AXI ADC buffer address and size in samples.

    Parameters
    ----------
    channel
        Channel A or B for which we want to set the ADC buffer size.address
        Address of the ADC buffer.

    C Parameters
    ------------
    size
        Size of the ADC buffer in samples.
    """

    __status_code = rp.rp_AcqAxiSetBufferSamples(channel, address, samples)

    if __status_code != StatusCode.OK:
        raise constants.RPPError(
            "rp_AcqAxiSetBufferSamples", (channel, address, samples), __status_code
        )


def set_buffer_bytes(channel: constants.Channel, address: int, size: int) -> None:
    """Sets the AXI ADC buffer address and size in bytes. Buffer size must be
    a multiple of 2.

    Parameters
    ----------
    channel
        Channel A or B for which we want to set the ADC buffer bytes.address
        Address of the ADC buffer.size
        Size of the ADC buffer in samples.
    """

    __status_code = rp.rp_AcqAxiSetBufferBytes(channel, address, size)

    if __status_code != StatusCode.OK:
        raise constants.RPPError(
            "rp_AcqAxiSetBufferBytes", (channel, address, size), __status_code
        )
