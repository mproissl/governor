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
"""Collection of useful helper methods."""

# Third-Party Dependencies
from typing import Union as _Union


def string_splitter(string_object: str,
                    delimiter: str,
                    return_index: int = -1) -> _Union[list, str]:
    """Split a string given delimiter and optional return_index.

    Note:
        If delimiter or return_index is not valid, None is returned.

    Args:
        string_object: A string
        delimiter: A sub-string to split the string_object
        return_index: (Optional) Index of sub-string to return

    Returns:
        List of splitted sub-strings or single sub-string or None
    """
    # Vars
    string_object_splitted = None

    # Split
    if delimiter.lower() in string_object:
        string_object_splitted = string_object.split(delimiter.lower())
    elif delimiter.upper() in string_object:
        string_object_splitted = string_object.split(delimiter.upper())

    # Return
    if string_object_splitted is not None:
        if (return_index >=0 and len(string_object_splitted) >=return_index+1):
            return string_object_splitted[return_index].strip()
        else:
            return string_object_splitted

    return None


def strings_contain_whitespace(*strings) -> tuple:
    """Flag string arguments containing whitespace.

    Args:
        strings: String arguments

    Returns:
        Tuple with boolean if whitespace found and stripped string list
    """
    # Vars
    strings_ = []
    has_whitespace = False

    # Check
    for s in strings:
        if " " in s:
            has_whitespace = True
        strings_.append(str(s).strip())

    return strings_, has_whitespace
