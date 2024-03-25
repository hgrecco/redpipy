"""
    redpipy.acq
    ~~~~~~~~~~~

    Pythonic wrapper for the rp package.

    Skipped functions
    -----------------
    - rp_createBuffer
    - rp_deleteBuffer

    original file: rp_acq.h
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


def _to_debug(*values):
    VALID = (int, float, str, bool)
    return tuple(value if isinstance(value, VALID) else type(value) for value in values)


def set_arm_keep(enable: bool) -> None:
    """Enables continous acquirement even after trigger has happened.

    Parameters
    ----------
    enable
        True for enabling and false disabling

    """

    __status_code = rp.rp_AcqSetArmKeep(enable)

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_AcqSetArmKeep", _to_debug(enable), __status_code)

    return


def get_arm_keep() -> bool:
    """Gets status of continous acquirement even after trigger has happened.

    Parameters
    ----------
    state
        Returns status

    """

    __status_code, __state = rp.rp_AcqGetArmKeep()

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_AcqGetArmKeep", _to_debug(), __status_code)

    return __state


def get_buffer_fill_state() -> bool:
    """Indicates whether the ADC buffer was full of data. The length of the
    buffer is determined by the delay. By default, the delay is half the
    buffer.

    Parameters
    ----------
    state
        Returns status

    """

    __status_code, __state = rp.rp_AcqGetBufferFillState()

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_AcqGetBufferFillState", _to_debug(), __status_code)

    return __state


def set_decimation(decimation: constants.Decimation) -> None:
    """Sets the decimation used at acquiring signal. There is only a set of
    pre-defined decimation values which can be specified. See the
    #rp_acq_decimation_t enum values.

    Parameters
    ----------
    decimation
        Specify one of pre-defined decimation values

    """

    __status_code = rp.rp_AcqSetDecimation(decimation.value)

    if __status_code != StatusCode.OK.value:
        raise RPPError(
            "rp_AcqSetDecimation", _to_debug(decimation.value), __status_code
        )

    return


def get_decimation() -> constants.Decimation:
    """Gets the decimation used at acquiring signal. There is only a set of
    pre-defined decimation values which can be specified. See the
    #rp_acq_decimation_t enum values.

    Parameters
    ----------
    decimation
        Returns one of pre-defined decimation values which is currently
        set.

    """

    __status_code, __decimation = rp.rp_AcqGetDecimation()

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_AcqGetDecimation", _to_debug(), __status_code)

    return constants.Decimation(__decimation)


def convert_factor_to_decimation(factor: int) -> constants.Decimation:
    """Convert factor to decimation used at acquiring signal. There is only a
    get of pre-defined decimation values which can be specified. See the
    #rp_acq_decimation_t enum values.

    Parameters
    ----------
    factor
        Decimation factor.
    decimation
        Returns one of pre-defined decimation values which is currently
        set.

    """

    __status_code, __decimation = rp.rp_AcqConvertFactorToDecimation(factor)

    if __status_code != StatusCode.OK.value:
        raise RPPError(
            "rp_AcqConvertFactorToDecimation", _to_debug(factor), __status_code
        )

    return constants.Decimation(__decimation)


def set_decimation_factor(decimation: int) -> None:
    """Sets the decimation used at acquiring signal. You can specify values
    in the range (1,2,4,8,16-65536)

    Parameters
    ----------
    decimation
        Decimation values

    """

    __status_code = rp.rp_AcqSetDecimationFactor(decimation)

    if __status_code != StatusCode.OK.value:
        raise RPPError(
            "rp_AcqSetDecimationFactor", _to_debug(decimation), __status_code
        )

    return


def get_decimation_factor() -> int:
    """Gets the decimation factor used at acquiring signal in a numerical
    form. Although this method returns an integer value representing the
    current factor of the decimation, there is only a set of pre-defined
    decimation factor values which can be returned. See the
    #rp_acq_decimation_t enum values.

    Parameters
    ----------
    decimation
        Returns decimation factor value which is currently set.

    """

    __status_code, __decimation = rp.rp_AcqGetDecimationFactor()

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_AcqGetDecimationFactor", _to_debug(), __status_code)

    return __decimation


def get_sampling_rate_hz() -> float:
    """Gets the sampling rate for acquiring signal in a numerical form in Hz.
    Although this method returns a float value representing the current
    value of the sampling rate, there is only a set of pre-defined
    sampling rate values which can be returned. See the
    #rp_acq_sampling_rate_t enum values.

    Parameters
    ----------
    sampling_rate
        returns currently set sampling rate in Hz

    """

    __status_code, __sampling_rate = rp.rp_AcqGetSamplingRateHz()

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_AcqGetSamplingRateHz", _to_debug(), __status_code)

    return __sampling_rate


def set_averaging(enable: bool) -> None:
    """Enables or disables averaging of data between samples. Data between
    samples can be averaged by setting the averaging flag in the Data
    decimation register.

    C Parameters
    ------------
    enabled
        When true, the averaging is enabled, otherwise it is disabled.

    """

    __status_code = rp.rp_AcqSetAveraging(enable)

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_AcqSetAveraging", _to_debug(enable), __status_code)

    return


def get_averaging() -> bool:
    """Returns information if averaging of data between samples is enabled or
    disabled. Data between samples can be averaged by setting the
    averaging flag in the Data decimation register.

    C Parameters
    ------------
    enabled
        Set to true when the averaging is enabled, otherwise is it set to
        false.

    """

    __status_code, __enable = rp.rp_AcqGetAveraging()

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_AcqGetAveraging", _to_debug(), __status_code)

    return __enable


def set_trigger_src(source: constants.AcqTriggerSource) -> None:
    """Sets the trigger source used at acquiring signal. When acquiring is
    started, the FPGA waits for the trigger condition on the specified
    source and when the condition is met, it starts writing the signal to
    the buffer.

    Parameters
    ----------
    source
        Trigger source.

    """

    __status_code = rp.rp_AcqSetTriggerSrc(source.value)

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_AcqSetTriggerSrc", _to_debug(source.value), __status_code)

    return


def get_trigger_src() -> constants.AcqTriggerSource:
    """Gets the trigger source used at acquiring signal. When acquiring is
    started, the FPGA waits for the trigger condition on the specified
    source and when the condition is met, it starts writing the signal to
    the buffer.

    Parameters
    ----------
    source
        Currently set trigger source.

    """

    __status_code, __source = rp.rp_AcqGetTriggerSrc()

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_AcqGetTriggerSrc", _to_debug(), __status_code)

    return constants.AcqTriggerSource(__source)


def get_trigger_state() -> constants.AcqTriggerState:
    """Returns the trigger state. Either it is waiting for a trigger to
    happen, or it has already been triggered. By default it is in the
    triggered state, which is treated the same as disabled.

    Parameters
    ----------
    state
        Trigger state

    """

    __status_code, __state = rp.rp_AcqGetTriggerState()

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_AcqGetTriggerState", _to_debug(), __status_code)

    return constants.AcqTriggerState(__state)


def set_trigger_delay(decimated_data_num: int) -> None:
    """Sets the number of decimated data after trigger written into memory.

    Parameters
    ----------
    decimated_data_num
        Number of decimated data. It must not be higher than the ADC
        buffer size.

    """

    __status_code = rp.rp_AcqSetTriggerDelay(decimated_data_num)

    if __status_code != StatusCode.OK.value:
        raise RPPError(
            "rp_AcqSetTriggerDelay", _to_debug(decimated_data_num), __status_code
        )

    return


def get_trigger_delay() -> int:
    """Returns current number of decimated data after trigger written into
    memory.

    Parameters
    ----------
    decimated_data_num
        Number of decimated data.

    """

    __status_code, __decimated_data_num = rp.rp_AcqGetTriggerDelay()

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_AcqGetTriggerDelay", _to_debug(), __status_code)

    return __decimated_data_num


def set_trigger_delay_direct(decimated_data_num: int) -> None:
    """Sets the number of decimated data after trigger written into memory.

    Parameters
    ----------
    decimated_data_num
        Number of decimated data. It must not be higher than the ADC
        buffer size.

    """

    __status_code = rp.rp_AcqSetTriggerDelayDirect(decimated_data_num)

    if __status_code != StatusCode.OK.value:
        raise RPPError(
            "rp_AcqSetTriggerDelayDirect", _to_debug(decimated_data_num), __status_code
        )

    return


def get_trigger_delay_direct() -> int:
    """Returns current number of decimated data after trigger written into
    memory.

    Parameters
    ----------
    decimated_data_num
        Number of decimated data.

    """

    __status_code, __decimated_data_num = rp.rp_AcqGetTriggerDelayDirect()

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_AcqGetTriggerDelayDirect", _to_debug(), __status_code)

    return __decimated_data_num


def set_trigger_delay_ns(time_ns: int) -> None:
    """Sets the amount of decimated data in nanoseconds after trigger written
    into memory.

    Parameters
    ----------
    time_ns
        Time in nanoseconds. Number of ADC samples within the specified
        time must not be higher than the ADC buffer size.

    """

    __status_code = rp.rp_AcqSetTriggerDelayNs(time_ns)

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_AcqSetTriggerDelayNs", _to_debug(time_ns), __status_code)

    return


def get_trigger_delay_ns() -> int:
    """Returns the current amount of decimated data in nanoseconds after
    trigger written into memory.

    Parameters
    ----------
    time_ns
        Time in nanoseconds.

    """

    __status_code, __time_ns = rp.rp_AcqGetTriggerDelayNs()

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_AcqGetTriggerDelayNs", _to_debug(), __status_code)

    return __time_ns


def set_trigger_delay_ns_direct(time_ns: int) -> None:
    """Sets the amount of decimated data in nanoseconds after trigger written
    into memory.

    Parameters
    ----------
    time_ns
        Time in nanoseconds. Number of ADC samples within the specified
        time must not be higher than the ADC buffer size.

    """

    __status_code = rp.rp_AcqSetTriggerDelayNsDirect(time_ns)

    if __status_code != StatusCode.OK.value:
        raise RPPError(
            "rp_AcqSetTriggerDelayNsDirect", _to_debug(time_ns), __status_code
        )

    return


def get_trigger_delay_ns_direct() -> int:
    """Returns the current amount of decimated data in nanoseconds after
    trigger written into memory.

    Parameters
    ----------
    time_ns
        Time in nanoseconds.

    """

    __status_code, __time_ns = rp.rp_AcqGetTriggerDelayNsDirect()

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_AcqGetTriggerDelayNsDirect", _to_debug(), __status_code)

    return __time_ns


def get_pre_trigger_counter() -> int:
    """Returns the number of valid data ponts before trigger.

    C Parameters
    ------------
    time_ns
        number of data points.

    """

    __status_code, __value = rp.rp_AcqGetPreTriggerCounter()

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_AcqGetPreTriggerCounter", _to_debug(), __status_code)

    return __value


def set_trigger_level(channel: constants.TriggerChannel, voltage: float) -> None:
    """Sets the trigger threshold value in volts. Makes the trigger when ADC
    value crosses this value.

    Parameters
    ----------
    voltage
        Threshold value for the channel

    """

    __status_code = rp.rp_AcqSetTriggerLevel(channel.value, voltage)

    if __status_code != StatusCode.OK.value:
        raise RPPError(
            "rp_AcqSetTriggerLevel", _to_debug(channel.value, voltage), __status_code
        )

    return


def get_trigger_level(channel: constants.TriggerChannel) -> float:
    """Gets currently set trigger threshold value in volts

    Parameters
    ----------
    voltage
        Current threshold value for the channel

    """

    __status_code, __voltage = rp.rp_AcqGetTriggerLevel(channel.value)

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_AcqGetTriggerLevel", _to_debug(channel.value), __status_code)

    return __voltage


def set_trigger_hyst(voltage: float) -> None:
    """Sets the trigger threshold hysteresis value in volts. Value must be
    outside to enable the trigger again.

    Parameters
    ----------
    voltage
        Threshold hysteresis value for the channel

    """

    __status_code = rp.rp_AcqSetTriggerHyst(voltage)

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_AcqSetTriggerHyst", _to_debug(voltage), __status_code)

    return


def get_trigger_hyst() -> float:
    """Gets currently set trigger threshold hysteresis value in volts

    Parameters
    ----------
    voltage
        Current threshold hysteresis value for the channel

    """

    __status_code, __voltage = rp.rp_AcqGetTriggerHyst()

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_AcqGetTriggerHyst", _to_debug(), __status_code)

    return __voltage


def set_gain(channel: constants.Channel, state: constants.PinState) -> None:
    """Sets the acquire gain state. The gain should be set to the same value
    as it is set on the Red Pitaya hardware by the LV/HV gain jumpers. LV
    = 1V; HV = 20V.

    Parameters
    ----------
    channel
        Channel A or B
    state
        High or Low state

    """

    __status_code = rp.rp_AcqSetGain(channel.value, state.value)

    if __status_code != StatusCode.OK.value:
        raise RPPError(
            "rp_AcqSetGain", _to_debug(channel.value, state.value), __status_code
        )

    return


def get_gain(channel: constants.Channel) -> constants.PinState:
    """Returns the currently set acquire gain state in the library. It may
    not be set to the same value as it is set on the Red Pitaya hardware
    by the LV/HV gain jumpers. LV = 1V; HV = 20V.

    Parameters
    ----------
    channel
        Channel A or B
    state
        Currently set High or Low state in the library.

    """

    __status_code, __state = rp.rp_AcqGetGain(channel.value)

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_AcqGetGain", _to_debug(channel.value), __status_code)

    return constants.PinState(__state)


def get_gainv(channel: constants.Channel) -> float:
    """Returns the currently set acquire gain in the library. It may not be
    set to the same value as it is set on the Red Pitaya hardware by the
    LV/HV gain jumpers. Returns value in Volts.

    Parameters
    ----------
    channel
        Channel A or B
    voltage
        Currently set gain in the library. 1.0 or 20.0 Volts

    """

    __status_code, __voltage = rp.rp_AcqGetGainV(channel.value)

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_AcqGetGainV", _to_debug(channel.value), __status_code)

    return __voltage


def get_write_pointer() -> int:
    """Returns current position of ADC write pointer.

    Parameters
    ----------
    pos
        Write pointer position

    """

    __status_code, __pos = rp.rp_AcqGetWritePointer()

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_AcqGetWritePointer", _to_debug(), __status_code)

    return __pos


def get_write_pointer_at_trig() -> int:
    """Returns position of ADC write pointer at time when trigger arrived.

    Parameters
    ----------
    pos
        Write pointer position

    """

    __status_code, __pos = rp.rp_AcqGetWritePointerAtTrig()

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_AcqGetWritePointerAtTrig", _to_debug(), __status_code)

    return __pos


def start() -> None:
    """Starts the acquire. Signals coming from the input channels are
    acquired and written into memory.
    """

    __status_code = rp.rp_AcqStart()

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_AcqStart", _to_debug(), __status_code)

    return


def stop() -> None:
    """Stops the acquire."""

    __status_code = rp.rp_AcqStop()

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_AcqStop", _to_debug(), __status_code)

    return


def reset() -> None:
    """Resets the acquire writing state machine and set by default all
    parameters.
    """

    __status_code = rp.rp_AcqReset()

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_AcqReset", _to_debug(), __status_code)

    return


def reset_fpga() -> None:
    """Resets the acquire writing state machine."""

    __status_code = rp.rp_AcqResetFpga()

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_AcqResetFpga", _to_debug(), __status_code)

    return


def unlock_trigger() -> None:
    """Unlocks trigger capture after a trigger has been detected."""

    __status_code = rp.rp_AcqUnlockTrigger()

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_AcqUnlockTrigger", _to_debug(), __status_code)

    return


def get_unlock_trigger() -> bool:
    """Returns the trigger's current blocking state.."""

    __status_code, __state = rp.rp_AcqGetUnlockTrigger()

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_AcqGetUnlockTrigger", _to_debug(), __status_code)

    return __state


