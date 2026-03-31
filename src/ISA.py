#Look up table of the RISC-V register file used for register validation and conversion to its corresponding number. 
RegisterTable = {
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
   None: None
}

Instructions = {
  "R-type": {
    "add": {"controlBits": (51, 0, 0)},  # Controlbits = opcode, func3, func7 
    "sub": {"controlBits": (51, 0, 32)},
    "sll": {"controlBits": (51, 1, 0)},
    "slt": {"controlBits": (51, 2, 0)},
    "sltu": {"controlBits": (51, 3, 0)},
    "xor": {"controlBits": (51, 4, 0)},
    "srl": {"controlBits": (51, 5, 0)},
    "sra": {"controlBits": (51, 5, 32)}
  },

  "I-type": {
    "addi": {"controlBits": (19, 0, None)},
  },

  "S-type": {
    "sw":{"controlBits": (35, 2, None) },
  },

  "B-type": {
    "beq":{"controlBits": (99, 0, None) },
  },

  "U-type": {
   "lui": {"controlBits": (55, None, None) },
  },

  "J-type": {
    "jal":{"controlBits": (111, None, None) },
  }
}