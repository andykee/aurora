import os
import sys
import argparse
import webbrowser

from aurora.database import new_engine, new_session, Base
from aurora import util

DEFAULT_PORT = 5000
DEFAULT_HOST = 'localhost'

CONFIG = {
    'autolaunch_browser': True,
    'ignore_duplicates': True,
}

#DRIVERS = [
#    {'driver': JSON, 'pattern': '*.json'},
#    {'driver': PNG, 'pattern': '*.png'}
#]

def main(argv=sys.argv[1:]):
    
    parser = argparse.ArgumentParser(
        description='Start Aurora on http://<host>:<port>'
    )
    
    parser.add_argument(dest='input', nargs='?',
                        help='Path where to find Aurora content or catalog file',
                        default='.')

    parser.add_argument('--live', dest='live',
                        help='Run Aurora in live mode',
                        action='store_true')

    parser.add_argument('-p', '--port', dest='port',
                        help='Port to serve HTTP files at (default: 5000)',
                        default=DEFAULT_PORT)

    parser.add_argument('-H', '--host', dest='host',
                        help='IP to serve HTTP files at (default: localhost)',
                        default=DEFAULT_HOST)
    
    args = parser.parse_args(argv)

    if os.path.isfile(args.input):
        engine = new_engine(catalog=args.input)
        session = new_session(engine)
    else:
        files = util.walk_dir(args.input)

        engine = new_engine()
        session = new_session(engine)


    if args.live:
        print("Fuck it, we'll do it live")

    # Stand up the webserver
    print(f'Running Aurora on http://{args.host}:{args.port}')

    #if CONFIG['autolaunch_browser']:
    #    webbrowser.open(f'http://{host}:{port}', new=2)
