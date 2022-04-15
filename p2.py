import argparse, sys
import _thread
from src.servers.tokenGenerator import TokenGenerator

#defines localhost ip for the server

#condition to recieve the port from system args (8080 if none is passed)

host = 'localhost'
#host = '169.254.92.100'
port = 50003

parser = argparse.ArgumentParser()

parser.add_argument('-H', '--host', help='Host')
parser.add_argument('-p', '--port', help='Port')

args = parser.parse_args()

if args.host != None:
    host = args.host

if args.port != None:
    port = int(args.port)


server = TokenGenerator(host, port) #create server instance

server.createSocket() #create server's socket
server.bindSocket() #actually create socket's connection

#main loop to accept many connections
while True:
    try:
        conn, addr = server.acceptConnection() #get connection class and address from new client

        _thread.start_new_thread(server.run, (conn, addr)) #start new thread for client

    except KeyboardInterrupt:
        break

print('closing socket and shutting down server...')
server.closeServer()
print('goodbye!') #close socket after loop