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

#Check for debug flag, if it is provided then debugFlag will be set with the flag
try:
	debugFlag = sys.argv[2]
except:
	debugFlag = ""

#Store all three users in one wanna-be database
hardcodedDB = [userOne, userTwo, userThree]

print "The server is ready to receive!"

#Infinite while loop since the server is supposed to run forever
while(1):
	#Listens for an incoming request
	request, clientAddress = serverSocket.recvfrom(2048)
	
	#If a request does come in, attend to it
	if(request):
		if debugFlag == "-d":	
			print "DEBUG: The request: " + request + " has come in."
	#Regardless of request, split it using the ":" delimiter
	request = request.split(":")

		#Generates one-time use challenge value in the form of a 64 char string & adds it to challengeStrings array
		challengeString = ''.join(random.choice(string.lowercase) for i in range(64))
		if debugFlag == "-d":	
			print "DEBUG: Challenge string generated."

		#Stores the challenge string to the user requesting it as a way to get around UDP's liitations
		for user in hardcodedDB:
			if user.username == request[1]:
				user.challenge = challengeString
		
		#Send the challenge string to the client
		serverSocket.sendto(challengeString, clientAddress)
		if debugFlag == "-d":	
			print "DEBUG: Challenge string sent to " + str(clientAddress[0]) + "\n String sent:" + challengeString

		#Coreates a list for the response from client, when client responds it will be stored in this variable
		usernameFromClientAndHashDigestAndAction = ["Empty"]
		
		#Basically guard-checking whether the request coming in is from a client responding to a challenge
		#or a request to connect and receive a challenge string
		while(usernameFromClientAndHashDigestAndAction[0] != "response"):

			#Receives response from client and splits it up
			usernameFromClientAndHashDigestAndAction, clientAddress = serverSocket.recvfrom(2048)
			usernameFromClientAndHashDigestAndAction = usernameFromClientAndHashDigestAndAction.split(":")
			usernameFromClient = usernameFromClientAndHashDigestAndAction[1]

			#Checking to see if the client wants to connect and receive a challenge WHILE another client is being serviced
			#If client is someone who is in the process of being authenticated, another if statement will catch that
			#Basically, it's like this:
			#	If another user is like "Hey I wanna connect! Then you can just generate a 
			#	random string and be like "Umm, was really just waiting for the other user
			#	to respond but sure, here ya go". So it's rude but it works!

			if(usernameFromClientAndHashDigestAndAction[0] == "I want to connect!"):
				challengeString = ''.join(random.choice(string.lowercase) for i in range(64))
				serverSocket.sendto(challengeString, clientAddress)

				#if another user wants the challenge string while another is returning the challenge, we 
				#generate a challenge string for the other user
				for user in hardcodedDB:
					if user.username == usernameFromClient:
						user.challenge = challengeString
				if debugFlag == "-d":	
					print "DEBUG: Challenge string sent!: " + challengeString
			
					
		#Since my design lets the client send whether the client wants to withdraw or deposit 
		#and the amount along with the username and hash, we need to break these up:
		usernameFromClient = usernameFromClientAndHashDigestAndAction[1]
		hashOfChallenge = usernameFromClientAndHashDigestAndAction[2]
		accountAction = usernameFromClientAndHashDigestAndAction[3]
		actionValue = usernameFromClientAndHashDigestAndAction[4]
		if debugFlag == "-d":	
			print "DEBUG: username received is: " + usernameFromClient

		#Server computes hash value with the actual username and password acquired from
		# the 'database' above and checks hash value with hash received from client:
		#Sets initial userFound variable to false, will set to true if user is found in DB
		userFound = False
		for user in hardcodedDB:
			if user.username == usernameFromClient:
				legitHash = hashlib.md5(user.username + user.password + user.challenge)
				
				userFound = True

		#If username don't exist in DB, then you exit session with user.
		if userFound != True:
			print "Username was not found in our database"

		#Compares legitimash hash with client-provided hash. If they match them authentication is successful
		if (legitHash.hexdigest() == hashOfChallenge):
			if debugFlag == "-d":
				print "DEBUG: User Authenticated"

			#Now to go through the account and withdraw/deposit the respective amount
			#I used a for loop here in order to select the user from the DB and then
			#apply the respective method and value to the user's balance
			for user in hardcodedDB:
				if user.username == usernameFromClient:
					
					#If sufficient funds, withdrawing subtracts from user's balance
					if accountAction == "withdraw":
						if user.balance >= int(actionValue):
							user.balance = user.balance - int(actionValue)
							print "****************************"
							print "Welcome " + user.username
							print "Your withdraw of " + str(actionValue) + " is successfully recorded."
							print "Your new account balance is: " + str(user.balance)
							print "Thank you for banking with us!"
							print "****************************"
						#If the withdrawal value is larger than balance, print this message
						else:
							print "****************************"
							print "Welcome " + user.username
							print "Your withdraw of " + str(actionValue) + " is successfully recorded." 
							print "However, you do not have sufficient funds to withdraw that amount"
							print "Please try again"
							print "Thank you for banking with us!"
							print "****************************"
					
					#If authenticated user wishes to deposit, add the deposit value to the user's balance
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
			print "Incorrect password. User authorization failed"
			if debugFlag == "-d":
				print "DEBUG: I was looking for legit hash: " + legitHash.hexdigest()
	
	#If the hash provided by client doens't match the correct hash, then don't authorize user
	else:
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
		if userFound != True:
			print "Username was not found in our database"

		#Compares legitimash hash with client-provided hash. If they match them authentication is successful
		if (legitHash.hexdigest() == hashOfChallenge):
			if debugFlag == "-d":
				print "Authenticated"
		
			#Now to go through the account and withdraw/deposit the respective amount
			#I used a for loop here in order to select the user from the DB and then
			#apply the respective method and value to the user's balance
			for user in hardcodedDB:
				if user.username == usernameFromClient:

					#If sufficient funds, withdrawing subtracts from user's balance
					if accountAction == "withdraw":
						if user.balance >= int(actionValue):
							user.balance = user.balance - int(actionValue)
							print "****************************"
							print "Welcome " + user.username
							print "Your withdraw of " + str(actionValue) + " is successfully recorded."
							print "Your new account balance is: " + str(user.balance)
							print "Thank you for banking with us!"
							print "****************************"
						#If the withdrawal value is larger than balance, print this message
						else:
							print "****************************"
							print "Welcome " + user.username
							print "Your withdraw of " + str(actionValue) + " is successfully recorded." 
							print "However, you do not have sufficient funds to withdraw that amount"
							print "Please try again"
							print "Thank you for banking with us!"
							print "****************************"
					
					#If authenticated user wishes to deposit, add the deposit value to the user's balance
					if accountAction == "deposit":
						#Add money and return remaining balance
						user.balance = user.balance + int(actionValue)
						print "****************************"
						print "Welcome " + user.username
						print "Your deposit of " + str(actionValue) + " is successfully recorded."
						print "Your new account balance is: " + str(user.balance)
						print "Thank you for banking with us!"
						print "****************************"
		
		#If the hash provided by client doens't match the correct hash, then don't authorize user
		else:
			print "Incorrect password.  You are a fake, get out my server."
			if debugFlag == "-d":	
				print "was looking for legit hash: " + legitHash.hexdigest()


#The server is never supposed to close, but to comply with the structure of server
# code I added this method:
serverSocket.close()




