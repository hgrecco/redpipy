"""
    redpipy.gen
    ~~~~~~~~~~~

    Pythonic wrapper for the rp package.

    original file: rp_gen.h
    commit id: 1f7b7c35070dce637ac699d974d3648b45672f89

    :copyright: 2024 by redpipy Authors, see AUTHORS for more details.
    :license: BSD, see LICENSE for more details.
"""

import rp

from . import constants
from .constants import StatusCode
from .error import RPPError


def _to_debug(values=tuple()):
    VALID = (int, float, str, bool)
    return tuple(value if isinstance(value, VALID) else type(value) for value in values)


def reset() -> None:
    """Sets generate to default values."""

    __status_code = rp.rp_GenReset()

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_GenReset", _to_debug(), __status_code)

    return


def out_enable(channel: constants.Channel) -> None:
    """Enables output

    Parameters
    ----------
    channel
        Channel A or B which we want to enable

    """

    __status_code = rp.rp_GenOutEnable(channel.value)

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_GenOutEnable", _to_debug(channel.value), __status_code)

    return


def out_enable_sync(enable: bool) -> None:
    """Runs/Stop two channels synchronously"""

    __status_code = rp.rp_GenOutEnableSync(enable)

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_GenOutEnableSync", _to_debug(enable), __status_code)

    return


def out_disable(channel: constants.Channel) -> None:
    """Disables output

    Parameters
    ----------
    channel
        Channel A or B which we want to disable

    """

    __status_code = rp.rp_GenOutDisable(channel.value)

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_GenOutDisable", _to_debug(channel.value), __status_code)

    return


def out_is_enabled(channel: constants.Channel) -> bool:
    """Gets value true if channel is enabled otherwise return false.

    Parameters
    ----------
    channel
        Channel A or B.
    value
        Pointer where value will be returned

    """

    __status_code, __value = rp.rp_GenOutIsEnabled(channel.value)

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_GenOutIsEnabled", _to_debug(channel.value), __status_code)

    return __value


def amp(channel: constants.Channel, amplitude: float) -> None:
    """Sets channel signal peak to peak amplitude.

    Parameters
    ----------
    channel
        Channel A or B for witch we want to set amplitude
    amplitude
        Amplitude of the generated signal. From 0 to max value. Max
        amplitude is 1

    """

    __status_code = rp.rp_GenAmp(channel.value, amplitude)

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_GenAmp", _to_debug(channel.value, amplitude), __status_code)

    return


def get_amp(channel: constants.Channel) -> float:
    """Gets channel signal peak to peak amplitude.

    Parameters
    ----------
    channel
        Channel A or B for witch we want to get amplitude.
    amplitude
        Pointer where value will be returned.

    """

    __status_code, __amplitude = rp.rp_GenGetAmp(channel.value)

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_GenGetAmp", _to_debug(channel.value), __status_code)

    return __amplitude


def offset(channel: constants.Channel, offset: float) -> None:
    """Sets DC offset of the signal. signal = signal + DC_offset.

    Parameters
    ----------
    channel
        Channel A or B for witch we want to set DC offset.
    offset
        DC offset of the generated signal. Max offset is 2.

    """

    __status_code = rp.rp_GenOffset(channel.value, offset)

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_GenOffset", _to_debug(channel.value, offset), __status_code)

    return


def get_offset(channel: constants.Channel) -> float:
    """Gets DC offset of the signal.

    Parameters
    ----------
    channel
        Channel A or B for witch we want to get amplitude.
    offset
        Pointer where value will be returned.

    """

    __status_code, __offset = rp.rp_GenGetOffset(channel.value)

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_GenGetOffset", _to_debug(channel.value), __status_code)

    return __offset


def freq(channel: constants.Channel, frequency: float) -> None:
    """Sets channel signal frequency.

    Parameters
    ----------
    channel
        Channel A or B for witch we want to set frequency.
    frequency
        Frequency of the generated signal in Hz.

    """

    __status_code = rp.rp_GenFreq(channel.value, frequency)

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_GenFreq", _to_debug(channel.value, frequency), __status_code)

    return


