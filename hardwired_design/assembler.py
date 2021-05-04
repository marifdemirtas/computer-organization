'''
    A basic assembler that takes a file in.txt which contains
    the code written accordingly to project file and outputs
    out.txt which is the hex version of the given code to be
    directly loaded into Logisim RAM, using Load From Image File
    option.

    There is a SKIP command to leave some bytes empty. For example,
    the line SKIP 8 will leave 16 bytes empty (or 8 cells in the default
    Logisim RAM settings). SKIP can be used with BRA to set a
    starting point in programs.
'''

regsel3b = {
    "R0": '000',
    "R1": '001',
    "R2": '010',
    "R3": '011',
    "PC": '101',
    "AR": '110',
    "SP": '111'
}

regsel2b = {
    "R0": '00',
    "R1": '01',
    "R2": '10',
    "R3": '11'
}

opcodes = {
    "LD": '00000',
    "ST": '00001',
    "MOV": '00010',
    "PSH": '00011',
    "PUL": '00100',
    "ADD": '00101',
    "SUB": '00110',
    "DEC": '00111',
    "INC": '01000',
    "AND": '01001',
    "OR": '01010',
    "NOT": '01011',
    "LSL": '01100',
    "LSR": '01101',
    "BRA": '01110',
    "BEQ": '01111',
    "BNE": '10000',
    "CALL": '10001',
    "RET": '10010',
}

address_mode = {
    "IM": '0',
    "D": '1'
}

type_1_inst = ["LD", "ST", "BRA", "BEQ", "BNE", "CALL"]


def create_instruction(readable_code=""):
    '''
    Takes in a line of code written in the format
    specified in project file, outputs the
    corresponding hex code.
    '''
    if readable_code == "":
        readable_code = input()
    opcode, *splitted = readable_code.upper().split()
    if opcode == "SKIP":
        return "{}*00".format(int(splitted[0]) * 2)

    binary_code = opcodes.get(opcode, "00000")
    if opcode in type_1_inst:
        binary_code += regsel2b.get(splitted[0], "00")
        binary_code += address_mode.get(splitted[1], "0")
        value = splitted[2][2:] if len(splitted[2]) == 4 else splitted[2]
        value = "0" * 8 + bin(int(value, 16))[2:]
        binary_code += value[-8:]
    else:
        binary_code += regsel3b.get(splitted[0], "000")
        binary_code += regsel3b.get(splitted[1], "000")
        binary_code += regsel3b.get(splitted[2],
                                    "000") if len(splitted) == 3 else "000"
        binary_code += "00"

    formatted_binary_code = ""
    hex_code = ""
    while binary_code:
        formatted_binary_code += binary_code[:4] + " "
        hex_code += hex(int(binary_code[:4], 2))[2:]
        binary_code = binary_code[4:]

    formatted_binary_code[:-1]
    hex_code = hex_code[0:2] + " " + hex_code[2:4]

    # print(formatted_binary_code)
    # print(hex_code)
    return hex_code


with open('./in.txt', 'r') as fp, open('./out.txt', 'w') as op:
    line = fp.readline()
    op.write("v2.0 raw\n")
    while line:
        op.write(create_instruction(line) + " ")
        line = fp.readline()
