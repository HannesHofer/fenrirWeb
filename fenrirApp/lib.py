from bottle import TEMPLATE_PATH
from sqlite3 import connect, OperationalError
from os.path import dirname, realpath
from logging import debug
from bcrypt import gensalt, hashpw
from fenrir.filehandler import filehandler
from fenrir.fenrir import Fenrir

APPPATH = dirname(realpath(__file__))
TEMPLATE_PATH[:] = [f'{APPPATH}/views']
DBPATH = '/var/cache/fenrir/fenrir.sqlite'


def getdevices(dbpath=DBPATH) -> list:
    """ return all devices present in datavase

    :param dbpath: path to database
    returns list of row mapping or empty list for no result
    """
    results = []
    try:
        with connect(f'file:{dbpath}?mode=ro', timeout=10, check_same_thread=False, uri=True) as db:
            cursor = db.cursor()
            for res in cursor.execute('SELECT mac, IP, vendor, active from devices;').fetchall():
                results.append({'IP': res[1], 'MAC': res[0], 'VENDOR': res[2], 'ENABLED': res[3]})
    except OperationalError as e:
        debug(f'unable to open Database at {dbpath}: {e}')
    return results


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


def updateneededprofilesquery(updateset, needed):
    cmd = f'UPDATE vpnprofiles SET isneeded = {needed} WHERE '
    for i in range(len(updateset)):
        if i > 0:
            cmd += 'OR '
        cmd += 'name like ? '
    return cmd, tuple(updateset)


def updateondemandstate(dbpath=DBPATH):
    """ set isneeded for ondemand vpn settings

    :param dbpath: path to settings database
    """
    with connect(dbpath) as db:
        # get needed profilenames and needdefault
        cursor = db.cursor()
        result = cursor.execute('''SELECT ipconnectionmap.name, settings.ip
                                   FROM settings LEFT JOIN ipconnectionmap ON settings.ip = ipconnectionmap.ip
                                   WHERE settings.active = 1''')
        neededprofiles = set()
        needdefault = False
        for row in result.fetchall():
            if not row[0]:
                needdefault = True
            else:
                neededprofiles.add(row[0])
        # get current config
        result = cursor.execute('SELECT name, isdefault FROM vpnprofiles WHERE isneeded = 1')
        activeprofiles = set()
        hasdefault = False
        for row in result.fetchall():
            name, isdefault = row
            if isdefault:
                hasdefault = True
            else:
                activeprofiles.add(name)
        # handle default setting
        if hasdefault != needdefault:
            cursor.execute('UPDATE vpnprofiles SET isneeded = ? WHERE isdefault = 1', (1 if needdefault else 0,))
        # disable no longer needed connections
        cmd, params = updateneededprofilesquery(updateset=activeprofiles - neededprofiles, needed=0)
        if len(params) > 0:
            cursor.execute(cmd, params)
        # activate new needed profiles
        cmd, params = updateneededprofilesquery(updateset=neededprofiles - activeprofiles, needed=1)
        if len(params) > 0:
            cursor.execute(cmd, params)


def initDB(dbpath=DBPATH):
    Fenrir(inputinterface='', vpninterface='').initDB()


def changedbstate(dbpath=DBPATH, state=-1, ip='') -> int:
    """ change current setting for spoofing enabled/disabled

    :param dbpath: path to settings database
    :param state: state to change to (1=enable, 0=disable, -1=toggle)
    :param ip: ip of device to change state for

    change current spoof state to given state or toggle state.
    update device and settings databases
    """
    try:
        if state == -1:
            state = 0 if getstateforIP(dbpath=dbpath, ip=ip) > 0 else 1

        with connect(dbpath) as db:
            cursor = db.cursor()
            cursor.execute('INSERT OR REPLACE INTO settings(ip, active) values(?, ?);', (ip, state))
            cursor.execute('UPDATE devices SET active = ? WHERE IP = ?', (state, ip))

        updateondemandstate(dbpath=dbpath)
    except OperationalError as e:
        debug(f'unable to open Database at {dbpath}: {e}')
        state = 0

    return state


