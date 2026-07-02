from Encoding import R_encoding, I_encoding, S_encoding, B_encoding, J_encoding
from registers import register_address

# function to check if an instruction has the correct number of operands
def is_valid_instruction(operation, operands):
    """
    verifies if the instruction follows the correct format based on its type.
    """
    if operation in R_encoding.R_operations or operation in I_encoding.I_operations or operation in B_encoding.B_operations:
        # r, i, and b-type instructions usually need three operands, except 'lw', which needs only two
        return len(operands) == 2 if operation == "lw" else len(operands) == 3
    
    if operation in S_encoding.S_operations or operation in J_encoding.J_operations:
        # s and j-type instructions should have exactly two operands
        return len(operands) == 2
    
    # return false if the instruction type is unknown
    return False

# function to check if the given registers exist
def are_valid_registers(registers):
    """
    checks if the provided register names are valid by looking them up in the register list.
    """
    for reg in registers:
        if reg not in register_address:
            return f"error: {reg} is not a valid register"
    return None  # all registers are valid

# function to process and validate an instruction
def process_instruction(line):
    """
    takes an instruction as input, extracts operation and operands, 
    checks if the registers are valid, and verifies instruction format.
    """
    components = line.split(" ")  # split the instruction into parts
    operation = components[0]  # first part is the operation (e.g., 'add', 'lw')
    operands = [operand.strip() for operand in components[1:]]  # extract and clean operands
    
    # split the first operand string to extract register names
    registers = operands[0].split(",") if operands else []
    
    # validate register names
    invalid_register_message = are_valid_registers(registers)
    if invalid_register_message:
        print(invalid_register_message)
        return
    
    # validate instruction format
    if not is_valid_instruction(operation, registers):
        print("error: invalid instruction format")
