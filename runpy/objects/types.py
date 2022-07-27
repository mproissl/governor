# MIT License
#
# Copyright (c) 2022 Manuel Proissl
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
"""Common type definitions used by operators and graphs."""

# Dependencies
from enum import Enum as _Enum, unique as _unique


@_unique
class OperatorState(_Enum):
    """Operator state types."""
    ERROR = -1
    OFFLINE = 0
    ONLINE = 1
    COMPLETED = 2


def operator_state_description():
    """Operator state descriptions."""
    return {
        OperatorState.ERROR: "Operator execution failed.",
        OperatorState.OFFLINE: "Operator is not running.",
        OperatorState.ONLINE: "Operator is running.",
        OperatorState.COMPLETED: "Operator execution completed."
    }
