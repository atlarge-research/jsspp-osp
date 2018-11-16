# Copyright (c) 2018 atlarge-research
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

from enum import Enum
from typing import List, Optional, Union
from dataclasses import dataclass

from jsspp.osp.model.environment import RackUnit


@dataclass(frozen=True)
class ProcessingUnit:
    """
    A processing unit in a machine.
    """
    clock_rate: float
    cores: int
    id: Optional[Union[int, str]] = None


class MachineState(Enum):
    HALT = 0,
    RUNNING = 1,
    MAINTENANCE = 2,
    FAILURE = 3


@dataclass(frozen=True)
class PhysicalMachine(RackUnit):
    """
    A physical machine installed in a rack slot
    """
    state: MachineState
    cpus: List[ProcessingUnit]
    gpus: List[ProcessingUnit] = []
    id: Optional[Union[int, str]] = None