def freq_direct(channel: constants.Channel, frequency: float) -> None:
    """Sets channel signal frequency in fpga without reset generator and
    rebuild signal.

    Parameters
    ----------
    channel
        Channel A or B for witch we want to set frequency.
    frequency
        Frequency of the generated signal in Hz.

    """

    __status_code = rp.rp_GenFreqDirect(channel.value, frequency)

    if __status_code != StatusCode.OK.value:
        raise RPPError(
            "rp_GenFreqDirect", _to_debug(channel.value, frequency), __status_code
        )

    return


def get_freq(channel: constants.Channel) -> float:
    """Gets channel signal frequency.

    Parameters
    ----------
    channel
        Channel A or B for witch we want to get frequency.
    frequency
        Pointer where value will be returned.

    """

    __status_code, __frequency = rp.rp_GenGetFreq(channel.value)

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_GenGetFreq", _to_debug(channel.value), __status_code)

    return __frequency


def sweep_start_freq(channel: constants.Channel, frequency: float) -> None:
    """Sets channel sweep signal start frequency.

    Parameters
    ----------
    channel
        Channel A or B for witch we want to set frequency.
    frequency
        Frequency of the generated signal in Hz.

    """

    __status_code = rp.rp_GenSweepStartFreq(channel.value, frequency)

    if __status_code != StatusCode.OK.value:
        raise RPPError(
            "rp_GenSweepStartFreq", _to_debug(channel.value, frequency), __status_code
        )

    return


def get_sweep_start_freq(channel: constants.Channel) -> float:
    """Gets channel sweep signal start frequency.

    Parameters
    ----------
    channel
        Channel A or B for witch we want to get frequency.
    frequency
        Pointer where value will be returned.

    """

    __status_code, __frequency = rp.rp_GenGetSweepStartFreq(channel.value)

    if __status_code != StatusCode.OK.value:
        raise RPPError(
            "rp_GenGetSweepStartFreq", _to_debug(channel.value), __status_code
        )

    return __frequency


def sweep_end_freq(channel: constants.Channel, frequency: float) -> None:
    """Sets channel sweep signal end frequency.

    Parameters
    ----------
    channel
        Channel A or B for witch we want to set frequency.
    frequency
        Frequency of the generated signal in Hz.

    """

    __status_code = rp.rp_GenSweepEndFreq(channel.value, frequency)

    if __status_code != StatusCode.OK.value:
        raise RPPError(
            "rp_GenSweepEndFreq", _to_debug(channel.value, frequency), __status_code
        )

    return


def get_sweep_end_freq(channel: constants.Channel) -> float:
    """Gets channel sweep signal end frequency.

    Parameters
    ----------
    channel
        Channel A or B for witch we want to get frequency.
    frequency
        Pointer where value will be returned.

    """

    __status_code, __frequency = rp.rp_GenGetSweepEndFreq(channel.value)

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_GenGetSweepEndFreq", _to_debug(channel.value), __status_code)

    return __frequency


def phase(channel: constants.Channel, phase: float) -> None:
    """Sets channel signal phase. This shifts the signal in time.

    Parameters
    ----------
    channel
        Channel A or B for witch we want to set phase.
    phase
        Phase in degrees of the generated signal. From 0 deg to 180 deg.

    """

    __status_code = rp.rp_GenPhase(channel.value, phase)

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_GenPhase", _to_debug(channel.value, phase), __status_code)

    return


def get_phase(channel: constants.Channel) -> float:
    """Gets channel signal phase.

    Parameters
    ----------
    channel
        Channel A or B for witch we want to get phase.
    phase
        Pointer where value will be returned.

    """

    __status_code, __phase = rp.rp_GenGetPhase(channel.value)

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_GenGetPhase", _to_debug(channel.value), __status_code)

    return __phase


