from socket import *
import string
import random
import hashlib
import time
import sys
#Specifies the port number of this server, creates a socket, and then binds a port
#number to it, making this a server socket.
serverPort = int(sys.argv[1])
serverSocket = socket(AF_INET, SOCK_DGRAM);
serverSocket.bind(('', serverPort))

#Made a user class to contain 3 users:
class User(object):
	username = ""
	password = ""
	balance = ""

#Populate the class with users
userOne = User()
userOne.username = "Fiqi"
userOne.password = "Cat"
userOne.balance = 100;

userTwo = User()
userTwo.username = "Hoodie"
userTwo.password = "TaubaHain"
userTwo.balance = 1000;

userThree = User()
userThree.username = "Sheeni"
userThree.password = "Kitty"
userThree.balance = 10000;

#Store all three users in one wanna-be database
hardcodedDB = [userOne, userTwo, userThree]
challengedStrings = []
print "The server is ready to receive!"

while(1):
	print challengedStrings
	request, clientAddress = serverSocket.recvfrom(2048)
	#First step of a state-based check:
	if (request == "I want to connect!"):
		#Generates one-time use challenge value in the form of a 64 char string & adds it to challengeStrings array
		challengeString = ''.join(random.choice(string.lowercase) for i in range(64))
		challengedStrings.append(challengeString)
		#Sends string to client:
		serverSocket.sendto(challengeString, clientAddress)
		print "DEBUG: Challenge string sent!: " + challengeString
		#Receives computed hash in the form of a string
		usernameFromClientAndHashDigest, clientAddress = serverSocket.recvfrom(2048)
		usernameFromClientAndHashDigest = usernameFromClientAndHashDigest.split(":")
		usernameFromClient = usernameFromClientAndHashDigest[0]
		hashOfChallenge = usernameFromClientAndHashDigest[1]
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

		#If username, password, and hash are correct
		if (legitHash.hexdigest() == hashOfChallenge):
			print "Authenticated"
			accountActionAndValue, clientAddress = serverSocket.recvfrom(2048)
			
			accountActionAndValue = accountActionAndValue.split(':')
			accountAction = accountActionAndValue[0]
			actionValue = accountActionAndValue[1]
			#No need for the challenge entry in our list, so remove it:
			#challengedStrings.remove()
			#Now to go through the account and withdraw/deposit
			for user in hardcodedDB:
				if user.username == usernameFromClient:
				
					if accountAction == "withdraw":
						if user.balance >= int(actionValue):
							user.balance = user.balance - int(actionValue)
							print "Withdraw requested. Remaining balance for " + user.username + "is " + str(user.balance)
						else:
							print "Cannot perform requested withdrawal: Money in account is less than value you wish to withdraw"
					
					if accountAction == "deposit":
						#Add money and return remaining balance
						user.balance = user.balance + int(actionValue)
						print "Withdraw requested. Remaining balance for " + user.username + "is " + str(user.balance)

		else:
			print "Incorrect pass. You iz stoop, get out my server."


serverSocket.close()




