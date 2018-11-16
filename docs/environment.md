---
title: Environment  
---

This document is concerned with creating a description of a large-scale computing environment. This
description includes including key size and topology information of the environment, types of resources, but also 
various operational and management rules such as scheduled maintenance, allocation and other constraints, etc.

The environment description is written in JSON format and consists of the following elements:

1. **Topology**  
   A topology of the environment which specifies what resources are available and how they are organized within the
   environment.
2. **Events**  
   A list of timestamped events that occurred to model dynamic changes in the environment, such as scheduled 
   maintenance or failures.
3. **Definitions**  
   A set of user-defined definitions that can used in the topology and event list. This prevents duplication of common
   resource types in the environment, such as standard physical machine types.

A JSON schema for this format is provided [here](/schemas/environment.schema.json) and additional information on tools
to validate the description can be found [here](validation.md).

## Getting Started
Let's start with a minimal environment description, that only contains the required information (according to the schema):
```json
{
    "$schema": "https://raw.githubusercontent.com/atlarge-research/jsspp-osp/v1/schemas/environment.schema.json",
    "environment": {
        "datacenters": []
    },
    "events": [],
    "definitions": {}
}
```
This shows the basic structure of an environment description in this format. Additionally, the following extra information can be provided at the root of the document:

- `name` - The name of the environment
- `description` - A small textual description about the environment that is being modeled 

The `$schema` property is used to refer to the schema of the document and enables support for schema validation in many text editors (such as Jetbrains Products, Visual Studio Code).

## Using definitions
The format uses a nested, denormalized structure to represent an environment. This might cause duplication when for example
using common resource types. To prevent such duplication, the format supports referencing other objects in the document:

