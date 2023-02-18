from bottle import static_file, jinja2_template, request, response, Bottle
from lib import DBPATH, getdevices, changedbstate, APPPATH, isvpnconfigset
from json import dumps, loads


app = Bottle()


@app.route('/static/<filename>')
def static_files(filename):
    """ retrun static files in /static/"""
    return static_file(filename, root=f'{APPPATH}/static/')


@app.route('/favicon.ico')
def favicon():
    """ return favicon.ico for browsers located in /static/ """
    return static_file('favicon.ico', root=f'{APPPATH}/static/')


@app.route('/index.html')
@app.route('/')
def index():
    """ render index template """
    return jinja2_template('index', results=getdevices(), hasprofiles=isvpnconfigset())


@app.route('/enable/<ip>', method=['GET'])
def enable(ip):
    """ enable spoofing for given IP Address

    :param ip: IP Address to enable spoofing for
    """
    changedbstate(dbpath=DBPATH, state=1, ip=ip)
    return '<! -- ENABLED --> <html><head><meta HTTP-EQUIV="REFRESH" content="0; url=/"></head></html>'


@app.route('/disable/<ip>', method=['GET'])
def disable(ip):
    """ disable spoofing for given IP Address

    :param ip: IP Address to disable spoofing for
    """
    changedbstate(dbpath=DBPATH, state=0, ip=ip)
    return '<! -- DISABLED --> <html><head><meta HTTP-EQUIV="REFRESH" content="0; url=/"></head></html>'


@app.route('/changestate', method=['POST'])
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

    currentstate = changedbstate(dbpath=DBPATH, state=STATES[jsondata['state']], ip=jsondata['ip'])
    jsondata['state'] = list(STATES.keys())[list(STATES.values()).index(currentstate)] + 'd'

    response.content_type = 'application/json'
    return dumps(jsondata)
