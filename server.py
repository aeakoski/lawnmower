#!/usr/bin/env python
import argparse
from http.server import HTTPServer, BaseHTTPRequestHandler
import time
import os
import sys
import json

class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def _set_api_headers(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET")
        self.send_header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept, Cache-Control")
        self.end_headers()

    def _api(self, path):
        params = {}
        for x in path[path.find("?")+1:].split("&"):
            params[x.split("=")[0]] = x.split("=")[1]
        json_object = json.dumps(params, indent = 4)
        return json_object.encode("utf8")  # NOTE: must return a bytes object!

    def _html(self, path):
        print("Path: " + path)
        content = ""
        if path == "" or path == "/":
            path = "index.html"
        fullPath = "www/" + path

        with open(fullPath, "r") as target:
            content = target.read()
        return content.encode("utf8")  # NOTE: must return a bytes object!

    def do_GET(self):
        if self.path[0:10] == "/api/drive":
            res = self._api(self.path)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(res)
            return
        else:
            try:
                responsePayload = self._html(self.path)
                self.send_response(200)
                self.end_headers()
                self.wfile.write(responsePayload)
            except:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b'error')
            return


    def do_POST(self):
        self._set_headers()
        self.wfile.write("POST!")

def run(server_class=HTTPServer, handler_class=S, addr="localhost", port=8080):
    server_address = (addr, port)
    httpd = server_class(server_address, handler_class)
    print("Starting http server on", addr, port)
    httpd.serve_forever()

if __name__ == "__main__":
    try:
        run(port = int(sys.argv[1]))
    except Exception:
        print("Psst. Supply a serverport as an argument if 8000 does not float yor goat")
        run()