def waveform(channel: constants.Channel, type: constants.Waveform) -> None:
    """Sets channel signal waveform. This determines how the signal looks.

    Parameters
    ----------
    channel
        Channel A or B for witch we want to set waveform type.


    C Parameters
    ------------
    form
        Wave form of the generated signal [SINE, SQUARE, TRIANGLE,
        SAWTOOTH, PWM, DC, ARBITRARY, SWEEP].

    """

    __status_code = rp.rp_GenWaveform(channel.value, type.value)

    if __status_code != StatusCode.OK.value:
        raise RPPError(
            "rp_GenWaveform", _to_debug(channel.value, type.value), __status_code
        )

    return


def get_waveform(channel: constants.Channel) -> constants.Waveform:
    """Gets channel signal waveform.

    Parameters
    ----------
    channel
        Channel A or B for witch we want to get waveform.
    type
        Pointer where value will be returned.

    """

    __status_code, __type = rp.rp_GenGetWaveform(channel.value)

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_GenGetWaveform", _to_debug(channel.value), __status_code)

    return constants.Waveform(__type)


def sweep_mode(channel: constants.Channel, mode: constants.GenSweepMode) -> None:
    """Sets the generation mode for the sweep signal.

    Parameters
    ----------
    channel
        Channel A or B for witch we want to set waveform type.
    mode
        Mode of the generated signal [RP_GEN_SWEEP_MODE_LINEAR,
        RP_GEN_SWEEP_MODE_LOG].

    """

    __status_code = rp.rp_GenSweepMode(channel.value, mode.value)

    if __status_code != StatusCode.OK.value:
        raise RPPError(
            "rp_GenSweepMode", _to_debug(channel.value, mode.value), __status_code
        )

    return


def get_sweep_mode(channel: constants.Channel) -> constants.GenSweepMode:
    """Gets the generation mode for the sweep signal.

    Parameters
    ----------
    channel
        Channel A or B for witch we want to get waveform.
    mode
        Pointer where value will be returned.

    """

    __status_code, __mode = rp.rp_GenGetSweepMode(channel.value)

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_GenGetSweepMode", _to_debug(channel.value), __status_code)

    return constants.GenSweepMode(__mode)


def sweep_dir(channel: constants.Channel, mode: constants.GenSweepDirection) -> None:
    """Sets the direction of frequency change for sweep.

    Parameters
    ----------
    channel
        Channel A or B for witch we want to set waveform type.
    mode
        Wave form of the generated signal [RP_GEN_SWEEP_DIR_NORMAL,
        RP_GEN_SWEEP_DIR_UP_DOWN].

    """

    __status_code = rp.rp_GenSweepDir(channel.value, mode.value)

    if __status_code != StatusCode.OK.value:
        raise RPPError(
            "rp_GenSweepDir", _to_debug(channel.value, mode.value), __status_code
        )

    return


def get_sweep_dir(channel: constants.Channel) -> constants.GenSweepDirection:
    """Gets the direction of frequency change for sweep.

    Parameters
    ----------
    channel
        Channel A or B for witch we want to get waveform.
    mode
        Pointer where value will be returned.

    """

    __status_code, __mode = rp.rp_GenGetSweepDir(channel.value)

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_GenGetSweepDir", _to_debug(channel.value), __status_code)

    return constants.GenSweepDirection(__mode)


def arb_waveform(channel: constants.Channel, length: int) -> float:
    """Sets user defined waveform.

    Parameters
    ----------
    channel
        Channel A or B for witch we want to set waveform.
    waveform
        Use defined wave form, where min is -1V an max is 1V.
    length
        Length of waveform.

    """

    __status_code, __waveform = rp.rp_GenArbWaveform(channel.value, length)

    if __status_code != StatusCode.OK.value:
        raise RPPError(
            "rp_GenArbWaveform", _to_debug(channel.value, length), __status_code
        )

    return __waveform


