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


def reset() -> None:
    """Sets generate to default values."""

    __status_code = rp.rp_GenReset()

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_GenReset", (), __status_code)


def out_enable(channel: constants.Channel) -> None:
    """Enables output

    Parameters
    ----------
    channel
        Channel A or B which we want to enable
    """

    __status_code = rp.rp_GenOutEnable(channel.value)

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_GenOutEnable", (channel,), __status_code)


def out_enable_sync(enable: bool) -> None:
    """Runs/Stop two channels synchronously"""

    __status_code = rp.rp_GenOutEnableSync(enable)

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_GenOutEnableSync", (enable,), __status_code)


def out_disable(channel: constants.Channel) -> None:
    """Disables output

    Parameters
    ----------
    channel
        Channel A or B which we want to disable
    """

    __status_code = rp.rp_GenOutDisable(channel.value)

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_GenOutDisable", (channel,), __status_code)


def out_is_enabled(channel: constants.Channel, value: bool) -> None:
    """Gets value true if channel is enabled otherwise return false.

    Parameters
    ----------
    channel
        Channel A or B.value
        Pointer where value will be returned
    """

    __status_code = rp.rp_GenOutIsEnabled(channel.value, value)

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_GenOutIsEnabled", (channel, "<value>"), __status_code)


def amp(channel: constants.Channel, amplitude: float) -> None:
    """Sets channel signal peak to peak amplitude.

    Parameters
    ----------
    channel
        Channel A or B for witch we want to set amplitudeamplitude
        Amplitude of the generated signal. From 0 to max value. Max
        amplitude is 1
    """

    __status_code = rp.rp_GenAmp(channel.value, amplitude)

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_GenAmp", (channel, amplitude), __status_code)


def get_amp(channel: constants.Channel) -> float:
    """Gets channel signal peak to peak amplitude.

    Parameters
    ----------
    channel
        Channel A or B for witch we want to get amplitude.

    C Parameters
    ------------
    amplitude
        Pointer where value will be returned.
    """

    __status_code, __value = rp.rp_GenGetAmp(channel.value)

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_GenGetAmp", (channel,), __status_code)

    return __value


def offset(channel: constants.Channel, offset: float) -> None:
    """Sets DC offset of the signal. signal = signal + DC_offset.

    Parameters
    ----------
    channel
        Channel A or B for witch we want to set DC offset.offset
        DC offset of the generated signal. Max offset is 2.
    """

    __status_code = rp.rp_GenOffset(channel.value, offset)

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_GenOffset", (channel, offset), __status_code)


def get_offset(channel: constants.Channel) -> float:
    """Gets DC offset of the signal.

    Parameters
    ----------
    channel
        Channel A or B for witch we want to get amplitude.

    C Parameters
    ------------
    offset
        Pointer where value will be returned.
    """

    __status_code, __value = rp.rp_GenGetOffset(channel.value)

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_GenGetOffset", (channel,), __status_code)

    return __value


def freq(channel: constants.Channel, frequency: float) -> None:
    """Sets channel signal frequency.

    Parameters
    ----------
    channel
        Channel A or B for witch we want to set frequency.frequency
        Frequency of the generated signal in Hz.
    """

    __status_code = rp.rp_GenFreq(channel.value, frequency)

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_GenFreq", (channel, frequency), __status_code)


def freq_direct(channel: constants.Channel, frequency: float) -> None:
    """Sets channel signal frequency in fpga without reset generator and
    rebuild signal.

    Parameters
    ----------
    channel
        Channel A or B for witch we want to set frequency.frequency
        Frequency of the generated signal in Hz.
    """

    __status_code = rp.rp_GenFreqDirect(channel.value, frequency)

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_GenFreqDirect", (channel, frequency), __status_code)


def get_freq(channel: constants.Channel) -> float:
    """Gets channel signal frequency.

    Parameters
    ----------
    channel
        Channel A or B for witch we want to get frequency.

    C Parameters
    ------------
    frequency
        Pointer where value will be returned.
    """

    __status_code, __value = rp.rp_GenGetFreq(channel.value)

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_GenGetFreq", (channel,), __status_code)

    return __value


def sweep_start_freq(channel: constants.Channel, frequency: float) -> None:
    """Sets channel sweep signal start frequency.

    Parameters
    ----------
    channel
        Channel A or B for witch we want to set frequency.frequency
        Frequency of the generated signal in Hz.
    """

    __status_code = rp.rp_GenSweepStartFreq(channel.value, frequency)

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_GenSweepStartFreq", (channel, frequency), __status_code)


