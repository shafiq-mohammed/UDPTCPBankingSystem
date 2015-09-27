from socket import *
import string
import random
import hashlib
import time
import sys
#Specifies the port number of this server, creates a socket, and then binds a port
#number to it, making this a server socket. localhost is typically 127.0.0.1
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
userOne.challenge = ""

userTwo = User()
userTwo.username = "Hoodie"
userTwo.password = "TaubaHain"
userTwo.balance = 1000;
userTwo.challenge = ""

userThree = User()
userThree.username = "Sheeni"
userThree.password = "Kitty"
userThree.balance = 10000;
userThree.challenge = ""

try:
	debugFlag = sys.argv[2]
except:
	debugFlag = ""

#Store all three users in one wanna-be database
hardcodedDB = [userOne, userTwo, userThree]
challengedStrings = []
concurrentUsername = ""
print "The server is ready to receive!"


while(1):
	request, clientAddress = serverSocket.recvfrom(2048)
	if(request):
		if debugFlag == "-d":	
			print "DEBUG: The request: " + request + " has come in."
	request = request.split(":")


	#First step of a state-based check:
	if (request[0] == "I want to connect!"):
		#Generates one-time use challenge value in the form of a 64 char string & adds it to challengeStrings array
		challengeString = ''.join(random.choice(string.lowercase) for i in range(64))
		if debugFlag == "-d":	
			print "DEBUG: Challenge string generated."
		challengedStrings.append(challengeString)
		for user in hardcodedDB:
			if user.username == request[1]:
				user.challenge = challengeString
		#Sends string to client:
		serverSocket.sendto(challengeString, clientAddress)
		if debugFlag == "-d":	
			print "DEBUG: Challenge string sent to " + str(clientAddress[0]) + "\n String sent:" + challengeString
		#Receives computed hash in the form of a string. Also receives the username, the account action (withdraw vs deposit) and the value of that action. Does a lot of splitting here.

		usernameFromClientAndHashDigestAndAction = ["Empty"]
		while(usernameFromClientAndHashDigestAndAction[0] != "response"):

			usernameFromClientAndHashDigestAndAction, clientAddress = serverSocket.recvfrom(2048)
			usernameFromClientAndHashDigestAndAction = usernameFromClientAndHashDigestAndAction.split(":")
			usernameFromClient = usernameFromClientAndHashDigestAndAction[1]


			if(usernameFromClientAndHashDigestAndAction[0] == "I want to connect!"):
				challengeString = ''.join(random.choice(string.lowercase) for i in range(64))
				challengedStrings.append(challengeString)
				serverSocket.sendto(challengeString, clientAddress)
				for user in hardcodedDB:
					if user.username == usernameFromClient:
						user.challenge = challengeString
				if debugFlag == "-d":	
					print "DEBUG: Challenge string sent!: " + challengeString
			
		
			#If another user is like "Hey I wanna connect! Then you can just generate a random string and be like "Umm, was really just waiting for the other user to respond but sure, here ya go. So it's rude but it works!"
			
	#	IF THERE IS A RESPONSE YOU AUTOMAGICALLY NAVIGATE THEM HERE DOO ITTTT!
	#	********
		usernameFromClient = usernameFromClientAndHashDigestAndAction[1]
		hashOfChallenge = usernameFromClientAndHashDigestAndAction[2]
		accountAction = usernameFromClientAndHashDigestAndAction[3]
		actionValue = usernameFromClientAndHashDigestAndAction[4]
		if debugFlag == "-d":	
			print "DEBUG: username received is: " + usernameFromClient
		#Server computes hash value with legit username and checks value with hash received
		userFound = False
		for user in hardcodedDB:
			if user.username == usernameFromClient:
				legitHash = hashlib.md5(user.username + user.password + user.challenge)
				
				userFound = True

		#If username don't exist in DB, then you exit session with user.
		#TODO: Just randomly coded this for now, come back to it and fix this ish
		if userFound != True:
			print "Username was not found in our database"

		#If username, password, and hash are correct
		if (legitHash.hexdigest() == hashOfChallenge):
			if debugFlag == "-d":
				print "DEBUG: User Authenticated"
			#No need for the challenge entry in our list, so remove it:
			challengedStrings.remove(usernameFromClientAndHashDigestAndAction[5])
			#Now to go through the account and withdraw/deposit
			for user in hardcodedDB:
				if user.username == usernameFromClient:
				
					if accountAction == "withdraw":
						if user.balance >= int(actionValue):
							user.balance = user.balance - int(actionValue)
							#print "Withdraw requested. Remaining balance for " + user.username + "is " + str(user.balance)
							print "****************************"
							print "Welcome " + user.username
							print "Your withdraw of " + str(actionValue) + " is successfully recorded."
							print "Your new account balance is: " + str(user.balance)
							print "Thank you for banking with us!"
							print "****************************"
						else:
							print "****************************"
							print "Welcome " + user.username
							print "Your withdraw of " + str(actionValue) + " is successfully recorded." 
							print "However, you do not have sufficient funds to withdraw that amount"
							print "Please try again"
							print "Thank you for banking with us!"
							print "****************************"
					
					if accountAction == "deposit":
						#Add money and return remaining balance
						user.balance = user.balance + int(actionValue)
						print "****************************"
						print "Welcome " + user.username
						print "Your deposit of " + str(actionValue) + " is successfully recorded."
						print "Your new account balance is: " + str(user.balance)
						print "Thank you for banking with us!"
						print "****************************"
		
		else:
			print "Incorrect pass. You are a fake, get out my server."
			if debugFlag == "-d":
				print "DEBUG: I was looking for legit hash: " + legitHash.hexdigest()
	#Big ol else statement I created to see if I could use with multiple concurrent users
	else:
		#Debug remove print statement afterwards
		usernameFromClientAndHashDigestAndAction = request
		usernameFromClient = usernameFromClientAndHashDigestAndAction[1]
		hashOfChallenge = usernameFromClientAndHashDigestAndAction[2]
		accountAction = usernameFromClientAndHashDigestAndAction[3]
		actionValue = usernameFromClientAndHashDigestAndAction[4]

		if debugFlag == "-d":
			print "DEBUG: username received is: " + usernameFromClient
		#Server computes hash value with legit username and checks value with hash received
		userFound = False
		for user in hardcodedDB:
			if user.username == usernameFromClient:
				legitHash = hashlib.md5(user.username + user.password + user.challenge)
				
				userFound = True

		#If username don't exist in DB, then you exit session with user.
		#TODO: Just randomly coded this for now, come back to it and fix this ish
		if userFound != True:
			print "Username was not found in our database"

		#If username, password, and hash are correct
		if (legitHash.hexdigest() == hashOfChallenge):
			if debugFlag == "-d":
				print "Authenticated"
			#No need for the challenge entry in our list, so remove it:
			#DEBUG: May not need a challengeStrings array after all
			#challengedStrings.remove(usernameFromClientAndHashDigestAndAction[5])
			#Now to go through the account and withdraw/deposit
			for user in hardcodedDB:
				if user.username == usernameFromClient:
				
					if accountAction == "withdraw":
						if user.balance >= int(actionValue):
							user.balance = user.balance - int(actionValue)
							#print "Withdraw requested. Remaining balance for " + user.username + "is " + str(user.balance)
							print "****************************"
							print "Welcome " + user.username
							print "Your withdraw of " + str(actionValue) + " is successfully recorded."
							print "Your new account balance is: " + str(user.balance)
							print "Thank you for banking with us!"
							print "****************************"
						else:
							print "****************************"
							print "Welcome " + user.username
							print "Your withdraw of " + str(actionValue) + " is successfully recorded." 
							print "However, you do not have sufficient funds to withdraw that amount"
							print "Please try again"
							print "Thank you for banking with us!"
							print "****************************"
					
					if accountAction == "deposit":
						#Add money and return remaining balance
						user.balance = user.balance + int(actionValue)
						print "****************************"
						print "Welcome " + user.username
						print "Your deposit of " + str(actionValue) + " is successfully recorded."
						print "Your new account balance is: " + str(user.balance)
						print "Thank you for banking with us!"
						print "****************************"
		
		else:
			print "Incorrect pass. You are a fake, get out my server."
			if debugFlag == "-d":	
				print "was looking for legit hash: " + legitHash.hexdigest()


serverSocket.close()




