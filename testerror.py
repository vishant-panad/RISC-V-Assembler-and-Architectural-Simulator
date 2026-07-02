from Encoding import R_encoder
from Encoding import I_encoder
from Encoding import S_encoder
from Encoding import B_encoder
from Encoding import U_encoder
from Encoding import J_encoder


register_map = {
"zero": "00000",
"ra":"00001", 
"sp": "00010",
"gp": "00011",
"tp":"00100",
"t0":"00101",
"t1":"00110",
"t2":"00111",
"s0":"01000",
"fp":"01000",
"s1":"01001",
"a0":"01010",
"a1":"01011",
"a2":"01100",
"a3":"01101",
"a4":"01110",
"a5":"01111",
"a6":"10000",
"a7":"10001",
"s2":"10010",
"s3":"10011",
"s4":"10100",
"s5":"10101",
"s6":"10110",
"s7":"10111",
"s8":"11000",
"s9":"11001",
"s10":"11010",
"s11":"11011",
"t3":"11100",
"t4":"11101",
"t5":"11110",
"t6":"11111"
}

# Check if the register is valid
def validate_register(reg:str):
    if reg not in register_map.keys():
        return False
    return True

# Check if the instruction is valid
def validate_instruction(line:str):
    operation, operands = line.split()
    
    # Handle R, I, or B type operations
    if operation in R_encoder.R_ops or operation in I_encoder.I_ops or operation in B_encoder.B_ops:
        if operation in R_encoder.R_ops:
            rd, rs1, rs2 = operands.split(",")
            if not validate_register(rd) or not validate_register(rs1) or not validate_register(rs2):
                 return False, "register not found"
            return True, "valid"
        elif operation in I_encoder.I_ops:
            if operation == "lw": # special case for lw
                rd, other = operands.split(",")
                if not validate_register(rd):
                    return False, "register not found"
                num, rd = other.split("(")
                rd = rd.rstrip(")")
                if not validate_register(rd):
                    return False, "register not found"
                if int(num) < -1 * 2**11 or int(num) > (2**11-1):
                    return False, "out of bound"
                return True, "valid"
            else:
                rd, rs, num = operands.split(",")
                if not validate_register(rd) or not validate_register(rs):
                    return False, "register not found"
                if int(num) < -1 * 2**11 or int(num) > (2**11-1):
                    return False, "out of bound"
                return True, "valid"
        else: # for B encoding
            rs1, rs2, num = operands.split(",") 
            if not validate_register(rs1) or not validate_register(rs2):
                return False, "register not found"
            if num.isalpha():
                return True, "valid"
            if num.isnumeric() or (num[0] == '-' and num[1:].isnumeric()):
                if int(num) < -1 * 2**12 or int(num) > (2**12-1):
                    return False, "out of bound"
            return True, "valid"
    
    # Handle S, U, or J type operations
    elif operation in S_encoder.S_ops or operation in U_encoder.U_ops or operation in J_encoder.J_ops:
        if operation in S_encoder.S_ops:
            rs2, other = operands.split(",")
            num, rs1 = other.split("(")
            rs1 = rs1.rstrip(")")
            if not validate_register(rs1) or not validate_register(rs2):
                return False, "register not found"
            if int(num) < -1 * 2**11 or int(num) > (2**11-1):
                return False, "out of bound"
            return True, "valid"
        elif operation in U_encoder.U_ops:
            rd, num = operands.split(",")
            if not validate_register(rd):
                return False, "register not found"
            if int(num) < -2147483648 or int(num) > (2147483647):
                return False, "out of bound"
            return True, "valid"
        else: # for J encoding
            rd, num = operands.split(",")
            if not validate_register(rd):
                return False, "register not found"
            if num.isnumeric() or (num[0] == "-1" and num[1:].isnumeric()):
                if int(num) < -1048576 or int(num) > (1048575):
                    return False, "out of bound"
            return True, "valid"
    
    # If the opcode is not recognized
    else:
        return False, "opcode not found"

# a = open("test_assembly.txt","r")
# lines = a.readlines()
# for x in lines:
#     print(x, end=" ")
#     print(validate_instruction(x))  
