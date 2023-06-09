from bottle import route, request, response, Bottle, jinja2_template, auth_basic
from . lib import storevpnsettings, getvpnconfig, deletevpnconfig, is_passwordset, \
                  getipprofilemapping, getdevices, addmappingcmd, deletemappingcmd, \
                  is_authenticated_user, createpasswordcmd, setvpnpassword, \
                  needspasswordcheck, set_needspasswordcheck, is_passworusedforencryption, \
                  changepasswordcmd
from json import loads, dumps


app = Bottle()


def is_authenticated_header(authheader):
    """ check if authentication header is present and correct

    return true if authentication is present and correct; otherwise return false
    """
    if not authheader or len(authheader) < 2:
        return False
    return is_authenticated_user(username=authheader[0], password=authheader[1])


@app.route('/storeconfig', method=['POST'])
@auth_basic(is_authenticated_user)
@route('/storeconfig', method=['POST'])
def storeconfig(replace=False):
    """ store config settings

    return error or success messages when storing succeeds/fails
    """
    postdata = request.body.read()
    jsondata = loads(postdata.decode('utf-8'))
    response.content_type = 'text/json'
    if 'vpnconfig' not in jsondata.keys() or 'username' not in jsondata.keys() or \
       'password' not in jsondata.keys() or 'profilename' not in jsondata.keys():
        return dumps({'error': True, 'text': 'unable to get needed parameters'})

    if jsondata['profilename'] == '':
        return dumps({'error': True, 'text': 'refusing to create profile with no name'})

    id = None
    if replace:
        id = jsondata['vpnprofileid']

    encpassword = None
    if is_passworusedforencryption():
        if not request.auth or len(request.auth) < 2:
            return dumps({'error': False, 'text': 'encryption password not set'})
        encpassword = request.auth[1]
    ret = storevpnsettings(vpnprofilename=jsondata['profilename'], vpnuser=jsondata['username'], vpnpass=jsondata['password'],
                           vpnconfig=jsondata['vpnconfig'], description=jsondata['description'], passphrase=encpassword,
                           isdefault=jsondata['isdefault'], ondemand=jsondata['ondemand'], id=id)
    if ret and len(ret) > 0:
        return dumps({'error': True, 'text': 'unable to get store configuration: ' + ret})

    action = 'added'
    if replace:
        action = 'modified'
    return dumps({'error': False, 'text': f'successfully {action} configuration'})


@app.route('/ispasswordusedforencryption', method=['POST'])
@auth_basic(is_authenticated_user)
@route('/ispasswordusedforencryption', method=['POST'])
def ispasswordusedforencryption():
    return dumps({'error': False, 'checked': is_passworusedforencryption()})

@app.route('/replaceconfig', method=['POST'])
@auth_basic(is_authenticated_user)
@route('/replaceconfig', method=['POST'])
def replaceconfig():
    """ replace config settings

    return error or success messages when storing succeeds/fails
    """
    return storeconfig(replace=True)


@app.route('/deleteconfig', method=['POST'])
@auth_basic(is_authenticated_user)
@route('/deleteconfig', method=['POST'])
def deleteconfig():
    """ delete config settings

    return error or success messages when deleting succeeds/fails
    """
    postdata = request.body.read()
    jsondata = loads(postdata.decode('utf-8'))
    response.content_type = 'text/json'

    profile = jsondata['profilename']
    if getipprofilemapping(name=profile):
        return dumps({'error': True,
                      'text': f"""VPNProfile '{profile}' is referenced in IP/VPNProfile mapping.</br>
                                  remove all occurences of '{profile}' in IP/VPNProfile mapping first."""})
    ret = deletevpnconfig(profilename=profile)
    if ret:
        return dumps({'error': True, 'text': ret})

    return dumps({'error': False, 'text': 'successfully deleted configuration'})


@app.route('/deletemapping', method=['POST'])
@route('/deletemapping', method=['POST'])
def deletemapping():
    """ delete vpnmapping settings

    return error or success messages when deleting succeeds/fails
    """
    postdata = request.body.read()
    jsondata = loads(postdata.decode('utf-8'))
    response.content_type = 'text/json'

    ret = deletemappingcmd(ip=jsondata['profilename'])
    if ret:
        return dumps({'error': True, 'text': ret})

    return dumps({'error': False, 'text': 'successfully deleted mapping'})


