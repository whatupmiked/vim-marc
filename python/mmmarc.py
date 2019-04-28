#!/bin/python3
import vim
import sys
import argparse

def mrcCompile():
    """
    VIM Script function for converting a single line
    mrc record into a displayed mrc record
    """
    record = vim.current.buffer[0]
    split_record = record.replace('\x1f','$').replace('\x1d','\n').split('\x1e')
    split_record = split_record[:-1]
    LDR = split_record[0][:24]
    recordDIR = split_record[0][24:]
    vim.current.buffer[0] = "=LDR  " + LDR
    directory = []
    j = 0
    for i in range(12, len(recordDIR)+12, 12):
        directory.append(recordDIR[j:i])
        j = i
    # Print out the display record
    for i in range(len(directory)):
        vim.current.buffer.append("=" + directory[i][:3] + "  " + split_record[i+1])

def mrcDisplay():
    display_list = vim.current.buffer

    field_len = []
    field_tag = []

    for i in range(len(display_list[1:])):
        # Convert to utf-8 to get the correct ASCII character length
        field_len.append(len(display_list[i+1][5:].encode('utf-8')))
        field_tag.append(display_list[i+1][1:4])

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

    for k in range(len(display_list)-1):
        compiled_record += display_list[k+1].replace('$', subfield_delimiter)[6:] + field_delimiter

    compiled_record += eof_delimiter
    compiled_record = LDR + field_delimiter + compiled_record

    print(str(len(field_len)), str(len(field_tag)), str(len(field_offset)))
    del vim.current.buffer[:]
    vim.current.buffer[0] = compiled_record
