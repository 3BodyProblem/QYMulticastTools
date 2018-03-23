# -*- coding: utf-8 -*-
"""
        @brief  组播数据接收工具
        @barry  barry
        @date   2018/3/21
"""


import os, sys, getopt, time, socket

  
SENDERIP = '0.0.0.0'#'192.168.3.220' 
MYPORT = 0#3400
MYGROUP = ''#'230.12.1.1'  


def usage():
	print( "\nUsage:" )
	print( "python3 QYMultirecv.py -h  [命令帮助]" )
	print( "\n" )
	print( """python3 QYMultirecv.py --mcip=230.12.1.1 --mcport=3400 [命令接收组播行情 --mcip=组播ip --mcport=组播端口]""" )
print( "\n" )

  
def receiver():  
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  
	#allow multiple sockets to use the same PORT number  
	sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)  
	#Bind to the port that we know will receive multicast data  
	sock.bind((SENDERIP,MYPORT))  
	#tell the kernel that we are a multicast socket  
	#sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 255)  
	#Tell the kernel that we want to add ourselves to a multicast group  
	#The address for the multicast group is the third param  
	status = sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, socket.inet_aton(MYGROUP) + socket.inet_aton(SENDERIP));  

	print( '[OK] receiver started!' )
	sock.setblocking(0)  
	#ts = time.time()  
	while 1:  
		try:  
			data, addr = sock.recvfrom(8192)  
		except Exception as e:
			pass
			#print( e )
			#time.sleep( 1 )
		else:  
			print( data )


if __name__ == "__main__":
	opts, args = getopt.getopt( sys.argv[1:], "h", ["mcip=", "mcport="] )
	if len(opts) == 0:
		usage()
		sys.exit( 0 )

	for op, value in opts:
		if op in( "--mcip" ):
			MYGROUP = value
		elif op in( "--mcport" ):
			MYPORT = int(value)
		elif op == "-h":
			usage()
			sys.exit( 0 )

	receiver()  