def get_sweep_start_freq(channel: constants.Channel) -> float:
    """Gets channel sweep signal start frequency.

    Parameters
    ----------
    channel
        Channel A or B for witch we want to get frequency.

    C Parameters
    ------------
    frequency
        Pointer where value will be returned.
    """

    __status_code, __value = rp.rp_GenGetSweepStartFreq(channel.value)

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_GenGetSweepStartFreq", (channel,), __status_code)

    return __value


def sweep_end_freq(channel: constants.Channel, frequency: float) -> None:
    """Sets channel sweep signal end frequency.

    Parameters
    ----------
    channel
        Channel A or B for witch we want to set frequency.frequency
        Frequency of the generated signal in Hz.
    """

    __status_code = rp.rp_GenSweepEndFreq(channel.value, frequency)

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_GenSweepEndFreq", (channel, frequency), __status_code)


def get_sweep_end_freq(channel: constants.Channel) -> float:
    """Gets channel sweep signal end frequency.

    Parameters
    ----------
    channel
        Channel A or B for witch we want to get frequency.

    C Parameters
    ------------
    frequency
        Pointer where value will be returned.
    """

    __status_code, __value = rp.rp_GenGetSweepEndFreq(channel.value)

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_GenGetSweepEndFreq", (channel,), __status_code)

    return __value


def phase(channel: constants.Channel, phase: float) -> None:
    """Sets channel signal phase. This shifts the signal in time.

    Parameters
    ----------
    channel
        Channel A or B for witch we want to set phase.phase
        Phase in degrees of the generated signal. From 0 deg to 180 deg.
    """

    __status_code = rp.rp_GenPhase(channel.value, phase)

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_GenPhase", (channel, phase), __status_code)


def get_phase(channel: constants.Channel) -> float:
    """Gets channel signal phase.

    Parameters
    ----------
    channel
        Channel A or B for witch we want to get phase.

    C Parameters
    ------------
    phase
        Pointer where value will be returned.
    """

    __status_code, __value = rp.rp_GenGetPhase(channel.value)

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_GenGetPhase", (channel,), __status_code)

    return __value


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
        raise RPPError("rp_GenWaveform", (channel, type), __status_code)


def get_waveform(channel: constants.Channel) -> constants.Waveform:
    """Gets channel signal waveform.

    Parameters
    ----------
    channel
        Channel A or B for witch we want to get waveform.

    C Parameters
    ------------
    type
        Pointer where value will be returned.
    """

    __status_code, __value = rp.rp_GenGetWaveform(channel.value)

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_GenGetWaveform", (channel,), __status_code)

    return __value


def sweep_mode(channel: constants.Channel, mode: constants.GenSweepMode) -> None:
    """Sets the generation mode for the sweep signal.

    Parameters
    ----------
    channel
        Channel A or B for witch we want to set waveform type.mode
        Mode of the generated signal [RP_GEN_SWEEP_MODE_LINEAR,
        RP_GEN_SWEEP_MODE_LOG].
    """

    __status_code = rp.rp_GenSweepMode(channel.value, mode.value)

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_GenSweepMode", (channel, mode), __status_code)


def get_sweep_mode(channel: constants.Channel) -> constants.GenSweepMode:
    """Gets the generation mode for the sweep signal.

    Parameters
    ----------
    channel
        Channel A or B for witch we want to get waveform.

    C Parameters
    ------------
    mode
        Pointer where value will be returned.
    """

    __status_code, __value = rp.rp_GenGetSweepMode(channel.value)

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_GenGetSweepMode", (channel,), __status_code)

    return __value


def sweep_dir(channel: constants.Channel, mode: constants.GenSweepDirection) -> None:
    """Sets the direction of frequency change for sweep.

    Parameters
    ----------
    channel
        Channel A or B for witch we want to set waveform type.mode
        Wave form of the generated signal [RP_GEN_SWEEP_DIR_NORMAL,
        RP_GEN_SWEEP_DIR_UP_DOWN].
    """

    __status_code = rp.rp_GenSweepDir(channel.value, mode.value)

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_GenSweepDir", (channel, mode), __status_code)


def get_sweep_dir(channel: constants.Channel) -> constants.GenSweepDirection:
    """Gets the direction of frequency change for sweep.

    Parameters
    ----------
    channel
        Channel A or B for witch we want to get waveform.

    C Parameters
    ------------
    mode
        Pointer where value will be returned.
    """

    __status_code, __value = rp.rp_GenGetSweepDir(channel.value)

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_GenGetSweepDir", (channel,), __status_code)

    return __value


