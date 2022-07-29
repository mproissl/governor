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
"""Master controller of end-to-end runtime of operator networks."""

# Third-Party Dependencies
from typing import Union as _Union
from secrets import token_urlsafe as _token_urlsafe

# Local Dependencies
from governor.io import Config as _Config
from governor.io.types import ConfigType as _ConfigType
from governor.objects.network import Network as _Network
from governor.runtime.memory import Memory as _Memory

class Controller():
    """Controller of a network of operators."""

    def __init__(self,
                 # Required inputs
                 config: _Union(_Config, str, dict),
                ):
        """Initialize a new controller.

        Args:
            config: Configuration network operations and its operator nodes,
                    either in the form of an :_Config: object, string
                    path to either YAML or JSON files, or already in
                    dictionary format.
        """
        # Private vars
        self._me = "Controller():"
        self._config = None
        self._network = None
        self._memory = _Memory()

        # Load config
        self._load_configuration(config)

        # Create operator network
        self._create_network()

    def _load_configuration(self, config):
        """Load configuration provided by user."""

        # Load config directly
        if isinstance(config, _Config):
            self._config = config

        # Load dictionary config
        elif isinstance(config, dict):
            self._config = _Config(
                id_ = _token_urlsafe(16),
                source = config,
                source_type = _ConfigType.DICT
            )

        # Load string config
        elif isinstance(config, str):

            # Note: we implement this naive approach to ease
            # user experience as for advanced settings, one
            # is expected to pass a _Config object directly
            if ".yaml" in config.lower():
                source_type = _ConfigType.YAML
            elif ".json" in config.lower():
                source_type = _ConfigType.JSON
            else:
                source_type = _ConfigType.JSON_STRING

            self._config = _Config(
                id_ = _token_urlsafe(16),
                source = config,
                source_type = source_type
            )

        # Source configuration content (with validation)
        if not self._config.load():
            raise ImportError(f"{self._me} Failed importing configuration -> "\
                              f"{self._config.exception}")

    def _create_network(self):
        """Create operator network from configuration."""
        try:
            self._network = _Network(
                id_ = _token_urlsafe(16),
                config = self._config
            )
        # pylint: disable=broad-except
        except Exception as err:
            self._network = None
            raise ValueError(f"{self._me} Failed creating network from "\
                             f"configuration -> {err}") from err
        # pylint: enable=broad-except
