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
"""Webserver with headless or browser UI for control and monitoring."""

# Third-Party Dependencies
from typing import Union as _Union
from starlette.applications import Starlette as _Starlette
from starlette.middleware.cors import CORSMiddleware as _CORSMiddleware
import uvicorn as _uvicorn

# Local Dependencies
from governor.io import Config as _Config
from governor.runtime.api import API_ROUTES as _API_ROUTES
from governor.runtime.ui import UI_ROUTES as _UI_ROUTES


class Server():
    """Governor Server for API and UI interactions."""

    def __init__(self,
                 host: str = "127.0.0.1",
                 port: int = 8585,
                 controller_config: _Union[_Config, str, dict] = None):
        """Initialize a new server.

        Args:
            host: (Optional) Bind socket to this host.
                  [default: 127.0.0.1]
            port: (Optional) Bind socket to this port.
                  [default: 8585]
            controller_config: (Optional) Configuration of server,
                    network operations and its operator nodes, either
                    in the form of an :_Config: object, string path
                    to either YAML or JSON files, or already in
                    dictionary format.
        """
        # Private vars
        self._me = "Server():"
        self._host = host
        self._port = port
        self._controller_config = controller_config
        self._app = self._setup_app()

    def _setup_app(self) -> _Starlette:
        """Setup of application instance.

        Returns:
            Starlette instance
        """
        # Routes
        routes = _UI_ROUTES
        routes.extend(_API_ROUTES)

        # Create instance
        app = _Starlette(routes=routes)
        app.add_middleware(_CORSMiddleware, allow_origins=['*'])
        return app

    def run(self):
        """Run the server."""
        _uvicorn.run(
            self._app,
            host = self._host,
            port = self._port,
            reload = True)
