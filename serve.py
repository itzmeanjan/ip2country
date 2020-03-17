#!/usr/bin/python3

from http.server import HTTPServer, BaseHTTPRequestHandler
from model.ip2country import IP2Country
from re import compile as rcompile
from os import environ
from json import dumps

# will be used for looking up ip address, like we do in case of map/ dict, if found, returns country record
ip2country = IP2Country.read('./data/IP2LOCATION-LITE-DB1.CSV')
# regex for extract IPv4 address from a string i.e. request path
reg = rcompile(r'((\d{1,3}\.){3}\d{1,3})')


class Handler(BaseHTTPRequestHandler):

    def do_GET(self):  # serves GET requests
        resp = {'status': 'not found'}
        if self.path == '/':  # if no specific ip address is provided, we'll look up client ip address
            mobj = reg.search(self.address_string())
            if mobj:
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                resp = dict(zip(['code', 'country'],
                                ip2country[mobj.group()].split(':')))
            else:  # returns 404 if nothing is found
                self.send_response(404)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
        else:  # ip request is of http://localhost:8008/x.x.x.x, they we'll for looking up x.x.x.x
            mobj = reg.search(self.path)
            if mobj:
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                resp = dict(zip(['code', 'country'],
                                ip2country[mobj.group()].split(':')))
            else:  # returns 404 if nothing is found
                self.send_response(404)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
        # writing response to output stream
        self.wfile.write(dumps(resp).encode('utf-8'))


def serve():
    # tries to read environment variable for determining on which port to listen to, otherwise goes for 8008
    port = int(environ.get('IP2COUNTRYPORT') or '8008')
    server = HTTPServer(("", port), Handler)
    try:
        print("IP2Country listening :{} ...".format(port))
        server.serve_forever()  # keeps serving GET request until explicitly closed
    except Exception:
        server.server_close()  # in case on occurance of error, shuts server down


if __name__ == '__main__':
    print("This module isn't supposed to be used this way")
