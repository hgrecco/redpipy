"""
    redpipy.rp
    ~~~~~~~~~~

    Pythonic wrapper for the rp package.

    original file: rp.h
    commit id: 1f7b7c35070dce637ac699d974d3648b45672f89

    :copyright: 2024 by redpipy Authors, see AUTHORS for more details.
    :license: BSD, see LICENSE for more details.
"""
from __future__ import annotations

import rp

from . import constants
from .constants import StatusCode
from .error import RPPError


def _to_debug(*values):
    VALID = (int, float, str, bool)
    return tuple(value if isinstance(value, VALID) else type(value) for value in values)


def init() -> None:
    """ """

    __status_code = rp.rp_Init()

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_Init", _to_debug(), __status_code)

    return


def init_reset(reset: bool) -> None:
    """ """

    __status_code = rp.rp_InitReset(reset)

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_InitReset", _to_debug(reset), __status_code)

    return


def is_api_init() -> None:
    """ """

    __status_code = rp.rp_IsApiInit()

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_IsApiInit", _to_debug(), __status_code)

    return


def release() -> None:
    """Releases the library resources. It must be called last, after library
    is not used anymore. Typically before application exits.
    """

    __status_code = rp.rp_Release()

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_Release", _to_debug(), __status_code)

    return


def reset() -> None:
    """Resets all modules. Typically calles after rp_Init() application
    exits.
    """

    __status_code = rp.rp_Reset()

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_Reset", _to_debug(), __status_code)

    return


def get_version() -> str:
    """Retrieves the library version number"""

    __value = rp.rp_GetVersion()

    return __value


def get_error(error_code: int) -> str:
    """Returns textual representation of error code.

    Parameters
    ----------
    error_code
        Error code returned from API.

    """

    __value = rp.rp_GetError(error_code)

    return __value


def enable_digital_loop(enable: bool) -> None:
    """Enable or disables digital loop. This internally connect output to
    input

    Parameters
    ----------
    enable
        True if you want to enable this feature or false if you want to
        disable it

    """

    __status_code = rp.rp_EnableDigitalLoop(enable)

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_EnableDigitalLoop", _to_debug(enable), __status_code)

    return


def id_get_id() -> int:
    """Gets FPGA Synthesized ID"""

    __status_code, __id = rp.rp_IdGetID()

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_IdGetID", _to_debug(), __status_code)

    return __id


def id_get_dna() -> int:
    """Gets FPGA Unique DNA"""

    __status_code, __dna = rp.rp_IdGetDNA()

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_IdGetDNA", _to_debug(), __status_code)

    return __dna


def led_set_state(state: int) -> None:
    """ """

    __status_code = rp.rp_LEDSetState(state)

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_LEDSetState", _to_debug(state), __status_code)

    return


def led_get_state() -> int:
    """ """

    __status_code, __state = rp.rp_LEDGetState()

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_LEDGetState", _to_debug(), __status_code)

    return __state


def gpio_n_set_direction(direction: int) -> None:
    """ """

    __status_code = rp.rp_GPIOnSetDirection(direction)

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_GPIOnSetDirection", _to_debug(direction), __status_code)

    return


def gpio_n_get_direction() -> int:
    """ """

    __status_code, __direction = rp.rp_GPIOnGetDirection()

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_GPIOnGetDirection", _to_debug(), __status_code)

    return __direction


def gpio_n_set_state(state: int) -> None:
    """ """

    __status_code = rp.rp_GPIOnSetState(state)

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_GPIOnSetState", _to_debug(state), __status_code)

    return


def gpio_n_get_state() -> int:
    """ """

    __status_code, __state = rp.rp_GPIOnGetState()

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_GPIOnGetState", _to_debug(), __status_code)

    return __state


def gpio_p_set_direction(direction: int) -> None:
    """ """

    __status_code = rp.rp_GPIOpSetDirection(direction)

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_GPIOpSetDirection", _to_debug(direction), __status_code)

    return


def gpio_p_get_direction() -> int:
    """ """

    __status_code, __direction = rp.rp_GPIOpGetDirection()

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_GPIOpGetDirection", _to_debug(), __status_code)

    return __direction


def gpio_p_set_state(state: int) -> None:
    """ """

    __status_code = rp.rp_GPIOpSetState(state)

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_GPIOpSetState", _to_debug(state), __status_code)

    return


def gpio_p_get_state() -> int:
    """ """

    __status_code, __state = rp.rp_GPIOpGetState()

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_GPIOpGetState", _to_debug(), __status_code)

    return __state


