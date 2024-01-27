"""
    redpipy.constants
    ~~~~~~~~~~~~~~~~~

    original file: rp_enums.h and rp.h
    commit id: 1f7b7c35070dce637ac699d974d3648b45672f89

    :copyright: 2024 by redpipy Authors, see AUTHORS for more details.
    :license: BSD, see LICENSE for more details.
"""

import enum
from dataclasses import dataclass
from typing import Any

import rp

#############
# rp_enums.h
#############


class Pin(enum.Enum):
    """Type representing digital input output pins."""

    LED0 = rp.RP_LED0  #  LED 0
    LED1 = rp.RP_LED1  #  LED 1
    LED2 = rp.RP_LED2  #  LED 2
    LED3 = rp.RP_LED3  #  LED 3
    LED4 = rp.RP_LED4  #  LED 4
    LED5 = rp.RP_LED5  #  LED 5
    LED6 = rp.RP_LED6  #  LED 6
    LED7 = rp.RP_LED7  #  LED 7
    DIO0_P = rp.RP_DIO0_P  #  DIO_P 0
    DIO1_P = rp.RP_DIO1_P  #  DIO_P 1
    DIO2_P = rp.RP_DIO2_P  #  DIO_P 2
    DIO3_P = rp.RP_DIO3_P  #  DIO_P 3
    DIO4_P = rp.RP_DIO4_P  #  DIO_P 4
    DIO5_P = rp.RP_DIO5_P  #  DIO_P 5
    DIO6_P = rp.RP_DIO6_P  #  DIO_P 6
    DIO7_P = rp.RP_DIO7_P  #  DIO_P 7
    DIO0_N = rp.RP_DIO0_N  #  DIO_N 0
    DIO1_N = rp.RP_DIO1_N  #  DIO_N 1
    DIO2_N = rp.RP_DIO2_N  #  DIO_N 2
    DIO3_N = rp.RP_DIO3_N  #  DIO_N 3
    DIO4_N = rp.RP_DIO4_N  #  DIO_N 4
    DIO5_N = rp.RP_DIO5_N  #  DIO_N 5
    DIO6_N = rp.RP_DIO6_N  #  DIO_N 6
    DIO7_N = rp.RP_DIO7_N  #  DIO_N 7


class PinState(enum.Enum):
    """Type representing pin's high or low state (on/off)."""

    LOW = rp.RP_LOW  #  Low state 1:1
    HIGH = rp.RP_HIGH  # High state 1:20


class OutTriggerMode(enum.Enum):
    """Type representing pin's high or low state (on/off).
    # TODO: this is wrong
    """

    ADC = 0  #  ADC trigger
    DAC = 1  #  DAC trigger


class PinDirection(enum.Enum):
    """Type representing pin's input or output direction."""

    IN = rp.RP_IN  #  Input direction
    OUT = rp.RP_OUT  #  Output direction


class AnalogPin(enum.Enum):
    """Type representing analog input output pins."""

    OUT0 = rp.RP_AOUT0  #  Analog output 0
    OUT1 = rp.RP_AOUT1  #  Analog output 1
    OUT2 = rp.RP_AOUT2  #  Analog output 2
    OU3 = rp.RP_AOUT3  #  Analog output 3
    IN0 = rp.RP_AIN0  #  Analog input 0
    IN1 = rp.RP_AIN1  #  Analog input 1
    IN2 = rp.RP_AIN2  #  Analog input 2
    IN3 = rp.RP_AIN3  #  Analog input 3


class Waveform(enum.Enum):
    SINE = rp.RP_WAVEFORM_SINE  #  Wave form sine
    SQUARE = rp.RP_WAVEFORM_SQUARE  #  Wave form square
    TRIANGLE = rp.RP_WAVEFORM_TRIANGLE  #  Wave form triangle
    RAMP_UP = rp.RP_WAVEFORM_RAMP_UP  #  Wave form sawtooth (/|)
    RAMP_DOWN = rp.RP_WAVEFORM_RAMP_DOWN  #  Wave form reversed sawtooth (|\)
    DC = rp.RP_WAVEFORM_DC  #  Wave form dc
    PWM = rp.RP_WAVEFORM_PWM  #  Wave form pwm
    ARBITRARY = rp.RP_WAVEFORM_ARBITRARY  #  Use defined wave form
    DC_NEG = rp.RP_WAVEFORM_DC_NEG  #  Wave form negative dc
    SWEEP = rp.RP_WAVEFORM_SWEEP  #  Wave form sweep


