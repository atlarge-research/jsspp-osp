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

import sys
import argparse
import logging

from jsspp.osp.parser.workload import parse_workload, load_schema as load_workload_schema
from jsspp.osp.parser.environment import parse_environment, load_schema as load_environment_schema
from jsspp.osp.validation.schema import validate

__description__ = 'Tooling and documentation of of the formats used for Open Scheduling Problems (OSPs) of JSSPP'

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')


def validate_workload(args):
    """
    Validate a workload description for JSSPP OSP.
    :param args: The command line arguments passed to this command.
    :return:
    """
    logging.info('Processing file %s', args.file.name)
    logging.info('Validating structural requirements')

    schema = load_workload_schema()
    instance = parse_workload(args.file)
    error = validate(schema, instance)

    if error is not None:
        path = '/'.join(map(str, error.absolute_path))
        logging.error('File does not match schema at %s: %s', path, error)
        sys.exit(1)

    logging.info('Format OK')


def validate_environment(args):
    """
    Validate an environment description for JSSPP OSP.
    :param args: The command line arguments passed to this command.
    """
    logging.info('Processing file %s', args.file.name)
    logging.info('Validating structural requirements')

    schema = load_environment_schema()
    instance = parse_environment(args.file)
    error = validate(schema, instance)

    if error is not None:
        path = '/'.join(map(str, error.absolute_path))
        logging.error('File does not match schema at %s: %s', path, error)
        sys.exit(1)

    logging.info('Format OK')


def main():
    """
    Main entry point of the application.
    """
    parser = argparse.ArgumentParser(description=__description__)
    subparsers = parser.add_subparsers(title='Commands', dest='command')
    subparsers.required = True

    workload_parser = subparsers.add_parser('validate-workload', help='Validate a workload')
    workload_parser.add_argument('file', type=argparse.FileType('r'), help='The path to the workload description file')
    workload_parser.set_defaults(func=validate_workload)

    env_parser = subparsers.add_parser('validate-environment', help='Validate an environment description')
    env_parser.add_argument('file', type=argparse.FileType('r'), help='The path to the environment description file')
    env_parser.set_defaults(func=validate_environment)

    args = parser.parse_args()
    if args.func:
        return args.func(args)


if __name__ == '__main__':
    main()
