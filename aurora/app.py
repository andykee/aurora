import os
import sys
import argparse
import webbrowser

from cheroot.wsgi import Server
from sqlalchemy.orm import scoped_session
from flask import Flask, _app_ctx_stack

from aurora.database import new_engine, new_session, Base
from aurora import models, config
from aurora.api import api
from aurora import util

HOST = 'localhost'
PORT = 5000

#CONFIG = {
#    'autolaunch_browser': False,
#    'ignore_duplicates': True
#}


app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello World!'

app.register_blueprint(api, url_prefix='/api')


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
                        default=PORT)

    parser.add_argument('-H', '--host', dest='host',
                        help='IP to serve HTTP files at (default: localhost)',
                        default=HOST)
    
    args = parser.parse_args(argv)

    # The default behavior should be as follows:
    # * If the user provides a catalog file to open, open it
    # * If the user does not provide a catalog file to open:
    #     * Webapp should prompt them to either open a file
    #       or specify the location for a new one.
    #
    # In the meantime, we'll just create one in memory

    if os.path.isfile(args.input):
        # User provided a catalog file
        engine = new_engine(catalog=args.input)
    else:
        engine = new_engine()

    session = new_session(engine)
    Base.metadata.create_all(bind=engine)


    api.session = scoped_session(session, scopefunc=_app_ctx_stack)


    # We need to read the config from the db here to figure out what to do re: a bunch of stuff


    server = Server((args.host, args.port), app)

    if args.live:
        print("Fuck it, we'll do it live")
    else:
        pass

    # Stand up the webserver
    print(f'Running Aurora on http://{args.host}:{args.port}')

    try:
        server.start()
        if CONFIG['autolaunch_browser']:
            webbrowser.open(f'http://{HOST}:{PORT}', new=2)
    except KeyboardInterrupt:
        print(f'\n\nShutting down Aurora')
        server.stop()

