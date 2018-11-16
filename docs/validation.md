---
title: Validation  
---

This page describes how you can validate the workload and environment descriptions you made. We provide the
`jsspp-osp` tool for this purpose.

## Validating an Environment Description
Suppose that we want to validate the environment description located at `examples/environment.json`. We use the
`validate-environment` command of the `jsspp-osp` tool for this:

```bash
$ jsspp-osp validate-environment examples/environment.json
```
If your descriptions does not match the schema, the tool will show you which values are incorrect and why 
they do not match the schema:
```
INFO: Processing file examples/environment.json
INFO: Validating structural requirements
ERROR: File does not match schema: -5 is less than the minimum of 1

Failed validating 'minimum' in schema[1]['properties']['cpus']['items']['properties']['cores']:
    {'description': 'The amount of physical cores in the processing unit',
     'minimum': 1,
     'type': 'integer'}

On instance['cpus'][1]['cores']:
    -5
```

## Validating a Workload Description
The procedure for validating a workload description is similar: Suppose that we want to validate the environment description located at `examples/environment.json`. We use the
`validate-workload` command of the `jsspp-osp` tool for this:

```bash
$ jsspp-osp validate-workload examples/workload.json
```

This is the expected output for a correct file:

```
INFO: Processing file examples/workload.json
INFO: Validating structural requirements
INFO: Format OK
```

## Usage
```
$ jsspp-osp -h
usage: jsspp-osp [-h] {validate-workload,validate-environment} ...

Tooling and documentation of of the formats used for Open Scheduling Problems
(OSPs) of JSSPP

optional arguments:
  -h, --help            show this help message and exit

Commands:
  {validate-workload,validate-environment}
    validate-workload   Validate a workload
    validate-environment
                        Validate an environment description

```
