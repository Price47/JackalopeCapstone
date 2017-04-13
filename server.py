#! /usr/bin/env python3

import urllib.request
import urllib.parse
import logging
import codecs
import socket
import sys
import http.client

# Server socket created and starting to listen
Serv_Port = 8080
Serv_Sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
Serv_Sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Prepare a server socket
print ("starting server ....")
Serv_Sock.bind(('', Serv_Port))
Serv_Sock.listen(5)

# Create sanitation function that checks if API_TOKEN is included
# Checks for both regular text as well as hex encoded(how I evaded the system)
def sanitize(message, socket):
    if b'API_TOKEN' in message:
        return_error(socket)
    if 'API_TOKEN' in urllib.parse.unquote(str(message)):
        return_error(socket)

# Send a 403 forbidden if API_TOKEN is found
def return_error(socket):
    socket.send(b'HTTP/1.1 403 forbidden\n\n')
    print("Malicious request detected, denied.")

# Forwards the response from the target server back to the client
# This function is needed because I don't know how else to pass along
# An HTTPResponse object as bytes and have it be accepted by urllib
def forward_response(resp, client):
    fields = []
    fields.append('HTTP/1.1 ')
    fields.append(str(resp.status) + ' ' + resp.msg + ' \n')
    fields.append('Content-Length: ' + resp.getheader('Content-Length') + '\n')
    fields.append('Content-Type: ' + resp.getheader('Content-Type') + '\n\n')
    data = resp.read()
    fields.append(data)

    response = b''
    for data in fields:
        try:
            response += data
        except:
            response += bytes(str(data), 'utf-8')
    client.send(response)

# Main loop, continously parse traffic and check for malicious code
while True:
    try:
        # Start receiving data from the client
        print ('Intrusion Detection System Waiting For Request...')
        Client, addr = Serv_Sock.accept() # Accept a connection from client
        message = Client.recv(8192)

        splitMessage = message.split()
        if len(splitMessage) <= 1:
          continue

        # Set URL to forward requests
        url = 'http://localhost:8081' + splitMessage[1].decode("utf-8")

        # Use input sanitation function
        sanitize(splitMessage[1], Client)

        # Finally send the request if it passes
        with urllib.request.urlopen(url) as f:
            forward_response(f,Client)
            
    except urllib.error.HTTPError as e:
        forward_response(e, Client)
        
    except KeyboardInterrupt:
        sys.exit(1)

