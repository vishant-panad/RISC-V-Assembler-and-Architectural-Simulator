import sys


input_file = "inp.txt"
output_file = "out.txt"

if len(sys.argv) >= 3:
    input_file = sys.argv[1]
    output_file = sys.argv[2]


registers_values = {f"x{i}": 0 for i in range(32)}

registers_values["x2"] = 380# Example register values for testing
memory = {i:"0" for i in range(65536, 65661, 4)}

def read_instructions_from_file(file_path):
    """Reads binary instructions from a text file."""
    try:
        with open(file_path, 'r') as file:
            instruction_memory = [line.strip() for line in file.readlines()]
        return instruction_memory
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
        return []

def write_trace_to_file(file_path, trace_data):
    """Writes the trace data (registers_values and memory content) to a text file."""
    try:
        with open(file_path, 'w') as file:
            for line in trace_data:
                file.write(line + '\n')
    except Exception as e:
        print(f"Error writing to file {file_path}: {e}") # Set Up Memory for Instructions




# Implement the Program Counter (PC)
PC = 0  # Start at 0

def fetch_instruction(instruction_memory):
    global PC
    try:
        instruction = instruction_memory[PC//4]
        if instruction == "00000000000000000000000001100011":
            PC -= 4
        PC += 4  # Move to next instruction (RISC-V uses 32-bit, so +4 in real hardware)
        return instruction
    except:
        return None
      # No more instructions

def twos_complement(x):
    """
    Returns the 2's complement of a binary string x as an integer.
    
    :param x: Binary string (e.g., '0110', '1011')
    :return: Two's complement of x as an integer
    """
    if x[0] == 1:
        num = int(x, 2)
        num = (1 << len(x)) - num
    else:
        num = int(x,2)
    return num # Return as an integer

def binary_to_decimal(binary_str):
    try:
        return int(binary_str, 2)
    except ValueError:
        return "Invalid binary number"

def opcode_func(binary_str):
    return binary_str[25:]

def identify_instruction_type(binary_str):
    opcode = opcode_func(binary_str)

    I_opcode = {
        "lw": "0000011",
        "addi": "0010011",
        "sltiu": "0010011",
        "jalr": "1100111"
    }

    B_opcode = "1100011"
    J_opcode = "1101111"
    R_opcode = "0110011"
    S_opcode = "0100011"

    if opcode in I_opcode.values():
        return "I-type"
    elif opcode == B_opcode:
        return "B-type"
    elif opcode == J_opcode:
        return "J-type"
    elif opcode == R_opcode:
        return "R-type"
    elif opcode == S_opcode:
        return "S-type"
    else:
        return "Unknown instruction type"


def R_type_decoding(binary_str):
    global registers_values
    lst = [binary_str[:7], binary_str[7:12], binary_str[12:17], binary_str[17:20], binary_str[20:25], binary_str[25:]]
    
    funct7 = lst[0]
    rs2 = "x" + str(int(lst[1], 2))  # Convert binary to integer
    rs1 = "x" + str(int(lst[2], 2))  # Convert binary to integer
    funct3 = lst[3]
    rd = "x" + str(int(lst[4], 2))   # Convert binary to integer
    opcode = lst[5]

    print(f"Decoded values:\n  funct7: {funct7}\n  rs2: {rs2}\n  rs1: {rs1}\n  funct3: {funct3}\n  rd: {rd}\n  opcode: {opcode}")

    if rd not in registers_values:
        registers_values[rd] = 0  # Initialize if not present

    if funct7 == '0100000' and funct3 == '000':  # SUB instruction
        instruction_name = 'sub'
        result = registers_values.get(rs1, 0) - registers_values.get(rs2, 0)

    elif funct7 == '0000000' and funct3 == '000':  # ADD instruction
        instruction_name = 'add'
        result = registers_values.get(rs1, 0) + registers_values.get(rs2, 0)

    elif funct7 == '0000001' and funct3 == '000':  # MUL (Multiplication)
        instruction_name = 'mul'
        result = registers_values.get(rs1, 0) * registers_values.get(rs2, 0)

    elif funct7 == '0000001' and funct3 == '001':  # MULH (Multiply High)
        instruction_name = 'mulh'
        product = registers_values.get(rs1, 0) * registers_values.get(rs2, 0)  # 64-bit multiplication
        result = (product >> 32) & 0xFFFFFFFF  # Extract upper 32 bits

    elif funct7 == '0000000' and funct3 == '001':  # SLL (Shift Left Logical)
        instruction_name = 'sll'
        result = registers_values.get(rs1, 0) << (registers_values.get(rs2, 0) & 0x1F)

    elif funct7 == '0000000' and funct3 == '010':  # SLT (Set Less Than)
        instruction_name = 'slt'
        result = 1 if registers_values.get(rs1, 0) < registers_values.get(rs2, 0) else 0

    elif funct7 == '0000000' and funct3 == '011':  # SLTU (Set Less Than Unsigned)
        instruction_name = 'sltu'
        result = 1 if (registers_values.get(rs1, 0) & 0xFFFFFFFF) < (registers_values.get(rs2, 0) & 0xFFFFFFFF) else 0

    elif funct7 == '0000000' and funct3 == '100':  # XOR
        instruction_name = 'xor'
        result = registers_values.get(rs1, 0) ^ registers_values.get(rs2, 0)

    elif funct7 == '0000000' and funct3 == '101':  # SRL (Shift Right Logical)
        instruction_name = 'srl'
        result = registers_values.get(rs1, 0) >> (registers_values.get(rs2, 0) & 0x1F)

    elif funct7 == '0000000' and funct3 == '110':  # OR
        instruction_name = 'or'
        result = registers_values.get(rs1, 0) | registers_values.get(rs2, 0)

    elif funct7 == '0000000' and funct3 == '111':  # AND
        instruction_name = 'and'
        result = registers_values.get(rs1, 0) & registers_values.get(rs2, 0)

    else:
        return 'Invalid instruction'

    # Convert result to a 32-bit binary string
    result_bin = format(result & 0xFFFFFFFF, '032b')
    
    # Convert to signed integer using twos_complement
    result_signed = twos_complement(result_bin)

    # Store the final signed result
    registers_values[rd] = result_signed

    print(f"{instruction_name} {rd}, {rs1}, {rs2} -> {rd} = {result_signed}")

    return f"{instruction_name} {rd}, {rs1}, {rs2} (Result: {rd} = {result_signed})"



def I_type_decoding(binary_str):
    global memory
    global registers_values
    global PC  # Add this to modify PC
    lst = [binary_str[:12], binary_str[12:17], binary_str[17:20], binary_str[20:25], binary_str[25:]]
    rs1 = "x" + str(twos_complement(lst[1]))
    funct3 = lst[2]
    rd = "x" + str(twos_complement(lst[3]))
    opcode = lst[4]

    # Checking if imm is negative (sign-extension for 12-bit immediate)
    imm_val = twos_complement(lst[0])

    print(f"Decoded values:\n  rs1: {rs1} \n  funct3: {funct3}\n  rd: {rd}  \n  opcode: {opcode} \n imm_value: {imm_val}")

    # ADDI: rd = rs1 + imm
    if funct3 == '000' and opcode == '0010011':
        instruction_name = 'addi'
        registers_values[rd] = registers_values[rs1] + imm_val
        return f'{instruction_name} {rd}, {rs1}, {imm_val}  # {rd} = {registers_values[rd]}'

    # **SUBI: rd = rs1 - imm**
    elif funct3 == '000' and opcode == '0010011':  
        instruction_name = 'subi'
        registers_values[rd] = registers_values[rs1] - imm_val
        return f'{instruction_name} {rd}, {rs1}, {imm_val}  # {rd} = {registers_values[rd]}'

    # LW: Load word (rd = Mem[rs1 + imm])
    elif funct3 == '010' and opcode == '0000011':
        instruction_name = 'lw'
        address = registers_values[rs1] + imm_val
        registers_values[rd] = memory.get(address, 0)  # Load from memory, default 0 if not found
        return f'{instruction_name} {rd}, {imm_val}({rs1})  # {rd} = Mem[{address}] = {registers_values[rd]}'

    # SLTIU: Set Less Than Immediate Unsigned (rd = 1 if rs1 < imm else 0)
    elif funct3 == '011' and opcode == '0010011':
        instruction_name = 'sltiu'
        registers_values[rd] = 1 if registers_values[rs1] < imm_val else 0
        return f'{instruction_name} {rd}, {rs1}, {imm_val}  # {rd} = {registers_values[rd]}'
    
    elif funct3 == '001' and opcode == '0010011':
        instruction_name = 'slli'
        shamt = int(lst[0][-5:], 2)  # Extract last 5 bits as shift amount
        registers_values[rd] = registers_values[rs1] << shamt
        return f'{instruction_name} {rd}, {rs1}, {shamt}  # {rd} = {registers_values[rd]}'

    # JALR: Jump and Link Register (rd = PC + 4, PC = rs1 + imm)
    elif funct3 == '000' and opcode == '1100111':
        instruction_name = 'jalr'

        # Store return address (PC + 4) in rd
        registers_values[rd] = PC + 4

        # Update PC
        new_pc = (registers_values[rs1] + imm_val) & ~1  # Ensure LSB is 0
        PC = new_pc  # Now PC is properly updated

        return f'{instruction_name} {rd}, {rs1}, {imm_val}  # {rd} = {registers_values[rd]}, PC = {PC}'

    return 'invalid instruction'




def S_type_decoding(binary_str):
    global memory, registers_values
    
    # Extract fields from binary string
    imm_4_0 = binary_str[:7]  # First part of immediate
    rs2 = "x" + str(int(binary_str[7:12], 2))
    rs1 = "x" + str(int(binary_str[12:17], 2))
    funct3 = binary_str[17:20]
    imm_11_5 = binary_str[20:25]  # Second part of immediate
    opcode = binary_str[25:]
    
    # Combine immediate fields and compute signed value
    imm = imm_11_5 + imm_4_0  # Concatenate immediate parts
    imm_val = twos_complement(imm)  # Convert to integer

    print(f"Decoded values:\n  rs2: {rs2}\n  rs1: {rs1}\n  funct3: {funct3}\n  opcode: {opcode}\n  imm: {imm_val}")

    # Store word (SW) operation: Mem[rs1 + imm] = rs2
    if funct3 == '010' and opcode == '0100011':  
        instruction_name = 'sw'
        mem_address = registers_values[rs1] + imm_val  # Compute memory address
        memory[mem_address] = registers_values[rs2]  # Store value at memory address
        return f'{instruction_name} {rs2}, {imm_val}({rs1})  # Mem[{mem_address}] = {registers_values[rs2]}'

    return 'Invalid instruction'

def B_type_decoding(binary_str):
    global registers_values, PC  # Use PC instead of program_counter
    
    # Extract fields from binary string
    imm_12 = binary_str[0]   # 12th bit
    imm_10_5 = binary_str[1:7]   # Bits 10-5
    rs2 = "x" + str(int(binary_str[7:12], 2))
    rs1 = "x" + str(int(binary_str[12:17], 2))
    funct3 = binary_str[17:20]
    imm_4_1 = binary_str[20:24]  # Bits 4-1
    imm_11 = binary_str[24]  # 11th bit
    opcode = binary_str[25:]

    # Construct the immediate value
    imm = imm_12 + imm_11 + imm_10_5 + imm_4_1 + '0'  # Concatenating bits and adding 0 at LSB
    imm_val = twos_complement(imm)  # Convert to signed integer

    print(f"Decoded values:\n  rs1: {rs1}\n  rs2: {rs2}\n  funct3: {funct3}\n  opcode: {opcode}\n  imm: {imm_val}")

    # Branch instructions: conditional jumps
    branch_taken = False
    if funct3 == '000' and opcode == '1100011':  # BEQ (Branch if Equal)
        instruction_name = 'beq'

        # If BEQ x0, x0, 0 is detected, do NOT increment PC
        if rs1 == 'x0' and rs2 == 'x0' and imm_val == 0:
            print("Halting execution: BEQ x0, x0, 0 detected.")
            return "HALT"
        
        branch_taken = registers_values[rs1] == registers_values[rs2]
        

    elif funct3 == '001' and opcode == '1100011':  # BNE (Branch if Not Equal)
        instruction_name = 'bne'
        branch_taken = registers_values[rs1] != registers_values[rs2]

    elif funct3 == '100' and opcode == '1100011':  # BLT (Branch if Less Than)
        instruction_name = 'blt'
        branch_taken = registers_values[rs1] < registers_values[rs2]

    elif funct3 == '110' and opcode == '1100011':  # **BLTU (Branch if Less Than Unsigned)**
        instruction_name = 'bltu'
        rs1_val = registers_values[rs1] & 0xFFFFFFFF  # Convert to unsigned 32-bit
        rs2_val = registers_values[rs2] & 0xFFFFFFFF  # Convert to unsigned 32-bit
        branch_taken = rs1_val < rs2_val  # Unsigned comparison

    elif funct3 == '101' and opcode == '1100011':  # BGE (Branch if Greater or Equal)
        instruction_name = 'bge'
        branch_taken = registers_values[rs1] >= registers_values[rs2]
    else:
        return 'Invalid instruction'

    # Update PC if branch is taken
    if branch_taken:
        PC += imm_val
        return f'{instruction_name} {rs1}, {rs2}, {imm_val}  # Branch taken to PC={PC}'
    else:
        return f'{instruction_name} {rs1}, {rs2}, {imm_val}  # Branch not taken'



def J_type_decoding(binary_str):
    global registers_values, PC
    
    # Extract fields from binary string
    imm_20 = binary_str[0]  # 20th bit (sign bit)
    imm_10_1 = binary_str[1:11]  # Bits 10-1
    imm_11 = binary_str[11]  # 11th bit
    imm_19_12 = binary_str[12:20]  # Bits 19-12
    rd = int(binary_str[20:25], 2)  # Destination register (as an integer)
    opcode = binary_str[25:]  # Opcode (should be '1101111' for JAL)

    # Construct the immediate value correctly (sign extend it)
    imm = imm_20 + imm_19_12 + imm_11 + imm_10_1 + '0'  # Concatenate and add LSB 0
    imm_val = twos_complement(imm)  # Convert to signed integer with correct bit-width

    print(f"Decoded values:\n  rd: x{rd}\n  opcode: {opcode}\n  imm: {imm_val}")

    if opcode == '1101111':  # JAL (Jump and Link)
        instruction_name = 'jal'
        registers_values[f'x{rd}'] = PC  # Store return address (next instruction)
        PC = PC + imm_val - 4  # Fix PC update since fetch already added 4
        return f'{instruction_name} x{rd}, {imm_val}  # Jump to PC={PC} with return address stored in x{rd}'
    
    return 'Invalid instruction'





def main(): # output in binary
    memory_state = ""
    input_file = "inp.txt"
    output_file = "out.txt"
    
    global instruction_memory
    instruction_memory = read_instructions_from_file(input_file)
    
    trace_output = []
    
    while True:
        binary_str = fetch_instruction(instruction_memory)
        if binary_str is None:
            break  # Stop when no more instructions

        instr_type = identify_instruction_type(binary_str)
        
        if instr_type == "R-type":
            result = R_type_decoding(binary_str)
        elif instr_type == "I-type":
            result = I_type_decoding(binary_str)
        elif instr_type == "J-type":
            result = J_type_decoding(binary_str)
        elif instr_type == "S-type":
            result = S_type_decoding(binary_str)
        elif instr_type == "B-type":
            result = B_type_decoding(binary_str)
        else:
            result = f"Error: Unknown Instruction Type at line {PC}: {binary_str}"
            print(result)
            break  # Stop execution on first error

        print(f"After execution: PC = {PC}\n")


        # Convert all register values to decimal format in a single line
        registers_state = ' '.join(f"0b{registers_values[f'x{i}'] & 0xFFFFFFFF:032b}" for i in range(32))
        
        # Format PC in decimal instead of binary
        pc_state = format(PC & 0xFFFFFFFF, '032b')
        
        memory_state = ''.join(f"0x{addr:08X}:{memory[addr]}\n" for addr in sorted(memory.keys()))  # Memory in decimal format
        
        trace_output.append(f"0b{pc_state} {registers_state}")  # Store PC as decimal

        if binary_str == "00000000000000000000000001100011":
            break 

    # Append memory state at the end
    trace_output.append(f"{memory_state}\n")
    write_trace_to_file(output_file, trace_output)


# def main(): # output in decimal
#     input_file = "inp.txt"
#     output_file = "out.txt"
    
#     global instruction_memory
#     instruction_memory = read_instructions_from_file(input_file)
    
#     trace_output = []
    
#     while True:
#         binary_str = fetch_instruction(instruction_memory)
#         if binary_str is None:
#             break  # Stop when no more instructions

#         instr_type = identify_instruction_type(binary_str)
        
#         if instr_type == "R-type":
#             result = R_type_decoding(binary_str)
#         elif instr_type == "I-type":
#             result = I_type_decoding(binary_str)
#         elif instr_type == "J-type":
#             result = J_type_decoding(binary_str)
#         elif instr_type == "S-type":
#             result = S_type_decoding(binary_str)
#         elif instr_type == "B-type":
#             result = B_type_decoding(binary_str)
#         else:
#             result = f"Error: Unknown Instruction Type at line {PC}: {binary_str}"
#             print(result)
#             break  # Stop execution on first error

#         print(f"After execution: PC = {PC}\n")


#         # Convert all register values to decimal format in a single line
#         registers_state = ' '.join(str(registers_values[f"x{i}"]) for i in range(32))
        
#         # Format PC in decimal instead of binary
#         pc_state = str(PC)
        
#         memory_state = ' '.join(f"\n0x{addr:08X}:{memory[addr]}" for addr in sorted(memory.keys()))  # Memory in decimal format
        
#         trace_output.append(f"{pc_state} {registers_state}")  # Store PC as decimal

#         if binary_str == "00000000000000000000000001100011":
#             break 

#     # Append memory state at the end
#     trace_output.append(f"{memory_state}\n")
#     write_trace_to_file(output_file, trace_output)





main()
