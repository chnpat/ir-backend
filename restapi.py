from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import re
import json
from controller import QueryController
from model.model import Course

hostName = "localhost"
hostPort = 8080

class IRRestBaseHandler(BaseHTTPRequestHandler):

    def header_response(self, http_status = 201, content_type = 'application/json'):
        self.send_response(200)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def response_message(self, message):
        message = message if 'str' == type(message).__name__ else str(message)
        return bytes(message, 'utf-8')

    def write_message(self, message):
        self.wfile.write( self.response_message(message) )

class IRRestAPI(IRRestBaseHandler):

    def do_GET(self):
        query = QueryController() # IRBackend

        response_number = 404
        msg = ''

        if None != re.search('\?q\=', self.path):
            queryString = self.path[self.path.find('?')+1:]
            queryString = queryString.split('&')

            params = dict()
            for c in queryString:
                (key, value) = c.split('=')
                params[key] = value

            result = query.get_result(params['q'])
            msg = json.JSONEncode(result)

            # - - - - - - -
            # process some query 


        self.header_response()
        self.write_message(msg)

if '__main__' == __name__:
    irrestServer = HTTPServer((hostName, hostPort), IRRestAPI)
    print(time.asctime(), "Server Starts - {}:{}".format(hostName, hostPort))

    try:
        irrestServer.serve_forever()
    except KeyboardInterrupt:
        pass

    irrestServer.server_close()
    print(time.asctime(), "Server Stop - {}:{}".format(hostName, hostPort))

