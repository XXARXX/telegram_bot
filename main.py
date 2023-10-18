import os
import argparse

from waitress import serve

import server
from config_ops import make_config

def main():
    parser = argparse.ArgumentParser(description= 'telegram bot')
    subparsers = parser.add_subparsers(required=True, dest='subcommand')
    # database
    #database_parser = subparsers.add_parser('db', help='database related commands')
    # config
    config_parser = subparsers.add_parser('config', help='config related commands')
    config_parser.add_argument('-t', '--token', required=True, help='telegram bot token')
    # server
    server_parser = subparsers.add_parser('server', help='server related commands')
    server_parser.add_argument('-d', '--debug', action='store_true', help='start in debug mode')
    server_parser.add_argument('-p', '--port', default=5000, help='listen port')
    server_parser.add_argument('-ip', '--address', dest='ip', default='127.0.0.1', help='bind ip')


    args = vars(parser.parse_args())
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

if __name__ == '__main__':
    main()