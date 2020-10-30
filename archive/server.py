import os
import sys
import argparse


def parse_arguments(argv):
    parser = argparse.ArgumentParser(
        description='Start Aurora server on http://<host>:<port>'
    )
    
    parser.add_argument(dest='path', nargs='?',
                        help='Path where to find the Aurora content',
                        default='.')

    parser.add_argument('-p', '--port', dest='port',
                        help='Port to serve HTTP files at (default: 5000)',
                        default=DEFAULTS['port'])

    parser.add_argument('-H', '--host', dest='host',
                        help='IP to serve HTTP files at (default: localhost)',
                        default=DEFAULTS['host'])
    
    parser.add_argument('-c', '--config', dest='config',
                        help='Config file for the application (default: conf.py)',
                        default=DEFAULTS['config_file'])

    args = parser.parse_args(argv)

    return args


def main(argv=sys.argv[1:]):

    # TODO: need to add which directory to poll
    # I think we might actually just want to point to a config.py or something
    parser = argparse.ArgumentParser(description='Aurora server')
    args = parser.parse_args(argv)

    port = args.port if args.port else DEFAULTS['port']
    host = args.host if args.host else DEFAULTS['host']

    print(f'Running Aurora on http://{host}:{port}')