def get_normalized_data_pos(pos: int) -> int:
    """Normalizes the ADC buffer position. Returns the modulo operation of
    ADC buffer size...

    Parameters
    ----------
    pos
        position to be normalized

    """

    __value = rp.rp_AcqGetNormalizedDataPos(pos)

    return __value


def get_data_pos_raw(
    channel: constants.Channel,
    start_pos: int,
    end_pos: int,
    buffer_size: int = constants.ADC_BUFFER_SIZE,
) -> npt.NDArray[np.int16]:
    """Returns the ADC buffer in raw units from start to end position.

    Parameters
    ----------
    channel
        Channel A or B for which we want to retrieve the ADC buffer.
    start_pos
        Starting position of the ADC buffer to retrieve.
    end_pos
        Ending position of the ADC buffer to retrieve.
    buffer
        The output buffer gets filled with the selected part of the ADC
        buffer.
    buffer_size
        Length of input buffer. Returns length of filled buffer. In case
        of too small buffer, required size is returned.

    """

    buffer = rp.iBuffer(buffer_size)

    __status_code, __buffer, __buffer_size = rp.rp_AcqGetDataPosRaw(
        channel.value, start_pos, end_pos, buffer, buffer_size
    )

    if __status_code != StatusCode.OK.value:
        raise RPPError(
            "rp_AcqGetDataPosRaw",
            _to_debug(channel.value, start_pos, end_pos, buffer, buffer_size),
            __status_code,
        )

    __arr_buffer = np.fromiter(buffer, dtype=np.int16, count=__buffer_size)

    return __arr_buffer


