---
title: Workload  
---

This document describes which elements should be present in the traces, including types and structure.
The workload description is in JSON format and consists of five main elements:

1. The **workload**: depict the start and end date as well as a description highlighting important conventions used. E.g. when non-functional requirements are preset in key:value format, the meaning of what each key and value represents is entered here. 
2. **Workflows**: The workflow object comprises generic information about the application or job. It contains the domain and field the workflow belongs to, a list of tasks and other meta information such as the scheduler that scheduled this workflow. 
3. **Tasks**: The task object describes the resource needs, dependencies, and other information associated with this task. Each workflow consists of one or more tasks that may have computational depencies between each other.
4. **Resources**: Resources describe the environment the task was executed on. This object contains information such as the time the resource was assigned to this task and when it was released, the operating system and resources available.
5. **Datatransfers**: describe all data transfers that took place while executing the workflow. Often, tasks require several input files which may need to be transferred between machines.

## Validating traces
A tool to validate the JSON data exists which checks if all the required components and correct keys are set and if values are of the right type.

## Examples
We provide examples in the `examples` directory:

1. [Simple](/examples/workload.json) - A very basic description of a single-workflow workload to use as a starting point
