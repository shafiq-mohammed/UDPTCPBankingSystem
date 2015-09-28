#Name: Shafiq Mohammed

#Import the respective libraries
from socket import *
import sys
#importing the following allows us to use an MD5 Hash function from the hashlib library
#example where I learned how to use md5 hash code:  http://rosettacode.org/wiki/MD5#Python
import hashlib
import time

#Takes the command line argument for the servername and the port, breaks it up into 
#serverName and port, and maps it to respective variable
firstArg   = sys.argv[1].split(':')
serverName = firstArg[0]
serverPort = int(firstArg[1])

#Create a TCP socket and initiate connection request to the server
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

#Takes the arguments from the command line, and maps it to the respective variables:
username = sys.argv[2]
password = sys.argv[3]
accountAction = sys.argv[4]
actionValue = sys.argv[5]

#Check for debug flag, if it is provided then debugFlag will be set with the flag
try:
	debugFlag = sys.argv[6]
except:
	debugFlag = ""

#Sends an authentication request to the server
clientSocket.send("I want to connect!")
if debugFlag == "-d":	
	print "DEBUG: Sent server a request to connect"

#Listens for server to respond with a challenge string
challengeString = clientSocket.recv(2048)
if debugFlag == "-d":	
	print "DEBUG: received challenge from server!"

#Computes hash of received challenge string with the username and password
hashOfChallenge = hashlib.md5(username + password + challengeString)

#Sends username, above computed hash, whether the user wants to withdraw or deposit money, and the amount
clientSocket.send(username + ":" + hashOfChallenge.hexdigest() + ":" + accountAction + ":" + actionValue)
if debugFlag == "-d":	
	print "DEBUG: Sent client the username, hash value, and the respective account action and value, along with the challenge string"
	print "DEBUG: Sent: " + username + ":" + hashOfChallenge.hexdigest() + ":" + accountAction + ":" + actionValue

#Once we send the server the request, we will close our connection with the server
clientSocket.close()
if debugFlag == "-d":	
	print "DEBUG: Socket connection closed."













