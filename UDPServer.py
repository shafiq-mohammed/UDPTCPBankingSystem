from socket import *
import string
import random
import hashlib

#Specifies the port number of this server, creates a socket, and then binds a port
#number to it, making this a server socket.
serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM);
serverSocket.bind(('', serverPort))

#Made a user class to contain 3 users:
class User(object):
	username = ""
	password = ""
	balance = ""

#Populate the class with users
userOne = User()
userOne.username = "Shafiq"
userOne.password = "Cat"
userOne.balance = 100;

userTwo = User()
userTwo.username = "Huda"
userTwo.password = "TaubaHain"
userTwo.balance = 1000;

userThree = User()
userThree.username = "Sheeni"
userThree.password = "Kitty"
userThree.balance = 10000;

#Store all three users in one wanna-be database
hardcodedDB = [userOne, userTwo, userThree]

print "The server is ready to receive!"

while(1):
	request, clientAddress = serverSocket.recvfrom(2048)
	if (request == "I want to connect!"):
		print "I see you wanna connect"
		#Generates one-time use challenge value in the form of a 64 char string:
		challengeString = ''.join(random.choice(string.lowercase) for i in range(64))
		#Sends string to client:
		serverSocket.sendto(challengeString, clientAddress)
		print "Challenge string sent!: " + challengeString
		#Receives computed hash in the form of a string
		usernameFromClient, clientAddress = serverSocket.recvfrom(2048)
		hashOfChallenge, clientAddress = serverSocket.recvfrom(2048)
		print "DEBUG: username received is: " + usernameFromClient
		#Server computes hash value with legit username and checks value with hash received
		userFound = False
		for user in hardcodedDB:
			if user.username == usernameFromClient:
				legitHash = hashlib.md5(user.username + user.password + challengeString)
				userFound = True
		#If username don't exist in DB, then you exit session with user.
		#TODO: Just randomly coded this for now, come back to it and fix this ish
		if userFound != True:
			print "Username was not found in our database"
			

		if (legitHash.hexdigest() == hashOfChallenge):
			print "YO MAH NIGGA " + usernameFromClient + " YOU HAZ BEEN AUTHENTICATATED TURN UP!!!"
		else:
			print "Incorrect pass. You iz stoop, get out my server."





serverSocket.close()