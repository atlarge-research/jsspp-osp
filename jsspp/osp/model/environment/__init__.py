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


class RackUnit:
    """
    A unit in a rack
    """
    pass


class RoomObject:
    """
    An object in a datacenter room
    """
    pass


@dataclass(frozen=True)
class Rack(RoomObject):
    """
    A rack in a datacenter room
    """
    capacity: int
    units: List[RackUnit]
    id: Optional[Union[int, str]] = None


class RoomType(Enum):
    COOLING = 0
    HALLWAY = 1
    OFFICE = 2
    POWER = 3
    SERVER = 4


@dataclass(frozen=True)
class Room:
    """
    A room in a datacenter
    """
    objects: List[RoomObject]
    type: RoomType = RoomType.SERVER
    id: Optional[Union[int, str]] = None


@dataclass(frozen=True)
class Datacenter:
    """
    A description of a datacenter that is part of the cloud computing environment
    """
    rooms: List[Room]
    id: Optional[Union[int, str]] = None


@dataclass(frozen=True)
class Environment:
    """
    A description on a cloud computing environment
    """
    datacenters: List[Datacenter]
    name: Optional[str] = None
