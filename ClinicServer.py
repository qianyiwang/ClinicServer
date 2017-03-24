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
hr_current = []
hr_last = 0

adas_last = ''
adas = []
adas_current = []

location = []
location_current = []
location_last = ''

velocity = []
velocity_current = []
velocity_last = ''

acceleration = []
acceleration_current = []
acceleration_last = '';

brake_state = []
brake_state_current = []
brake_state_last = ''

lane_offset = []
lane_offset_current = []
lane_offset_last = ''

steering_angle = []
steering_angle_current = []
steering_angle_last = ''

simulator_time_last = ''
simulator_time_current = []
simulator_time = []

subject_name = raw_input('Enter subject ID:')

def parseContent(data):
	return data[data.index('_')+1:];

def speakTaskOrder(data):
	# cmd = parseContent(data);
	# print str(datetime.datetime.now()), cmd
	if 'ClimateTaskIssued' in data:
		system('say please set driver temperature to 24.5 from smart watch')
	elif 'AudioTaskIssued' in data:
		system('say please play sleep away mp3 from smart watch')
	elif 'MCSTaskIssued' in data:
		system('say please bring up the MCS UI from smart watch')

while True:
	try:
		data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
		# check if data comes from simulator
		print data
		if '|' in data:
			all_vehicle_data = data.split('|')
			simulator_time_last = all_vehicle_data[1]+':'+all_vehicle_data[2]+':'+all_vehicle_data[3]
			velocity_last = all_vehicle_data[4]
			location_last = all_vehicle_data[5]+','+all_vehicle_data[6]
			steering_angle_last = all_vehicle_data[7]
			brake_state_last = all_vehicle_data[8]
			acceleration_last = all_vehicle_data[9]
			lane_offset_last = all_vehicle_data[10]
		# check if data comes from Qt 
		elif 'QtEnd' in data:
			data = data[0:data.index('QtEnd')]
		
		# check if the data comes from administrator
		elif 'Human_' in data:
			thread.start_new_thread(speakTaskOrder, (data,))

		elif "ADAS" in data:
			adas_last = data

		# store continous data
		elif "hr:" in data:
			print str(datetime.datetime.now()), data, adas_last
			hr_last = data[data.index(':')+1:]
			hr.append(hr_last)
			adas.append(adas_last)
			adas_last = ''
			velocity.append(velocity_last)
			location.append(location_last)
			acceleration.append(acceleration_last)
			brake_state.append(brake_state_last)
			lane_offset.append(lane_offset_last)
			steering_angle.append(steering_angle_last)
			simulator_time.append(simulator_time_last)

		# store event data
		else:
			# print str(datetime.datetime.now()), data
			taskName.append(data)
			taskTime.append(str(datetime.datetime.now()))
			hr_current.append(hr_last)
			adas_current.append(adas_last) 
			location_current.append(location_last)
			velocity_current.append(velocity_last)
			brake_state_current.append(brake_state_last)
			lane_offset_current.append(lane_offset_last)
			acceleration_current.append(acceleration_last)
			steering_angle_current.append(steering_angle_last)
			simulator_time_current.append(simulator_time_last)
  	except KeyboardInterrupt:
		break
# generate the event xml
root = etree.Element("Subject%s_Event" % subject_name)
for i in range(0,len(taskName)):
	task = etree.SubElement(root, "Event")
	if 'CCHMI Mobile' in taskName[i]:
		etree.SubElement(task, 'Source').text = 'CCHMI Mobile'
	elif 'CCHMI Watch' in taskName[i]:
		etree.SubElement(task, 'Source').text = 'CCHMI Watch'
	elif 'SYNC RC' in taskName[i]:
		etree.SubElement(task, 'Source').text = 'SYNC RC'
	elif 'Human' in taskName[i]:
		etree.SubElement(task, 'Source').text = 'Human'
	elif 'Vehicle Simulator' in taskName[i]:
		etree.SubElement(task, 'Source').text = 'Human'
	etree.SubElement(task, "Name").text = parseContent(taskName[i])
	etree.SubElement(task, "Time").text = taskTime[i]
	etree.SubElement(task, "HR").text = str(hr_current[i])
	etree.SubElement(task, "ADAS").text = adas_current[i]
	etree.SubElement(task, "Velocity").text = velocity_current[i]
	etree.SubElement(task, "Acceleration").text = acceleration_current[i]
	etree.SubElement(task, "Brake State").text = brake_state_current[i]
	etree.SubElement(task, "Steering Wheel Angle").text = steering_angle_current[i]
	etree.SubElement(task, "Lane Offset").text = lane_offset_current[i]
	etree.SubElement(task, "Location").text = location_current[i]
	etree.SubElement(task, "Simulator Time").text = simulator_time_current[i]

et = etree.ElementTree(root)
et.write('data/Subject%s_Event.xml' % subject_name, pretty_print=True)
# generate the continous data xml
root2 = etree.Element('Subject%s_Data' % subject_name)
for i in range(0, len(hr)):
	task2 = etree.SubElement(root2, "Data")
	etree.SubElement(task2, "Time").text = str(datetime.datetime.now())
	etree.SubElement(task2, "HR").text = hr[i]
	etree.SubElement(task2, "ADAS").text = adas[i]
	etree.SubElement(task, "Velocity").text = velocity[i]
	etree.SubElement(task, "Acceleration").text = acceleration[i]
	etree.SubElement(task, "Brake State").text = brake_state[i]
	etree.SubElement(task, "Steering Wheel Angle").text = steering_angle[i]
	etree.SubElement(task, "Lane Offset").text = lane_offset[i]
	etree.SubElement(task, "Location").text = location[i]
	etree.SubElement(task, "Simulator Time").text = simulator_time[i]
et2 = etree.ElementTree(root2)
et2.write('data/Subject%s_Data.xml' % subject_name, pretty_print=True)