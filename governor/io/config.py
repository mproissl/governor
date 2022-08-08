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
from typing import Union as _Union

# Local Dependencies
from governor.io.types import ConfigType as _ConfigType
from governor.io.types import config_header_parameters as _config_header_parameters
from governor.io.types import config_payload_operator_parameters as _config_payload_operator_parameters
from governor.io.types import config_payload_variation_parameters as _config_payload_variation_parameters


class Config():
    """Configuration handler."""

    def __init__(self,
                 # Required inputs
                 id_: str,
                 source: _Union[str, dict],
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
        self._exception = ""

    @property
    def config(self) -> dict:
        """Exception message."""
        return self._config

    @property
    def exception(self) -> str:
        """Raw configuration as dictionary."""
        return self._exception

    def load(self) -> bool:
        """Load and validate configuration.

        Returns:
            Flag if loading successful
        """
        # Reset
        self._config = None
        self._exception = ""

        try:
            # Load config
            if self._source_type == _ConfigType.YAML:
                with open(self._source, mode="r", encoding="UTF-8") as file:
                    self._config = _yaml.full_load(file)

            elif self._source_type == _ConfigType.JSON:
                with open(self._source, mode="r", encoding="UTF-8") as file:
                    self._config = _json.load(file)

            elif self._source_type == _ConfigType.JSON_STRING:
                self._config = _json.loads(self._source)

            elif (self._source_type == _ConfigType.DICT and
                  isinstance(self._source, dict)):
                self._config = self._source
                self._source = "self._config"

            # Validate config
            self._validate()

            return True

        # pylint: disable=broad-except
        except (
            FileNotFoundError,
            _yaml.YAMLError,
            _json.JSONDecodeError,
            OSError,
            ValueError,
            TypeError,
            Exception
        ) as err:
            self._exception = repr(err).replace("\n", " ")
            self._config = None
            pass
        # pylint: enable=broad-except

        return False

    def _validate(self):
        """Validate loaded configuration."""

        # Config is dictionary
        if not isinstance(self._config, dict):
            raise ValueError(f"{self._me} Loaded config has the wrong format.")

        # Header key exists
        if "header" not in self._config:
            raise ValueError(f"{self._me} Header specification missing.")

        # Header is dictionary
        if not isinstance(self._config["header"], dict):
            raise ValueError(f"{self._me} Header does not comply with the "\
                             f"right format. Please check the documentation.")

        # Header is not empty
        if not self._config["header"]:
            raise ValueError(f"{self._me} Header is empty. Please provide "\
                             f"at least a name.")

        # Header contains known settings
        if (not all(key in _config_header_parameters()
            for key in self._config["header"].keys())):
            keys = ", ".join(_config_header_parameters().keys())
            raise ValueError(f"{self._me} Header contains unknown settings. "\
                             f"Only the following are supported: {keys}")

        # Header settings are of correct type
        if (not all(isinstance(self._config["header"][key],
                               _config_header_parameters()[key]["dtype"])
            for key in self._config["header"].keys())):
            raise ValueError(f"{self._me} Header contains settings of "\
                             f"incorrect type. Please review the docs.")

        # Payload key exists
        if "payload" not in self._config:
            raise ValueError(f"{self._me} Payload specification missing.")

        # Payload is dictionary
        if not isinstance(self._config["payload"], dict):
            raise ValueError(f"{self._me} Payload does not comply with the "\
                             f"right format. Please check the documentation.")

        # Operators in payload exist
        if "operators" not in self._config["payload"]:
            raise ValueError(f"{self._me} Operators in payload "\
                             f"specification missing.")

        # Operators is a list
        if not isinstance(self._config["payload"]["operators"], list):
            raise ValueError(f"{self._me} Operators does not comply with the "\
                             f"right format. Please check the documentation.")

        # Operators list not empty
        if len(self._config["payload"]["operators"]) == 0:
            raise ValueError(f"{self._me} Operators list is empty. Please "\
                             f"add at least one operator.")

        # Operators contain known settings
        user_ids = []
        for idx_, operator_ in enumerate(self._config["payload"]["operators"]):

            # Operator is dictionary
            if not isinstance(operator_, dict):
                raise ValueError(f"{self._me} Operator at index {idx_} does "\
                                 f"not comply with the right format. "\
                                 f"Please check the documentation.")

            # Operator contains known settings
            if (not all(key in _config_payload_operator_parameters()
                for key in operator_.keys())):
                keys = ", ".join(_config_payload_operator_parameters().keys())
                raise ValueError(f"{self._me} Operator at index {idx_} "\
                                 f"contains unknown settings. Only the "\
                                 f"following are supported: {keys}")

            # Operator settings are of correct type
            if (not all(isinstance(operator_[key],
                        _config_payload_operator_parameters()[key]["dtype"])
                for key in operator_.keys())):
                raise ValueError(f"{self._me} Operator at index {idx_} "\
                                 f"contains settings of incorrect type. "\
                                 f"Please review the docs.")

            # Operator run_after setting not at first
            # TODO

            # Collect operator IDs for uniqueness check
            if "id_" in operator_:
                user_ids.append(operator_["id_"])

            # Collect run_after IDs for existence test
            # TODO

        # Operators contain unique user-defined IDs
        if len(user_ids) != len(set(user_ids)):
            raise ValueError(f"{self._me} Operators contain duplicate id_ "\
                             f"values. Please make them unqiue.")

        # Variation checks
        if "variations" in self._config["payload"]:

            # Variation is dictionary
            if not isinstance(self._config["payload"]["variations"], dict):
                raise ValueError(f"{self._me} Variations does not comply "\
                                 f"with the right format. Please check "\
                                 f"the documentation.")

            # Variation contains known settings
            if (not all(key in _config_payload_variation_parameters()
                for key in self._config["payload"]["variations"].keys())):
                keys = ", ".join(_config_payload_variation_parameters().keys())
                raise ValueError(f"{self._me} Variations contains unknown "\
                                 f"settings. Only the following are "\
                                 f"supported: {keys}")

            # Variation settings are of correct type
            # TODO

            # Variation repeat_groups contains known groups
            # TODO

class ConfigWrapper():
    """Simple Convenience Wrapper of Configuration."""

    def __init__(self, config: Config):
        """Initialize a new configuration wrapper.

        Note:
            Exposed properties are limited to only the
            most used features.

        Args:
            config: Configuration from governor.io.Config()
        """
        # Private vars
        self._me = "ConfigWrapper():"
        self._config = config

        # Load if not loaded
        if self._config.config is None:
            if not self._config.load():
                raise ImportError(f"{self._me} Failed importing "\
                                  f"configuration -> "\
                                  f"{self._config.exception}")

        # Reduce to config only
        self._config = self._config.config

    @property
    def header(self):
        return self._config["header"]

    @property
    def payload(self):
        return self._config["payload"]

    @property
    def operators(self):
        return self._config["payload"]["operators"]

    @property
    def variations(self):
        if "variations" in self._config["payload"]:
            return self._config["payload"]["variations"]
        return None

    @property
    def header_shared_data(self):
        if "shared_data" in self.header:
            return self.header["shared_data"]
        return _config_header_parameters()["shared_data"]["default"]

    @property
    def header_enable_multiprocessing(self):
        if "enable_multiprocessing" in self.header:
            return self.header["enable_multiprocessing"]
        return _config_header_parameters()["enable_multiprocessing"]["default"]


class ConfigReader():
    """Reader of Dictionary in Configuration."""

    def __init__(self, config: dict, defaults: dict = None):
        """Initialize a new configuration reader.

        Args:
            config: Any configuration in dictionary form
            defaults: (Optional) Dictionary of default values
        """
        for key in config:
            setattr(self, key, config[key])
        if defaults is not None:
            for key in defaults:
                if key not in config:
                    setattr(self, key, defaults[key])

    def exists(self, attribute: str) -> bool:
        """Check if class contains attribute of given name.

        Args:
            attribute: Name of attribute

        Returns:
            Boolean flag
        """
        return hasattr(self, attribute)
        #try:
        #    _ = getattr(self, attribute)
        #except AttributeError:
        #    return False
        #return True

    def get(self, attribute: str) -> any:
        """Return attribute value by given name."""
        return getattr(self, attribute)
