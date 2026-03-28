
'''
Encode instruction according to instruction type: R, I, S/B, U/J
Registers must already be converted to their number (defined by RISC-V ISA)
input instruction example format:
  "add 18, 19, 20" 

'''


def encode(instruction):

  match instruction.Type:
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




def encode_R_type(opcode, rd, rs1, rs2, func3, func7):
  ...

def encode_I_type(opcode, rd, rs1, func3, imm):
  ...

def encode_S_type(opcode, rs1, rs2, func3, imm):
  ... 

def encode_B_type(opcode, rs1, rs2, func3, imm):
  ... 

def encode_U_type(opcode, rd, imm):
  ... 

def encode_J_type(opcode, rd, imm):
  ... 
