#! /usr/bin/env python
import smartcard
import os
import random
import RPi.GPIO as GPIO
#import thread
from time import sleep
from smartcard.ATR import ATR
from smartcard.CardType import ATRCardType
from smartcard.CardRequest import CardRequest
from smartcard.util import *
from smartcard.CardMonitoring import CardMonitor, CardObserver


print "\nstarting...\n"

GPIO.setmode(GPIO.BOARD)
GPIO.setup(37,GPIO.OUT)
GPIO.setup(38,GPIO.OUT)
GPIO.setup(40,GPIO.OUT)
#GPIO.setup(15,GPIO.OUT)

#reset
GPIO.output(37,True)
GPIO.output(38,True)
GPIO.output(40,True)
#GPIO.output(15,False)
#global activeFlag
#activeFlag=-1

print "online card reader:",smartcard.System.readers(),"\n"


class cardober( CardObserver ):

	def __init__( self ):
		self.cards=[]
		self.cardservice=[]
#		self.GPIOStatus=[False for i in range(42)]

	def changeGPIOStatus(self,num):
		if self.GPIOStatus[num+1]:
			self.GPIOStatus[num+1]=False
			GPIO.output(num,False)
		else:
			self.GPIOStatus[num+1]=True
			GPIO.output(num,True)
		
	def getGPIOStatus(self,num):
		return self.GPIOStatus[num+1]	

	def update( self, observable, (addedcards, removedcards) ):
		for card in addedcards:
			if card not in self.cards:
				self.cards+=[card]
				print "+Inserted: ", toHexString( card.atr )
				self.cardservice=card
				self.cardservice.connection = self.cardservice.createConnection()
				self.cardservice.connection.connect()
#				activeFlag=1				
#				for i in range(0,16):
#					self.auth(i*4,"A",0)
#					for j in range(0,4):
#						print "----- block :",i*4+j
#						response,sw1,sw2=self.read(i*4+j)
#						print 'response: ', toHexString(response), ' status words: ', "%x %x" % (sw1, sw2)
				if self.verifyCard():
#					self.debugVerifyCard()
					self.operation()
