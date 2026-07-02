from Encoding import R_encoding
from Encoding import I_encoding
from Encoding import S_encoding
from Encoding import J_encoding

def check_zero(rd,line):
    if(rd=="zero"):
        print("Error On Line",line,": Value Is Being Written On x0 or the zero register which doesn't support any writes")    
        return False
    else:
        return True

def main4(instruction,line):
    instruction=instruction.split(" ")
    operation = instruction[0]
    if (operation in R_encoding.R_operations) or (operation in I_encoding.I_operations) or (operation in J_encoding.J_operations):
        rd=instruction[1].split(",")[0]
        if(not check_zero(rd,line)):
            return False
    return True
