from bottle import route, run, static_file, jinja2_template, TEMPLATE_PATH, Bottle, request, response
import sqlite3
import os
import json

APPPATH=os.path.dirname(os.path.realpath(__file__))
TEMPLATE_PATH[:] = [f'{APPPATH}/views']
DBPATH='/var/cache/fenrir/'

app = application = Bottle()

def getdevices(dbpath=f'{DBPATH}netdevices.sqlite'):
    try:
        with sqlite3.connect(f'file:{dbpath}?mode=ro', timeout=10, check_same_thread=False, uri=True) as db:
            cursor = db.cursor()
            return cursor.execute('SELECT mac, IP, vendor, active from devices;').fetchall()
    except:
        return ''

def getstateforIP(dbpath, ip):
    try:
        with sqlite3.connect(f'file:{dbpath}?mode=ro', timeout=10, check_same_thread=False, uri=True) as db:
            cursor = db.cursor()
            return cursor.execute('SELECT active from settings WHERE ip = ?;', (ip, )).fetchone()
    except:
        return None


def changedbstate(dbpath=f'{DBPATH}settings.sqlite', state=-1, ip='', devicespath=f'{DBPATH}netdevices.sqlite'):
    try:
        if state == -1:
            currentstate = getstateforIP(dbpath=dbpath, ip=ip)
            comparestate = int(currentstate[0]) if currentstate and len(currentstate) > 0 else 0
            state = 0 if comparestate > 0 else 1

        with sqlite3.connect(dbpath) as db:
            cursor = db.cursor()
            cursor.execute('CREATE TABLE IF NOT EXISTS settings(ip TEXT PRIMARY KEY, ACTIVE INTEGER DEFAULT 0);')
            cursor.execute('INSERT OR REPLACE INTO settings(ip, active) values(?, ?);', (ip, state))

        with sqlite3.connect(devicespath) as db:
            cursor = db.cursor()
            cursor.execute('UPDATE devices SET active = ? WHERE IP = ?', (state, ip))
    except:
        state = 0

    return state


@app.route('/index.html')
@route('/index.html')
@app.route('/')
@route('/')
def index():
    results = []
    for res in getdevices(dbpath=f'{DBPATH}netdevices.sqlite'):
        results.append({'IP': res[1], 'MAC': res[0], 'VENDOR': res[2], 'ENABLED': res[3]})
    return jinja2_template('index', results=results)


@route('/static/<filename>')
@app.route('/static/<filename>')
def static_files(filename):
    return static_file(filename, root=f'{APPPATH}/static/')


@route('/favicon.ico')
@app.route('/favicon.ico')
def favicon():
    return static_file('favicon.ico', root=f'{APPPATH}/static/')


@route('/enable/<ip>', method = ['GET'])
@app.route('/enable/<ip>', method = ['GET'])
def enable(ip):
    changedbstate(dbpath=f'{DBPATH}settings.sqlite', state=1, ip=ip)
    return '<! -- ENABLED --> <html><head><meta HTTP-EQUIV="REFRESH" content="0; url=/"></head></html>'


@route('/disable/<ip>', method = ['GET'])
@app.route('/disable/<ip>', method = ['GET'])
def disable(ip):
    changedbstate(dbpath=f'{DBPATH}settings.sqlite', state=0, ip=ip)
    return '<! -- DISABLED --> <html><head><meta HTTP-EQUIV="REFRESH" content="0; url=/"></head></html>'


@app.route('/changestate', method = ['POST'])
@route('/changestate', method = ['POST'])
def changestate():
    postdata = request.body.read()
    if len(postdata) < 0:
        return '{}'

    STATES = {'enable' : 1, 'disable' : 0, 'toggle': -1}
    jsondata = json.loads(postdata.decode('utf-8'))
    if 'ip' not in jsondata.keys() or 'state' not in jsondata.keys() or jsondata['state'] not in STATES:
        return '{}'

    currentstate = changedbstate(dbpath=f'{DBPATH}settings.sqlite', state=STATES[jsondata['state']], ip=jsondata['ip'])
    jsondata['state'] = list(STATES.keys())[list(STATES.values()).index(currentstate)] + 'd'

    response.content_type = 'application/json'
    return json.dumps(jsondata)


if __name__ == "__main__":
    run(host='0.0.0.0', port=8080, debug=True)
