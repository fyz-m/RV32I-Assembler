''' 
First parse: 
- Remove blank lines and comments
- Check validity of instructions (Error checking)
  - Valid Operations
  - Valid registers
  - Valid Immediates 
  - Correct format for the instruction type

- Add memory address to each instruction 
- Collect labels for encoding 
- Calculate branch offsets to encode labels for B and J-type instructions 


Second parse:
- Collect operation, operand registers, immediate
- Encode instruction according to RISC-V ISA 
  - Get OpCode, func3 and func7 according to operation
  - Get registers 
  - Convert register names into their corresponding number

'''

