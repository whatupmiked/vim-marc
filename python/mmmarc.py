#!/bin/python3
import vim

def singleMrcDisplay(stdin):
    displayed = ''
    split_record = stdin.replace('\x1f','$').replace('\x1d','\n').split('\x1e')
    split_record = split_record[:-1]
    LDR = split_record[0][:24]
    recordDIR = split_record[0][24:]
    displayed += "=LDR  " + LDR + "\n"
    directory = []
    j = 0
    for i in range(12, len(recordDIR)+12, 12):
        directory.append(recordDIR[j:i])
        j = i
    # Build the display record
    for i in range(len(directory)):
        displayed += "=" + directory[i][:3] + "  " + split_record[i+1] + "\n"
    return displayed + "\n"

def singleMrcCompile(stdin):
    display_record = stdin
    display_list = display_record.split('\n')
    display_list.pop()

    field_len = []
    field_tag = []

    for i in range(len(display_list[1:])):
        # Convert to utf-8 to get the correct ASCII character length
        field_len.append(len(display_list[i+1][5:].encode('utf-8')))
        field_tag.append(display_list[i+1][1:4])

    field_len = field_len[:-1]
    total_offset = 0
    field_offset = []
    for i in range(len(field_len)):
        field_offset.append(total_offset)
        total_offset += field_len[i]

    # Make Header
    # Make Payload
    recordDIR = ""
    for j in range(len(field_offset)):
        recordDIR += field_tag[j] + str(field_len[j]).zfill(4) + str(field_offset[j]).zfill(5)

    # CALCULATED
    LDR = display_list[0][6:]
    LDR += recordDIR

    compiled_record = ''
    eof_delimiter = '\x1d' #^]
    field_delimiter = '\x1e' #^^
    subfield_delimiter = '\x1f' #^_

    for k in range(1, len(display_list)-1):
        compiled_record += display_list[k].replace('$', subfield_delimiter)[6:] + field_delimiter

    compiled_record += eof_delimiter
    compiled_record = LDR + field_delimiter + compiled_record

    return compiled_record

def mrcDisplay():
    stdin = vim.current.buffer[0]
    records = []
    displayedOut = ''
    if stdin.count('\x1d') > 1:
        # split stdin
        records = stdin.replace('\x1d','\x1d\n').split('\n')
    else:
        records.append(stdin)
    for rcd in records:
        if rcd != '':
            displayedOut += singleMrcDisplay(rcd)
    del vim.current.buffer[:]
    # Split on new-line and return list since VIM
    # buffer throws vim.error on strings with newline
    displayedOutList = displayedOut.split("\n")
    vim.current.buffer[0] = displayedOutList[0]
    vim.current.buffer.append(displayedOutList[1:-1])

def mrcCompile():
    # Join on newline because vim buffers
    # Strip newlines from lines
    stdin = '\n'.join(vim.current.buffer) + '\n'
    compiledOut = ''
    if stdin.count('\n\n') > 1:
        records = []
        # split stdin
        records = stdin.split('\n\n')
        for rcd in records:
            if rcd != '':
                compiledOut += singleMrcCompile(rcd+'\n\n')
    else:
        compiledOut = singleMrcCompile(stdin)
    del vim.current.buffer[:]
    vim.current.buffer[0] = compiledOut
