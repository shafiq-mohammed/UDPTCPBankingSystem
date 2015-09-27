from socket import *
import sys
import hashlib
import time

serverName = 'localhost'
serverPort = 13000
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))


#sentence = raw_input("Input lowercase shizniz: ")
#time.sleep(2)
#clientSocket.send(sentence)
#modifiedSentence = clientSocket.recv(1024)
#print "From server: ", modifiedSentence
#clientSocket.close()

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
clientSocket.send("I want to connect!" + ":" + username)
if debugFlag == "-d":	
	print "DEBUG: Sent server a request to connect"
challengeString = clientSocket.recv(2048)
if debugFlag == "-d":	
	print "DEBUG: received challenge from server!"

#Client has now received challenge, computes hash and sends username and hash to server:
#Note: Must send hash as a string because of sendto function limitations, so sent as string
hashOfChallenge = hashlib.md5(username + password + challengeString)
#May not need: status = "response"
#Used to test concurrent clients connecting at same time (remove after coding) time.sleep(3)
clientSocket.sendto(username + ":" + hashOfChallenge.hexdigest() + ":" + accountAction + ":" + actionValue, (serverName, serverPort))
if debugFlag == "-d":	
	print "DEBUG: Sent client the username, hash value, and the respective account action and value, along with the challenge string"
	print "DEBUG: Sent: " + username + ":" + hashOfChallenge.hexdigest() + ":" + accountAction + ":" + actionValue

clientSocket.close()
if debugFlag == "-d":	
	print "DEBUG: Socket connection closed."