Using the `$base` property on an object, you can reference another object in the document (using a [JSON Pointer](https://tools.ietf.org/html/rfc6901)) to inherit its properties.
Note that properties of the object that contains `$base`, take precedence over the properties in the referenced object.
```json
{
    "test": {
        "a": 2,
        "$base": "#/definition"
    },
    "definition": {
        "a": 1,
        "b": 2
    }
}
```
This document resolves to:
```json
{
    "test": {
        "a": 2,
        "b": 2
    },
    "definition": {
        "a": 1,
        "b": 2
    }
}
```

### Multiple Inheritance
To inherit from multiple definitions, you can use an array syntax to specify multiple references. Please note the 
ascending precedence is based on the definition order.
```json
{
    "test": {
        "a": 2,
        "$base": ["#/definition-a", "#/defintion-b"]
    },
    "definition-a": {
        "a": 1,
        "b": 2,
        "c": 3
    },
    "definition-b": {
        "b": 3
    }
}
```
This document resolves to:
```json
{
    "test": {
        "a": 2,
        "b": 3,
        "c": 3
    },
    "definition-a": {
        "a": 1,
        "b": 2,
        "c": 3
    },
    "definition-b": {
        "b": 3
    }
}
```

### Merging Properties
The format additionally supports merging of properties one-level deep using the `$merge` property. This works for
arrays and objects.
```json
{
    "test": {
        "array": [1, 2],
        "object": { "a":  1 },
        "$base": "#/definition",
        "$merge": ["array", "object"] 
    },
    "definition": {
        "array": [2, 3, 4],
        "object": { "a": 2, "b": 2 }
    }
}
```
This document resolves to:
```json
{
    "test": {
        "array": [1, 2, 2, 3, 4],
        "object": { "a":  1, "b": 2 }
    },
    "definition": {
        "array": [2, 3, 4],
        "object": { "a": 2, "b": 2 }
    }
}
```

### Concrete Example
Below, a concrete example of defining and using a common machine type:
```json
{
    "$schema": "https://raw.githubusercontent.com/atlarge-research/jsspp-osp/v1/schemas/environment.schema.json",
    "environment": {
        "datacenters": [
            {
                "rooms": [
                    {
                        "type": "SERVER",
                        "objects": [
                            {
                                "type": "RACK",
                                "units": [
                                    { 
                                        "id": 1,
                                        "name": "hostname-1.example.com",
                                        "state": "ACTIVE",
                                        "$base": "#/definitions/machine/default"
                                    } 
                                ]
                            }
                        ]
                    }
                ]
            }
        ]
    },
    "events": [],
    "definitions": {
        "machines": {
            "default": {
                "type": "MACHINE",
                "cpus": [
                    {
                        "manufacturer": "Intel",
                        "family": "Xeon",
                        "generation": "v3",
                        "model": "E5-2630",
                        "clock-rate": 2400000000,
                        "cores": 8
                    }
                ],
                "memory": [
                    {
                        "capacity": 8000
                    }
                ]                       
            }
        }
    }
}
```

## Describing the topology
In this format, a topology consists of at the following elements:

- `datacenters` (required) - A list of datacenters that are part of the environment 

No additional properties are specified for the topology, however feel free to add additional properties if you prefer so.

### Datacenters
A datacenter consists of the following elements:

- `id` - A unique identifier (with respect to the other datacenters) that represents this datacenter
- `name` - The name of the datacenter
- `location` - A textual representation of the location of the datacenter
- `operator` - The name of the operator of the datacenter
- `operational` - Operational details about the datacenter (such as scheduling information). 
See [Operational Details](#operational-details) for more information.
- `rooms` (required) - A list of rooms in the datacenter. If you prefer not to disclose this information, please model the datacenter
    as having a single room.
    
An example of such a description:
```json
{
    "$schema": "https://raw.githubusercontent.com/atlarge-research/jsspp-osp/v1/schemas/environment.schema.json",
    "environment": {
        "datacenters": [
            {
                "id": 0,
                "name": "europe-west4",
                "location": "Eemshaven, Netherlands",
                "operator": "Google",
                "operational": {
                    "scheduler": {
                        "name": "stage-scheduler",
                        "options": {
                            "selection": "FIFO",
                            "placement": "BEST-FIT"
                        }
                    }
                },
                "rooms": []
            }
        ]
    },
    "events": [],
    "definitions": {}
}
```

#### Operational Details
The operational details of a datacenter consist of the following elements:

- `scheduler` - Information about the task scheduler used in the datacenter:
    - `name` (required) - The name of the scheduler that is used
    - `url` - An URL referring to the document that describes this scheduler (such as a publication)
    - `options` - The configuration of the scheduler represented as a key-value mapping

Additional operational details may be specified, but we provide no format for these details.

### Rooms
A room consists of the following elements:

- `id` - A unique identifier (with respect to _all_ other rooms) that represents this room
- `name` - The name of the room
- `type` (required) - The type of this room, which is one of:
    - `COOLING` 
    - `HALLWAY`
    - `OFFICE`
    - `POWER`
    - `SERVER`
- `size` - The size of the room:
    - `width` - The width of the room in meters
    - `height` - The height of the room in meters
- `location` - The location of the room within the datacenter:
    - `x` - The x-coordinate of the upper-left corner of the room 
    - `y` - The y-coordinate of the upper-left corner of the room 
- `objects`: A list of objects within this room:
    - [Rack](#racks) - A server rack for mounting electronic equipment

An example of such a description:
```json
{
    "$schema": "https://raw.githubusercontent.com/atlarge-research/jsspp-osp/v1/schemas/environment.schema.json",
    "environment": {
        "datacenters": [
            {
                "rooms": [
                    {
                        "type": "SERVER",
                        "name": "Server Room",
                        "objects": []
                    }
                ]
            }
        ]
    },
    "events": [],
    "definitions": {}
}
```

### Racks
A rack is a room object and consists of the following elements:

- `id` - A unique identifier (with respect to _all_ other racks) that represents this rack
- `type` (required) - Must equal `RACK` to indicate that it is a rack
- `name` - The name of the rack
- `capacity` - The maximum amount of 1U units in this rack
- `power-capacity` - The power capacity of the rack in watts
- `units` - The installed rack units in the rack:
    - Empty - An explicit empty slot in the rack represented as:
        ```json
         { "type":  "EMPTY" }
        ``` 
    - [Physical Machine](#physical-machines) - A physical machine in the rack
    
An example of such a description:
```json
{
    "$schema": "https://raw.githubusercontent.com/atlarge-research/jsspp-osp/v1/schemas/environment.schema.json",
    "environment": {
        "datacenters": [
            {
                "rooms": [
                    {
                        "type": "SERVER",
                        "name": "Server Room",
                        "objects": [
                            {
                                "type": "RACK",
                                "capacity": 42,
                                "units": [
                                    { "type":  "EMPTY" },
                                    { "type":  "MACHINE", "cpus":  [] }
                                ]
                            }
                        ]
                    }
                ]
            }
        ]
    },
    "events": [],
    "definitions": {}
}
```
    
### Physical Machines
A physical machine is a rack unit and consists of the following elements:

- `id` - A unique identifier (with respect to _all_ other machines) that represents this machine
- `type` (required) - Must equal `MACHINE` to indicate this a machine
- `name` - The name of the machine (such as a hostname)
- `state` - The state of the machine, which is one of:
    - `ACTIVE`
    - `HALT`
    - `MAINTENANCE`
    - `FAILURE`
- `cpus` - A list of CPUs installed in the machine. See [Processing Units](#processing-units) on how to specify a CPU.
- `cpus` - A list of GPUs installed in the machine. See [Processing Units](#processing-units) on how to specify a GPU.
- `memory` - A list of memory units installed in the machine. See [Memory or Storage](#memory-or-storage) for more information.
- `storage` - A list of storage units installed in the machine. See [Memory or Storage](#memory-or-storage) for more information.

An example of such a description:
```json
{
    "$schema": "https://raw.githubusercontent.com/atlarge-research/jsspp-osp/v1/schemas/environment.schema.json",
    "environment": {
        "datacenters": [
            {
                "rooms": [
                    {
                        "type": "SERVER",
                        "name": "Server Room",
                        "objects": [
                            {
                                "type": "RACK",
                                "capacity": 42,
                                "units": [
                                    { "type":  "EMPTY" },
                                    { 
                                        "type": "MACHINE",
                                        "id": 1,
                                        "name": "hostname-1.example.com",
                                        "state": "ACTIVE",
                                        "cpus": [
                                            {
                                                "manufacturer": "Intel",
                                                "family": "Xeon",
                                                "generation": "v3",
                                                "model": "E5-2630",
                                                "clock-rate": 2400000000,
                                                "cores": 8
                                            }
                                        ],
                                        "gpus": [
                                            {
                                                "manufacturer": "nVidia",
                                                "family": "GTX",
                                                "generation": "4",
                                                "model": "1080",
                                                "clock-rate": 1200000000,
                                                "cores": 2000
                                            }
                                        ],
                                        "memory": [
                                            {
                                                "manufacturer": "Samsung",
                                                "family": "DDR4",
                                                "generation": "K4A8G085WB",
                                                "model": "BIWE",
                                                "read-speed": 25000,
                                                "write-speed": 25000,
                                                "capacity": 8000
                                                
                                            }
                                        ],
                                        "storage": [
                                            {
                                                "manufacturer": "Samsung",
                                                "family": "QVO",
                                                "generation": "2018",
                                                "model": "MZ-76Q4T0BW",
                                                "read-speed": 500,
                                                "write-speed": 500,
                                                "capacity": 4000000
                                            }
                                        ]
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        ]
    },
    "events": [],
    "definitions": {}
}
```

#### Processing Units
A processing unit consists of the following elements:

- `id` - A unique identifier (with respect to _all_ other processing units) that represents this processing unit
- `manufacturer` - The manufacturer of the processing unit
- `family` - The family of the processing unit
- `generation` - The generation of the processing unit
- `model` - The model of the processing unit
- `clock-rate` (required) - The clock rate of the processing unit in Hz
- `cores` (required) - The amount of physical cores in the processing unit
- `energy-consumption` - The average energy consumption of the processing unit in watts

#### Memory or Storage
A memory unit consists of the following elements:

- `id` - A unique identifier (with respect to _all_ other memory/storage units) that represents this unit
- `manufacturer` - The manufacturer of the unit
- `family` - The family of the unit
- `generation` - The generation of the unit
- `model` - The model of the unit
- `read-speed` - The read speed in MB/s
- `write-speed` - The write speed in MB/s 
- `capacity` - The capacity of the unit in MBs
- `energy-consumption` - The average energy consumption of the unit in watts

## Creating events
There are several event types supported in the format:
- [Datacenter Events](#datacenter-events)
- [Machine Events](#machine-events)

An example of using events is shown below:
```json
{
    "name": "Google Cloud",
    "environment": {
        ... 
    },
    "events": [
        {
            "type": "MACHINE_STATE_CHANGE",
            "time": 1,
            "machine": 1,
            "state": "MAINTENANCE"
        },
        {
            "type": "MACHINE_STATE_CHANGE",
            "time": 100,
            "machine": 2,
            "state": "FAILURE",
            "cause": "Hard-disk drive failed"
        },
        {
            "type": "DATACENTER_SCHEDULER_CHANGE",
            "time": 300,
            "datacenter": 1,
            "scheduler": {
                "name": "stage-scheduler",
                "options": {
                    "selection": "SRTF",
                    "placement": "BEST-FIT"
                }
            }
        }
    ],
    "definitions": {}
}
```

### Datacenter Events
The following events are supported for a datacenter entity:
1. `DATACENTER_SCHEDULER_CHANGE` - This event indicates that the datacenter changed scheduler and has the following structure:
    - `type` (required) - Must equal `DATACENTER_SCHEDULER_CHANGE`
    - `datacenter` (required) - A unique identifier of a datacenter 
    - `scheduler` (required) - The scheduler the datacenter changed to
    
    An example of this event:
    ```json
    {
       "type": "DATACENTER_SCHEDULER_CHANGE",
       "datacenter": 1,
       "scheduler":  {
           "name": "stage-scheduler",
           "options": {
               "selection": "SRTF",
               "placement": "BEST-FIT"
           }
       }
    }
    ```

### Machine Events
The following events are supported for a machine entity:
1. `MACHINE_STATE_CHANGE` - This event indicates that the state of a machine changed and has the following structure:
    - `type` (required) - Must equal `MACHINE_STATE_CHANGE`
    - `machine` (required) - A unique identifier of a machine
    - `state` (required) - The state the machine changed to
    
    An example of this event:
    ```json
    {
       "type": "MACHINE_STATE_CHANGE",
       "machine": 1,
       "state": "MAINTENANCE"
    }
    ```

## Examples
We provide examples in the `examples` directory:

1. [Simple](/examples/environment.json) - A very basic description of an environment to use as a starting point

