"""
    redpipy.analog_input
    ~~~~~~~~~~~~~~~~~~~~

    RedPitaya's analog input.


    :copyright: 2024 by redpipy Authors, see AUTHORS for more details.
    :license: BSD, see LICENSE for more details.
"""
from __future__ import annotations

import math
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from functools import cached_property
from typing import Any, ClassVar, Generator, Literal, get_args

import numpy as np
import numpy.typing as npt
import pandas as pd

from . import common
from .rpwrap import RPBoard, acq, acq_axi, constants


def get_maximum_sampling_rate() -> float:
    acq.set_decimation(constants.Decimation.DEC_1)
    return acq.get_sampling_rate_hz()


# At most 32 buffer size (32 * 2**14)
DATA_SIZE = 524288


#: Samples per second
MAXIMUM_SAMPLING_RATE = 125e6  # get_maximum_sampling_rate()


def frequency_to_decimation(at_least_hz: float) -> common.DECIMATION_VALUES:
    for decimation in reversed(get_args(common.DECIMATION_VALUES)):
        sampling_rate = MAXIMUM_SAMPLING_RATE / decimation
        if sampling_rate > at_least_hz:
            return decimation
    raise ValueError("Cannot find decimation for frequency")


@dataclass(frozen=True)
class ReadDataAcq:
    size: int
    sampling_rate: float
    trigger_delay: int

    def get_time_raw(self) -> npt.NDArray[np.int64]:
        return (
            np.arange(self.size, dtype=np.int64)
            + self.trigger_delay
            - constants.ADC_BUFFER_SIZE // 2
        )

    def get_time(self) -> npt.NDArray[np.float32]:
        return self.get_time_raw() / self.sampling_rate

    def get_ch1_raw(self) -> npt.NDArray[np.int16]:
        return acq.get_oldest_data_raw(constants.Channel.CH_1, size=self.size)

    def get_ch2_raw(self) -> npt.NDArray[np.int16]:
        return acq.get_oldest_data_raw(constants.Channel.CH_2, size=self.size)

    def get_ch1(self) -> npt.NDArray[np.float32]:
        # TODO: for cache reasons, it would be nice to build this from ch1_raw
        return acq.get_oldest_datav(constants.Channel.CH_1, size=self.size)

    def get_ch2(self) -> npt.NDArray[np.float32]:
        # TODO: for cache reasons, it would be nice to build this from ch2_raw
        return acq.get_oldest_datav(constants.Channel.CH_2, size=self.size)

    def wait_until_done(self, channel1: bool, channel2: bool):
        """Wait until the triggering condition has been met."""
        trace_duration = self.size / self.sampling_rate
        sleep_duration = max(trace_duration / 1000, 100e-6)
        while acq.get_trigger_state() == constants.AcqTriggerState.WAITING:
            time.sleep(sleep_duration)

        if channel1 or channel2:
            while not acq.get_buffer_fill_state():
                time.sleep(sleep_duration)

    def is_data_ready(self, channel1: bool, channel2: bool) -> bool:
        if acq.get_trigger_state() == constants.AcqTriggerState.WAITING:
            return False
        if channel1 or channel2:
            if not acq.get_buffer_fill_state():
                return False

        return True

    def stop(self, channel1: bool, channel2: bool):
        if channel1 or channel2:
            acq.stop()


