from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import re
import json
from controller import QueryController
from model.model import Course
from urllib.parse import urlparse, parse_qs

import uuid

hostName = "localhost"
hostPort = 8080

class DataCleansing:

    @staticmethod
    def course_cleansing(course_id):
        return course_id.replace('-', '')[:-1]

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
        methods = ['Cosine', 'Jaccard', 'Euclidean', 'Manhudtan']

        response_number = 404
        response_msg = "{'result': 'Not found'}"
        urlparsed = urlparse(self.path)
        query = parse_qs(urlparsed.query)
        response_msg = query 

        if 'q' in query:
            response_number = 201
            method = 'Cosine' if 'c' not in query else methods[int(query['c'][0])-1]
            response_msg = ' '.join(query['q'])
            found_courses = queryDocument.get_result(query['q'][0], method=method)
            course_id = [DataCleansing.course_cleansing(doc_id[0]) for doc_id in found_courses] 
            raw_in_clause = "'{}'".format("', '".join(course_id))
            courses = Course.raw("SELECT * FROM course WHERE course_id in ({}) ORDER BY FIELD(course_id, {})".format(raw_in_clause, raw_in_clause))

            response_msg = [c.dictionary() for c in courses]

        response_msg = json.JSONEncoder().encode(response_msg)

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

