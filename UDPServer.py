from socket import *
serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM);
serverSocket.bind(('', serverPort))
correctUsername = "Shafiq"
correctPassword = "Meow"


print "The server is ready to receive!"


providedUsername, clientAddress = serverSocket.recvfrom(2048)
providedPassword, clientAddress = serverSocket.recvfrom(2048)

if providedUsername == correctUsername and providedPassword == correctPassword:
	authMessage = "You have been authentiated"
else:
	authMessage = "You are a fake"

serverSocket.sendto(authMessage, clientAddress)
serverSocket.close();