@dataclass(frozen=True)
class ReadDataAcqAxi:
    size: int
    sampling_rate: float
    trigger_delay: int

    def get_time_raw(self) -> npt.NDArray[np.int64]:
        return (
            np.arange(self.size, dtype=np.int64)
            + self.trigger_delay
            - constants.ADC_BUFFER_SIZE // 2
        )

    def get_time(self) -> npt.NDArray[np.float32]:
        return self.get_time_raw() / self.sampling_rate

    def get_ch1_raw(self) -> npt.NDArray[np.int16]:
        pos = acq_axi.get_write_pointer_at_trig(constants.Channel.CH_1)
        return acq_axi.get_data_raw(constants.Channel.CH_1, pos, self.size)

    def get_ch2_raw(self) -> npt.NDArray[np.int16]:
        pos = acq_axi.get_write_pointer_at_trig(constants.Channel.CH_1)
        return acq_axi.get_data_raw(constants.Channel.CH_2, pos, self.size)

    def get_ch1(self) -> npt.NDArray[np.float32]:
        # TODO: for cache reasons, it would be nice to build this from ch1_raw
        pos = acq_axi.get_write_pointer_at_trig(constants.Channel.CH_1)
        return acq_axi.get_datav(constants.Channel.CH_1, pos, self.size)

    def get_ch2(self) -> npt.NDArray[np.float32]:
        # TODO: for cache reasons, it would be nice to build this from ch2_raw
        pos = acq_axi.get_write_pointer_at_trig(constants.Channel.CH_1)
        return acq_axi.get_datav(constants.Channel.CH_2, pos, self.size)

    def wait_until_done(self, channel1: bool, channel2: bool):
        """Wait until the triggering condition has been met."""
        trace_duration = self.size / self.sampling_rate
        sleep_duration = max(trace_duration / 1000, 100e-6)

        while acq.get_trigger_state() == constants.AcqTriggerState.WAITING:
            time.sleep(sleep_duration)

        if channel1:
            while not acq_axi.get_buffer_fill_state(constants.Channel.CH_1):
                time.sleep(sleep_duration)

        if channel2:
            while not acq_axi.get_buffer_fill_state(constants.Channel.CH_2):
                time.sleep(sleep_duration)

    def is_data_ready(self, channel1: bool, channel2: bool) -> bool:
        if acq.get_trigger_state() == constants.AcqTriggerState.WAITING:
            return False
        if channel1:
            if not acq_axi.get_buffer_fill_state(constants.Channel.CH_1):
                return False
        if channel2:
            if not acq_axi.get_buffer_fill_state(constants.Channel.CH_1):
                return False

        return True

    def stop(self, channel1: bool, channel2: bool):
        if channel1 or channel2:
            acq.stop()


@dataclass(frozen=True)
class Data:
    timestamp: str
    ch1_enabled: bool
    ch2_enabled: bool
    metadata: dict[str, Any]
    reader: ReadDataAcq | ReadDataAcqAxi

    state: ClassVar[
        Literal[
            "running",  # measuring + data ready
            "completed",
            "canceled",
        ]
    ] = "running"

    @cached_property
    def time_raw(self) -> npt.NDArray[np.int64]:
        self.check()
        return self.reader.get_time_raw()

    @cached_property
    def time(self) -> npt.NDArray[np.float32]:
        self.check()
        return self.reader.get_time()

    @cached_property
    def ch1_raw(self) -> npt.NDArray[np.int16]:
        self.check()
        return self.reader.get_ch1_raw()

    @cached_property
    def ch2_raw(self) -> npt.NDArray[np.int16]:
        self.check()
        return self.reader.get_ch2_raw()

    @cached_property
    def ch1(self) -> npt.NDArray[np.float32]:
        self.check()
        return self.reader.get_ch1()

    @cached_property
    def ch2(self) -> npt.NDArray[np.float32]:
        self.check()
        return self.reader.get_ch2()

    def as_dataframe(self, raw: bool = False) -> pd.DataFrame:
        """Get data (time, and traces of enabled channels"""

        if raw:
            out: dict[str, npt.NDArray[Any]] = dict(time=self.time_raw)
            if self.ch1_enabled:
                out["ch1"] = self.ch1_raw
            if self.ch2_enabled:
                out["ch2"] = self.ch2_raw
        else:
            out: dict[str, npt.NDArray[Any]] = dict(time=self.time)
            if self.ch1_enabled:
                out["ch1"] = self.ch1
            if self.ch2_enabled:
                out["ch2"] = self.ch2

        df = pd.DataFrame(out)
        df.attrs["timestamp"] = self.timestamp
        for k, v in self.metadata:
            df.attrs[k] = v

        return df

    def read_or_raise(self):
        # Cache results
        if not self.reader.is_data_ready(self.ch1_enabled, self.ch2_enabled):
            raise ValueError("Data is not ready.")

        self._set_as_completed()

    def _set_as_completed(self):
        object.__setattr__(self, "state", "completed")
        self.reader.stop(self.ch1_enabled, self.ch2_enabled)
        _ = self.time, self.ch1, self.ch2, self.time_raw, self.ch1_raw, self.ch2_raw

    def cancel(self):
        object.__setattr__(self, "state", "canceled")
        self.reader.stop(self.ch1_enabled, self.ch2_enabled)

    def check(self, wait: bool = True):
        if self.state == "completed":
            return
        elif self.state == "running":
            self.reader.wait_until_done(self.ch1_enabled, self.ch2_enabled)
            self._set_as_completed()
        if self.state == "canceled":
            raise ValueError("Results not available, measurement canceled.")


