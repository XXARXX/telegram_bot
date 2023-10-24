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
    database_parser.add_argument('-c', '--create', dest='dbname', default='default.db', help='create new database')
    database_parser.add_argument('-g', '--get-status', dest='id')
    # config
    config_parser = subparsers.add_parser('config', help='config related commands')
    config_parser.add_argument('-t', '--token', required=True, help='telegram bot token')
    config_parser.add_argument('-d', '--database', default='default.db', help='database path')
    # test config
    test_parser = subparsers.add_parser('test', help='testing related commands')
    test_parser.add_argument('-t', '--token', required=True, help='telegram bot token used for testing')
    test_parser.add_argument('-d', '--database', default='test.db', help='name of database used for testing')
    test_parser.add_argument('-c', '--chatid', required=True, help='chat for testing')
    # server
    server_parser = subparsers.add_parser('server', help='server related commands')
    server_parser.add_argument('-d', '--debug', action='store_true', help='start in debug mode')
    server_parser.add_argument('-p', '--port', default=5000, help='listen port')
    server_parser.add_argument('-ip', '--address', dest='ip', default='127.0.0.1', help='bind ip')


    args = vars(parser.parse_args())
    subcommand = args.pop('subcommand')
    if subcommand == 'config':
        make_config(args, 'config.xml')

    elif subcommand == 'server':
        debug = args['debug']
        ip = args['ip'] 
        port = int(args['port'])

        if debug:
            server.create_app().run(debug=True, host=ip, port=port)
        else:
            print('run server on {0}:{1} in production mode'.format(ip, port))
            serve(server.create_app(), host=ip, port=port, threads=4)

    elif subcommand == 'db':
        dbname = args['dbname']
        msg_id = args['id']
        if dbname:
            sql.create_db('{0}'.format(dbname))
        elif msg_id:
            sql.get(msg_id)

    elif subcommand == 'test':
        make_config(args, 'test_config.xml')

if __name__ == '__main__':
    main()