def arb_waveform(channel: constants.Channel, waveform: float, length: int) -> None:
    """Sets user defined waveform.

    Parameters
    ----------
    channel
        Channel A or B for witch we want to set waveform.waveform
        Use defined wave form, where min is -1V an max is 1V.length
        Length of waveform.
    """

    __status_code = rp.rp_GenArbWaveform(channel.value, waveform, length)

    if __status_code != StatusCode.OK.value:
        raise RPPError(
            "rp_GenArbWaveform", (channel, "<waveform>", length), __status_code
        )


def get_arb_waveform(
    channel: constants.Channel, waveform: float, length: int
) -> tuple[constants.Channel, float, int]:
    """Gets user defined waveform.

    Parameters
    ----------
    channel
        Channel A or B for witch we want to get waveform.waveform
        Pointer where waveform will be returned.length
        Pointer where waveform length will be returned.
    """

    __status_code, __value = rp.rp_GenGetArbWaveform(channel.value, waveform, length)

    if __status_code != StatusCode.OK.value:
        raise RPPError(
            "rp_GenGetArbWaveform", (channel, "<waveform>", "<length>"), __status_code
        )

    return __value


def duty_cycle(channel: constants.Channel, ratio: float) -> None:
    """Sets duty cycle of PWM signal.

    Parameters
    ----------
    channel
        Channel A or B for witch we want to set duty cycle.ratio
        Ratio betwen the time when signal in HIGH vs the time when signal
        is LOW.
    """

    __status_code = rp.rp_GenDutyCycle(channel.value, ratio)

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_GenDutyCycle", (channel, ratio), __status_code)


def get_duty_cycle(channel: constants.Channel) -> float:
    """Gets duty cycle of PWM signal.

    Parameters
    ----------
    channel
        Channel A or B for witch we want to get duty cycle.

    C Parameters
    ------------
    ratio
        Pointer where value will be returned.
    """

    __status_code, __value = rp.rp_GenGetDutyCycle(channel.value)

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_GenGetDutyCycle", (channel,), __status_code)

    return __value


def rise_time(channel: constants.Channel, time: float) -> None:
    """ """

    __status_code = rp.rp_GenRiseTime(channel.value, time)

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_GenRiseTime", (channel, time), __status_code)


def get_rise_time(channel: constants.Channel) -> float:
    """ """

    __status_code, __value = rp.rp_GenGetRiseTime(channel.value)

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_GenGetRiseTime", (channel,), __status_code)

    return __value


def fall_time(channel: constants.Channel, time: float) -> None:
    """ """

    __status_code = rp.rp_GenFallTime(channel.value, time)

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_GenFallTime", (channel, time), __status_code)


def get_fall_time(channel: constants.Channel) -> float:
    """ """

    __status_code, __value = rp.rp_GenGetFallTime(channel.value)

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_GenGetFallTime", (channel,), __status_code)

    return __value


def mode(channel: constants.Channel, mode: constants.GenMode) -> None:
    """Sets generation mode.

    Parameters
    ----------
    channel
        Channel A or B for witch we want to set generation mode.mode
        Type of signal generation (CONTINUOUS, BURST, STREAM).
    """

    __status_code = rp.rp_GenMode(channel.value, mode.value)

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_GenMode", (channel, mode), __status_code)


def get_mode(channel: constants.Channel) -> constants.GenMode:
    """Gets generation mode.

    Parameters
    ----------
    channel
        Channel A or B for witch we want to get generation mode.

    C Parameters
    ------------
    mode
        Pointer where value will be returned.
    """

    __status_code, __value = rp.rp_GenGetMode(channel.value)

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_GenGetMode", (channel,), __status_code)

    return __value


def burst_count(channel: constants.Channel, num: int) -> None:
    """Sets number of generated waveforms in a burst.

    Parameters
    ----------
    channel
        Channel A or B for witch we want to set number of generated
        waveforms in a burst.num
        Number of generated waveforms. If -1 a continuous signal will be
        generated.
    """

    __status_code = rp.rp_GenBurstCount(channel.value, num)

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_GenBurstCount", (channel, num), __status_code)


def get_burst_count(channel: constants.Channel) -> int:
    """Gets number of generated waveforms in a burst.

    Parameters
    ----------
    channel
        Channel A or B for witch we want to get number of generated
        waveforms in a burst.

    C Parameters
    ------------
    num
        Pointer where value will be returned.
    """

    __status_code, __value = rp.rp_GenGetBurstCount(channel.value)

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_GenGetBurstCount", (channel,), __status_code)

    return __value