class Channel:
    """Oscilloscope channel."""

    channel: constants.Channel

    # Is there a real way to enable/disable a channel?
    enabled: bool = False

    def __init__(self, channel: Literal[1, 2], gain: Literal[1, 5] = 1):
        if channel == 1:
            self.channel = constants.Channel.CH_1
        elif channel == 2:
            self.channel = constants.Channel.CH_2

        self.set_gain(gain)

        self.enabled = False

    def set_gain(self, gain: Literal[1, 5]):
        if gain == 1:
            acq.set_gain(self.channel, constants.PinState.LOW)
        elif gain == 5:
            acq.set_gain(self.channel, constants.PinState.HIGH)


class RPAnalog(RPBoard):
    """Analog"""

    _last_data: Data | None = None

    _decimation: constants.Decimation
    _trigger_delay: int
    _trigger_src: constants.AcqTriggerSource
    _trigger_ch: constants.TriggerChannel
    _trigger_level: float

    def __init__(self) -> None:
        super().__init__()
        self.channel1 = Channel(1)
        self.channel2 = Channel(2)
        self.configure_trigger()
        self.configure_timebase(1024, 1, 0.5, "trace")

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

        source, positive_edge = common.TRIGGER_MAP.inv[self._trigger_src]
        tch = common.TRIGGER_CH_MAP[source]
        return dict(
            source=source,
            level=acq.get_trigger_level(tch),
            positive_edge=positive_edge,
        )

    def configure_trigger(
        self,
        *,
        source: Literal["ch1", "ch2", "ext"] = "ch1",
        level: float = 0,
        positive_edge: bool = True,
    ) -> None:
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
        # Store this to be used when arming trigger.
        self._trigger_src = common.TRIGGER_MAP[(source, positive_edge)]
        self._trigger_ch = common.TRIGGER_CH_MAP[source]
        self._trigger_level = level

    def configure_timebase(
        self,
        samples: int,
        decimation: common.DECIMATION_VALUES,
        delay: float,
        delay_units: Literal["second", "trace"] = "trace",
    ):
        """Configure the timebase.

        The duration of acquisition window can only take certain discrete
        values. It is guaranteed that the chosen one will be the shortest
        one that can fit the provided trace duration hint. The actual trace
        duration, is returned.

        Set the trigger delay.

        The trigger delay is the amount of traces or seconds that are acquired
        after the trigger.

        For example, if the trace_duration is 1s:

        trigger_delay (traces):
        *  0: Trigger and stop acquiring.
        *  1: Trigger and acquire one full trace.
        *  1.5: Trigger, let half a trace pass and acquire a full trace.
        *  2: Trigger, let one trace pass and acquire a full trace.
        And so on.

        trigger_delay (seconds):
        *  0: Trigger and stop acquiring.
        *  1: Trigger and acquire data for 1 second after stopping.
        *  1.5: Trigger and acquire data for 1.5 seconds after stopping.
        *  2: Trigger and acquire data for 2 seconds after stopping.
        And so on.

        Parameters
        ----------
        samples
            Number of data points to acquire
        decimation
            decimation factor (i.e. sampling rate)
        delay
            Amount of traces (or seconds) during which data is acquired after triggering.
        units, optional
            Units in which the delay is specified, either "trace" or "second" by default trace.

        Parameters
        ----------
        trace_duration_hint
            Duration of the trace to be measured (in seconds).
        full_buffer
            The full RP buffer size is returned, by default False.
        """
        self._samples = samples
        self._decimation = common.DECIMATION_MAP[decimation]

        # TODO: fix trigger_delay <= 1trace problems.

        if delay_units == "second":
            delay_samples = math.ceil(delay * acq.get_sampling_rate_hz())
        elif delay_units == "trace":
            delay_samples = delay * self._samples

        self._trigger_delay = int(
            delay_samples + constants.ADC_BUFFER_SIZE * 1 / 2 - self._samples
        )

        return delay_samples

    def acquire(self, trigger_now: bool = False) -> Data:
        if self._last_data is not None and self._last_data.state == "running":
            self._last_data.read_or_raise()

        if self._samples > constants.ADC_BUFFER_SIZE:
            data = self._acquire_axi(trigger_now)
        else:
            data = self._acquire_acq(trigger_now)

        self._last_data = data
        return data

    def _acquire_acq(self, trigger_now: bool = False) -> Data:
        """Arm the trigger.

        If wait is True (default), the thread will lock until the acquisition
        is complete.
        """
        acq.reset_fpga()
        acq.start()

        acq.set_decimation(self._decimation)
        if trigger_now:
            acq.set_trigger_src(constants.AcqTriggerSource.NOW)
        else:
            acq.set_trigger_level(self._trigger_ch, self._trigger_level)
            acq.set_trigger_delay(self._trigger_delay)
            acq.set_trigger_src(self._trigger_src)

        return Data(
            datetime.now(tz=timezone.utc).isoformat(),
            self.channel1.enabled,
            self.channel2.enabled,
            dict(self.get_metadata()),
            ReadDataAcq(self._samples, acq.get_sampling_rate_hz(), self._trigger_delay),
        )

    def _acquire_axi(self, trigger_now: bool = False) -> Data:
        """Arm the trigger.

        If wait is True (default), the thread will lock until the acquisition
        is complete.
        """
        acq.reset_fpga()

        enabled = self.channel1.enabled, self.channel2.enabled

        if sum(enabled) == 0:
            raise

        mem_start, mem_size = acq_axi.get_memory_region()

        # Todo Check this calculation
        # mem size is in bytes
        # each sample takes 2 bytes.
        if 2 * self._samples * sum(enabled) > mem_size:
            raise ValueError("Not enought memory")

        if enabled == (True, False):
            mem_start1, mem_start2 = mem_start, 0
        elif enabled == (False, True):
            mem_start1, mem_start2 = 0, mem_start
        else:  # enabled == (True, True):
            mem_start1, mem_start2 = mem_start, mem_start + mem_size // 2

        acq_axi.set_decimation_factor(self._decimation)

        if self.channel1.enabled:
            acq_axi.set_trigger_delay(constants.Channel.CH_1, self._trigger_delay)
            acq_axi.set_buffer_samples(
                constants.Channel.CH_1, mem_start1, self._samples
            )
            acq_axi.enable(constants.Channel.CH_1, True)

        if self.channel2.enabled:
            acq_axi.set_trigger_delay(constants.Channel.CH_2, self._trigger_delay)
            acq_axi.set_buffer_samples(
                constants.Channel.CH_2, mem_start2, self._samples
            )
            acq_axi.enable(constants.Channel.CH_2, True)

        if trigger_now:
            acq.set_trigger_src(constants.AcqTriggerSource.NOW)
        else:
            acq.set_trigger_level(self._trigger_ch, self._trigger_level)
            acq.set_trigger_delay(self._trigger_delay)
            acq.set_trigger_src(self._trigger_src)

        acq.start()

        return Data(
            datetime.now(tz=timezone.utc).isoformat(),
            self.channel1.enabled,
            self.channel2.enabled,
            dict(self.get_metadata()),
            ReadDataAcqAxi(
                self._samples, acq.get_sampling_rate_hz(), self._trigger_delay
            ),
        )