def get_data_posv(
    channel: constants.Channel,
    start_pos: int,
    end_pos: int,
    buffer_size: int = constants.ADC_BUFFER_SIZE,
) -> npt.NDArray[np.float32]:
    """Returns the ADC buffer in Volt units from start to end position.

    Parameters
    ----------
    channel
        Channel A or B for which we want to retrieve the ADC buffer.
    start_pos
        Starting position of the ADC buffer to retrieve.
    end_pos
        Ending position of the ADC buffer to retrieve.
    buffer
        The output buffer gets filled with the selected part of the ADC
        buffer.
    buffer_size
        Length of input buffer. Returns length of filled buffer. In case
        of too small buffer, required size is returned.

    """

    buffer = rp.fBuffer(buffer_size)

    __status_code, __buffer, __buffer_size = rp.rp_AcqGetDataPosV(
        channel.value, start_pos, end_pos, buffer, buffer_size
    )

    if __status_code != StatusCode.OK.value:
        raise RPPError(
            "rp_AcqGetDataPosV",
            _to_debug(channel.value, start_pos, end_pos, buffer, buffer_size),
            __status_code,
        )

    __arr_buffer = np.fromiter(buffer, dtype=np.float32, count=__buffer_size)

    return __arr_buffer


def get_data_raw(
    channel: constants.Channel, pos: int, size: int = constants.ADC_BUFFER_SIZE
) -> npt.NDArray[np.int16]:
    """Returns the ADC buffer in raw units from specified position and
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

    __status_code, __size, __buffer = rp.rp_AcqGetDataRaw(
        channel.value, pos, size, buffer
    )

    if __status_code != StatusCode.OK.value:
        raise RPPError(
            "rp_AcqGetDataRaw",
            _to_debug(channel.value, pos, size, buffer),
            __status_code,
        )

    __arr_buffer = np.fromiter(buffer, dtype=np.int16, count=__size)

    return __arr_buffer


def get_data_raw_with_calib(
    channel: constants.Channel, pos: int, size: int = constants.ADC_BUFFER_SIZE
) -> npt.NDArray[np.int16]:
    """Returns the ADC buffer in calibrated raw units from specified position
    and desired size. Output buffer must be at least 'size' long.

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

    __status_code, __size, __buffer = rp.rp_AcqGetDataRawWithCalib(
        channel.value, pos, size, buffer
    )

    if __status_code != StatusCode.OK.value:
        raise RPPError(
            "rp_AcqGetDataRawWithCalib",
            _to_debug(channel.value, pos, size, buffer),
            __status_code,
        )

    __arr_buffer = np.fromiter(buffer, dtype=np.int16, count=__size)

    return __arr_buffer


