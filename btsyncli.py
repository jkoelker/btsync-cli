#!/usr/bin/env python
""" cli interface for btsync """

import argparse
import btsync
import locale
import os
import sys


try:
    import simplejson as json
except ImportError:
    import json

from blessings import Terminal


def sync_dir_exists(client, path):
    """
    checks if directory exists in btsync already and returns bool

    Keyword arguments:
    client -- the btsync client
    path -- a file path to check against btsync
    """

    folder_list = client.sync_folders
    for folder in folder_list:
        if os.path.abspath(path) == os.path.abspath(folder['name']):
            return True


def add_sync_folder(client, path, secret=None):
    """
    Checks for a a directory 'path' on the file system and creates it if it
    does not exist then setup ownership/perms. If seceret is not passed in,
    we genrate one and then add 'path' to btsync.

    Keyword arguments:
    client -- the btsync client
    path -- a filesystem path to create/add to btsync
    secret -- a btsync secret.
    """

    if sync_dir_exists(client, path):
        print "This directory is already being synced. Exiting"
        sys.exit(1)
    if not secret:
        secret = client.generate_secret()['rosecret']
    if not os.path.exists(path):
        os.makedirs(path)
        os.chmod(path, 1755)
        os.chown(path, -1, 1002)
    client.add_sync_folder(path, secret)


def parse_status(status_string):
    """
    converts status_string into something human readable

    Keyword arguments:
    status_string -- btsync.Client.sync['folders']['peers']['status']
    """

    l = status_string.split('>')
    locale.setlocale(locale.LC_ALL, '')
    code = locale.getpreferredencoding()
    if 'downarrow' in l[0]:
        l[0] = u'\u2B07'.encode(code)
    if 'uparrow' in l[0]:
        l[0] = u'\u2B06'.encode(code)
    return ''.join(l)


def pprint_sync_folders(sync_folders):
    """
    prints out a pretty status for all btsync folders

    Keyword arguments:
    status_string -- btsync.Client.sync_folders
    """

    term = Terminal()
    width = term.width
    for folder in sync_folders:
        print(term.green(folder['name']))
        for peer in folder['peers']:
            new_status = parse_status(peer['status'])
            padding = ' '*(width-5-len(new_status)-(len(peer['name'])))
            print "  |--%s%s%s" % (peer['name'], padding, new_status)


def main():
    """ main """
    parser = argparse.ArgumentParser(
        description='A command line interface for btsync.')
    parser.add_argument('-l', '--list', action='store_true', dest='l',
                        help='list sync folders')
    parser.add_argument('-a', '--add', action='store', dest='folder',
                        help='add a sync folder')
# not yet implimented
#    parser.add_argument('-d', '--dump', action='store_true', dest='dump',
#                        help='dump json output for all sync folders')
#    parser.add_argument('-i', '--import', action='store_true', dest='import',
#                        help='add all folders in a json dump')
#    parser.add_argument('-c', '--config', action='store_true', dest='config',
#                        help='use values in you btsync config file')
#    parser.add_argument('-H', '--host', action='store_true', dest='host',
#                        help='the host of your btsync webservice')
#    parser.add_argument('-u', '--user', action='store_true', dest='user',
#                        help='your btsync username')
#    parser.add_argument('-p', '--pass', action='store_true', dest='pass',
#                        help='prompt for btsync password')
    parser.add_argument('-s', '--secret', action='store', default=None,
                        dest='secret',
                        help='a btsync secret')

    args = parser.parse_args()
    config_file = '/var/lib/btsync/.sync/sync.conf'
    with open(config_file) as config_file:
        config = json.load(config_file)

    sync_client = btsync.Client(
        host=config['webui']['listen'].split(':')[0],
        port=config['webui']['listen'].split(':')[1],
        username=config['webui']['login'],
        password=config['webui']['password'])

    if args.l:
        pprint_sync_folders(sync_client.sync_folders)
    if args.folder:
        sync_path = os.path.abspath(args.folder)
        add_sync_folder(sync_client, sync_path, args.secret)

if __name__ == "__main__":
    main()