def burst_last_value(channel: constants.Channel, amplitude: float) -> None:
    """Sets the value to be set at the end of the generated signal in burst
    mode.

    Parameters
    ----------
    channel
        Channel A or B for witch we want to set number of generated
        waveforms in a burst.amplitude
        Amplitude level at the end of the signal (Volt).
    """

    __status_code = rp.rp_GenBurstLastValue(channel.value, amplitude)

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_GenBurstLastValue", (channel, amplitude), __status_code)


def get_burst_last_value(channel: constants.Channel) -> float:
    """Gets the value to be set at the end of the generated signal in burst
    mode.

    Parameters
    ----------
    channel
        Channel A or B for witch we want to get number of generated
        waveforms in a burst.

    C Parameters
    ------------
    amplitude
        Amplitude where value will be returned (Volt).
    """

    __status_code, __value = rp.rp_GenGetBurstLastValue(channel.value)

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_GenGetBurstLastValue", (channel,), __status_code)

    return __value


def set_init_gen_value(channel: constants.Channel, amplitude: float) -> None:
    """The level of which is set by the generator after the outputs are
    turned on before the signal is generated.

    Parameters
    ----------
    channel
        Channel A or B for witch we want to set number of generated
        waveforms in a burst.amplitude
        Amplitude level at the end of the signal (Volt).
    """

    __status_code = rp.rp_GenSetInitGenValue(channel.value, amplitude)

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_GenSetInitGenValue", (channel, amplitude), __status_code)


def get_init_gen_value(channel: constants.Channel) -> float:
    """Gets the value of the initial signal level.

    Parameters
    ----------
    channel
        Channel A or B for witch we want to get number of generated
        waveforms in a burst.

    C Parameters
    ------------
    amplitude
        Amplitude where value will be returned (Volt).
    """

    __status_code, __value = rp.rp_GenGetInitGenValue(channel.value)

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_GenGetInitGenValue", (channel,), __status_code)

    return __value


def burst_repetitions(channel: constants.Channel, repetitions: int) -> None:
    """Sets number of burst repetitions. This determines how many bursts will
    be generated.

    Parameters
    ----------
    channel
        Channel A or B for witch we want to set number of burst
        repetitions.repetitions
        Number of generated bursts. If 0x10000, infinite bursts will be
        generated.
    """

    __status_code = rp.rp_GenBurstRepetitions(channel.value, repetitions)

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_GenBurstRepetitions", (channel, repetitions), __status_code)


def get_burst_repetitions(channel: constants.Channel) -> int:
    """Gets number of burst repetitions.

    Parameters
    ----------
    channel
        Channel A or B for witch we want to get number of burst
        repetitions.

    C Parameters
    ------------
    repetitions
        Pointer where value will be returned.
    """

    __status_code, __value = rp.rp_GenGetBurstRepetitions(channel.value)

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_GenGetBurstRepetitions", (channel,), __status_code)

    return __value


def burst_period(channel: constants.Channel, period: int) -> None:
    """Sets the time/period of one burst in micro seconds. Period must be
    equal or greater then the time of one burst. If it is greater than the
    difference will be the delay between two consequential bursts.

    Parameters
    ----------
    channel
        Channel A or B for witch we want to set burst period.period
        Time in micro seconds.
    """

    __status_code = rp.rp_GenBurstPeriod(channel.value, period)

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_GenBurstPeriod", (channel, period), __status_code)


def get_burst_period(channel: constants.Channel) -> int:
    """Gets the period of one burst in micro seconds.

    Parameters
    ----------
    channel
        Channel A or B for witch we want to get burst period.

    C Parameters
    ------------
    period
        Pointer where value will be returned.
    """

    __status_code, __value = rp.rp_GenGetBurstPeriod(channel.value)

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_GenGetBurstPeriod", (channel,), __status_code)

    return __value


def trigger_source(channel: constants.Channel, src: constants.TriggerSource) -> None:
    """Sets trigger source.

    Parameters
    ----------
    channel
        Channel A or B for witch we want to set trigger source.src
        Trigger source (INTERNAL, EXTERNAL_PE, EXTERNAL_NE, GATED_BURST).
    """

    __status_code = rp.rp_GenTriggerSource(channel.value, src.value)

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_GenTriggerSource", (channel, src), __status_code)


def get_trigger_source(channel: constants.Channel) -> constants.TriggerSource:
    """Gets trigger source.

    Parameters
    ----------
    channel
        Channel A or B for witch we want to get burst period.

    C Parameters
    ------------
    src
        Pointer where value will be returned.
    """

    __status_code, __value = rp.rp_GenGetTriggerSource(channel.value)

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_GenGetTriggerSource", (channel,), __status_code)

    return __value