def get_arb_waveform(
    channel: constants.Channel, waveform: float, length: int
) -> tuple[float, int]:
    """Gets user defined waveform.

    Parameters
    ----------
    channel
        Channel A or B for witch we want to get waveform.
    waveform
        Pointer where waveform will be returned.
    length
        Pointer where waveform length will be returned.

    """

    __status_code, __waveform, __length = rp.rp_GenGetArbWaveform(
        channel.value, waveform, length
    )

    if __status_code != StatusCode.OK.value:
        raise RPPError(
            "rp_GenGetArbWaveform",
            _to_debug(channel.value, waveform, length),
            __status_code,
        )

    return __waveform, __length


def duty_cycle(channel: constants.Channel, ratio: float) -> None:
    """Sets duty cycle of PWM signal.

    Parameters
    ----------
    channel
        Channel A or B for witch we want to set duty cycle.
    ratio
        Ratio betwen the time when signal in HIGH vs the time when signal
        is LOW.

    """

    __status_code = rp.rp_GenDutyCycle(channel.value, ratio)

    if __status_code != StatusCode.OK.value:
        raise RPPError(
            "rp_GenDutyCycle", _to_debug(channel.value, ratio), __status_code
        )

    return


def get_duty_cycle(channel: constants.Channel) -> float:
    """Gets duty cycle of PWM signal.

    Parameters
    ----------
    channel
        Channel A or B for witch we want to get duty cycle.
    ratio
        Pointer where value will be returned.

    """

    __status_code, __ratio = rp.rp_GenGetDutyCycle(channel.value)

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_GenGetDutyCycle", _to_debug(channel.value), __status_code)

    return __ratio


def rise_time(channel: constants.Channel, time: float) -> None:
    """ """

    __status_code = rp.rp_GenRiseTime(channel.value, time)

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_GenRiseTime", _to_debug(channel.value, time), __status_code)

    return


def get_rise_time(channel: constants.Channel) -> float:
    """ """

    __status_code, __time = rp.rp_GenGetRiseTime(channel.value)

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_GenGetRiseTime", _to_debug(channel.value), __status_code)

    return __time


def fall_time(channel: constants.Channel, time: float) -> None:
    """ """

    __status_code = rp.rp_GenFallTime(channel.value, time)

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_GenFallTime", _to_debug(channel.value, time), __status_code)

    return


def get_fall_time(channel: constants.Channel) -> float:
    """ """

    __status_code, __time = rp.rp_GenGetFallTime(channel.value)

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_GenGetFallTime", _to_debug(channel.value), __status_code)

    return __time


def mode(channel: constants.Channel, mode: constants.GenMode) -> None:
    """Sets generation mode.

    Parameters
    ----------
    channel
        Channel A or B for witch we want to set generation mode.
    mode
        Type of signal generation (CONTINUOUS, BURST, STREAM).

    """

    __status_code = rp.rp_GenMode(channel.value, mode.value)

    if __status_code != StatusCode.OK.value:
        raise RPPError(
            "rp_GenMode", _to_debug(channel.value, mode.value), __status_code
        )

    return


def get_mode(channel: constants.Channel) -> constants.GenMode:
    """Gets generation mode.

    Parameters
    ----------
    channel
        Channel A or B for witch we want to get generation mode.
    mode
        Pointer where value will be returned.

    """

    __status_code, __mode = rp.rp_GenGetMode(channel.value)

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_GenGetMode", _to_debug(channel.value), __status_code)

    return constants.GenMode(__mode)


def burst_count(channel: constants.Channel, num: int) -> None:
    """Sets number of generated waveforms in a burst.

    Parameters
    ----------
    channel
        Channel A or B for witch we want to set number of generated
        waveforms in a burst.
    num
        Number of generated waveforms. If -1 a continuous signal will be
        generated.

    """

    __status_code = rp.rp_GenBurstCount(channel.value, num)

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_GenBurstCount", _to_debug(channel.value, num), __status_code)

    return


