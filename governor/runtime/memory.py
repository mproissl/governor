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
"""Memory handler of shared and dedicated data in memory."""

# Third-Party Dependencies
from copy import deepcopy as _deepcopy
from datetime import datetime as _datetime


class Memory():
    """Memory of a network of operators."""

    def __init__(self):
        """Initialize a new memory block."""

        # Private vars
        self._me = "Memory():"
        self._shared = self._Shared()
        self._dedicated = self._Dedicated()
        self._shared_last_accessed = ""
        self._dedicated_last_accessed = ""

    @property
    def shared(self):
        """Access to shared memory."""
        self._shared_last_accessed = \
            _datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        return self._shared

    @property
    def dedicated(self):
        """Access to dedicated memory."""
        self._dedicated_last_accessed = \
            _datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        return self._shared

    @property
    def shared_last_accessed(self):
        """Date of last access to shared memory."""
        return self._shared_last_accessed

    @property
    def dedicated_last_accessed(self):
        """Date of last access to dedicated memory."""
        return self._dedicated_last_accessed

    class _Shared():
        """Shared data handler.

        Note:
            This version considers future upgrades. For now,
            we keep it simple and while having the API ready
            for extensions. Moreover, the controller is
            responsible for uniqueness of access IDs, thus
            we skip any response in case of error here.
        """

        def __init__(self):
            """Initialize shared memory."""
            self._data = {}

        def exists(self, id_: str) -> bool:
            """Boolean flag if identifier in memory.

            Args:
                id_: Unique identifier of data
            """
            return id_ in self._data

        def add(self, id_: str, data: any):
            """Add new data given its identifier.

            Args:
                id_: Unique identifier of data
                data: Any data structure
            """
            if id_ not in self._data:
                self._data[id_] = {
                    id_: data
                }

        def get(self, id_: str, deepcopy: bool = False) -> any:
            """Get data given its identifier.

            Args:
                id_: Unique identifier of data
                deepcopy: (Optional) Return copy of data

            Returns:
                Data object or None if it does not exist
            """
            if id_ not in self._data:
                return None
            elif not deepcopy:
                return self._data[id_][id_]
            else:
                return _deepcopy(self._data[id_][id_])

        def get_modifiable(self, id_: str) -> dict:
            """Get modifiable data given its identifier.

            Args:
                id_: Unique identifier of data

            Returns:
                Dictionary of data object
            """
            if id_ not in self._data:
                return None
            else:
                return self._data[id_]

        def update(self, id_: str, data: any, create: bool = False):
            """Update existing data given its identifier.

            Args:
                id_: Unique identifier of data
                data: Any data structure
                create: (Optional) Flag to create if id_ does not exist
            """
            if id_ in self._data:
                self._data[id_][id_] = data
            elif create:
                self.add(id_, data)

        def remove(self, id_: str):
            """Remove existing data given its identifier.

            Args:
                id_: Unique identifier of data
            """
            if id_ in self._data:
                del self._data[id_]

    class _Dedicated():
        """Dedicated data handler.

        Note:
            This version considers future upgrades. For now,
            we keep it simple and while having the API ready
            for extensions. Moreover, the controller is
            responsible for uniqueness of access IDs, thus
            we skip any response in case of error here.
        """

        def __init__(self):
            """Initialize dedicated memory."""
            self._data = {}

        def add(self, owner: str, id_: str, data: any):
            """Add new data given its owner and identifier.

            Args:
                owner: Owner of data
                id_: Unique identifier of data
                data: Any data structure
            """
            if owner not in self._data:
                self._data[owner] = {}
            if id_ not in self._data[owner]:
                self._data[owner][id_] = data

        def get(self, owner: str, id_: str, deepcopy: bool = False) -> any:
            """Get data given its owner and identifier.

            Args:
                owner: Owner of data
                id_: Unique identifier of data
                deepcopy: (Optional) Return copy of data

            Returns:
                Data object or None if it does not exist
            """
            if owner not in self._data:
                return None
            if id_ not in self._data[owner]:
                return None
            elif not deepcopy:
                return self._data[owner][id_]
            else:
                return _deepcopy(self._data[owner][id_])

        def update(self, owner: str, id_: str, data: any):
            """Update existing data given its owner and identifier.

            Args:
                owner: Owner of data
                id_: Unique identifier of data
                data: Any data structure
            """
            if owner in self._data:
                if id_ in self._data[owner]:
                    self._data[owner][id_] = data

        def remove(self, owner: str, id_: str):
            """Remove existing data given its owner and identifier.

            Args:
                owner: Owner of data
                id_: Unique identifier of data
            """
            if owner in self._data:
                if id_ in self._data[owner]:
                    del self._data[owner][id_]

        def remove_owner(self, owner: str):
            """Remove all existing data belonging to an owner.

            Args:
                owner: Owner of data
            """
            if owner in self._data:
                del self._data[owner]
