from bottle import route, run, static_file, jinja2_template, TEMPLATE_PATH, Bottle, request, response
from sqlite3 import connect, OperationalError
from os.path import dirname, realpath
from json import loads, dumps
from argparse import ArgumentParser
from logging import debug, basicConfig, INFO, DEBUG
from sys import stdout
from fenrir.filehandler import filehandler

APPPATH = dirname(realpath(__file__))
TEMPLATE_PATH[:] = [f'{APPPATH}/views']
DBPATH = '/var/cache/fenrir/'
VPNCONFIG = '/storage/vpn.conf'
VPNAUTH = '/storage/vpn.auth'

app = application = Bottle()


def getdevices(dbpath=f'{DBPATH}netdevices.sqlite') -> str:
    """ return all devices present in datavase

    :param dbpath: path to database
    """
    try:
        with connect(f'file:{dbpath}?mode=ro', timeout=10, check_same_thread=False, uri=True) as db:
            cursor = db.cursor()
            return cursor.execute('SELECT mac, IP, vendor, active from devices;').fetchall()
    except OperationalError as e:
        debug(f'unable to open Database at {dbpath}: {e}')
        return ''


def getstateforIP(dbpath, ip) -> int:
    """ return state for given IP (default 0)

    :param dbpath: path to database
    :param ip: ip to do state lookup for
    """
    try:
        with connect(f'file:{dbpath}?mode=ro', timeout=10, check_same_thread=False, uri=True) as db:
            cursor = db.cursor()
            dbval = cursor.execute('SELECT active from settings WHERE ip = ?;', (ip, )).fetchone()
            return int(dbval[0]) if dbval and len(dbval) > 0 else 0
    except OperationalError as e:
        debug(f'unable to open Database at {dbpath}: {e}')
        return 0


def changedbstate(dbpath=f'{DBPATH}settings.sqlite', state=-1, ip='', devicespath=f'{DBPATH}netdevices.sqlite') -> int:
    """ change current setting for spoofing enabled/disabled

    :param dbpath: path to settings database
    :param state: state to change to (1=enable, 0=disable, -1=toggle)
    :param ip: ip of device to change state for
    :param devicespath: path of devices database

    change current spoof state to given state or toggle state.
    update device and settings databases
    """
    try:
        if state == -1:
            state = 0 if getstateforIP(dbpath=dbpath, ip=ip) > 0 else 1

        with connect(dbpath) as db:
            cursor = db.cursor()
            cursor.execute('CREATE TABLE IF NOT EXISTS settings(ip TEXT PRIMARY KEY, ACTIVE INTEGER DEFAULT 0);')
            cursor.execute('INSERT OR REPLACE INTO settings(ip, active) values(?, ?);', (ip, state))

        with connect(devicespath) as db:
            cursor = db.cursor()
            cursor.execute('UPDATE devices SET active = ? WHERE IP = ?', (state, ip))
    except OperationalError as e:
        debug(f'unable to open Database at {dbpath}: {e}')
        state = 0

    return state


@app.route('/index.html')
@route('/index.html')
@app.route('/')
@route('/')
def index():
    """ render index template """
    results = []
    for res in getdevices(dbpath=f'{DBPATH}netdevices.sqlite'):
        results.append({'IP': res[1], 'MAC': res[0], 'VENDOR': res[2], 'ENABLED': res[3]})
    return jinja2_template('index', results=results)


@route('/static/<filename>')
@app.route('/static/<filename>')
def static_files(filename):
    """ retrun static files in /static/"""
    return static_file(filename, root=f'{APPPATH}/static/')


@route('/favicon.ico')
@app.route('/favicon.ico')
def favicon():
    """ return favicon.ico for browsers located in /static/ """
    return static_file('favicon.ico', root=f'{APPPATH}/static/')


@route('/enable/<ip>', method=['GET'])
@app.route('/enable/<ip>', method=['GET'])
def enable(ip):
    """ enable spoofing for given IP Address

    :param ip: IP Address to enable spoofing for
    """
    changedbstate(dbpath=f'{DBPATH}settings.sqlite', state=1, ip=ip)
    return '<! -- ENABLED --> <html><head><meta HTTP-EQUIV="REFRESH" content="0; url=/"></head></html>'


@route('/disable/<ip>', method=['GET'])
@app.route('/disable/<ip>', method=['GET'])
def disable(ip):
    """ disable spoofing for given IP Address

    :param ip: IP Address to disable spoofing for
    """
    changedbstate(dbpath=f'{DBPATH}settings.sqlite', state=0, ip=ip)
    return '<! -- DISABLED --> <html><head><meta HTTP-EQUIV="REFRESH" content="0; url=/"></head></html>'


@app.route('/changestate', method=['POST'])
@route('/changestate', method=['POST'])
def changestate():
    """ change spoofing for given IP Address and state

    post body must contain valid json with ip and state keys
    ip is IPAddress for which change to change spoof state
    state is state to change to (1=enable, 0=disable, -1=toggle)
    """
    postdata = request.body.read()
    if len(postdata) < 0:
        return '{}'

    STATES = {'enable': 1, 'disable': 0, 'toggle': -1}
    jsondata = loads(postdata.decode('utf-8'))
    if 'ip' not in jsondata.keys() or 'state' not in jsondata.keys() or jsondata['state'] not in STATES:
        return '{}'

    currentstate = changedbstate(dbpath=f'{DBPATH}settings.sqlite', state=STATES[jsondata['state']], ip=jsondata['ip'])
    jsondata['state'] = list(STATES.keys())[list(STATES.values()).index(currentstate)] + 'd'

    response.content_type = 'application/json'
    return dumps(jsondata)


@app.route('/storeconfig', method=['POST'])
@route('/storeconfig', method=['POST'])
def storeconfig():
    """ store config settings

    return error or success messages when storing succeeds/fails
    """
    postdata = request.body.read()
    jsondata = loads(postdata.decode('utf-8'))
    response.content_type = 'text/html'
    if 'vpnconfig' not in jsondata.keys() or 'vpnauth' not in jsondata.keys():
        return '<div class="alert alert-danger" role="alert">unable to get needed parameters</div>'

    try:
        fh = filehandler()
        cipherconfig = fh.encode(jsondata['vpnconfig'])
        cipherauth = fh.encode(jsondata['vpnauth'])

        open(VPNCONFIG, 'w').write(cipherconfig.decode('utf-8'))
        open(VPNAUTH, 'w').write(cipherauth.decode('utf-8'))
    except Exception as e:
        return f'<div class="alert alert-danger" role="alert">unable to get store configuration: {str(e)}</div>'

    return '<div class="alert alert-success" role="alert">Successfully stored config</div>'


@app.route('/config')
@route('/config')
def config():
    """ send config page to store settings """
    return static_file('config.html', root=f'{APPPATH}/static/')


def main() -> None:
    """ main method

    parse given commandline arguments
    start webserver
    initialise logging
    """
    parser = ArgumentParser()
    parser.add_argument('--debug', help='run in debug mode', action='store_true')
    parser.add_argument('--vpnconfigfile', help='config file for vpn service (openvpn)')
    parser.add_argument('--vpnauthfile', help='auth file (username/password) for vpnservice')
    args = parser.parse_args()
    basicConfig(stream=stdout, level=DEBUG if args.debug else INFO)
    if args.vpnconfigfile:
        global VPNCONFIG
        VPNCONFIG = args.vpnconfigfile
    if args.vpnauthfile:
        global VPNAUTH
        VPNAUTH = args.vpnauthfile
    run(host='0.0.0.0', port=8080, debug=args.debug)


if __name__ == "__main__":
    main()
