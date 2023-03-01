import sys, socket, bitstring, argparse, time, os
from datetime import datetime
parser = argparse.ArgumentParser()
parser.add_argument("-p", "--port", help="port")
parser.add_argument("-ip", "--ip", help="ip")
ip = parser.parse_args().ip
port1 = parser.parse_args().port
port = int(port1)
err = 0
c_num = 0
try:
	os.remove('data.ts')
except OSError:
	None
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
	reply = reply[38:]
	total_frames = bitstring.BitStream(hex=str(reply[:4])).read('uint')
	frame_number = bitstring.BitStream(hex=str(reply[4:8])).read('uint')
	if(int(frame_number)!=int(int(c_num)+1)):
		err+= int(int(frame_number))-int(c_num)
	frame_length = bitstring.BitStream(hex=str(reply[8:12])).read('uint')
	frame_y = bitstring.BitStream(hex=str(reply[12:14])).read('uint')
	frame_m = str(bitstring.BitStream(hex=str(reply[14:16])).read('uint')).zfill(2)
	frame_d = str(bitstring.BitStream(hex=str(reply[16:18])).read('uint')).zfill(2)
	frame_H = str(bitstring.BitStream(hex=str(reply[18:20])).read('uint')).zfill(2)
	frame_MIN = str(bitstring.BitStream(hex=str(reply[20:22])).read('uint')).zfill(2)
	frame_S = str(bitstring.BitStream(hex=str(reply[22:24])).read('uint')).zfill(2)
	cam_num = bitstring.BitStream(hex=str(reply[24:26]))
	bit_cam_num = cam_num.read('bin')
	b7 = bit_cam_num[:5]
	camera_number = str(bitstring.BitStream(bin=b7).read('uint')).zfill(2)
	b2 = bit_cam_num[5:8]
	pc = bitstring.BitStream(hex=str(reply[26:28])).read('bin')
	photo_counter = bitstring.BitStream(bin=str(b2)+str(pc)).read('uint')
	photo_specs = bitstring.BitStream(hex=str(reply[28:30]))
	bit_photo_specs = photo_specs.read('bin')
	quality = bit_photo_specs[:4]
	if(quality == '0000'):
		quality = 'High'
	if(quality == '0001'):
		quality = 'Medium'
	if(quality == '0010'):
		quality = 'Low'
	resolution = bit_photo_specs[4:8]
	if(resolution == '0000'):
		resolution = '800x480'
	if(resolution == '0001'):
		resolution = '1280x720'
	if(resolution == '0010'):
		resolution = '320x240'
	if(resolution == '0011'):
		resolution = '1440x896'
	if(resolution == '0100'):
		resolution = '640x480'
	if(resolution == '0101'):
		resolution = '1920x1080'
	if(resolution == '0110'):
		resolution = '800x600'
	if(resolution == '0111'):
		resolution = '1024x768'
	reply = reply[30:]
	reply = [reply[i:i+2] for i in range(0, len(reply), 2)]
	reply = ' '.join(reply)
	if(len(reply) > 510):
		if(int(str(reply).find('ff d8')) >= int(0)):
			sync_f = 't'
			n = datetime.now().strftime('%H_%M_%S')
			d0 = str(reply)[:-3]
			d1 = str(d0).replace("db dc", "c0")
			d2 = str(d1).replace("dc dd","db")
			d3 = str(d2).replace("db dd","db")
			d3 = d3.replace(' ', '')
			with open('out_image_'+str(n)+'.jpg', 'ab') as out_file:
				bitstring.BitArray(hex=str(d3)).tofile(out_file)
			with open('data.ts', 'a') as out_file_ts:
				out_file_ts.write(str('out_image_'+str(n)+'.jpg'))
			c+=1
			if(sync_f == 't'):
				rx = 'Normal!'
			else:
				rx = 'Bad! Synchronization code not received!'
			c_num = int(frame_number)
			print('RX Mode: '+rx+' | Total frames: '+str(total_frames)+' | Frame number: '+str(frame_number)+' | Frame length: '+str(frame_length)+' | Photo time: 20'+str(frame_y)+'.'+str(frame_m)+'.'+str(frame_d)+' '+str(frame_H)+':'+str(frame_MIN)+':'+str(frame_S)+' | Camera number: '+str(camera_number)+' | Photo counter: '+str(photo_counter)+' | Resolution: '+str(resolution)+' | Quality: '+str(quality)+str(' '*4), end='\r')
		if(int(str(reply).find('ff d8')) < int(0)):
			d0 = str(reply)[:-3]
			d1 = str(d0).replace("db dc", "c0")
			d2 = str(d1).replace("dc dd","db")
			d3 = str(d2).replace("db dd","db")
			d3 = d3.replace(' ', '')
			with open('out_image_'+str(n)+'.jpg', 'ab') as out_file:
				bitstring.BitArray(hex=str(d3)).tofile(out_file)
			c+=1
			if(sync_f == 't'):
				rx = 'Normal!'
			else:
				rx = 'Bad! Synchronization code not received!'
			c_num = int(frame_number)
			print('RX Mode: '+rx+' | Total frames: '+str(total_frames)+' | Frame number: '+str(frame_number)+' | Total frames loss: '+str(err)+' | Frame length: '+str(frame_length)+' | Photo time: 20'+str(frame_y)+'.'+str(frame_m)+'.'+str(frame_d)+' '+str(frame_H)+':'+str(frame_MIN)+':'+str(frame_S)+' | Camera number: '+str(camera_number)+' | Photo counter: '+str(photo_counter)+' | Resolution: '+str(resolution)+' | Quality: '+str(quality)+str(' '*4), end='\r')
	if(len(reply) <= 510):
		print('Telemetry frame! Skip...'+str(' '*228), end='\r')
		n = datetime.now().strftime('%H_%M_%S')
		c=0
		sync_f = 'n'
		err = 0
		try:
			os.remove('data.ts')
		except OSError:
			None
#print('Total frames: '+str(total_frames)+' | Frame number: '+str(frame_number)+' | Frame length: '+str(frame_length)+' | Photo time: 20'+str(frame_y)+'.'+str(frame_m)+'.'+str(frame_d)+' '+str(frame_H)+':'+str(frame_MIN)+':'+str(frame_S)+' | Camera number: '+str(camera_number)+' | Photo counter: '+str(photo_counter)+' | Resolution: '+str(resolution)+' | Quality: '+str(quality))