class GenMode(enum.Enum):
    #  Continuous signal generation
    CONTINUOUS = rp.RP_GEN_MODE_CONTINUOUS
    #  Signal is generated N times, wher N is defined with rp_GenBurstCount method
    BURST = rp.RP_GEN_MODE_BURST
    #  User can continuously write data to buffer
    STREAM = rp.RP_GEN_MODE_STREAM


class GenSweepDirection(enum.Enum):
    #  Generate sweep signal from start frequency to end frequency
    NORMAL = rp.RP_GEN_SWEEP_DIR_NORMAL
    #  Generate sweep signal from start frequency to end frequency
    #  and back to start frequency
    UP_DOWN = rp.RP_GEN_SWEEP_DIR_UP_DOWN


class GenSweepMode(enum.Enum):
    LINEAR = rp.RP_GEN_SWEEP_MODE_LINEAR  #  Generate sweep signal in linear mode
    LOG = rp.RP_GEN_SWEEP_MODE_LOG  #  Generate sweep signal in log mode


class TriggerSource(enum.Enum):
    INTERNAL = 1  #  Internal trigger source
    EXT_PE = 2  #  External trigger source positive edge
    EXT_NE = 3  #  External trigger source negative edge


class GenGain(enum.Enum):
    X1 = 0  #  Set output gain in x1 mode
    X5 = 1  #  Set output gain in x5 mode


class Channel(enum.Enum):
    """Type representing Input/Output channels."""

    CH_1 = 0  #  Channel A
    CH_2 = 1  #  Channel B
    CH_3 = 2  #  Channel C
    CH_4 = 3  #  Channel D


class TriggerChannel(enum.Enum):
    """Type representing Input/Output channels in trigger."""

    CH_1 = 0  #  Channel A
    CH_2 = 1  #  Channel B
    CH_3 = 2  #  Channel C
    CH_4 = 3  #  Channel D
    CH_EXT = 4


class EqFilterCoefficient(enum.Enum):
    """The type represents the names of the coefficients in the filter."""

    AA = rp.AA  #  AA
    BB = rp.BB  #  BB
    PP = rp.PP  #  PP
    KK = rp.KK  #  KK


# typedef struct
# {
#     uint8_t channels;
#     uint32_t size;
#     bool     use_calib_for_raw;
#     bool     use_calib_for_volts;
#     int16_t  *ch_i[4];
#     double   *ch_d[4];
#     float    *ch_f[4];
# } buffers_t;


class Decimation(enum.Enum):
    """Type representing decimation used at acquiring signal."""

    DEC_1 = 1  #  Decimation 1
    DEC_2 = 2  #  Decimation 2
    DEC_4 = 4  #  Decimation 4
    DEC_8 = 8  #  Decimation 8
    DEC_16 = 16  #  Decimation 16
    DEC_32 = 32  #  Decimation 32
    DEC_64 = 64  #  Decimation 64
    DEC_128 = 128  #  Decimation 128
    DEC_256 = 256  #  Decimation 256
    DEC_512 = 512  #  Decimation 512
    DEC_1024 = 1024  #  Decimation 1024
    DEC_2048 = 2048  #  Decimation 2048
    DEC_4096 = 4096  #  Decimation 4096
    DEC_8192 = 8192  #  Decimation 8192
    DEC_16384 = 16384  #  Decimation 16384
    DEC_32768 = 32768  #  Decimation 32768
    DEC_65536 = 65536  #  Decimation 65536


class AcqMode(enum.Enum):
    DC = (0,)
    AC = 1


class AcqTriggerSource(enum.Enum):
    """Type representing different trigger sources used at acquiring signal."""

    DISABLED = 0  #  Trigger is disabled
    NOW = 1  #  Trigger triggered now (immediately)
    CHA_PE = 2  #  Trigger set to Channel A threshold positive edge
    CHA_NE = 3  #  Trigger set to Channel A threshold negative edge
    CHB_PE = 4  #  Trigger set to Channel B threshold positive edge
    CHB_NE = 5  #  Trigger set to Channel B threshold negative edge
    EXT_PE = 6  #  Trigger set to external trigger positive edge (DIO0_P pin)
    EXT_NE = 7  #  Trigger set to external trigger negative edge (DIO0_P pin)
    AWG_PE = 8  #  Trigger set to arbitrary wave Gen application positive edge
    AWG_NE = 9  #  Trigger set to arbitrary wave Gen application negative edge
    CHC_PE = 10  #  Trigger set to Channel C threshold positive edge
    CHC_NE = 11  #  Trigger set to Channel C threshold negative edge
    CHD_PE = 12  #  Trigger set to Channel D threshold positive edge
    CHD_NE = 13  #  Trigger set to Channel D threshold negative edge


