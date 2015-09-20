from socket import *
import sys
#importing the following allows us to use an MD5 Hash function
#example where I learned how to use md5 hash code:  http://rosettacode.org/wiki/MD5#Python
import hashlib

serverName = 'localhost'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_DGRAM);
x = 0

username = sys.argv[1]
password = sys.argv[2]

#Sending over username and password for authentication
#clientSocket.sendto(username,(serverName, serverPort))
#clientSocket.sendto(password,(serverName, serverPort))
clientSocket.sendto("I want to connect!",(serverName, serverPort))
challengeString, serverAddress = clientSocket.recvfrom(2048)
print "received challenge!"
#Client has now received challenge, computes hash and sends username and hash to server:
#Note: Must send hash as a string because of sendto function limitations, so sent as string
hashOfChallenge = hashlib.md5(username + password + challengeString)
clientSocket.sendto(username, (serverName, serverPort))
clientSocket.sendto(hashOfChallenge.hexdigest(), (serverName, serverPort))
print "Sent user and hash to server!"


clientSocket.close()