import os
import argparse
from config_ops import make_config
import server
from waitress import serve

def main():
    parser = argparse.ArgumentParser(description= 'telegram bot')
    subparsers = parser.add_subparsers(required=True, dest='subcommand')
    # database
    #database_parser = subparsers.add_parser('db', help='database related commands')
    # config
    config_parser = subparsers.add_parser('config', help='config related commands')
    config_parser.add_argument('-t', '--token', help='telegram bot token')
    # server
    server_parser = subparsers.add_parser('server', help='server related commands')
    server_parser.add_argument('-d', '--debug', action='store_true', help='start in debug mode')
    server_parser.add_argument('-p', '--port', help='listen port')
    server_parser.add_argument('-ip', '--address', dest='ip', help='bind ip')


    args = vars(parser.parse_args())
    if args['subcommand'] == 'config':
        make_config(args, 'config.xml')
    elif args['subcommand'] == 'server':
        debug = args['debug']
        ip = args['ip'] or '127.0.0.1'
        port = int(args['port']) if args['port'] else 5000

        if debug:
            server.app.run(debug=True)
        else:
            print('run server on {0}:{1} in production mode'.format(ip, port))
            serve(server.app, host=ip, port=port, threads=4)

if __name__ == '__main__':
    main()