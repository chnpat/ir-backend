from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import re
import json
from controller import QueryController
from model.model import Course
from urllib.parse import urlparse, parse_qs

hostName = "localhost"
hostPort = 8080

class IRRestAPI(BaseHTTPRequestHandler):
    def header_response(self, http_status=201, content_type='application/json'):
        self.send_response(http_status)
        self.send_header('Content-type', "{}; charset=utf-8".format(content_type))
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def response_message(self, message):
        message = message if 'str' == type(message).__name__ else str(message)
        return bytes(message, 'utf-8')

    def write_message(self, message):
        self.wfile.write( self.response_message(message) )

    def do_GET(self):
        queryDocument = QueryController() # IRBackend

        response_number = 404
        response_msg = "{'result': 'Not found'}"
        urlparsed = urlparse(self.path)
        query = parse_qs(urlparsed.query)
        response_msg = query 

        if 'q' in query:
            response_number = 201
            response_msg = ' '.join(query['q'])
            response_msg = queryDocument.get_result(query['q'][0])
            response_msg = json.JSONEncoder().encode(response_msg)
            pass
            # response_msg = 'dd'

            # - - - - - - -
            # process some query 


        self.header_response(http_status=response_number)
        self.write_message(response_msg)

if '__main__' == __name__:
    irrestServer = HTTPServer((hostName, hostPort), IRRestAPI)
    print(time.asctime(), "Server Starts - {}:{}".format(hostName, hostPort))

    try:
        irrestServer.serve_forever()
    except KeyboardInterrupt:
        pass

    irrestServer.server_close()
    print(time.asctime(), "Server Stop - {}:{}".format(hostName, hostPort))

