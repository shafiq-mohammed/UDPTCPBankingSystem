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

#Check for debug flag
try:
	debugFlag = sys.argv[6]
except:
	debugFlag = ""

#Sending over username and password for authentication
clientSocket.sendto("I want to connect!" + ":" + username,(serverName, serverPort))
if debugFlag == "-d":	
	print "DEBUG: Sent server a request to connect"
challengeString, serverAddress = clientSocket.recvfrom(2048)
if debugFlag == "-d":	
	print "DEBUG: received challenge from server!"
#Client has now received challenge, computes hash and sends username and hash to server:
#Note: Must send hash as a string because of sendto function limitations, so sent as string
hashOfChallenge = hashlib.md5(username + password + challengeString)
status = "response"
time.sleep(3)
clientSocket.sendto(status + ":" + username + ":" + hashOfChallenge.hexdigest() + ":" + accountAction + ":" + actionValue + ":" + challengeString, (serverName, serverPort))
if debugFlag == "-d":	
	print "DEBUG: Sent client the username, hash value, and the respective account action and value, along with the challenge string (For identification purpose of this assignment since we are sending all of our requests for one IP"
#Now send the bank request, if we authenticate correctly it shall deposit/withdraw money from that account:
#clientSocket.sendto(accountAction + ":" + actionValue, (serverName, serverPort))

clientSocket.close()

if debugFlag == "-d":	
	print "DEBUG: Socket connection closed."