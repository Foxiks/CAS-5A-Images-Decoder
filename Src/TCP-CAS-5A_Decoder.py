import sys, socket, bitstring, argparse, time
from datetime import datetime
parser = argparse.ArgumentParser()
parser.add_argument("-p", "--port", help="port")
parser.add_argument("-ip", "--ip", help="ip")
ip = parser.parse_args().ip
port1 = parser.parse_args().port
port = int(port1)
try:
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error:
	print('Failed to create socket')
	sys.exit()
n = datetime.now().strftime('%H_%M_%S')
c=0
sync_f = 'n'
host = ip
try:
	remote_ip = socket.gethostbyname( host )
except socket.gaierror:
	print('Hostname could not be resolved. Exiting')
	time.sleep(5)
	sys.exit()
s.connect((remote_ip , port))
print('CAS-5A (FO-118) Images decoder by Egor UB1QBJ')
print('Connected to ' + str(remote_ip) + ":" + str(port))
print("")
while True:
	reply = s.recv(4096).hex()
	if(str(reply[:50]) != "c00086a240404040608682a66a82406103f0010001000100a7"):
		if(int(str(reply[36:]).find('ffd8')) >= int(0)):
			sync_f = 't'
			n = datetime.now().strftime('%H_%M_%S')
			d0 = str(reply)[36:-2]
			d1 = str(d0).replace("dbdc", "c0")
			d2 = str(d1).replace("dcdd","db")
			d3 = str(d2).replace("dbdd","db")
			with open('out_iamge_'+str(n)+'.jpg', 'ab') as out_file:
				bitstring.BitArray(hex=str(d3)).tofile(out_file)
			c+=1
			print('New image frame! '+str(c) + ' [First frame received!]'+str(''*130), end='\r')
		if(int(str(reply[36:]).find('ffd8')) < int(0)):
			d0 = str(reply)[36:-2]
			d1 = str(d0).replace("dbdc", "c0")
			d2 = str(d1).replace("dcdd","db")
			d3 = str(d2).replace("dbdd","db")
			with open('out_iamge_'+str(n)+'.jpg', 'ab') as out_file:
				bitstring.BitArray(hex=str(d3)).tofile(out_file)
			c+=1
			if(sync_f == 't'):
				print('New image frame! '+str(c) + ' [First frame received!]'+str(''*130), end='\r')
			else:
				print('New image frame! '+str(c) + ''' [You didn't get the sync word for the photo. This means that you will not be able to view the photo. Try to get another photo...]''', end='\r')
	if(str(reply[:50]) == "c00086a240404040608682a66a82406103f0010001000100a7"):
		print('Telemetry frame! Skip...'+str(' '*145), end='\r')
		n = datetime.now().strftime('%H_%M_%S')
		c=0
		sync_f = 'n'