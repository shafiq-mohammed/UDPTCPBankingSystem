from socket import *
serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM);
serverSocket.bind(('', serverPort))
print "The server is ready to receive!"

#while 1:
message, clientAddress = serverSocket.recvfrom(2048)
print "Client: " + message
serverSocket.sendto("what is yo username and password?", clientAddress)
username, clientAddress = serverSocket.recvfrom(2048)
password, clientAddress = serverSocket.recvfrom(2048)

print username 
print password