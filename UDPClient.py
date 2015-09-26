from socket import *
import sys
#importing the following allows us to use an MD5 Hash function
#example where I learned how to use md5 hash code:  http://rosettacode.org/wiki/MD5#Python
import hashlib
import time

#serverName = 'localhost'
#serverPort = 12000
clientSocket = socket(AF_INET, SOCK_DGRAM);

firstArg   = sys.argv[1].split(':')
serverName = firstArg[0]
serverPort = int(firstArg[1])


username = sys.argv[2]
password = sys.argv[3]
accountAction = sys.argv[4]
actionValue = sys.argv[5]

#Sending over username and password for authentication
clientSocket.sendto("I want to connect!",(serverName, serverPort))
challengeString, serverAddress = clientSocket.recvfrom(2048)
print "DEBUG: received challenge!"
#Client has now received challenge, computes hash and sends username and hash to server:
#Note: Must send hash as a string because of sendto function limitations, so sent as string
hashOfChallenge = hashlib.md5(username + password + challengeString)

clientSocket.sendto(username, (serverName, serverPort))
clientSocket.sendto(hashOfChallenge.hexdigest(), (serverName, serverPort))
#Now send the bank request, if we authenticate correctly it shall deposit/withdraw money from that account:
clientSocket.sendto(accountAction, (serverName, serverPort))
clientSocket.sendto(actionValue, (serverName, serverPort))


print "DEBUG: Sent user, hash, and value to server!"


clientSocket.close()
s