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
"""Network abstraction of any operators."""

# Third-Party Dependencies
from secrets import token_urlsafe as _token_urlsafe

# Local Dependencies
from governor.io import ConfigWrapper as _ConfigWrapper


class Network():
    """Directed graph of operators representing a network."""

    def __init__(self,
                 # Required inputs
                 id_: str,
                 config: _ConfigWrapper,
                 # Optional inputs
                 name: str = None
                ):
        """Initialize a new network.

        Args:
            id_: Unique network identifier, which is usually set
                 by the Controller that assures uniqueness.
            config: Configuration containing all logic to construct the
                    network.
            name: (Optional) User-defined name of the network, which can
                  be set through its configuration.
        """
        # Private vars by class args
        self._id = id_
        self._name = name

        # Private vars by init
        self._me = "Network():"
        self._operators = {}
        self._edges = []

        # Build network
        self._build(config.operators)

    @property
    def edges(self):
        """List of network edges."""
        return self._edges

    @property
    def edges_str(self):
        """String of network edges."""
        return ", ".join(str(edge) for edge in self._edges)

    @property
    def operators(self):
        """Operator configuration."""
        return self._operators

    def operator_sequence(self) -> list:
        """Sequence of operators based on edge order.

        Returns:
            List of operators
        """
        sequence_ = []
        for idx, edge in enumerate(self._edges):
            if idx == 0:
                sequence_.extend([edge.source, edge.target])
            elif edge.source != sequence_[-1]:
                sequence_.extend([edge.source, edge.target])
            else:
                sequence_.append(edge.target)

        return sequence_

    def _build(self, config_: list):
        """Build network structure based on configuration.

        Args:
            config_: Payload operator configuration list
        """

        # Create unique node/operator identifiers
        ids_ = []
        for cfg in config_:
            ids_.append(self._operator_id(cfg))
            self._operators[ids_[-1]] = cfg

        # Initialize network edges with run_after blindness
        for idx_, id_ in enumerate(ids_):

            # Skip first
            if idx_ == 0:
                continue

            # Create new edge
            self._edges.append(self._Link(
                source = ids_[idx_ - 1],
                target = id_
            ))

        # Apply run_after instructions
        n_edges = len(self._edges)
        for _ in range(n_edges):

            # Change params
            insert_edge = None
            remove_edge = None
            update_edge = None
            update_now = False
            update_later = False

            # Evaluate
            for idx_, edge in enumerate(self._edges):

                # Target operator config
                target_cfg = self._operators[edge.target]

                # Skip without run_after
                if not self._has_run_after(target_cfg):
                    continue

                # Expected source of target operator
                expected_source_ = target_cfg["run_after"]

                # Single instruction
                if isinstance(expected_source_, str):
                    # Skip if already paired
                    if edge.source == expected_source_:
                        continue

                    # Find new position based on source (priority!)
                    for idx__, edge_ in enumerate(self._edges):
                        # Skip myself
                        if idx__ == idx_:
                            continue

                        # Found first source match
                        if edge_.source == expected_source_:
                            # Check if next one is match too
                            if idx__+1 < n_edges:
                                if (self._edges[idx__+1].source
                                    == expected_source_):
                                    continue

                            # Flag to update
                            update_now = True

                        # Keep track of target matches
                        elif edge_.target == expected_source_:
                            update_later = True

                        # Prepare updates
                        if update_now or update_later:
                            insert_edge = idx__+1, self._Link(
                                source = expected_source_,
                                target = edge.target
                            )
                            remove_edge = idx_+1 if idx__ < idx_ else idx_
                            update_edge = remove_edge

                        # Stop here
                        if update_now:
                            break

                # Multiple instructions
                elif isinstance(expected_source_, list):

                    # Counter
                    found_ = 0

                    # Find new position
                    for idx__, edge_ in enumerate(self._edges):
                        if edge_.source in expected_source_:
                            found_ += 1
                            if found_ == len(expected_source_):

                                # Prepare updates
                                insert_edge = idx__+1, self._Link(
                                    source = expected_source_,
                                    target = edge.target
                                )
                                remove_edge = idx_+1 if idx__ < idx_ else idx_
                                update_edge = remove_edge
                                update_now = True
                                break

                if update_now or update_later:
                    break

            # Update
            if update_now or update_later:
                self._edges.insert(insert_edge[0], insert_edge[1])
                del self._edges[remove_edge]
                if update_edge < n_edges:
                    if (self._edges[update_edge].source ==
                        insert_edge[1].target):
                        self._edges[update_edge].source = \
                            self._edges[update_edge-1].target

    def _operator_id(self, operator_: dict) -> str:
        """Return unique identifier of operator.

        Args:
            operator_: Configuration of operator

        Returns:
            Unique id string
        """
        if self._has_user_id(operator_):
            if operator_["id_"] not in self._operators:
                return operator_["id_"]
            else:
                # Sanity (bug) check: should be discovered already during
                # config import validation
                raise ValueError(f"{self._me} Duplicate user-defined "\
                                 f"operator identifier found: "\
                                 f"{operator_['id_']}")
        else:
            return self._create_id()

    def _has_user_id(self, operator_: dict):
        """Flag if operator has user-defined identifier.

        Args:
            operator_: Operator settings dictionary

        Returns:
            Boolean flag
        """
        return "id_" in operator_

    def _create_id(self, length: int = 16) -> str:
        """Create random unique id.

        Args:
            length: (Optional) Length of id

        Returns:
            Unique id string
        """
        id_ = _token_urlsafe(length)
        if id_ in self._operators:
            self._create_id(length)

        return id_

    def _has_run_after(self, operator_: dict) -> bool:
        """Flag if operator has run_after instruction.

        Args:
            operator_: Operator settings dictionary

        Returns:
            Boolean flag
        """
        return "run_after" in operator_

    class _Link():
        """Named network links."""
        def __init__(self,
                     source: str = None,
                     target: str = None,
                     label: str = None):
            """Create new link.

            Args:
                source: id_ of source operator
                target: id_ of target operator
                label: optional link label
            """
            self.source = source
            self.target = target
            self.label = label

        def __str__(self):
            """String representation."""
            return f"Link(source={self.source}, target={self.target})"