def get_burst_count(channel: constants.Channel) -> int:
    """Gets number of generated waveforms in a burst.

    Parameters
    ----------
    channel
        Channel A or B for witch we want to get number of generated
        waveforms in a burst.
    num
        Pointer where value will be returned.

    """

    __status_code, __num = rp.rp_GenGetBurstCount(channel.value)

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_GenGetBurstCount", _to_debug(channel.value), __status_code)

    return __num


def burst_last_value(channel: constants.Channel, amplitude: float) -> None:
    """Sets the value to be set at the end of the generated signal in burst
    mode.

    Parameters
    ----------
    channel
        Channel A or B for witch we want to set number of generated
        waveforms in a burst.
    amplitude
        Amplitude level at the end of the signal (Volt).

    """

    __status_code = rp.rp_GenBurstLastValue(channel.value, amplitude)

    if __status_code != StatusCode.OK.value:
        raise RPPError(
            "rp_GenBurstLastValue", _to_debug(channel.value, amplitude), __status_code
        )

    return


def get_burst_last_value(channel: constants.Channel) -> float:
    """Gets the value to be set at the end of the generated signal in burst
    mode.

    Parameters
    ----------
    channel
        Channel A or B for witch we want to get number of generated
        waveforms in a burst.
    amplitude
        Amplitude where value will be returned (Volt).

    """

    __status_code, __amplitude = rp.rp_GenGetBurstLastValue(channel.value)

    if __status_code != StatusCode.OK.value:
        raise RPPError(
            "rp_GenGetBurstLastValue", _to_debug(channel.value), __status_code
        )

    return __amplitude


def set_init_gen_value(channel: constants.Channel, amplitude: float) -> None:
    """The level of which is set by the generator after the outputs are
    turned on before the signal is generated.

    Parameters
    ----------
    channel
        Channel A or B for witch we want to set number of generated
        waveforms in a burst.
    amplitude
        Amplitude level at the end of the signal (Volt).

    """

    __status_code = rp.rp_GenSetInitGenValue(channel.value, amplitude)

    if __status_code != StatusCode.OK.value:
        raise RPPError(
            "rp_GenSetInitGenValue", _to_debug(channel.value, amplitude), __status_code
        )

    return


def get_init_gen_value(channel: constants.Channel) -> float:
    """Gets the value of the initial signal level.

    Parameters
    ----------
    channel
        Channel A or B for witch we want to get number of generated
        waveforms in a burst.
    amplitude
        Amplitude where value will be returned (Volt).

    """

    __status_code, __amplitude = rp.rp_GenGetInitGenValue(channel.value)

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_GenGetInitGenValue", _to_debug(channel.value), __status_code)

    return __amplitude


def burst_repetitions(channel: constants.Channel, repetitions: int) -> None:
    """Sets number of burst repetitions. This determines how many bursts will
    be generated.

    Parameters
    ----------
    channel
        Channel A or B for witch we want to set number of burst
        repetitions.
    repetitions
        Number of generated bursts. If 0x10000, infinite bursts will be
        generated.

    """

    __status_code = rp.rp_GenBurstRepetitions(channel.value, repetitions)

    if __status_code != StatusCode.OK.value:
        raise RPPError(
            "rp_GenBurstRepetitions",
            _to_debug(channel.value, repetitions),
            __status_code,
        )

    return


def get_burst_repetitions(channel: constants.Channel) -> int:
    """Gets number of burst repetitions.

    Parameters
    ----------
    channel
        Channel A or B for witch we want to get number of burst
        repetitions.
    repetitions
        Pointer where value will be returned.

    """

    __status_code, __repetitions = rp.rp_GenGetBurstRepetitions(channel.value)

    if __status_code != StatusCode.OK.value:
        raise RPPError(
            "rp_GenGetBurstRepetitions", _to_debug(channel.value), __status_code
        )

    return __repetitions