def enable_debug_reg() -> None:
    """ """

    __status_code = rp.rp_EnableDebugReg()

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_EnableDebugReg", _to_debug(), __status_code)

    return


def set_can_mode_enable(enable: bool) -> None:
    """Enables or disables the output of the CAN controller on pins CAN0_tx:
    GPIO_P 7 and CAN0_rx: GPIO_N 7

    Parameters
    ----------
    enable
        True if you want to enable this feature or false if you want to
        disable it

    """

    __status_code = rp.rp_SetCANModeEnable(enable)

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_SetCANModeEnable", _to_debug(enable), __status_code)

    return


def get_can_mode_enable() -> bool:
    """Returns the current state of GPIO outputs

    Parameters
    ----------
    state
        True if this mode is enabled

    """

    __status_code, __state = rp.rp_GetCANModeEnable()

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_GetCANModeEnable", _to_debug(), __status_code)

    return __state


def dpin_reset() -> None:
    """Sets digital pins to default values. Pins DIO1_P - DIO7_P, RP_DIO0_N -
    RP_DIO7_N are set all INPUT and to LOW. LEDs are set to LOW/OFF
    """

    __status_code = rp.rp_DpinReset()

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_DpinReset", _to_debug(), __status_code)

    return


def dpin_set_state(pin: constants.Pin, state: constants.PinState) -> None:
    """Sets digital input output pin state.

    Parameters
    ----------
    pin
        Digital input output pin.
    state
        High/Low state that will be set at the given pin.

    """

    __status_code = rp.rp_DpinSetState(pin.value, state.value)

    if __status_code != StatusCode.OK.value:
        raise RPPError(
            "rp_DpinSetState", _to_debug(pin.value, state.value), __status_code
        )

    return


def dpin_get_state(pin: constants.Pin) -> constants.PinState:
    """Gets digital input output pin state.

    Parameters
    ----------
    pin
        Digital input output pin.
    state
        High/Low state that is set at the given pin.

    """

    __status_code, __state = rp.rp_DpinGetState(pin.value)

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_DpinGetState", _to_debug(pin.value), __status_code)

    return constants.PinState(__state)


def dpin_set_direction(pin: constants.Pin, direction: constants.PinDirection) -> None:
    """Sets digital input output pin direction. LED pins are already
    automatically set to the output direction, and they cannot be set to
    the input direction. DIOx_P and DIOx_N are must set either output or
    input direction before they can be used. When set to input direction,
    it is not allowed to write into these pins.

    Parameters
    ----------
    pin
        Digital input output pin.
    direction
        In/Out direction that will be set at the given pin.

    """

    __status_code = rp.rp_DpinSetDirection(pin.value, direction.value)

    if __status_code != StatusCode.OK.value:
        raise RPPError(
            "rp_DpinSetDirection", _to_debug(pin.value, direction.value), __status_code
        )

    return


def dpin_get_direction(pin: constants.Pin) -> constants.PinDirection:
    """Gets digital input output pin direction.

    Parameters
    ----------
    pin
        Digital input output pin.
    direction
        In/Out direction that is set at the given pin.

    """

    __status_code, __direction = rp.rp_DpinGetDirection(pin.value)

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_DpinGetDirection", _to_debug(pin.value), __status_code)

    return constants.PinDirection(__direction)


def set_enable_daisy_chain_trig_sync(enable: bool) -> None:
    """Enables trigger sync over SATA daisy chain connectors. Once the
    primary board will be triggered, the trigger will be forwarded to the
    secondary board over the SATA connector where the trigger can be
    detected using rp_GenTriggerSource with EXT_NE selector. Noticed that
    the trigger that is received over SATA is ORed with the external
    trigger from GPIO.

    Parameters
    ----------
    enable
        Turns on the mode.

    """

    __status_code = rp.rp_SetEnableDaisyChainTrigSync(enable)

    if __status_code != StatusCode.OK.value:
        raise RPPError(
            "rp_SetEnableDaisyChainTrigSync", _to_debug(enable), __status_code
        )

    return


def get_enable_daisy_chain_trig_sync() -> bool:
    """Returns the current state of the SATA daisy chain mode.

    Parameters
    ----------
    status
        Current state.

    """

    __status_code, __status = rp.rp_GetEnableDaisyChainTrigSync()

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_GetEnableDaisyChainTrigSync", _to_debug(), __status_code)

    return __status


