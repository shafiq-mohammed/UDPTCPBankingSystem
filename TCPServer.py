from socket import *
import string
import random
import hashlib
import time
import sys

#Specifies the port number of this server, creates a socket
#And then binds a port number to it, making this a server socket. localhost is typically 127.0.0.1
serverPort = int(sys.argv[1])
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(("", serverPort))

#Made a user class to contain 3 users:
class User(object):
	username = ""
	password = ""
	balance = ""

#Populate the class with the three users
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

#Creates a list with the 3 users to mimic a database
hardcodedDB = [userOne, userTwo, userThree]

#Check for debug flag, if it is provided then debugFlag will be set with the flag
try:
	debugFlag = sys.argv[2]
except:
	debugFlag = ""

#Enables the server to accept connections:
serverSocket.listen(1)
if debugFlag == "-d":
	print "Server is ready to receive!"

#Infinite while loop since the server is supposed to run forever
while 1:
	#Listens for an incoming request
	connectionSocket, addr = serverSocket.accept()
	request = connectionSocket.recv(2048)
	if debugFlag == "-d":
		print "DEBUG: Received a request from: " + str(addr)

	#Generates a random 64-character string to send as a challenge to the client
	challengeString = ''.join(random.choice(string.lowercase) for i in range(64))
	if debugFlag == "-d":	
		print "DEBUG: Challenge string generated."

	#Sends the challenge string to the client
	connectionSocket.send(challengeString)

	#Listens for the client to respond with a computer hash based on the clients username, password, and the challenge string
	usernameFromClientAndHashDigestAndAction = connectionSocket.recvfrom(2048)
	usernameFromClientAndHashDigestAndAction = usernameFromClientAndHashDigestAndAction[0].split(":")
	
	#Since my design lets the client send whether the client wants to withdraw or deposit 
	#and the amount along with the username and hash, we need to break these up:
	usernameFromClient = usernameFromClientAndHashDigestAndAction[0]
	hashOfChallenge = usernameFromClientAndHashDigestAndAction[1]
	accountAction = usernameFromClientAndHashDigestAndAction[2]
	actionValue = usernameFromClientAndHashDigestAndAction[3]
	legitHash = ""

	if debugFlag == "-d":	
		print "DEBUG: username received is: " + usernameFromClient
	
	#Server computes hash value with the actual username and password acquired from
	# the 'database' above and checks hash value with hash received from client:
	#Sets initial userFound variable to false, will set to true if user is found in DB
	userFound = False
	#Checks if user exists in DB and then computes what the proper hash should be
	for user in hardcodedDB:
		if user.username == usernameFromClient:
			legitHash = hashlib.md5(user.username + user.password + challengeString)
			userFound = True
			if debugFlag == "-d":
				print "DEBUG: Username was found in our database!"

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
	
	#If the hash provided by client doens't match the correct hash, then don't authorize user
	else:
		print "Incorrect password. User authorization failed. Try again."
		#Debug flag allows us to see what the expected hash was supposed to be
		if debugFlag == "-d":
			print "DEBUG: I was looking for legit hash: " + legitHash.hexdigest()


#The server is never supposed to close, but to comply with the structure of server
# code I added this method:
connectionSocket.close()