def burst_period(channel: constants.Channel, period: int) -> None:
    """Sets the time/period of one burst in micro seconds. Period must be
    equal or greater then the time of one burst. If it is greater than the
    difference will be the delay between two consequential bursts.

    Parameters
    ----------
    channel
        Channel A or B for witch we want to set burst period.
    period
        Time in micro seconds.

    """

    __status_code = rp.rp_GenBurstPeriod(channel.value, period)

    if __status_code != StatusCode.OK.value:
        raise RPPError(
            "rp_GenBurstPeriod", _to_debug(channel.value, period), __status_code
        )

    return


def get_burst_period(channel: constants.Channel) -> int:
    """Gets the period of one burst in micro seconds.

    Parameters
    ----------
    channel
        Channel A or B for witch we want to get burst period.
    period
        Pointer where value will be returned.

    """

    __status_code, __period = rp.rp_GenGetBurstPeriod(channel.value)

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_GenGetBurstPeriod", _to_debug(channel.value), __status_code)

    return __period


def trigger_source(channel: constants.Channel, src: constants.TriggerSource) -> None:
    """Sets trigger source.

    Parameters
    ----------
    channel
        Channel A or B for witch we want to set trigger source.
    src
        Trigger source (INTERNAL, EXTERNAL_PE, EXTERNAL_NE, GATED_BURST).

    """

    __status_code = rp.rp_GenTriggerSource(channel.value, src.value)

    if __status_code != StatusCode.OK.value:
        raise RPPError(
            "rp_GenTriggerSource", _to_debug(channel.value, src.value), __status_code
        )

    return


def get_trigger_source(channel: constants.Channel) -> constants.TriggerSource:
    """Gets trigger source.

    Parameters
    ----------
    channel
        Channel A or B for witch we want to get burst period.
    src
        Pointer where value will be returned.

    """

    __status_code, __src = rp.rp_GenGetTriggerSource(channel.value)

    if __status_code != StatusCode.OK.value:
        raise RPPError(
            "rp_GenGetTriggerSource", _to_debug(channel.value), __status_code
        )

    return constants.TriggerSource(__src)


def synchronise() -> None:
    """The generator is reset on both channels."""

    __status_code = rp.rp_GenSynchronise()

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_GenSynchronise", _to_debug(), __status_code)

    return


def reset_trigger(channel: constants.Channel) -> None:
    """The generator is reset on channels.

    Parameters
    ----------
    channel
        Channel A or B

    """

    __status_code = rp.rp_GenResetTrigger(channel.value)

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_GenResetTrigger", _to_debug(channel.value), __status_code)

    return


def trigger_only(channel: constants.Channel) -> None:
    """ """

    __status_code = rp.rp_GenTriggerOnly(channel.value)

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_GenTriggerOnly", _to_debug(channel.value), __status_code)

    return


def reset_channel_sm(channel: constants.Channel) -> None:
    """Reset the state machine for the selected channel.

    Parameters
    ----------
    channel
        Channel A or B

    """

    __status_code = rp.rp_GenResetChannelSM(channel.value)

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_GenResetChannelSM", _to_debug(channel.value), __status_code)

    return


def set_enable_temp_protection(channel: constants.Channel, enable: bool) -> None:
    """Sets the DAC protection mode from overheating. Only works with
    Redpitaya 250-12 otherwise returns RP_NOTS

    Parameters
    ----------
    channel
        Channel A or B for witch we want to set protection.
    enable
        Flag enabling protection mode.total

    """

    __status_code = rp.rp_SetEnableTempProtection(channel.value, enable)

    if __status_code != StatusCode.OK.value:
        raise RPPError(
            "rp_SetEnableTempProtection",
            _to_debug(channel.value, enable),
            __status_code,
        )

    return