def set_dpin_enable_trig_output(enable: bool) -> None:
    """Function turns GPION_0 into trigger output for selected source -
    acquisition or generation

    Parameters
    ----------
    enable
        Turns on the mode.

    """

    __status_code = rp.rp_SetDpinEnableTrigOutput(enable)

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_SetDpinEnableTrigOutput", _to_debug(enable), __status_code)

    return


def get_dpin_enable_trig_output() -> bool:
    """Returns the current mode state for GPION_0. If true, then the pin mode
    works as a source

    C Parameters
    ------------
    status
        Current state.

    """

    __status_code, __state = rp.rp_GetDpinEnableTrigOutput()

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_GetDpinEnableTrigOutput", _to_debug(), __status_code)

    return __state


def set_source_trig_output(mode: constants.OutTriggerMode) -> None:
    """Sets the trigger source mode. ADC/DAC

    Parameters
    ----------
    mode
        Sets the mode.

    """

    __status_code = rp.rp_SetSourceTrigOutput(mode.value)

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_SetSourceTrigOutput", _to_debug(mode.value), __status_code)

    return


def get_source_trig_output() -> constants.OutTriggerMode:
    """Returns the trigger source mode. ADC/DAC

    Parameters
    ----------
    mode
        Returns the current mode.

    """

    __status_code, __mode = rp.rp_GetSourceTrigOutput()

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_GetSourceTrigOutput", _to_debug(), __status_code)

    return constants.OutTriggerMode(__mode)


def set_enable_diasy_chain_clock_sync(enable: bool) -> None:
    """Enables clock sync over SATA daisy chain connectors. Primary board
    will start generating clock for secondary unit and so on.

    Parameters
    ----------
    enable
        Turns on the mode.

    """

    __status_code = rp.rp_SetEnableDiasyChainClockSync(enable)

    if __status_code != StatusCode.OK.value:
        raise RPPError(
            "rp_SetEnableDiasyChainClockSync", _to_debug(enable), __status_code
        )

    return


def get_enable_diasy_chain_clock_sync() -> bool:
    """ """

    __status_code, __state = rp.rp_GetEnableDiasyChainClockSync()

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_GetEnableDiasyChainClockSync", _to_debug(), __status_code)

    return __state


def apin_reset() -> None:
    """Sets analog outputs to default values (0V)."""

    __status_code = rp.rp_ApinReset()

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_ApinReset", _to_debug(), __status_code)

    return


def apin_get_value(
    pin: constants.AnalogPin, value: float, raw: int
) -> tuple[float, int]:
    """Gets value from analog pin in volts.

    Parameters
    ----------
    pin
        Analog pin.
    value
        Value on analog pin in volts
    raw
        raw value

    """

    __status_code, __value, __raw = rp.rp_ApinGetValue(pin.value, value, raw)

    if __status_code != StatusCode.OK.value:
        raise RPPError(
            "rp_ApinGetValue", _to_debug(pin.value, value, raw), __status_code
        )

    return __value, __raw


def apin_get_value_raw(pin: constants.AnalogPin) -> int:
    """Gets raw value from analog pin.

    Parameters
    ----------
    pin
        Analog pin.
    value
        Raw value on analog pin

    """

    __status_code, __value = rp.rp_ApinGetValueRaw(pin.value)

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_ApinGetValueRaw", _to_debug(pin.value), __status_code)

    return __value


def apin_set_value(pin: constants.AnalogPin, value: float) -> None:
    """Sets value in volts on analog output pin.

    Parameters
    ----------
    pin
        Analog output pin.
    value
        Value in volts to be set on given output pin.

    """

    __status_code = rp.rp_ApinSetValue(pin.value, value)

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_ApinSetValue", _to_debug(pin.value, value), __status_code)

    return


def apin_set_value_raw(pin: constants.AnalogPin, value: int) -> None:
    """Sets raw value on analog output pin.

    Parameters
    ----------
    pin
        Analog output pin.
    value
        Raw value to be set on given output pin.

    """

    __status_code = rp.rp_ApinSetValueRaw(pin.value, value)

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_ApinSetValueRaw", _to_debug(pin.value, value), __status_code)

    return


def apin_get_range(
    pin: constants.AnalogPin, min_val: float, max_val: float
) -> tuple[float, float]:
    """Gets range in volts on specific pin.

    Parameters
    ----------
    pin
        Analog input output pin.
    min_val
        Minimum value in volts on given pin.
    max_val
        Maximum value in volts on given pin.

    """

    __status_code, __min_val, __max_val = rp.rp_ApinGetRange(
        pin.value, min_val, max_val
    )

    if __status_code != StatusCode.OK.value:
        raise RPPError(
            "rp_ApinGetRange", _to_debug(pin.value, min_val, max_val), __status_code
        )

    return __min_val, __max_val


