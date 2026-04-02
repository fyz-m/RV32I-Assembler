

def encode(instruction):
  '''
  Takes Instruction object as input (contains field values like opcode and registers)
  Returns string of field values encoded according to its instruction type 
  '''
  
  match instruction.Type:
    case "R-type":
      encode_R_type(fields)
    case "I-type":
      encode_I_type(fields)
    case "S-type":
      encode_S_type(fields)
    case "B-type":
      encode_B_type(fields)
    case "U-type":
      encode_U_type(fields)
    case "B-type":
      encode_B_type(fields)


'''
  Encoding the values into 32-bit machine code is done by:
   - shifting the value to its bit postion, padding least significant bits with 0
   - OR-ing all the values, resulting in concatenation

   e.g:
   bin1 = 0110
   bin2 = 1111

   bin2 << 4 = bin2_0000
   bin1 | bin2 = 
                0000_0110
                |||| ||||   bit-wise OR
                1111_0000
                ---------
                1111_0110
'''

def sign_extend(n, bits):
    # Create a mask e.g. for 8 bits, 0b11111111
    mask = (1 << bits) - 1
    # Bitwise AND 
    return n & mask

def encode_R_type(op, rd, rs1, rs2, funct3, funct7):
  '''
  R-type instruction are encoded as the following:

  bit[6:0] = opcode
  bit[11:7] = destination register (rd)
  bit[14:12] = function field 3
  bit[19:15] = source register 1 (rs1)
  bit[24:20] = source register 2 (rs2)
  bit[31:25] = function field 7

  '''
  # Shift the value to its starting bit postion, pad with zeroes 
  rd = rd << 7   # rd = rd_000_0000
  funct3 = funct3 << 12
  rs1 = rs1 << 15
  rs2 = rs2 << 20
  funct7 = funct7 << 25
  
  return op | rd | funct3 | rs1 | rs2 | funct7



def encode_I_type(op, rd, rs1, funct3, imm):
  '''
  I-type instruction are encoded as the following:
  
  bit[6:0] = opcode
  bit[11:7] = destination register (rd)
  bit[14:12] = function field 3
  bit[19:15] = source register 1 (rs1)
  bit[31:20] = Immediate

  '''
  
  # Sign extend immediate to 12 bits
  imm = sign_extend(imm, 12)


  # If instruction is srai, imm[10] should be set
  if op == 19 and funct3 == 5:
    imm = imm | 1 << 10
  

  rd = rd << 7  
  funct3 = funct3 << 12
  rs1 = rs1 << 15
  imm = imm << 20
  


  return op | rd | funct3 | rs1 | imm




def encode_S_type():
  ... 

def encode_B_type():
  ... 

def encode_U_type():
  ... 

def encode_J_type():
  ... 


  

