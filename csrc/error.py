"""
    redpipy.error
    ~~~~~~~~~~~~~

    Classes and methods for exception handling.

    :copyright: 2024 by redpipy Authors, see AUTHORS for more details.
    :license: BSD, see LICENSE for more details.
"""

from dataclasses import dataclass
from typing import Any

from .constants import StatusCode


def get_status_message(code: StatusCode | int) -> str:
    try:
        code = StatusCode(code)
    except ValueError:
        return "Unknown error {code}"

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
    status_code_value: int

    def __str__(self) -> str:
        err_msg = get_status_message(self.status_code_value)

        return (
            f"While calling {self.function} with arguments {self.arguments}: "
            f"{err_msg} ({self.status_code_value}))"
        )
