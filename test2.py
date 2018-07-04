import xml.etree.ElementTree as ET

tree = ET.parse('ant.xml')
root = tree.getroot()

for child in root:
    print (child.tag, child.attrib)
print("next")
#print(root[0][0].text)
#for neighbor in root[1]:
#    print (neighbor.attrib)
#print("end")
for unit in root:
    print("unit:")
    print (unit)
    for elt in unit:
        print("elt:")
        print (elt)
print('end')

for test in root.iter("{http://www.srcML.org/srcML/src}comment"):
    ctext = test.text
    ctype = test.get('type')
    cformat = test.get('format')
    print("type: ", ctype)
    print("format: ", cformat)
    print(ctext)
print('end2')