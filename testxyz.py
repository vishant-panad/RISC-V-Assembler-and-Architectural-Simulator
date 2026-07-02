registers_values = {f"x{i}": 0 for i in range(32)}

registers_values["x2"] = 8# Example register values for testing
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
    rd = "x" + str(int(lst[4], 2))   # Convert binary to integer (FIXED)
    opcode = lst[5]

    print(f"Decoded values:\n  funct7: {funct7}\n  rs2: {rs2}\n  rs1: {rs1}\n  funct3: {funct3}\n  rd: {rd}\n  opcode: {opcode}")

    if rd not in registers_values:
        registers_values[rd] = 0  # Initialize if not present

    if funct7 == '0100000' and funct3 == '000':  # SUB instruction
        instruction_name = 'sub'
        registers_values[rd] = registers_values.get(rs1, 0) - registers_values.get(rs2, 0)
        print(f"{instruction_name} {rd}, {rs1}, {rs2} -> {rd} = {registers_values[rd]}")

    elif funct7 == '0000000' and funct3 == '000':
        instruction_name = 'add'
        registers_values[rd] = registers_values.get(rs1, 0) + registers_values.get(rs2, 0)
    elif funct7 == '0000000' and funct3 == '001':
        instruction_name = 'sll'
        registers_values[rd] = registers_values.get(rs1, 0) << (registers_values.get(rs2, 0) & 0x1F)
    elif funct7 == '0000000' and funct3 == '010':
        instruction_name = 'slt'
        registers_values[rd] = 1 if registers_values.get(rs1, 0) < registers_values.get(rs2, 0) else 0
    elif funct7 == '0000000' and funct3 == '011':
        instruction_name = 'sltu'
        registers_values[rd] = 1 if (registers_values.get(rs1, 0) & 0xFFFFFFFF) < (registers_values.get(rs2, 0) & 0xFFFFFFFF) else 0
    elif funct7 == '0000000' and funct3 == '100':
        instruction_name = 'xor'
        registers_values[rd] = registers_values.get(rs1, 0) ^ registers_values.get(rs2, 0)
    elif funct7 == '0000000' and funct3 == '101':
        instruction_name = 'srl'
        registers_values[rd] = registers_values.get(rs1, 0) >> (registers_values.get(rs2, 0) & 0x1F)
    elif funct7 == '0000000' and funct3 == '110':
        instruction_name = 'or'
        registers_values[rd] = registers_values.get(rs1, 0) | registers_values.get(rs2, 0)
    elif funct7 == '0000000' and funct3 == '111':
        instruction_name = 'and'
        registers_values[rd] = registers_values.get(rs1, 0) & registers_values.get(rs2, 0)
    else:
        return 'Invalid instruction'

    return f"{instruction_name} {rd}, {rs1}, {rs2} (Result: {rd} = {registers_values[rd]})"



def I_type_decoding(binary_str):
    global memory
    global registers_values
    lst = [binary_str[:12], binary_str[12:17], binary_str[17:20], binary_str[20:25], binary_str[25:]]
    rs1 = "x" + str(twos_complement(lst[1]))
    funct3 = lst[2]
    rd = "x" + str(twos_complement(lst[3]))
    opcode = lst[4]

    print(f"Decoded values:\n  rs1: {rs1} \n  funct3: {funct3}\n  rd: {rd}  \n  opcode: {opcode}")

    # Checking if imm is negative (sign-extension for 12-bit immediate)
    imm_val = twos_complement(lst[0])

    # ADDI: rd = rs1 + imm
    if funct3 == '000' and opcode == '0010011':
        instruction_name = 'addi'
        registers_values[rd] = registers_values[rs1] + imm_val
        return f'{instruction_name} x{rd}, x{rs1}, {imm_val}  # x{rd} = {registers_values[rd]}'

    # LW: Load word (rd = Mem[rs1 + imm])
    elif funct3 == '010' and opcode == '0000011':
        instruction_name = 'lw'
        address = registers_values[rs1] + imm_val
        registers_values[rd] = memory.get(address, 0)  # Load from memory, default 0 if not found
        return f'{instruction_name} x{rd}, {imm_val}(x{rs1})  # x{rd} = Mem[{address}] = {registers_values[rd]}'

    # SLTIU: Set Less Than Immediate Unsigned (rd = 1 if rs1 < imm else 0)
    elif funct3 == '011' and opcode == '0010011':
        instruction_name = 'sltiu'
        registers_values[rd] = 1 if registers_values[rs1] < imm_val else 0
        return f'{instruction_name} x{rd}, x{rs1}, {imm_val}  # x{rd} = {registers_values[rd]}'

    # JALR: Jump and Link Register (rd = PC + 4, PC = rs1 + imm)
    elif funct3 == '000' and opcode == '1100111':
        instruction_name = 'jalr'
        registers_values[rd] = 0  # Assume PC+4 is 0 for now
        new_pc = (registers_values[rs1] + imm_val) & ~1  # Ensure LSB is 0
        return f'{instruction_name} x{rd}, x{rs1}, {imm_val}  # x{rd} = 0, PC = {new_pc}'

    return 'invalid instruction'



