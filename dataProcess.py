import xml.etree.ElementTree as ET
import xlsxwriter

# declear excel workbook and worksheets
sunject_id = raw_input('Enter subject ID:')
workbook = xlsxwriter.Workbook('data/Subject%s.xlsx' % sunject_id)
worksheet_event = workbook.add_worksheet('Event')
worksheet_data = workbook.add_worksheet('Data')

# read event tree and find row and column
eventTree = ET.parse('data/Subject%s_Event.xml' % sunject_id)
root = eventTree.getroot()
rowNum = len(root)
columnNum = len(root[0])
# data = [[0 for x in range(columnNum)] for y in range(rowNum)]
# write event worksheet
for row in range(rowNum):
	for column in range(columnNum):
		if(row == 0):
			worksheet_event.write(0, column, str(root[0][column].tag))

		else:
			worksheet_event.write(row, column, root[row][column].text)

# read data tree and find row and column
dataTree = ET.parse('data/Subject%s_Data.xml' % sunject_id)
root = dataTree.getroot()
rowNum = len(root)
columnNum = len(root[0])

# write data worksheet
for row in range(rowNum):
	for column in range(columnNum):
		if(row == 0):
			worksheet_data.write(0, column, str(root[0][column].tag))
		else:
			worksheet_data.write(row, column, root[row][column].text)

workbook.close()
