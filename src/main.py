import os
import argparse

from waitress import serve

from . import server
from .config import make_config
from . import sql

def main():
    parser = argparse.ArgumentParser(description= 'telegram bot')
    subparsers = parser.add_subparsers(required=True, dest='subcommand')
    # database
    database_parser = subparsers.add_parser('db', help='database related commands')
    database_parser.add_argument('-c', '--create', dest='dbname', required=False, help='create new database')
    database_parser.add_argument('-i', '--insert', dest='row', action='store_true', help='insert row')
    database_parser.add_argument('-g', '--get-status', dest='id')
    # config
    config_parser = subparsers.add_parser('config', help='config related commands')
    config_parser.add_argument('-t', '--token', required=True, help='telegram bot token')
    # server
    server_parser = subparsers.add_parser('server', help='server related commands')
    server_parser.add_argument('-d', '--debug', action='store_true', help='start in debug mode')
    server_parser.add_argument('-p', '--port', default=5000, help='listen port')
    server_parser.add_argument('-ip', '--address', dest='ip', default='127.0.0.1', help='bind ip')


    args = vars(parser.parse_args())
    subcommand = args.pop('subcommand')
    if args['subcommand'] == 'config':
        make_config(args, 'config.xml')

    elif args['subcommand'] == 'server':
        debug = args['debug']
        ip = args['ip'] 
        port = int(args['port'])

        if debug:
            server.app.run(debug=True, host=ip, port=port)
        else:
            print('run server on {0}:{1} in production mode'.format(ip, port))
            serve(server.app, host=ip, port=port, threads=4)

    elif args['subcommand'] == 'db':
        dbname = args['dbname']
        row = args['row']
        msg_id = args['id']
        if dbname:
            sql.create_db('db/{0}'.format(dbname))
        elif row:
            sql.insert({'id': 'test', 'status': 'test'})
        elif msg_id:
            sql.get(msg_id)

if __name__ == '__main__':
    main()