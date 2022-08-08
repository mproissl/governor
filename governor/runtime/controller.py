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
from governor.io import ConfigWrapper as _ConfigWrapper
from governor.io import ConfigReader as _ConfigReader
from governor.io.types import ConfigType as _ConfigType
from governor.io.types import get_config_values as _get_config_values
from governor.objects.network import Network as _Network
from governor.objects.operator import Operator as _Operator, OperatorSettings as _OperatorSettings
from governor.runtime.memory import Memory as _Memory

class Controller():
    """Controller of a network of operators."""

    def __init__(self,
                 # Required inputs
                 config: _Union[_Config, str, dict],
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
        self._parallelize = False
        self._executed = []

        # Helper
        self._operator_defaults = _get_config_values(
            "config_payload_operator_parameters()",
            "default")

        # Load config
        self._load_configuration(config)

        # Create operator network
        self._create_network()

        # Process header
        self._process_header()

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

        # Keep only wrapper for access
        self._config = _ConfigWrapper(self._config)

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

    def _process_header(self):
        """Process header instructions in configuration."""

        # Add shared data to memory
        shared_data = self._config.header_shared_data
        if shared_data is not None:
            for id_ in shared_data:
                self._memory.shared.add(id_, shared_data[id_])

        # Prepare to parallelize (TODO: prep mp)
        self._parallelize = self._config.header_enable_multiprocessing

    def run(self):
        """Run operator network based on user configuration."""

        # Sequential execution
        #if not self._parallelize:
        self._run_sequential()

    def _run_sequential(self):
        """Run operators in sequential order disregarding network
           architecture.
        """
        # TODO Add controller instructions here (own class)
        for id_ in self._network.operator_sequence():

            # Config
            cfg = _ConfigReader(config = self._network.operators[id_],
                                defaults = self._operator_defaults)

            # Repeat
            runs = cfg.repeat

            # Variations
            # TODO

            # Save
            save = None
            if cfg.save_output:
                if cfg.shared_output_name is not None:
                    save = cfg.shared_output_name
                else:
                    save = id_

            # Operator
            operator = self._get_operator(id_)

            # Run
            while runs > 0:
                if save is None:
                    _ = operator.run().response
                else:
                    self._memory.shared.update(id_, operator.run().response,\
                                               create=True)

                # Log
                self._executed.append(id_)
                runs -= 1

    def _get_operator(self, id_: str) -> _Operator:
        """Retrieve operator by given identifier.

        Args:
            id_: Operator ID

        Returns:
            Operator object
        """
        # Existing operator
        # TODO
        # return X

        # New operator
        cfg = self._network.operators[id_]
        return _Operator(
            **_OperatorSettings(cfg).settings\
            .update({ "input_params": self._compile_input_params(cfg)})
        )

    def _compile_input_params(self, cfg: _ConfigReader) -> dict:
        """Compile dedicated and shared input parameters.

        Args:
            cfg: Operator configuration reader

        Returns:
            Dictionary of compiled input parameters
        """
        # Vars
        input_params = {}

        # Dedicated inputs
        if cfg.exists("dedicated_input_params"):
            input_params.update(cfg.dedicated_input_params)

        # Shared inputs
        if cfg.exists("shared_input_params"):
            input_ = cfg.shared_input_params
            if isinstance(input_, str):
                if self._memory.shared.exists(input_):
                    input_params[input_] = self._memory.shared.get(input_)
                else:
                    raise MemoryError(f"{self._me} Shared input parameter "\
                                      f"{input_} does not exist in memory.")

            elif isinstance(input_, list):
                for name_ in input_:
                    if isinstance(name_, str):
                        if self._memory.shared.exists(name_):
                            input_params[name_] = self._memory.shared.get(name_)
                        else:
                            raise MemoryError(
                                f"{self._me} Shared input parameter "\
                                f"{name_} does not exist in memory.")
                    else:
                        raise ValueError(
                                f"{self._me} Shared input parameter "\
                                f"{name_} is not a String.")

            elif isinstance(input_, dict):
                for name_ in input_:
                    if isinstance(name_, str):
                        if not self._memory.shared.exists(name_):
                            self._memory.shared.add(name_, input_[name_])
                            input_params[name_] = self._memory.shared.get(name_)
                        else:
                            input_params[name_] = self._memory.shared.get(name_)
                            if cfg.exists("shared_input_init_only"):
                                if cfg.shared_input_init_only:
                                    raise ValueError(
                                        f"{self._me} Shared input parameter "\
                                        f"{name_} already exists in memory.")
                    else:
                        raise ValueError(
                                f"{self._me} Shared input parameter "\
                                f"{name_} is not a String.")

        return input_params
