from Encoding import R_encoding, I_encoding, S_encoding, B_encoding, J_encoding

# Function to check if an immediate value is valid for a given operation
def is_valid_immediate(value, operation):
    # Define the valid ranges for each type of instruction
    valid_ranges = {
        **{op: (-2048, 2047) for op in I_encoding.I_operations | S_encoding.S_operations},
        **{op: (-4096, 4095) for op in B_encoding.B_operations},
        **{op: (-1048576, 1048575) for op in J_encoding.J_operations}
    }
    
    # Retrieve the valid range for the given operation and check if the value is within range
    if operation in valid_ranges:
        min_val, max_val = valid_ranges[operation]
        return min_val <= value <= max_val
    return False

# Function to validate if an instruction contains a valid immediate value
def validate_instruction(line):
    # Split the instruction into parts
    parts = line.split()
    if not parts:
        return False  # Return False if the instruction is empty
    
    operation = parts[0]  # Extract the operation
    operands = parts[-1].split(',')  # Extract operands by splitting at commas
    
    # Extract the immediate value based on the type of instruction
    if operation in I_encoding.I_operations:
        imm = operands[-1].split('(')[0] if operation == "lw" else operands[-1]
    elif operation in S_encoding.S_operations:
        imm = operands[-1].split('(')[0]
    elif operation in B_encoding.B_operations | J_encoding.J_operations:
        imm = operands[-1] if operands[-1].isnumeric() else None
    else:
        return False  # Return False if operation is not recognized
    
    # Check if the extracted immediate value is valid
    return is_valid_immediate(int(imm), operation) if imm and imm.lstrip('-').isdigit() else False

