'''
    A basic microprogrammer that takes in a file in.txt that
    contains the microprogram written accordingly to
    project file, and outputs the out.txt Logisim image file
    that contains the hex version of the code. Microprogram
    format is explained in our project report.

    You can use labels in your code. You need to specify label EMPTY
    even if you do not use the address value of a microinstruction.
    You can omit the NOP value for micro operations in field 2, but
    if you want to use a type-2 micro operation on its own, you need
    to write NOP for type-1 micro operation.
'''

conditions = {
    "U": '00',
    "I": '01',
    "Z": '10',
}

branches = {
    "JMP": '00',
    "CALL": '01',
    "RET": '10',
    "MAP": '11',
}

addresses = dict()

cat1_ops = {
    "NOP": '00000',
    "READ": '00001',
    "MREAD": '00010',
    "STORE": '00011',
    "BRANCH": '00100',
    "FLAG": '00101',
    "SETSTACK": '00110',
#    "ALUA": '00111',
#    "ALUAB": '01000',
    "INCR": '01001',
    "DECR": '01010',
    "GETSTACK": '01011',
    "CHNGSTACK": '01100',
    "STRSTACK": '01101',
    "PCTIRH": '01110',
    "PCTIRL": '01111',
    "MOVM": '10000',
    "NOTM": '10001',
    "LSLM": '10010',
    "LSRM": '10011',
    "ADDM": '10100',
    "SUBM": '10101',
    "ANDM": '10110',
    "ORM": '10111'
}

cat2_ops = {
    "NOP": '00',
    "INCPC": '01',
    "INCSTACK": '10',
    "DECSTACK": '11'
}


current_address = 0

binary_instructions = list()

minsts = dict()

empty_address = '00000000'
address_form = '08b'
max_OPs = 2
empty_instruction = '00000' + '00' + '00' + '00'


def first_run(code=""):
    '''
    Takes the given line of code, transforms it to binary
    and saves the label in to the addresses dictionary.
    '''
    if code == "":
        code = input()
    code = code.upper()
    global current_address
    # CHECK FOR ORG
    if code.find("ORG") != -1:
        org_address = code.split()[-1]
        current_address = int(org_address)
        return ''

    # CHECK IF LABEL EXISTS
    if code.find(":") != -1:
        label, *code = code.split(':')
        addresses[label] = format(current_address, address_form)
        code = code[0]

    # EXTRACT mOP, CD, BR, AD
    *m_OPs, cd, br, ad = code.split() 

    binary_code = ""
    while len(m_OPs) < max_OPs:
        m_OPs.append('NOP')
    print(m_OPs)

    binary_code += cat1_ops.get(m_OPs[0].split(',')[0], '00000')
    binary_code += cat2_ops.get(m_OPs[1].split(',')[0], '00')
    print(binary_code)
#    for op in m_OPs:
#        op = op.split(',')[0]
#        binary_code += cat1_ops.get(op, cat2_ops.get(op, '00'))

    binary_code += conditions.get(cd, "00")
    binary_code += branches.get(br, "00")

    if ad == 'NEXT' or ad == 'EMPTY':
        binary_code += 'n'
    else:
        binary_code += ad  # Change this to NEXT

    minsts[format(current_address, address_form)] = binary_code

    current_address += 1


def second_run():
    '''
    Fills in the values for addresses and labels.
    '''
    my_address = 0
    while my_address < current_address:
        inst = minsts.get(format(my_address, address_form), empty_instruction)
        if inst[-1] == 'n':
            inst = inst[0:-1] + format(my_address + 1, address_form)
        else:
            label = inst.replace('0', '').replace('1', '')
            if label == "":
                inst = inst + empty_address
            else:
                inst = inst.replace(label, addresses.get(label, empty_address))
        minsts[format(my_address, address_form)] = inst
        my_address += 1


with open('./in.txt', 'r') as fp, open('./out.txt', 'w') as op:
    line = fp.readline()
    while line:
        first_run(line)
        line = fp.readline()

    second_run()

    op.write("v2.0 raw\n")
    used_addresses = list()
    for item in sorted(minsts.items()):
        used_addresses.append(item[0])

    for address in used_addresses:
        binary_code = minsts.get(address)
        hex_code = ''
        # print(address)
        # print(binary_code)
        while binary_code:
            hex_code = hex(int(binary_code[-4:], 2))[2:] + hex_code
            binary_code = binary_code[:-4]
        # print(hex_code)
        op.write(hex_code + ' ')