def getipprofilemapping(dbpath=DBPATH, name='%') -> dict:
    """ get IP/VPNProfile mapping

    :param dbpath: path to settings database

    returns dict of matching IP/VPNProfiles
    """
    returndict = {}
    try:
        with connect(dbpath) as db:
            cursor = db.cursor()
            results = cursor.execute("""SELECT ip, name FROM ipconnectionmap WHERE name like ?;""", (name,)).fetchall()
            for row in results:
                returndict[row[0]] = row[1]
    except OperationalError as e:
        debug(f'unable to query Database {dbpath}: {e}')

    return returndict


def isvpnconfigset(dbpath=DBPATH) -> bool:
    """ get if vpn config is set

    :param dbpath: path to settings database

    returns wether or not a valid vpn profile is present
    """
    try:
        with connect(dbpath) as db:
            cursor = db.cursor()
            results = cursor.execute('SELECT name from vpnprofiles LIMIT 1;').fetchone()
            if results:
                return True
    except OperationalError as e:
        debug(f'no VPN profile in {dbpath}: {e}')

    return False


def getvpnconfig(profilename=None, getauth=False, dbpath=DBPATH, passphrase=None) -> dict:
    """ get vpn config from database

    :param profilename: name for profile to be filtered for (empty for all configs)
    :param getauth: True or False depending if auth data should be returned
    :param dbpath: path to settings database
    :param passphrase: passphrase to be used for encryption. if empty default phrase (MAC Address) will be used


    returns dict of matching VPNConfigs
    """
    if not profilename:
        profilename = '%'

    returndict = {}
    try:
        with connect(dbpath) as db:
            cursor = db.cursor()
            results = cursor.execute("""SELECT name, description, isdefault, ondemand, username, password, config, id
                                        from vpnprofiles where name like ?""", (profilename, )).fetchall()
            valuedict = {}
            for i, result in enumerate(results):
                valuedict['profilename'] = result[0]
                valuedict['description'] = result[1]
                valuedict['isdefault'] = result[2]
                valuedict['ondemand'] = result[3]
                if getauth:
                    fh = filehandler(passphrase=passphrase)
                    valuedict['username'] = fh.decode(result[4].decode('utf-8')).decode('utf-8')
                    valuedict['password'] = fh.decode(result[5].decode('utf-8')).decode('utf-8')
                    valuedict['vpnconfig'] = fh.decode(result[6].decode('utf-8')).decode('utf-8')
                    valuedict['vpnprofileid'] = result[7]
                returndict[f'profile{i}'] = valuedict.copy()
    except OperationalError as e:
        debug(f'unable to query Database {dbpath}: {e}')

    return returndict


def storevpnsettings(vpnprofilename, vpnconfig, description, vpnuser, vpnpass,
                     dbpath=DBPATH, isdefault=False, ondemand=False,
                     passphrase=None, id=None) -> str:
    """ store given vpn settings encrypted in database

    :param vpnprofilename: name for which vpn settings will be stored. Is not encrypted and must be unique
    :param description: description of VPN profile
    :param isdefault: True or False depending if given config is default config
    :param ondemand: True of False depending if connection should established dynamically (when needed)
    :param vpnconfig: vpn config file to be stored. Is encrypted
    :param vpnusername: vpn username information to be stored. Is encrypted
    :param vpnpassword: vpn password information to be stored. Is encryptedAUTOINCREMENTAUTOINCREMENT
    :param dbpath: path to settings database
    :param passphrase: passphrase to be used for encryption. if empty default phrase (MAC Address) will be used
    :param id: replace existing configuration for given id
    """
    try:
        fh = filehandler(passphrase=passphrase)
        cipherconfig = fh.encode(vpnconfig)
        cipheruser = fh.encode(vpnuser)
        cipherpass = fh.encode(vpnpass)

        with connect(dbpath) as db:
            cursor = db.cursor()
            cmd = 'INSERT INTO vpnprofiles(name, description, isdefault, ondemand, config, username, password)'
            cmdvalues = 'values(?,?,?,?,?,?,?)'
            parameters = (vpnprofilename, description, isdefault, ondemand, cipherconfig, cipheruser, cipherpass)
            if id:
                cmd = cmd.replace('INSERT', 'REPLACE ')
                cmd = cmd.replace(')', ',id)')
                cmdvalues = cmdvalues.replace('?)', '?,?)')
                parameters += (id,)
            else:
                if cursor.execute('SELECT name from vpnprofiles where name = ?', (vpnprofilename, )).fetchall():
                    return f'VPNprofile with name {vpnprofilename} already exists'

            cursor.execute(cmd + cmdvalues, parameters)
    except Exception as e:
        return str(e)

    return ''