def get_oldest_data_raw(
    channel: constants.Channel, size: int = constants.ADC_BUFFER_SIZE
) -> npt.NDArray[np.int16]:
    """Returns the ADC buffer in raw units from the oldest sample to the
    newest one. Output buffer must be at least 'size' long. CAUTION: Use
    this method only when write pointer has stopped (Trigger happened and
    writing stopped).

    Parameters
    ----------
    channel
        Channel A or B for which we want to retrieve the ADC buffer.
    size
        Length of the ADC buffer to retrieve. Returns length of filled
        buffer. In case of too small buffer, required size is returned.
    buffer
        The output buffer gets filled with the selected part of the ADC
        buffer.

    """

    buffer = rp.iBuffer(size)

    __status_code, __size, __buffer = rp.rp_AcqGetOldestDataRaw(
        channel.value, size, buffer
    )

    if __status_code != StatusCode.OK.value:
        raise RPPError(
            "rp_AcqGetOldestDataRaw",
            _to_debug(channel.value, size, buffer),
            __status_code,
        )

    __arr_buffer = np.fromiter(buffer, dtype=np.int16, count=__size)

    return __arr_buffer


def get_latest_data_raw(
    channel: constants.Channel, size: int = constants.ADC_BUFFER_SIZE
) -> npt.NDArray[np.int16]:
    """Returns the latest ADC buffer samples in raw units. Output buffer must
    be at least 'size' long.

    Parameters
    ----------
    channel
        Channel A or B for which we want to retrieve the ADC buffer.
    size
        Length of the ADC buffer to retrieve. Returns length of filled
        buffer. In case of too small buffer, required size is returned.
    buffer
        The output buffer gets filled with the selected part of the ADC
        buffer.

    """

    buffer = rp.iBuffer(size)

    __status_code, __size, __buffer = rp.rp_AcqGetLatestDataRaw(
        channel.value, size, buffer
    )

    if __status_code != StatusCode.OK.value:
        raise RPPError(
            "rp_AcqGetLatestDataRaw",
            _to_debug(channel.value, size, buffer),
            __status_code,
        )

    __arr_buffer = np.fromiter(buffer, dtype=np.int16, count=__size)

    return __arr_buffer


