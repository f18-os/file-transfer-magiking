#!/usr/bin/env python3

import socket, sys, re, os

sys.path.append("../lib")       # for params
import params

from framedSock import framedSend, framedReceive

client_file_dir = "./client_files"

prompt = 'file to send> '

switchesVarDefaults = (
    (('-s', '--server'), 'server', "127.0.0.1:50001"),
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


def get_filename():
    ''' Get name of file to be sent. '''
    global client_file_dir
    # get the commands
    global prompt
    input_fname = input(prompt)
    input_fname = str.strip(input_fname)
    if not os.path.exists(client_file_dir + '/' + input_fname):
        print("%s does not exist. Try again." % input_fname)
        return get_filename()
    return input_fname


def send_file(fname, s, debug):
    ''' Read file and use framedSend to send to server. '''
    global client_file_dir
    with open(client_file_dir + '/' + fname, 'r') as f:
        chunk = f.readline()
        while chunk:
            if debug: print("Next chunk:\n%s\n" % chunk)
            framedSend(s, chunk.encode(), debug)
            # print("waiting for ack of framed send")
            # print(framedReceive(s, debug)) # wait for ack?
            chunk = f.readline()


def check_filename(s, fname, debug):
    framedSend(s, fname.encode(), debug) 
    answer = framedReceive(s, debug)
    if not (answer == b"OK"):
        print(answer.decode())
        exit()


def main():
    progname = "fileClient"
    paramMap = params.parseParams(switchesVarDefaults)

    server, usage, debug  = paramMap["server"], paramMap["usage"], paramMap["debug"]

    if usage:
        params.usage()

    s = get_socket(server)

    if s is None:
        print('could not open socket')
        sys.exit(1)

    fname = get_filename()
    check_filename(s, fname, debug)
    send_file(fname, s, debug)
    s.close()


main()
