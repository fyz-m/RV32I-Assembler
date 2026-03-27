
'''
Encode instruction according to instruction type: R, I, S/B, U/J
'''

R_type = ("add")
I_type = ("addi")
S_type = ("sw")
B_type = ("beq")
U_type = ("lui")
J_type = ("jal")

Instructions = {
  "R-type": R_type, 
  "I-type": I_type,
  "S-type": S_type,
  "B-type": B_type,
  "U-type": U_type,
  "J-type": J_type     
}

def encode(instruction):

  ...

def getType(instruction):
  '''Returns instructon type based on the mnemonic e.g ADDI'''
  #example input instruction: "add s3, s1, s2"
  
  mnemonic, instruction = instruction.split(" ", 1)
  for type in  Instructions:
    if mnemonic in Instructions[type]:
      return type
  


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
