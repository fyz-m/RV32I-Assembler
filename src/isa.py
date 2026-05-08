# Contains the RISC-V registers (register file), supported instructions and their control bits (opcode, funct3, funct7)
# Used in the Instruction class for:
# - Register and mnemonic validation 
# - Looking up field values



INSTRUCTION_SET = {

  "R-type": {

    "add": { "op": 51, "funct3": 0, "funct7": 0},  
    "sub": { "op": 51, "funct3": 0, "funct7": 32},
    "sll": { "op": 51, "funct3": 1, "funct7": 0},
    "slt": { "op": 51, "funct3": 2, "funct7": 0},
    "sltu": { "op": 51, "funct3": 3, "funct7": 0},
    "xor": { "op": 51, "funct3": 4, "funct7": 0},
    "srl": { "op": 51, "funct3": 5, "funct7": 0},
    "sra": { "op": 51, "funct3": 5, "funct7": 32},
    "or": { "op": 51, "funct3": 6, "funct7": 0},
    "and": { "op": 51, "funct3": 7, "funct7": 0},

    # RV32M Multiply extension 
    "mul": { "op": 51, "funct3": 0, "funct7": 1},
    "mulh": { "op": 51, "funct3": 1, "funct7": 1},
    "mulsu": { "op": 51, "funct3": 2, "funct7": 1},
    "mulu": { "op": 51, "funct3": 3, "funct7": 1},
    "div": { "op": 51, "funct3": 4, "funct7": 1},
    "divu": { "op": 51, "funct3": 5, "funct7": 1},
    "rem": { "op": 51, "funct3": 6, "funct7": 1},
    "remu": { "op": 51, "funct3": 7, "funct7": 1}

  },

  "I-type": {

    "lb": { "op": 3, "funct3": 0, "funct7": None },
    "lh": { "op": 3, "funct3": 1, "funct7": None },
    "lw": { "op": 3, "funct3": 2, "funct7": None },
    "lbu": { "op": 3, "funct3": 4, "funct7": None },
    "lhu": { "op": 3, "funct3": 5, "funct7": None },
    "addi": { "op": 19, "funct3": 0, "funct7": None},
    "slli": { "op": 19, "funct3": 1, "funct7": 0 },
    "slti": { "op": 19, "funct3": 2, "funct7": None },
    "sltiu": { "op": 19, "funct3": 3, "funct7": None },
    "xori": { "op": 19, "funct3": 4, "funct7": None },
    "srli": { "op": 19, "funct3": 5, "funct7": 0 },
    "srai": { "op": 19, "funct3": 5, "funct7": 32 },
    "ori": { "op": 19, "funct3": 6, "funct7": None},
    "andi": { "op": 19, "funct3": 7, "funct7": None},
    "jalr": { "op": 103, "funct3": 0, "funct7": None}

  },

  "S-type": {

    "sb": { "op": 35, "funct3": 0, "funct7": None},
    "sh": { "op": 35, "funct3": 1, "funct7": None},
    "sw":{ "op": 35, "funct3": 2, "funct7": None}

  },

  "B-type": {

    "beq":{ "op": 99, "funct3": 0, "funct7": None},
    "bne": { "op": 99, "funct3": 1, "funct7": None},
    "blt": { "op": 99, "funct3": 4, "funct7": None},
    "bge": { "op": 99, "funct3": 5, "funct7": None},
    "bltu": { "op": 99, "funct3": 6, "funct7": None},
    "bgeu": { "op": 99, "funct3": 7, "funct7": None}

  },

  "U-type": {

   "auipc": { "op": 23, "funct3": None, "funct7": None},
   "lui": { "op": 55, "funct3": None, "funct7": None},

  },

  "J-type": {

    "jal":{ "op": 111, "funct3": None , "funct7": None},

  }
}


REGISTER_FILE = {
  
   "zero":0, "x0":0,
   "ra":1, "x1":1,
   "sp":2, "x2":2,
   "gp":3, "x3":3,
   "tp":4, "x4":4,
   "t0":5, "x5":5,
   "t1":6, "x6":6,
   "t2":7, "x7":7,
   "s0":8, "x8":8, "fp":8,
   "s1":9, "x9":9,
   "a0":10, "x10":10,
   "a1":11, "x11":11,
   "a2":12, "x12":12,
   "a3":13, "x13":13,
   "a4":14, "x14":14,
   "a5":15, "x15":15,
   "a6":16, "x16":16,
   "a7":17, "x17":17,
   "s2":18, "x18":18,
   "s3":19, "x19":19,
   "s4":20, "x20":20,
   "s5":21, "x21":21,
   "s6":22, "x22":22,
   "s7":23, "x23":23,
   "s8":24, "x24":24,
   "s9":25, "x25":25,
   "s10":26, "x26":26,
   "s11":27, "x27":27,
   "t3":28, "x28":28,
   "t4":29, "x29":29,
   "t5":30, "x30":30,
   "t6":31, "x31":31,

}