#					self.renewBlock()
					self.finish()
				else:
					self.errorshow(10,0,1)					

		for card in removedcards:
			print "-Removed: ", toHexString( card.atr )
			if card in self.cards:
				self.cards.remove( card )


	#define card data path
	dataPath="/card"


	#define APDU

	apdu_fireware_version=[0xFF,0x00,0x48,0x00,0x00]
	apdu_read_cardnum=[0xFF,0xCA,0x00,0x00,0x04]

	apdu_putkey_head=[0xFF,0x82,0x00]
	apdu_Akey=[0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
	apdu_Bkey=[0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
	apdu_auth_head=[0xFF,0x86,0x00,0x00,0x05,0x01,0x00]

	apdu_read_block_head=[0xFF,0xB0,0x00]
	apdu_write_block_head=[0xFF,0xD6,0x00]

	def loadKey(self,key_location,key):
		response, sw1, sw2 = self.cardservice.connection.transmit( self.apdu_putkey_head+[key_location,0x06]+key )
		print 'response: ', map(chr,map(int,response)), ' status words: ', "%x %x" % (sw1, sw2)


	def auth(self,block_number,type,key_location):
		self.apdu_keytype=[]
		if(type=="a")or(type=="A"):
		    self.apdu_keytype=[0x60]
		else:
		    self.apdu_keytype=[0x61]
		print toHexString(self.apdu_auth_head+[block_number]+self.apdu_keytype+[key_location])
		response, sw1, sw2 = self.cardservice.connection.transmit(self.apdu_auth_head+[block_number]+self.apdu_keytype+[key_location])
		
		print 'response: ', map(chr,map(int,response)), ' status words: ', "%x %x" % (sw1, sw2)


	def read(self,block_number,length=16):
		return self.cardservice.connection.transmit(self.apdu_read_block_head+[block_number]+[length])
		#print 'response: ', toHexString(response), ' status words: ', "%x %x" % (sw1, sw2)

	#4 or 16 bits
	def write(self,block_number,data):
		length=len(data)
		print data
		if(length==4)or(length==16):
			response, sw1, sw2 = self.cardservice.connection.transmit(self.apdu_write_block_head+[block_number]+[length]+data)
			print 'response: ', toHexString(response), ' status words: ', "%x %x" % (sw1, sw2)
		else:
		    print 'data length need 4 or 16'

	def readCardNum(self,rawData=False):
		response, sw1, sw2 = self.cardservice.connection.transmit(self.apdu_read_cardnum)
		
		if(sw1==0x90)and(sw2==0x00):
			if(rawData):
				return True,response
			else:
				return True,toHexString(response).replace(' ','')
		else:
		    return False,"%x %x"  % (sw1, sw2)

	def checkCardNum(self,num):
		return os.path.exists(dataPath+"\\"+num)


	def autoCheckCardNum(self):
		status,value=readCardNum()
		if(status):
			return checkCardNum(value)
		else:
			errorshow(20,0,1)
			return False

	def errorshow(self,uptime,sleeptime,times):
		response, sw1, sw2 = self.cardservice.connection.transmit([0xFF,0x00,0x40,0x50,0x04,uptime,sleeptime,times,0x01])


	def randomBytes(self,length=16):
		returnlist=[]
		for i in range(length):
		    returnlist+=[random.randint(0,255)]
		return returnlist

	def randomBlockSaveAndWriteCard(self,num,Akey,Bkey):
		if(num==0):
			print "modify 0 block is danger"
			return False
		self.checkAutoMkdir()
		status,value=self.readCardNum()
		if not status:
		    return false
		self.loadKey(0,Akey)
#		self.loadKey(1,Bkey)
		self.auth(num*4,"a",0)
#		self.auth(num*4,"b",1)
		
		for i in range(0,3):
			ranlist=self.randomBytes()
			self.write(num*4+i,ranlist)		
			fp = open(self.dataPath+"/"+value+"/block_"+str(num*4+i),"wb+")
			fp.write(str(ranlist))
			fp.close()
		
		#newAkey=self.randomBytes(6)
		#newBkey=self.randomBytes(6)
		#newkey=newAkey+[0xFF,0x07,0x80,0x69]+newBkey
		#print newkey

	def verifyBlock(self,num):
		print "verifyBlock:",num
                self.checkCardExistDir()
                status,value=self.readCardNum()
		
                if not status:
                    return False
                self.loadKey(0,self.apdu_Akey)
#               self.loadKey(1,self.apdu_Bkey)
                self.auth(num*4,"a",0)
#                self.auth(num*4,"b",1)
		
		keygroup=[[],[],[]]
		
		try:
			for i in range(0,3):
				fp = open(self.dataPath+"/"+value+"/block_"+str(num*4+i),"rb")
				#print eval(fp.readlines()[0])
				keygroup[i]=eval(fp.readlines()[0])
				fp.close()
		
			for i in range(0,3):
				response, sw1, sw2 =self.read(num*4+i)
				#print keygroup[i]
				#print response
				if(keygroup[i]!=response):
					return False
		except:
			return False
		return True

	def checkCardExistDir(self):
		status,value=self.readCardNum()
		if(status):
			mkpath = os.path.join(self.dataPath,value )
			if os.path.isdir(mkpath):
				return True
		return False



	def checkAutoMkdir(self):
	    #mkdir
		status,value=self.readCardNum()
		if(status):
			mkpath = os.path.join(self.dataPath,value )
			if not os.path.isdir(mkpath):
			    os.makedirs(mkpath)


	def operation(self):
#		self.changeGPIOStatus(37)
#		self.changeGPIOStatus(38)
#		self.changeGPIOStatus(40)
		GPIO.output(37,False)
		GPIO.output(38,False)
		GPIO.output(40,False)
		return True

	def finish(self):
		response, sw1, sw2 = self.cardservice.connection.transmit([0xFF,0x00,0x40,0x04,0x04,0x02,0x01,0x03,0x01])
#		thread.start_new_thread(self.restart)
		self.restart()

	def restart(self):
		print "waiting for restart..."
		sleep(10)
		GPIO.output(37,True)
		GPIO.output(38,True)
		GPIO.output(40,True)
#		thread.exit_thread()

	def debugVerifyCard(self):
		for i in range(1,16):
			if not (self.verifyBlock(i)):
				self.errorshow(10,0,1)

	def verifyCard(self):

		if(self.verifyBlock(1))and (self.verifyBlock(random.randint(2,15))):
			print "successful card:",self.readCardNum()
	
		else:
			print "except card:",self.readCardNum()
			return False
		#for i in range(1,16):
		#	print self.verifyBlock(i)
		#	self.randomBlockSaveAndWriteCard(i,self.apdu_Akey,self.apdu_Bkey)
		return True

	def renewBlock(self):
		self.randomBlockSaveAndWriteCard(1,self.apdu_Akey,self.apdu_Bkey)
		print "successful : renew block 1"
		newran=random.randint(2,15)
                self.randomBlockSaveAndWriteCard(newran,self.apdu_Akey,self.apdu_Bkey)
		print "seccessful : renew block ",newran

cardmonitor = CardMonitor()
cardobserver = cardober()
cardmonitor.addObserver( cardobserver )

while True:
	sleep(60)
#	print activeFlag
#	if activeFlag==0:
#		GPIO.output(37,True)
#		GPIO.output(38,True)
#		GPIO.output(40,True)
#		activeFlag=-1
#	if activeFlag==1:
#		activeFlag=0 	

#loadKey(0,apdu_Akey)
#loadKey(1,apdu_Bkey)

#for i in range(1,16):
#	randomBlockSaveAndWriteCard(i,apdu_Akey,apdu_Bkey)
#auth(4,"A",0)
#for i in range(4,7):
#	write(i,randomBytes())

#for i in range(0,16):
#	auth(i*4,"A",0)
#	for j in range(0,4):
#		read(i*4+j)

