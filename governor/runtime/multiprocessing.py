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
"""Distribution handler for multiprocessing operators in network nodes."""

# Third-Party Dependencies
from multiprocessing import Process as _Process
from multiprocessing import Queue as _Queue
from multiprocessing import Event as _Event
from time import sleep as _sleep
from time import time_ns as _time_ns
from os import getpid as _getpid

# Local Dependencies
from governor.objects.operator import Operator as _Operator


class ProcessMetaData():
    """Abstraction of meta data from a process."""

    def __init__(self,
                 start_time_ns: int,
                 pid: int):
        """Initialize meta data object.

        Args:
            start_time_ns: Number of nanoseconds that have passed
                           since the epoch (Jan 1, 1970 at
                           00:00:00 UTC)
            pid: Process ID by operating system
        """
        self._start_time_ns = start_time_ns
        self._end_time_ns = start_time_ns
        self._pid = pid

    def end_time_ns(self, time_ns: int):
        """Set end time of process in nanoseconds since epoch.
        
        Args:
            time_ns: Number of nanoseconds that have passed
                     since the epoch (Jan 1, 1970 at
                     00:00:00 UTC)

        Returns:
            Self
        """
        self._end_time_ns = time_ns
        return self
    
    @property
    def dict(self) -> dict:
        """Returns dictionary version of meta data.

        Note: Milliseconds are returned but with
              nanosecond precision.        
        """
        return {
            "start_time_ms": self._start_time_ns/1000,
            "end_time_ms": self._end_time_ns/1000,
            "pid": self._pid
        }


class OperatorProcess(_Process):
    """Process for operators"""

    def __init__(self,
                 operator: _Operator,
                 name: str = "",
                 return_queue: _Queue = None,
                 standby_event: _Event = None,
                 start_event: _Event = None,
                 done_event: _Event = None,
                 error_event: _Event = None):
        """Initialize a new process.

        Args:
            operator: Operator to run in this process
            name: (Optional) Identifier of operator process
            return_queue: (Optional) Operator return queue
            standby_event: (Optional) Event to launch in standby mode
            start_event: (Optional) Event to notify caller of started execution
            done_event: (Optional) Event to notify caller of completed execution
            error_event: (Optional) Event to notify caller of error
        """
        # Base constructor
        _Process.__init__(self)

        # Public vars
        self.name = name

        # Private vars
        self._operator = operator
        self._return_queue = return_queue
        self._standby_event = standby_event
        self._start_event = start_event
        self._done_event = done_event
        self._error_event = error_event

    @property
    def return_value(self):
        """Return value of operator"""
        return self._return_queue.get() if self._return_queue is not None\
                                        else None

    def run(self):
        """Operator run method"""

        # Standby
        if self._standby_event is not None:
            self._standby_event.wait()

        # Notify start
        if self._start_event is not None:
            self._start_event.set()

        # Register meta data
        meta = ProcessMetaData(
            start_time_ns = _time_ns(),
            pid = _getpid()
        )

        # Execute
        try:
            if self._return_queue is None:
                _ = self._operator.run()
            else:
                self._return_queue.put(
                    (self._operator.run().response,
                     meta.end_time_ns(_time_ns()).dict)
                )
        except RuntimeError:
            self._return_queue.put(
                (self._operator.exceptione,
                 meta.end_time_ns(_time_ns()).dict)
            )
            self._error_event.set()
            pass

        # Done
        if self._done_event is not None:
            self._done_event.set()


