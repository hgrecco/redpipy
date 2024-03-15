# type: ignore
"""
    redpipy.constants
    ~~~~~~~~~~~~~~~~~

    We need to ignore types as we do not have typing for rp constants.

    original file: rp_enums.h and rp.h
    commit id: 1f7b7c35070dce637ac699d974d3648b45672f89

    :copyright: 2024 by redpipy Authors, see AUTHORS for more details.
    :license: BSD, see LICENSE for more details.
"""
from __future__ import annotations

import enum

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

    ADC = rp.OUT_TR_ADC  #  ADC trigger
    DAC = rp.OUT_TR_DAC  #  DAC trigger


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
    INTERNAL = rp.RP_GEN_TRIG_SRC_INTERNAL  #  Internal trigger source
    EXT_PE = rp.RP_GEN_TRIG_SRC_EXT_PE  #  External trigger source positive edge
    EXT_NE = rp.RP_GEN_TRIG_SRC_EXT_NE  #  External trigger source negative edge


class GenGain(enum.Enum):
    X1 = rp.RP_GAIN_1X  #  Set output gain in x1 mode
    X5 = rp.RP_GAIN_5X  #  Set output gain in x5 mode


class Channel(enum.Enum):
    """Type representing Input/Output channels."""

    CH_1 = rp.RP_CH_1  #  Channel A
    CH_2 = rp.RP_CH_2  #  Channel B
    CH_3 = rp.RP_CH_3  #  Channel C
    CH_4 = rp.RP_CH_4  #  Channel D


class TriggerChannel(enum.Enum):
    """Type representing Input/Output channels in trigger."""

    CH_1 = rp.RP_T_CH_1  #  Channel A
    CH_2 = rp.RP_T_CH_2  #  Channel B
    CH_3 = rp.RP_T_CH_3  #  Channel C
    CH_4 = rp.RP_T_CH_4  #  Channel D
    CH_EXT = rp.RP_T_CH_EXT


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

    DEC_1 = rp.RP_DEC_1  #  Decimation 1
    DEC_2 = rp.RP_DEC_2  #  Decimation 2
    DEC_4 = rp.RP_DEC_4  #  Decimation 4
    DEC_8 = rp.RP_DEC_8  #  Decimation 8
    DEC_16 = rp.RP_DEC_16  #  Decimation 16
    DEC_32 = rp.RP_DEC_32  #  Decimation 32
    DEC_64 = rp.RP_DEC_64  #  Decimation 64
    DEC_128 = rp.RP_DEC_128  #  Decimation 128
    DEC_256 = rp.RP_DEC_256  #  Decimation 256
    DEC_512 = rp.RP_DEC_512  #  Decimation 512
    DEC_1024 = rp.RP_DEC_1024  #  Decimation 1024
    DEC_2048 = rp.RP_DEC_2048  #  Decimation 2048
    DEC_4096 = rp.RP_DEC_4096  #  Decimation 4096
    DEC_8192 = rp.RP_DEC_8192  #  Decimation 8192
    DEC_16384 = rp.RP_DEC_16384  #  Decimation 16384
    DEC_32768 = rp.RP_DEC_32768  #  Decimation 32768
    DEC_65536 = rp.RP_DEC_65536  #  Decimation 65536


class AcqMode(enum.Enum):
    DC = rp.RP_DC
    AC = rp.RP_AC


class AcqTriggerSource(enum.Enum):
    """Type representing different trigger sources used at acquiring signal."""

    DISABLED = rp.RP_TRIG_SRC_DISABLED  #  Trigger is disabled
    NOW = rp.RP_TRIG_SRC_NOW  #  Trigger triggered now (immediately)
    CHA_PE = rp.RP_TRIG_SRC_CHA_PE  #  Trigger set to Channel A threshold positive edge
    CHA_NE = rp.RP_TRIG_SRC_CHA_NE  #  Trigger set to Channel A threshold negative edge
    CHB_PE = rp.RP_TRIG_SRC_CHB_PE  #  Trigger set to Channel B threshold positive edge
    CHB_NE = rp.RP_TRIG_SRC_CHB_NE  #  Trigger set to Channel B threshold negative edge
    EXT_PE = (
        rp.RP_TRIG_SRC_EXT_PE
    )  #  Trigger set to external trigger positive edge (DIO0_P pin)
    EXT_NE = (
        rp.RP_TRIG_SRC_EXT_NE
    )  #  Trigger set to external trigger negative edge (DIO0_P pin)
    AWG_PE = (
        rp.RP_TRIG_SRC_AWG_PE
    )  #  Trigger set to arbitrary wave Gen application positive edge
    AWG_NE = (
        rp.RP_TRIG_SRC_AWG_NE
    )  #  Trigger set to arbitrary wave Gen application negative edge
    CHC_PE = rp.RP_TRIG_SRC_CHC_PE  #  Trigger set to Channel C threshold positive edge
    CHC_NE = rp.RP_TRIG_SRC_CHC_NE  #  Trigger set to Channel C threshold negative edge
    CHD_PE = rp.RP_TRIG_SRC_CHD_PE  #  Trigger set to Channel D threshold positive edge
    CHD_NE = rp.RP_TRIG_SRC_CHD_NE  #  Trigger set to Channel D threshold negative edge


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
