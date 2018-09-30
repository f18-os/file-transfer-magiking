#!/usr/bin/env python3

import sys, re, socket
sys.path.append("../lib")       # for params
import params
from framedSock import framedSend, framedReceive

server_files_dir = "./server_files"

switchesVarDefaults = (
    (('-l', '--listenPort') ,'listenPort', 50001),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )

progname = "fileServer"
paramMap = params.parseParams(switchesVarDefaults)

debug, listenPort = paramMap['debug'], paramMap['listenPort']

if paramMap['usage']:
    params.usage()

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # listener socket
bindAddr = ("127.0.0.1", listenPort)
lsock.bind(bindAddr)
lsock.listen(5)
print("listening on:", bindAddr)

sock, addr = lsock.accept()

print("connection rec'd from", addr)

fname = server_files_dir + '/' + "temp"
with open(fname, 'w') as f:
    while True:
        payload = framedReceive(sock, debug)
        if debug: print("fileServer rec'd: ", payload)
        if not payload:
            print("empty payload")
            break
        f.write(payload.decode())
    

