#!/usr/bin/env python3

import socket, sys, re, os

sys.path.append("../lib")       # for params
import params

from framedSock import framedSend, framedReceive

prompt = 'file to send> '

switchesVarDefaults = (
    (('-s', '--server'), 'server', "127.0.0.1:50001"),
    (('-f', '--folder'), "folder",  "./client_files"), # default directory to look for files
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )


def get_socket(server):
    ''' Try establishing a socket connection to the sever. '''
    try:
        serverHost, serverPort = re.split(":", server)
        serverPort = int(serverPort)
    except:
        print("Can't parse server:port from '%s'" % server)
        sys.exit(1)

    s = None
    for res in socket.getaddrinfo(serverHost, serverPort, socket.AF_UNSPEC, socket.SOCK_STREAM):
        af, socktype, proto, canonname, sa = res
        try:
            print("creating sock: af=%d, type=%d, proto=%d" % (af, socktype, proto))
            s = socket.socket(af, socktype, proto)
        except socket.error as msg:
            print(" error: %s" % msg)
            s = None
            continue
        try:
            print(" attempting to connect to %s" % repr(sa))
            s.connect(sa)
        except socket.error as msg:
            print(" error: %s" % msg)
            s.close()
            s = None
            continue
        break
    return s


def get_filename(folder):
    ''' Get name of file to be sent. '''
    # get the commands
    global prompt
    input_fname = input(prompt)
    input_fname = str.strip(input_fname)
    if not os.path.exists(folder + '/' + input_fname):
        print("%s does not exist. Try again." % input_fname)
        return get_filename(folder)
    return input_fname


def send_file(fname, s, folder, debug):
    ''' Read file in chunks and use framedSend to send to server. '''
    with open(folder + '/' + fname, 'r') as f:
        chunk = f.read(100)
        while chunk:
            if debug: print("Next chunk:\n%s\n" % chunk)
            framedSend(s, chunk.encode(), debug)
            # print("waiting for ack of framed send")
            # print(framedReceive(s, debug)) # wait for ack?
            chunk = f.read(100)


def send_filename(s, fname, debug):
    framedSend(s, fname.encode(), debug) 
    answer = framedReceive(s, debug)
    if not (answer == b"OK"):
        print(answer.decode())
        exit()


def main():
    progname = "fileClient"
    paramMap = params.parseParams(switchesVarDefaults)

    server, usage, debug  = paramMap["server"], paramMap["usage"], paramMap["debug"]
    folder = paramMap["folder"]

    if usage:
        params.usage()

    s = get_socket(server)

    if s is None:
        print('could not open socket')
        sys.exit(1)

    fname = get_filename(folder)
    send_filename(s, fname, debug)
    send_file(fname, s, folder, debug)
    s.close()


main()
