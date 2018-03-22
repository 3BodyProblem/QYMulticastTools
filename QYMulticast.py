# -*- coding: utf-8 -*-
"""
        @brief  Step数据文件的组播程序
        @note	以独占方式处理文件
	@barry	barry
	@date	2018/3/21
"""


import os, sys, time, getopt, struct
from socket import *


class UDPSender:
	"""
		组播放发送类
	"""
	sVersion = r'[Version 1.0.0]'			# version string
	bInitialized = False				# initialize flag

	def __init__( self, sLocalIP, nLocalPort, sMCGroupIP, nMCPort, nMCTTL ):
		self.__sLocalIP = sLocalIP
		self.__nLocalPort = nLocalPort
		self.__sMCGroupIP = sMCGroupIP
		self.__nMCPort = nMCPort
		self.__nMCTTL = nMCTTL
		self.__oMCSocket = None
		self.__oMCTTL_Bin = None
		print( "UDPSender.__init()__ : [INF] object created!" )

	def Initialize( self ):
		if UDPSender.bInitialized == True:
			return True

		print( 'UDPSender.Initialize() : [INF] initializing ............' )
		self.__oMCSocket = socket( AF_INET, SOCK_DGRAM, IPPROTO_UDP )
		print( 'UDPSender.Initialize() : [INF] socket created!' )
		self.__oMCSocket.bind( (self.__sLocalIP, self.__nLocalPort ) )
		print( 'UDPSender.Initialize() : [INF] bind ip!' )
		self.__oMCTTL_Bin = struct.pack( '@i', self.__nMCTTL )
		self.__oMCSocket.setsockopt( IPPROTO_IP, IP_MULTICAST_TTL, self.__oMCTTL_Bin )
		print( 'UDPSender.Initialize() : [INF] set socket option' )
		nStatus = self.__oMCSocket.setsockopt( IPPROTO_IP, IP_ADD_MEMBERSHIP, inet_aton( self.__sMCGroupIP ) + inet_aton( self.__sLocalIP ) )
		UDPSender.bInitialized = True
		print( 'UDPSender.Initialize() : [OK] multicast sender has been initialized!' )

		return True


	def SendMCPkg( self, bData ):
		if UDPSender.bInitialized == False:
			raise Exception( "UDPSender.SendMCPkg() : socket is not initialized!" )

		self.__oMCSocket.sendto( bData, ( self.__sMCGroupIP, self.__nMCPort ) )
		#print( "UDPSender.SendMCPkg() : sending data .........." )
		print( bData )


def usage():
	print( "\nUsage:" )
	print( "python3 QYMulticast.py -h  [命令帮助]" )
	print( "\n" )
	print( """python3 QYMulticast.py -f ./20180226.dat --ip=192.168.3.220 --port=31256 --mcip=230.12.1.1 --mcport=3400 [命令组播本地行情 -f/--file=本地行情文件 --ip=本机ip --port=本机port --mcip=组播ip --mcport=组播端口]""" )
	print( "\n" )


if __name__ == '__main__':
	try:
		sDataSourcePath = ""#"20180226.dat"
		sSendIP = ""#"192.168.3.220"
		nSendPort = ""#31256
		sMCIP = ""#"230.12.1.1"
		nMCPort = ""#3400
		opts, args = getopt.getopt( sys.argv[1:], "hf:", ["file=","ip=","port=","mcip=", "mcport="] )
		if len(opts) == 0:
			usage()
			sys.exit( 0 )
		for op, value in opts:
			if op in ( "-f", "--file" ):
				sDataSourcePath = value
			elif op in ( "--ip" ):
				sSendIP = value
			elif op in( "--port" ):
				nSendPort = int( value )
			elif op in( "--mcip" ):
				sMCIP = value
			elif op in( "--mcport" ):
				nMCPort = int(value)
			elif op == "-h":
				usage()
				sys.exit( 0 )

		oDataFile = open( sDataSourcePath, 'rb' )
		oMCSender = UDPSender( sSendIP, nSendPort, sMCIP, nMCPort, 255 )

		if None == oDataFile:
			raise Exception( 'cannot access data source file!' )
		oMCSender.Initialize()

		while True:
			bReadData = oDataFile.read( 50 )
			if not bReadData:
				print( '[INF] End Of File................................' )
				break

			#nHeadPos = bReadData.find( b'8=FIXT.1.1' )
			nLenPos = bReadData.find( b'9=' ) + 2
			nLenEnd = bReadData[nLenPos:].find( b'\x01' )
			nLenValue = int( bReadData[nLenPos:nLenPos+nLenEnd] )
			bReadData += oDataFile.read( nLenValue - 50 + nLenPos + nLenEnd + 7 + 1 )
			#print( bReadData )

			oMCSender.SendMCPkg( bReadData )
			#time.sleep( 1 )

	except Exception as e:
		print( r'[EXCEPTION] ' + str(e) )
	finally:
		print( "#########################################################################" )





