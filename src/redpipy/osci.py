"""
    redpipy.osci
    ~~~~~~~~~~~~

    RedPitaya's oscilloscope.


    :copyright: 2024 by redpipy Authors, see AUTHORS for more details.
    :license: BSD, see LICENSE for more details.
"""

import time
import math
from datetime import datetime, timezone
from typing import Any, Generator, Literal

import numpy as np
import numpy.typing as npt
import pandas as pd

from . import common
from .rpwrap import acq, constants, rp


def get_maximum_sampling_rate() -> float:
    acq.set_decimation(constants.Decimation.DEC_1)
    return acq.get_sampling_rate_hz()


#: Samples per second
MAXIMUM_SAMPLING_RATE = 125e6  # get_maximum_sampling_rate()


def calculate_best_decimation(trace_duration: float) -> constants.Decimation:
    """Calculate the best decimation in order to acquire a signal
    of a certain duration.

    Parameter
    ---------
    trace_duration
        Duration of the trace in seconds
    """

    for exponent in range(17):
        decimation = int(2**exponent)
        sampling_rate = MAXIMUM_SAMPLING_RATE / decimation
        current_trace_duration = constants.ADC_BUFFER_SIZE / sampling_rate
        if current_trace_duration >= trace_duration:
            return getattr(constants.Decimation, "DEC_{:d}".format(decimation))

    raise ValueError(
        "Could not find suitable decimation value " "for {trace_duration} seconds."
    )

def calculate_amount_datapoints(min_trace_duration: float, sampling_rate: float) -> int:
    """Calculate the least amount of datapoints that verifies
    trace_duration <= amount_datapoints/sampling_rate.

    Parameter
    ---------
    min_trace_duration
        Duration of the minimum desired trace in seconds.
    sampling_rate
        RP's sampling rate.
    """
    amount_datapoints = math.ceil(min_trace_duration * sampling_rate)
    assert 0 < amount_datapoints <= constants.ADC_BUFFER_SIZE
    return amount_datapoints


_TRIGGER_MAP = common.TwoWayDict[
    tuple[Literal["ch1", "ch2", "ext"], bool], constants.AcqTriggerSource
](
    {
        ("ch1", True): constants.AcqTriggerSource.CHA_PE,
        ("ch1", False): constants.AcqTriggerSource.CHA_NE,
        ("ch2", True): constants.AcqTriggerSource.CHB_PE,
        ("ch2", False): constants.AcqTriggerSource.CHB_PE,
        ("ext", True): constants.AcqTriggerSource.EXT_PE,
        ("ext", False): constants.AcqTriggerSource.EXT_NE,
    }
)

_TRIGGER_CH_MAP = common.TwoWayDict[
    Literal["ch1", "ch2", "ext"], constants.TriggerChannel
](
    {
        "ch1": constants.TriggerChannel.CH_1,
        "ch2": constants.TriggerChannel.CH_2,
        "ext": constants.TriggerChannel.CH_EXT,
    }
)


class Channel:
    """Oscilloscope channel."""

    channel: constants.Channel

    # Is there a real way to enable/disable a channel?
    enabled: bool = False

    def __init__(self, channel: Literal[1, 2], gain: Literal[1, 20] = 1):
        if channel == 1:
            self.channel = constants.Channel.CH_1
        elif channel == 2:
            self.channel = constants.Channel.CH_2

        self.set_gain(gain)

        self.enabled = False

    def get_trace(self, size: int = constants.ADC_BUFFER_SIZE) -> npt.NDArray[np.float32]:
        """Get trace (in volts)."""
        return acq.get_oldest_datav(self.channel, size=size)

    def get_trace_raw(self, size: int = constants.ADC_BUFFER_SIZE) -> npt.NDArray[np.int16]:
        """Get trace (in ADU)."""
        return acq.get_oldest_data_raw(self.channel, size=size)

    def set_gain(self, gain: Literal[1, 20]):
        if gain == 1:
            acq.set_gain(self.channel, constants.PinState.HIGH)
        elif gain == 5:
            acq.set_gain(self.channel, constants.PinState.LOW)


