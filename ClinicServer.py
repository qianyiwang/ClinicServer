import socket
import datetime
from lxml import etree
UDP_IP = "10.0.0.189"
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
subject_name = raw_input('Enter subject ID:')
while True:
	try:
		data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
		if 'QtEnd' in data:
				data = data[0:data.index('QtEnd')]
		print str(datetime.datetime.now()), data, addr
		if "hr:" in data:
			hr_last = data[data.index(':')+1:];
			hr.append(hr_last)
			adas.append(adas_last)
			adas_last = ''
		if "ADAS" in data:
			adas_last = data
		else:
			taskName.append(data)
			taskTime.append(str(datetime.datetime.now()))
			hr_current.append(hr_last) 
	
  	except KeyboardInterrupt:
		break
# generate the event xml
root = etree.Element("Subject%s_Event" % subject_name)
for i in range(0,len(taskName)):
	task = etree.SubElement(root, "Event")
	etree.SubElement(task, "Name").text = taskName[i]
	etree.SubElement(task, "Time").text = taskTime[i]
	etree.SubElement(task, "HR").text = str(hr_current[i])
et = etree.ElementTree(root)
et.write('Subject%s_Event.xml' % subject_name, pretty_print=True)
# generate the data xml
root2 = etree.Element('Subject%s_Data' % subject_name)
for i in range(0, len(hr)):
	task2 = etree.SubElement(root2, "Data")
	etree.SubElement(task2, "HR").text = hr[i]
	etree.SubElement(task2, "ADAS").text = adas[i]
et2 = etree.ElementTree(root2)
et2.write('Subject%s_Data.xml' % subject_name, pretty_print=True)