def get_enable_temp_protection(channel: constants.Channel) -> bool:
    """Get status of DAC protection mode from overheating. Only works with
    Redpitaya 250-12 otherwise returns RP_NOTS

    Parameters
    ----------
    channel
        Channel A or B for witch we want to set protection.
    enable
        Flag return current status.

    """

    __status_code, __enable = rp.rp_GetEnableTempProtection(channel.value)

    if __status_code != StatusCode.OK.value:
        raise RPPError(
            "rp_GetEnableTempProtection", _to_debug(channel.value), __status_code
        )

    return __enable


def set_latch_temp_alarm(channel: constants.Channel, status: bool) -> None:
    """Resets the flag indicating that the DAC is overheated. Only works with
    Redpitaya 250-12 otherwise returns RP_NOTS

    Parameters
    ----------
    channel
        Channel A or B.
    status
        New status for latch trigger.

    """

    __status_code = rp.rp_SetLatchTempAlarm(channel.value, status)

    if __status_code != StatusCode.OK.value:
        raise RPPError(
            "rp_SetLatchTempAlarm", _to_debug(channel.value, status), __status_code
        )

    return


def get_latch_temp_alarm(channel: constants.Channel) -> bool:
    """Returns the status that there was an overheat. Only works with
    Redpitaya 250-12 otherwise returns RP_NOTS

    Parameters
    ----------
    channel
        Channel A or B.
    status
        State of latch trigger.

    """

    __status_code, __status = rp.rp_GetLatchTempAlarm(channel.value)

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_GetLatchTempAlarm", _to_debug(channel.value), __status_code)

    return __status


def get_runtime_temp_alarm(channel: constants.Channel) -> bool:
    """Returns the current DAC overheat status in real time. Only works with
    Redpitaya 250-12 otherwise returns RP_NOTS

    Parameters
    ----------
    channel
        Channel A or B.
    status
        Get current state.

    """

    __status_code, __status = rp.rp_GetRuntimeTempAlarm(channel.value)

    if __status_code != StatusCode.OK.value:
        raise RPPError(
            "rp_GetRuntimeTempAlarm", _to_debug(channel.value), __status_code
        )

    return __status


def set_gain_out(channel: constants.Channel, mode: constants.GenGain) -> None:
    """Sets the gain modes for output. Only works with Redpitaya 250-12
    otherwise returns RP_NOTS

    Parameters
    ----------
    channel
        Channel A or B.
    mode
        Set current state.

    """

    __status_code = rp.rp_GenSetGainOut(channel.value, mode.value)

    if __status_code != StatusCode.OK.value:
        raise RPPError(
            "rp_GenSetGainOut", _to_debug(channel.value, mode.value), __status_code
        )

    return


def get_gain_out(channel: constants.Channel) -> constants.GenGain:
    """Get the gain modes for output. Only works with Redpitaya 250-12
    otherwise returns RP_NOTS

    Parameters
    ----------
    channel
        Channel A or B.
    status
        Set current state.

    """

    __status_code, __status = rp.rp_GenGetGainOut(channel.value)

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_GenGetGainOut", _to_debug(channel.value), __status_code)

    return constants.GenGain(__status)


def set_ext_trigger_debouncer_us(value: float) -> None:
    """Sets ext. trigger debouncer for generation in Us (Value must be
    positive).

    Parameters
    ----------
    value
        Value in microseconds.

    """

    __status_code = rp.rp_GenSetExtTriggerDebouncerUs(value)

    if __status_code != StatusCode.OK.value:
        raise RPPError(
            "rp_GenSetExtTriggerDebouncerUs", _to_debug(value), __status_code
        )

    return


def get_ext_trigger_debouncer_us() -> float:
    """Gets ext. trigger debouncer for generation in Us

    Parameters
    ----------
    value
        Return value in microseconds.

    """

    __status_code, __value = rp.rp_GenGetExtTriggerDebouncerUs()

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_GenGetExtTriggerDebouncerUs", _to_debug(), __status_code)

    return __value
