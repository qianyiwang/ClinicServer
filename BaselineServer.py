import socket
import datetime
from lxml import etree
from os import system
import thread
UDP_IP = "192.168.0.86"
UDP_PORT = 8001
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))
taskName = []
taskTime = []
hr = []
adas_last = ''
adas = []
hr_current = []
hr_last = 0;
location = []
location_current = []
location_last = ''
velocity = []
velocity_current = []
velocity_last = ''
subject_name = raw_input('Enter subject ID:')

def parseContent(data):
	return data[data.index('_')+1:];

def speakTaskOrder(data):
	# cmd = parseContent(data);
	# print str(datetime.datetime.now()), cmd
	if 'ClimateTaskIssued' in data:
		system('say please set driver temperature to 24.5 from SYNC')
	elif 'AudioTaskIssued' in data:
		system('say please play sleep away mp3 from SYNC')
	elif 'MCSTaskIssued' in data:
		system('say please bring up the MCS UI from the setting tag of SYNC')
	elif 'GoogleMapCmdIssued' in data:
		system('say please launch Google Map on your phone')
	elif 'EnterAddressIssued' in data:
		system('say please enter destination address')
	elif 'parkopediaIssued' in data:
		system('say please launch parkopedia on your phone')
while True:
	try:
		data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
		if 'QtEnd' in data:
				data = data[0:data.index('QtEnd')]

		if 'Human_' in data:
			thread.start_new_thread(speakTaskOrder, (data,))
	
		if "hr:" in data:
			print str(datetime.datetime.now()), data, adas_last
			hr_last = data[data.index(':')+1:];
			hr.append(hr_last)
			adas.append(adas_last)
			adas_last = ''
		elif "ADAS" in data:
			adas_last = data
		elif 'Velocity' in data:
			velocity_last = data[data.index(':')+1:];
		elif 'Location' in data:
			location_last = data[data.index(':')+1:];
		else:
			print str(datetime.datetime.now()), data
			taskName.append(data)
			taskTime.append(str(datetime.datetime.now()))
			hr_current.append(hr_last)
			location_current.append(location_last)
			velocity_current.append(velocity_last)
	
  	except KeyboardInterrupt:
		break
# generate the event xml
root = etree.Element("Subject%s_Event" % subject_name)
for i in range(0,len(taskName)):
	task = etree.SubElement(root, "Event")
	if 'SYNC' in taskName[i]:
		etree.SubElement(task, 'Source').text = 'SYNC'
	elif 'Phone' in taskName[i]:
		etree.SubElement(task, 'Source').text = 'Phone'
	elif 'Human' in taskName[i]:
		etree.SubElement(task, 'Source').text = 'Human'
	etree.SubElement(task, "Name").text = parseContent(taskName[i])
	etree.SubElement(task, "Time").text = taskTime[i]
	etree.SubElement(task, "HR").text = str(hr_current[i])
	etree.SubElement(task, "Location").text = str(location_current[i])
	etree.SubElement(task, "Velocity").text = str(velocity_current[i])
	etree.SubElement(task, "DrivingData").text = ''
et = etree.ElementTree(root)
et.write('data/Subject%s_BaselineEvent.xml' % subject_name, pretty_print=True)
# generate the data xml
root2 = etree.Element('Subject%s_Data' % subject_name)
for i in range(0, len(hr)):
	task2 = etree.SubElement(root2, "Data")
	etree.SubElement(task2, "Time").text = str(datetime.datetime.now())
	etree.SubElement(task2, "HR").text = hr[i]
	etree.SubElement(task2, "ADAS").text = adas[i]
	etree.SubElement(task2, "DrivingData").text = ''
et2 = etree.ElementTree(root2)
et2.write('data/Subject%s_BaselineData.xml' % subject_name, pretty_print=True)