def ai_pin_get_value(pin: int, value: float, raw: int) -> tuple[float, int]:
    """Gets value from analog pin in volts.

    Parameters
    ----------
    pin
        pin index
    value
        voltage
    raw
        raw value

    """

    __status_code, __value, __raw = rp.rp_AIpinGetValue(pin, value, raw)

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_AIpinGetValue", _to_debug(pin, value, raw), __status_code)

    return __value, __raw


def ai_pin_get_value_raw(pin: int) -> int:
    """Gets raw value from analog pin.

    Parameters
    ----------
    pin
        pin index
    value
        raw 12 bit XADC value

    """

    __status_code, __value = rp.rp_AIpinGetValueRaw(pin)

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_AIpinGetValueRaw", _to_debug(pin), __status_code)

    return __value


def ao_pin_reset() -> None:
    """Sets analog outputs to default values (0V)."""

    __status_code = rp.rp_AOpinReset()

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_AOpinReset", _to_debug(), __status_code)

    return


def ao_pin_get_value(pin: int, value: float, raw: int) -> tuple[float, int]:
    """Gets value from analog pin in volts.

    Parameters
    ----------
    pin
        Analog output pin index.
    value
        Value on analog pin in volts
    raw
        Value on analog pin in raw

    """

    __status_code, __value, __raw = rp.rp_AOpinGetValue(pin, value, raw)

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_AOpinGetValue", _to_debug(pin, value, raw), __status_code)

    return __value, __raw


def ao_pin_get_value_raw(pin: int) -> int:
    """Gets raw value from analog pin.

    Parameters
    ----------
    pin
        Analog output pin index.
    value
        Raw value on analog pin

    """

    __status_code, __value = rp.rp_AOpinGetValueRaw(pin)

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_AOpinGetValueRaw", _to_debug(pin), __status_code)

    return __value


def ao_pin_set_value(pin: int, value: float) -> None:
    """Sets value in volts on analog output pin.

    Parameters
    ----------
    pin
        Analog output pin index.
    value
        Value in volts to be set on given output pin.

    """

    __status_code = rp.rp_AOpinSetValue(pin, value)

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_AOpinSetValue", _to_debug(pin, value), __status_code)

    return


def ao_pin_set_value_raw(pin: int, value: int) -> None:
    """Sets raw value on analog output pin.

    Parameters
    ----------
    pin
        Analog output pin index.
    value
        Raw value to be set on given output pin.

    """

    __status_code = rp.rp_AOpinSetValueRaw(pin, value)

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_AOpinSetValueRaw", _to_debug(pin, value), __status_code)

    return


def ao_pin_get_range(pin: int, min_val: float, max_val: float) -> tuple[float, float]:
    """Gets range in volts on specific pin.

    Parameters
    ----------
    pin
        Analog input output pin index.
    min_val
        Minimum value in volts on given pin.
    max_val
        Maximum value in volts on given pin.

    """

    __status_code, __min_val, __max_val = rp.rp_AOpinGetRange(pin, min_val, max_val)

    if __status_code != StatusCode.OK.value:
        raise RPPError(
            "rp_AOpinGetRange", _to_debug(pin, min_val, max_val), __status_code
        )

    return __min_val, __max_val


def get_pll_control_enable() -> bool:
    """Only works with Redpitaya 250-12 otherwise returns RP_NOTS

    Parameters
    ----------
    enable
        return current state.

    """

    __status_code, __enable = rp.rp_GetPllControlEnable()

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_GetPllControlEnable", _to_debug(), __status_code)

    return __enable


def set_pll_control_enable(enable: bool) -> None:
    """Only works with Redpitaya 250-12 otherwise returns RP_NOTS

    Parameters
    ----------
    enable
        Flag enabling PLL control.

    """

    __status_code = rp.rp_SetPllControlEnable(enable)

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_SetPllControlEnable", _to_debug(enable), __status_code)

    return


def get_pll_control_locked() -> bool:
    """Only works with Redpitaya 250-12 otherwise returns RP_NOTS

    Parameters
    ----------
    status
        Get current state.

    """

    __status_code, __status = rp.rp_GetPllControlLocked()

    if __status_code != StatusCode.OK.value:
        raise RPPError("rp_GetPllControlLocked", _to_debug(), __status_code)

    return __status
