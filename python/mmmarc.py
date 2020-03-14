"""
The mmmarc.py module is the backend to the VIM plugin
vim-marc and is used for converting mrk formatted files
to mrc format.
"""
import vim
import xml.etree.ElementTree as ET
import re
from xml.etree.ElementTree import parse, XML, fromstring, tostring

def xml_add_mrk_leader(line, xmlElement):
    '''
    Takes as input a ldr field line from a mrk format file and
    adds the leader to the xml object
    '''
    leader = ET.SubElement(xmlElement, "leader")
    leader.text = line[6:]

def xml_add_mrk_control_field(line, xmlElement):
    '''
    Takes as input a control field line
    from a mrk format file and adds the controlfield
    to the xml object
    '''
    controlField = ET.SubElement(xmlElement, "controlfield")
    controlField.set("tag", line[1:4])
    controlField.text = line[6:]

def xml_add_mrk_datafield(line, xmlElement):
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
        xml_add_mrk_subdatafield(sub[0], sub[1:], dataField)

def xml_add_mrk_subdatafield(code, text, xmlElement):
    '''
    Takes as input the subelement code and text
    and adds the subfield to the xml object
    '''
    subField = ET.SubElement(xmlElement, "subfield")
    subField.set("code", code)
    subField.text = text

def mrk_add_xml_ldr(element):
    '''
    From an XML element create the MRK formatted
    leader line and return it as a string
    '''
    ldrLine = ""
    if not mrk_check_xml_tag(element.tag, "leader"):
        print("ERROR: Passed element that != leader")
    else:
        ldrLine += "=ldr  " + element.text
    return ldrLine

def mrk_add_xml_control(element):
    '''
    From an XML element create an MRK formatted
    control line and return it as a string
    '''
    ctrlLine = ""
    if not mrk_check_xml_tag(element.tag, "controlfield"):
        print("ERROR: Passed element that != controlfield")
    else:
        ctrlLine = "=" + mrk_get_xml_attr(element, 'tag') + "  " + element.text
    return ctrlLine

def mrk_add_xml_datafield(element):
    '''
    From an XML element create an MRK formatted datafield line and
    return it as a string
    '''
    dfLine = ""
    if not mrk_check_xml_tag(element.tag, "datafield"):
        print("ERROR: Passd element that != datafield")
    else:
        if mrk_get_xml_attr(element, 'ind1') is "":
            ind1 = " "
        else:
            ind1 = mrk_get_xml_attr(element, 'ind1')
        if mrk_get_xml_attr(element, 'ind2') is "":
            ind2 = " "
        else:
            ind2 = mrk_get_xml_attr(element, 'ind2')
        dfLine = "=" + mrk_get_xml_attr(element, 'tag') + "  " + ind1 + ind2
        for sub in element:
            dfLine += mrk_add_xml_subdatafield(sub)
    return dfLine

def mrk_add_xml_subdatafield(element):
    '''
    From an XML element create an MRK formatted subfield string and
    return that string
    '''
    sfString = ""
    if not mrk_check_xml_tag(element.tag, "subfield"):
        print("ERROR: Passed element that != subfield")
    else:
        sfString += "$" + element.attrib['code'] + element.text
    return sfString

def mrk_add_xml_record(element):
    '''
    From an XML element create a MRK formatted record
    '''
    record = []
    if not mrk_check_xml_tag(element.tag, "record"):
        print("ERROR: Passed element that != record")
    else:
        for field in element:
            if mrk_check_xml_tag(field.tag, 'leader'):
                record.append(mrk_add_xml_ldr(field))
            elif mrk_check_xml_tag(field.tag, 'controlfield'):
                record.append(mrk_add_xml_control(field))
            elif mrk_check_xml_tag(field.tag, 'datafield'):
                record.append(mrk_add_xml_datafield(field))
    return record

def mrk_check_xml_tag(tag, name):
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

def mrk_get_xml_attr(element, attr):
    '''
    Return the string representation of the element
    attrib and handle xmlns
    '''
    if '{' in element.attrib[attr]:
        attribute = element.attrib[attr].split("}")[1]
    else:
        attribute = element.attrib[attr]
    return attribute

def vim_mrk_to_xml():
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
            xml_add_mrk_leader(line.strip(), record)
        elif re.search(r'^=00[1-9A-Za-z]{1}', line):
            xml_add_mrk_control_field(line.strip(), record)
        elif re.search(r'^=(0([1-9A-Z][0-9A-Z])|0([1-9a-z][0-9a-z]))|(([1-9A-Z][0-9A-Z]{2})|([1-9a-z][0-9a-z]{2}))', line):
            xml_add_mrk_datafield(line.strip(), record)
        elif line.strip() == "":
            newRecord = True

    xml_out = tostring(root)
    del vim.current.buffer[:]
    vim.current.buffer[0] = xml_out

def vim_xml_to_mrk():
    '''
    VIM function that takes XML standard input and converts it
    to MRK format
    '''
    # Join because vim buffers XML
    # operates on single string
    stdin = ''.join(vim.current.buffer)
    root = XML(stdin)
    mrk_out_list = []
    for record in root:
        mrk_out_list += mrk_add_xml_record(record)
        mrk_out_list += ['']
    mrk_out_list += [''] # EOF

    del vim.current.buffer[:]
    vim.current.buffer[0] = mrk_out_list[0]
    vim.current.buffer.append(mrk_out_list[1:-1])

