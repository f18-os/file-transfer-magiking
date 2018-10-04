# File Server and File Client

A File Server that allows clients to send files (PUT) over a TCP socket connection.

Messages are framed, meaning that the size of the message is sent ahead of it's contents.

## Some notes

Zero length files can be written to the server,
because a zero length message is what tells the server
to stop writing to the file.
This isn't great because it clogs the namespace of files.

Also, the server will not write a file
if it already has one by the same name.

## File Client

Client defaults

``` python
switchesVarDefaults = (
    (('-s', '--server'), 'server', "127.0.0.1:50001"),
    (('-f', '--folder'), "folder",  "./client_files"), # default directory to look for files
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )
```

A different address:socket combo can be specified via the `-s addr:sock` argument.

The client looks for the given filename in the directory specified by `-f`.
It defaults to the relative directory `./client_files`.

If the client is able to connect to the server,
the user is presented with a prompt `file to send> ` to enter the name of the file they would like to send.
If that file can be found in the directory specified by `-f`,
then the filename will be sent to the server.
If the filename is not found, the user will again be presented with the prompt.

If the server sends the 'OK',
then file transmission will begin.

## File Server

Server defaults

``` python
switchesVarDefaults = (
    (('-l', '--listenPort') ,'listenPort', 50001),
    (('-f', '--folder'), "folder",  "./server_files"), # default directory to look for files
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )
```

A different listening port can be specified by the `-l` flag.

The server looks for/stores files in the directory specified by the `-f` argument.
It defaults to `./server_files`.

After starting the server,
it listens for a client to connect.
Once a client connects,
the server forks a new child to handle the client.

The server first listens for a filename to be sent across.
If the server finds a file by the same name in it's `-f` directory,
it will not write the file.
The client is notified of this and the connection is terminated.

If the server does not already have a file of that name in it's directory,
it will send an 'OK' back to the client,
who will then begin sending over the file.

The server waits for a 0-length message to stop writing messages to the file.
Once this is encountered, it finishes writing the file and then terminates.