@app.route('/addmapping', method=['POST'])
@route('/addmapping', method=['POST'])
def addmapping():
    """ add vpnmapping settings

    return error or success messages when adding succeeds/fails
    """
    postdata = request.body.read()
    jsondata = loads(postdata.decode('utf-8'))
    response.content_type = 'text/json'

    ret = addmappingcmd(ip=jsondata['ip'], name=jsondata['name'])
    if ret:
        return dumps({'error': True, 'text': ret})

    return dumps({'error': False, 'text': 'successfully added mapping'})


@app.route('/changepassword', method=['POST'])
@route('/changepassword', method=['POST'])
def changepassword():
    """ change current VPNProfile protection password

    return error or success messages when changing succeeds/fails
    """
    postdata = request.body.read()
    jsondata = loads(postdata.decode('utf-8'))
    response.content_type = 'text/json'

    if jsondata['password'] != jsondata['passwordrepeat']:
        return dumps({'error': True, 'text': 'passwords do not match'})

    if not is_authenticated_user(username=None, password=jsondata['currentpassword']):
        return dumps({'error': True, 'text': 'current password ist not correct'})

    ret = changepasswordcmd(currentpassword=jsondata['currentpassword'], password=jsondata['password'],
                            usedforencryption=jsondata['passwordusedforencryption'] == 'on')
    if ret:
        return dumps({'error': True, 'text': ret})

    return dumps({'error': False, 'text': 'successfully changed password.'})


@app.route('/createpassword', method=['POST'])
@route('/createpassword', method=['POST'])
def createpassword():
    """ create password for VPNProfile protection

    return error or success messages when creating succeeds/fails
    """
    postdata = request.body.read()
    jsondata = loads(postdata.decode('utf-8'))
    response.content_type = 'text/json'

    if jsondata['password'] != jsondata['passwordrepeat']:
        return dumps({'error': False, 'text': 'passwords do not match'})

    ret = createpasswordcmd(password=jsondata['password'], usedforencryption=jsondata['passwordusedforencryption'] == 'on')
    if ret:
        return dumps({'error': True, 'text': ret})

    return dumps({'error': False, 'text': 'successfully created password. click unlock again. Username field can be ignored.'})


@app.route('/passwordset', method=['POST'])
@route('/passwordset', method=['POST'])
def passwordset():
    """ check if VPNProfile password is set

    return wether or not VPN Profile password is set
    """
    return dumps({'error': False, 'value': is_passwordset()})


@app.route('/getvpnconfigurations', method=['GET', 'POST'])
@route('/getvpnconfigurations', method=['GET', 'POST'])
def getvpnconfigurations():
    """ get all stored vpn configurations

    retruns VPN Configuration
    """
    profilename = ''
    getauth = False
    if request.method == 'POST':
        postdata = request.body.read()
        jsondata = loads(postdata.decode('utf-8'))
        profilename = jsondata.get('profilename')
        getauth = jsondata.get('completeData') and is_authenticated_header(request.auth)
    else:
        profilename = request.args.get('profilename')

    passphrase = None
    if getauth and len(request.auth) > 1:
        passphrase = request.auth[1]

    return dumps(getvpnconfig(profilename=profilename, getauth=getauth, passphrase=passphrase))


@app.route('/getmappings', method=['GET', 'POST'])
@route('/getmappings', method=['GET', 'POST'])
def getmappings():
    """ get all stored IP/VPN mappings """
    return dumps(getipprofilemapping())


@app.route('/settingsauthenticated')
@auth_basic(is_authenticated_user)
def authtest():
    if needspasswordcheck() and request.auth:
        set_needspasswordcheck(not setvpnpassword(password=request.auth[1]))

    return config(isauthenticated=True)


@app.route('/settings')
@route('/settings')
def config(isauthenticated=False):
    """ send config page to store settings """
    vpnconfigs = getvpnconfig()
    ipmappings = getipprofilemapping()
    devices = getdevices()
    if not isauthenticated:
        isauthenticated = is_authenticated_header(request.auth)
        if needspasswordcheck() and request.auth:
            set_needspasswordcheck(not setvpnpassword(password=request.auth[1]))
    return jinja2_template('settings', vpnconfigs=vpnconfigs,
                           vpnmappinconfig=ipmappings, devices=devices,
                           isauthenticated=isauthenticated, needscreatepassword=True)