def S_type_decoding(binary_str):
    global memory
    lst = [binary_str[:7], binary_str[7:12], binary_str[12:17], binary_str[17:20], binary_str[20:25], binary_str[25:]]
    rs2 = "x" + str(int(lst[1]))
    rs1 = "x" + str(int(lst[2]))
    funct3 = lst[3]
    opcode = lst[5]
    
    print(f"Decoded values:\n  rs2: {rs2}\n  rs1: {rs1}\n  funct3: {funct3}\n opcode: {opcode}")

    registers_values = {i: f"x{i}" for i in range(32)}
    
    imm = lst[0] + lst[4]
    imm_val = twos_complement(imm)  

    # checking if imm is negative or positive

    if funct3 == '010' and opcode == '0100011':
        instruction_name = 'sw'
        return f'{instruction_name} {registers_values[rs2]}, {imm_val}({registers_values[rs1]})'

    return 'invalid instruction'

def B_type_decoding(binary_str):
    global registers_value
    lst = [binary_str[:1], binary_str[1:7], binary_str[7:12], binary_str[12:17], binary_str[17:20], binary_str[20:24], binary_str[24:25], binary_str[25:]]
    
    imm_12 = lst[0]
    imm_10_5 = lst[1]
    rs2 = "x" + str(int(lst[2]))
    rs1 = "x" + str(int(lst[3]))
    funct3 = lst[4]
    imm_4_1 = lst[5]
    imm_11 = lst[6]
    opcode = lst[7]


    imm = imm_12 + imm_11 + imm_10_5 + imm_4_1 + '0'  # Combining immediate fields
    imm_val = twos_complement(imm)


    # checking if imm is negative or positive
    if (imm[0] == '1'):
        imm_val = imm_val - (1 << 13)
    
    if funct3 == '000':
        instruction_name = 'beq'
        return f"{instruction_name} {registers_values[rs1]}, {registers_values[rs2]}, {imm_val}"
    
    elif funct3 == '001':
        instruction_name = 'bne'
        return f"{instruction_name} {registers_values[rs1]}, {registers_values[rs2]}, {imm_val}"

    elif funct3 == '100':
        instruction_name = 'blt'
        return f"{instruction_name} {registers_values[rs1]}, {registers_values[rs2]}, {imm_val}"

    elif funct3 == '101':
        instruction_name = 'bge'
        return f"{instruction_name} {registers_values[rs1]}, {registers_values[rs2]}, {imm_val}"

    elif funct3 == '110':
        instruction_name = 'bltu'
        return f"{instruction_name} {registers_values[rs1]}, {registers_values[rs2]}, {imm_val}"
    
    elif funct3 == '111':
        instruction_name = 'bgeu'
        return f"{instruction_name} {registers_values[rs1]}, {registers_values[rs2]}, {imm_val}"
    
    return 'invalid instruction'

def J_type_decoding(binary_str):
    global registers_values
    lst = [binary_str[:1], binary_str[1:11], binary_str[11:12], binary_str[12:20], binary_str[20:25], binary_str[25:]]
    imm_20 = lst[0]
    imm_10_1 = lst[1]
    imm_11 = lst[2]
    imm_19_12 = lst[3]
    rd = "x" + str(int(lst[4], 2))
    opcode = lst[5]


    imm = imm_20 + imm_19_12 + imm_11 + imm_10_1 + '0' # Combining immediate fields
    imm_val = twos_complement(imm_20 + imm_19_12 + imm_11 + imm_10_1 + '0', 2)

    if opcode == '1101111':
        instruction_name = 'jal'
        return f"{instruction_name} {registers_values[rd]}, {imm_val}"
 
    return f"invalid instruction"



def main():
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
        
        '''
        # Store the register values in binary format
        registers_state = ' '.join(format(i, '032b') for i in range(32))  # Example format, replace with actual values
        memory_state = ' '.join(f"{addr:08X}:{memory[addr]}" for addr in sorted(memory.keys()))
        trace_output.append(f"{PC} {registers_state}")
    
    # Simulate memory dump (replace with actual memory content)
    trace_output.append(f"{memory_state}\n")
    write_trace_to_file(output_file, trace_output)        
        
        
        '''

    
    # Convert all register values to 32-bit binary format in a single line
        registers_state = ' '.join(f"0b{format(registers_values[f'x{i}'] & 0xFFFFFFFF, '032b')}" for i in range(32))        
        memory_state = ' '.join(f"0x{addr:08X}:{memory[addr]}\n" for addr in sorted(memory.keys()))
        
        trace_output.append(f"0b{format(PC & 0xFFFFFFFF, '032b')} {registers_state}")  # Store PC as 32-bit binary


    # Append memory state at the end
    trace_output.append(f"{memory_state}\n")
    write_trace_to_file(output_file, trace_output)



main()
