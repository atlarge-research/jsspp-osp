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

import typing

from jsspp.osp.model.environment import Environment, Datacenter, Room, RoomType, RoomObject, Rack, RackUnit
from jsspp.osp.model.environment.resources.machine import PhysicalMachine, MachineState, ProcessingUnit
from jsspp.osp.model.environment.events import Event


def map_environment(document: typing.Dict) -> typing.Tuple[Environment, typing.List[Event]]:
    """
    Map the specified dictionary to an environment.
    :param document: The document to map.
    :return: The document mapped to an environment.
    """
    events = document.get('events', [])
    events = list(map(lambda e: Event(e['type'], e['time']), events))

    env = document['environment']
    datacenters = list(map(map_datacenter, env['datacenters']))
    name = env.get('name')
    env = Environment(datacenters=datacenters, name=name)

    return env, events


def map_datacenter(document: typing.Dict) -> Datacenter:
    id = document.get('id')
    rooms = list(map(map_room, document['rooms']))
    return Datacenter(rooms=rooms, id=id)


def map_room(document: typing.Dict) -> Room:
    id = document.get('id')
    type = RoomType[document.get('type', 'SERVER')]
    objects = list(map(map_room_object, document.get('objects', [])))
    return Room(objects=objects, type=type, id=id)


def map_room_object(document: typing.Dict) -> RoomObject:
    type = document['type']
    if type == 'RACK':
        return map_rack(document)
    raise Exception(f"Invalid type {type}")


def map_rack(document: typing.Dict) -> Rack:
    id = document.get('id')
    capacity = document.get('capacity')
    units = list(map(map_rack_unit, document['units']))
    return Rack(capacity=capacity, units=units, id=id)


def map_rack_unit(document: typing.Dict) -> RackUnit:
    type = document['type']
    if type == 'MACHINE':
        return map_machine(document)
    raise Exception(f"Invalid type {type}")


def map_machine(document: typing.Dict) -> PhysicalMachine:
    id = document.get('id')
    state = MachineState[document.get('state', 'RUNNING')]
    cpus = list(map(map_processing_unit, document.get('cpus', [])))
    gpus = list(map(map_processing_unit, document.get('gpus', [])))
    return PhysicalMachine(id=id, state=state, cpus=cpus, gpus=gpus)


def map_processing_unit(document: typing.Dict) -> ProcessingUnit:
    id = document.get('id')
    clock_rate = document['clock-rate']
    cores = document['cores']
    return ProcessingUnit(id=id, clock_rate=clock_rate, cores=cores)
