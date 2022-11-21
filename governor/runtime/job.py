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
"""Abstraction of jobs for different runtimes."""

# Local Dependencies
from governor.objects.operator import Operator as _Operator
from governor.io import ConfigReader as _ConfigReader


class Job():
    """Job abstraction class."""

    def __init__(self,
                 id_: str,
                 operator: _Operator,
                 config: _ConfigReader
                ):
        """Initialize a new job.

        Args:
            operator: Operator object
            config: Operator configuration
        """
        # Private vars
        self._me = "Job():"
        self._id = id_
        self._operator = operator
        self._config = config
        self._repeat = 1
        self._online = False

    @property
    def id(self) -> str:
        """Unique identifier of job."""
        return self._id

    @property
    def operator(self) -> _Operator:
        """Operator object."""
        return self._operator

    @property
    def config(self) -> _ConfigReader:
        """Operator config."""
        return self._config

    @property
    def repeat(self):
        """Number of iterations to run this job."""
        return self._repeat

    @repeat.setter
    def repeat(self, value: int):
        self._repeat = value if value >= 0 else 0

    @property
    def online(self):
        """Job online status flag."""
        return self._online

    @online.setter
    def online(self, value: bool):
        self._online = value


class Jobs():
    """Container class for jobs."""

    def __init__(self):
        """Initialize a jobs container."""

        # Private vars
        self._me = "Jobs():"
        self._jobs = {}

    def add(self,
            job_config: dict,
            id_: str = None,
            overwrite: bool = False):
        """Add new job to container.

        Note: If no ID is given and the job's own
              ID is already taken, this method
              ignores the request and does not issue
              any warning by design.

        Args:
            job: Job object configuration
            id_: (Optional) Identifier of a job object
            overwrite: (Optional) Flag to overwrite job
                       in case the ID already exists.
                       Default: False
        """
        # Create
        job = None
        try:
            job = Job(**job_config)
        except Exception as err:
            raise ValueError(f"{self._me} Job settings "\
                             f"failed initialization.") from err
        # Add
        if id_ is None:
            if job.id not in self._jobs or overwrite:
                self._jobs[job.id] = job
        else:
            if id_ not in self._jobs or overwrite:
                self._jobs[id_] = job

    def delete(self, job_id: str):
        """Delete a job given its ID.

        Args:
            job_id: Identifier of job to delete
        """
        if job_id in self._jobs:
            del self._jobs[job_id]

    def delete_conditional(self, online: bool):
        """Delete a job given its online state.

        Args:
            online: Job online status flag
        """
        removal = []
        for id_, job in self._jobs.items():
            if job.online == online:
                removal.append(id_)
        for id_ in removal:
            del self._jobs[id_]

    def get(self, job_id: str) -> Job:
        """Retrieve a job given its ID.

        Args:
            job_id: Identifier of job

        Returns:
            Job object or None
        """
        if job_id in self._jobs:
            return self._jobs[job_id]
        return None

    @property
    def all(self) -> dict:
        """Retrieve all jobs."""
        return self._jobs