class Oscilloscope:
    """Oscilloscope"""

    def __init__(self) -> None:
        self.device_metadata = {
            "FPGA Unique DNA": rp.id_get_dna(),
            "FPGA Synthesized ID": rp.id_get_id(),
            "Library Version": rp.get_version(),
        }
        self.channel1 = Channel(1)
        self.channel2 = Channel(2)
        self.configure_trigger()
        self._wait_after_trigger = 0

    def get_metadata(self) -> Generator[tuple[Any, Any], Any, None]:
        yield from self.device_metadata.items()
        yield from self.get_timebase_settings().items()
        yield from self.get_trigger_settings().items()

    def get_timebase_settings(self) -> dict[str, Any]:
        """Get timebase settings."""
        trigger_delay = acq.get_trigger_delay() - constants.ADC_BUFFER_SIZE / 2
        sampling_rate = acq.get_sampling_rate_hz()
        return dict(
            decimation=acq.get_decimation_factor(),
            sampling_rate=sampling_rate,
            trace_duration=constants.ADC_BUFFER_SIZE / sampling_rate,
            trigger_delay=trigger_delay / sampling_rate,
            trigger_delay_samples=trigger_delay,
        )

    def get_trigger_settings(self) -> dict[str, Any]:
        """Get trigger settings.

        The trigger source and edge values are read from the Oscilloscope
        class internal configuration. Instead, the trigger level value is
        asked to the hardware.

        """
        if self._trigger_src == constants.AcqTriggerSource.DISABLED:
            return dict(source="disabled", level=None, positive_edge=None)
        elif self._trigger_src == constants.AcqTriggerSource.NOW:
            return dict(source="now", level=None, positive_edge=None)

        source, positive_edge = _TRIGGER_MAP.inv[self._trigger_src]
        tch = _TRIGGER_CH_MAP[source]
        return dict(
            source=source,
            level=acq.get_trigger_level(tch),
            positive_edge=positive_edge,
        )

    def get_timevector_raw(self, size: int = constants.ADC_BUFFER_SIZE) -> npt.NDArray[np.int64]:
        """Get timevector (in samples)."""
        return (
            np.arange(size, dtype=np.int64)  # type: ignore
            + acq.get_trigger_delay() - constants.ADC_BUFFER_SIZE//2
        )

    def get_timevector(self, size: int = constants.ADC_BUFFER_SIZE) -> npt.NDArray[np.float32]:
        """Get timevector (in seconds)."""
        # TODO: update docs to take into account new parameter
        return self.get_timevector_raw(size=size) / acq.get_sampling_rate_hz()

    def get_data(self, raw: bool = False) -> pd.DataFrame:
        """Get data (time, and traces of enabled channels"""
        # TODO: update docs to take into account new parameter
        timestamp = datetime.now(tz=timezone.utc).isoformat()

        if raw:
            out: dict[str, npt.NDArray[Any]] = dict(time=self.get_timevector_raw(size=self._amount_datapoints))
            if self.channel1.enabled:
                out["ch1"] = self.channel1.get_trace_raw(size=self._amount_datapoints)
            if self.channel2.enabled:
                out["ch2"] = self.channel1.get_trace_raw(size=self._amount_datapoints)
        else:
            out: dict[str, npt.NDArray[Any]] = dict(time=self.get_timevector(size=self._amount_datapoints))
            if self.channel1.enabled:
                out["ch1"] = self.channel1.get_trace(size=self._amount_datapoints)
            if self.channel2.enabled:
                out["ch2"] = self.channel1.get_trace(size=self._amount_datapoints)

        df = pd.DataFrame(out)
        df.attrs["timestamp"] = timestamp
        for k, v in self.get_metadata():
            df.attrs[k] = v

        return df

    def configure_trigger(
        self,
        *,
        source: Literal["ch1", "ch2", "ext"] = "ch1",
        level: float = 0,
        positive_edge: bool = True,
    ):
        """Configure the trigger

        Parameters
        ----------
        source, optional
            Trigger source, by default "ch1"
        level, optional
            Trigger level (in volts), by default 0
        positive_edge, optional
            Triggering occurs in positive edge, by default True
        """

        src = _TRIGGER_MAP[(source, positive_edge)]
        tch = _TRIGGER_CH_MAP[source]

        # Store this to be used when arming trigger.
        self._trigger_src = src
        self._trigger_level = (tch, level)

        acq.reset_fpga()
        acq.set_trigger_level(*self._trigger_level)

    def set_timebase(
        self, trace_duration_hint: float, trigger_position: float = 0
    ) -> float:
        """Configure the timebase.

        The duration of acquisition window can only take certain discrete
        values. It is guaranteed that the chosen one will be the shortest
        one that can fit the provided trace duration hint. The actual trace
        duration, is returned.

        Trigger position
        min: -1e5
        max: 1
        *  1: at the end of the measured buffer.
        *  0.5: at the middle of the measured buffer.
        *  0: at the beginning of the measured buffer.
        * -0.5: at the middle of the first previously measured buffer.
        * -1: at the beginning of the first previously measured buffer.
        * -2: at the beginning of the second previously measured buffer.
        and so on.

        Parameters
        ----------
        trace_duration_hint
            Duration of the trace to be measured (in seconds).
        trigger_position, optional
            Position of the trigger as fraction of the buffer size, by default 0
        """
        acq.set_decimation(calculate_best_decimation(trace_duration_hint))

        # TODO: replace trace_duration_hint for the smallest time with the setted decimation
        # that is greater than trace_duration_hint.
        self._amount_datapoints = calculate_amount_datapoints(trace_duration_hint)

        trigger_delay = int(self._amount_datapoints * (-trigger_position) + constants.ADC_BUFFER_SIZE * 1 / 2)
        acq.set_trigger_delay(trigger_delay)

        trace_duration = constants.ADC_BUFFER_SIZE / acq.get_sampling_rate_hz()

        return trace_duration

    def wait_for_trigger(self):
        """Wait until the triggering condition has been met."""
        trace_duration = constants.ADC_BUFFER_SIZE / acq.get_sampling_rate_hz()
        sleep_duration = trace_duration / 1000
        while acq.get_trigger_state() == constants.AcqTriggerState.WAITING:
            time.sleep(sleep_duration)

        # TODO: move this to another function or change the name of thisone. 
        while not acq.get_buffer_fill_state():
            time.sleep(sleep_duration)


    def arm_trigger(self, wait: bool = True) -> None:
        """Arm the trigger.

        If wait is True (default), the thread will lock until the acquisition
        is complete.
        """
        acq.reset_fpga()
        acq.start()
        acq.set_trigger_src(self._trigger_src)
        if wait:
            self.wait_for_trigger()

    def trigger_now(self, wait: bool = True):
        """Trigger now.

        If wait is True (default), the thread will lock until the acquisition
        is complete.
        """
        acq.set_trigger_src(constants.AcqTriggerSource.NOW)
        if wait:
            self.wait_for_trigger()
