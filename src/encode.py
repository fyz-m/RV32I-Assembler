

def encode(instruction):
  '''
  Takes Instruction object as input (contains field values like opcode and registers)
  Returns string of field values encoded according to its instruction type 
  '''

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




def encode_R_type(instruction):
  ...

def encode_I_type(instruction):
  ...

def encode_S_type(instruction):
  ... 

def encode_B_type(instruction):
  ... 

def encode_U_type(instruction):
  ... 

def encode_J_type(instruction):
  ... 