def synchronise() -> None:
    """The generator is reset on both channels."""

    __status_code = rp.rp_GenSynchronise()

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_GenSynchronise", (), __status_code)


def reset_trigger(channel: constants.Channel) -> None:
    """The generator is reset on channels.

    Parameters
    ----------
    channel
        Channel A or B
    """

    __status_code = rp.rp_GenResetTrigger(channel.value)

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_GenResetTrigger", (channel,), __status_code)


def trigger_only(channel: constants.Channel) -> None:
    """ """

    __status_code = rp.rp_GenTriggerOnly(channel.value)

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_GenTriggerOnly", (channel,), __status_code)


def reset_channel_sm(channel: constants.Channel) -> None:
    """Reset the state machine for the selected channel.

    Parameters
    ----------
    channel
        Channel A or B
    """

    __status_code = rp.rp_GenResetChannelSM(channel.value)

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_GenResetChannelSM", (channel,), __status_code)


def set_enable_temp_protection(channel: constants.Channel, enable: bool) -> None:
    """Sets the DAC protection mode from overheating. Only works with
    Redpitaya 250-12 otherwise returns RP_NOTS

    Parameters
    ----------
    channel
        Channel A or B for witch we want to set protection.enable
        Flag enabling protection mode.total
    """

    __status_code = rp.rp_SetEnableTempProtection(channel.value, enable)

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_SetEnableTempProtection", (channel, enable), __status_code)


def get_enable_temp_protection(channel: constants.Channel) -> bool:
    """Get status of DAC protection mode from overheating. Only works with
    Redpitaya 250-12 otherwise returns RP_NOTS

    Parameters
    ----------
    channel
        Channel A or B for witch we want to set protection.

    C Parameters
    ------------
    enable
        Flag return current status.
    """

    __status_code, __value = rp.rp_GetEnableTempProtection(channel.value)

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_GetEnableTempProtection", (channel,), __status_code)

    return __value


def set_latch_temp_alarm(channel: constants.Channel, status: bool) -> None:
    """Resets the flag indicating that the DAC is overheated. Only works with
    Redpitaya 250-12 otherwise returns RP_NOTS

    Parameters
    ----------
    channel
        Channel A or B.status
         New status for latch trigger.
    """

    __status_code = rp.rp_SetLatchTempAlarm(channel.value, status)

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_SetLatchTempAlarm", (channel, status), __status_code)


def get_latch_temp_alarm(channel: constants.Channel) -> bool:
    """Returns the status that there was an overheat. Only works with
    Redpitaya 250-12 otherwise returns RP_NOTS

    Parameters
    ----------
    channel
        Channel A or B.

    C Parameters
    ------------
    status
         State of latch trigger.
    """

    __status_code, __value = rp.rp_GetLatchTempAlarm(channel.value)

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_GetLatchTempAlarm", (channel,), __status_code)

    return __value


def get_runtime_temp_alarm(channel: constants.Channel) -> bool:
    """Returns the current DAC overheat status in real time. Only works with
    Redpitaya 250-12 otherwise returns RP_NOTS

    Parameters
    ----------
    channel
        Channel A or B.

    C Parameters
    ------------
    status
         Get current state.
    """

    __status_code, __value = rp.rp_GetRuntimeTempAlarm(channel.value)

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_GetRuntimeTempAlarm", (channel,), __status_code)

    return __value


def set_gain_out(channel: constants.Channel, mode: constants.GenGain) -> None:
    """Sets the gain modes for output. Only works with Redpitaya 250-12
    otherwise returns RP_NOTS

    Parameters
    ----------
    channel
        Channel A or B.mode
        Set current state.
    """

    __status_code = rp.rp_GenSetGainOut(channel.value, mode.value)

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_GenSetGainOut", (channel, mode), __status_code)


def get_gain_out(channel: constants.Channel) -> constants.GenGain:
    """Get the gain modes for output. Only works with Redpitaya 250-12
    otherwise returns RP_NOTS

    Parameters
    ----------
    channel
        Channel A or B.

    C Parameters
    ------------
    status
        Set current state.
    """

    __status_code, __value = rp.rp_GenGetGainOut(channel.value)

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_GenGetGainOut", (channel,), __status_code)

    return __value


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
        raise RPPError("rp_GenSetExtTriggerDebouncerUs", (value,), __status_code)


def get_ext_trigger_debouncer_us() -> float:
    """Gets ext. trigger debouncer for generation in Us

    C Parameters
    ------------
    value
        Return value in microseconds.
    """

    __status_code, __value = rp.rp_GenGetExtTriggerDebouncerUs()

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_GenGetExtTriggerDebouncerUs", (), __status_code)

    return __value