class AcqTriggerState(enum.Enum):
    """Type representing different trigger states."""

    #  Trigger is triggered/disabled
    TRIGGERED = rp.RP_TRIG_STATE_TRIGGERED
    #  Trigger is set up and waiting (to be triggered)
    WAITING = rp.RP_TRIG_STATE_WAITING


#############
# rp.h
#############

ADC_BUFFER_SIZE = int(16 * 1024)
DAC_BUFFER_SIZE = int(16 * 1024)
SPECTR_OUT_SIG_LEN = int(2 * 1024)


RISE_FALL_MIN_RATIO = 0.0001  # ratio of rise/fall time to period
RISE_FALL_MAX_RATIO = 0.1

############################################
# Various error codes returned by the API.
############################################


class StatusCode(enum.Enum):
    OK = rp.RP_OK
    EOED = rp.RP_EOED
    EOMD = rp.RP_EOMD
    ECMD = rp.RP_ECMD
    EMMD = rp.RP_EMMD
    EUMD = rp.RP_EUMD
    EOOR = rp.RP_EOOR
    ELID = rp.RP_ELID
    EMRO = rp.RP_EMRO
    EWIP = rp.RP_EWIP
    EPN = rp.RP_EPN
    UIA = rp.RP_UIA
    FCA = rp.RP_FCA
    RCA = rp.RP_RCA
    BTS = rp.RP_BTS
    EIPV = rp.RP_EIPV
    EUF = rp.RP_EUF
    ENN = rp.RP_ENN
    EFOB = rp.RP_EFOB
    EFCB = rp.RP_EFCB
    EABA = rp.RP_EABA
    EFRB = rp.RP_EFRB
    EFWB = rp.RP_EFWB
    EMNC = rp.RP_EMNC
    NOTS = rp.RP_NOTS


def get_status_message(code: StatusCode) -> str:
    if code == StatusCode.OK:
        return "Success"
    elif code == StatusCode.EOED:
        return "Failed to Open EEPROM Device"
    elif code == StatusCode.EOMD:
        return "Failed to Open Memory Device"
    elif code == StatusCode.ECMD:
        return "Failed to Close Memory Device"
    elif code == StatusCode.EMMD:
        return "Failed to Map Memory Device"
    elif code == StatusCode.EUMD:
        return "Failed to Unmap Memory Device"
    elif code == StatusCode.EOOR:
        return "Value Out Of Range"
    elif code == StatusCode.ELID:
        return "LED Input Direction is not valid"
    elif code == StatusCode.EMRO:
        return "Modifying Read Only field"
    elif code == StatusCode.EWIP:
        return "Writing to Input Pin is not valid"
    elif code == StatusCode.EPN:
        return "Invalid Pin number"
    elif code == StatusCode.UIA:
        return "Uninitialized Input Argument"
    elif code == StatusCode.FCA:
        return "Failed to Find Calibration Parameters"
    elif code == StatusCode.RCA:
        return "Failed to Read Calibration Parameters"
    elif code == StatusCode.BTS:
        return "Buffer too small"
    elif code == StatusCode.EIPV:
        return "Invalid parameter value"
    elif code == StatusCode.EUF:
        return "Unsupported Feature"
    elif code == StatusCode.ENN:
        return "Data not normalized"
    elif code == StatusCode.EFOB:
        return "Failed to open bus"
    elif code == StatusCode.EFCB:
        return "Failed to close bus"
    elif code == StatusCode.EABA:
        return "Failed to acquire bus access"
    elif code == StatusCode.EFRB:
        return "Failed to read from the bus"
    elif code == StatusCode.EFWB:
        return "Failed to write to the bus"
    elif code == StatusCode.EMNC:
        return "Extension module not connected"
    elif code == StatusCode.NOTS:
        return "Command not supported"
    else:
        return "Unknown error {code}"


@dataclass(frozen=True)
class RPPError(Exception):
    function: str
    arguments: Any
    status_code: StatusCode

    def __str__(self) -> str:
        return (
            f"While calling {self.function} with arguments {self.arguments}: "
            f"{get_status_message(self.status_code)} ({self.status_code.value}))"
        )
