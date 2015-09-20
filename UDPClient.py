from socket import *
import sys
serverName = 'localhost'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_DGRAM);
x = 0

username = sys.argv[1]
password = sys.argv[2]


#while(1):
#Sending over username and password for authentication
clientSocket.sendto(username,(serverName, serverPort))
clientSocket.sendto(password,(serverName, serverPort))


receivedMsg, serverAddress = clientSocket.recvfrom(2048)
print receivedMsg;
clientSocket.close()