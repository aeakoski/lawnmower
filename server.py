#!/usr/bin/env python
import argparse
import serial
from http.server import HTTPServer, BaseHTTPRequestHandler
import time
import os
import sys
import json

serialPort = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
serialPort.flush()
if serialPort.isOpen():
    serialPort.close()
serialPort.open()

pathToMowerFiles = os.getenv('PATH_TO_MOWER_FILES', "")

class S(BaseHTTPRequestHandler):
    def sendCommand(self, command):
        global serialPort
        serialPort.write(command.encode())

    def driveMower(self, commands):
        if (not commands["up"] and not commands["down"] and not commands["left"] and not commands["right"] and not commands["break"]):
            ## Dont move
            print("Dont move 1")
            return

        if (commands["up"] and commands["down"]):
            ## Dont move
            print("Dont move 2")
            return

        if (commands["down"] and commands["left"] and commands["right"]):
            ## Move backwards
            print("Down move 1")
            self.sendCommand("d")
            return

        if (not commands["down"] and not commands["up"] and commands["left"] and commands["right"]):
            ## Move backwards
            print("Up move 1")
            self.sendCommand("u")
            return

        if (commands["up"] and commands["left"] and commands["right"]):
            ## Move forewards
            print("Up move 2")
            self.sendCommand("u")
            return

        if (commands["down"] and commands["left"]):
            ## Turn left
            print("y move 1")
            self.sendCommand("y")
            return

        if (commands["down"] and commands["right"]):
            ## Turn left
            print("x move 1")
            self.sendCommand("x")
            return

        if (commands["up"] and commands["left"] or commands["left"]):
            ## Turn left
            print("Left move 1")
            self.sendCommand("r")
            return

        if (commands["up"] and commands["right"] or commands["right"]):
            ## Turn right
            print("Right move 1")
            self.sendCommand("l")
            return

        if (commands["up"]):
            ##  Go forewards
            print("Up move 3")
            self.sendCommand("u")
            return

        if (commands["down"]):
            # Go backwards
            print("Down move 3")
            self.sendCommand("d")
            return



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
            if (x.split("=")[0] in ["up", "down", "left", "right", "break"]):
                try:
                    params[x.split("=")[0]] = int(x.split("=")[1])
                except:
                    continue
        self.driveMower(params)
        json_object = json.dumps(params, indent = 4)
        return json_object.encode("utf8")  # NOTE: must return a bytes object!

    def _html(self, path):
        global pathToMowerFiles
        print("Full path: " + path)
        path = path[path.find("/"):]
        content = ""
        if path == "" or path == "/":
            path = "index.html"
        fullPath = pathToMowerFiles + "www/" + path

        with open(fullPath, "r") as target:
            content = target.read()
        return content.encode("utf8")  # NOTE: must return a bytes object!

    def do_GET(self):
        if "/api/drive" in self.path:
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

def run(server_class=HTTPServer, handler_class=S, addr="0.0.0.0", port=8080):
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
