# RISC-V Assembler

A basic assembler for RISC-V assembly. Translates RISC-V assembly into machine code. 

The focus of this project was to learn core concepts in computer architecture, object-oriented programming, systems-programming and Python in general. 

## Features

- **Instruction set:** All RV32IM instructions
- **Two-pass architecture:** forward and backward label references supported
- **Syntax:**
    - ABI register names (`zero`, `ra`, `s0-s11` etc.)
    - Numbered register names (`x0`, `x12` etc.)
    - Immediates can be in decimal, hexadecimal (`0x`) or binary (`0b`)
    - Comment support (`#`)
- **Error handling:** Precise error messages with line number, context and issue (e.g Invalid immediate) for developer-friendly debugging  
- **Binary output:** Can output assembled instructions in binary to run on a simulator
## Usage

```bash
python main.py -f program.s
```
Output is written to `program_assembled.txt` as one hex word per instruction. Adding the `-b` flag creates a binary file `program_assembled.bin` instead of a text file. If you want to simulate the assembled binaries, check out my [RISC-V simulator](https://github.com/fyz-m/RV-ISS).  

### Examples
Input:
```asm
# Countdown loop
    addi t0, zero, 10      # t0 = 10
loop:
    addi t0, t0, -1        # t0--
    bne  t0, zero, loop    # repeat until t0 == 0
```
Output:
```
00a00293
fff28293
fe029ee3
```

Erroneous input:
```asm
    addi t0, t0, s1      # I-type instruction's third operand should be an immediate  
    add s1, s2, reg      # 'reg' is not a RISC-V register
```
Output:
```
  Failed with 2 error(s):

      line 1: Invalid immediate 's1'
       > addi t0, t0, s1
       - Immediates must be either:
        - Decimal
        - Hexadecimal prefixed with '0x'
        - Binary prefixed with '0b'

      line 2: Invalid register 'reg'
       > add s1, s2, reg
```
## Project Structure
```
rv32i-assembler/
├── src/
│   ├── isa.py          # Instruction set — Lookup table for mnemonic, control bits(opcode/function fields), ABI registers
│   ├── Instruction.py  # Instruction class — tokenizer, operand extraction and validation
│   ├── encode.py       # Encode operands into 32-bit machine code
│   └── parse.py        # Two-pass assembler pipeline
├── tests/
│   ├── test_Instruction.py   # Unit tests: parsing, validation, operand extraction
│   ├── test_encode.py        # Unit tests: Encoding for all instruction formats
│   └── test_parse.py         # Integration tests: full programs through both passes
└── main.py                   # CLI entry point
```
## Architecture
The assembler is implemented with a two-pass architecture:
### Pass 1  
Scan every line, remove comments, add byte address to each instruction and create symbol table to resolve forward label references. This is required because if an instruction refers to a label that appears late on in the program, there would be no way calculate the branch offset (number of bytes from the instruction to the label) unless the entire file is scanned first.  
### Pass 2
Encodes and validates each instruction and calculates branch/jump offsets by looking up the target address in the symbol table for a given label. 

## Testing
This project was focused on test-driven development, ensuring each part was free of fatal bugs before being implemented in the assembler pipeline. To run the test-suite, execute:
```bash
pytest tests/
```

## Future additions
- **Simulator Integration:** Connect to a RISC-V simulator to execute the assembled instructions
- **Extend ISA:**
    - `RV32M` (Multiply/Divide) - Done ✅
    - `RV32F` (Floating point)

## What I learnt
This was my first python project, here the things I learned while making this assembler:
- How RISC-V encodes each instruction type into 32-bit machine code
- Why a two-pass architecture is necessary for forward reference label resolution
- Bit manipulation in Python: shifting, masking and sign-extending without fixed-width integers
- Testing code with Pytest and using a debugger: the debugger was extremely useful in debugging the encoding functions and seeing exactly which line of code was the problem
- Structuring a multi-module project in Python
- Validating input and object-oriented programming
- Error-handling and creating useful error messages
