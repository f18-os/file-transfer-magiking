#!/usr/bin/env python3

import sys, re, socket, os
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

def recv_file_name():
    ''' Get file name from client and check if exists.'''
    global server_files_dir
    payload = framedReceive(sock, debug)
    fname = server_files_dir + '/' + payload.decode()
    if os.path.exists(fname):
        framedSend(sock, b"file already exists")
        exit()
    else:
        framedSend(sock, b"OK")
        return payload.decode()
    return None


def recv_file(filename):
    ''' Receive file from client and write to server_files_dir/filename. '''
    global server_files_dir
    fname = server_files_dir + '/' + filename
    with open(fname, 'w') as f:
        while True:
            payload = framedReceive(sock, debug)
            if debug: print("fileServer rec'd: ", payload)
            if not payload:
                print("empty payload")
                break
            f.write(payload.decode())
    

### Stuff starts happening
paramMap = params.parseParams(switchesVarDefaults)

debug, listenPort = paramMap['debug'], paramMap['listenPort']

if paramMap['usage']:
    params.usage()

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # listener socket
bindAddr = ("127.0.0.1", listenPort)
lsock.bind(bindAddr)
lsock.listen(5)
print("listening on:", bindAddr)


while True:
    sock, addr = lsock.accept()

    if not os.fork():
        print("new child process handling connection from", addr)
        fname = recv_file_name()
        recv_file(fname)
