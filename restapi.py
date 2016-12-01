from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import re
import json

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

    def __init__(self):
        self.query = None # IRBackend

    def do_GET(self):

        response_number = 404
        query = ''
        msg = ''

        if None != re.search('\?q\=', self.path):
            query = self.path[self.path.find('?')+1:]
            query = query.split('&')

            params = dict()
            for c in query:
                (key, value) = c.split('=')
                params[key] = value

            # - - - - - - -
            # process some query 

            msg = '[{"course_id": "abcdefgh","course_title": "สวัสดี", "course_description": "some description", "language": "English", "level": "Introduction", "student_enrolled": 42, "ratings": 423445, "overall_rating": 2.3, "course_url": "http://localhost/message", "cover_image": "http://localhost/image.jpg", "source": "edx"},{"course_id": "abceefw","course_title": "สวัสดี", "course_description": "some description", "language": "English", "level": "Introduction", "student_enrolled": 42, "ratings": 423445, "overall_rating": 2.3, "course_url": "http://localhost/message", "cover_image": "http://localhost/image.jpg", "source": "edx"}]'

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

