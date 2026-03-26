
'''
Encode instruction according to instruction type: R, I, S/B, U/J
'''
instructionList = [
  {"R-type": "add"},
  {"I-Type": "addi"},
  {"S-Type": "sw"},
  {"B-Type":"beq"},
  {"U-Type": "lui"},
  {"J-Type": "jal"}
]

def encode(Instruction):

  ...

def getType():
  ...

def encode_R_type(op, rd, rs1, rs2, func3, func7):
  ...

def encode_I_type(op, rd, rs1, func3, imm):
  ...

def encode_S_type(op, rs1, rs2, func3, imm):
  ... 

def encode_B_type(op, rs1, rs2, func3, imm):
  ... 

def encode_U_type(op, rd, imm):
  ... 

def encode_J_type(op, rd, imm):
  ... 
