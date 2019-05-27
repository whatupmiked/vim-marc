"""
The mmmarc.py module is the backend to the VIM plugin
vim-marc and is used for converting mrk formatted files
to mrc format.
"""
import vim

def single_mrc_display(stdin):
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

def single_mrc_compile(stdin):
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

def vim_mrc_display():
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
            displayed_out += single_mrc_display(rcd)
    del vim.current.buffer[:]
    # Split on new-line and return list because VIM
    # buffer throws vim.error on strings with newline
    displayed_out_list = displayed_out.split("\n")
    vim.current.buffer[0] = displayed_out_list[0]
    vim.current.buffer.append(displayed_out_list[1:-1])

def vim_mrc_compile():
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
                compiled_out += single_mrc_compile(rcd+'\n\n')
    else:
        compiled_out = single_mrc_compile(stdin)
    del vim.current.buffer[:]
    vim.current.buffer[0] = compiled_out
