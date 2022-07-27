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
"""Input handler of configuration files and web requests."""

# Third-Party Dependencies
import yaml as _yaml
import json as _json

# Local Dependencies
from governor.io.types import ConfigType as _ConfigType


class Config():
    """Configuration handler."""

    def __init__(self,
                 # Required inputs
                 id_: str,
                 source: str,
                 source_type: _ConfigType,
                 # Optional inputs
                 name: str = None):
        """Initialize a new configuration.

        Args:
            id_: Unique identifier of configuration
            source: Configuration content
            type: (Optional) Type of :source:
            name: (Optional) User-defined name of configuration
        """
        # Private vars by class args
        self._id = id_
        self._source = source
        self._source_type = source_type
        self._name = name

        # Private vars by init
        self._me = "Config():"
        self._config = None

    def load(self) -> bool:
        """Load configuration into memory.
        
        Returns:
            Flag if loading successful
        """
        try:
            if self._source_type == _ConfigType.YAML:
                with open(self._source, mode="r", encoding="UTF-8") as file:
                    self._config = _yaml.full_load(file)

            elif self._source_type == _ConfigType.JSON:
                with open(self._source, mode="r", encoding="UTF-8") as file:
                    self._config = _json.load(file)

            elif self._source_type == _ConfigType.JSON_STRING:
                self._config = _json.loads(self._source)
        
            return True
        
        except (
            FileNotFoundError,
            _yaml.YAMLError,
            _json.JSONDecodeError,
            OSError
        ) as err:
            pass
        except:
            pass
        
        return False

    @property
    def config(self) -> dict:
        """Raw configuration as dictionary."""
        return self._config