class Processor():
    """Processor of parallel operator executions."""

    def __init__(self,
                 id_: str,
                 operators: dict,
                 expected_returns: dict = None,
                 standby_events: dict = None):
        """Initialize a new processor.

        Args:
            id_: Unique identifier of processor
            operators: Dictionary of operators to run in processes,
                       where the keys refer to the identifiers of
                       the respective operators
            expected_returns: (Optional) dictionary of boolean flags
                              to get returns from respective operators
            standby_events: (Optional) dictionary of events to put
                            operator processes in standby until set
                            by caller
        """
        # Private vars
        self._me = "Processor():"
        self._processor_id = id_
        self._operators = operators
        self._return_queues = None
        self._standby_events = standby_events
        self._start_events = {id_: _Event() for id_ in self._operators}
        self._done_events = {id_: _Event() for id_ in self._operators}
        self._error_events = {id_: _Event() for id_ in self._operators}
        self._processes = {id_: None for id_ in self._operators}

        # Setup optional retuns with queues
        # Note: We use for simplicity queues in isolation, to allocate
        #       separate memory blocks per operator
        if expected_returns is not None:
            # Sanity check
            if len(expected_returns) == 0:
                raise ValueError(f"{self._me} Received no expected returns.")

            # Fill
            self._return_queues = {}
            for id_ in self._operators:
                if id_ in expected_returns:
                    if expected_returns[id_]:
                        self._return_queues[id_] = _Queue()
                        #self._return_queues[id_].put(None)
                    else:
                        self._return_queues[id_] = None
                else:
                    self._return_queues[id_] = None

    @property
    def processor_id(self) -> str:
        """Identifier of processor."""
        return self._processor_id

    def return_queue(self, id_: str) -> _Queue:
        """Retrieve return queue of operator.

        Args:
            id_: Operator identifier

        Returns:
            Queue() object or None
        """
        if isinstance(self._return_queues, dict):
            if id_ in self._return_queues:
                return self._return_queues[id_]
            else:
                raise ValueError(f"{self._me} Operator ID {id_} "\
                                 f"does not exist.")
        return None

    def return_value(self, id_: str) -> any:
        """Retrieve return queue of operator.

        Args:
            id_: Operator identifier

        Returns:
            Operator return value or None
        """
        ret = self.return_queue(id_)
        if ret is not None:
            return ret.get()

        return None

    def _standby_event(self, id_: str) -> _Event:
        """Retrieve standby event of operator.

        Args:
            id_: Operator identifier

        Returns:
            Event() for standby of operator or None
        """
        if self._standby_events is not None:
            if (id_ in self._standby_events and\
                id_ in self._operators):
                return self._standby_events[id_]
            else:
                raise ValueError(f"{self._me} Operator ID {id_} "\
                                 f"does not exist.")
        return None

    def start_event(self, id_: str) -> _Event:
        """Retrieve start event of operator.

        Args:
            id_: Operator identifier

        Returns:
            Event() for start of operator
        """
        if id_ in self._start_events:
            return self._start_events[id_]
        else:
            raise ValueError(f"{self._me} Operator ID {id_} "\
                             f"does not exist.")

    def is_started(self, id_: str) -> bool:
        """Flag if start state of operator is set.

        Args:
            id_: Operator identifier

        Returns:
            Boolean
        """
        return self.start_event(id_).is_set()

    def done_event(self, id_: str) -> _Event:
        """Retrieve done event of operator.

        Args:
            id_: Operator identifier

        Returns:
            Event() for done of operator
        """
        if id_ in self._done_events:
            return self._done_events[id_]
        else:
            raise ValueError(f"{self._me} Operator ID {id_} "\
                             f"does not exist.")

    def is_done(self, id_: str) -> bool:
        """Flag if done state of operator is set.

        Args:
            id_: Operator identifier

        Returns:
            Boolean
        """
        return self.done_event(id_).is_set()

    def all_done(self) -> bool:
        """Flag if all operators are set to done.

        Returns:
            Boolean
        """
        return all([self.is_done(id_) for id_ in self._operators])

    def error_event(self, id_: str) -> _Event:
        """Retrieve error event of operator.

        Args:
            id_: Operator identifier

        Returns:
            Event() for errors of operator
        """
        if id_ in self._error_events:
            return self._error_events[id_]
        else:
            raise ValueError(f"{self._me} Operator ID {id_} "\
                             f"does not exist.")

    def has_error(self, id_: str) -> bool:
        """Flag if error state of operator is set.

        Args:
            id_: Operator identifier

        Returns:
            Boolean
        """
        return self.error_event(id_).is_set()

    def create_processes(self):
        """Create process per operator."""

        # Initialize operator processes
        for id_, operator in self._operators.items():
            self._processes[id_] = OperatorProcess(
                operator=operator,
                name=id_,
                return_queue=self.return_queue(id_),
                standby_event=self._standby_event(id_),
                start_event=self.start_event(id_),
                done_event=self.done_event(id_),
                error_event=self.error_event(id_)
            )

    def start_processes(self):
        """Start all operator processes."""
        for id_, process in self._processes.items():
            if process is not None:
                self._processes[id_].start()
            else:
                raise RuntimeError(f"{self._me} Operator ID {id_} "\
                                   f"does not have a process yet.")

    def get_process(self, id_: str) -> OperatorProcess:
        """Retrieve operator process by identifier.

        Args:
            id_: Operator identifier

        Returns:
            OperatorProcess
        """
        if id_ in self._processes:
            return self._processes[id_]
        else:
            raise ValueError(f"{self._me} Operator ID {id_} "\
                             f"does not exist.")

    def terminate_process(self, id_: str):
        """Terminate operator process by identifier.

        Args:
            id_: Operator identifier
        """
        try:
            # Done
            self.done_event(id_).set()

            # Terminate
            self.get_process(id_).terminate()
            _sleep(0.5)

            # Join
            if not self.get_process(id_).is_alive():
                self.get_process(id_).join(timeout=1.0)
            
            # Close respective queue
            queue = self.return_queue(id_)
            if queue is not None:
                queue.close()

        # pylint: disable=broad-except
        except Exception:
            print("DEBUG: terminate_process() exception", id_)
            pass
        # pylint: enable=broad-except

    def terminate_processes(self):
        """Terminate all operator processes."""
        for id_ in self._operators:
            self.terminate_process(id_)

    @property
    def num_processes(self) -> int:
        """Number of processes."""
        return len(self._processes)

    @property
    def operator_ids(self) -> list:
        """List of operator identifiers."""
        return list(self._operators.keys())