def single_mrk_mrk(stdin):
    '''
    Converts a single mrc record into a
    multi-line record in the mrk format
    and returns the string
    '''
    directory = []
    split_record = stdin.replace('\x1f', '$').replace('\x1d', '\n').split('\x1e')
    split_record = split_record[:-1]
    # Create the Leader
    ldr = split_record[0][:24]
    record_dir = split_record[0][24:]
    displayed = "=ldr  " + ldr + "\n"
    j = 0
    for i in range(12, len(record_dir)+12, 12):
        directory.append(record_dir[j:i])
        j = i
    # Build the display record
    for i, value in enumerate(directory):
        displayed += "=" + value[:3] + "  " + split_record[i+1] + "\n"
    return displayed + "\n"

def single_mrc_21(stdin):
    '''
    Converts a single mrk record into a
    single-line record in the mrc format
    and returns the string
    '''
    field_len = []
    field_tag = []
    field_offset = []
    total_offset = 0
    display_record = stdin
    display_list = display_record.split('\n')
    display_list.pop()
    for i, value in enumerate(display_list[1:]):
        # Convert to utf-8 to get the correct ASCII character length
        field_len.append(len(display_list[i+1][5:].encode('utf-8')))
        field_tag.append(display_list[i+1][1:4])
    field_len = field_len[:-1]
    for value in field_len:
        field_offset.append(total_offset)
        total_offset += value
    # Make Header
    # Make Payload
    record_dir = ""
    for j, value in enumerate(field_offset):
        record_dir += field_tag[j] + str(field_len[j]).zfill(4) + str(value).zfill(5)
    # CALCULATED
    ldr = display_list[0][6:]
    ldr += record_dir
    compiled_record = ''
    eof_delimiter = '\x1d' #^]
    field_delimiter = '\x1e' #^^
    subfield_delimiter = '\x1f' #^_
    for k in range(1, len(display_list)-1):
        compiled_record += display_list[k].replace('$', subfield_delimiter)[6:] + field_delimiter
    compiled_record += eof_delimiter
    compiled_record = ldr + field_delimiter + compiled_record
    return compiled_record

def vim_mrc_to_mrk():
    '''
    VIM Function that takes a bibliographic record in .mrc
    format, converts it to .mrk format and places in the
    current VIM window
    '''
    stdin = vim.current.buffer[0]
    records = []
    displayed_out = ''
    if stdin.count('\x1d') > 1:
        # split stdin
        records = stdin.replace('\x1d', '\x1d\n').split('\n')
    else:
        records.append(stdin)
    for rcd in records:
        if rcd != '':
            displayed_out += single_mrk_mrk(rcd)
    del vim.current.buffer[:]
    # Split on new-line and return list because VIM
    # buffer throws vim.error on strings with newline
    displayed_out_list = displayed_out.split("\n")
    vim.current.buffer[0] = displayed_out_list[0]
    vim.current.buffer.append(displayed_out_list[1:-1])

def vim_mrk_to_mrc():
    '''
    VIM Function that takes a bibliographic record in .mrk
    format, converts it to .mrk format and places in the
    current VIM window
    '''
    # Join on newline because vim buffers
    # strip newlines from lines
    stdin = '\n'.join(vim.current.buffer) + '\n'
    compiled_out = ''
    if stdin.count('\n\n') > 1:
        records = []
        # split stdin
        records = stdin.split('\n\n')
        for rcd in records:
            if rcd != '':
                compiled_out += single_mrc_21(rcd+'\n\n')
    else:
        compiled_out = single_mrc_21(stdin)
    del vim.current.buffer[:]
    vim.current.buffer[0] = compiled_out

def vim_detect():
    '''
    Detect input format and return value
    '''
    first_line = vim.current.buffer[0]
    if first_line[0] == '=':
        # mrk format
        return 'mrk'
    elif re.search(r'^[0-9]', first_line[0]):
        # mrc format
        return 'mrc'
    elif first_line[0] == '<':
        # xml format
        return 'xml'
    else:
        return 'none'

def vim_xml():
    '''
    Detect input format and convert to XML
    '''
    file_format = vim_detect()
    if file_format == 'mrk':
        # mrk format
        vim_mrk_to_xml()
    elif file_format == 'mrc':
        # mrc format
        vim_mrc_to_mrk()
        vim_mrk_to_xml()
    elif file_format == 'xml':
        print("Already viewing XML file")
    elif file_format == 'none':
        print("Cannot detect file format")

def vim_mrk():
    '''
    Detect input format and convert to MRK
    '''
    file_format = vim_detect()
    if file_format == 'mrc':
        # mrc format
        vim_mrc_to_mrk()
    elif file_format == 'xml':
        # xml format
        vim_xml_to_mrk()
    elif file_format == 'mrk':
        print("Already viewing MRK file")
    elif file_format == 'none':
        print("Cannot detect file format")

def vim_mrc21():
    '''
    Detect input format and convert to MRK
    '''
    file_format = vim_detect()
    if file_format == 'mrk':
        # mrk format
        vim_mrk_to_mrc()
    elif file_format == 'xml':
        # xml format
        vim_xml_to_mrk()
        vim_mrk_to_mrc()
    elif file_format == 'mrc':
        print("Already viewing Marc21 file")
    elif file_format == 'none':
        print("Cannot detect file format")

def vim_marc_carousel():
    '''
    Detect input format and cycle through
    mrc -> mrk -> xml
    '''
    file_format = vim_detect()
    if file_format == 'mrc':
        # mrc format
        vim_mrc_to_mrk()
        vim.command('''set filetype=mrk''')
    elif file_format == 'mrk':
        # mrk format
        vim_mrk_to_xml()
        vim.command('''set filetype=xml''')
    elif file_format == 'xml':
        # xml format
        vim_xml_to_mrk()
        vim_mrk_to_mrc()
        vim.command('''set filetype=mrc''')
    elif file_format == 'none':
        print("Cannot detect file format")

