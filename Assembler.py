import Encoding.R_encoding as R_encoding
import Encoding.I_encoding as I_encoding
import Encoding.S_encoding as S_encoding
import Encoding.B_encoding as B_encoding
import Encoding.J_encoding as J_encoding
import sys
import error as error1
import error2 as error2
import error4 as error3
import testerror as testerror

input_file = "input1.txt"
output_file = "output1.txt"

if len(sys.argv) >= 3:
    input_file = sys.argv[1]
    output_file = sys.argv[2]

from registers import Register, register_address

# Converts a number to its binary representation of a specified length.
# Handles both positive and negative numbers using two's complement.
def binary_to_specified_len(num, length):
    if num >= 0:
        bin_string = bin(num)[2:]  # Convert to binary and remove '0b'
        bin_string = bin_string.zfill(length)  # Pad with leading zeros
    else:
        bin_string = bin((abs(num) ^ ((2**length) - 1)) + 1)[2:]  # Two's complement
        bin_string = bin_string.zfill(length)  # Pad with leading ones
    return bin_string

# Initialize registers with default value 0
registers = {key: Register(register_address[key]) for key in register_address}

# Read assembly instructions
out = []
with open(input_file, "r") as assembly:
    instructions = [x for x in assembly.readlines() if x.strip()]

# Labels dictionary to store label addresses
labels = {}
no_of_lines = len(instructions)
lines = no_of_lines * 4  # Address increments by 4 since each instruction is 32-bit

# Process labels
for line in range(no_of_lines):
    instruction = instructions[line].strip().split(" ")
    if instruction[0].endswith(":"):
        labels[instruction[0][:-1]] = line * 4
        instructions[line] = " ".join(instruction[1:]) + "\n"
    else:
        no_of_lines -= 1

# Ensure last instruction is a halt command
if instructions[-1].strip() != "beq zero,zero,0":
    print("Virtual Halt Missing")
    exit()

# Check for errors in instructions
error_happened = False
for i, instr in enumerate(instructions):
    valid, error_type = testerror.mainchecker(instr.strip())
    if not valid:
        print(f"{error_type} error in line {i + 1}")
        print(instr.strip())
        error_happened = True
        break
if error_happened:
    exit()

pc = 0  # Program counter

# Process instructions
while pc < lines:
    instruction = instructions[pc // 4].strip()
    if not error2.main2(instruction):
        print("Error: Immediate out of range at line", (pc // 4) + 1)
        exit()
    
    inp = instruction.split(" ")
    operation = inp[0]

    # R-Type Instructions
    if operation in R_encoding.R_operations:
        rd, rs1, rs2 = inp[1].split(",")
        final = (
            R_encoding.R_funct7[operation] + register_address[rs2] + 
            register_address[rs1] + R_encoding.R_funct3[operation] + 
            register_address[rd] + R_encoding.R_oppcode
        )
        out.append(final)
    
    # I-Type Instructions
    elif operation in I_encoding.I_operations:
        rd, rs, imm = inp[1].split(",") if operation != "lw" else inp[1].split(",", 1)
        if operation == "lw":
            imm, rs = imm.split("(")
            rs = rs.rstrip(")")
        final = (
            binary_to_specified_len(int(imm), 12) + register_address[rs] + 
            I_encoding.I_funct3[operation] + register_address[rd] + 
            I_encoding.I_oppcode[operation]
        )
        out.append(final)
    
    # J-Type Instructions
    elif operation in J_encoding.J_operations:
        rd, imm = inp[1].split(",")
        imm = binary_to_specified_len(labels.get(imm, int(imm)) - pc, 21)
        final = (
            imm[-21] + imm[-11:-1] + imm[-12] + imm[-20:-12] + 
            register_address[rd] + J_encoding.J_oppcode
        )
        out.append(final)
    
    # B-Type (Branch) Instructions
    elif operation in B_encoding.B_operations:
        rs1, rs2, imm = inp[1].split(",")
        if imm not in labels and not imm.lstrip("-").isdigit():
            print("Error on line:", (pc // 4) + 1, "-> No such label")
            break
        offset = labels.get(imm, int(imm) * 4)
        imm_13bit = binary_to_specified_len(offset, 13)
        final = (
            imm_13bit[-13] + imm_13bit[-11] + imm_13bit[-10:-5] + 
            register_address[rs2] + register_address[rs1] + 
            B_encoding.B_funct3[operation] + imm_13bit[-5:-1] + 
            imm_13bit[-12] + B_encoding.B_oppcode
        )
        out.append(final)
    
    # S-Type Instructions
    elif operation in S_encoding.S_operations:
        rs2, k = inp[1].split(",")
        imm, rs1 = k.rstrip(")").split("(")
        final = (
            binary_to_specified_len(int(imm), 12)[-12:-5] + register_address[rs2] + 
            register_address[rs1] + S_encoding.S_funct3[operation] + 
            binary_to_specified_len(int(imm), 12)[-5:] + S_encoding.S_oppcode
        )
        out.append(final)
    
    pc += 4  # Increment program counter

# Write output to file
with open(output_file, "w") as output:
    output.write("\n".join(out))