class Processors():
    """Container class for processors."""

    def __init__(self):
        """Initialize a processors container."""

        # Private vars
        self._me = "Processors():"
        self._processors = {}
        self._operators = {}
        self._expected_returns = None
        self._standby_events = None
        self._operator_map = {}

    def reset(self):
        """Cleanup previous configuration"""
        self._operators = {}
        self._expected_returns = None
        self._standby_events = None

    def add_config(self,
                   id_: str,
                   operator: _Operator,
                   expected_return: bool = None,
                   standby_event: _Event = None,
                   overwrite: bool = False):
        """Add new config for processor creation.

        Args:
            id_: Operator identifier
            operator: Operator object
            expected_return: (Optional) Flag to expect return
                             value
            standby_event: (Optional) Event to trigger process
                           standby
            overwrite: (Optional) Flag to overwrite processor
                       in case the ID already exists.
                       Default: False
        """
        # Operator
        if id_ not in self._operators or overwrite:
            self._operators[id_] = operator

        # Expected return
        if expected_return is not None:
            if isinstance(self._expected_returns, dict):
                if id_ not in self._expected_returns or overwrite:
                    self._expected_returns[id_] = expected_return
            else:
                self._expected_returns = {id_: expected_return}

        # Standby event
        if standby_event is not None:
            if isinstance(self._standby_events, dict):
                if id_ not in self._standby_events or overwrite:
                    self._standby_events[id_] = standby_event
            else:
                self._standby_events = {id_: standby_event}

    def create(self):
        """Create new processor.
        
        Returns:
            Processor ID or None
        """
        #  Sanity check: number of operators
        if len(self._operators) == 0:
            return None

        # New processor ID
        processor_id = "1"\
                       if self.num_processors == 0\
                       else str(max([int(id_)\
                            for id_ in self._processors.keys()])+1)

        # Create processor
        try:
            self._processors[processor_id] = Processor(
                id_ = processor_id,
                operators = self._operators,
                expected_returns = self._expected_returns,
                standby_events = self._standby_events
            )
        except Exception as err:
            raise ValueError(f"{self._me} Processor "\
                             f"failed initialization.") from err

        # Add respective operators to map
        for id_ in self._operators:
            self._operator_map[id_] = processor_id
        
        return processor_id

    def get(self,
            id_: str,
            by_operator: bool = False) -> Processor:
        """Retrieve processor of respective operator.
        
        Args:
            id_: Operator or processor identifier
            by_operator: (Optional) Flag to select by
                         operator identifier
        
        Returns:
            Processor object or None
        """
        if by_operator:
            if id_ in self._operator_map:
                return self._processors[self._operator_map[id_]]
        elif id_ in self._processors:
            return self._processors[id_]
        
        return None

    @property
    def all(self) -> dict:
        """Retrieve all processors."""
        return self._processors

    @property
    def num_processors(self) -> int:
        """Number of processors."""
        return len(self.all)

    def any_errors(self) -> bool:
        """Flag if any errors in processes found."""
        return len(self.error_messages()) > 0

    def error_messages(self) -> str:
        """Complilation of any error messages."""
        msg = ""
        for operator_id, processor_id in self._operator_map.items():
            if self._processors[processor_id].has_error(operator_id):
                msg += " [Processor "+processor_id+", Operator "+operator_id+"]: "+\
                       str(self._processors[processor_id].return_value(operator_id))
        return msg

    def terminate(self,
                  id_: str = None,
                  by_operator: bool = False):
        """Terminate processes.

        Note: If id_ is not set, then all processes will be
              terminated.

        Args:
            id_: (Optional) Operator or processor identifier
            by_operator: (Optional) Flag to select by
                         operator identifier
        """
        if id_ is None:
            for processor in self._processors.values():
                processor.terminate_processes()
            self._processors = {}
            self._operator_map = {}
            self.reset()

        else:
            processor = self.get(id_, by_operator)
            if processor is not None:
                if by_operator:
                    processor.terminate_process(id_)
                    if processor.all_done():
                        del self._processors[processor.processor_id]
                    if id_ in self._operator_map:
                        del self._operator_map[id_]
                else:
                    processor.terminate_processes()
                    del self._processors[id_]
                    for operator_id in self.operators(id_):
                        del self._operator_map[operator_id]

    def operators(self, processor_id: str = None) -> list:
        """List of operators with done state.

        Args:
            processor_id: (Optional) ID of respective processor
        
        Returns:
            List of operator IDs
        """
        # All IDs
        if processor_id is None:
            return list(self._operator_map.keys())

        # Mapped to processor ID
        ids_ = []
        for operator_id, processor_id_ in self._operator_map.items():
            if processor_id == processor_id_:
                ids_.append(operator_id)
        return ids_

    def done_operators(self) -> list:
        """List of operators with done state.
        
        Returns:
            List of operator IDs
        """
        done = []
        for operator_id, processor_id in self._operator_map.items():
            if self.get(processor_id).is_done(operator_id):
                done.append(operator_id)
        return done

    def done_processors(self) -> list:
        """List of processors with only operators in done state.
        
        Returns:
            List of processor IDs
        """
        done = []
        for id_, processor in self._processors.items():
            if processor.all_done():
                done.append(id_)
        return done

    def full_operator_match(self, operator_ids: list) -> list:
        """List of processors complete-matching full list of respective operators.

        Args:
            operator_ids: List of operator identifiers
        
        Returns:
            List of processor IDs
        """
        # Sanity check: non-empty list
        if len(operator_ids) == 0:
            return []

        # Search
        matched = []
        for proc_id, processor in self._processors.items():
            if all([id_ in operator_ids for id_ in processor.operator_ids]):
                matched.append(proc_id)
        return matched
