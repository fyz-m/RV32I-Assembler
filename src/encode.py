
'''
Encode instruction according to instruction type: R, I, S/B, U/J
Registers must be converted to their number (defined by RISC-V ISA)
input instruction example format:
  "add 18, 19, 20" 

'''
# Controlbits = op, func3, func7 
Instructions = {
  "R-type": {
    "add": {"controlBits": (51, 0, 0)},
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



def encode(instruction):

  Type = getType(instruction)
  fields = getFields(Type, instruction)

  match Type:
    case "R-type":
      encode_R_type(instruction)
    case "I-type":
      encode_I_type(instruction)
    case "S-type":
      encode_S_type(instruction)
    case "B-type":
      encode_B_type(instruction)
    case "U-type":
      encode_U_type(instruction)
    case "B-type":
      encode_B_type(instruction)

def getType(instruction):
  '''
  Returns instructon type based on the mnemonic 
  E.g: input = "add s3, s1, s2"
       output = "R-type"
  '''
  
  h, instruction = instruction.split(" ", 1)
  for type in Instructions:
    if h in Instructions[type]:
        return type
  
def getFields(type, instruction):
  '''
  Returns the field values of each instruction
  '''
  

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
