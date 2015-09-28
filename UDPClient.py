#Name: Shafiq Mohammed
#Import the respective libraries
from socket import *
import sys
#importing the following allows us to use an MD5 Hash function from the hashlib library
#example where I learned how to use md5 hash code:  http://rosettacode.org/wiki/MD5#Python
import hashlib
import time


#Create a UDP socket and initiate connection request to the server
clientSocket = socket(AF_INET, SOCK_DGRAM);

#Takes the command line argument for the servername and the port, breaks it up into 
#serverName and port, and maps it to respective variable
firstArg   = sys.argv[1].split(':')
serverName = firstArg[0]
serverPort = int(firstArg[1])

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

#Sending an authentication request to the server with username
#Reason why username is sent is because with UDP, I needed a way to keep track of user sessions since UDP doesn't create separate connections for users, it just listens and processes whatever request it receives
#So the way this works is that the server takes the username, generates the challenge, and binds it to the username in the database 
#So that when we send our hash, the UDP server pulls the challenge string from the DB, computes the hash, and compares it to the hash the client generated.
clientSocket.sendto("I want to connect!" + ":" + username,(serverName, serverPort))
if debugFlag == "-d":	
	print "DEBUG: Sent server a request to connect"

#Listens for server to respond with a challenge string
challengeString, serverAddress = clientSocket.recvfrom(2048)
if debugFlag == "-d":	
	print "DEBUG: received challenge from server!"


#Client has now received challenge, computes hash and sends username and hash to server:
#Note: We use the hexdigest function to convert the hash into a string. We need to send the hash as a string because of sendto function limitations that only allows for a string
hashOfChallenge = hashlib.md5(username + password + challengeString)

#We have to set the status to response, so the server understands that we are a client
#that have already received the challenge. Done to get around UDP's connectionless method. 
#This is a part of our custom protocol implementation
status = "response"

#Sends the server the status code, the username, the hash, whether we want to deposit or withdraw, and the amount
clientSocket.sendto(status + ":" + username + ":" + hashOfChallenge.hexdigest() + ":" + accountAction + ":" + actionValue + ":" + challengeString, (serverName, serverPort))
if debugFlag == "-d":	
	print "DEBUG: Sent client the username, hash value, and the respective account action and value, along with the challenge string (For identification purpose of this assignment since we are sending all of our requests for one IP"

#Once we send the server the request, we will close our connection with the server
clientSocket.close()

if debugFlag == "-d":	
	print "DEBUG: Socket connection closed."




