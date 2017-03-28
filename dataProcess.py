import xml.etree.ElementTree as ET

sunject_id = raw_input('Enter subject ID:')
eventTree = ET.parse('data/Subject%s_Event.xml' % sunject_id)
root = eventTree.getroot()
# for child in root:
# 	for grandchild in child:
# 		print grandchild.tag
print len(root[0])
