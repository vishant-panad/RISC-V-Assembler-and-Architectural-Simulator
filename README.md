# RISC-V Assembler and Architectural Simulator

A modular Python implementation of a 32-bit RISC-V Assembler and Simulator. This project translates RISC-V assembly code into structural binary machine code and simulates a processing pipeline, tracking instruction execution, register state modifications, and program counter progress.

##  Key Features
- **Multi-Format Assembly Support:** Accurately encodes R, I, S, B, J, and U-type RISC-V instructions into standard 32-bit binary strings.
- **Robust Error Validation Pipeline:**
  - Syntax checking for missing or malformed operands.
  - Hardcoded write-protection guarding the `zero` register (`x0`).
  - Strict boundary validation for instruction immediate fields (e.g., I/S-types constrained to 12-bit signed limits).
- **Program Counter & Memory Simulation:** Models dynamic code execution steps, jumps, and conditional branching logic, outputting detailed system states per execution cycle.

##  File Structure Overview
- `Assembler.py`: The core compiler orchestrating input file parsing, structural formatting, and binary file generation.
- `simulator_1.py`: The execution environment that processes compiled code, stepping through execution addresses and mimicking hardware states.
- `Encoding/`: Contains dedicated mapping rules and formatting modules for different operational types (`R_encoding`, `I_encoding`, etc.).
- `error*.py` & `testerror.py`: A sequence of semantic checks dedicated to trapping invalid boundaries, edge cases, and runtime format issues.

##  How to Run
```bash
python Assembler.py <path_to_input_assembly.txt> <path_to_output_binary.txt>
