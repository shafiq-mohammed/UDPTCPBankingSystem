from socket import *
serverName = 'localhost'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_DGRAM);
x = 0

#while(1):
clientSocket.sendto("Hey! I want to connect!",(serverName, serverPort))
receivedMsg, serverAddress = clientSocket.recvfrom(2048)
print receivedMsg;
username = raw_input("Username: ")
password = raw_input("Password: ")

clientSocket.sendto(username,(serverName, serverPort))
clientSocket.sendto(password,(serverName, serverPort))

#clientSocket.close()