def deletevpnconfig(profilename=None, dbpath=DBPATH) -> str:
    """ delete vpn config from database

    :param profilename: name for profile to be deleted
    :param dbpath: path to settings database

    returns error or empty string on success
    """
    if not profilename:
        return 'refusing to delete unspecified (all) profiles'

    try:
        with connect(dbpath) as db:
            cursor = db.cursor()
            cursor.execute('DELETE from vpnprofiles where name like ?', (profilename, )).fetchall()
    except Exception as e:
        return str(e)

    return ''


def deletemappingcmd(ip=None, dbpath=DBPATH) -> str:
    """ delete mapping from database

    :param ip: ip for mapping to be deleted
    :param dbpath: path to settings database

    returns error or empty string on success
    """
    if not ip:
        return 'refusing to delete unspecified (all) mappings'

    try:
        with connect(dbpath) as db:
            cursor = db.cursor()
            cursor.execute('DELETE from ipconnectionmap where ip like ?', (ip, )).fetchall()
    except Exception as e:
        return str(e)

    return ''


def passwordtablepresent(dbpath=DBPATH) -> bool:
    """ check wether or not VPN Profile password protection table is present

    :param dbpath: path to settings database
    """
    try:
        with connect(dbpath) as db:
            cursor = db.cursor()
            ret = cursor.execute('SELECT name FROM sqlite_master WHERE type="table" AND name="profilepassword";').fetchone()
            return ret != None
    except Exception:
        return False


def createpasswordcmd(password, dbpath=DBPATH) -> str:
    """ create password for VPN password protection

    :param password: password to be used for VPNProfile protection
    :param dbpath: path to settings database
    """

    try:
        with connect(dbpath) as db:
            cursor = db.cursor()
            if (passwordtablepresent(dbpath=dbpath)):
                return 'Password already set.'
            salt = gensalt()
            hpassword = hashpw(password.encode('utf-8'), salt)
            cursor.execute('CREATE TABLE profilepassword(salt STRING NOT NULL, hash STRING NOT NULL);')
            cursor.execute('INSERT INTO profilepassword(salt, hash) values(?,?);', (salt, hpassword))
    except Exception as e:
        return str(e)

    return ''


def addmappingcmd(ip=None, name=None, dbpath=DBPATH) -> str:
    """ delete mapping from database

    :param ip: ip for mapping to be added
    :param name: name for mapping to be added
    :param dbpath: path to settings database

    returns error or empty string on success
    """
    if not ip or not name:
        return 'refusing to add unspecified ip or name'

    try:
        with connect(dbpath) as db:
            cursor = db.cursor()
            cursor.execute('REPLACE INTO ipconnectionmap(ip, name) values(?, ?)', (ip, name)).fetchall()
    except Exception as e:
        return str(e)

    return ''


def is_authenticated_user(username=None, password=None, dbpath=DBPATH):
    """ check if password is correct

    :param username: just for completeness. Currently not used.
    :param password: password to check
    :param dbpath: path to settings database

    return true if password is correct otherwise false
    """
    try:
        with connect(dbpath) as db:
            cursor = db.cursor()
            ret = cursor.execute('SELECT salt, hash FROM profilepassword LIMIT 1;').fetchone()
            if ret:
                hpassword = hashpw(password.encode('utf-8'), ret[0])
                if hpassword == ret[1]:
                    return True
    except Exception as e:
        debug(f'uable to query auth state {dbpath}: {e}')

    return False