def get_datav(
    channel: constants.Channel, pos: int, size: int = constants.ADC_BUFFER_SIZE
) -> npt.NDArray[np.float32]:
    """Returns the ADC buffer in Volt units from specified position and
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

    __status_code, __size, __buffer = rp.rp_AcqGetDataV(
        channel.value, pos, size, buffer
    )

    if __status_code != StatusCode.OK.value:
        raise RPPError(
            "rp_AcqGetDataV", _to_debug(channel.value, pos, size, buffer), __status_code
        )

    __arr_buffer = np.fromiter(buffer, dtype=np.float32, count=__size)

    return __arr_buffer


def get_data(pos: int) -> np.ndarray:
    """Returns the ADC buffers from specified position and desired size.
    Output buffer must be at least 'size' long.

    Parameters
    ----------
    pos
        Starting position of the ADC buffer to retrieve
    out
        The buffer will be filled according to the settings.


    C Parameters
    ------------
    size
        Length of the ADC buffer to retrieve. Returns length of filled
        buffer. In case of too small buffer, required size is returned.

    """

    __status_code, __out = rp.rp_AcqGetData(pos)

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_AcqGetData", _to_debug(pos), __status_code)

    return __out


def get_oldest_datav(
    channel: constants.Channel, size: int = constants.ADC_BUFFER_SIZE
) -> npt.NDArray[np.float32]:
    """Returns the ADC buffer in Volt units from the oldest sample to the
    newest one. Output buffer must be at least 'size' long. CAUTION: Use
    this method only when write pointer has stopped (Trigger happened and
    writing stopped).

    Parameters
    ----------
    channel
        Channel A or B for which we want to retrieve the ADC buffer.
    size
        Length of the ADC buffer to retrieve. Returns length of filled
        buffer. In case of too small buffer, required size is returned.
    buffer
        The output buffer gets filled with the selected part of the ADC
        buffer.

    """

    buffer = rp.fBuffer(size)

    __status_code, __size, __buffer = rp.rp_AcqGetOldestDataV(
        channel.value, size, buffer
    )

    if __status_code != StatusCode.OK.value:
        raise RPPError(
            "rp_AcqGetOldestDataV",
            _to_debug(channel.value, size, buffer),
            __status_code,
        )

    __arr_buffer = np.fromiter(buffer, dtype=np.float32, count=__size)

    return __arr_buffer


def get_latest_datav(
    channel: constants.Channel, size: int = constants.ADC_BUFFER_SIZE
) -> npt.NDArray[np.float32]:
    """Returns the latest ADC buffer samples in Volt units. Output buffer
    must be at least 'size' long.

    Parameters
    ----------
    channel
        Channel A or B for which we want to retrieve the ADC buffer.
    size
        Length of the ADC buffer to retrieve. Returns length of filled
        buffer. In case of too small buffer, required size is returned.
    buffer
        The output buffer gets filled with the selected part of the ADC
        buffer.

    """

    buffer = rp.fBuffer(size)

    __status_code, __size, __buffer = rp.rp_AcqGetLatestDataV(
        channel.value, size, buffer
    )

    if __status_code != StatusCode.OK.value:
        raise RPPError(
            "rp_AcqGetLatestDataV",
            _to_debug(channel.value, size, buffer),
            __status_code,
        )

    __arr_buffer = np.fromiter(buffer, dtype=np.float32, count=__size)

    return __arr_buffer


def get_buf_size() -> int:
    """Returns the ADC buffer size in samples.

    Parameters
    ----------
    size
        Size of the ADC buffer in samples.

    """

    __status_code, __size = rp.rp_AcqGetBufSize()

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_AcqGetBufSize", _to_debug(), __status_code)

    return __size


def update_acq_filter(channel: constants.Channel) -> None:
    """Sets the current calibration values from temporary memory to the FPGA
    filter
    """

    __status_code = rp.rp_AcqUpdateAcqFilter(channel.value)

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_AcqUpdateAcqFilter", _to_debug(channel.value), __status_code)

    return


def get_filter_calib_value(
    channel: constants.Channel, coef_aa: int, coef_bb: int, coef_kk: int, coef_pp: int
) -> tuple[int, int, int, int]:
    """Sets the current calibration values from temporary memory to the FPGA
    filter

    Parameters
    ----------
    channel
        Channel A or B for which we want to retrieve the ADC buffer.
    coef_aa
        Return AA coefficient.
    coef_bb
        Return BB coefficient.
    coef_kk
        Return KK coefficient.
    coef_pp
        Return PP coefficient.

    """

    (
        __status_code,
        __coef_aa,
        __coef_bb,
        __coef_kk,
        __coef_pp,
    ) = rp.rp_AcqGetFilterCalibValue(channel.value, coef_aa, coef_bb, coef_kk, coef_pp)

    if __status_code != StatusCode.OK.value:
        raise RPPError(
            "rp_AcqGetFilterCalibValue",
            _to_debug(channel.value, coef_aa, coef_bb, coef_kk, coef_pp),
            __status_code,
        )

    return __coef_aa, __coef_bb, __coef_kk, __coef_pp


def set_ext_trigger_debouncer_us(value: float) -> None:
    """Sets ext. trigger debouncer for acquisition in Us (Value must be
    positive).

    Parameters
    ----------
    value
        Value in microseconds.

    """

    __status_code = rp.rp_AcqSetExtTriggerDebouncerUs(value)

    if __status_code != StatusCode.OK.value:
        raise RPPError(
            "rp_AcqSetExtTriggerDebouncerUs", _to_debug(value), __status_code
        )

    return


def get_ext_trigger_debouncer_us() -> float:
    """Gets ext. trigger debouncer for acquisition in Us

    Parameters
    ----------
    value
        Return value in microseconds.

    """

    __status_code, __value = rp.rp_AcqGetExtTriggerDebouncerUs()

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_AcqGetExtTriggerDebouncerUs", _to_debug(), __status_code)

    return __value


def set_ac_dc(channel: constants.Channel, mode: constants.AcqMode) -> None:
    """Sets the AC / DC modes for input. Only works with Redpitaya 250-12
    otherwise returns RP_NOTS

    Parameters
    ----------
    channel
        Channel A or B.
    mode
        Set current state.

    """

    __status_code = rp.rp_AcqSetAC_DC(channel.value, mode.value)

    if __status_code != StatusCode.OK.value:
        raise RPPError(
            "rp_AcqSetAC_DC", _to_debug(channel.value, mode.value), __status_code
        )

    return


def get_ac_dc(channel: constants.Channel) -> constants.AcqMode:
    """Get the AC / DC modes for input. Only works with Redpitaya 250-12
    otherwise returns RP_NOTS

    Parameters
    ----------
    channel
        Channel A or B.
    status
        Set current state.

    """

    __status_code, __status = rp.rp_AcqGetAC_DC(channel.value)

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_AcqGetAC_DC", _to_debug(channel.value), __status_code)

    return constants.AcqMode(__status)
