import vim
import xml.etree.ElementTree as ET
import re
from xml.etree.ElementTree import parse, XML, fromstring, tostring

def xmlAddMrkLeader(line, xmlElement):
    '''
    Takes as input a ldr field line from a mrk format file and
    adds the leader to the xml object
    '''
    leader = ET.SubElement(xmlElement, "leader")
    leader.text = line[6:]

def xmlAddMrkControlField(line, xmlElement):
    '''
    Takes as input a control field line
    from a mrk format file and adds the controlfield
    to the xml object
    '''
    controlField = ET.SubElement(xmlElement, "controlfield")
    controlField.set("tag", line[1:4])
    controlField.text = line[6:]

def xmlAddMrkDataField(line, xmlElement):
    '''
    Takes as input a line from a mrk format
    file and adds a datafield to the xml object
    '''
    dataField = ET.SubElement(xmlElement, "datafield")
    dataField.set("tag", line[1:4])
    if line[6] is not " ":
        dataField.set("ind1", line[6])
    else:
        dataField.set("ind1", "")
    if line[7] is not " ":
        dataField.set("ind2", line[7])
    else:
        dataField.set("ind2", "")
    subFields = line[8:]
    subFieldList = subFields.split("$")[1:]
    for sub in subFieldList:
        xmlAddMrkSubDataField(sub[0], sub[1:], dataField)

def xmlAddMrkSubDataField(code, text, xmlElement):
    '''
    Takes as input the subelement code and text
    and adds the subfield to the xml object
    '''
    subField = ET.SubElement(xmlElement, "subfield")
    subField.set("code", code)
    subField.text = text

def mrkAddXMLLDR(element):
    '''
    From an XML element create the MRK formatted
    leader line and return it as a string
    '''
    ldrLine = ""
    if not mrkCheckXMLTag(element.tag, "leader"):
        print("ERROR: Passed element that != leader")
    else:
        ldrLine += "=ldr  " + element.text
    return ldrLine

def mrkAddXMLControl(element):
    '''
    From an XML element create an MRK formatted
    control line and return it as a string
    '''
    ctrlLine = ""
    if not mrkCheckXMLTag(element.tag, "controlfield"):
        print("ERROR: Passed element that != controlfield")
    else:
        ctrlLine = "=" + mrkGetXMLAttrib(element, 'tag') + "  " + element.text
    return ctrlLine

def mrkAddXMLDataField(element):
    '''
    From an XML element create an MRK formatted datafield line and
    return it as a string
    '''
    dfLine = ""
    if not mrkCheckXMLTag(element.tag, "datafield"):
        print("ERROR: Passd element that != datafield")
    else:
        if mrkGetXMLAttrib(element, 'ind1') is "":
            ind1 = " "
        else:
            ind1 = mrkGetXMLAttrib(element, 'ind1')
        if mrkGetXMLAttrib(element, 'ind2') is "":
            ind2 = " "
        else:
            ind2 = mrkGetXMLAttrib(element, 'ind2')
        dfLine = "=" + mrkGetXMLAttrib(element, 'tag') + "  " + ind1 + ind2
        for sub in element:
            dfLine += mrkAddXMLSubDataField(sub)
    return dfLine

def mrkAddXMLSubDataField(element):
    '''
    From an XML element create an MRK formatted subfield string and
    return that string
    '''
    sfString = ""
    if not mrkCheckXMLTag(element.tag, "subfield"):
        print("ERROR: Passed element that != subfield")
    else:
        sfString += "$" + element.attrib['code'] + element.text
    return sfString

def mrkAddXMLRecord(element):
    '''
    From an XML element create a MRK formatted record
    '''
    #record = ""
    record = []
    if not mrkCheckXMLTag(element.tag, "record"):
        print("ERROR: Passed element that != record")
    else:
        for field in element:
            if mrkCheckXMLTag(field.tag, 'leader'):
                #record += mrkAddXMLLDR(field) + "\n"
                record.append(mrkAddXMLLDR(field))
            elif mrkCheckXMLTag(field.tag, 'controlfield'):
                #record += mrkAddXMLControl(field) + "\n"
                record.append(mrkAddXMLControl(field))
            elif mrkCheckXMLTag(field.tag, 'datafield'):
                #record += mrkAddXMLDataField(field) + "\n"
                record.append(mrkAddXMLDataField(field))
        #record += "\n" #Add newline between records
    return record

def mrkCheckXMLTag(tag, name):
    '''
    Return true if the tag matches the name
    Handle xmlns
    '''
    if '{' in tag:
        # xmlns detected
        if tag.split('}')[1] == name:
            return True
        else:
            return False
    else:
        if tag == name:
            return True
        else:
            return False

def mrkGetXMLAttrib(element, attr):
    '''
    Return the string representation of the element
    attrib and handle xmlns
    '''
    if '{' in element.attrib[attr]:
        attribute = element.attrib[attr].split("}")[1]
    else:
        attribute = element.attrib[attr]
    return attribute

def mrkToXML():
    '''
    VIM function that takes MRK file format standard input
    and converst to XML output
    '''
    root = ET.Element("collection")
    record = ET.SubElement(root, "record")
    newRecord = False

    # Join on newline because vim buffers
    # strip newlines from lines
    stdin = vim.current.buffer

    for line in stdin:
        if newRecord:
            record = ET.SubElement(root, "record")
            newRecord = False
        if re.search(r'^=ldr', line):
            xmlAddMrkLeader(line.strip(), record)
        elif re.search(r'^=00[1-9A-Za-z]{1}', line):
            xmlAddMrkControlField(line.strip(), record)
        elif re.search(r'^=(0([1-9A-Z][0-9A-Z])|0([1-9a-z][0-9a-z]))|(([1-9A-Z][0-9A-Z]{2})|([1-9a-z][0-9a-z]{2}))', line):
            xmlAddMrkDataField(line.strip(), record)
        elif line.strip() == "":
            newRecord = True

    xml_out = tostring(root)
    del vim.current.buffer[:]
    vim.current.buffer[0] = xml_out

def xmlToMrk():
    '''
    VIM function that takes XML standard input and converts it
    to MRK format
    '''
    # Join because vim buffers XML
    # operates on single string
    stdin = ''.join(vim.current.buffer)
    root = XML(stdin)
    #mrk_out = ""
    mrk_out_list = []
    for record in root:
        mrk_out_list += mrkAddXMLRecord(record)
        mrk_out_list += ['']
        #mrk_out += mrkAddXMLRecord(record)
    mrk_out_list += ['']

    #mrk_out_list = mrk_out.split('\n')
    del vim.current.buffer[:]
    vim.current.buffer[0] = mrk_out_list[0]
    vim.current.buffer.append(mrk_out_list[1:-1])

