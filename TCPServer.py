from socket import *
import time

serverPort = 13000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(("", serverPort))
serverSocket.listen(1)

print "Server is ready to receive!"
while 1:
	connectionSocket, addr = serverSocket.accept()
	sentence = connectionSocket.recv(1024)
	capitalizedSentence = sentence.upper()
	time.sleep(3)
	connectionSocket.send(capitalizedSentence)
	print "Sent!"
	connectionSocket.close()