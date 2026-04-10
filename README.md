# RV32I Assembler

A basic assembler for the RISC-V 32-bit base integer instruction set (RV32I). Translates RV32I assembly into machine code.

## Features

- All 40 RV32I instructions
- Two-pass architecture, forward and backward label references supported
- ABI register names (`zero`, `ra`, `s0-s11` etc.)
- Numbered register names (`x0`, `x12` etc.)
- Immediates can be in decimal, hexadecimal or binary
- Comment support (`#`)
- Error messages with line numbers and context  
- Verified against GNU `riscv64-unknown-elf-as` output

## Usage

```bash
python main.py -f program.s
```
Output is written to `program_assembled.txt` as one hex word per instruction.

### Example
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
