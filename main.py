import os
import argparse
from config_ops import make_config
import server
from waitress import serve

def main():
    parser = argparse.ArgumentParser(description= 'telegram bot')
    parser.add_argument('-t', '--token', help='telegram bot token')
    parser.add_argument('-d', '--debug', help='start in debug mode')
    parser.add_argument('-p', '--port', help='listen port')
    parser.add_argument('--ip', help='bind ip')

    args = parser.parse_args()
    if (args.token):
        make_config('config.xml', args)
        return 0

    debug = args.debug
    ip = args.ip or '127.0.0.1'
    port = int(args.port or 5000)

    if debug:
        server.app.run(debug=True)
    else:
        print('run server on {0}:{1} in production mode'.format(ip, port))
        serve(server.app, host=ip, port=port, threads=4)

if __name__ == '__main__':
    main()