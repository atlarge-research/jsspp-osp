# JSSPP OSP Formats and Tools
This repository contains tooling and documentation of the formats used for
Open Scheduling Problems (OSPs) of the [JSSPP](http://jsspp.org/index.php?page=cfp) workshop.

Scheduling large parallel systems remains a formidable challenge today. Facing this challenge, however, requires knowledge of the actual problems encountered in the field. We hope to facilitate the sharing of open problems in scheduling these systems by defining a common standard in which problems can be defined and then shared with the community. We consider an Open Scheduling Problem (OSP) to consist of two main aspects:

* The **environment**, consisting of the static topology (physical and logical organization of the machines) and system events which change that topology.
* The **workload**, consisting of the jobs and tasks that the system should run.

This repository provides the format for specifying this information and the tools to validate whether these formats are valid. If you want to submit an OSP, it needs to be specified in terms of at least two JSON files: One for the environment, and one for the workload. Both need to comply with their respective JSON schemas, which can be found in `schemas/`. The schemas are flexible, allowing you to share as much or as little as you can disclose. If you feel that a certain machine-readable part of the format does not adequately express your problem, feel free to use the free-form text description fields to complement the machine-readable information.

We have provided a basic "Hello World" example, consisting of a simple environment and workflow workload. To explore this example, follow the documentation below, or see the `examples/` folder for a quick impression. Note that this example is not an exhaustive representation of what can be expressed in the formats. Please refer to the schemas for a complete list of the properties that can be modeled.

## Documentation
The documentation of the formats is located in the `docs` directory and is divided into:

1. [Install Tools](docs/installation.md): How to install the tooling necessary for validating your descriptions.
2. [Create Environment Description](docs/environment.md): How to write/generate an environment description complying with the format.
3. [Create Workload Description](docs/workload.md): How to write/generate a workload description complying with the format.
4. [Validate Descriptions](docs/validation.md): How to run the validation tools against your descriptions.
5. [Submit Files](docs/submission.md): How to submit an OSP to JSSPP.

## Contributing
### Build Environment
Run the following command in the root directory of the project:
```bash
$ pipenv install
```
This will install the required dependencies and setup the Python virtual environment.

### Generate Documentation
Please make sure you have installed `ruby` and `bundler`. Run the following
commands in the source directory:

```bash
$ bundler install
$ bundler exec jekyll build
```

The generated documentation can be found in `site/`.

### License
The code is released under the MIT license. See the [LICENSE.txt](LICENSE.txt) file.
