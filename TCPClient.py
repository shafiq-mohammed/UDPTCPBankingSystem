from socket import *
import time

serverName = 'localhost'
serverPort = 13000
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))


sentence = raw_input("Input lowercase shizniz: ")
time.sleep(2)
clientSocket.send(sentence)
modifiedSentence = clientSocket.recv(1024)
print "From server: ", modifiedSentence
clientSocket.close()
