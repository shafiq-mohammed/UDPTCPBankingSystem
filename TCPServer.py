from socket import *
import string
import random
import hashlib
import time
import sys

#Specifies the port number of this server, creates a socket, and then binds a port
#number to it, making this a server socket. localhost is typically 127.0.0.1
serverPort = int(sys.argv[1])
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(("", serverPort))

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

hardcodedDB = [userOne, userTwo, userThree]
#REMOVE: challengedStrings = []
#concurrentUsername = ""

serverSocket.listen(1)
print "Server is ready to receive!"
while 1:
	connectionSocket, addr = serverSocket.accept()
	request = connectionSocket.recv(2048)
	if debugFlag == "-d":
		print "DEBUG: Received a request from: " + str(addr)
	request = request.split(":")

	challengeString = ''.join(random.choice(string.lowercase) for i in range(64))
	if debugFlag == "-d":	
		print "DEBUG: Challenge string generated."
#REMOVE:	challengedStrings.append(challengeString)
	connectionSocket.send(challengeString)
	usernameFromClientAndHashDigestAndAction = connectionSocket.recvfrom(2048)
	usernameFromClientAndHashDigestAndAction = usernameFromClientAndHashDigestAndAction[0].split(":")
	
	usernameFromClient = usernameFromClientAndHashDigestAndAction[0]
	hashOfChallenge = usernameFromClientAndHashDigestAndAction[1]
	accountAction = usernameFromClientAndHashDigestAndAction[2]
	actionValue = usernameFromClientAndHashDigestAndAction[3]
	legitHash = ""

	if debugFlag == "-d":	
		print "DEBUG: username received is: " + usernameFromClient
	#Server computes hash value with legit username and checks value with hash received
	userFound = False
	for user in hardcodedDB:
		if user.username == usernameFromClient:
			legitHash = hashlib.md5(user.username + user.password + challengeString)
			userFound = True
			if debugFlag == "-d":
				print "DEBUG: Username was found in our database!"

	#If username don't exist in DB, then you exit session with user.
	#TODO: Just randomly coded this for now, come back to it and fix this ish
	if userFound != True:
		print "Username was not found in our database"
#****
	#If username, password, and hash are correct
	
	if (legitHash.hexdigest() == hashOfChallenge):
		if debugFlag == "-d":
			print "DEBUG: User Authenticated"

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
		print "Incorrect password. User authorization failed"
		if debugFlag == "-d":
			print "DEBUG: I was looking for legit hash: " + legitHash.hexdigest()

#*****

		#If username,
#	capitalizedSentence = sentence.upper()
#	time.sleep(3)
#	connectionSocket.send(capitalizedSentence)
#	print "Sent!"
connectionSocket.close()








