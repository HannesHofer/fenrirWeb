from bottle import Bottle, run
from logging import basicConfig, INFO, DEBUG
from sys import stdout
from argparse import ArgumentParser
from . view_main import app as main_app
from . view_config import app as config_app
from . lib import initDB, set_needspasswordcheck, checkvpnpassword, is_passworusedforencryption


def make_app() -> Bottle:
    """ combine apps (views) and return new app """
    app = Bottle()
    app.merge(main_app)
    app.merge(config_app)
    return app


app = make_app()


def main() -> None:
    """ main method

    parse given commandline arguments
    start webserver
    initialise logging
    """
    parser = ArgumentParser()
    parser.add_argument('--debug', help='run in debug mode', action='store_true')
    args = parser.parse_args()
    basicConfig(stream=stdout, level=DEBUG if args.debug else INFO)
    initDB()
    set_needspasswordcheck(is_passworusedforencryption() and not checkvpnpassword())
    run(app, host='0.0.0.0', port=8080, debug=args.debug, reloader=True)


if __name__ == "__main__":
    main()
